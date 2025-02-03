import math
import unittest

from aggkit import metrics
from aggkit.native import NativeError


class HistogramTests(unittest.TestCase):
    def test_counts_and_clamping(self):
        h = metrics.Histogram(0, 100, 10)
        for x in (5, 15, 99.9, -50, 500):
            h.push(x)
        self.assertEqual(h.total, 5)
        self.assertEqual(h.counts()[0], 2)
        self.assertEqual(h.counts()[9], 2)

    def test_percentiles(self):
        h = metrics.Histogram(0, 100, 10)
        for i in range(100):
            h.push(i + 0.5)
        self.assertAlmostEqual(h.percentile(50), 50.0)
        self.assertAlmostEqual(h.percentile(99), 100.0)

    def test_empty_histogram_percentile_is_nan(self):
        self.assertTrue(math.isnan(metrics.Histogram(0, 10, 5).percentile(50)))

    def test_invalid_construction(self):
        with self.assertRaises(NativeError):
            metrics.Histogram(5, 5, 10)
        with self.assertRaises(NativeError):
            metrics.Histogram(0, 10, 1000)
