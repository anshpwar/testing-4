import unittest

from aggkit import ingest, rules


class ParseTests(unittest.TestCase):
    def test_valid_line_with_tags(self):
        e = ingest.parse_line("1700000000|api.latency_ms|12.5|region=eu,tier=pro")
        self.assertEqual((e.ts, e.metric, e.value), (1700000000, "api.latency_ms", 12.5))
        self.assertEqual(e.tags, {"region": "eu", "tier": "pro"})

    def test_rejections(self):
        for bad in ("1|m", "x|m|1", "1|m!|1", "1|m|abc", "1|m|nan", "1|m|1|novalue", "1||2"):
            with self.assertRaises(ingest.IngestError, msg=bad):
                ingest.parse_line(bad)

    def test_stream_collects_errors_with_line_numbers(self):
        lines = ["# comment", "1|m|1", "", "bad", "2|m|2"]
        events, errors = ingest.parse_stream(lines)
        self.assertEqual(len(events), 2)
        self.assertEqual([n for n, _ in errors], [4])


class BatchTests(unittest.TestCase):
    def test_batch_size_follows_policy(self):
        events = [ingest.Event(i, "m", 1.0) for i in range(500)]
        size = max(1, rules.batch_size_for_rate(300))
        out = ingest.batches(events, 300)
        self.assertEqual(len(out[0]), min(size, 500))
        self.assertEqual(sum(len(b) for b in out), 500)

    def test_retry_delays_follow_policy(self):
        self.assertEqual(ingest.retry_delays(3), [rules.ingest_retry_delay_s(i) for i in (1, 2, 3)])
