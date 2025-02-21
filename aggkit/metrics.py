"""Python wrappers over the C aggregation kernels."""
import math

from .native import check, ffi, lib


class Stats:
    """Streaming count/mean/variance/min/max (Welford) held in a C struct."""

    def __init__(self):
        self._s = ffi.new("agg_stats *")
        check(lib.agg_stats_init(self._s), "stats init")

    def push(self, x):
        check(lib.agg_stats_push(self._s, float(x)), "stats push")
        return self

    def extend(self, xs):
        for x in xs:
            self.push(x)
        return self

    @property
    def count(self):
        return self._s.count

    @property
    def sum(self):
        return self._s.sum

    @property
    def mean(self):
        return self._s.mean if self._s.count else math.nan

    @property
    def min(self):
        return self._s.min if self._s.count else math.nan

    @property
    def max(self):
        return self._s.max if self._s.count else math.nan

    def variance(self):
        out = ffi.new("double *")
        rc = lib.agg_stats_variance(self._s, out)
        return math.nan if rc == -2 else (check(rc, "variance"), out[0])[1]

    def stddev(self):
        v = self.variance()
        return math.nan if math.isnan(v) else math.sqrt(v)

    def merged(self, other):
        result = Stats()
        check(lib.agg_stats_merge(result._s, self._s, other._s), "stats merge")
        return result


class Histogram:
    def __init__(self, lo, hi, buckets=20):
        self._h = ffi.new("agg_hist *")
        check(lib.agg_hist_init(self._h, float(lo), float(hi), buckets), "hist init")

    def push(self, x):
        check(lib.agg_hist_push(self._h, float(x)), "hist push")
        return self

    @property
    def total(self):
        return self._h.total

    def counts(self):
        return list(self._h.counts[0:self._h.buckets])

    def percentile(self, p):
        out = ffi.new("double *")
        rc = lib.agg_hist_percentile(self._h, float(p), out)
        if rc == -2:
            return math.nan
        check(rc, "percentile")
        return out[0]


def window_sums(values, window):
    n = len(values)
    if window > n:
        return []
    xs = ffi.new("double[]", [float(v) for v in values])
    out = ffi.new("double[]", n - window + 1)
    check(lib.agg_window_sum(xs, n, window, out), "window sum")
    return list(out)
