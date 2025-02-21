import unittest

from aggkit import contract, consumer_82


class ExportTests(unittest.TestCase):
    def test_export_line(self):
        rec = contract.Record("TX-9", 700, "open")
        self.assertEqual(consumer_82.export_line(rec), "TX-9,700")
