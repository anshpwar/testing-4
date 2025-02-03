import io
import json
import pathlib
import tempfile
import unittest

from aggkit import alerts, cli, ingest, rollup


class EndToEndTests(unittest.TestCase):
    def test_file_to_alert_pipeline(self):
        lines = [f"{1000 + i * 60}|api.latency_ms|{10 + (i % 3)}|region=eu" for i in range(12)]
        lines.append("1720|api.latency_ms|400|region=eu")
        events, errors = ingest.parse_stream(lines)
        self.assertEqual(errors, [])
        history = [e.value for e in events[:-1]]
        alert = alerts.evaluate("api.latency_ms", history, events[-1].value, level=3)
        self.assertIsNotNone(alert)
        summary = rollup.summarize(events, by_tags=("region",))
        self.assertEqual(summary[("api.latency_ms", ("region", "eu"))]["count"], 13)

    def test_cli_round_trip_over_generated_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "e.txt"
            path.write_text("\n".join(f"{i}|queue.depth|{i * 2}" for i in range(1, 51)) + "\n")
            out = io.StringIO()
            self.assertEqual(cli.main(["summarize", str(path)], out=out), 0)
        row = json.loads(out.getvalue())["series"][0]
        self.assertEqual((row["count"], row["min"], row["max"]), (50, 2.0, 100.0))
