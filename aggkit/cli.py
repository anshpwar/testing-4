"""Command line: summarise a telemetry file.   python -m aggkit.cli summarize FILE [--by tag]"""
import argparse
import json
import sys

from . import ingest, rollup


def main(argv=None, out=None):
    out = out or sys.stdout
    ap = argparse.ArgumentParser(prog="aggkit")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("summarize")
    s.add_argument("file")
    s.add_argument("--by", action="append", default=[])
    args = ap.parse_args(argv)
    with open(args.file) as fh:
        events, errors = ingest.parse_stream(fh)
    summary = rollup.summarize(events, tuple(args.by))
    rows = [{"series": [str(p) for p in key], **vals} for key, vals in summary.items()]
    json.dump({"events": len(events), "rejected": len(errors), "series": rows}, out, indent=2, sort_keys=True)
    out.write("\n")
    return 0 if not errors else 2


if __name__ == "__main__":
    sys.exit(main())
