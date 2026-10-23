"""W2 observations must distinguish enumeration, initial claim and sustained acceptance."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / 'fixtures/acceptance' / ('wii-w2-' + name + '-host.json')).read_text())


class WiiW2HostRuns(unittest.TestCase):
    def test_default_filter_and_explicit_wii_profile_are_distinct(self):
        before, after = load('sdl-before'), load('sdl-after')
        for run in [before, after]:
            self.assertEqual(run['summaries']['disposition'], 'blocked')
            self.assertEqual(run['environment']['sdl_version'], '3.2.10')
            self.assertEqual(run['environment']['probe_source_sha256'],
                             hashlib.sha256((ROOT / 'tools/wii_w2/host_probe.rs').read_bytes()).hexdigest())
            self.assertTrue(run['resources']['owned_hid_gone'])
            self.assertTrue(run['resources']['owned_hidraw_gone'])
        for run, count in [(before, 0), (after, 1)]:
            m = run['samples'][0]['observations']['measurements']
            self.assertEqual(m['direct_hidraw'], [{'open': 1, 'errno': 0}])
            self.assertEqual(m['owned_hid_count'], [{'count': count}])
            self.assertEqual(m['owned_joystick'][0]['backend'], 'evdev')
        self.assertEqual(after['samples'][0]['observations']['measurements']['owned_hid'],
                         [{'bus': 2, 'usage_page': 1, 'usage': 5, 'open': 1}])

    def test_initial_hidapi_claim_does_not_hide_later_disconnect(self):
        m = load('sdl-after')['samples'][1]['observations']['measurements']
        self.assertEqual(m['owned_joystick'],
                         [{'backend': 'hidapi', 'axes': 6, 'buttons': 26, 'hats': 0, 'gamepad': 1}])
        self.assertEqual(m['sensors'], [{'accel': 1, 'gyro': 0}])
        self.assertEqual({s['connected0'] for s in m['unique_snapshots']}, {0, 1})
        self.assertEqual(m['unique_snapshots'][-1]['connected0'], 0)

    def test_kernel_shapes_and_led_intent_survive_collection_change(self):
        before, after = load('sdl-before'), load('sdl-after')
        shapes = [r['samples'][0]['observations']['owned_kernel_shapes'] for r in [before, after]]
        self.assertEqual(*shapes)
        self.assertEqual(len({n['name'] for row in shapes[0] for n in row['nodes']}), 6)
        for r in [before, after]:
            self.assertEqual(r['resources']['led_writes']['retained_leds'], [True] * 4)
            self.assertEqual(r['resources']['led_writes']['writes'], [{'success': True, 'errno': None}] * 4)

    def test_timing_resources_and_missing_oracles_are_not_promoted(self):
        for n in [1, 4]:
            r = load('bt-n' + str(n))
            self.assertEqual(r['environment']['git_sha'], '07e42cb49dd3840dbe37017ad86263114d8c15d8')
            self.assertFalse(r['environment']['dirty'])
            self.assertEqual(len(r['samples']), n * 10)
            for sample in r['samples']:
                self.assertEqual(sample['errors'], [])
                self.assertIsNotNone(sample['stages']['node_gone']['value_ns'])
                for stage in ['consumer_open', 'first_neutral', 'sdl_ready']:
                    self.assertIsNone(sample['stages'][stage]['value_ns'])
                    self.assertTrue(sample['stages'][stage]['reason'])
            exp = json.loads((ROOT / 'records/experiment' / ('wii-w2-bt-n' + str(n) + '-host-run.json')).read_text())
            self.assertEqual(exp['status'], 'passed' if r['resources']['before'] == r['resources']['after'] else 'blocked')
        r = load('bt-n1')
        self.assertEqual(r['resources']['before']['input_nodes'], 26)
        self.assertEqual(r['resources']['after']['input_nodes'], 29)
