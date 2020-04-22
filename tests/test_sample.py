# -*- coding: utf-8 -*-

"""
Includes tests for spyondemain module.
"""


# python setup.py test

import os
import sys
import unittest


# add current directory to sys.path
_MODULE_PATH = os.path.dirname(os.path.realpath(__file__))
if _MODULE_PATH not in sys.path:
    sys.path.append(_MODULE_PATH)

# add spyonde directory to sys.path
_SPYONDE_DIR = os.path.abspath(os.path.join(_MODULE_PATH, "../spyonde"))
if _SPYONDE_DIR not in sys.path:
    sys.path.append(_SPYONDE_DIR)

# the following line will raise a warning in development time,
# but it will work in runtime.
import spyondemain  # pylint: disable=C0413,E0402,E0401
# C0413: import should be places at the top of the module.
# E0402: module level import not at top of file
# E0401: Unable to import 'spyondemain' (import-error)


class TestStartsWith(unittest.TestCase):
    """
    Tests starts_with() method.
    """

    def test_starts_with_true(self):
        """
        Tests the starts_with() method.
        """
        expected = True

        haystack = ["#%%", "# %%", "# <codecell>"]
        actual = spyondemain.starts_with(haystack, "#%% python strings")
        self.assertEqual(expected, actual)

        haystack = ["#%%", "# %%", "# <codecell>"]
        actual = spyondemain.starts_with(haystack, "#%%")
        self.assertEqual(expected, actual)

        haystack = ["#%%", "# %%", "# <codecell>"]
        actual = spyondemain.starts_with(haystack, "# %%")
        self.assertEqual(expected, actual)

        haystack = ["#%%", "# %%", "# <codecell>"]
        actual = spyondemain.starts_with(haystack, "# <codecell>")
        self.assertEqual(expected, actual)

    def test_starts_with_false(self):
        """
        Tests the starts_with() method.
        """
        expected = False

        haystack = ["#%%", "# %%", "# <codecell>"]
        actual = spyondemain.starts_with(haystack, "#  %% python strings")
        self.assertEqual(expected, actual)

        haystack = ["#%%", "# %%", "# <codecell>"]
        actual = spyondemain.starts_with(haystack, "#  %%")
        self.assertEqual(expected, actual)

        haystack = ["#%%", "# %%", "# <codecell>"]
        actual = spyondemain.starts_with(haystack, " # %%")
        self.assertEqual(expected, actual)

        haystack = ["#%%", "# %%", "# <codecell>"]
        actual = spyondemain.starts_with(haystack, "#  <codecell>")
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
