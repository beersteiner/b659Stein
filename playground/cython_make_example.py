#!/usr/bin/env python

"""
Simple script showing how a module that was built using distutils and
Cython.Build can be directly imported similar to any python module.
"""

__author__ = 'John Stein' 
__email__ = 'jodstein@iu.edu'


from hello import say_hello_to

say_hello_to('John')
