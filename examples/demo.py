# -*- coding: utf-8 -*-

"""
module doc
"""

import os
import sys
# import stuff as usual.

# spyonde:ignore-cell
# the line above means that, this cell will not be in the .ipynb file.

# pylint: disable=C0103
# Constant name doesn't conform to UPPER_CASE naming style (invalid-name)

# pylint: disable=C0301
# Line too long (105/100) (line-too-long)

# pylint: disable=C0413
# Import should be placed at the top of the module (wrong-import-position)

# pylint: disable=C0412
# Imports from package are not grouped (ungrouped-imports)

# pylint: disable=W0404
# Reimport (imported line 44) (reimported)



# %% Welcome to Tiny Python Introduction

# ## Python Language

# - As Wikipedia [says](https://en.wikipedia.org/wiki/Python_(programming_language)):
# - interpreted
# - high level
# - **type system**: `duck typing`, `dynamic`



#     %% Next Slide Will Be Great

# - This cell is expected to be in a separate cell.
# - And so it is.
# - Code is coming.



# %%
# - this is a cell without a header.
# - that's it.
# - see the next slide.
print("hi")



# %% this is a cell with a header.
# - that's it.
# - see the next slide.
print("hi")



# %% String Definition

# type inference
s1 = "stuff"
s2 = 'another stuff'
# this will be an ordinary comment.



# %% Printing Strings

print(s1)
# we should also print the other.
print(s2)



# %% Printing Strings (2)

# - since this cell
# - has an line that is not a comment
# - it will be a code cell, not a markdown cell.
print("told you so.")



# %% Multi-line Strings

python_implementations = """
Some Python implementations are as follows:

Python (also known as CPython, the reference implementation)
PyPy
Jython
IronPython
"""
print(python_implementations)



# %% A `for` loop Example

for a in range(10):
    print(a)



# %% Some Languages for DOS

#- BASIC
#- Pascal
#- Python (yes, there _was_ a [Python for DOS](https://web.archive.org/web/20020804011430/http://www.python.org/ftp/python/wpy/dos.html))
#- C/C++
#- dBase (both a database and language)



# %% Image Handling in Spyonde

# - Image handling it directly passed to Markdown as-is.
# - The design and colors of Python.org [from 2005](https://web.archive.org/web/20050801073427/http://www.python.org/):
#
# ![](python_org_2005.png)
