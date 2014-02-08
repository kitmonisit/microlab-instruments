#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: base_classes
   :synopsis: Defines the base classes from which all instruments are derived.
"""

import aardvark_py as aapy
import gpib
import serial
import socket
from random import randint
from array import array
from struct import unpack

class Instrument(object):
    def _is_little_endian(self):
        """Returns ``True`` if the most significant bit as at the right,
        ``False`` if the most significant bit is at the left.
        """
        return self.ask_ascii(self.DATA['get_byte_order']) == self.DATA['byte_order_little']

    def _get_expected_bytes(self):
        """Used by methods that expect fixed-length binary or IEEE-754 data.
        The format of such a response is::

        #<number of decimal digits to represent size><size in bytes of payload>

        For example, the expected data payload is 1 byte long.  The beginning
        of the response stream will look like this::

        #11

        If the expected data payload is 1097 bytes long, then the beginning of
        the response stream will look like this::

        #41097
        """
        # Read number of decimal digits to represent expected data size
        s = self.read(2)
        size_length = int(s[1])

        # Read expected data size in bytes.  The ``expected_size`` is increased
        # by 1 to include the terminating newline character.
        s = self.read(size_length)
        expected_size = int(s) + 1
        return expected_size

    def read_ascii(self, bufsize=4096):
        """Read ASCII response from instrument in chunks of ``bufsize`` bytes
        until a ``\\n`` is encountered.

        :param int bufsize:
            Defaults to 4096 bytes.  Size of consecutive chunks of data to be read.

        :returns out:
            Response from the instrument.
        :rtype: str
        """
        stream = []
        while True:
            s = self.read(bufsize)
            stream.append(s)
            if '\n' in s:
                break
        out = ''.join(stream)
        return out

    def read_binary(self):
        """Read raw binary data from instrument.  It is the developer's
        responsiblity to make sense of it.

        :returns out:
            Response from the instrument.  This is just a string of binary
            code.
        :rtype: str

        A typical use case is obtaining a screenshot of the instrument panel.
        The following code is for the Agilent B2902A Precision Source Measure
        Unit, nicknamed 'Yveltal'.

        .. code-block:: python

            import microlab_instruments as mi

            yveltal = mi.Yveltal()
            yveltal.write(':DISP:ENAB ON')
            yveltal.write(':DISP:VIEW GRAP')
            yveltal.write(':HCOP:SDUM:FORM JPG')
            yveltal.ask_ascii('*OPC?')
            yveltal.write(':HCOP:SDUM:DATA?')
            image_data = yveltal.read_binary()

            file_handle = open('screendump.jpg', 'wb')
            file_handle.write(image_data)
            file_handle.close()
        """
        expected_size = self._get_expected_bytes()

        # Read actual data
        stream = []
        while sum(map(len, stream)) < expected_size:
            s = self.read(expected_size)
            stream.append(s)
        out = ''.join(stream)
        return out

    def read_ieee754(self):
        """A convenience function to read binary data known to be formatted in
        IEEE-754 floating-point.  Internally calls :meth:`.read_binary` and
        automatically determines half-, single-, or double-precision based on
        the instrument's settings.

        :returns out:
            A list of floating-point numbers.
        :rtype: list
        """
        # Read actual data
        # and discard the newline character
        stream = self.read_binary()[:-1]

        # Convert floating-point to Python ``float``
        # single- or double-precision
        if self.DATA['nickname'] in \
                ('genesect',
                 'giratina',
                 'yveltal'):

            # Calculate number of floating point data points
            precision = self.ask_ascii(self.DATA['get_data_format'])

            # one single-precision number is 4 bytes
            if precision == self.DATA['data_format_single']:
                num_bytes = 4
            # one double-precision number is 8 bytes
            elif precision == self.DATA['data_format_double']:
                num_bytes = 8
            n = len(stream)*8/num_bytes

            # Get byte order
            b = '<' if self._is_little_endian() else '>'

            # Convert the binary data to Python ``float``s
            fmt = '{0}{1}f'.format(b, n)
            out = list(unpack(fmt, stream))
            return out
        # half-precision
        elif self.DATA['nickname'] in \
                ('deoxys',):
            # Chop the stream into 16-bit elements
            stream = [w for w in self._chop16(stream)]

            # Convert the stream into ``float``\ s
            out = map(self._half_to_float, stream)
            return out

    def ask_ascii(self, scpi_string):
        """A convenience function for calling :meth:`.write` and
        :meth:`.read_ascii` consecutively.

        :param str scpi_string:
            A valid SCPI query command. See the instrument's SCPI command reference.
        """
        if scpi_string.strip()[-1] != '?':
            raise Exception, 'The scpi_string argument for ask_* functions must be a query, i.e. end with a ?'
        self.write(scpi_string)
        self.write('*OPC')
        return self.read_ascii()

    def ask_binary(self, scpi_string):
        """A convenience function for calling :meth:`.write` and
        :meth:`.read_binary` consecutively.

        :param str scpi_string:
            A valid SCPI query command. See the instrument's SCPI command reference.
        """
        if scpi_string.strip()[-1] != '?':
            raise Exception, 'The scpi_string argument for ask_* functions must be a query, i.e. end with a ?'
        self.write(scpi_string)
        self.write('*OPC')
        return self.read_binary()

    def ask_ieee754(self, scpi_string):
        """A convenience function for calling :meth:`.write` and
        :meth:`.read_ieee754` consecutively.

        :param str scpi_string:
            A valid SCPI query command. See the instrument's SCPI command reference.
        """
        if scpi_string.strip()[-1] != '?':
            raise Exception, 'The scpi_string argument for ask_* functions must be a query, i.e. end with a ?'
        self.write(scpi_string)
        self.write('*OPC')
        return self.read_ieee754()


class AardvarkInstrument(object):

    #: These are the status codes used by :meth:`.i2c_write`\ ,
    #: :meth:`.i2c_read`\ , and :meth:`.i2c_write_read` when raising
    #: Exceptions.
    I2C_STATUS_CODES = {
        1 : 'AA_I2C_STATUS_BUS_ERROR',
        2 : 'AA_I2C_STATUS_SLA_ACK',
        3 : 'AA_I2C_STATUS_SLA_NACK',
        4 : 'AA_I2C_STATUS_DATA_NACK',
        5 : 'AA_I2C_STATUS_ARB_LOST',
        6 : 'AA_I2C_STATUS_BUS_LOCKED',
        7 : 'AA_I2C_STATUS_LAST_DATA_ACK',
        }

    def __init__(self):
        """Initialize an Aardvark.

        :raises Exception:
            Upon instantiation, SPI communication is tested. A
            25-long *array* of bytes is sent twice to the Aardvark (and
            subsequently to the FPGA).  After the second attempt, a response
            identical to the *array* must be received.  If not, an Exception is
            raised.  In this case, it may be likely that the FPGA did not respond
            properly.
        """
        port = aapy.aa_find_devices(1)[1][0]
        self.__device = aapy.aa_open(port)
        if self.__device <= 0:
            raise Exception, 'Aardvark not accessible'
        # General configuration
        aapy.aa_target_power(self.__device, aapy.AA_TARGET_POWER_NONE)
        aapy.aa_configure(self.__device, aapy.AA_CONFIG_SPI_I2C)

        # I2C configuration
        aapy.aa_i2c_pullup(self.__device, aapy.AA_I2C_PULLUP_BOTH)

        # SPI configuration
        aapy.aa_spi_bitrate(self.__device, 1000)
        aapy.aa_spi_configure(self.__device, aapy.AA_SPI_POL_RISING_FALLING, aapy.AA_SPI_PHASE_SAMPLE_SETUP, aapy.AA_SPI_BITORDER_MSB)
        self.__spi_test()

    def __del__(self):
        aapy.aa_close(self.__device)

    def __spi_test(self):
        TEST_MESSAGE = array('B', [randint(0x00, 0xFF) for n in range(25)])
        self.spi_write(TEST_MESSAGE)
        TEST_RESPONSE = self.spi_write(array('B', [0]*25))
        aa = map(hex, TEST_MESSAGE)
        bb = map(hex, TEST_RESPONSE)
        for match in zip(aa, bb):
            print match
        if TEST_MESSAGE == TEST_RESPONSE:
            print 'SPI communication OK'
        else:
            raise Exception, 'SPI communication not working'

    def i2c_write(self, address, bytecode):
        """Write ``bytecode`` to the Aardvark output to be received by I2C
        slave with ``address``.

        :param int address:
            Slave address to receive ``bytecode``.  Limited to 8 bits.
        :param int bytecode:
            Raw bytecode to send.  Limited to 8 bits.

        :returns out:
            Number of bytes sent.
        :rtype: int

        :raises Exception: if the status response is not 0. See :attr:`.I2C_STATUS_CODES`.
        """
        xout = aapy.array_u08(1)
        xout[0] = bytecode
        status, bytes_sent = aapy.aa_i2c_write_ext(self.__device, address, aapy.AA_I2C_NO_FLAGS, xout)
        if status == 0:
            out = bytes_sent
            return out
        else:
            raise Exception, self.I2C_STATUS_CODES[status]

    def i2c_read(self, address, bufsize):
        """Read ``bufsize`` number of bytes from the I2C slave with ``address``.

        :param int address:
            Slave address from which to receive response.
        :param int bufsize:
            Size in bytes of expected response from slave.

        :returns out:
            Response from slave.  A ``bufsize``\ -length *list* of *int*\ s.
        :rtype: list

        :raises Exception: if the status response is not 0. See :attr:`.I2C_STATUS_CODES`.
        """
        xin = aapy.array_u08(bufsize)
        status, data_recv, bytes_recv = aapy.aa_i2c_read_ext(self.__device, address, aapy.AA_I2C_NO_FLAGS, xin)
        if status == 0:
            out = xin
            return out
        else:
            raise Exception, self.I2C_STATUS_CODES[status]

    def i2c_write_read(self, address, bytecode, bufsize):
        """Write ``bytecode`` to, and read ``bufsize`` bytes from, I2C slave
        with ``address`` in one fell swoop!

        :param int address:
            Slave address to receive ``bytecode``.  Limited to 8 bits.
        :param int bytecode:
            Raw bytecode to send.  Limited to 8 bits.
        :param int bufsize:
            Size in bytes of expected response from slave.

        :returns out:
            Response from slave.  A ``bufsize``-length *list* of *int*\ s.
        :rtype: list

        :raises Exception: if the status response is not 0. See :attr:`.I2C_STATUS_CODES`.
        """
        xout = aapy.array_u08(1)
        xout[0] = bytecode
        xin = aapy.array_u08(bufsize)
        status, bytes_sent, data_recv, bytes_recv = aapy.aa_i2c_write_read(self.__device, address, aapy.AA_I2C_NO_FLAGS, xout, xin)
        if status == 0:
            out = xin
            return out
        else:
            raise Exception, self.I2C_STATUS_CODES[status]

    def spi_write(self, bytecode):
        """Write ``bytecode`` to, and read 25 bytes from, the SPI
        channel in one fell swoop!

        :param list bytecode:
            Raw bytecodes to send.  Must be exactly 25-long *list* of bytes.

        :returns out:
            Response bytes.  A 25-length *list* of *int*\ s.
        :rtype: list

        :raises Exception: if ``bytecode`` does not have exactly 25 8-bit elements.
        """
        if isinstance(bytecode, list):
            bits = [b.bit_length() for b in bytecode]
            if all([length <= 8 for length in bits]):
                xout = array('B', bytecode)
            else:
                raise Exception, 'bytecode must be a 25-long array of bytes'
        elif isinstance(bytecode, array) and bytecode.typecode == 'B':
            xout = bytecode
        else:
            raise Exception, 'bytecode must be a 25-long array of bytes'
        xin = aapy.array_u08(25)
        bytes_sent, data_recv = aapy.aa_spi_write(self.__device, xout, xin)
        out = xin
        return out


class GPIBInstrument(Instrument):
    def __init__(self, nickname):
        """Initialize a GPIB instrument

        :param str nickname:
            A nickname associated with a GPIB primary address and defined in
            ``/etc/gpib.conf``.
        """
        self.__device = gpib.find(nickname)
        self.reset()

    def __del__(self):
        """Close the GPIB conection.
        """
        gpib.close(self.__device)

    def reset(self):
        """Reset the GPIB instrument.
        """
        gpib.clear(self.__device)

    def write(self, scpi_string):
        """Write SCPI command to the instrument.  The end-of-string character
        (for example, ``\\n``) is automatically appended.

        :param str scpi_string:
            A valid SCPI command. See the instrument's SCPI command reference.
        """
        s = ''.join([scpi_string, '\n'])
        return gpib.write(self._device, s)

    def read(self, bufsize=4096):
        """Read ``bufsize`` bytes from instrument.  Using this low-level
        function, there is no way to ensure that all the response data has been
        retrieved, or to make sense of binary data.  It is strongly recommended
        to use :meth:`.read_ascii`\ , :meth:`.read_binary`\ , or
        :meth:`.read_ieee754`\ .

        :param int bufsize:
            Defaults to 4096 bytes.  Expected size in bytes of the response
            from the instrument.

        :returns out:
            Response from the instrument.
        :rtype: str
        """
        return gpib.read(self._device, bufsize)


class TCPIPInstrument(Instrument):
    def __init__(self, socket_pair):
        """Initialize TCP/IP instrument.

        :param tuple socket_pair:
            A 2-tuple of the form ``('192.168.1.2', 5025)``.
        """
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect(socket_pair)
        self._socket.settimeout(30)
        self.reset()

    def __del__(self):
        """Close the socket connection properly.
        """
        self._socket.shutdown(socket.SHUT_RDWR)
        self._socket.close()

    def reset(self):
        """Reset the instrument.
        """
        self.write('*CLS')
        self.write('*RST')

    def write(self, scpi_string):
        """Write SCPI command to the instrument.  The end-of-string character
        (for example, ``\\n``) is automatically appended.

        :param str scpi_string:
            A valid SCPI command. See the instrument's SCPI command reference.
        """
        s = ''.join([scpi_string, '\n'])
        return self._socket.send(s)

    def read(self, bufsize=4096):
        """Read ``bufsize`` bytes from instrument.  Using this low-level
        function, there is no way to ensure that all the response data has been
        retrieved, or to make sense of binary data.  It is strongly recommended
        to use :meth:`.read_ascii`\ , :meth:`.read_binary`\ , or
        :meth:`.read_ieee754`\ .

        :param int bufsize:
            Defaults to 4096 bytes.  Expected size in bytes of the response
            from the instrument.

        :returns out:
            Response from the instrument.
        :rtype: str
        """
        return self._socket.recv(bufsize)


class SerialInstrument(Instrument):
    def __init__(self, device_port):
        """Initialize an RS-232 instrument.
        """
        self.__serial = serial.Serial(device_port)

    def __del__(self):
        self.__serial.close()

