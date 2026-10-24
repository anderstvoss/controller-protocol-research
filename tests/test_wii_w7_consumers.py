"""Keep virtual consumer observations separate from source and physical claims."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def observations(arm):
    record = json.loads((ROOT / 'fixtures/acceptance' / f'wii-w7-{arm}-host.json').read_text())
    return record, record['samples'][0]['observations']


class WiiW7Consumers(unittest.TestCase):
    def test_motionplus_drive_and_static_normalization_are_measured_not_calibrated(self):
        record, obs = observations('xwiimote')
        raw, offset, adaptive = obs['gyro_phases']
        self.assertTrue(all(p['events'] > 0 for p in (raw, offset, adaptive)))
        self.assertEqual(raw['minimum'], [-3528, -10728, -10728])
        self.assertEqual(raw['maximum'], [2772, 7272, 7272])
        for bound in ('minimum', 'maximum'):
            self.assertEqual(offset[bound], [v - n for v, n in zip(raw[bound], (10, 20, 30))])
        self.assertTrue(obs['lib_open']['opened'] & 256)
        self.assertFalse(obs['nunchuk_opened'])
        self.assertIn(5, obs['kernel_register_maps']['motionplus_nunchuk_phase'])
        _, control = observations('evtest')
        self.assertIn(4, control['kernel_register_maps']['motionplus_phase'])
        self.assertEqual(set(control['axes']), {'ABS_RX', 'ABS_RY', 'ABS_RZ'})
        for axis in control['axes'].values():
            self.assertGreater(axis['events'], 0)
            self.assertLess(axis['minimum'], axis['maximum'])
        self.assertEqual(record['summaries']['disposition'], 'passed')

    def test_retroarch_controls_do_not_promote_rejected_sensor_activation(self):
        _, obs = observations('retroarch')
        self.assertEqual({a['realization'] for a in obs['arms']},
                         {'linux.uinput', 'linux.uhid.bluetooth'})
        for arm in obs['arms']:
            self.assertEqual(len(arm['ports']), 8)
            self.assertGreater(arm['ports'][0]['changes'], 0)
            self.assertGreater(arm['ports'][1]['changes'], 0)
            self.assertTrue(all(not p['gyro_enable'] and not p['accel_enable']
                                for p in arm['ports']))
            self.assertEqual(len(arm['held_owned_node_names_at_4_and_8_seconds']), 2)
            for names in arm['held_owned_node_names_at_4_and_8_seconds']:
                self.assertEqual(set(names), {'Nintendo Wii Remote', 'Nintendo Wii Remote Nunchuk'})
            self.assertIn('RXYZ fallback not exercised', arm['attribution'])

    def test_sandbox_access_and_positive_control_are_not_dolphin_acceptance(self):
        record, obs = observations('dolphin')
        self.assertEqual(record['summaries']['disposition'], 'blocked')
        self.assertTrue(obs['sandbox_access']['owned_raw_open'])
        self.assertEqual(obs['positive_control']['exit_code'], 0)
        self.assertIn('owned-open', obs['positive_control']['trace_kinds'])
        self.assertTrue(all(a['owned_dynamic_io_trace_events'] == 0 for a in obs['arms']))
        self.assertIn('not established', obs['checkpoints']['connect'])
        self.assertIn('not established', obs['checkpoints']['controller_interface_add_device'])
        self.assertEqual(obs['checkpoints']['gyro'], 'not evaluated')
        self.assertTrue(obs['initial_pilot_limitation']['first_child_outlived_profile_switch'])
        self.assertTrue(record['config']['attachment_constant_during_each_child'])
        self.assertTrue(record['config']['cleanup_between_profiles'])
        for arm in obs['arms']:
            self.assertTrue(arm['child_cleanup']['owned_children_gone_before_next_profile'])
            self.assertEqual(arm['child_cleanup']['force_kill_count'], 0)
        self.assertEqual(set(obs['initial_pilot_limitation']['dynamic_trace_events_at_final_cleanup'].values()), {0})
        self.assertTrue(record['resources']['owned_children_gone'])
        self.assertEqual(record['resources']['explicit_term_count'], 2)
        self.assertEqual(record['resources']['force_kill_count'], 0)

    def test_all_arms_have_scoped_consumer_lineage_and_exact_cleanup(self):
        for arm in ('cemu', 'xwiimote', 'evtest', 'retroarch', 'dolphin'):
            record, _ = observations(arm)
            claim = json.loads((ROOT / 'records/claim' / f'wii-w7-{arm}-consumer-result.json').read_text())
            self.assertIn('evidence_role: consumer', claim['applicability']['scope'])
            self.assertIn(claim['status'], ('inferred', 'unknown'))
            self.assertEqual(claim['experiments'], [f'wii-w7-{arm}-host-run'])
            for key in ('owned_hid_gone', 'owned_hidraw_gone', 'owned_led_nodes_gone',
                        'owned_uinput_nodes_gone', 'idempotent_close', 'owned_children_gone'):
                self.assertIs(record['resources'][key], True)
        record, obs = observations('cemu')
        self.assertEqual(record['summaries']['disposition'], 'blocked')
        self.assertFalse(obs['native_executable_found'])
        self.assertFalse(obs['flatpak_aarch64_ref_found'])
        ledger = (ROOT / 'docs/ledgers/wii-remote-l0.md').read_text()
        self.assertIn('137 Wii claims', ledger)
