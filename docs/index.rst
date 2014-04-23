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

    $ pip install git+https://github.com/kitmonisit/microlab-instruments.git
    $ python

.. code-block:: python

    import microlab_instruments as mi

    giratina = mi.Giratina()
    giratina.write('*IDN?')
    print giratina.read_ascii()

Contents
========

.. toctree::
   :maxdepth: 3

   readme
   installation
   tutorial
   microlab_instruments
   contributing
   authors
   history

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
