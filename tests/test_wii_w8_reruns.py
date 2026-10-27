import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(arm):
    return json.loads((ROOT / f'fixtures/acceptance/wii-w8-{arm}-host.json').read_text())


class W8Reruns(unittest.TestCase):
    def test_dolphin_mp_mapping_changes_all_four_inputs_without_physical_promotion(self):
        data = read('dolphin-imported-motionplus')
        self.assertEqual(data['summaries']['disposition'], 'passed')
        self.assertEqual(data['environment']['git_sha'],
                         '5a11e507ac973c23ca10beb36edb44fc35034376')
        self.assertEqual(len(data['samples']), 2)
        for sample in data['samples']:
            trace = sample['observations']['trace']
            self.assertEqual(trace['native_memory_reads']['a40020/32'], 1)
            self.assertEqual(trace['memory_read_address_errors']['0020/0'], 1)
            self.assertEqual(trace['memory_read_address_errors']['0030/0'], 1)
            self.assertEqual(sample['observations']['caller_calibration_chunk_matches'],
                             {'motionplus_head': 1, 'motionplus_tail': 1})
            self.assertFalse(trace['decoded_gyro_observed'], 'raw trace is not a UI oracle')
        ui = data['samples'][1]['observations']['mapping_ui']
        for key in ['device_in_mapping_view', 'changing_buttons', 'changing_accelerometer',
                    'changing_basic_ir_points', 'changing_gyroscope_indicator']:
            self.assertTrue(ui[key], key)
        self.assertFalse(ui['physical_calibration_claim'])
        self.assertEqual(ui['ui_gyro_calibration_period_seconds'], 0)
        self.assertEqual(ui['displayed_accel_g'], [1.37, 2.27])
        self.assertTrue(data['config']['no_real_slots'])
        self.assertTrue(all(data['resources'].values()))

    def test_dolphin_passthrough_identity_blocks_before_mp_calibration(self):
        data = read('dolphin-imported-motionplus-nunchuk')
        obs = data['samples'][0]['observations']
        self.assertEqual(data['summaries']['disposition'], 'blocked')
        self.assertEqual(obs['trace']['native_memory_reads']['a400f6/4'], 12128)
        self.assertEqual(obs['trace']['memory_read_address_errors']['00f6/7'], 12128)
        self.assertNotIn('a40020/32', obs['trace']['native_memory_reads'])
        self.assertTrue(obs['mapping_ui']['mapping_view_device_observed'])
        self.assertIsNone(obs['mapping_ui']['changing_gyro'])
        self.assertFalse(obs['visible_basic_ir_drive'])
        self.assertIn('before MP calibration', obs['ladder']['i'])

    def test_cemu_coexistence_is_not_a_clean_nunchuk_or_decoded_gyro_pass(self):
        for case in ['motionplus', 'motionplus-nunchuk']:
            data = read('cemu-imported-' + case)
            self.assertEqual(data['summaries']['disposition'], 'blocked')
            self.assertTrue(data['config']['external_companion_holder_at_preflight'])
            self.assertFalse(data['config']['runner_opened_holder'])
            self.assertIn('blocked before consumer', data['config']['no_holder_preflight'])
            obs = data['samples'][0]['observations']
            self.assertFalse(obs['decoded_application_state_observed'])
            self.assertEqual(obs['trace']['memory_read_address_errors']['0016/0'], 1)
            if case == 'motionplus':
                self.assertNotIn('a40020/16', obs['trace']['native_memory_reads'])
            else:
                self.assertEqual(obs['trace']['native_memory_reads']['a40020/16'], 44)
                self.assertEqual(obs['served_calibration_block_counts'],
                                 {'motionplus_first_half': 44})
                self.assertEqual(obs['native_prefix_sequence'][5]['identity'], 'motionplus')
            self.assertTrue(all(data['resources'].values()))

    def test_clean_cemu_mp_retains_missing_calibration_and_decoded_oracle(self):
        data = read('cemu-imported-clean-motionplus')
        self.assertFalse(data['config']['external_companion_holder_at_preflight'])
        self.assertFalse(data['config']['runner_opened_holder'])
        self.assertTrue(data['config']['no_holder_preflight'].startswith('passed'))
        obs = data['samples'][0]['observations']
        self.assertEqual(obs['trace']['memory_read_address_errors']['0016/0'], 1)
        self.assertNotIn('a40020/16', obs['trace']['native_memory_reads'])
        self.assertEqual(obs['served_calibration_block_counts'], {})
        self.assertFalse(obs['decoded_application_state_observed'])
        self.assertTrue(all(data['resources'].values()))

    def test_clean_cemu_nunchuk_calibration_delivery_is_not_decoded_motion(self):
        data = read('cemu-imported-clean-motionplus-nunchuk')
        self.assertFalse(data['config']['external_companion_holder_at_preflight'])
        self.assertFalse(data['config']['runner_opened_holder'])
        obs = data['samples'][0]['observations']
        self.assertEqual(obs['trace']['native_memory_reads']['a40020/16'], 18)
        self.assertEqual(obs['trace']['memory_read_address_errors']['0020/0'], 18)
        self.assertEqual(obs['served_calibration_block_counts'],
                         {'motionplus_first_half': 1, 'nunchuk': 17})
        self.assertEqual(obs['native_prefix_sequence'][4]['identity'], 'nunchuk')
        self.assertFalse(obs['decoded_application_state_observed'])
        self.assertEqual(data['summaries']['disposition'], 'blocked')
        self.assertTrue(all(data['resources'].values()))
