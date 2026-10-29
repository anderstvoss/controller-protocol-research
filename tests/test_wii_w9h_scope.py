import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def arm(name):
    return json.loads((ROOT / 'fixtures/acceptance' /
                       ('wii-w9h-' + name + '-host.json')).read_text())


def observed(d):
    return d['samples'][0]['observations']


class WiiW9hScope(unittest.TestCase):
    def test_copy_off_isolates_child_stick_not_gyro_or_all_buttons(self):
        d = arm('dolphin-original-motionplus-nunchuk-copy-off')
        t = observed(d)['native_transport']
        ui = observed(d)['mapping_ui']
        self.assertEqual(d['summaries']['disposition'], 'blocked')
        self.assertFalse(d['config']['creation_options']['motionplus_passthrough_calibration_copy'])
        self.assertTrue(t['post_map_mode_37_resent'])
        self.assertTrue(t['f6_success'])
        self.assertTrue(t['mp_calibration_matches_import'])
        self.assertFalse(t['child_calibration_matches_import'])
        self.assertTrue(any(r['address'] == 64 and r['error'] == 7 and r['count'] > 0
                            for r in t['post_map_read_replies']))
        self.assertTrue(ui['changing_gyro_observed'])
        self.assertTrue(ui['nunchuk_buttons_respond_observed'])
        self.assertFalse(ui['changing_nunchuk_stick_observed'])
        self.assertGreater(t['post_map_frames']['child'], 0)
        old = json.loads((ROOT / 'fixtures/acceptance/'
                          'wii-w9g-dolphin-motionplus-nunchuk-on-host.json').read_text())
        for key in ['motionplus_sha256', 'nunchuk_sha256']:
            self.assertEqual(d['config']['synthetic_resources'][key],
                             old['config']['synthetic_resources'][key])
        self.assertTrue(old['config']['creation_options']['motionplus_passthrough_calibration_copy'])
        self.assertTrue(observed(old)['mapping_ui']['changing_nunchuk_stick_observed'])

    def test_classic_mode07_is_its_own_decoded_control_pass(self):
        d = arm('dolphin-original-motionplus-classic-on')
        t = observed(d)['native_transport']
        ui = observed(d)['mapping_ui']
        self.assertEqual(t['mapped_mode'], 7)
        self.assertTrue(t['post_map_mode_37_resent'] and t['f6_success'])
        self.assertTrue(t['mp_calibration_matches_import'] and t['child_calibration_matches_import'])
        for k in ['changing_gyro_observed', 'changing_classic_left_stick_observed',
                  'changing_classic_right_stick_observed', 'selected_classic_a_b_buttons_change_observed']:
            self.assertTrue(ui[k])
        self.assertFalse(ui['all_classic_buttons_or_triggers_qualified'])
        self.assertEqual(t['post_map_frames']['mp'], 4483)
        self.assertEqual(t['post_map_frames']['child'], 4483)
        c = d['config']['synthetic_resources']['classic']
        self.assertTrue(c['synthetic'] and c['no_retail_factory_or_hardware_claim'])
        self.assertEqual(c['length'], 16)
        self.assertIn('wii-c5-classic-cpp', c['source_records'])

    def test_plus_both_id_styles_have_independent_decoded_evidence(self):
        for name, external, suffix in [('default', False, 'A4200005'), ('external', True, 'A6200005')]:
            d = arm('dolphin-plus-motionplus-nunchuk-' + name)
            self.assertTrue(d['config']['revision'].startswith('Tr'))
            self.assertEqual(d['config']['creation_options']['motionplus_inactive_id_external_style'], external)
            self.assertEqual(d['config']['source_expected_inactive_identity_suffix'], suffix)
            t = observed(d)['native_transport']
            self.assertEqual(t['mapped_mode'], 5)
            self.assertTrue(t['f6_success'] and t['mp_calibration_matches_import']
                            and t['child_calibration_matches_import'])
            self.assertTrue(observed(d)['mapping_ui']['changing_gyro_observed'])
            self.assertTrue(observed(d)['mapping_ui']['changing_nunchuk_stick_observed'])
            self.assertEqual(d['environment']['distinct_decoded_stick_positions_sampled'], 2)
            self.assertFalse(t['raw_trace_is_decoded_gyro_oracle'])
        d = arm('dolphin-plus-motionplus-nunchuk-default')
        self.assertFalse(d['environment']['preliminary_run']['changing_stick_qualified'])
        self.assertFalse(d['environment']['preliminary_run']['used_for_complete_stick_acceptance'])

    def test_claim_citations_and_reused_plus_identity_scope(self):
        for name in ['original-motionplus-nunchuk-copy-off',
                     'plus-motionplus-nunchuk-default', 'plus-motionplus-nunchuk-external']:
            claim = json.loads((ROOT / 'records/claim' /
                                ('wii-w9h-dolphin-' + name + '-result.json')).read_text())
            self.assertNotIn('wii-c5-classic-cpp', claim['sources'])
            self.assertNotIn('wii-c5-classic-h', claim['sources'])
        classic = json.loads((ROOT / 'records/claim/'
                              'wii-w9h-dolphin-original-motionplus-classic-on-result.json').read_text())
        self.assertIn('wii-c5-classic-cpp', classic['sources'])
        self.assertIn('wii-c5-classic-h', classic['sources'])
        d = arm('dolphin-plus-motionplus-nunchuk-default')
        self.assertTrue(d['environment']['accepted_repeat_device_reused'])
        self.assertEqual(d['environment']['accepted_repeat_pre_map_inactive_mode_byte'], 5)
        self.assertEqual(d['environment']['preliminary_pre_map_inactive_mode_byte'], 0)
        self.assertIn('Fresh mode 00 decoded-stick acceptance is not established',
                      d['config']['identity_scope'])

    def test_kernel_plus_gate_precedes_generic_and_separates_cleanup(self):
        d = arm('kernel-plus-motionplus-nunchuk')
        o = observed(d)
        self.assertEqual(d['config']['binding'], 'wiimote')
        self.assertEqual(d['config']['devtype'], 'gen20')
        self.assertEqual(o['mapped_mode'], 5)
        self.assertTrue(all(v['distinct_values'] == 2 for v in o['kernel_axes'].values()))
        self.assertEqual(o['xwiimote_distinct_values'], 2)
        self.assertEqual(o['xwiimote_events'], 93)
        self.assertEqual(o['reinitialisation_first_18_seconds'], 0)
        self.assertGreater(o['first_post_map_reinit_seconds'][0], 18)
        self.assertEqual([x['extension_bit'] for x in o['statuses'][:2]], [False, True])
        self.assertEqual(o['stimulus']['commit_errors'], 0)

    def test_generic_cleanup_scope_and_rates_do_not_promote_physical(self):
        names = ['original-motionplus-nunchuk-copy-off', 'original-motionplus-classic-on',
                 'plus-motionplus-nunchuk-default', 'plus-motionplus-nunchuk-external']
        for n in names:
            d = arm('dolphin-' + n)
            self.assertTrue(all(d['resources'].values()))
            self.assertFalse(d['config']['hid_wiimote_bound'])
            self.assertIn('#258', d['config']['binding_scope'])
            self.assertEqual(d['config']['owner_window']['restored_value'], 0)
            t = observed(d)['native_transport']
            self.assertEqual(t['native_post_map_a400f0_55'], 0)
            self.assertEqual(t['native_post_map_a600f0_55'], 0)
            self.assertEqual(t['post_map_frames']['denominator_seconds'], 180)
            self.assertFalse(t['raw_trace_is_decoded_gyro_oracle'])
        claims = [json.loads(p.read_text()) for p in (ROOT / 'records/claim').glob('wii-w9h-*.json')]
        self.assertEqual(len(claims), 5)
        self.assertTrue(all(c['evidence_role'] == 'consumer' and c['status'] == 'inferred' for c in claims))
