"""Composite charges built from the policy tables."""
from . import rules


def combined_charge(x):
    """Total of the two base schedules for x."""
    return rules.retention_days_v2(x) + rules.export_row_limit(x)
