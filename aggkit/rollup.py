"""Group events by metric and tags and roll them up with the native kernels."""
from collections import defaultdict

from . import rules
from .metrics import Histogram, Stats, window_sums


def series_key(event, by_tags=()):
    return (event.metric,) + tuple((t, event.tags.get(t, "")) for t in by_tags)


def group(events, by_tags=()):
    out = defaultdict(list)
    for e in events:
        out[series_key(e, by_tags)].append(e)
    return out


def summarize(events, by_tags=(), max_series=None):
    """Per-series count/mean/stddev/min/max. Cardinality is capped by plan tier."""
    groups = group(events, by_tags)
    if max_series is not None and len(groups) > max_series:
        raise ValueError(f"{len(groups)} series exceeds the plan limit of {max_series}")
    result = {}
    for key, evs in sorted(groups.items()):
        s = Stats().extend(e.value for e in evs)
        result[key] = {"count": s.count, "mean": s.mean, "stddev": s.stddev(), "min": s.min, "max": s.max}
    return result


def minute_buckets(events):
    buckets = defaultdict(list)
    for e in events:
        buckets[e.ts - e.ts % 60].append(e.value)
    return dict(sorted(buckets.items()))


def moving_totals(events, window):
    sums = {k: sum(v) for k, v in minute_buckets(events).items()}
    return list(sums), window_sums(list(sums.values()), window)


def latency_percentiles(events, metric, lo, hi, plan_width=None):
    width = plan_width or (hi - lo)
    h = Histogram(lo, hi, rules.histogram_buckets(width))
    for e in events:
        if e.metric == metric:
            h.push(e.value)
    return {p: h.percentile(p) for p in (50, 90, 99)}
