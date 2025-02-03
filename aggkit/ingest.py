"""Event ingestion: parse pipe-delimited telemetry lines into validated events.

Line format:  <unix_ts>|<metric>|<value>|<k=v,k=v>
"""
from dataclasses import dataclass, field

from . import rules


class IngestError(ValueError):
    pass


@dataclass(frozen=True)
class Event:
    ts: int
    metric: str
    value: float
    tags: dict = field(default_factory=dict)


def parse_line(line):
    parts = line.rstrip("\n").split("|")
    if len(parts) not in (3, 4):
        raise IngestError(f"expected 3 or 4 fields, got {len(parts)}")
    ts_s, metric, value_s = parts[:3]
    if not ts_s.isdigit():
        raise IngestError(f"bad timestamp {ts_s!r}")
    if not metric or not all(c.isalnum() or c in "._" for c in metric):
        raise IngestError(f"bad metric name {metric!r}")
    try:
        value = float(value_s)
    except ValueError:
        raise IngestError(f"bad value {value_s!r}") from None
    if value != value or value in (float("inf"), float("-inf")):
        raise IngestError("value must be finite")
    tags = {}
    if len(parts) == 4 and parts[3]:
        for pair in parts[3].split(","):
            key, sep, val = pair.partition("=")
            if not sep or not key:
                raise IngestError(f"bad tag {pair!r}")
            tags[key] = val
    return Event(int(ts_s), metric, value, tags)


def parse_stream(lines):
    """Return (events, errors) where errors is a list of (line_number, message)."""
    events, errors = [], []
    for n, line in enumerate(lines, 1):
        if not line.strip() or line.startswith("#"):
            continue
        try:
            events.append(parse_line(line))
        except IngestError as exc:
            errors.append((n, str(exc)))
    return events, errors


def batches(events, events_per_second):
    """Split events into batches sized by the ingest policy for the observed rate."""
    size = max(1, rules.batch_size_for_rate(events_per_second))
    return [events[i:i + size] for i in range(0, len(events), size)]


def retry_delays(attempts):
    return [rules.ingest_retry_delay_s(a) for a in range(1, attempts + 1)]
