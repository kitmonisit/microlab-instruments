#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base_classes as bc

# GPIB Instruments
ARCEUS   = {
    'name'         : 'Agilent 8753ES S-Parameter Network Analyzer',
    'gpib_nickname': 'arceus'
    }
MELOETTA = {
    'name'         : 'Hewlett-Packard 6623A System DC Power Supply',
    'gpib_nickname': 'meloetta'
    }
XERNEAS  = {
    'name'         : 'Hewlett-Packard 4156A Precision Semiconductor Parameter Analyzer',
    'gpib_nickname': 'xerneas'
    }

# TCPIP Instruments
DARKRAI  = {
    'name'  : 'Agilent N9020A MXA Signal Analyzer',
    'socket': ('192.168.1.5', 5025),
    }
DEOXYS   = {
    'name'  : 'Agilent InfiniiVision MSO7104A Mixed Signal Oscilloscope',
    'socket': ('192.168.1.10', 5025),
    }
GENESECT = {
    'name'  : 'Agilent B2962A Power Source',
    'socket': ('192.168.1.9', 5025),
    }
GIRATINA = {
    'name'  : 'Agilent B2962A Power Source',
    'socket': ('192.168.1.8', 5025),
    }
HEATRAN  = {
    'name'  : 'Agilent 16803A Logic Analyzer',
    'socket': ('192.168.1.11', 5025),
    }
HO_OH    = {
    'name'  : 'Agilent N5182A MXG Vector Signal Generator',
    'socket': ('192.168.1.4', 5025),
    }
KYUREM   = {
    'name'  : 'Agilent N5183A MXG Analog Signal Generator',
    'socket': ('192.168.1.3', 5025),
    }
RAYQUAZA = {
    'name'  : 'Agilent E4443A PSA Series Spectrum Analyzer',
    'socket': ('192.168.1.2', 5025),
    }
YVELTAL  = {
    'name'  : 'Agilent B2902A Precision Source/Measure Unit',
    'socket': ('192.168.1.7', 5025),
    }
ZYGARDE  = {
    'name'  : 'Agilent E5071C ENA Series Network Analyzer',
    'socket': ('192.168.1.6', 5025),
    }

class Arceus(bc.GPIBInstrument):
    def __init__(self):
        super(Arceus, self).__init__(nickname=ARCEUS['gpib_nickname'])

class Meloetta(bc.GPIBInstrument):
    def __init__(self):
        super(Meloetta, self).__init__(nickname=MELOETTA['gpib_nickname'])

class Xerneas(bc.GPIBInstrument):
    def __init__(self):
        super(Xerneas, self).__init__(nickname=XERNEAS['gpib_nickname'])

class Darkrai(bc.TCPIPInstrument):
    def __init__(self):
        super(Darkrai, self).__init__(socket_pair=DARKRAI['socket'])

class Deoxys(bc.TCPIPInstrument):
    def __init__(self):
        super(Deoxys, self).__init__(socket_pair=DEOXYS['socket'])

class Genesect(bc.TCPIPInstrument):
    def __init__(self):
        super(Genesect, self).__init__(socket_pair=GENESECT['socket'])

class Giratina(bc.TCPIPInstrument):
    def __init__(self):
        super(Giratina, self).__init__(socket_pair=GIRATINA['socket'])

class Heatran(bc.TCPIPInstrument):
    def __init__(self):
        super(Heatran, self).__init__(socket_pair=HEATRAN['socket'])

class Ho_oh(bc.TCPIPInstrument):
    def __init__(self):
        super(Ho_oh, self).__init__(socket_pair=HO_OH['socket'])

class Kyurem(bc.TCPIPInstrument):
    def __init__(self):
        super(Kyurem, self).__init__(socket_pair=KYUREM['socket'])

class Rayquaza(bc.TCPIPInstrument):
    def __init__(self):
        super(Rayquaza, self).__init__(socket_pair=RAYQUAZA['socket'])

class Yveltal(bc.TCPIPInstrument):
    def __init__(self):
        super(Yveltal, self).__init__(socket_pair=YVELTAL['socket'])

class Zygarde(bc.TCPIPInstrument):
    def __init__(self):
        super(Zygarde, self).__init__(socket_pair=ZYGARDE['socket'])
