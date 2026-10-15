import json
import unittest
from pathlib import Path


class XboxSeriesLedger(unittest.TestCase):
    def test_consumer_records_do_not_promote_device_transports(self):
        root = Path(__file__).resolve().parents[1]
        claims = [json.loads(p.read_text()) for p in (root / 'records/claim').glob('xbox-series-*.json')]
        consumers = [c for c in claims if c['status'] == 'source_supported']
        self.assertEqual(len(consumers), 8)
        self.assertTrue(all(c['applicability']['transport'] == 'source_only' for c in consumers))
        gaps = [c for c in claims if c['status'] == 'unknown']
        self.assertEqual({c['applicability']['transport'] for c in gaps}, {'usb', 'bluetooth'})
        self.assertTrue(all(not c['experiments'] for c in claims))
