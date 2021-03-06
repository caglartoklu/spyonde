Spyonde
=============================

Converts cell separated regular Python scripts to Jupyter notebooks.

With Spyonde, it is possible to use any IDE/editor to create Jupyter notebooks, presenatations and lecture notes.


Purpose
-------------------

Using a presentation software such as Microsoft PowerPoint or LibreOffice/OpenOffice Impress contributes a lot to visualization, but they do not get along with code snippets.

While using such a software, keeping the presentation technically correct is very hard since you can not *"run"* a presentation.

Jupyter is a nice presentation tool that can run code, but it is not an IDE/editor. It does not provide pylint/pycodestyle/PEP8 analysis and debugging features.
For some small code snippets, this can be ignored, but for longer code bases, using IDE/editor is more useful.

I wanted a solution where I can *"develop"* and *"run"* a presentation in any IDE/editor.
The alternatives had too many dependencies, so I have created my own solution.
Spyonde allows using any IDE/editor to create Jupyter notebooks.

My favorite editor is `Vim <https://www.vim.org/>`_, and I have been using it for a long time.
Time to time, I also use `Spyder <https://www.spyder-ide.org/>`_.
Spyder has a very useful `code cell <https://docs.spyder-ide.org/editor.html#defining-code-cells>`_ feature,
and I had already created a Python code selection executor in Vim,
called `pyin.vim <https://github.com/caglartoklu/pyin.vim>`_.



Installation
=============================

::

    pip install git+https://github.com/caglartoklu/spyonde

After installation, `pip` will create an executable (`spyonde`) for Spyonde.

Spyonde then can be used from command line as follows:

::

    spyonde mypresentation.py

Note that, on Windows, ``C:\Python3x\Scripts`` directory is NOT automatically added to `PATH` variables.
It is advised to add this directory to `PATH` variables.

or, launch Spyonde with a command like this:

::

    C:\Python37\Scripts\spyonde.exe myfile.py


Usage
=============================

**Step 1: Write a .py file as usual, in your favorite IDE/editor.**

The screenshot below shows Spyder, but any IDE/editor can be used.

Be sure to divide your cells using `code cell syntax of Spyder <https://docs.spyder-ide.org/editor.html#defining-code-cells>`_.
Note that each cell can be run separately by ``ctrl enter`` in Spyder.

.. image:: https://user-images.githubusercontent.com/2071639/83352252-ed2cbf80-a352-11ea-90b5-20b42271ced5.png

**Step 2: Run Spyonde by the following command.**

::

    spyonde demo.py

This command will generate the file ``demo.py.gen.ipynb``.

.. image:: https://user-images.githubusercontent.com/2071639/81415443-2194cd80-9151-11ea-84ec-d6f515d75152.gif

**Step 3: Your .ipynb file is ready. Simply open it.**

.. image:: https://user-images.githubusercontent.com/2071639/81415461-25c0eb00-9151-11ea-8ca5-0fde2b036771.gif


Command Line Options
----------------------

**--nbversion** :
The version string to be embedded into the Jupyter file. It is ``"3.7.4"`` by default.

**--overwrite** :
If provided, automatically confirms overwrite. It does not overwrites files by default. Default is ``False``.

Examples:

::

    spyonde demo.py
    spyonde demo.py --nbversion 3.8.0
    spyonde demo.py --overwrite
    spyonde --overwrite demo1.py demo2.py



Example Input
-------------

The input can be any ``.py`` file, written in your favorite IDE.

Note that the cells are defined by ``#%%`` lines.
That is how Spyonde distinguishes the cells.

If a cell has only comment lines and nothing else, it will be accepted as a Markdown cell. Example:

::

    # %% Some Languages for DOS

    #- BASIC
    #- Pascal
    #- Python (yes, there _was_ a [Python for DOS](https://web.archive.org/web/20020804011430/http://www.python.org/ftp/python/wpy/dos.html))
    #- C/C++
    #- dBase (both a database and language)

If not, it will be a code cell.

Full source code of ``demo.py`` is provided in ``examples`` folder.


Ignoring Cells
------------------------

It is possible to ignore a cell by adding the following line in the ``.py`` file.
Any cell including this comment will be skipped and not rendered into ``.ipynb`` file.

::

    # spyonde:ignore-cell


FAQ
=============================

- **Q: I want to change the generated file name, how can I do that?**
- A: Currently, you can not. It will be added in upcoming versions.

- **Q: Do I need Jupyter to use Spyonde?**
- A: No, you do not. Jupyter may be useful if you want to see and work on generated .ipynb files. If you want, you can use `python-notebook-viewer <https://addons.mozilla.org/en-US/firefox/addon/python-notebook-viewer/>`_ which is a Firefox plugin that lets you view/render python notebooks on Firefox without running a notebook server.

- **Q: Do I have to use Spyder to create a .py file?**
- A: No, you do not. You can use any IDE or text editor, even Notepad if you like.

- **Q: How to pronounce Spyonde?**
- A: As you like.



Compatibility and Requirements
===================================

**Runtime Requirements**

- Officially, minimum tested Python version supported is 3.4.4.
- Untested: should work with Python 3.3 and 3.2, but not lower, since it uses `argparse <https://docs.python.org/3/library/argparse.html>`_.
- Python 2 is not supported and it is not in to do list.
- Jupyter is not required since a ``.ipynb`` file is nothing but a JSON file and Spyonde will create them without Jupyter. However, to see the created files, you may use Jupyter.

**Windows 10**

Tested and developed with Python 3.7.4 on Windows 10.
Development has been made with Python 3.7.4 on Windows 10.


**Linux**

Tested on Ubuntu 18.04 LTS on Windows 10 WSL with Python 3.6.9.

.. image:: https://user-images.githubusercontent.com/2071639/79972299-69073280-849e-11ea-82fa-bfd3060f992d.png

**Windows XP**

Tested on Windows XP, Python 3.4.4.

.. image:: https://user-images.githubusercontent.com/2071639/79972305-6a385f80-849e-11ea-8901-c887de50d128.png


**macOS**

Untested but it is expected to work.
Waiting for comments from macOS users.



Development
==============================

makefile: ``makepile.py``
--------------------------

``makepile.py`` is the make file of Spyonde.
It has no dependencies and it is written in pure Python.

It provides the following commands that can be run from command line:

python makepile.py
--------------------

Shows the main menu of makepile.py and possible targets.

::

    C:\projects1\spyonde>python makepile.py
    Possible targets:
    ['clean', 'demo', 'install', 'linecount', 'lint', 'pyinstaller', 'readme', 'test', 'uninstall']

    No target specified
    if you are on Windows, make sure you are running the script:
      python makepile.py target
    instead of:
      makepile.py target

    enter target: >>>


python makepile.py install
----------------------------

Installs the package locally with pip.


python makepile.py clean
-------------------------

Cleans the ``temp``, ``dist`` and generated files.


python makepile.py pyinstaller
--------------------------------

Packs the package using `PyInstaller <https://www.pyinstaller.org/>`_.

Since this is not mandatory, it has not been added to a ``requirements.txt`` file.

To use this target, PyInstaller must be already installed using:

::

    pip install pyinstaller


python makepile.py demo
-------------------------

Installs the package and uses it to convert the files in ``examples`` directory to Jupyter notebooks.


python makepile.py test
-------------------------

Applies unit testing to package.
Earlier versions have very small number of unit tests, more to come.


python makepile.py lint
-----------------------

Applies
`Pylint <https://www.pylint.org/>`_
to the files in the package.

Requires:

::

    pip install pylint


python makepile.py pep8
-----------------------

Applies
`pycodestyle <https://pycodestyle.pycqa.org/en/latest/>`_
to the files in the package.

Requires:

::

    pip install pycodestyle


python makepile.py vulture
--------------------------

Applies
`vulture <https://pypi.org/project/vulture/>`_
to the files in the package.

Requires:

::

    pip install vulture


python makepile.py linecount
------------------------------

Counts the number of lines in the project using ``cloc`` command.

Requires:

`cloc <https://github.com/AlDanial/cloc>`_ utility
must be already installed.


python makepile.py readme
------------------------------

Converts the ``README.rst`` file to ``README.rst.html`` using `rst2html5 <https://pypi.org/project/rst2html5/>`_.

Requires:

::

    pip install rst2html5


To Do
==============================

- ``[x]`` using makepile.py as makefile
- ``[x]`` examples directory
- ``[x]`` running examples from makepile.py: target:demo
- ``[x]`` add makepile usage to Development section
- ``[x]`` screenshots to README.rst
- ``[x]`` upload to Github
- ``[ ]`` upload to pypi
- ``[ ]`` more unit test coverage
- ``[ ]`` recursively generate .ipynb files under a directory.
- ``[ ]`` standalone Windows version.
- ``[ ]`` icon for standalone Windows version.
- ``[ ]`` date-time suffix option when generating files.



Related Projects
==============================

- `Jupytext <https://github.com/mwouts/jupytext>`_ Jupytext can save Jupyter notebooks as Markdown, RMarkdown and some others.
- `nbconvert <https://github.com/jupyter/nbconvert>`_ : The nbconvert tool allows you to convert an .ipynb notebook file into various static formats including HTML, LaTeX, PDF, Markdown, reStructuredText and some others.
- `pynb <https://github.com/elehcimd/pynb>`_ Jupyter notebooks as plain Python code with embedded Markdown text. The missions of pynb and Spyonde are very similar.
- `python-notebook-viewer <https://addons.mozilla.org/en-US/firefox/addon/python-notebook-viewer/>`_ This Firefox plugin lets you view/render python notebooks without running notebook server, by a simple drag and drop.



The name "Spyonde"
------------------

::

> There are only two hard things in Computer Science:
> cache invalidation and naming things.

-- Phil Karlton

I have checked the `Moons of Jupiter <https://en.wikipedia.org/wiki/Moons_of_Jupiter#List>`_ and I think I have found a suitable one in #76:
`Sponde <https://en.wikipedia.org/wiki/Sponde>`_

From Wikipedia:

::

> Sponde, also known as Jupiter XXXVI, is a natural satellite of Jupiter.
> It was discovered by a team of astronomers from the University of Hawaii led by Scott S. Sheppard in 2001.
> Sponde is about 2 kilometres in diameter.

It seems that it is a nice fit for low-dependency utility.

A little word-play on ``Sponde``, and we have ``Spyonde`` as in ``Jupyter`` and ``Spyder``.



Licence
==============================

MIT Licensed.
See the `LICENSE.txt <LICENSE.txt>`_ file.

