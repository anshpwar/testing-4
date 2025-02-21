import math
import unittest

from aggkit import metrics
from aggkit.native import NativeError, ffi, lib


class StatsTests(unittest.TestCase):
    def test_matches_reference_moments(self):
        s = metrics.Stats().extend([2, 4, 4, 4, 5, 5, 7, 9])
        self.assertEqual(s.count, 8)
        self.assertAlmostEqual(s.mean, 5.0)
        self.assertAlmostEqual(s.variance(), 32 / 7)
        self.assertEqual((s.min, s.max), (2.0, 9.0))

    def test_empty_and_single_value(self):
        s = metrics.Stats()
        self.assertTrue(math.isnan(s.mean) and math.isnan(s.variance()))
        s.push(3)
        self.assertTrue(math.isnan(s.stddev()))

    def test_nan_is_rejected(self):
        with self.assertRaises(NativeError):
            metrics.Stats().push(float("nan"))

    def test_merge_equals_single_pass(self):
        a, b, whole = metrics.Stats(), metrics.Stats(), metrics.Stats()
        for i in range(1, 11):
            (a if i <= 4 else b).push(i * 1.5)
            whole.push(i * 1.5)
        m = a.merged(b)
        self.assertEqual(m.count, whole.count)
        self.assertAlmostEqual(m.variance(), whole.variance())

    def test_struct_layout_matches_library(self):
        self.assertEqual(ffi.sizeof("agg_stats"), lib.agg_sizeof_stats())
        self.assertEqual(ffi.sizeof("agg_hist"), lib.agg_sizeof_hist())


class SumTests(unittest.TestCase):
    def test_running_sum(self):
        self.assertEqual(metrics.Stats().extend([1, 2, 3.5]).sum, 6.5)


class WindowTests(unittest.TestCase):
    def test_window_sums(self):
        self.assertEqual(metrics.window_sums([1, 2, 3, 4, 5], 3), [6.0, 9.0, 12.0])

    def test_window_larger_than_series(self):
        self.assertEqual(metrics.window_sums([1, 2], 3), [])
