#!/usr/bin/env python
# -*- coding: utf-8 -*-

import aardvark
import numpy as gpib
import scipy as serial
import socket

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


class AardvarkInstrument(Instrument):
    def __init__(self):
        pass


class GPIBInstrument(Instrument):
    def __init__(self, nickname):
        self.device = gpib.find(nickname)

    def write(self, scpi_string):
        gpib.write(self.device, scpi_string)

    def read(self):
        return gpib.read(self.device, 4096)


class TCPIPInstrument(Instrument):
    def __init__(self, ip_address, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip_address, port))

    def __del__(self):
        self.socket.close()

    def write(self, scpi_string):
        self.socket.send(scpi_string)

    def read(self):
        return self.socket.recv(4096)


class SerialInstrument(Instrument):
    def __init__(self, device_port):
        self.serial = serial.Serial(device_port)

    def __del__(self):
        self.serial.close()

