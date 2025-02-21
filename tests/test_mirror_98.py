import unittest

from aggkit import legacy_mirror_98
from aggkit.native import lib


class LegacyMirrorTests(unittest.TestCase):
    def test_v1_layout_matches_the_library(self):
        self.assertEqual(legacy_mirror_98.v1_size(), lib.agg_sizeof_stats())
