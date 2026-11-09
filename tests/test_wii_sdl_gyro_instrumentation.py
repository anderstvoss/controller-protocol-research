import json
import unittest
from pathlib import Path


class WiiSDLInstrumentedGyro(unittest.TestCase):
    def test_virtual_results_preserve_dispatch_and_disconnect_evidence(self):
        root = Path(__file__).resolve().parents[1]
        prefix = 'wii-sdl-gyro-instrumented-'
        fixtures = root / 'fixtures/acceptance'
        primary = {
            f'{case}-sdl-{version}'
            for case in ('motionplus', 'motionplus-nunchuk', 'tr')
            for version in ('3-2-10', '3-4-20')
        }
        late = 'motionplus-nunchuk-sdl-3-4-20-late-holder'
        names = {
            p.stem.removeprefix(prefix).removesuffix('-host')
            for p in fixtures.glob(f'{prefix}*-host.json')
        }
        self.assertEqual(names, primary | {late})
        for name in sorted(names):
            with self.subTest(arm=name):
                fixture = json.loads((fixtures / f'{prefix}{name}-host.json').read_text())
                self.assertEqual(fixture['realization'], 'linux.uhid.bluetooth')
                self.assertTrue(fixture['config']['hid_wiimote_bound_before_and_after_child'])
                self.assertTrue(fixture['resources']['owned_hid_gone'])
                obs = fixture['samples'][0]['observations']
                summary = obs['summary']
                self.assertTrue(summary['hidapi_open'])
                self.assertFalse(summary['gyro_capable'])
                self.assertFalse(summary['gyro_enabled'])
                self.assertEqual(summary['gyro_events'], 0)
                self.assertEqual(summary['gyro_nonzero_events'], 0)
                self.assertEqual(summary['removals'], 1)
                self.assertTrue(all(n > 0 for n in summary['kernel_gyro_events']))
                self.assertEqual(
                    [(s['present'], s['mode']) for s in obs['cached_state_transitions']],
                    [(0, 0)],
                )
                events = obs['sdl_transactions_and_states']
                resets = [e for e in events if e['point'] == 'write-register'
                          and e['address'] == 'a400f0' and e['first_data_byte'] == 0x55]
                self.assertTrue(resets)
                if name in primary:
                    self.assertEqual(len(resets), 2)
                    self.assertTrue(any(e['point'] == 'linux-activation-bypass' for e in events))
                if name == 'motionplus-sdl-3-4-20':
                    self.assertEqual(obs['decode_decisions']['skip-mode-none-gyro-marked'], 4)
                    self.assertEqual(obs['sdl_hidraw_expected_gyro_reports_in_drive'],
                                     [{'vector': [7800, 9000, 7000], 'reports': 4}])
                    self.assertTrue(any(e['point'] == 'periodic-identify' and e['detail'][1] == 0x0405
                                        and e['mode'] == 0 for e in events))
                else:
                    self.assertEqual(obs['sdl_hidraw_expected_gyro_reports_in_drive'], [])
