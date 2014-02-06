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
    def ask(self, scpi_string):
        """Just the same as calling :meth:`.write` and :meth:`.read`
        consecutively.  See the methods implemented in the subclass for
        details.
        """
        self.write(scpi_string)
        return self.read()

    def ask_binary(self, scpi_string):
        """Just the same as calling :meth:`.write` and :meth:`.read_binary`
        consecutively.  See the methods implemented in the subclass for
        details.
        """
        self.write(scpi_string)
        return self.read_binary()


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

        :raises Exception: Upon instantiation, SPI communication is tested. A
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
        gpib.write(self.__device, scpi_string + '\n')

    def read(self, bufsize=4096):
        """Read ``bufsize`` bytes from GPIB instrument.

        :param int bufsize:
            Defaults to 4096 bytes.  Expected size in bytes of the response
            from the instrument.

        :returns out:
            Response from the instrument.
        :rtype: str
        """
        out = gpib.read(self.__device, bufsize)
        return out


class TCPIPInstrument(Instrument):
    def __init__(self, socket_pair):
        """Initialize TCP/IP instrument.

        :param tuple socket_pair:
            A 2-tuple of the form ``('192.168.1.2', 5025)``.
        """
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect(socket_pair)
        self.__socket.settimeout(30)
        self.reset()

    def __del__(self):
        self.__socket.shutdown(socket.SHUT_RDWR)
        self.__socket.close()

    def __get_expected_bytes(self):
        """Used by methods that expect fixed-length binary or IEEE-754 data.
        The format of such a response is

        #<number of decimal digits to represent size><size in bytes of payload>

        For example, the expected data payload is 1 byte long.  The beginning
        of the response stream will look like this:

        #11

        If the expected data payload is 1097 bytes long, then the beginning of
        the response stream will look like this:

        #41097

        The ``expected_size`` is increased by 1 to include the terminating
        newline character.
        """
        # Read number of decimal digits to represent expected data size
        s = self.__socket.recv(2)
        size_length = int(s[1])

        # Read expected data size in bytes
        s = self.__socket.recv(size_length)
        expected_size = int(s) + 1
        return expected_size

    def __is_little_endian(self):
        """Returns ``True`` if the most significant bit as at the right,
        ``False`` if the most significant bit is at the left.
        """
        # TODO ':format:border' may not be the correct SCPI command for all
        # instruments Move this method to the corresponding instrument
        # subclass.
        return self.ask(':format:border?') == 'NORM'

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

        :returns out:
            The number of bytes sent
        :rtype int:
        """
        out = self.__socket.send(scpi_string + '\n')
        return out

    def read(self, bufsize=4096):
        """Read ``bufsize`` bytes from instrument.  Use this method when you
        are expecting an ASCII response terminated by ``\\n``.

        :param int bufsize:
            Defaults to 4096 bytes. Expected size in bytes of the response from
            the instrument.

        :returns out:
            ASCII response from the instrument.
        :rtype: str
        """
        out = ''
        while '\n' not in out:
            out += self.__socket.recv(bufsize)
        return out

    def read_binary(self):
        """Read raw binary data from instrument.

        :returns out:
            Response from the instrument.
        :rtype: str
        """
        expected_size = self.__get_expected_bytes()

        # Read actual data
        out = ''
        while len(out) < expected_size:
            out += self.__socket.recv(expected_size)
        return out

    def read_single(self):
        """Read IEEE-754 single-precision data from instrument.

        :returns out:
            A list of floating-point numbers.
        :rtype: list
        """
        expected_size = self.__get_expected_bytes()

        # Read actual data
        out = ''
        while len(out) < expected_size:
            out += self.__socket.recv(expected_size)

        # Discard the newline character
        out = out[:-1]

        # Calculate number of floating point data points
        # 1 single-precision number is 4 bytes
        n = (expected_size - 1)/4

        # Get byte order
        b = '<' if self.__is_little_endian() else '>'

        # Convert the binary data to Python ``float``s
        fmt = '{0}{1}f'.format(b, n)
        out = list(unpack(fmt, out))
        return out

    def read_double(self):
        """Read IEEE-754 double-precision data from instrument.

        :returns out:
            A list of floating-point numbers.
        :rtype: list
        """
        expected_size = self.__get_expected_bytes()

        # Read actual data
        out = ''
        while len(out) < expected_size:
            out += self.__socket.recv(expected_size)

        # Discard the newline character
        out = out[:-1]

        # Calculate number of floating point data points
        # 1 double-precision number is 8 bytes
        n = (expected_size - 1)/8

        # Get byte order
        b = '<' if self.__is_little_endian() else '>'

        # Convert the binary data to Python ``float``s
        fmt = '{0}{1}f'.format(b, n)
        out = list(unpack(fmt, out))
        return out


class SerialInstrument(Instrument):
    def __init__(self, device_port):
        """Initialize an RS-232 instrument.
        """
        self.__serial = serial.Serial(device_port)

    def __del__(self):
        self.__serial.close()

