import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from sanitize import review_descriptor


class XboxPhysicalReference(unittest.TestCase):
    def test_reviewed_descriptor_matches_measured_hash(self):
        record = json.loads((ROOT / 'records/fixture/xsphys-bt-descriptor.json').read_text())
        path = ROOT / record['path']
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), record['sha256'])
        self.assertEqual(len(bytes.fromhex(path.read_text())), 283)
        self.assertEqual(
            review_descriptor(path),
            'a681e2cb8b5d9466f258e2f07f0fcc518ec438231af1b61b125c213d2c62e165')

    def test_descriptor_review_rejects_strings_long_items_and_truncation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'descriptor.hex'
            for encoded in ('a1017901c0', 'fe010000', '270102', 'c0', 'a101'):
                with self.subTest(encoded=encoded):
                    path.write_text(encoded)
                    with self.assertRaises(ValueError):
                        review_descriptor(path)

    def test_descriptor_and_input_evidence_roles_remain_distinct(self):
        descriptor = json.loads((ROOT / 'records/claim/xsphys-bt-descriptor-match.json').read_text())
        inputs = json.loads((ROOT / 'records/claim/xsphys-xpad-input.json').read_text())
        self.assertEqual(descriptor['evidence_role'], 'device')
        self.assertEqual(inputs['evidence_role'], 'consumer')
        self.assertEqual(descriptor['applicability']['transport'], 'bluetooth')
        self.assertEqual(inputs['applicability']['transport'], 'usb')
        original = json.loads((ROOT / 'records/claim/xbox-cgap-descriptor-example.json').read_text())
        self.assertEqual(original['status'], 'source_supported')

    def test_wired_sweep_keeps_press_release_and_full_axis_coverage(self):
        trace = json.loads((ROOT / 'fixtures/xsphys-xpad-sweep.json').read_text())
        self.assertFalse(trace['manifest']['synthetic'])
        self.assertEqual(len(trace['frames']), 799)
        keys, axes, hats = {}, {}, set()
        x = y = 0
        for frame in trace['frames']:
            for event in frame['events']:
                kind, code, value = (event[name] for name in ('event_type', 'code', 'value'))
                if kind == 1:
                    keys.setdefault(code, set()).add(value)
                elif kind == 3:
                    axes.setdefault(code, set()).add(value)
                    if code == 16:
                        x = value
                    elif code == 17:
                        y = value
            hats.add((x, y))
        self.assertEqual(len(keys), 12)
        self.assertTrue(all(values == {0, 1} for values in keys.values()))
        self.assertEqual(hats, {(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1)})
        for code in (0, 1, 3, 4):
            self.assertEqual((min(axes[code]), max(axes[code])), (-32768, 32767))
        for code in (2, 5):
            self.assertEqual((min(axes[code]), max(axes[code])), (0, 1023))
