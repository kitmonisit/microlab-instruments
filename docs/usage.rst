==================
Usage and Tutorial
==================

To use Microlab Instruments in a project

.. code-block:: python

    import microlab_instruments as mi

    kyurem = mi.Kyurem()
    kyurem.write('*IDN?')
    print kyurem.read()
