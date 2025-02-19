import unittest

from aggkit import consumer_80


class ColumnTests(unittest.TestCase):
    def test_column(self):
        self.assertEqual(consumer_80.column("ab"), "          ab")
