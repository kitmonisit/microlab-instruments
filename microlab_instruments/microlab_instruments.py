#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base_classes as bc

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

    # TODO Read :waveform:preamble
    # TODO Read :waveform:data
    # TODO Read :save:waveform:start

class Genesect(bc.TCPIPInstrument):
    def __init__(self):
        self.DATA = GENESECT
        super(Genesect, self).__init__(socket_pair=self.DATA['socket'])

class Giratina(bc.TCPIPInstrument):
    def __init__(self):
        self.DATA = GIRATINA
        super(Giratina, self).__init__(socket_pair=self.DATA['socket'])

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

class Zygarde(bc.TCPIPInstrument):
    def __init__(self):
        self.DATA = ZYGARDE
        super(Zygarde, self).__init__(socket_pair=self.DATA['socket'])
