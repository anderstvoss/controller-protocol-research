import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def arm(name):
    return json.loads((ROOT / 'fixtures/acceptance' /
                       ('wii-w9g-' + name + '-host.json')).read_text())


class WiiW9gScope(unittest.TestCase):
    def test_bound_kernel_gate_separates_activation_from_reader_close(self):
        for name, mode in [('motionplus', 4), ('motionplus-nunchuk', 5)]:
            d = arm('kernel-' + name)
            o = d['samples'][0]['observations']
            self.assertEqual(d['summaries']['disposition'], 'passed')
            self.assertEqual(o['mapped_mode'], mode)
            self.assertTrue(all(v['distinct_values'] == 2 for v in o['kernel_axes'].values()))
            self.assertEqual(o['xwiimote']['distinct_motionplus_values'], 2)
            r = o['kernel_reinitialisation']
            self.assertEqual(r['a400f0_55_first_18_seconds_after_map'], 0)
            self.assertEqual(r['a600f0_55_first_18_seconds_after_map'], 0)
            self.assertGreater(r['first_post_map_writes'][0]['seconds_after_map'], 18)
            flags = [v['extension_bit'] for v in o['observed_statuses']]
            self.assertEqual(flags[:2], [True, True] if mode == 4 else [False, True])
            self.assertFalse(o['stimulus']['observed_rate_qualified'])

    def test_positive_arm_keeps_transport_and_decoded_oracles_distinct(self):
        d = arm('dolphin-motionplus-nunchuk-on')
        o = d['samples'][0]['observations']
        t = o['native_transport']
        self.assertTrue(t['post_map_report_mode_37_resent'])
        self.assertTrue(t['f6_success'])
        self.assertEqual(t['f7_fixed_compat_byte_observed'], 2)
        self.assertTrue(t['mp_calibration_matches_caller'])
        self.assertTrue(t['child_calibration_matches_caller'])
        self.assertEqual(t['post_map_frames']['mp'], 4480)
        self.assertEqual(t['post_map_frames']['child'], 4479)
        self.assertAlmostEqual(t['post_map_frames']['mp_per_consumer_second'], 4480 / 180, places=6)
        self.assertFalse(t['decoded_gyro_observed'])
        self.assertTrue(o['mapping_ui']['changing_gyro_observed'])
        self.assertTrue(o['mapping_ui']['changing_nunchuk_stick_observed'])
        self.assertFalse(o['mapping_ui']['decoded_buttons_qualified'])
        self.assertFalse(d['environment']['preliminary_profile_run']['used_for_stick_acceptance'])

    def test_controls_disable_one_gate_without_promoting_raw_frames(self):
        off = arm('dolphin-motionplus-nunchuk-reattach-off')
        mirror = arm('dolphin-motionplus-nunchuk-mirror-off')
        for d in [off, mirror]:
            self.assertEqual(d['summaries']['disposition'], 'blocked')
            self.assertTrue(d['config']['creation_options']['motionplus_passthrough_calibration_copy'])
            self.assertFalse(d['samples'][0]['observations']['mapping_ui']['changing_gyro_observed'])
        t = off['samples'][0]['observations']['native_transport']
        self.assertFalse(t['post_map_report_mode_37_resent'])
        self.assertFalse(t['f6_success'])
        self.assertEqual(t['post_map_frames']['mp'], 0)
        self.assertEqual(t['post_map_frames']['child'], 0)
        self.assertIsNone(off['samples'][0]['observations']['mapping_ui']['changing_nunchuk_stick_observed'])
        t = mirror['samples'][0]['observations']['native_transport']
        self.assertTrue(t['post_map_report_mode_37_resent'])
        self.assertGreater(t['post_map_frames']['mp'], 0)
        self.assertFalse(t['f6_success'])
        self.assertFalse(t['mp_calibration_matches_caller'])
        self.assertFalse(t['child_calibration_matches_caller'])
        self.assertTrue(any(r['address'] == 246 and r['error'] == 7
                            for r in t['read_reply_errors']))
        self.assertFalse(any(r['address'] in [32, 64] for r in t['post_map_read_requests']))

    def test_generic_scope_and_cleanup_do_not_erase_release_gate(self):
        for name in ['on', 'reattach-off', 'mirror-off']:
            d = arm('dolphin-motionplus-nunchuk-' + name)
            self.assertFalse(d['config']['hid_wiimote_bound'])
            self.assertIn('#258', d['config']['binding_scope'])
            self.assertEqual(d['config']['owner_window']['restored_value'], 0)
            self.assertTrue(all(d['resources'].values()))
            self.assertEqual(d['samples'][0]['observations']['native_transport']
                             ['native_a400f0_55_after_map'], 0)
        claims = [json.loads(p.read_text()) for p in (ROOT / 'records/claim').glob('wii-w9g-*.json')]
        self.assertEqual(len(claims), 5)
        self.assertTrue(all(c['evidence_role'] == 'consumer' and c['status'] == 'inferred'
                            and c['applicability']['revision'].startswith('Original') for c in claims))
