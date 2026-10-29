import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def record(kind, name):
    return json.loads((ROOT / 'records' / kind / (name + '.json')).read_text())


class WiiW9eScope(unittest.TestCase):
    def test_failed_host_preflight_does_not_become_a_dolphin_failure_or_pass(self):
        run = record('experiment', 'wii-w9e-per-device-bind-host-run')
        self.assertEqual(run['status'], 'blocked')
        self.assertEqual(run['kind'], 'virtual_host_run')
        self.assertEqual(run['fixtures'], [])
        for boundary in ['No such device', 'verified the driver link',
                         'HID/raw/LED removal', 'Both native Dolphin 2503 arms were not run']:
            self.assertIn(boundary, run['semantic_outcome'])
        claim = record('claim', 'wii-w9e-per-device-bind-blocked-result')
        self.assertEqual(claim['status'], 'inferred')
        self.assertEqual(claim['experiments'], [run['id']])
        self.assertIn('evidence_role: consumer', claim['applicability']['scope'])

    def test_unrun_register_ui_p3_and_generic_node_tradeoff_stay_unknown(self):
        claim = record('claim', 'wii-w9e-consumer-arms-unmeasured-result')
        self.assertEqual(claim['status'], 'unknown')
        self.assertEqual(claim['applicability']['transport'], 'not_measured')
        for checkpoint in ['before F6', 'A40020/32', 'A40040/16',
                           'Nunchuk and gyro', 'A400F0=55', 'xwiimote',
                           'No adoption pass follows']:
            self.assertIn(checkpoint, claim['statement'])
        self.assertEqual(claim['supersedes'], [])
        self.assertEqual(claim['conflicts_with'], [])

    def test_generic_match_source_is_not_a_host_policy_authorization(self):
        claim = record('claim', 'wii-w9e-generic-match-source')
        self.assertEqual(claim['status'], 'source_supported')
        self.assertEqual(claim['applicability']['transport'], 'source_only')
        self.assertEqual(claim['experiments'], [])
        self.assertIn('does not authorize changing global policy', claim['statement'])
        for name in claim['sources']:
            source = record('source', name)
            self.assertEqual(source['revision'], 'v6.12.113')
            self.assertEqual(source['kind'], 'kernel_source')
            self.assertTrue(source['url'].startswith('https://github.com/gregkh/linux/'))
            self.assertEqual(len(source['sha256']), 64)
            self.assertIn('not a hash of the Debian running kernel binary', source['locator'])
