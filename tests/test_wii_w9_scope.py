import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class WiiW9Scope(unittest.TestCase):
    def test_fixed_f7_is_non_ready_compat_without_challenge_or_physical_promotion(self):
        c = json.loads((ROOT / 'records/claim/wii-w9-f7-fixed-preparing-compat.json').read_text())
        self.assertEqual(c['status'], 'inferred')
        self.assertEqual(c['applicability']['transport'], 'source_only')
        self.assertIn('provenance_class: compat', c['applicability']['scope'])
        self.assertIn('holds F7 at 0x02', c['statement'])
        self.assertIn('never advances', c['statement'])
        self.assertIn('0x50 remains error 7', c['statement'])
        self.assertEqual(c['experiments'], [])
        self.assertIn('not physical readback', c['statement'])
