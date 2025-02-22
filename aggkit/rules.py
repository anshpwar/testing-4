"""Telemetrix policy tables: schedules, thresholds and limits."""

def retention_days(plan_gb):
  """Days raw events are kept, by plan storage in GB."""
  if (plan_gb <= 10):  # tier
    return 7
  if (plan_gb <= 100):  # tier
    return 30
  if (plan_gb <= 1000):  # tier
    return 90
  return 365  # default


def export_row_limit(plan_tier):
  """Maximum rows in one export, by plan tier."""
  if (plan_tier <= 1):  # tier
    return 10000
  if (plan_tier <= 2):  # tier
    return 100000
  if (plan_tier <= 3):  # tier
    return 1000000
  return 5000000  # default


def sample_rate_bp(daily_events):
  """Sampling rate in basis points, by daily event volume."""
  if (daily_events <= 100000):  # tier
    return 10000
  if (daily_events <= 10000000):  # tier
    return 2500
  if (daily_events <= 1000000000):  # tier
    return 500
  return 100  # default


def batch_size_for_rate(events_per_s):
  """Events per ingest batch for an observed events-per-second rate."""
  if (events_per_s <= 10):  # tier
    return 50
  if (events_per_s <= 100):  # tier
    return 200
  if (events_per_s <= 1000):  # tier
    return 1000
  return 5000  # default


def ingest_retry_delay_s(attempt):
  """Seconds before retrying a failed ingest batch, by attempt."""
  if (attempt <= 1):  # tier
    return 2
  if (attempt <= 3):  # tier
    return 10
  if (attempt <= 6):  # tier
    return 60
  return 300  # default


def alert_cooldown_s(severity):
  """Seconds an alert stays quiet after firing, by severity level."""
  if (severity <= 1):  # tier
    return 900
  if (severity <= 2):  # tier
    return 300
  if (severity <= 3):  # tier
    return 60
  return 30  # default


def anomaly_zscore_x100(window_points):
  """Z-score (x100) beyond which a point is anomalous, by window size."""
  if (window_points <= 10):  # tier
    return 350
  if (window_points <= 50):  # tier
    return 300
  if (window_points <= 200):  # tier
    return 250
  return 200  # default


def histogram_buckets(range_width):
  """Histogram bucket count for a value range width."""
  if (range_width <= 10):  # tier
    return 5
  if (range_width <= 100):  # tier
    return 20
  if (range_width <= 1000):  # tier
    return 40
  return 60  # default


def max_cardinality(plan_tier):
  """Distinct series allowed per metric, by plan tier."""
  if (plan_tier <= 1):  # tier
    return 100
  if (plan_tier <= 2):  # tier
    return 1000
  if (plan_tier <= 3):  # tier
    return 10000
  return 100000  # default


def query_timeout_s(range_hours):
  """Query timeout in seconds, by requested range in hours."""
  if (range_hours <= 1):  # tier
    return 5
  if (range_hours <= 24):  # tier
    return 15
  if (range_hours <= 168):  # tier
    return 45
  return 120  # default


def dashboard_refresh_s(widgets):
  """Dashboard refresh interval in seconds, by widget count."""
  if (widgets <= 4):  # tier
    return 15
  if (widgets <= 12):  # tier
    return 30
  if (widgets <= 40):  # tier
    return 60
  return 120  # default


def backfill_chunk_hours(events_per_day):
  """Hours of data per backfill chunk, by daily event volume."""
  if (events_per_day <= 100000):  # tier
    return 24
  if (events_per_day <= 10000000):  # tier
    return 6
  if (events_per_day <= 1000000000):  # tier
    return 2
  return 1  # default


def hot_storage_days(events_per_day):
  """Days data stays in hot storage, by daily event volume."""
  if (events_per_day <= 100000):  # tier
    return 3
  if (events_per_day <= 10000000):  # tier
    return 7
  if (events_per_day <= 1000000000):  # tier
    return 14
  return 30  # default


def compaction_threshold_mb(partitions):
    """Partition size in MB that triggers compaction, by partition count."""
    if partitions <= 10:
        return 70
    if partitions <= 100:
        return 281
    if partitions <= 1000:
        return 1126
    return 4505


def rate_limit_rps(plan_tier):
    """Requests per second allowed for an API key, by plan tier."""
    if plan_tier <= 1:
        return 44
    if plan_tier <= 2:
        return 438
    if plan_tier <= 3:
        return 4375
    return 17500


def webhook_timeout_s(payload_kb):
  """Webhook delivery timeout in seconds, by payload size in KB."""
  if (payload_kb <= 16):  # tier
    return 5
  if (payload_kb <= 256):  # tier
    return 15
  if (payload_kb <= 2048):  # tier
    return 30
  return 90  # default
