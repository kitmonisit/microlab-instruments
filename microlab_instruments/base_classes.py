#!/usr/bin/env python
# -*- coding: utf-8 -*-

import aardvark_py as aapy
import gpib
import serial
import socket
from random import randint
from array import array

class Instrument(object):
    def __init__(self):
        pass

    def write(self):
        pass

    def read(self):
        pass

    def ask(self, scpi_string):
        self.write(scpi_string)
        return self.read()


class AardvarkInstrument(object):
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
        TEST_RESPONSE = self.spi_write(TEST_MESSAGE)
        aa = map(hex, TEST_MESSAGE)
        bb = map(hex, TEST_RESPONSE)
        for match in zip(aa, bb):
            print match
        if TEST_MESSAGE == TEST_RESPONSE:
            print 'SPI communication OK'
        else:
            raise Exception, 'SPI communication not working'

    def i2c_write(self, address, bytecode):
        """Write `bytecode` to the Aardvark output to be received by I2C
        slave with `address`.

        Parameters
        ----------
        address : int
            Slave address to receive `bytecode`.  Limited to 8 bits.
        bytecode : int
            Raw bytecode to send.  Limited to 8 bits.

        Returns
        -------
        bytes_sent : int
            Number of bytes sent.
        """
        xout = aapy.array_u08(1)
        xout[0] = bytecode
        status, bytes_sent = aapy.aa_i2c_write_ext(self.__device, address, aapy.AA_I2C_NO_FLAGS, xout)
        if status == 0:
            return bytes_sent
        else:
            raise Exception, self.I2C_STATUS_CODES[status]

    def i2c_read(self, address, bufsize):
        """Read `bufsize` number of bytes from the I2C slave with `address`.

        Parameters
        ----------
        address : int
            Slave address to receive `bytecode`.  Limited to 8 bits.
        bufsize : int
            Size in bytes of expected response from slave.

        Returns
        -------
        out : array
            A `bufsize`-length array of `int`s.
        """
        xin = aapy.array_u08(bufsize)
        status, data_recv, bytes_recv = aapy.aa_i2c_read_ext(self.__device, address, aapy.AA_I2C_NO_FLAGS, xin)
        if status == 0:
            out = xin
            return out
        else:
            raise Exception, self.I2C_STATUS_CODES[status]

    def i2c_write_read(self, address, bytecode, bufsize):
        """Write `bytecode` to, and read `bufsize` bytes from, I2C slave
        with `address` in one fell swoop!

        Parameters
        ----------
        address : int
            Slave address to receive `bytecode`.  Limited to 8 bits.
        bytecode : int
            Raw bytecode to send.  Limited to 8 bits.
        bufsize : int
            Size in bytes of expected response from slave.

        Returns
        -------
        out : array
            Response from slave.  A `bufsize`-length array of `int`s.
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
        """Write `bytecode` to, and read 25 bytes from, the SPI
        channel in one fell swoop!

        Parameters
        ----------
        bytecode : array
            Raw bytecodes to send.  Must be exactly 25-long array of bytes.

        Returns
        -------
        out : array
            Response byte.  A 1-length array of `int`.
        """
        if isinstance(bytecode, array):
            xout = bytecode
        elif isinstance(bytecode, list):
            xout = array('B', bytecode)
        else:
            raise Exception, 'bytecode must be a 25-long array of bytes'
        xin = aapy.array_u08(25)
        bytes_sent, data_recv = aapy.aa_spi_write(self.__device, xout, xin)
        out = xin
        return out


class GPIBInstrument(Instrument):
    def __init__(self, nickname):
        self.__device = gpib.find(nickname)
        self.clear()

    def __del__(self):
        gpib.close(self.__device)

    def clear(self):
        gpib.clear(self.__device)

    def write(self, scpi_string):
        gpib.write(self.__device, scpi_string + '\n')

    def read(self):
        return gpib.read(self.__device, 4096)


class TCPIPInstrument(Instrument):
    def __init__(self, socket_pair):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect(socket_pair)
        self.reset()

    def __del__(self):
        self.__socket.close()

    def reset(self):
        self.write('*RST')

    def write(self, scpi_string):
        self.__socket.send(scpi_string + '\n')

    def read(self):
        return self.__socket.recv(4096)


class SerialInstrument(Instrument):
    def __init__(self, device_port):
        self.__serial = serial.Serial(device_port)

    def __del__(self):
        self.__serial.close()

