"""Keep bounded W1 consumer results separate from physical/application acceptance."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_run(name):
    return json.loads((ROOT / 'fixtures/acceptance' / ('wii-w1-' + name + '-host.json')).read_text())


class WiiW1HostRuns(unittest.TestCase):
    def test_original_probe_hashes_and_cleanup_are_retained(self):
        for name in ['numeric-bt', 'numeric-uinput', 'sdl', 'dolphin', 'battery-rumble-led']:
            run = load_run(name)
            self.assertFalse(run['environment']['synthetic'])
            self.assertEqual(run['environment']['backend'], 'linux')
            self.assertEqual(run['environment']['virtualgamepad_revision'],
                             '50161b913d0f82950c292465625e9cdd8854daf2')
            for file, expected in run['environment']['probe_source_hashes'].items():
                self.assertEqual(hashlib.sha256((ROOT / 'tools/wii_w1' / file).read_bytes()).hexdigest(), expected)
            for sample in run['samples']:
                self.assertIsNone(sample['stages']['first_neutral']['value_ns'])
        for name in ['numeric-bt', 'numeric-uinput']:
            resources = load_run(name)['resources']
            self.assertTrue(resources['owned_inputs_gone'])
            self.assertEqual(resources['before_fds'], resources['after_fds'])

    def test_selected_native_values_reached_both_virtual_event_consumers(self):
        for target, fuzz in [('bt', [2, 1, 4]), ('uinput', [0, 0, 0])]:
            run = load_run('numeric-' + target)
            self.assertEqual(run['summaries']['disposition'], 'passed')
            self.assertEqual(len(run['samples']), 4)
            for sample in run['samples']:
                nodes = {node['role_name']: node for node in sample['observations']['nodes']}
                accel = nodes['Nintendo Wii Remote Accelerometer']
                for code, value in [(3, 88), (4, -112), (5, 0)]:
                    self.assertIn([3, code, value], accel['events'])
                self.assertEqual([(a['minimum'], a['maximum'], a['flat'], a['fuzz'], a['resolution'])
                                  for a in accel['axes']], [(-500, 500, 4, fuzz[0], 0)] * 3)
                self.assertEqual([a['delivered_value'] for a in accel['axes']], [-512] * 3)
                ir = nodes['Nintendo Wii Remote IR']
                self.assertIn([3, 16, 123], ir['events'])
                self.assertIn([3, 17, 234], ir['events'])
                self.assertTrue(all(a['delivered_value'] == 1023 for a in ir['axes']))
                phase = sample['observations']['phase']
                if phase == 1:
                    nunchuk = nodes['Nintendo Wii Remote Nunchuk']
                    for event in [[3, 16, 22], [3, 17, -28], [3, 3, 88], [3, 4, -112], [1, 306, 1]]:
                        self.assertIn(event, nunchuk['events'])
                elif phase == 2:
                    classic = nodes['Nintendo Wii Remote Classic Controller']
                    for code, value in zip(range(18, 24), [18, -12, 8, -12, 18, 8]):
                        self.assertIn([3, code, value], classic['events'])
                    self.assertTrue(all(a['fuzz'] == fuzz[1] for a in classic['axes']))
                    self.assertNotIn('Nintendo Wii Remote Nunchuk', nodes)
                elif phase == 3:
                    mp = nodes['Nintendo Wii Remote Motion Plus']
                    self.assertIn([3, 4, -1728], mp['events'])
                    self.assertIn([3, 5, 7272], mp['events'])
                    self.assertTrue(all(a['fuzz'] == fuzz[2] for a in mp['axes']))

    def test_permissions_and_fallback_never_become_hidapi_or_dolphin_acceptance(self):
        for sample in load_run('sdl')['samples']:
            measurements = sample['observations']['measurements']
            self.assertEqual(measurements['direct_hidraw'], [{'open': 0, 'errno': 13}])
            self.assertEqual(measurements['owned_joystick'][0]['backend'], 'evdev')
            self.assertEqual(measurements['sensors'], [{'accel': 0, 'gyro': 0}])
            self.assertEqual(measurements['output_request'][0]['rumble'], 1)
            self.assertEqual(measurements['output_request'][0]['led'], 0)
        dolphin = load_run('dolphin')['samples'][0]['observations']
        self.assertTrue(dolphin['owned_hidraw_present_in_sandbox'])
        self.assertTrue(dolphin['owned_hidraw_open_denied_in_sandbox'])
        self.assertEqual(dolphin['backend_connection'], 'not_observed')
        battery = load_run('battery-rumble-led')['samples'][0]['observations']
        self.assertEqual((battery['battery_raw'], battery['capacity']), (192, '75'))
        self.assertTrue(battery['rumble_live']['native_rumble_seen'])
        self.assertEqual([led['errno'] for led in battery['led_writes']], [13] * 4)
        for name in ['sdl', 'dolphin', 'battery-rumble-led']:
            self.assertEqual(load_run(name)['summaries']['disposition'], 'blocked')
