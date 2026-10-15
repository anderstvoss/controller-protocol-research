import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from validate import validate
from sanitize import transform

TRACE = {
    'manifest': {
        'format_version': 1,
        'synthetic': True,
        'sources': [{'reported_name': 'Synthetic pad', 'bus_type': 3, 'vendor_id': 0,
                     'product_id': 0, 'version': 0, 'transport': 'Usb', 'control_count': 1}],
    },
    'controls': [{'source_index': 0, 'event_type': 1, 'code': 304, 'absolute_range': None}],
    'frames': [{'source_index': 0, 'events': [{'event_type': 1, 'code': 304, 'value': 1}]}],
}


class EvdevTraceFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'corpus'
        shutil.copytree(Path(__file__).resolve().parents[1], self.root,
                        ignore=shutil.ignore_patterns('.git', '.venv', '__pycache__'))

    def add(self, trace, kind='synthetic'):
        encoded = json.dumps(trace).encode()
        (self.root / 'fixtures/synthetic-evdev.json').write_bytes(encoded)
        record = {
            'schema_version': 1, 'id': 'synthetic-evdev', 'kind': kind,
            'format': 'evdev_trace_json', 'path': 'fixtures/synthetic-evdev.json',
            'sha256': hashlib.sha256(encoded).hexdigest(), 'sources': ['kernel'],
            'experiments': ['seed-inspection'], 'parent': None, 'transform': None, 'claims': [],
        }
        (self.root / 'records/fixture/synthetic-evdev.json').write_text(json.dumps(record))

    def test_synthetic_trace_validates(self):
        before = validate(self.root)
        self.add(TRACE)
        self.assertEqual(validate(self.root), before + 1)

    def test_synthetic_flag_must_match_kind(self):
        self.add(dict(TRACE, manifest=dict(TRACE['manifest'], synthetic=False)))
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_byte_sanitizer_rejects_traces(self):
        self.add(TRACE)
        with self.assertRaises(ValueError):
            transform(self.root, 'synthetic-evdev', 'derived', 0, b'\x00')


if __name__ == '__main__':
    unittest.main()
