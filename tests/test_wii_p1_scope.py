import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARMS = ['kernel-motionplus', 'kernel-motionplus-nunchuk', 'sdl-motionplus',
        'sdl-motionplus-nunchuk', 'dolphin-motionplus']


def fixture(name):
    return json.loads((ROOT / 'fixtures/acceptance' / ('wii-p1-' + name + '-host.json')).read_text())


class WiiP1Scope(unittest.TestCase):
    def test_kernel_and_xwiimote_have_one_concurrent_gyro_oracle(self):
        for name in ARMS[:2]:
            d = fixture(name)
            o = d['samples'][0]['observations']
            self.assertEqual(d['summaries']['disposition'], 'passed')
            self.assertEqual(o['devtype'], 'gen20')
            self.assertTrue(o['xwiimote']['same_capture_as_evtest'])
            self.assertEqual(o['xwiimote']['distinct_motionplus_values'], 2)
            for axis in ['ABS_RX', 'ABS_RY', 'ABS_RZ']:
                self.assertEqual(o['kernel_axes'][axis]['distinct_values'], 2)
                self.assertLess(o['kernel_axes'][axis]['minimum'], o['kernel_axes'][axis]['maximum'])

    def test_sdl_capability_and_polled_zeros_never_become_gyro_success(self):
        for name, capable in [('sdl-motionplus', False), ('sdl-motionplus-nunchuk', True)]:
            d = fixture(name)
            o = d['samples'][0]['observations']
            self.assertEqual(d['summaries']['disposition'], 'blocked')
            self.assertEqual(len(d['environment']['consumer_library_sha256']), 64)
            self.assertEqual(len(d['environment']['consumer_probe_source_sha256']), 64)
            self.assertTrue(o['hidapi_open'])
            self.assertEqual(o['disconnected_polls'], 0)
            self.assertEqual(o['removed_events'], 0)
            self.assertTrue(o['kernel_mp_event_held'])
            self.assertTrue(all(v == 2 for v in o['concurrent_kernel_gyro_distinct_values'].values()))
            self.assertEqual(o['sensors']['gyro']['capable'], capable)
            self.assertEqual(o['sensors']['gyro']['min'], [0, 0, 0])
            self.assertEqual(o['sensors']['gyro']['max'], [0, 0, 0])
            self.assertFalse(o['decoded_gyro_change_observed'])

    def test_dolphin_ui_success_is_separate_from_raw_transport(self):
        d = fixture('dolphin-motionplus')
        o = d['samples'][0]['observations']
        self.assertEqual(d['summaries']['disposition'], 'passed')
        self.assertTrue(o['kernel_kept_bound'])
        self.assertTrue(o['mapping_ui']['changing_gyroscope_observed'])
        self.assertEqual(o['mapping_ui']['gyro_calibration_period_seconds'], 0)
        self.assertFalse(o['trace']['decoded_gyro_observed'])
        self.assertGreater(o['caller_mp_chunks_match']['0020'], 0)
        self.assertGreater(o['caller_mp_chunks_match']['0030'], 0)

    def test_kernel_detection_is_not_full_identity_log_readback(self):
        for name in ARMS[:2]:
            o = fixture(name)['samples'][0]['observations']['kernel_inactive_id_log']
            self.assertTrue(o['owner_readonly_filter_obtained'])
            self.assertTrue(o['gen20_detection_logged'])
            self.assertFalse(o['full_inactive_hex_logged'])
            self.assertIsNone(o['logged_id_hex'])

    def test_revision_default_binding_and_cleanup_are_distinct_from_original(self):
        for name in ARMS:
            d = fixture(name)
            self.assertEqual(d['config']['revision'], 'Tr / Wii Remote Plus')
            self.assertEqual(d['config']['binding'], 'wiimote')
            self.assertFalse(d['config']['motionplus_inactive_id_external_style'])
            self.assertTrue(d['config']['no_special_driver_window'])
            self.assertTrue(all(d['resources'].values()))
            c = json.loads((ROOT / 'records/claim' / ('wii-p1-' + name + '-result.json')).read_text())
            self.assertEqual(c['evidence_role'], 'consumer')
            self.assertEqual(c['status'], 'inferred')
            self.assertIn('no Original inheritance', c['applicability']['scope'])
