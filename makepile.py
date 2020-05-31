r"""
makepile.py

A simplistic, pure Python make tool without dependencies.
This copy is modified for Spyonde.

Usage:
    python makepile.py
    python makepile.py <target>


Documenation:
    The script works with old school python functions.
    Any public function you add becomes a target.
    If you have two functions in the file, named `install()` and `test()`
    you can call a target like:

        python makepile.py install
    or
        python makepile.py test

    To provide dependencies, simply call a function from another.


makepile.py is MIT licensed:

    Copyright (c) 2020 Caglar Toklu

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

# pylint: disable=missing-docstring
# pylint: disable=C0111
# C0111 - Missing %s docstring
# C:  1, 0: Missing module docstring (missing-docstring)
# C: 13, 0: Missing function docstring (missing-docstring)

# pylint: disable=invalid-name
# pylint: disable=C0103
# C: 10, 0: Invalid constant name "variable1" (invalid-name)

# pylint: disable=line-too-long
# pylint: disable=C0301
# C: 22, 0: Line too long (127/100) (line-too-long)

# pylint: disable=trailing-newlines
# pylint: disable=C0303
# C: 59, 0: Trailing newlines (trailing-newlines)


from __future__ import print_function

import inspect  # pylint: disable=unused-import
import os  # pylint: disable=unused-import
import shutil  # pylint: disable=unused-import
import sys

# change directory to script dir
os.chdir(os.path.abspath(os.path.dirname(__file__)))


def _multiline_str_to_list(haystack):
    r"""
    Converts a multiline string to a list.
    Empty lines are removed, and all the lines are stripped.
    """
    assert isinstance(haystack, str)
    list1 = haystack.split("\n")
    list1 = [x.strip() for x in list1 if x.strip()]
    return list1

# BEGIN TARGETs SECTION _________________________________________


def install():
    r"""
    Installs the package using pip.
    cmd = "pip install -e ."
    """
    # cmd = "python setup.py install"
    cmd = "python -m pip install -e ."
    os.system(cmd)


def uninstall():
    r"""
    Uninstalls the package using pip.
    """
    cmd = "python -m pip uninstall spyonde"
    os.system(cmd)


def clean():
    r"""
    Deletes the generated files and directories.
    """

    dirs_as_str = """
    spyonde.egg-info
    dist
    build
    spyonde/.pylint.d
    spyonde/__pycache__
    tests/.pylint.d
    tests/__pycache__
    README.rst.html
    spyonde.spec
    examples/.pylint.d
    examples/__pycache__
    examples/.ipynb_checkpoints
    examples/demo.py.gen.ipynb
    examples/simple1.py.gen.ipynb
    examples/simple2.py.gen.ipynb
    """
    dirs = _multiline_str_to_list(dirs_as_str)

    for item_name in dirs:
        print(item_name)
        if os.path.isdir(item_name):
            shutil.rmtree(os.path.normpath(item_name), ignore_errors=True)
            print("  removed dir:", item_name)
        elif os.path.isfile(item_name):
            os.remove(os.path.normpath(item_name))
            print("  removed file:", item_name)
        else:
            print("  not a directory/file: ", item_name)


def pyinstaller():
    r"""
    Makes a Windows executable using PyInstaller.

    requires:
    pip install pyinstaller
    """
    readme()
    main_source_file = os.path.normpath("spyonde/spyondemain.py")
    # root_name = os.path.split(main_source_file)[1]  # filename.py
    # root_name = os.path.splitext(root_name)[0]  # spyondemain

    target_name = "spyonde"
    # the full path will be:
    # dist/<target_name>/<target_name>.exe

    cmd = r"pyinstaller --noconfirm --clean --onedir --noupx --nowindowed "
    # TODO: 7 the following line did not work.
    # we needed it for optimization.
    # cmd = r"python -O -m pyinstaller --noconfirm --clean --onedir --noupx --nowindowed "
    # https://pyinstaller.readthedocs.io/en/stable/usage.html#running-pyinstaller-with-python-optimizations
    cmd += main_source_file
    cmd += " -n" + target_name
    os.system(cmd)

    files_to_bundle = """
    LICENSE.txt
    README.rst.html
    """
    # also possible to add:
    # spyonde/spyondemain.py

    files_to_bundle = _multiline_str_to_list(files_to_bundle)
    for file_name in files_to_bundle:
        src = os.path.normpath(file_name)
        # note that src can be a single file name or a path/file_name.
        only_file_name = os.path.split(src)[1]

        dst = os.path.normpath("dist/" + target_name + "/" + only_file_name)

        # not needed since we are directly copying .html file:
        # if only_file_name.lower() == "readme.rst":
        #     # Rename .rst file as .rst.txt for distribution.
        #     dst = dst + ".txt"

        print("\ncopying:")
        print("  ", src)
        print("as:")
        print("  ", dst)
        shutil.copyfile(src, dst)


def demo():
    """
    Runs a demo using files in examples directory.
    """
    clean()
    install()

    demo1_file = os.path.normpath("examples/demo.py")
    demo2_file = os.path.normpath("examples/simple1.py")
    demo3_file = os.path.normpath("examples/simple2.py")
    demo4_file = os.path.normpath("examples/empty1.py")
    demo5_file = os.path.normpath("examples/regular1.py")
    # demo2_file = os.path.normpath("examples/empty.py")
    demo_files = [demo1_file, demo2_file, demo3_file, demo4_file, demo5_file]

    for file_name in demo_files:
        generated_file_name = file_name + ".gen.ipynb"
        # TODO: 6 what if the output file name does not end with .gen.ipynb?
        if os.path.isfile(generated_file_name):
            print("deleting file:", generated_file_name)
            os.remove(generated_file_name)

        # TODO: 6 what to do if C:\Python3\Scripts is not on path?
        cmd = "spyonde " + file_name
        os.system(cmd)


def test():
    r"""
    Applies unit testing.
    """
    path = "tests/test_sample.py"
    cmd = "python " + os.path.normpath(path)
    print(cmd)
    os.system(cmd)


def lint():
    """
    Applies pylint to .py files in this project.

    requires:
    pip install pylint
    """
    path = "tests/make_lint.py"
    cmd = "python " + os.path.normpath(path)
    print(cmd)
    os.system(cmd)


def pep8():
    """
    Applies PEP8/pycodestyle to .py files in this project.

    requires:
    pip install pycodestyle
    """
    path = "tests/make_lint.py pep8"
    cmd = "python " + os.path.normpath(path)
    print(cmd)
    os.system(cmd)


def vulture():
    """
    Applies vulture to .py files in this project.

    requires:
    pip install vulture
    """
    path = "tests/make_lint.py vulture"
    cmd = "python " + os.path.normpath(path)
    print(cmd)
    os.system(cmd)


def linecount():
    r"""
    Counts lines in the project using cloc utility.

    Requires:
    https://github.com/AlDanial/cloc
    """
    cmd = "cloc ."
    print(cmd)
    os.system(cmd)


def readme():
    r"""
    Converts README.rst to README.rst.html.

    Requires:
    https://pypi.org/project/rst2html5/
    """
    cmd = "rst2html5 README.rst > README.rst.html"
    print(cmd)
    os.system(cmd)


# END TARGETs SECTION _________________________________________


def main():
    # any code not to mess with global namespace.
    pass


items_in_module = dir()
# ['A_CONSTANT', '__builtins__', '__cached__', '__doc__', '__file__',
# '__loader__', '__name__', '__package__', '__spec__', 'function1', 'main',
# 'os', 'print_function', 'function2', 'shutil', 'sys']

# detect the list of "target" functions in the module
targets_in_module = []
for item in items_in_module:
    code = "inspect.isfunction(" + item + ")"
    result = eval(code)  # pylint: disable=eval-used
    if result:
        if item not in ['main']:  # remove some fixed functions
            # remove private functions:
            if not item.startswith("_"):
                # this also covers __
                targets_in_module.append(item)
print("Possible targets:")
print(targets_in_module, "\n")

target_candidate = None
# print(len(sys.argv))
# print(sys.argv)
if len(sys.argv) == 1:
    # no target specified, no can do.
    print("No target specified")
    print("if you are on Windows, make sure you are running the script:")
    print("  python makepile.py target")
    print("instead of:")
    print("  makepile.py target")
    print()
    target_candidate = input("enter target: >>>")
elif len(sys.argv) == 2:
    # exactly one target specified as required.
    target_candidate = sys.argv[1]
else:
    # more than one target specified, no can do.
    print("Please specify exactly one target. Possible targets:")
    print(targets_in_module)

target_found = False
if target_candidate:
    if target_candidate in targets_in_module:
        print("\n/// target:", target_candidate)
        function_call = target_candidate + "()"
        exec(function_call)  # pylint: disable=exec-used
        target_found = True

if not target_found:
    print("Target not found : ", target_candidate)
    print("Possible targets:")
    print(targets_in_module)
