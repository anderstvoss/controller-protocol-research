import json
import unittest
from pathlib import Path


class XboxSeriesLedger(unittest.TestCase):
    def test_consumer_records_do_not_promote_device_transports(self):
        root = Path(__file__).resolve().parents[1]
        claims = [json.loads(p.read_text()) for p in (root / 'records/claim').glob('xbox-series-*.json')]
        consumers = [c for c in claims if c['status'] == 'source_supported']
        self.assertEqual(len(consumers), 9)
        self.assertTrue(all(c['applicability']['transport'] == 'source_only' for c in consumers))
        self.assertTrue(all(c.get('evidence_role') == 'consumer' for c in consumers))
        gaps = [c for c in claims if c['status'] == 'unknown']
        self.assertEqual({c['applicability']['transport'] for c in gaps}, {'usb', 'bluetooth'})
        self.assertTrue(all(not c['experiments'] for c in claims))

    def test_xpad_shape_preserves_consumer_capabilities_without_capture(self):
        root = Path(__file__).resolve().parents[1]
        fixture = json.loads((root / 'fixtures/xbox-series-xpad-evdev-golden.json').read_text())
        self.assertTrue(fixture['manifest']['synthetic'])
        self.assertEqual(fixture['frames'], [])
        self.assertEqual(len(fixture['manifest']['sources']), 1)
        self.assertEqual(fixture['manifest']['sources'][0]['control_count'], 26)
        controls = {(c['event_type'], c['code']): c['absolute_range'] for c in fixture['controls']}
        self.assertEqual(len(controls), 26)
        self.assertIn((1, 167), controls)  # KEY_RECORD (Share)
        self.assertIn((1, 316), controls)  # BTN_MODE (Guide)
        self.assertEqual({code for kind, code in controls if kind == 21}, {80, 81, 88, 89, 90, 96})
        self.assertEqual(controls[3, 0]['fuzz'], 16)
        self.assertEqual(controls[3, 0]['flat'], 128)
        self.assertEqual(controls[3, 2]['maximum'], 1023)
        self.assertEqual(controls[3, 5]['maximum'], 1023)
