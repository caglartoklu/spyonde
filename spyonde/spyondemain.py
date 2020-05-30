# -*- coding: utf-8 -*-

"""
spyonde
Create cells in your favorite text editor and Spyonde converts them to Jupyter notebooks.
"""

# pylint: disable=line-too-long

import argparse
import json
import os
import re
import sys
import tempfile
import token
import tokenize

__TOKEN_CELL_SEPS = ["#%%", "# %%", "# <codecell>"]

#  #%% (standard cell separator)
#  # %% (standard cell separator, when file has been edited with Eclipse)
#  # <codecell> (IPython notebook cell separator)
# https://docs.spyder-ide.org/editor.html

__CELL_TYPE_MARKDOWN = "markdown"
__CELL_TYPE_CODE = "code"
__COMMENT_STARTER = "#"


def starts_with(haystack, needle):
    """
    Returns True if needle starts with one of the items of haystack.

    :type haystack: list
    :param haystack: list of strings, these are various starters.
    :type needle: str
    :param needle: a single string.
    """
    assert isinstance(haystack, list)
    assert isinstance(needle, str)

    if haystack:
        assert isinstance(haystack[0], str)

    result = False
    for starter in haystack:
        if needle.startswith(starter):
            result = True
            break
    return result


def str_consists_of_only(haystack, needles):
    """
    Return True if haystack consists of characters only in needles.

    :type haystack: str
    :type needles: str
    :param needles: can eithter be a string, or a list of strings.
    :return: True if haystack consists of characters only in needles.
    :rtype: bool

    haystack1 = "54654645"
    numbers = "0123456789"
    print(str_consists_of_only(haystack1, numbers))  # True

    haystack1 = "xx54654645"
    numbers = "0123456789"
    print(str_consists_of_only(haystack1, numbers))  # False
    """
    assert isinstance(haystack, str)
    assert isinstance(needles, (list, str))
    if isinstance(needles, list):
        assert isinstance(needles[0], str)

    for char in needles:
        haystack = haystack.replace(char, "")

    if haystack:
        # something left.
        # that means, haystack has some characters that are not in needles.
        result = False
    else:
        # all the characters are replaced.
        # that means, haystack consists of characters only in needles.
        result = True
    return result


def remove_if_starts_with(haystack, needle):
    """
    Removes needle from haystack if haystack starts with needle.
    Haystack remains unchanged otherwise.

    print(remove_if_starts_with("python", "py"))  # thon
    print(remove_if_starts_with("python", "pyx"))  # python

    :type haystack: str
    :type needle: str
    """
    assert isinstance(haystack, str)
    assert isinstance(needle, str)
    if haystack.startswith(needle):
        haystack = haystack[len(needle):]
    return haystack


def remove_cell_separator_string(haystack):
    """
    Eats values from haystack and returns what is left.

    :type haystack: str

    print(remove_cell_separator_string("#%%"))  # ""
    print(remove_cell_separator_string("#%%my jam"))  # "my jam"
    print(remove_cell_separator_string("#%% my jam"))  # "my jam"
    print(remove_cell_separator_string("#  %% my jam"))  # "my jam"
    print(remove_cell_separator_string("#  <codecell> my jam"))  # "my jam"
    print(remove_cell_separator_string("# % % not my jam"))  # "% % not my jam"
    """
    assert isinstance(haystack, str)
    values_to_eat = ["#", "%%", "<codecell>"]
    haystack2 = haystack.strip()
    for value in values_to_eat:
        haystack2 = remove_if_starts_with(haystack2, value)
        haystack2 = haystack2.strip()
    return haystack2


def answer_in_yes_or_no(message):
    """
    Gets a yes/no answer.
    Only "y" or "yes" is "Yes", all others means "No".
    Returns True if answer is, False otherwise.

    :type message: str
    """
    assert isinstance(message, str)
    answer = input(message)
    answer = answer.strip().lower()
    result = False
    if answer in ["y", "yes"]:
        result = True
    return result


def is_cell_separator(line2):
    """
    Returns True if the line is a cell separator, False otherwise.

    is_cell_separator():
        pattern: #%% and some comment
    is_only_cell_separator():
        pattern: #%% <and that's it, no comments>
    Their only difference is the regular expression.

    :type line2: str

    __TOKEN_CELL_SEPS = ["#%%", "# %%", "# <codecell>"]
    """
    if not hasattr(is_cell_separator, "compiled_pattern"):
        # it doesn't exist yet, so initialize it once.
        is_cell_separator.compiled_pattern = re.compile(r'\s*#\s*%%\S*')
        # compile this pattern once, for performance reasons.
        # note that Spyder does not exactly use this.
        # it only allows one space after #.
        # examples according to Spyder
        # #%% valid cell separator
        # # %% valid cell separator
        # #  %% INvalid cell separator

    assert isinstance(line2, str)

    cell_separator_it_is = False
    if starts_with(__TOKEN_CELL_SEPS, line2):
        # a simple string comparison to especially find "# <codecell>"
        cell_separator_it_is = True
    elif is_cell_separator.compiled_pattern.match(line2):
        # a more complex regex search.
        cell_separator_it_is = True
    return cell_separator_it_is


def is_only_cell_separator(line2):
    """
    Returns True if the line is a cell separator without comments, False otherwise.

    is_cell_separator():
        pattern: #%% and some comment
    is_only_cell_separator():
        pattern: #%% <and that's it, no comments>
    Their only difference is the regular expression.

    :type line2: str

    __TOKEN_CELL_SEPS = ["#%%", "# %%", "# <codecell>"]
    """

    if not hasattr(is_only_cell_separator, "compiled_pattern1"):
        # it doesn't exist yet, so initialize it once.
        is_only_cell_separator.compiled_pattern1 = re.compile(r'\s*#\s*%%\s*\Z')
        is_only_cell_separator.compiled_pattern2 = re.compile(r'\s*#\s*<codecell>\s*\Z')
        # compile this pattern once, for performance reasons.
        # note that Spyder does not exactly use this.
        # it only allows one space after #.
        # examples according to Spyder
        # #%% valid cell separator
        # # %% valid cell separator
        # #  %% INvalid cell separator

    assert isinstance(line2, str)

    cell_separator_it_is = False
    if is_only_cell_separator.compiled_pattern1.match(line2):
        # a more complex regex search.
        cell_separator_it_is = True
    elif is_only_cell_separator.compiled_pattern2.match(line2):
        # a more complex regex search.
        cell_separator_it_is = True

    return cell_separator_it_is


def clean_cell_lines(cell_lines):
    """
    Removes "\\" characters that has been added with Python's untokenizer.
    """
    cell_lines = [x for x in cell_lines if x.strip() != '\\']
    return cell_lines


def detect_encoding(token1):
    """
    If the token1 is an encoding token, it returns the encoding as a string.
    Otherwise, it returns None.

    Python 3.6:
    TokenInfo(type=59 (ENCODING), string='utf-8', start=(0, 0), end=(0, 0), line='')
    https://docs.python.org/3.6/library/token.html

    Python 3.7:
    TokenInfo(type=57 (ENCODING), string='utf-8', start=(0, 0), end=(0, 0), line='')
    https://docs.python.org/3.7/library/token.html

    Changed in version 3.7: Added COMMENT, NL and ENCODING tokens.

    print(sys.version_info)
    sys.version_info(major=3, minor=7, micro=4, releaselevel='final', serial=0)
    """
    assert isinstance(token1, tokenize.TokenInfo)

    result = None

    it_is_encoding_cell = False
    py_version = sys.version_info
    if py_version.major >= 3 and py_version.minor >= 7:
        if token1.type == token.ENCODING:
            it_is_encoding_cell = True
    elif "type=59 (ENCODING)" in str(token1):
        it_is_encoding_cell = True

    if it_is_encoding_cell:
        result = token1.string

    return result


def is_comment_token(token1):
    """
    Returns True if the token1 is a comment token, False otherwise.
    Since there is an incompatibility between Python 3.6 and Python 3.7,
    this function resolves it.
    See more about the incompatibility here:
    detect_encoding()
    """
    assert isinstance(token1, tokenize.TokenInfo)
    result = False

    py_version = sys.version_info
    if py_version.major >= 3 and py_version.minor >= 7:
        if token1.type == token.COMMENT:
            result = True
    else:
        if "type=57 (COMMENT)" in str(token1):
            result = True

    return result


def split_to_cells(input_file_name):
    """
    Tokenizes the contents of input_file_name.

    :type input_file_name: str

    Token constants:
    https://docs.python.org/3/library/token.html

    Returns a list of strings.

    [
        ['# File Read and Write']
        ['# where are we?', '```python', 'print(os.getcwd())', '```']
        ['# data files.']
    ]
    """
    assert isinstance(input_file_name, str)

    def untokenize_to_str(tokens_list, encoding2="utf-8"):
        untokenized = tokenize.untokenize(tokens_list)
        if isinstance(untokenized, str):
            result2 = untokenized
        elif isinstance(untokenized, bytes):
            result2 = untokenized.decode(encoding2)
        else:
            raise ValueError("unexpected type for tokens_list:", str(type(untokenized)))
        return result2

    all_cell_lines = []
    detected_encoding = None

    temp_input_file_name = prepare_temp_file_name(input_file_name)

    with open(temp_input_file_name, 'rb') as handle:
        tokens = tokenize.tokenize(handle.readline)

        current_cell_tokens = []
        for token1 in tokens:

            token_str = token1.string
            token_line = token1.line

            detected_encoding_temp = detect_encoding(token1)
            if detected_encoding_temp:
                if detected_encoding is None:
                    detected_encoding = detected_encoding_temp
                    print("encoding set:", detected_encoding)
                else:
                    raise ValueError("re-encountered an encoding.")

            it_is_cell_separator = False
            if is_comment_token(token1):
                if is_cell_separator(token_line) and is_cell_separator(token_str):
                    it_is_cell_separator = True

            if it_is_cell_separator:
                current_cell_code = untokenize_to_str(tokens_list=current_cell_tokens,
                                                      encoding2=detected_encoding)
                assert isinstance(current_cell_code, str)

                current_cell_lines = current_cell_code.split("\n")
                current_cell_lines = clean_cell_lines(current_cell_lines)
                all_cell_lines.append(current_cell_lines)

                current_cell_tokens = [token1]
            else:
                current_cell_tokens.append(token1)

        # this block caused an IndexError in Python's untokenize method, so I have left it out:
        # if current_cell_tokens:
        #     current_cell_code = untokenize_to_str(tokens_list=current_cell_tokens,
        #                                           encoding2=detected_encoding)
        #     current_cell_lines = current_cell_code.split("\n")
        #     all_cell_lines.append(current_cell_lines)
        # Instead, prepare_temp_file_name() already added a dummy cell to be eaten here.

    try:
        os.remove(temp_input_file_name)
    except:  # pylint: disable=bare-except
        print("could not delete temp file:", temp_input_file_name)

    return all_cell_lines


def is_comment(needle):
    """
    Returns True if needle is a Python comment, False otherwise.

    :type needle: list
    """
    assert isinstance(needle, str)
    needle = needle.strip()
    result = False
    if needle.startswith(__COMMENT_STARTER):
        result = True
    return result


def detect_cell_type(cell):
    """
    Detects the cell type for a given cell.

    :type cell: list

    Algorithm:
    Parses each line in the cell.
    If there is anything except comment and empty lines,
    than it is labeled as a code cell.
    Otherwise, it is a markdown cell.

    cell: list of strings.
    """
    assert isinstance(cell, list)
    assert isinstance(cell[0], str)

    empty_line_count = 0
    code_line_count = 0
    comment_line_count = 0

    for line in cell:
        stripped_line = line.strip()
        if is_comment(stripped_line):
            comment_line_count += 1
        elif not stripped_line:
            empty_line_count += 1
        else:
            code_line_count += 1

    assert code_line_count > 0 or comment_line_count > 0

    if code_line_count > 0:
        result = __CELL_TYPE_CODE
    else:
        result = __CELL_TYPE_MARKDOWN

    return result


def prepare_markdown_cell(cell):
    """
    Removes markdown comments from each cell.

    :type cell: list

    this:
    [
        '#%%',
        '# # Python strings',
        '# - immutable',
        '# - fast',
        '# - silent but deadly'
    ]

    becomes this:
    [
        '%%',
        '# Python strings',
        '- immutable',
        '- fast',
        '- silent but deadly'
    ]
    """
    assert isinstance(cell, list)
    assert isinstance(cell[0], str)

    cell2 = []

    for line in cell:
        line2 = line
        if is_cell_separator(line2):
            line2 = remove_cell_separator_string(line2)
            # if the line is: '#%% string functions';
            # remaning will have "string functions".
            if line2:
                # if there is anything left, add it as a header.
                cell2.append("# " + line2)
        else:
            line2 = remove_if_starts_with(line, __COMMENT_STARTER).strip()
            cell2.append(line2)

    return cell2


def cell_ignored(cell_lines):
    """
    Returns True if the cell is to be ignored, False otherwise.

    The cell ignore string is as follows:

    # spyonde:ignore-cell
    """
    assert isinstance(cell_lines, list)

    if not hasattr(cell_ignored, "compiled_pattern"):
        # it doesn't exist yet, so initialize it once.
        cell_ignored.compiled_pattern = re.compile(r'\s*#*\s*spyonde\s*[:=]\s*ignore-cell\s*\Z')
        # \s whitespace
        # [:=] : or =
        # \Z : end of string

    result = False
    for line in cell_lines:
        if cell_ignored.compiled_pattern.match(line):
            result = True
            break

    return result


def align_comment_cells(cell_lines):
    """
    This is an idea to use multiline strings as comments, such as:

    :type cell_lines: list
    """
    # TODO: 7 align_comment_cells() implement
    return cell_lines


def remove_empty_cell_separator_leftovers(cell):
    """
    Returns a copy of a list without empty comments.

    https://github.com/caglartoklu/spyonde/issues/3

    cell is something like:
    [
        '# %%',
        '# - this is a cell without a header.',
        "# - that's it.",
        '# - see the next slide.',
        'print("hi")'
    ]

    Without this function;
    A Python code like this:

        # %%
        # - this is a cell without a header.
        # - that's it.
        # - see the next slide.
        print("hi")

    produced a Jupyter code cell like this:
        #
        # - this is a cell without a header.
        # - that's it.
        # - see the next slide.
        print("hi")
    """
    assert isinstance(cell, list)
    if cell:
        assert isinstance(cell[0], str)

    last_index_to_remove = None
    for i, line in enumerate(cell):
        if is_only_cell_separator(line):
            last_index_to_remove = i
        else:
            # we have hit the first non cell separator line.
            break

    if last_index_to_remove is not None:
        cell = cell[last_index_to_remove+1:]

    return cell


def remove_trailing_empty_elements(list1):
    """
    Returns a copy of a list without empty items from the end.
    The empty items at the start of the list and between remain intact.
    Example:
        list2 = ["", "a", "b", "c", "\t", "d", "  ", ""]
        list3 = remove_trailing_empty_elements(list2)
        print(list3)
        ['', 'a', 'b', 'c', '\t', 'd']
    """
    assert isinstance(list1, list)
    if list1:
        assert isinstance(list1[0], str)

    list2 = list1[:]
    indices_to_remove = []
    for i in range(len(list1)-1, -1, -1):
        line2 = list2[i].strip()
        if line2 == "":
            indices_to_remove.append(i)
        else:
            break

    # print(indices_to_remove)
    for i in indices_to_remove:
        list2.pop(i)
    return list2


def parse_cells(cells):
    """
    Parses cells and builds a data to be written to a file.

    :type cells: list

    Returns a data structure (parsed_cells) like:

    [
    ('markdown', ['# Python strings', '- immutable', '- fast']),
    ('markdown', ['# next slide will be great', '- code is coming']),
    ('code', ['#%% string defs', 's1 = "stuff"', 's2 = "another stuff"']),
    ('code', ['#%% printing strings', 'print(s1)', '# print the other.'])
    ]
    """
    assert isinstance(cells, list)
    assert isinstance(cells[0], list)
    assert isinstance(cells[0][0], str)

    # TODO: 7 align_comment_cells() call
    # cells = map(align_comment_cells, cells)

    parsed_cells = []
    for cell in cells:
        if cell_ignored(cell):
            continue
        cell_type = detect_cell_type(cell)
        if cell_type == __CELL_TYPE_MARKDOWN:
            cell = prepare_markdown_cell(cell)

        if cell_type == __CELL_TYPE_CODE:
            cell = remove_trailing_empty_elements(cell)

        parsed_cells.append((cell_type, cell))

    return parsed_cells


def build_cell_dict(cell_data):
    """
    Builds a dictionary for a single cell.
    This dictionary will later be used to create JSON data.

    :type cell_data: tuple

    cell_data would be one of the following:

    if it is markdown:
    ('markdown', ['# next slide will be great', '- code is coming']),

    if it is code:
    ('code', ['#%% string defs', 's1 = "stuff"', 's2 = "another stuff"']),

    example cell JSON:

    {
        "cell_type": "markdown",
        "metadata":
        {
            "slideshow":
            {
                 "slide_type": "slide"
            }
        },
        "source":
        [
            "# Python IDE and editors\n",
            "\n",
            "- Vim\n",
            "- EMACS\n",
            "- Spyder\n",
            "- PyCharm\n",
            "- and some others"
        ]
    },

    """
    assert isinstance(cell_data, tuple)
    cell_type = cell_data[0]
    # cell_type is either 'markdown' or 'code'

    lines = cell_data[1]
    # the lines as a list of strings.

    dct_cell = {}
    dct_cell["cell_type"] = cell_type
    dct_cell["metadata"] = {"slideshow": {"slide_type": "slide"}}
    dct_cell["source"] = []

    if cell_type == __CELL_TYPE_CODE:
        dct_cell["execution_count"] = None
        dct_cell["metadata"] = {"scrolled": True, "slideshow": {"slide_type": "slide"}}
        dct_cell["outputs"] = []

    lines = remove_empty_cell_separator_leftovers(lines)

    # there will be no trailing left overs.
    # if it would, they would be be starting a new cell.
    # lines = remove_empty_cell_separator_leftovers(list(reversed(lines)))

    for line in lines:
        if is_comment(line.strip()):
            # TODO: 6 use regex
            line = line.replace("#%%", "#", 1)
            line = line.replace("# %%", "#", 1)

            # TODO: 7 should we handle lines like following?
            # can str_consists_of_only() be used?
            # # #
            ##
        dct_cell["source"].append(line + "\n")

    return dct_cell


def build_notebook_json(data, pyversion):
    '''
    Iterates all the cell data, and returns a JSON string.

    :type data: list
    :type pyversion: str

    data:
    type  | len | value
    tuple | 2   | ('code', ['# %% demo.py\n', '# -*- coding: utf-8 -*-', '...])
    tuple | 2   | ('markdown', ['# Welcome to Tiny Python Course', '', '##...])
    tuple | 2   | ('code', ['# %% string definition', '', '# type inferenc...])
    tuple | 2   | ('code', ['# %% multi-line strings', '', 's3 = """', '1'...])
    tuple | 2   | ('code', ['# %% printing strings', '', 'print(s1)', '# w...])
    tuple | 2   | ('code', ['# %% and some loops', '', 'for a in range(10 ...])

    '''
    assert isinstance(data, list)
    assert isinstance(pyversion, str)

    all_cells_list = []
    for cell_data in data:
        cell_dict = build_cell_dict(cell_data)
        all_cells_list.append(cell_dict)

    all_cells_as_json = json.dumps(all_cells_list, indent=4)

    metadata = """
,
 "metadata": {
  "celltoolbar": "Slideshow",
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "%s"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
    """ % (pyversion)

    output = """
{
 "cells":
    """ + all_cells_as_json + metadata

    return output.strip()


def generate_output_file_name(input_file_name):
    """
    Generates an output file name from input file name.

    :type input_file_name: str
    """
    assert isinstance(input_file_name, str)
    output_file_name = input_file_name + ".gen.ipynb"
    return output_file_name


def prepare_temp_file_name(input_file_name, encoding="utf8"):
    """
    Adds a last empty cell to the temp copy of input_file_name and returns it.
    """
    assert isinstance(input_file_name, str)

    handle = open(input_file_name, encoding=encoding)
    content = handle.read()
    handle.close()

    content = content + """
#%% end

# - end.
    """

    # string can not be written to NamedTemporaryFile directly,
    # so convert it to bytes.
    content_bytes = content.encode()

    handle = tempfile.NamedTemporaryFile(delete=False)
    file_name = handle.name
    handle.write(content_bytes)
    handle.close()
    return file_name


def convert_file(input_file_name, args_dict):
    """
    Converts a .py file to a .ipynb file.
    .py file must be written in a specific format to be converter.

    :type input_file_name: str
    :type args_dict: dict

    args_dict:
    {
        'output': 'outfile.ipynb',
        'pyversion': '3.8',
        'overwrite_confirmed': True,
        'input': 'demo.py'
    }
    """

    assert isinstance(input_file_name, str)
    assert isinstance(args_dict, dict)

    output_file_name = args_dict["output"]
    assert isinstance(output_file_name, str) or output_file_name is None

    if not output_file_name:
        output_file_name = generate_output_file_name(input_file_name)

    cells = split_to_cells(input_file_name)

    data = parse_cells(cells)

    pyversion = args_dict["pyversion"]
    output_as_str = build_notebook_json(data, pyversion)

    if os.path.isfile(output_file_name):
        # file already exists.
        # will it be overwritten?
        to_be_written = False
        overwrite_confirmed = args_dict["overwrite_confirmed"]
        if overwrite_confirmed:
            to_be_written = True
        else:
            print("File exists: " + output_file_name)
            print("Do you want to override? y/n")
            answer = answer_in_yes_or_no(">>> ")
            if answer:
                # the user has selected "yes"
                to_be_written = True
    else:
        # file does not exists.
        to_be_written = True

    if to_be_written:
        # save the output as JSON.
        handle = open(output_file_name, "w", encoding="utf8")
        handle.write(output_as_str)
        handle.close()
        print("created: ", output_file_name)
    else:
        print("file is not written.")

    return output_as_str


def main():
    """
    The main entry point of this module.
    """
    raise ValueError("this module is not supposed to be run on its own.")


def main_trial():
    """
    The main entry point of this module in development mode.
    """
    module_path = os.path.dirname(os.path.realpath(__file__))
    input_file_path = os.path.join(module_path, "../")
    input_file_path = os.path.join(input_file_path, "examples")
    input_file_name = os.path.join(input_file_path, "demo.py")

    args_dict = {'output': None, 'pyversion': '3.8', 'overwrite_confirmed': False}
    args_dict["input"] = input_file_name

    convert_file(input_file_name, args_dict)


def start_command_line():
    """
    When called from command line, this function is executed.
    """
    print("Spyonde started.")
    parser = argparse.ArgumentParser()

    help1 = "List of .py files to be converted."
    parser.add_argument('files', nargs='+', help=help1)

    help1 = 'The version string to be embedded into the Jupyter file. It is "3.7.4" by default.'
    parser.add_argument('--nbversion', nargs='?', help=help1, default="3.7.4")

    help1 = 'If provided, automatically confirms overwrite. It does not overwrites files by default.'
    parser.add_argument('--overwrite', action='store_true', help=help1)

    args = parser.parse_args()

    print("args:")
    print(" ", args)

    args_dict = {}

    args_dict["output"] = None
    args_dict["pyversion"] = args.nbversion
    args_dict["overwrite_confirmed"] = args.overwrite

    for file_name in args.files:
        if os.path.isfile(file_name):
            args_dict["input"] = file_name
            convert_file(file_name, args_dict)
        else:
            print("NOT a file: ", file_name)


if __name__ == '__main__':
    main()
    # main_trial()
