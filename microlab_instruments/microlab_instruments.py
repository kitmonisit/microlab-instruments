#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base_classes as bc
from struct import unpack

# GPIB Instruments
ARCEUS   = {
    'gpib_nickname'    : 'arceus',
    'name'             : 'Agilent 8753ES S-Parameter Network Analyzer',
    'get_byte_order'   : '',
    'byte_order_little': '',
    }
MELOETTA = {
    'gpib_nickname'    : 'meloetta',
    'name'             : 'Hewlett-Packard 6623A System DC Power Supply',
    'get_byte_order'   : '',
    'byte_order_little': '',
    }
XERNEAS  = {
    'gpib_nickname'    : 'xerneas',
    'name'             : 'Hewlett-Packard 4156A Precision Semiconductor Parameter Analyzer',
    'get_byte_order'   : '',
    'byte_order_little': '',
    }

# TCPIP Instruments
DARKRAI  = {
    'nickname'         : 'darkrai',
    'name'             : 'Agilent N9020A MXA Signal Analyzer',
    'socket'           : ('192.168.1.5', 5025),
    'get_byte_order'   : '',
    'byte_order_little': '',
    }
DEOXYS   = {
    'nickname'         : 'deoxys',
    'name'             : 'Agilent InfiniiVision MSO7104A Mixed Signal Oscilloscope',
    'socket'           : ('192.168.1.10', 5025),
    'get_byte_order'   : ':waveform:byteorder?',
    'byte_order_little': 'LSBF',
    }
GENESECT = {
    'nickname'         : 'genesect',
    'name'             : 'Agilent B2962A Power Source',
    'socket'           : ('192.168.1.9', 5025),
    'get_byte_order'   : ':format:border?',
    'byte_order_little': 'NORM',
    }
GIRATINA = {
    'nickname'         : 'giratina',
    'name'             : 'Agilent B2962A Power Source',
    'socket'           : ('192.168.1.8', 5025),
    'get_byte_order'   : ':format:border?',
    'byte_order_little': 'NORM',
    }
HEATRAN  = {
    'nickname'         : 'heatran',
    'name'             : 'Agilent 16803A Logic Analyzer',
    'socket'           : ('192.168.1.11', 5025),
    'get_byte_order'   : '',
    'byte_order_little': '',
    }
HO_OH    = {
    'nickname'         : 'ho_oh',
    'name'             : 'Agilent N5182A MXG Vector Signal Generator',
    'socket'           : ('192.168.1.4', 5025),
    'get_byte_order'   : '',
    'byte_order_little': '',
    }
KYUREM   = {
    'nickname'         : 'kyurem',
    'name'             : 'Agilent N5183A MXG Analog Signal Generator',
    'socket'           : ('192.168.1.3', 5025),
    'get_byte_order'   : '',
    'byte_order_little': '',
    }
RAYQUAZA = {
    'nickname'         : 'rayquaza',
    'name'             : 'Agilent E4443A PSA Series Spectrum Analyzer',
    'socket'           : ('192.168.1.2', 5025),
    'get_byte_order'   : '',
    'byte_order_little': '',
    }
YVELTAL  = {
    'nickname'         : 'yveltal',
    'name'             : 'Agilent B2902A Precision Source/Measure Unit',
    'socket'           : ('192.168.1.7', 5025),
    'get_byte_order'   : ':format:border?',
    'byte_order_little': 'NORM',
    }
ZYGARDE  = {
    'nickname'         : 'zygarde',
    'name'             : 'Agilent E5071C ENA Series Network Analyzer',
    'socket'           : ('192.168.1.6', 5025),
    'get_byte_order'   : '',
    'byte_order_little': '',
    }



class Arceus(bc.GPIBInstrument):
    def __init__(self):
        self.DATA = ARCEUS
        super(Arceus, self).__init__(nickname=self.DATA['gpib_nickname'])

class Meloetta(bc.GPIBInstrument):
    def __init__(self):
        self.DATA = MELOETTA
        super(Meloetta, self).__init__(nickname=self.DATA['gpib_nickname'])

class Xerneas(bc.GPIBInstrument):
    def __init__(self):
        self.DATA = XERNEAS
        super(Xerneas, self).__init__(nickname=self.DATA['gpib_nickname'])

class Darkrai(bc.TCPIPInstrument):
    def __init__(self):
        self.DATA = DARKRAI
        super(Darkrai, self).__init__(socket_pair=self.DATA['socket'])

class Deoxys(bc.TCPIPInstrument):
    def __init__(self):
        self.DATA = DEOXYS
        super(Deoxys, self).__init__(socket_pair=self.DATA['socket'])
        self.write(':waveform:byteorder msbfirst')
        self.write(':waveform:format word')
        self.write('*OPC')

    # TODO Read :waveform:preamble
    #           format WORD
    #           type   :waveform:type?
    #           points :waveform:points? can be found in the header of :waveform:data?
    #           count  :acquire:count? averaging for one data point, etc
    #           xincrement
    #           xorigin
    #           xreference
    #           yincrement
    #           yorigin
    #           yreference

    def read_ieee754(self):
        """Read IEEE-754 floating-point data from instrument.

        :returns out:
            A two-column list of floating-point numbers, where the first column
            contains the X values and the second column contains the Y values.
        :rtype: list
        """
        # TODO Read :waveform:data
        #           :waveform:byteorder DONE
        #           :waveform:unsigned  DONE
        #           :waveform:format    DONE
        #           :waveform:source    channel | function | math | pod | bus | sbus
        #           0x0000 hole
        #           0x0001 clipped low
        #           0xFFFF clipped high

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
        # TODO Need to adjust these for special values (clipped, etc)
        # TODO Need to adjust these according to preamble
        # TODO Need to compose X and Y values
        return out
    # TODO Read :save:waveform:start

class Genesect(bc.TCPIPInstrument):
    def __init__(self):
        self.DATA = GENESECT
        super(Genesect, self).__init__(socket_pair=self.DATA['socket'])
        self.write(':format:data real,32')
        self.write('*OPC')

    def read_ieee754(self):
        """Read IEEE-754 floating-point data from instrument.

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
        precision = self.ask(':format:data?')
        if precision == 'REAL,32':
            num_bytes = 4
        elif precision == 'REAL,64':
            num_bytes = 8
        n = (expected_size - 1)/num_bytes

        # Get byte order
        b = '<' if self.__is_little_endian() else '>'

        # Convert the binary data to Python ``float``s
        fmt = '{0}{1}f'.format(b, n)
        out = list(unpack(fmt, out))
        return out

class Giratina(bc.TCPIPInstrument):
    def __init__(self):
        self.DATA = GIRATINA
        super(Giratina, self).__init__(socket_pair=self.DATA['socket'])
        self.write(':format:data real,32')
        self.write('*OPC')

    def read_ieee754(self):
        """Read IEEE-754 floating-point data from instrument.

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
        precision = self.ask(':format:data?')
        if precision == 'REAL,32':
            num_bytes = 4
        elif precision == 'REAL,64':
            num_bytes = 8
        n = (expected_size - 1)/num_bytes

        # Get byte order
        b = '<' if self.__is_little_endian() else '>'

        # Convert the binary data to Python ``float``s
        fmt = '{0}{1}f'.format(b, n)
        out = list(unpack(fmt, out))
        return out

class Heatran(bc.TCPIPInstrument):
    def __init__(self):
        self.DATA = HEATRAN
        super(Heatran, self).__init__(socket_pair=self.DATA['socket'])

class Ho_oh(bc.TCPIPInstrument):
    def __init__(self):
        self.DATA = HO_OH
        super(Ho_oh, self).__init__(socket_pair=self.DATA['socket'])

class Kyurem(bc.TCPIPInstrument):
    def __init__(self):
        self.DATA = KYUREM
        super(Kyurem, self).__init__(socket_pair=self.DATA['socket'])

class Rayquaza(bc.TCPIPInstrument):
    def __init__(self):
        self.DATA = RAYQUAZA
        super(Rayquaza, self).__init__(socket_pair=self.DATA['socket'])

class Yveltal(bc.TCPIPInstrument):
    def __init__(self):
        self.DATA = YVELTAL
        super(Yveltal, self).__init__(socket_pair=self.DATA['socket'])
        self.write(':format:data real,32')
        self.write('*OPC')

    def read_ieee754(self):
        """Read IEEE-754 floating-point data from instrument.

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
        precision = self.ask(':format:data?')
        if precision == 'REAL,32':
            num_bytes = 4
        elif precision == 'REAL,64':
            num_bytes = 8
        n = (expected_size - 1)/num_bytes

        # Get byte order
        b = '<' if self.__is_little_endian() else '>'

        # Convert the binary data to Python ``float``s
        fmt = '{0}{1}f'.format(b, n)
        out = list(unpack(fmt, out))
        return out

class Zygarde(bc.TCPIPInstrument):
    def __init__(self):
        self.DATA = ZYGARDE
        super(Zygarde, self).__init__(socket_pair=self.DATA['socket'])
