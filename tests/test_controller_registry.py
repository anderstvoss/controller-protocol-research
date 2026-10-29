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
        self.assertEqual(rows['wii-remote']['category'], 'Source evidence')
        self.assertEqual(rows['wii-remote']['transports']['source_only'], 'Source evidence')
        self.assertEqual(rows['wii-remote']['transports']['bluetooth'], 'Evidence in progress')
        # SDL or kernel source analysis alone is not device-protocol evidence.
        for controller in ['dualsense-edge', 'switch2-pro', 'xbox-series']:
            with self.subTest(controller=controller):
                self.assertEqual(rows[controller]['category'], 'Evidence in progress')
                self.assertEqual(rows[controller]['consumer_category'], 'Source evidence')
        # Independent source-backed device evidence was added for Switch Pro in C
        # and Xbox 360 in F. Neither claims a physical retail-capture baseline.
        self.assertEqual(rows['switch-pro']['category'], 'Source evidence')
        self.assertEqual(rows['switch-pro']['consumer_category'], 'Source evidence')
        self.assertEqual(rows['xbox360']['category'], 'Source evidence')
        self.assertEqual(rows['xbox360']['consumer_category'], 'Source evidence')
        puck = rows['steam-controller-2026-puck']['transports']
        self.assertEqual(puck['usb'], 'Source evidence')
        self.assertNotIn('source_only', puck)
        self.assertEqual(rows['steam-controller-2026-puck']['consumer_transports']['source_only'],
                         'Source evidence')

    def test_consumer_claims_do_not_promote_device_evidence(self):
        claim_path = self.root / 'records/claim/pro2-physical-macro-controls.json'
        claim = json.loads(claim_path.read_text())
        self.assertNotIn('evidence_role', claim)
        before = {row['id']: row for row in status(self.root)}['8bitdo-pro-2']
        self.assertEqual(before['category'], 'Source evidence')
        self.assertEqual(before['consumer_category'], 'No evidence')
        claim['evidence_role'] = 'consumer'
        claim_path.write_text(json.dumps(claim))
        after = {row['id']: row for row in status(self.root)}['8bitdo-pro-2']
        self.assertEqual(after['category'], 'Evidence in progress')
        self.assertEqual(after['consumer_category'], 'Source evidence')
        self.assertNotIn('source_only', after['transports'])
        self.assertEqual(after['consumer_transports']['source_only'], 'Source evidence')

    def test_evidence_role_enum_is_validated(self):
        path = self.root / 'records/claim/pro2-physical-macro-controls.json'
        claim = json.loads(path.read_text())
        claim['evidence_role'] = 'invalid'
        path.write_text(json.dumps(claim))
        with self.assertRaises(Exception):
            validate(self.root)

    def test_no_claims_still_produce_no_evidence(self):
        # Retain the original zero-evidence regression after adding the Wii ledger.
        for path in (self.root / 'records/claim').glob('wii-*.json'):
            path.unlink()
        # Audio claims about the Wii Remote cite the removed Wii claims; drop
        # them too so this corpus still has no Wii Remote claims at all.
        for path in (self.root / 'records/claim').glob('audio-wii-*.json'):
            path.unlink()
        # Remove fixture references with their claims in this isolated corpus.
        for path in (self.root / 'records/fixture').glob('wii-c5-*.json'):
            path.unlink()
        # Timing experiments reference the fixtures removed above; keep this
        # isolated no-claims corpus reference-valid without weakening its result.
        for path in (self.root / 'records/experiment').glob('wii-c5-*-host-run.json'):
            path.unlink()
        rows = {row['id']: row for row in status(self.root)}
        self.assertEqual(rows['wii-remote']['category'], 'No evidence')

    def test_unknown_only_claims_are_wip(self):
        for name in ['pro2-physical-macro-controls']:
            (self.root / 'records/claim' / (name + '.json')).unlink()
        rows = {row['id']: row for row in status(self.root)}
        self.assertEqual(rows['8bitdo-pro-2']['category'], 'Evidence in progress')


if __name__ == '__main__':
    unittest.main()
