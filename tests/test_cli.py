import io
import json
import pathlib
import tempfile
import unittest

from aggkit import cli


class CliTests(unittest.TestCase):
    def run_cli(self, text, extra=()):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "events.txt"
            path.write_text(text)
            out = io.StringIO()
            rc = cli.main(["summarize", str(path), *extra], out=out)
        return rc, json.loads(out.getvalue())

    def test_summarize_ok(self):
        rc, data = self.run_cli("1|m|1|r=a\n2|m|3|r=b\n")
        self.assertEqual(rc, 0)
        self.assertEqual(data["events"], 2)
        self.assertEqual(data["series"][0]["mean"], 2.0)

    def test_rejected_lines_change_exit_code(self):
        rc, data = self.run_cli("1|m|1\nbroken\n")
        self.assertEqual((rc, data["rejected"]), (2, 1))

    def test_group_by_tag(self):
        rc, data = self.run_cli("1|m|1|r=a\n2|m|3|r=b\n", ("--by", "r"))
        self.assertEqual(len(data["series"]), 2)
