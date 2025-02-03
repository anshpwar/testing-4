"""Threshold and anomaly alerting with policy-driven cool-downs."""
from dataclasses import dataclass

from . import rules
from .metrics import Stats


@dataclass(frozen=True)
class Alert:
    metric: str
    level: int
    reason: str
    cooldown_s: int


def zscore(history, x):
    s = Stats().extend(history)
    sd = s.stddev()
    if s.count < 3 or sd != sd or sd == 0:
        return 0.0
    return (x - s.mean) / sd


def evaluate(metric, history, latest, level=1, threshold=None):
    """Return an Alert when `latest` breaches the fixed threshold or is a z-score outlier."""
    window = len(history)
    limit = rules.anomaly_zscore_x100(window) / 100.0
    z = zscore(history, latest)
    if threshold is not None and latest > threshold:
        return Alert(metric, level, f"{latest} above threshold {threshold}", rules.alert_cooldown_s(level))
    if abs(z) >= limit:
        return Alert(metric, level, f"z-score {z:.2f} beyond {limit:.2f}", rules.alert_cooldown_s(level))
    return None


def suppressed(last_fired_ts, now_ts, level):
    return last_fired_ts is not None and now_ts - last_fired_ts < rules.alert_cooldown_s(level)
