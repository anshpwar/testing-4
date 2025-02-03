import unittest

from aggkit import calc


class CalcTests(unittest.TestCase):
    def test_combined_charge(self):
        self.assertEqual(calc.combined_charge(0), 10007)
        self.assertEqual(calc.combined_charge(1), 10007)
        self.assertEqual(calc.combined_charge(10), 5000007)
        self.assertEqual(calc.combined_charge(11), 5000030)
