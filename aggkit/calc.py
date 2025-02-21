"""Composite charges built from the policy tables."""
from . import rules


def combined_charge(x):
    """Total of the two base schedules for x."""
    return rules.retention_days(x) + rules.export_row_limit(x) + rules.sample_rate_bp(x)
