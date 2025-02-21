import unittest

from aggkit import calc


class CalcTests(unittest.TestCase):
    def test_combined_charge(self):
        self.assertEqual(calc.combined_charge(0), 20006)
        self.assertEqual(calc.combined_charge(1), 20006)
        self.assertEqual(calc.combined_charge(10), 5010006)
        self.assertEqual(calc.combined_charge(11), 5010027)
