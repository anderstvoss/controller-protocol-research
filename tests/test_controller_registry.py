import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from validate import validate
from status import status


class ControllerRegistry(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'corpus'
        shutil.copytree(Path(__file__).resolve().parents[1], self.root,
                        ignore=shutil.ignore_patterns('.git', '.venv', '__pycache__'))

    def edit_claim(self, name, **applicability):
        p = self.root / 'records/claim' / (name + '.json')
        value = json.loads(p.read_text())
        value['applicability'].update(applicability)
        p.write_text(json.dumps(value))

    def test_claims_must_name_a_registered_controller(self):
        self.edit_claim('ds-input', controller='DualSense')
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_transport_is_a_fixed_vocabulary(self):
        self.edit_claim('ds-input', transport='SDL HIDAPI')
        with self.assertRaises(Exception):
            validate(self.root)

    def test_controller_parent_must_exist(self):
        p = self.root / 'records/controller/dualsense.json'
        value = json.loads(p.read_text())
        value['parent'] = 'missing-family'
        p.write_text(json.dumps(value))
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_categories_follow_strongest_claim(self):
        rows = {row['id']: row for row in status(self.root)}
        self.assertEqual(rows['dualsense']['category'], 'Source evidence')
        self.assertEqual(rows['wii-remote']['category'], 'No evidence')
        self.assertEqual(rows['steam-controller-2026-puck']['transports'], {'usb': 'Source evidence'})

    def test_unknown_only_claims_are_wip(self):
        for name in ['pro2-physical-macro-controls']:
            (self.root / 'records/claim' / (name + '.json')).unlink()
        rows = {row['id']: row for row in status(self.root)}
        self.assertEqual(rows['8bitdo-pro-2']['category'], 'Evidence in progress')


if __name__ == '__main__':
    unittest.main()
