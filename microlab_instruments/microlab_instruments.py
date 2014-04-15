#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base_classes as bc
from struct import pack, unpack

# I2C Instruments
CHEN     = {
    'nickname'          : 'chen',
    'name'              : 'I2C Mux Thing',
    'address'           : 0x70,
    }
TRAXEX   = {
    'nickname'          : 'traxex',
    'name'              : 'Sensirion STS21 Temperature Sensor',
    'address'           : 0x4A,
    'mux_address'       : 0x04,
    }
XIN      = {
    'nickname'          : 'xin',
    'name'              : 'Sensirion STS21 Temperature Sensor',
    'address'           : 0x4A,
    'mux_address'       : 0x05,
    }

# GPIB Instruments
ARCEUS   = {
    'nickname'          : 'arceus',
    'name'              : 'Agilent 8753ES S-Parameter Network Analyzer',
    'get_byte_order'    : '',
    'byte_order_little' : '',
    }
MELOETTA = {
    'nickname'          : 'meloetta',
    'name'              : 'Hewlett-Packard 6623A System DC Power Supply',
    'get_byte_order'    : '',
    'byte_order_little' : '',
    }
XERNEAS  = {
    'nickname'          : 'xerneas',
    'name'              : 'Hewlett-Packard 4156A Precision Semiconductor Parameter Analyzer',
    'get_byte_order'    : '',
    'byte_order_little' : '',
    }

# TCPIP Instruments
DARKRAI  = {
    'nickname'          : 'darkrai',
    'name'              : 'Agilent N9020A MXA Signal Analyzer',
    'socket'            : ('192.168.1.5', 5025),
    'get_byte_order'    : '',
    'byte_order_little' : '',
    }
DEOXYS   = {
    'nickname'          : 'deoxys',
    'name'              : 'Agilent InfiniiVision MSO7104A Mixed Signal Oscilloscope',
    'socket'            : ('192.168.1.10', 5025),
    'get_byte_order'    : ':waveform:byteorder?',
    'byte_order_little' : 'LSBF',
    }
GENESECT = {
    'nickname'          : 'genesect',
    'name'              : 'Agilent B2962A Power Source',
    'socket'            : ('192.168.1.9', 5025),
    'get_byte_order'    : ':format:border?',
    'byte_order_little' : 'NORM',
    'get_data_format'   : ':format:data?',
    'data_format_single': 'REAL,32',
    'data_format_double': 'REAL,64',
    }
GIRATINA = {
    'nickname'          : 'giratina',
    'name'              : 'Agilent B2962A Power Source',
    'socket'            : ('192.168.1.8', 5025),
    'get_byte_order'    : ':format:border?',
    'byte_order_little' : 'NORM',
    'get_data_format'   : ':format:data?',
    'data_format_single': 'REAL,32',
    'data_format_double': 'REAL,64',
    }
HEATRAN  = {
    'nickname'          : 'heatran',
    'name'              : 'Agilent 16803A Logic Analyzer',
    'socket'            : ('192.168.1.11', 5025),
    'get_byte_order'    : '',
    'byte_order_little' : '',
    }
HO_OH    = {
    'nickname'          : 'ho_oh',
    'name'              : 'Agilent N5182A MXG Vector Signal Generator',
    'socket'            : ('192.168.1.4', 5025),
    'get_byte_order'    : '',
    'byte_order_little' : '',
    }
KYUREM   = {
    'nickname'          : 'kyurem',
    'name'              : 'Agilent N5183A MXG Analog Signal Generator',
    'socket'            : ('192.168.1.3', 5025),
    'get_byte_order'    : '',
    'byte_order_little' : '',
    }
RAYQUAZA = {
    'nickname'          : 'rayquaza',
    'name'              : 'Agilent E4443A PSA Series Spectrum Analyzer',
    'socket'            : ('192.168.1.2', 5025),
    'get_byte_order'    : '',
    'byte_order_little' : '',
    }
YVELTAL  = {
    'nickname'          : 'yveltal',
    'name'              : 'Agilent B2902A Precision Source/Measure Unit',
    'socket'            : ('192.168.1.7', 5025),
    'get_byte_order'    : ':format:border?',
    'byte_order_little' : 'NORM',
    'get_data_format'   : ':format:data?',
    'data_format_single': 'REAL,32',
    'data_format_double': 'REAL,64',
    }
ZYGARDE  = {
    'nickname'          : 'zygarde',
    'name'              : 'Agilent E5071C ENA Series Network Analyzer',
    'socket'            : ('192.168.1.6', 5025),
    'get_byte_order'    : '',
    'byte_order_little' : '',
    }

class Chen(bc.I2CMuxInstrument):
    def __init__(self, aardvark):
        """Initialize the I2C multiplexer.

        :param Aardvark aardvark:
            An Aardvark object through which I2C commands are relayed.

        .. code-block:: python

            import microlab_instruments as mi

            aa = mi.Aardvark()
            chen = mi.Chen(aa)
        """
        self.DATA = CHEN
        super(Chen, self).__init__(aardvark=aardvark)


class Traxex(bc.TempSensorInstrument):
    def __init__(self, aardvark, mux):
        """Initialize a Sensirion STS21 temperature sensor.

        :param Aardvark aardvark:
            An Aardvark object through which I2C commands are relayed.

        .. code-block:: python

            import microlab_instruments as mi

            aa = mi.Aardvark()
            traxex = mi.Traxex(aa)
            print traxex.read_temp()
        """
        self.DATA = TRAXEX
        super(Traxex, self).__init__(aardvark=aardvark, mux=mux)


class Xin(bc.TempSensorInstrument):
    def __init__(self, aardvark, mux):
        """Initialize a Sensirion STS21 temperature sensor.

        :param Aardvark aardvark:
            An Aardvark object through which I2C commands are relayed.

        .. code-block:: python

            import microlab_instruments as mi

            aa = mi.Aardvark()
            xin = mi.Xin(aa)
            print xin.read_temp()
        """
        self.DATA = XIN
        super(Xin, self).__init__(aardvark=aardvark, mux=mux)


class Arceus(bc.GPIBInstrument):
    def __init__(self):
        self.DATA = ARCEUS
        super(Arceus, self).__init__(nickname=self.DATA['nickname'])


class Meloetta(bc.GPIBInstrument):
    def __init__(self):
        self.DATA = MELOETTA
        super(Meloetta, self).__init__(nickname=self.DATA['nickname'])


class Xerneas(bc.GPIBInstrument):
    def __init__(self):
        self.DATA = XERNEAS
        super(Xerneas, self).__init__(nickname=self.DATA['nickname'])


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

    def _chop16(self, s):
        """A generator that, given a string, yields its 16-bit slices.

        :param str s:
            The string to be chopped
        :returns out:
            A two-character (16-bit) string.
        :rtype: str
        """
        n = 0
        while True:
            k = s[n:n+2]
            if not k:
                break
            yield k
            n += 2

    def _half_to_float(self, half):
        """Converts half-precision floating-point (16-bit) binary data to
        Python ``float``\ .

        :param str half:
            A 16-bit string to be converted to a Python float
        :returns out:
            The actual floating point number represented by the 16-bit string.
        :rtype: float

        This was copied from `fpmurphy`_

        .. _fpmurphy: http://fpmurphy.blogspot.com/2008/12/half-precision-floating-point-format_14.html
        """
        # Get byte order of input
        bo = '<' if self._is_little_endian() else '>'

        # Preliminary unpacking
        fmt = '{0}H'.format(bo)
        h = unpack(fmt, half)[0]

        # Pad 16 bits to 32 bits
        s = int((h >> 15) & 0x00000001)  # sign
        e = int((h >> 10) & 0x0000001F)  # exponent
        f = int(h         & 0x000003FF)  # fraction
        if e == 0x00:   # exponent is 0
            if f == 0x00:
                hpad = int(s << 31)
            else:
                while not (f & 0x00000400):
                    f <<= 1
                    e -= 1
                e += 1
                f &= ~0x00000400
        elif e == 0x1F: # exponent is 31
            if f == 0x00:
                hpad = int((s << 31) | 0x7F800000)
            else:
                hpad = int((s << 31) | 0x7F800000 | (f << 13))
        e = e + (127 - 15)
        f = f << 13
        hpad = int((s << 31) | (e << 23) | f)

        # struct.pack hack
        st = pack('I', hpad)
        out = unpack('f', st)
        return out

    def read_preamble(self):
        """Read the waveform preamble from Deoxys.  It contains the following
        metadata about the waveform data:

        :returns out:
        :rtype: dict
        """
        # TODO Combine write, preamble and data in one function
        # TODO Read :waveform:preamble
        #           format WORD this is two bytes for each data point
        #           type   :waveform:type?
        #           points :waveform:points? can be found in the header of :waveform:data?
        #           count  :acquire:count? averaging for one data point, etc
        #           xincrement
        #           xorigin
        #           xreference
        #           yincrement
        #           yorigin
        #           yreference
        # TODO Read :save:waveform:start I do not know how to transfer a file
        pass

    def compose_waveform_xy(self, waveform_y, waveform_preamble):
        """Compose the (x,y) data list according to the y data and preamble
        obtained from the instrument.

        :returns out:
            A 2-column list.  The first column holds the x values and the
            second column holds the y values.
        :rtype: list
        """
        # TODO Read :waveform:data
        #           :waveform:byteorder DONE
        #           :waveform:unsigned  DONE
        #           :waveform:format    DONE
        #           :waveform:source    channel | function | math | pod | bus | sbus
        #           :system:precision
        #           0x0000 hole
        #           0x0001 clipped low
        #           0xFFFF clipped high

        # TODO Need to adjust waveform_x for special values (clipped, etc)
        # TODO Need to adjust waveform_x according to preamble
        # TODO Need to create waveform_y according to preamble
        # TODO Need to compose X and Y values
        pass

    def ask_waveform_data(self):
        """A convenience function to query the waveform preamble and waveform
        data in one call.  Additionally, it also composes the (x,y) data list.

        :returns out:
            A 2-column list.  The first column holds the x values and the
            second column holds the y values.
        :rtype: list
        """
        self.write(':waveform:preamble?')
        waveform_preamble = self.read_preamble()
        self.write(':waveform:data?')
        waveform_y = self.read_ieee754()
        out = self.compose_waveform_xy(waveform_y, waveform_preamble)
        return out


class Genesect(bc.TCPIPInstrument):
    def __init__(self):
        self.DATA = GENESECT
        super(Genesect, self).__init__(socket_pair=self.DATA['socket'])
        self.write(':format:data real,32')
        self.write('*OPC')


class Giratina(bc.TCPIPInstrument):
    def __init__(self):
        self.DATA = GIRATINA
        super(Giratina, self).__init__(socket_pair=self.DATA['socket'])
        self.write(':format:data real,32')
        self.write('*OPC')


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


class Zygarde(bc.TCPIPInstrument):
    def __init__(self):
        self.DATA = ZYGARDE
        super(Zygarde, self).__init__(socket_pair=self.DATA['socket'])


