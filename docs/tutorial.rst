==================
Usage and Tutorial
==================

Basics
======

#.  Start using ``microlab-instruments``

    .. code-block:: python

        import microlab_instruments as mi

#.  Turn on the instrument nicknamed *Giratina*.
#.  Initialize *Giratina* in the software environment

    .. code-block:: python

        giratina = mi.Giratina()

#.  Query *Giratina* for its identification string.

    .. code-block:: python

        giratina.write('*IDN?')

#.  Read *Giratina*'s ASCII response

    .. code-block:: python

        print giratina.read_ascii()

#.  Putting them all together, you can write a script that asks *Giratina* for
    its identification string:

    .. code-block:: python

        import microlab_instruments as mi

        giratina = mi.Giratina()
        giratina.write('*IDN?')
        print giratina.read_ascii()


Types of Instruments
====================

Two types of instruments are modeled in this Python package.

#. **SCPI instruments** communicate via GPIB or TCP/IP.  They can receive
   string commands and respond in either ASCII, binary, or IEEE-754 floating
   point formats.
#. **I2C instruments** communicate via the Aardvark adapter.  They are more
   limited in terms of commands and response formats.

SCPI Instruments
----------------

The most important commands for SCPI instruments are:

*  :py:meth:`~microlab_instruments.base_classes.TCPIPInstrument.write`
*  :py:meth:`~microlab_instruments.base_classes.SCPIInstrument.read_ascii`
*  :py:meth:`~microlab_instruments.base_classes.SCPIInstrument.read_binary`
*  :py:meth:`~microlab_instruments.base_classes.SCPIInstrument.read_ieee754`

The ``read...`` commands return the following data types:

* ``read_ascii`` returns human-readable *str*.
* ``read_binary`` technically returns *str* but it is not guaranteed to be human-readable.  Printing the output of this function will only result in gibberish in your terminal.
* ``read_ieee754`` returns a *list* of numbers which are the result of a measurement SCPI query.

**WARNING** If you consecutively send ``write`` several commands that for which
you expect a response without reading their respective responses in turn, you
may no longer be able to segregate the data in the response buffer.  For
example:

.. code-block:: python

    import microlab_instruments as mi

    giratina = mi.Giratina()
    giratina.write('*IDN?')
    giratina.write(':fetch:arr:volt?')

    # The following line of code reads too much.  The response to '*IDN?' is
    # not necessarily 4096 bytes long.  The beginning of the response to
    # ':fetch:arr:volt' is read prematurely and this library does not provide
    # functions to reconstruct the data when it is read this way.
    giratina.read_ascii(bufsize=4096)

Convenience functions are provided such that ``write`` and ``read`` commands
are done consecutively.

*  :py:meth:`~microlab_instruments.base_classes.SCPIInstrument.ask_ascii`
*  :py:meth:`~microlab_instruments.base_classes.SCPIInstrument.ask_binary`
*  :py:meth:`~microlab_instruments.base_classes.SCPIInstrument.ask_ieee754`

SCPI Instruments Example
^^^^^^^^^^^^^^^^^^^^^^^^

The following code takes a screenshot of the present display on *Giratina* and
saves it in ``screenshot.jpg`` in the current directory.

.. code-block:: python

    giratina.write(':DISP:ENAB ON')
    giratina.write(':DISP:VIEW GRAPH')
    giratina.write(':HCOP:SDUM:FORM JPG')
    giratina.write('*OPC')
    giratina.write(':HCOP:SDUM:DATA?')
    d = giratina.read_binary()

    fd = open('screenshot.jpg', 'wb')
    fd.write(d)
    fd.close()

For the following code, connect a 1kΩ resistor between the positive and
negative probes.  We will sweep the voltage from 0 to 5 and measure the
current.  Voltage sweep values and the corresponding current values are
retrieved.

.. code-block:: python

    import microlab_instruments as mi
    import numpy as np

    giratina = mi.Giratina()
    giratina.write('*IDN?')

    giratina.write(':source:function:mode voltage')
    giratina.write(':source:sweep:direction up')
    giratina.write(':source:sweep:stair double')
    giratina.write(':source:sweep:spacing linear')
    giratina.write(':source:voltage:mode sweep')
    giratina.write(':source:voltage:start 0')
    giratina.write(':source:voltage:stop 5')
    giratina.write(':source:voltage:points 201')
    giratina.write(':sens:curr:prot 0.120')
    giratina.write(':trigger:source aint')
    giratina.write(':trigger:count 201')
    giratina.write(':format:data real,64')
    giratina.write(':outp on')
    giratina.write(':init (@1)')
    giratina.ask_ascii('*OPC?')
    giratina.write(':output off')
    giratina.write(':fetch:arr:volt? (@1)')
    volt = np.array(giratina.read_ieee754())
    giratina.write(':fetch:arr:curr? (@1)')
    curr = np.array(giratina.read_ieee754())
    res  = volt / curr
    for m, n, o in zip(volt, curr, res):
        a = '{0:>20.3e}'.format(m)
        b = '{0:>17.1f}mA'.format(n*1e3)
        c = '{0:>20.3e}'.format(o)
        print ''.join([a, b, c])


I2C Instruments
---------------

The I2C instruments are more specialized and thus we will discuss them here.
The four I2C instruments are listed below, but you will actively use only the
first three.

#.  ``Kerrigan``, an FPGA
#.  ``Traxex``, a temperature sensor
#.  ``Xin``, another temperature sensor identical to ``Traxex``
#.  ``Chen``, an I2C multiplexer used to coordinate the ``Traxex`` and ``Xin``

These I2C instruments communicate via the Aardvark adapter, which must be
initialized first.

I2C Instruments Example
^^^^^^^^^^^^^^^^^^^^^^^

``Kerrigan`` has only two commands, :py:meth:`~microlab_instruments.base_classes.FPGAInstrument.write` and :py:meth:`~microlab_instruments.base_classes.FPGAInstrument.read`

.. code-block:: python

    import microlab_instruments as mi

    aa = mi.Aardvark()
    kerrigan = mi.Kerrigan()
    REGISTER = 0x11
    PAYLOAD = 0xAA
    kerrigan.write(REGISTER, PAYLOAD)
    print kerrigan.read(REGISTER)  # This should output 0xAA
    print kerrigan.read(0x12)      # This should output 0x00


To use ``Traxex`` and ``Xin``, we also need to initialize ``Chen``.  The temperature sensors have only one command, :meth:`.read_temp`\ , which returns the temperature in Celsius degrees.

.. code-block:: python

    import microlab_instruments as mi

    aa = mi.Aardvark()
    chen = mi.Chen(aa)
    traxex = mi.Traxex(aa, chen)
    xin = mi.Xin(aa, chen)

    print traxex.read_temp()
    print xin.read_temp()
