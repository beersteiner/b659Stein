#!/usr/bin/env python

"""
Example build script using distutils.core.setup and Cython.Build.cythonize to
build the requisite package for import into a python program.
https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html

produces: hello.c, hello.cpython-<distro_info>.so, and build/ directory
"""

__author__ = 'John Stein'
__email__ = 'jodstein@iu.edu'

from distutils.core import setup
from Cython.Build import cythonize

setup(
    name="My hello app",
    ext_modules=cythonize('hello.pyx', compiler_directives={'embedsignature': True}),
)