import unittest

from aggkit import rollup, rules
from aggkit.ingest import Event


def events():
    out = []
    for i in range(6):
        out.append(Event(1000 + i * 30, "api.latency_ms", 10.0 + i, {"region": "eu" if i % 2 else "us"}))
    out.append(Event(1000, "api.errors", 1.0, {}))
    return out


class RollupTests(unittest.TestCase):
    def test_summarize_by_metric(self):
        s = rollup.summarize(events())
        self.assertEqual(s[("api.latency_ms",)]["count"], 6)
        self.assertAlmostEqual(s[("api.latency_ms",)]["mean"], 12.5)
        self.assertEqual(s[("api.errors",)]["count"], 1)

    def test_summarize_by_tag_splits_series(self):
        s = rollup.summarize(events(), by_tags=("region",))
        self.assertIn(("api.latency_ms", ("region", "eu")), s)
        self.assertEqual(s[("api.latency_ms", ("region", "us"))]["count"], 3)

    def test_cardinality_cap(self):
        with self.assertRaises(ValueError):
            rollup.summarize(events(), by_tags=("region",), max_series=2)

    def test_minute_buckets_and_moving_totals(self):
        buckets = rollup.minute_buckets(events())
        self.assertEqual(list(buckets), [960, 1020, 1080, 1140])
        starts, sums = rollup.moving_totals(events(), 2)
        self.assertEqual(len(sums), len(starts) - 1)

    def test_latency_percentiles_use_policy_bucket_count(self):
        evs = [Event(i, "lat", float(i)) for i in range(1, 101)]
        p = rollup.latency_percentiles(evs, "lat", 0, 100)
        self.assertLessEqual(p[50], p[90])
        self.assertLessEqual(p[90], p[99])
        self.assertGreaterEqual(rules.histogram_buckets(100), 1)
