#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Kristofer Monisit'
__email__ = 'kmonisit@gmail.com'
__version__ = '0.1.0'

import base_classes as bc
from base_classes import AardvarkInstrument

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
    'socket': ('', 5025),
    }
DEOXYS   = {
    'name'  : 'Agilent InfiniiVision MSO7104A Mixed Signal Oscilloscope',
    'socket': ('', 5025),
    }
GENESECT = {
    'name'  : 'Agilent B2962A Power Source',
    'socket': ('', 5025),
    }
GIRATINA = {
    'name'  : 'Agilent B2962A Power Source',
    'socket': ('', 5025),
    }
HEATRAN  = {
    'name'  : 'Agilent 16803A Logic Analyzer',
    'socket': ('', 5025),
    }
HO_OH    = {
    'name'  : 'Agilent N5182A MXG Vector Signal Generator',
    'socket': ('', 5025),
    }
KYUREM   = {
    'name'  : 'Agilent N5183A MXG Analog Signal Generator',
    'socket': ('10.158.6.30', 5025),
    }
RAYQUAZA = {
    'name'  : 'Agilent E4443A PSA Series Spectrum Analyzer',
    'socket': ('', 5025),
    }
YVELTAL  = {
    'name'  : 'Agilent B2902A Precision Source/Measure Unit',
    'socket': ('', 5025),
    }
ZYGARDE  = {
    'name'  : 'Agilent E5071C ENA Series Network Analyzer',
    'socket': ('', 5025),
    }

class Kyurem(bc.TCPIPInstrument):
    def __init__(self):
        super(Kyurem, self).__init__(socket_pair=KYUREM['socket'])
