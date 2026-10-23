"""W3 must retain host-side diagnosis limits and historical blocked measurements."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('w3_analyze', ROOT / 'tools/wii_w3/analyze.py')
analyze = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analyze)


def load(name):
    return json.loads((ROOT / 'fixtures/acceptance' / ('wii-w3-' + name + '-host.json')).read_text())


class WiiW3Diagnosis(unittest.TestCase):
    def test_filter_keeps_resume_after_status_without_copying_redundant_data(self):
        rows = [{'ns': t, 'direction': d, 'hex': h} for t, d, h in [
            (1, 'device-input', '200000020000c0'),
            (2, 'host-output', '120430'), (3, 'device-input', '300000'),
            (4, 'device-input', '300000'), (5, 'host-output', '1500'),
            (6, 'device-input', '200000020000c0')]]
        parsed = analyze.summarize(rows, 0, 10, 10)
        self.assertEqual(parsed['nunchuk_status_resume']['mode_delay_ns'], 1)
        self.assertEqual(parsed['nunchuk_status_resume']['data_delay_after_mode_ns'], 1)
        self.assertEqual(len(parsed['selected_reports']), 5)
        self.assertEqual(next(x['count'] for x in parsed['report_counts']
                              if x['direction'] == 'device-input' and x['report_id_hex'] == '30'), 2)

    def test_observed_resume_does_not_promote_later_disconnected_joystick(self):
        run = load('sdl-diagnosis')
        self.assertEqual(run['summaries']['disposition'], 'blocked')
        for sample in run['samples']:
            obs = sample['observations']
            transition = obs['protocol']['nunchuk_status_resume']
            self.assertLess(transition['mode_delay_ns'], 100_000_000)
            self.assertLess(transition['data_delay_after_mode_ns'], 100_000_000)
            snapshots = obs['snapshots']
            if obs['profile'].startswith('sdl-wii'):
                self.assertEqual(obs['measurements']['OWNED_JOYSTICK'][0]['backend'], 'hidapi')
                self.assertEqual({s['connected0'] for s in snapshots}, {0, 1})
                self.assertEqual(snapshots[-1]['connected0'], 0)
                self.assertTrue(obs['sdl_extension_connected_debug_observed'])
            else:
                self.assertEqual(obs['measurements']['OWNED_JOYSTICK'][0]['backend'], 'evdev')
                self.assertTrue(all(s['connected0'] == 1 for s in snapshots))
            self.assertEqual(obs['measurements']['W3_MP_DEACTIVATE'], [{'sent': 1}])
            reports = obs['protocol']['selected_reports']
            for prefix in ['1500', '1704a400fa', '1704a600fa', '1604a600fe0104', '1604a400f00155', '12']:
                self.assertTrue(any(r['direction'] == 'host-output' and r['hex'].startswith(prefix) for r in reports), prefix)

    def test_external_attribution_does_not_rewrite_historical_n1_gate(self):
        obs = load('n1-attribution')['samples'][0]['observations']
        self.assertEqual(obs['external_class_entry_count'], 3)
        self.assertEqual(obs['entry_roles'], ['input', 'event', 'joystick'])
        self.assertFalse(obs['association_match'])
        self.assertIn('outside virtual UHID', obs['ancestry'])
        self.assertLess(obs['clock_conversion_uncertainty_seconds'], obs['retained_udev_init_relative_to_w2_n1_seconds'])
        self.assertLess(obs['retained_udev_init_relative_to_w2_n1_seconds'], obs['w2_n1_duration_seconds'])
        self.assertEqual(obs['historic_n1_status'], 'blocked')
        self.assertFalse(obs['harness_ordering_change'])
        old = json.loads((ROOT / 'records/experiment/wii-w2-bt-n1-host-run.json').read_text())
        self.assertEqual(old['status'], 'blocked')
