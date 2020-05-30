#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Utility for cleaning files, applying pylint ve pycodestlye to the package.

Requirements:
    pylint and pycodestyle should be on path.
If you don't have them, install them by the following commands:
    pip install pylint pycodestyle
"""

import fnmatch
import os
import sys


def get_list_of_py_files(topdir=None):
    """
    Returns the list of .py files as a list.
    """
    if topdir is None:
        topdir = os.path.dirname(os.path.abspath(__file__))

        # go one upper dir:
        topdir = os.path.abspath(os.path.join(topdir, ".."))
        # print(topdir)

    file_list = []
    for root, dirs, files in os.walk(topdir, topdown=False):  # pylint: disable=W0612
        # W0612: unused-variable
        for name in files:
            full_file_path = os.path.join(root, name)
            if fnmatch.fnmatch(full_file_path, "*.py"):
                if not fnmatch.fnmatch(full_file_path, "*.eggs*"):
                    if not fnmatch.fnmatch(full_file_path, "*.private*"):
                        # ignore .py files in .eggs folders.
                        file_list.append(full_file_path)
        # for name in dirs:
        #     print(os.path.join(root, name))
    # print(file_list)
    return file_list


def print_separator():
    """
    Prints a separator to the screen.
    """
    print()
    print()
    print(79 * "/")


def apply_pylint(file_list):
    """
    Applies pylint to all .py files in the package.
    """
    for file_path in file_list:
        cmd = "pylint " + '"' + file_path + '"'
        print_separator()
        print(cmd)
        os.system(cmd)


def apply_pep8(file_list):
    """
    Applies pep8 to all .py files in the package.
    """
    for file_path in file_list:
        # cmd = "pep8 " + '"' + file_path + '"'
        cmd = "pycodestyle " + '"' + file_path + '"'
        print_separator()
        print(cmd)
        os.system(cmd)


def main():
    """
    Entry point of the module.
    """
    file_list = get_list_of_py_files()

    pep8_used = False
    if len(sys.argv) >= 2:
        arg = sys.argv[1]
        if arg in ["pep8", "pycodestyle"]:
            apply_pep8(file_list=file_list)
            pep8_used = True

    if not pep8_used:
        apply_pylint(file_list=file_list)


if __name__ == "__main__":
    main()
