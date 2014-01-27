#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='microlab_instruments',
    version='0.1.0',
    description='''Microlab Instruments is an abstraction layer for all the GPIB/Ethernet/USB/Serial instruments in the Microlab. All you have to do is instantiate an instrument class and with the help of each instrument's SCPI command reference, just ask(), write(), or read() commands. No need to worry about hardware and protocol settings.''',
    long_description=readme + '\n\n' + history,
    author='Kristofer Monisit',
    author_email='kmonisit@gmail.com',
    url='https://github.com/kitmonisit/microlab_instruments',
    packages=[
        'microlab_instruments',
    ],
    package_dir={'microlab_instruments': 'microlab_instruments'},
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='microlab_instruments',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
