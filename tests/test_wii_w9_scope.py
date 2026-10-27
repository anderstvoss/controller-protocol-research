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

    def read_arm(self, name):
        return json.loads((ROOT / f'fixtures/acceptance/wii-w9-{name}-host.json').read_text())

    def test_on_off_passthrough_runs_do_not_promote_unreached_shim_windows(self):
        for option, count in [('on', 14334), ('off', 14659)]:
            d = self.read_arm('dolphin-motionplus-nunchuk-' + option)
            o = d['samples'][0]['observations']
            self.assertEqual(d['summaries']['disposition'], 'blocked')
            self.assertEqual(o['trace']['native_memory_reads']['a400f6/4'], count)
            self.assertEqual(o['trace']['memory_read_address_errors']['00f6/7'], count)
            self.assertNotIn('a40020/32', o['trace']['native_memory_reads'])
            self.assertNotIn('a40040/16', o['trace']['native_memory_reads'])
            self.assertEqual(o['p3']['native_a400f0_after_first_map'], 0)
            self.assertEqual(o['p3']['combined_a400f0_after_first_map'], 1)
            self.assertFalse(o['live_compat_window_success_observed'])
            self.assertFalse(o['decoded_nunchuk_observed'])
            self.assertTrue(d['config']['kernel_kept_bound'])
            self.assertTrue(all(d['resources'].values()))

    def test_mp_only_control_ui_is_distinct_from_raw_transport_and_rate_accuracy(self):
        d = self.read_arm('dolphin-motionplus-on-control')
        o = d['samples'][0]['observations']
        self.assertEqual(d['summaries']['disposition'], 'passed')
        self.assertEqual(o['caller_mp_chunk_matches'], {'head': 1, 'tail': 1})
        self.assertTrue(o['mapping_ui']['changing_gyroscope_indicator'])
        self.assertTrue(o['mapping_ui']['changing_accelerometer'])
        self.assertTrue(o['mapping_ui']['changing_basic_ir_points'])
        self.assertFalse(o['trace']['decoded_gyro_observed'])
        self.assertEqual(d['config']['ui_gyro_calibration_period_seconds'], 0)
        self.assertIn('rate-accuracy', d['summaries']['semantic_outcome'])

    def test_fresh_kernel_control_keeps_reused_node_loss_visible(self):
        d = self.read_arm('kernel-motionplus-on-control')
        o = d['samples'][0]['observations']
        self.assertTrue(o['fresh_device_control'])
        self.assertIn('blocked before evtest', o['earlier_reused_device_preflight'])
        self.assertTrue(o['source_topology_preserved_at_phase_start'])
        for axis in ['ABS_RX', 'ABS_RY', 'ABS_RZ']:
            self.assertEqual(o['axes'][axis]['distinct_values'], 2)
            self.assertLess(o['axes'][axis]['minimum'], o['axes'][axis]['maximum'])
        self.assertTrue(all(d['resources'].values()))
