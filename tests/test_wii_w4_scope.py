"""W4 keeps fixed-configuration observations separate from consumer limitations."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('w4_analyze', ROOT / 'tools/wii_w4/analyze.py')
analyze = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analyze)


def record(kind, name):
    return json.loads((ROOT / 'records' / kind / (name + '.json')).read_text())


def observed():
    sensor = {'capable': True, 'enabled': True, 'samples': 2,
              'min': [0, 0, 0], 'max': [1, 0, 0]}
    return {'hidapi_open': True, 'raw_open': True, 'window_ms': 60_000,
            'polls': 2, 'disconnected_polls': 0, 'removed_events': 0,
            'button_seen_masks': [3], 'axes': [{'min': -1, 'max': 1}],
            'sensors': {'accelerometer': dict(sensor), 'gyro': dict(sensor)},
            'player_led_capable': True, 'player_index_1_request': True,
            'player_index_2_request': True}


OUTPUTS = [{'value': {'leds': state}} for state in [
    [False, True, False, False], [False, False, True, False]]]


class WiiW4Scope(unittest.TestCase):
    def test_initial_open_or_missing_sensor_never_becomes_complete_fixed_acceptance(self):
        data = observed()
        self.assertEqual(analyze.assess('motionplus-nunchuk', data, OUTPUTS)['disposition'], 'passed')
        for key, value in [('window_ms', 59_999), ('disconnected_polls', 1),
                           ('removed_events', 1), ('hidapi_open', False)]:
            changed = dict(data, **{key: value})
            self.assertEqual(analyze.assess('motionplus-nunchuk', changed, OUTPUTS)['disposition'], 'blocked')
        data['sensors']['gyro']['enabled'] = False
        result = analyze.assess('motionplus', data, OUTPUTS)
        self.assertTrue(result['claim_held'])
        self.assertFalse(result['gyro_variation'])
        self.assertEqual(result['disposition'], 'blocked')

    def test_classic_accel_is_consumer_omission_but_axes_and_led_are_required(self):
        data = observed()
        data['sensors'] = {}
        data['player_led_capable'] = False
        result = analyze.assess('classic', data, OUTPUTS)
        self.assertEqual(result['disposition'], 'passed')
        self.assertFalse(result['accelerometer_required'])
        self.assertEqual(analyze.assess('classic', data, OUTPUTS[:1])['disposition'], 'blocked')
        data['axes'] = [{'min': 0, 'max': 0}]
        self.assertEqual(analyze.assess('classic', data, OUTPUTS)['disposition'], 'blocked')

    def test_consumer_source_role_and_motionplus_disconnect_correction_stay_explicit(self):
        names = ['wii-w4-sdl-3-2-10-no-reattach', 'wii-w4-sdl-3-2-10-motionplus-disconnect-path',
                 'wii-w4-sdl-newer-no-reattach']
        for name in names:
            claim = record('claim', name)
            self.assertEqual(claim['status'], 'source_supported')
            self.assertEqual(claim['applicability']['transport'], 'source_only')
            self.assertIn('evidence_role: consumer', claim['applicability']['scope'])
            self.assertEqual(set(claim['experiments']), {
                'wii-w2-sdl-after-host-run', 'wii-w3-sdl-diagnosis-host-run'})
        mp = record('claim', names[1])
        self.assertIn('HandleButtonData sets m_bDisconnected', mp['statement'])
        newer = record('claim', names[2])
        self.assertIn('neither newer version was installed or run', newer['statement'])
        revisions = {record('source', source)['revision'] for source in newer['sources']}
        self.assertEqual(revisions, {'829a65d769d935c4852f8159e964312c0957260a',
                                    '8adc0f98837db84fd24f17c339e59dcf36a17156'})

    def test_real_fixed_claims_do_not_promote_zero_gyro_or_advisory_led_flag(self):
        for case in ['none', 'nunchuk', 'classic', 'motionplus', 'motionplus-nunchuk']:
            name = 'wii-w4-sdl-fixed-' + case
            fixture = record('fixture', name + '-host')
            run = json.loads((ROOT / fixture['path']).read_text())
            obs = run['samples'][0]['observations']
            result = analyze.assess(case, obs['sdl'], obs['host_outputs'])
            self.assertEqual(result, obs['assessment'])
            self.assertTrue(result['claim_held'])
            self.assertTrue(result['player_led_intent'])
            self.assertFalse(obs['sdl']['player_led_capable'])
            self.assertEqual(obs['attachment_changes_during_child'], 0)
            self.assertTrue(obs['attachment_before_open'])
            expected = 'blocked' if case.startswith('motionplus') else 'passed'
            self.assertEqual(record('experiment', name + '-host-run')['status'], expected)
            self.assertEqual(run['summaries']['disposition'], expected)
            if case.startswith('motionplus'):
                gyro = obs['sdl']['sensors']['gyro']
                self.assertTrue(gyro['capable'] and gyro['enabled'])
                self.assertEqual(gyro['min'], [0, 0, 0])
                self.assertEqual(gyro['max'], [0, 0, 0])
                self.assertFalse(result['gyro_variation'])
            self.assertTrue(run['resources']['owned_hid_gone'])
            self.assertTrue(run['resources']['owned_hidraw_gone'])
