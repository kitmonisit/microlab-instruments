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

    write(s)
    read_ascii(bufsize)
    read_binary()
    read_ieee754()

where ``s`` is an SCPI command (see the instrument documentation) and
``bufsize`` is the expected size in bytes of the ASCII response.  The ``read...`` commands return the following data types:

* ``read_ascii`` returns human-readable *str*.
* ``read_binary`` technically returns *str* but it is not guaranteed to be human-readable.  Printing the output of this function will only result in gibberish in your terminal.
* ``read_ieee754`` returns a *list* of numbers which are the result of a measurement SCPI query.

**WARNING** If you consecutively send ``write`` several commands that for which
you expect a response without reading their respective responses in turn, you
may no longer be able to segregate the data in the response buffer.  For
example:

.. code-block:: python

    giratina.write('*IDN?')
    giratina.write(':fetch:arr:volt?')

    # The following line of code reads too much.  The response to '*IDN?' is
    # not necessarily 4096 bytes long.  The beginning of the response to
    # ':fetch:arr:volt' is read prematurely and this library does not provide
    # functions to reconstruct the data when it is read this way.
    giratina.read_ascii(bufsize=4096)

Convenience functions are provided such that ``write`` and ``read`` commands
are done consecutively.

    ask_ascii(s)
    ask_binary(s)
    ask_ieee754(s)

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
retrived.

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

