import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ARMS = [
    'cemu-image-motionplus-no-holder',
    'cemu-image-motionplus-holder',
    'cemu-image-motionplus-nunchuk-no-holder',
    'dolphin-default-motionplus',
    'dolphin-default-motionplus-nunchuk',
    'dolphin-image-motionplus',
    'dolphin-image-motionplus-nunchuk',
]


def fixture(arm):
    return json.loads((ROOT / f'fixtures/acceptance/wii-w8-{arm}-host.json').read_text())


class W8Consumers(unittest.TestCase):
    def test_each_bounded_arm_retains_its_own_record_and_no_physical_promotion(self):
        for arm in ARMS:
            ident = f'wii-w8-{arm}'
            claim = json.loads((ROOT / f'records/claim/{ident}-result.json').read_text())
            experiment = json.loads((ROOT / f'records/experiment/{ident}-host-run.json').read_text())
            self.assertEqual(claim['experiments'], [ident + '-host-run'])
            self.assertEqual(claim['status'], 'inferred')
            self.assertEqual(experiment['status'], 'blocked')
            data = fixture(arm)
            self.assertFalse(data['environment']['synthetic'])
            self.assertEqual(data['config']['seconds_bound'], 35)
            self.assertFalse(data['config']['extension_blocks_imported'])
            self.assertTrue(all(data['resources'].values()))
            obs = data['samples'][0]['observations']
            self.assertFalse(obs['decoded_application_state_observed'])
            self.assertFalse(obs['trace']['decoded_gyro_observed'])
            self.assertTrue(all(stage['value_ns'] is None
                                for stage in data['samples'][0]['stages'].values()))

    def test_caller_image_changes_base_read_but_not_missing_extension_resource(self):
        for arm in ARMS[:3]:
            data = fixture(arm)
            obs = data['samples'][0]['observations']
            self.assertEqual(obs['trace']['memory_read_address_errors']['0016/0'], 1)
            image = data['config']['synthetic_caller_image']
            self.assertEqual(image['length'], 42)
            self.assertTrue(image['both_checksums_valid'])
            self.assertIn('not a codec factory scale', image['scale_origin'])
        obs = fixture(ARMS[2])['samples'][0]['observations']
        self.assertEqual(obs['preceding_identity'], 'Nunchuk')
        self.assertEqual(obs['extension_calibration_address_space'], 1)
        self.assertEqual(obs['trace']['native_memory_reads']['a40020/16'], 18)
        self.assertEqual(obs['trace']['memory_read_address_errors']['0020/7'], 18)

    def test_native_dolphin_log_is_primary_and_stages_are_not_overpromoted(self):
        for arm in ARMS[3:]:
            data = fixture(arm)
            obs = data['samples'][0]['observations']
            self.assertTrue(data['config']['own_file_log_primary'])
            self.assertTrue(data['config']['real_slots_disabled'])
            self.assertTrue(obs['own_log']['nonempty'])
            self.assertTrue(obs['own_log']['hidapi_discovery_notice'])
            self.assertTrue(obs['own_log']['controllerinterface_device_added'])
            self.assertEqual(obs['ladder']['d_mapping_ui'], 'not observed')
            if 'default' in arm:
                self.assertGreater(obs['own_log']['base_calibration_failure_count'], 0)
            else:
                self.assertEqual(obs['own_log']['base_calibration_failure_count'], 0)
                self.assertGreater(obs['native_output_report_counts']['19'], 0)
                self.assertFalse(any(k.startswith('a40020')
                                     for k in obs['trace']['native_memory_reads']))
            self.assertIn('not requested', obs['ladder']['i_mp_calibration'])
            self.assertIn('not observed', obs['ladder']['j_gyro'])
