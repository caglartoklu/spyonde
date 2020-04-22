# -*- coding: utf-8 -*-

"""
spyonde
Create cells in your favorite text editor and Spyonde converts them to Jupyter notebooks.
"""

__version__ = '0.1.0'
__author__ = 'Caglar Toklu <caglartoklu@gmail.com>'
__all__ = []


import os
import sys


# add current directory to sys.path
_MODULE_PATH = os.path.dirname(os.path.realpath(__file__))
if _MODULE_PATH not in sys.path:
    sys.path.append(_MODULE_PATH)

# add upper directory to sys.path
# _UPPER_DIRECTORY = os.path.abspath(os.path.join(_MODULE_PATH, "../"))
# if _UPPER_DIRECTORY not in sys.path:
#     sys.path.append(_UPPER_DIRECTORY)

# this line should be after sys.path stuff, so disabling a pylint message.
# import should be placed at the top of the module.
import spyondemain  # # pylint: disable=C0413

def convert_file(input_file_name, output_file_name=None):
    """
    Converts a .py file to a .ipynb file.
    .py file must be written in a specific format to be converter.
    """
    spyondemain.convert_file(input_file_name, output_file_name)
