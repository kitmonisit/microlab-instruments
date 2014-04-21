==================
Usage and Tutorial
==================

To use Microlab Instruments in a project

.. code-block:: python

    import microlab_instruments as mi

    giratina = mi.Giratina()
    giratina.write('*IDN?')
    print giratina.read_ascii()
