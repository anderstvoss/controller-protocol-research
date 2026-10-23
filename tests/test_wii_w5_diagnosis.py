"""Deterministic seams for W5 packet decoding and actor attribution."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('w5_analyze', ROOT / 'tools/wii_w5/analyze.py')
analyze = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analyze)


def row(ns, kind, payload, actor='aggregate'):
    return {'ns': ns, 'kind': kind, 'hex': payload, 'actor': actor}


class WiiW5Diagnosis(unittest.TestCase):
    def test_decode_uses_distinct_axes_and_rejects_reserved_or_passthrough_bits(self):
        # Authored independent reference: yaw8500,roll7000,pitch9000; all slow.
        payload = bytes([8500 & 255, 7000 & 255, 9000 & 255,
                         ((8500 >> 8) << 2) | 3, ((7000 >> 8) << 2) | 3,
                         ((9000 >> 8) << 2) | 2])
        self.assertEqual(analyze.decode_gyro(payload), ([8500, 7000, 9000], [True, True, True]))
        for last in [payload[5] | 1, payload[5] & ~2]:
            with self.assertRaises(ValueError):
                analyze.decode_gyro(payload[:5] + bytes([last]))

    def test_failed_map_ack_never_establishes_active_data(self):
        data = [row(1, 'host-output', '1604a600fe0105'),
                row(2, 'device-input', '2200001607'),
                row(3, 'device-input', '350000000000345828876f8e')]
        result = analyze.packet_checks(data)
        self.assertEqual(result['gyro_packets'], 0)
        self.assertEqual(result['acked_map_modes'], [])

    def test_remapping_starts_a_new_passthrough_alternation_segment(self):
        data = []
        for base in [0, 10]:
            data += [row(base + 1, 'host-output', '1604a600fe0105'),
                     row(base + 2, 'device-input', '2200001600'),
                     row(base + 3, 'device-input', '350000000000345828876f8e')]
        result = analyze.packet_checks(data)
        self.assertEqual(result['gyro_packets'], 2)
        self.assertEqual(result['invalid_or_mismatched'], 0)
        self.assertEqual(result['mode5_alternation_errors'], 0)

    def test_actor_match_retains_multiple_writer_ambiguity(self):
        command = '1604a400f00155'
        data = [row(1, 'raw-output', command, 'sdl'),
                row(2, 'host-output', command)]
        self.assertEqual(analyze.transactions(data, 0)[0]['actor'], 'sdl')
        data.insert(1, row(1, 'raw-output', command, 'probe'))
        self.assertEqual(analyze.transactions(data, 0)[0]['actor'], 'ambiguous')
        self.assertEqual(analyze.transactions([data[-1]], 0)[0]['actor'], 'kernel_or_untraced')

    def test_public_observations_strip_raw_bytes_and_preserve_time_and_errors(self):
        rows = [{'ns': 10, 'kind': 'marker', 'case': 'motionplus', 'arm': 'holder',
                 'label': 'child_start'},
                row(11, 'host-output', '1604a400f00155'),
                {'ns': 12, 'kind': 'marker', 'case': 'motionplus', 'arm': 'holder',
                 'label': 'child_end'}]
        messages = [{'kind': 'summary', 'gyro_events': 0},
                    {'kind': 'ids', 'phase': 'after_open_api',
                     'banks': [{'reply': False, 'reply_error': 7}]}]
        result = analyze.observations(rows, messages, 'motionplus', 'holder')
        command = result['transactions'][0]
        self.assertNotIn('hex', command)
        self.assertEqual(command['write_data_hex'], '55')
        self.assertEqual(command['relative_ns'], 1)
        self.assertNotIn('examples', result['packets'])
        self.assertEqual(result['identity_readbacks'], messages[1:])
        self.assertEqual(result['private_cached_mode'], 'not_instrumented')

    def test_real_runs_preserve_kernel_delivery_and_sdl_limits(self):
        import json
        import hashlib
        for arm in ['kernel', 'control', 'holder']:
            for case in ['motionplus', 'motionplus-nunchuk']:
                name = f'wii-w5-{case}-{arm}-host'
                fixture = json.loads((ROOT / 'records/fixture' / (name + '.json')).read_text())
                raw = (ROOT / fixture['path']).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), fixture['sha256'])
                run = json.loads(raw)
                obs = run['samples'][0]['observations']
                summary, packets = obs['summary'], obs['packets']
                self.assertTrue(obs['child_exit_success'])
                self.assertTrue(obs['attachment_before_open'])
                self.assertEqual(obs['attachment_changes_during_child'], 0)
                self.assertTrue(run['resources']['owned_hid_gone'])
                self.assertTrue(run['resources']['owned_hidraw_gone'])
                self.assertEqual(obs['private_cached_mode'], 'not_instrumented')
                self.assertEqual(packets['invalid_or_mismatched'], 0)
                self.assertEqual(packets['mode5_alternation_errors'], 0)
                if arm == 'kernel':
                    self.assertGreaterEqual(summary['window_ms'], 20_000)
                    self.assertTrue(summary['kernel_only'])
                    self.assertFalse(summary['hidapi_open'])
                    self.assertEqual([a['min'] for a in summary['evdev']], [-3528, -10728, -10728])
                    self.assertEqual([a['max'] for a in summary['evdev']], [2772, 7272, 7272])
                    self.assertTrue(all(a['events'] > 0 for a in summary['evdev']))
                    self.assertEqual(len(packets['vectors']), 2)
                    self.assertGreater(packets['gyro_packets'], 0)
                    if case.endswith('nunchuk'):
                        self.assertEqual(packets['downstream_packets'], packets['gyro_packets'])
                    self.assertEqual(run['summaries']['disposition'], 'passed')
                else:
                    self.assertGreaterEqual(summary['window_ms'], 60_000)
                    self.assertTrue(summary['hidapi_open'])
                    self.assertEqual(summary['gyro_events'], 0)
                    self.assertEqual(summary['gyro_nonzero_samples'], 0)
                    self.assertEqual(summary['gyro_min'], [0, 0, 0])
                    self.assertEqual(summary['gyro_max'], [0, 0, 0])
                    self.assertEqual(run['summaries']['disposition'], 'blocked')
                    self.assertTrue(any(t['actor'] == 'sdl' and t['address_hex'] == 'a400f0'
                                        for t in obs['transactions']))
        # The failed holder arm must not be described as gyro-enabled/sustained.
        run = json.loads((ROOT / 'fixtures/acceptance/wii-w5-motionplus-holder-host.json').read_text())
        summary = run['samples'][0]['observations']['summary']
        self.assertFalse(summary['gyro_capable'])
        self.assertFalse(summary['gyro_enabled'])
        self.assertGreater(summary['disconnected_polls'], 0)
