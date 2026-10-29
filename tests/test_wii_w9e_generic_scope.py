import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARMS = ['dolphin-motionplus-nunchuk', 'dolphin-motionplus-control', 'kernel-tradeoff']


def fixture(arm):
    return json.loads((ROOT / 'fixtures/acceptance' /
                       ('wii-w9e-generic-' + arm + '-host.json')).read_text())


class WiiW9eGenericScope(unittest.TestCase):
    def test_successful_calibration_does_not_promote_f6_or_decoded_passthrough(self):
        data = fixture(ARMS[0])
        observed = data['samples'][0]['observations']
        self.assertEqual(data['summaries']['disposition'], 'blocked')
        self.assertEqual(observed['caller_calibration_chunk_matches'],
                         {'0020': 1, '0030': 1, '0040': 1})
        self.assertNotIn('a400f6/4', observed['trace']['native_memory_reads'])
        self.assertIn('Not requested', observed['f6_checkpoint'])
        self.assertFalse(observed['mapping_ui']['changing_nunchuk_observed'])
        self.assertFalse(observed['mapping_ui']['changing_gyroscope_observed'])
        self.assertEqual(observed['trace']['received_report_ids']['37'], 28)
        self.assertIn('after successful MP/child calibration',
                      data['config']['first_unpassed_checkpoint'])

    def test_gyro_control_uses_ui_oracle_separately_from_transport(self):
        data = fixture(ARMS[1])
        observed = data['samples'][0]['observations']
        self.assertEqual(data['summaries']['disposition'], 'passed')
        self.assertTrue(observed['mapping_ui']['changing_gyroscope_observed'])
        self.assertFalse(observed['trace']['decoded_gyro_observed'])
        self.assertEqual(data['config']['ui_gyro_calibration_period_seconds'], 0)
        self.assertEqual(observed['caller_calibration_chunk_matches'],
                         {'0020': 1, '0030': 1})

    def test_post_map_reset_is_absent_in_both_observation_channels(self):
        for arm in ARMS[:2]:
            p3 = fixture(arm)['samples'][0]['observations']['p3']
            self.assertTrue(p3['mode05_observed'])
            self.assertEqual(p3['native_a400f0_after_first_mode05'], 0)
            self.assertEqual(p3['combined_a400f0_after_first_mode05'], 0)

    def test_generic_binding_tradeoff_is_checked_before_and_after(self):
        data = fixture(ARMS[2])
        observed = data['samples'][0]['observations']
        self.assertEqual(data['summaries']['disposition'], 'passed')
        self.assertFalse(observed['evdev_motionplus_axes_available'])
        self.assertFalse(observed['xwiimote_access_available'])
        for phase in ['before', 'after']:
            self.assertEqual(len(observed[phase]), 2)
            for device in observed[phase]:
                self.assertEqual(device['driver'], 'hid-generic')
                self.assertEqual(device['input_nodes'], 0)
                self.assertEqual(device['xwiimote']['iface_new_result'], -19)

    def test_window_restoration_cleanup_and_consumer_role_are_explicit(self):
        for arm in ARMS:
            data = fixture(arm)
            window = data['config']['owner_window']
            self.assertEqual(window['initial_value'], 0)
            self.assertEqual(window['restored_value'], 0)
            self.assertGreater(window['seconds'], 0)
            self.assertLess(window['seconds'], 10)
            self.assertTrue(all(data['resources'].values()))
            self.assertEqual(data['config']['binding'], 'hid-generic')
            claim = json.loads((ROOT / 'records/claim' /
                               ('wii-w9e-generic-' + arm + '-result.json')).read_text())
            self.assertEqual(claim['evidence_role'], 'consumer')
            self.assertEqual(claim['status'], 'inferred')
            self.assertEqual(claim['supersedes'], [])
            self.assertIn('#258', claim['applicability']['scope'])
