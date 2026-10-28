import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def arm(name):
    return json.loads((ROOT / 'fixtures/acceptance' /
                       ('wii-w9f-dolphin-' + name + '-host.json')).read_text())


class WiiW9fScope(unittest.TestCase):
    def test_pre_map_frames_do_not_become_passthrough_counts(self):
        d = arm('motionplus-nunchuk-on')
        o = d['samples'][0]['observations']
        self.assertEqual(d['summaries']['disposition'], 'blocked')
        self.assertEqual(o['trace']['received_report_ids']['37'], 28)
        self.assertEqual(o['pre_mode05_report37_count'], 28)
        self.assertEqual(o['post_mode05_frames']['mp'], 0)
        self.assertEqual(o['post_mode05_frames']['child'], 0)
        self.assertFalse(o['f6_read_observed'])
        self.assertFalse(o['mapping_ui']['changing_gyroscope_observed'])
        self.assertFalse(any(x['after_map'] and x['mode'] == 0x37
                             for x in o['report_mode_order']))

    def test_commit_counter_has_its_own_longer_interval(self):
        for name in ['motionplus-nunchuk-on', 'motionplus-control']:
            d = arm(name)
            s = d['samples'][0]['observations']['stimulus']
            self.assertGreater(s['successful_commits'], 1000)
            self.assertEqual(s['successful_commits'], s['commit_attempts'])
            self.assertEqual(s['commit_errors'], 0)
            self.assertGreater(s['producer_scope_seconds'], d['config']['seconds_bound'])
            self.assertAlmostEqual(s['observed_commit_hz'],
                                   s['successful_commits'] / s['producer_scope_seconds'], places=5)
            self.assertEqual(d['config']['owner_window']['restored_value'], 0)
            self.assertTrue(all(d['resources'].values()))

    def test_control_ui_and_post_map_rate_are_separate_oracles(self):
        d = arm('motionplus-control')
        o = d['samples'][0]['observations']
        self.assertEqual(d['summaries']['disposition'], 'passed')
        self.assertTrue(o['mapping_ui']['changing_gyroscope_observed'])
        self.assertFalse(o['trace']['decoded_gyro_observed'])
        self.assertTrue(any(x['after_map'] and x['mode'] == 0x37
                            for x in o['report_mode_order']))
        self.assertEqual(o['post_mode05_frames']['mp'], 7462)
        self.assertAlmostEqual(o['post_mode05_frames']['mp_per_consumer_second'], 7462 / 150, places=5)
        self.assertEqual(o['p3']['native_a400f0_after_first_mode05'], 0)
        self.assertEqual(o['p3']['combined_a400f0_after_first_mode05'], 0)
