import unittest

from aggkit.deps import textfmt


class TextfmtTests(unittest.TestCase):
    def test_pad_left(self):
        self.assertEqual(textfmt.pad_start("ab", 5), "   ab")

    def test_pad_left_fill(self):
        self.assertEqual(textfmt.pad_start("7", 3, "0"), "007")
