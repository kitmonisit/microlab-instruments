.. complexity documentation master file, created by
   sphinx-quickstart on Tue Jul  9 22:26:36 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

====================
Microlab Instruments
====================

Quick start
===========

.. code-block:: bash

    $ pip install microlab-instruments
    $ python

.. code-block:: python

    import microlab_instruments as mi

    kyurem = mi.Kyurem()
    kyurem.write('*IDN?')
    print kyurem.read_ascii()


Using the Verilog code
======================

The included Verilog code is used to program the Xilinx Virtex-5 FPGA so that
it can communicate in SPI and I2C protocol with the Aardvark as it is
configured in this library.

See the source code for the Aardvark protocol configuration of SPI and I2C.


Contents
========

.. toctree::
   :maxdepth: 2

   readme
   installation
   usage
   microlab_instruments
   contributing
   authors
   history

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
