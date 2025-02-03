import unittest

from aggkit import alerts, rules


class AlertTests(unittest.TestCase):
    HISTORY = [10, 11, 9, 10, 12, 10, 11, 9]

    def test_threshold_breach(self):
        a = alerts.evaluate("lat", self.HISTORY, 50, level=2, threshold=40)
        self.assertEqual(a.cooldown_s, rules.alert_cooldown_s(2))
        self.assertIn("threshold", a.reason)

    def test_zscore_outlier(self):
        a = alerts.evaluate("lat", self.HISTORY, 100)
        self.assertIsNotNone(a)
        self.assertIn("z-score", a.reason)

    def test_normal_value_is_quiet(self):
        self.assertIsNone(alerts.evaluate("lat", self.HISTORY, 10.5))

    def test_short_history_never_alerts_on_zscore(self):
        self.assertEqual(alerts.zscore([1, 2], 100), 0.0)

    def test_cooldown_suppression(self):
        cd = rules.alert_cooldown_s(1)
        self.assertTrue(alerts.suppressed(1000, 1000 + cd - 1, 1))
        self.assertFalse(alerts.suppressed(1000, 1000 + cd, 1))
        self.assertFalse(alerts.suppressed(None, 5, 1))
