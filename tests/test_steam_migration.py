import json
import unittest
from pathlib import Path


class SteamMigration(unittest.TestCase):
    def test_consumer_and_compatibility_evidence_stay_distinct(self):
        root = Path(__file__).resolve().parents[1]
        claims = [json.loads(p.read_text()) for p in (root / 'records/claim').glob('sc2-migration-*.json')]
        self.assertEqual(len(claims), 8)
        for claim in claims:
            if claim['id'].startswith('sc2-migration-kernel-'):
                self.assertEqual(claim['applicability']['transport'], 'source_only')
            else:
                self.assertEqual(claim['applicability']['controller'], 'openpuck-firmware')
            self.assertFalse(claim['experiments'])
        historical = json.loads((root / 'records/claim/puck-historical-compat.json').read_text())
        self.assertEqual(historical['status'], 'conflicted')
        self.assertIn('Unrecovered', historical['applicability']['scope'])
