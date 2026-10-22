import json
import unittest
from pathlib import Path


class WiiLedger(unittest.TestCase):
    def test_consumer_records_and_revision_gaps_remain_separate(self):
        root = Path(__file__).resolve().parents[1]
        claims = [json.loads(p.read_text()) for p in (root / 'records/claim').glob('wii-*.json')]
        self.assertEqual(len(claims), 43)
        self.assertTrue(all(c['applicability']['transport'] == 'source_only'
                            for c in claims if c['status'] == 'source_supported'))
        self.assertTrue(all(not c['experiments'] for c in claims))
        by_id = {c['id']: c for c in claims}
        revisions = [by_id[id]['applicability']['revision'] for id in
                     ['wii-original-remote-consumer-revision', 'wii-tr-consumer-revision',
                      'wii-early-plus-revision-gap']]
        self.assertEqual(len(set(revisions)), 3)
        self.assertEqual(by_id['wii-early-plus-revision-gap']['status'], 'unknown')
        self.assertEqual(by_id['wii-memory-size-hypothesis']['status'], 'unknown')
