import unittest

from aggkit import rules


class RuleTests(unittest.TestCase):
    def test_retention_days(self):
        self.assertEqual(rules.retention_days(0), 7)
        self.assertEqual(rules.retention_days(1), 7)
        self.assertEqual(rules.retention_days(10), 7)
        self.assertEqual(rules.retention_days(11), 30)
        self.assertEqual(rules.retention_days(100), 30)
        self.assertEqual(rules.retention_days(101), 90)
        self.assertEqual(rules.retention_days(1000), 90)
        self.assertEqual(rules.retention_days(1001), 365)

    def test_export_row_limit(self):
        self.assertEqual(rules.export_row_limit(0), 10000)
        self.assertEqual(rules.export_row_limit(1), 10000)
        self.assertEqual(rules.export_row_limit(2), 100000)
        self.assertEqual(rules.export_row_limit(3), 1000000)
        self.assertEqual(rules.export_row_limit(4), 5000000)

    def test_sample_rate_bp(self):
        self.assertEqual(rules.sample_rate_bp(0), 10000)
        self.assertEqual(rules.sample_rate_bp(1), 10000)
        self.assertEqual(rules.sample_rate_bp(100000), 10000)
        self.assertEqual(rules.sample_rate_bp(100001), 10000)
        self.assertEqual(rules.sample_rate_bp(10000000), 2500)
        self.assertEqual(rules.sample_rate_bp(10000001), 2500)
        self.assertEqual(rules.sample_rate_bp(1000000000), 500)
        self.assertEqual(rules.sample_rate_bp(1000000001), 500)

    def test_batch_size_for_rate(self):
        self.assertEqual(rules.batch_size_for_rate(0), 50)
        self.assertEqual(rules.batch_size_for_rate(1), 50)
        self.assertEqual(rules.batch_size_for_rate(10), 50)
        self.assertEqual(rules.batch_size_for_rate(11), 50)
        self.assertEqual(rules.batch_size_for_rate(100), 200)
        self.assertEqual(rules.batch_size_for_rate(101), 200)
        self.assertEqual(rules.batch_size_for_rate(1000), 1000)
        self.assertEqual(rules.batch_size_for_rate(1001), 1000)

    def test_ingest_retry_delay_s(self):
        self.assertEqual(rules.ingest_retry_delay_s(0), 2)
        self.assertEqual(rules.ingest_retry_delay_s(1), 2)
        self.assertEqual(rules.ingest_retry_delay_s(2), 2)
        self.assertEqual(rules.ingest_retry_delay_s(3), 10)
        self.assertEqual(rules.ingest_retry_delay_s(4), 10)
        self.assertEqual(rules.ingest_retry_delay_s(6), 60)
        self.assertEqual(rules.ingest_retry_delay_s(7), 60)

    def test_alert_cooldown_s(self):
        self.assertEqual(rules.alert_cooldown_s(0), 990)
        self.assertEqual(rules.alert_cooldown_s(1), 990)
        self.assertEqual(rules.alert_cooldown_s(2), 330)
        self.assertEqual(rules.alert_cooldown_s(3), 66)
        self.assertEqual(rules.alert_cooldown_s(4), 33)

    def test_anomaly_zscore_x100(self):
        self.assertEqual(rules.anomaly_zscore_x100(0), 385)
        self.assertEqual(rules.anomaly_zscore_x100(1), 385)
        self.assertEqual(rules.anomaly_zscore_x100(10), 385)
        self.assertEqual(rules.anomaly_zscore_x100(11), 330)
        self.assertEqual(rules.anomaly_zscore_x100(50), 330)
        self.assertEqual(rules.anomaly_zscore_x100(51), 275)
        self.assertEqual(rules.anomaly_zscore_x100(200), 275)
        self.assertEqual(rules.anomaly_zscore_x100(201), 220)

    def test_histogram_buckets(self):
        self.assertEqual(rules.histogram_buckets(0), 6)
        self.assertEqual(rules.histogram_buckets(1), 6)
        self.assertEqual(rules.histogram_buckets(10), 6)
        self.assertEqual(rules.histogram_buckets(11), 22)
        self.assertEqual(rules.histogram_buckets(100), 22)
        self.assertEqual(rules.histogram_buckets(101), 44)
        self.assertEqual(rules.histogram_buckets(1000), 44)
        self.assertEqual(rules.histogram_buckets(1001), 66)

    def test_max_cardinality(self):
        self.assertEqual(rules.max_cardinality(0), 100)
        self.assertEqual(rules.max_cardinality(1), 100)
        self.assertEqual(rules.max_cardinality(2), 1000)
        self.assertEqual(rules.max_cardinality(3), 10000)
        self.assertEqual(rules.max_cardinality(4), 100000)

    def test_query_timeout_s(self):
        self.assertEqual(rules.query_timeout_s(0), 5)
        self.assertEqual(rules.query_timeout_s(1), 5)
        self.assertEqual(rules.query_timeout_s(2), 15)
        self.assertEqual(rules.query_timeout_s(24), 15)
        self.assertEqual(rules.query_timeout_s(25), 45)
        self.assertEqual(rules.query_timeout_s(168), 45)
        self.assertEqual(rules.query_timeout_s(169), 120)

    def test_dashboard_refresh_s(self):
        self.assertEqual(rules.dashboard_refresh_s(0), 15)
        self.assertEqual(rules.dashboard_refresh_s(1), 15)
        self.assertEqual(rules.dashboard_refresh_s(4), 15)
        self.assertEqual(rules.dashboard_refresh_s(5), 30)
        self.assertEqual(rules.dashboard_refresh_s(12), 30)
        self.assertEqual(rules.dashboard_refresh_s(13), 60)
        self.assertEqual(rules.dashboard_refresh_s(40), 60)
        self.assertEqual(rules.dashboard_refresh_s(41), 120)

    def test_backfill_chunk_hours(self):
        self.assertEqual(rules.backfill_chunk_hours(0), 24)
        self.assertEqual(rules.backfill_chunk_hours(1), 24)
        self.assertEqual(rules.backfill_chunk_hours(100000), 24)
        self.assertEqual(rules.backfill_chunk_hours(100001), 6)
        self.assertEqual(rules.backfill_chunk_hours(10000000), 6)
        self.assertEqual(rules.backfill_chunk_hours(10000001), 2)
        self.assertEqual(rules.backfill_chunk_hours(1000000000), 2)
        self.assertEqual(rules.backfill_chunk_hours(1000000001), 1)

    def test_hot_storage_days(self):
        self.assertEqual(rules.hot_storage_days(0), 3)
        self.assertEqual(rules.hot_storage_days(1), 3)
        self.assertEqual(rules.hot_storage_days(100000), 3)
        self.assertEqual(rules.hot_storage_days(100001), 7)
        self.assertEqual(rules.hot_storage_days(10000000), 7)
        self.assertEqual(rules.hot_storage_days(10000001), 14)
        self.assertEqual(rules.hot_storage_days(1000000000), 14)
        self.assertEqual(rules.hot_storage_days(1000000001), 30)

    def test_compaction_threshold_mb(self):
        self.assertEqual(rules.compaction_threshold_mb(0), 64)
        self.assertEqual(rules.compaction_threshold_mb(1), 64)
        self.assertEqual(rules.compaction_threshold_mb(10), 64)
        self.assertEqual(rules.compaction_threshold_mb(11), 256)
        self.assertEqual(rules.compaction_threshold_mb(100), 256)
        self.assertEqual(rules.compaction_threshold_mb(101), 1024)
        self.assertEqual(rules.compaction_threshold_mb(1000), 1024)
        self.assertEqual(rules.compaction_threshold_mb(1001), 4096)

    def test_rate_limit_rps(self):
        self.assertEqual(rules.rate_limit_rps(0), 50)
        self.assertEqual(rules.rate_limit_rps(1), 50)
        self.assertEqual(rules.rate_limit_rps(2), 500)
        self.assertEqual(rules.rate_limit_rps(3), 5000)
        self.assertEqual(rules.rate_limit_rps(4), 20000)

    def test_webhook_timeout_s(self):
        self.assertEqual(rules.webhook_timeout_s(0), 5)
        self.assertEqual(rules.webhook_timeout_s(1), 5)
        self.assertEqual(rules.webhook_timeout_s(16), 5)
        self.assertEqual(rules.webhook_timeout_s(17), 5)
        self.assertEqual(rules.webhook_timeout_s(256), 15)
        self.assertEqual(rules.webhook_timeout_s(257), 15)
        self.assertEqual(rules.webhook_timeout_s(2048), 30)
        self.assertEqual(rules.webhook_timeout_s(2049), 30)
