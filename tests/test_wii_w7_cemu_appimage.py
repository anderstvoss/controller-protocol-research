"""Raw Cemu transport and calibration boundaries must not become gyro acceptance."""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    'wii_w7_cemu_trace', ROOT / 'tools/wii_w7/cemu_trace.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
reduce_trace = MODULE.reduce_trace


class WiiW7CemuAppImage(unittest.TestCase):
    def test_reducer_requires_complete_writes_and_keeps_transport_separate(self):
        def packet(kind, data, result=None):
            return {'kind': kind, 'hex': data.hex(),
                    'result': len(data) if result is None else result}

        status = packet('raw-write', bytes([0x15, 0]))
        result = reduce_trace([
            status, packet('raw-write', bytes([0x15, 0]), 1),
            packet('raw-write', bytes([0x17, 0, 0, 0, 0x16, 0, 8])),
            packet('raw-write', bytes([0x16, 4, 0xa6, 0, 0xfe, 1, 4])),
            packet('raw-write', bytes([0x16, 4, 0xa6, 0, 0xfe, 2, 4])),
            packet('raw-write', bytes([0x12, 4, 0x37])),
            packet('raw-read', bytes([0x21, 0, 0, 0xf8, 0, 0x16])),
            packet('raw-read', bytes([0x37, 0, 0])),
        ])
        self.assertEqual(result['counts']['status_requests'], 1)
        self.assertEqual(result['counts']['failed_or_partial_writes'], 1)
        self.assertEqual(result['counts']['truncated_memory_writes'], 1)
        self.assertEqual(result['native_memory_reads'], {'000016/8': 1})
        self.assertEqual(result['native_single_byte_register_writes'], {'a600fe/04': 1})
        self.assertEqual(result['native_report_modes'], {'37': 1})
        self.assertEqual(result['received_report_ids']['37'], 1)
        self.assertEqual(result['memory_read_address_errors'], {'0016/8': 1})
        self.assertFalse(result['decoded_gyro_observed'])

    def test_real_arms_preserve_calibration_and_decoded_state_limits(self):
        record = json.loads((ROOT / 'fixtures/acceptance/wii-w7-cemu-appimage-host.json').read_text())
        arms = record['samples'][0]['observations']['arms']
        self.assertEqual({(a['case'], a['kernel_holder']) for a in arms},
                         {(c, h) for c in ('motionplus', 'motionplus-nunchuk') for h in (False, True)})
        self.assertEqual(len(arms), 4)
        for arm in arms:
            trace = arm['trace']
            self.assertGreater(trace['counts']['status_requests'], 0)
            self.assertGreater(trace['counts']['owned_raw_opens'], 0)
            self.assertGreater(trace['native_memory_reads']['000016/8'], 0)
            self.assertGreater(trace['memory_read_address_errors']['0016/8'], 0)
            self.assertFalse(trace['decoded_gyro_observed'])
            self.assertEqual(arm['seconds_bound'], 35)
            self.assertTrue(arm['children_gone_before_next_arm'])
            self.assertEqual(arm['extra_owned_children_termed'], 0)
            writes = trace['native_single_byte_register_writes']
            if arm['kernel_holder']:
                self.assertNotIn('a600fe/04', writes)
                self.assertGreater(writes['a400f0/55'], 0)
                self.assertGreater(arm['holder_bytes_drained'], 0)
            else:
                self.assertEqual(writes['a600fe/04'], 1)
                self.assertEqual(writes['a600f0/55'], 1)
                self.assertEqual(arm['holder_bytes_drained'], 0)
            if arm['case'] == 'motionplus':
                self.assertNotIn('37', trace['native_report_modes'])
            else:
                self.assertGreater(trace['native_report_modes']['37'], 0)
                self.assertGreater(trace['received_report_ids']['37'], 0)
            self.assertTrue(arm['all_actor_a600fe_map_writes_during_phase'])
        self.assertEqual(record['summaries']['disposition'], 'blocked')
        self.assertFalse(record['config']['caller_eeprom_image_imported'])
        self.assertFalse(record['config']['cold_device_isolation'])
        self.assertTrue(record['resources']['all_eight_app_instances_gone'])
        for key in ('owned_hid_gone', 'owned_hidraw_gone', 'owned_led_nodes_gone', 'idempotent_close'):
            self.assertTrue(record['resources'][key])

    def test_availability_correction_is_additive(self):
        claim = json.loads((ROOT / 'records/claim/wii-w7-cemu-appimage-result.json').read_text())
        old = json.loads((ROOT / 'records/claim/wii-w7-cemu-consumer-result.json').read_text())
        self.assertEqual(claim['supersedes'], [old['id']])
        self.assertEqual(claim['status'], 'inferred')
        self.assertEqual(old['status'], 'unknown')
        self.assertIn('evidence_role: consumer', claim['applicability']['scope'])
        self.assertEqual(claim['experiments'], ['wii-w7-cemu-appimage-host-run'])
        self.assertIn('138 Wii claims', (ROOT / 'docs/ledgers/wii-remote-l0.md').read_text())
