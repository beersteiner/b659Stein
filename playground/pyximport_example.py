#!/usr/bin/env python

"""
Simple script showing how to directly import simple (do not depend
on external C libraries) Cython modules.
"""

__author__ = 'John Stein'
__email__ = 'jodstein@iu.edu'


import sys
import pyximport; pyximport.install(language_level = sys.version_info.major)
from hello import say_hello_to

say_hello_to('John')
