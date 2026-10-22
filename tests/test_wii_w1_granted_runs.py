"""Keep post-grant access separate from Wii backend or physical acceptance."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_run(name):
    return json.loads((ROOT / 'fixtures/acceptance' / ('wii-w1-granted-' + name + '-host.json')).read_text())


class WiiW1GrantedRuns(unittest.TestCase):
    def test_granted_led_intent_and_exact_cleanup_scope(self):
        run = load_run('led')
        self.assertEqual(run['summaries']['disposition'], 'passed')
        obs = run['samples'][0]['observations']
        self.assertEqual(obs['writes'], [{'success': True, 'errno': None}] * 4)
        self.assertEqual(obs['retained_leds'], [True] * 4)
        for name in ['led', 'sdl', 'dolphin']:
            run = load_run(name)
            self.assertEqual(run['environment']['virtualgamepad_revision'],
                             '78e667369d57fc3175e4dabd8b13e221f2035ad5')
            self.assertFalse(run['environment']['synthetic'])
            self.assertTrue(run['resources']['owned_hid_gone'])
            self.assertTrue(run['resources']['owned_hidraw_gone'])
            self.assertEqual(run['resources']['fd_counts'], 'not_measured_in_this_followup')
            self.assertEqual(hashlib.sha256((ROOT / 'tools/wii_w1/granted_probe.rs').read_bytes()).hexdigest(),
                             run['environment']['published_parameterized_source_sha256'])
            for sample in run['samples']:
                self.assertIsNone(sample['stages']['first_neutral']['value_ns'])

    def test_sdl_access_filter_and_backend_are_distinct(self):
        run = load_run('sdl')
        self.assertEqual(run['summaries']['disposition'], 'blocked')
        for sample, count in zip(run['samples'], [0, 1], strict=True):
            obs = sample['observations']
            m = obs['measurements']
            self.assertEqual(m['direct_hidraw'], [{'open': 1, 'errno': 0}])
            self.assertEqual(m['owned_hid_count'], [{'count': count}])
            self.assertEqual(m['owned_joystick'][0]['backend'], 'evdev')
            self.assertEqual(m['sensors'], [{'accel': 0, 'gyro': 0}])
            self.assertEqual(obs['sdl_wii_hidapi_connection'], 'not_observed')
        self.assertEqual(run['samples'][1]['observations']['measurements']['owned_hid'],
                         [{'bus': 2, 'usage_page': 65280, 'usage': 1, 'open': 1}])

    def test_dolphin_access_and_timeout_do_not_prove_connection(self):
        run = load_run('dolphin')
        obs = run['samples'][0]['observations']
        self.assertTrue(obs['owned_hidraw_open_succeeded_in_sandbox'])
        self.assertEqual(obs['exit_code'], 124)
        self.assertEqual(run['summaries']['disposition'], 'blocked')
        for field in ['backend_connection', 'report_modes', 'memory_reads', 'extension_init', 'motionplus_activation']:
            self.assertEqual(obs[field], 'not_observed')
