import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def arm(style):
    return json.loads((ROOT / 'fixtures/acceptance' /
                       ('wii-w9i-dolphin-plus-motionplus-nunchuk-' + style + '-host.json')).read_text())


class WiiW9iScope(unittest.TestCase):
    def test_both_candidates_are_fresh_with_native_zero_mode_readback(self):
        for style in ['default', 'external']:
            d = arm(style)
            e = d['environment']
            t = d['samples'][0]['observations']['native_transport']
            self.assertTrue(e['fresh_device_single_consumer'])
            self.assertTrue(e['distinct_device_pair_verified'])
            self.assertEqual(e['host_outputs_before_consumer'], 0)
            self.assertFalse(e['prior_activation_or_deactivation'])
            self.assertFalse(e['kernel_rerun'])
            self.assertEqual(t['pre_map_inactive_fe_mode_bytes'], [0])
            self.assertEqual(t['pre_map_a600fe_one_byte_requests'], 1)
            self.assertNotIn('preliminary_run', e)
            self.assertIn('No full inactive identity readback', d['config']['identity_scope'])

    def test_id_style_is_only_creation_option_difference(self):
        a, b = arm('default'), arm('external')
        ao = a['config']['creation_options'].copy()
        bo = b['config']['creation_options'].copy()
        self.assertFalse(ao.pop('motionplus_inactive_id_external_style'))
        self.assertTrue(bo.pop('motionplus_inactive_id_external_style'))
        self.assertEqual(ao, bo)
        self.assertTrue(all(ao.values()))
        self.assertEqual(a['config']['synthetic_resources'], b['config']['synthetic_resources'])
        self.assertEqual(a['config']['owner_window'], b['config']['owner_window'])
        self.assertEqual(a['environment']['git_sha'], b['environment']['git_sha'])
        self.assertNotEqual(a['environment']['original_private_artifact_sha256'],
                            b['environment']['original_private_artifact_sha256'])

    def test_both_pass_transport_and_independent_decoded_checkpoints(self):
        for style in ['default', 'external']:
            d = arm(style)
            o = d['samples'][0]['observations']
            t = o['native_transport']
            self.assertEqual(t['mapped_mode'], 5)
            for key in ['post_map_mode_37_resent', 'f6_success',
                        'mp_calibration_matches_import', 'child_calibration_matches_import']:
                self.assertTrue(t[key])
            self.assertTrue(o['mapping_ui']['changing_gyro_observed'])
            self.assertTrue(o['mapping_ui']['changing_nunchuk_stick_observed'])
            points = d['environment']['decoded_stick_positions']
            self.assertGreater(sum((points[0][i] - points[1][i])**2 for i in [0, 1]), 400)
            self.assertGreater(t['post_map_frames']['mp'], 0)
            self.assertGreater(t['post_map_frames']['child'], 0)
            self.assertFalse(t['raw_trace_is_decoded_gyro_oracle'])
            self.assertEqual(t['native_post_map_a400f0_55'], 0)
            self.assertEqual(t['native_post_map_a600f0_55'], 0)

    def test_scope_cleanup_and_claims_remain_bounded(self):
        for style in ['default', 'external']:
            d = arm(style)
            self.assertTrue(all(d['resources'].values()))
            self.assertFalse(d['config']['hid_wiimote_bound'])
            self.assertIn('#258', d['config']['binding_scope'])
            self.assertEqual(d['config']['owner_window']['restored_value'], 0)
            self.assertFalse(d['samples'][0]['observations']['mapping_ui']['all_buttons_or_physical_rates_qualified'])
            c = json.loads((ROOT / 'records/claim' /
                            ('wii-w9i-dolphin-plus-motionplus-nunchuk-' + style + '-result.json')).read_text())
            self.assertEqual(c['status'], 'inferred')
            self.assertEqual(c['evidence_role'], 'consumer')
            self.assertNotIn('wii-c5-classic-cpp', c['sources'])
            self.assertIn('no physical/radio/game/release/timing', c['statement'].lower())
