"""C5 fixtures describe synthetic compatibility, never captured Wii traffic."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class WiiC5Fixtures(unittest.TestCase):
    def test_legal_modes_have_independent_synthetic_packets(self):
        expected = {0x30: 3, 0x31: 6, 0x32: 11, 0x33: 18,
                    0x34: 22, 0x35: 22, 0x36: 22, 0x37: 22,
                    0x3d: 22, 0x3e: 22, 0x3f: 22}
        for mode, size in expected.items():
            path = ROOT / f'records/fixture/wii-c5-neutral-{mode:02x}.json'
            rec = json.loads(path.read_text())
            raw = (ROOT / rec['path']).read_bytes()
            self.assertEqual(rec['kind'], 'synthetic')
            self.assertIsNone(rec['parent'])
            self.assertEqual(rec['experiments'], [])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), rec['sha256'])
            packet = bytes.fromhex(raw.decode())
            self.assertEqual(packet[0], mode)
            self.assertEqual(len(packet), size)
        for mode in range(0x38, 0x3d):
            self.assertFalse((ROOT / f'fixtures/wii-c5-neutral-{mode:02x}.hex').exists())

    def test_no_physical_promotion_or_closed_revision_gaps(self):
        for path in (ROOT / 'records/claim').glob('wii-c5-*.json'):
            rec = json.loads(path.read_text())
            self.assertEqual(rec['status'], 'source_supported')
            self.assertEqual(rec['applicability']['transport'], 'source_only')
            self.assertEqual(rec['experiments'], [])
        for id in ['wii-memory-size-hypothesis', 'wii-early-plus-revision-gap',
                   'wii-extension-encryption-gap']:
            rec = json.loads((ROOT / f'records/claim/{id}.json').read_text())
            self.assertEqual(rec['status'], 'unknown')

    def test_error_fixtures_include_the_wire_result_and_length(self):
        ack = bytes.fromhex((ROOT / 'fixtures/wii-c5-write-invalid-address.hex').read_text())
        read = bytes.fromhex((ROOT / 'fixtures/wii-c5-read-invalid-address.hex').read_text())
        self.assertEqual(ack, bytes([0x22, 0, 0, 0x16, 8]))
        self.assertEqual(read, bytes([0x21, 0, 0, 0xf8, 0xff, 0xff] + [0] * 16))
