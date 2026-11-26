import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from validate import validate, validate_claim_transport
from sanitize import transform


class TransportApplicability(unittest.TestCase):
    def claim(self, id):
        path = Path(__file__).resolve().parents[1] / 'records' / 'claim' / (id + '.json')
        return json.loads(path.read_text())

    def test_missing_experiment_rejected_for_all_measured_transports(self):
        for transport in ('usb', 'bluetooth', 'receiver'):
            with self.subTest(transport=transport):
                claim = self.claim('ds-input')
                claim['applicability']['transport'] = transport
                with self.assertRaisesRegex(
                    ValueError, f'ds-input.*{transport}.*without an experiment.*source_only/not_measured'
                ):
                    validate_claim_transport(claim)

    def test_unknown_device_gap_allowed(self):
        claim = self.claim('sc2-gap-ble-identity')
        self.assertEqual(claim['status'], 'unknown')
        self.assertEqual(claim['experiments'], [])
        for transport in ('usb', 'bluetooth', 'receiver'):
            with self.subTest(transport=transport):
                claim['applicability']['transport'] = transport
                validate_claim_transport(claim)
        claim['evidence_role'] = 'consumer'
        with self.assertRaisesRegex(ValueError, 'sc2-gap-ble-identity'):
            validate_claim_transport(claim)

    def test_named_implementation_exceptions(self):
        for id in (
            'puck-current',
            'sc2-gap-puck-slots',
            'sc2-migration-openpuck-identities',
            'sc2-migration-openpuck-report-declarations',
            'sc2-migration-openpuck-slots',
        ):
            with self.subTest(id=id):
                claim = self.claim(id)
                self.assertEqual(claim['experiments'], [])
                self.assertEqual(claim['applicability']['transport'], 'usb')
                validate_claim_transport(claim)
                claim['applicability']['transport'] = 'bluetooth'
                with self.assertRaisesRegex(ValueError, id):
                    validate_claim_transport(claim)
                claim['applicability']['transport'] = 'usb'
                claim['id'] = 'unlisted-device-implementation'
                with self.assertRaisesRegex(ValueError, 'unlisted-device-implementation'):
                    validate_claim_transport(claim)

    def test_named_consumer_gap_exception(self):
        claim = self.claim('xbox-xone-physical-unknown')
        self.assertEqual(claim['experiments'], [])
        self.assertEqual(claim['evidence_role'], 'consumer')
        self.assertEqual(claim['status'], 'unknown')
        self.assertEqual(claim['applicability']['transport'], 'usb')
        validate_claim_transport(claim)
        claim['status'] = 'source_supported'
        with self.assertRaisesRegex(ValueError, 'xbox-xone-physical-unknown'):
            validate_claim_transport(claim)

    def test_claim_with_experiment_allowed(self):
        for id in ('ds-vg-exp0015-physical-usb-hid', 'puck-historical-physical'):
            with self.subTest(id=id):
                claim = self.claim(id)
                self.assertTrue(claim['experiments'])
                self.assertIn(claim['applicability']['transport'], ('usb', 'receiver'))
                validate_claim_transport(claim)

    def test_non_measured_transport_allowed(self):
        claim = self.claim('sc2-cadence')
        self.assertEqual(claim['applicability']['transport'], 'source_only')
        self.assertEqual(claim['experiments'], [])
        validate_claim_transport(claim)
        claim['applicability']['transport'] = 'not_measured'
        validate_claim_transport(claim)
        claim['applicability']['transport'] = 'usb'
        with self.assertRaisesRegex(ValueError, 'sc2-cadence'):
            validate_claim_transport(claim)


class Integrity(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'corpus'
        shutil.copytree(Path(__file__).resolve().parents[1], self.root,
                        ignore=shutil.ignore_patterns('.git', '.venv', '__pycache__'))

    def edit(self, record_path, **updates):
        p = self.root / record_path
        value = json.loads(p.read_text())
        value.update(updates)
        p.write_text(json.dumps(value))

    def test_seed_and_conflict_are_valid(self):
        self.assertGreater(validate(self.root), 10)

    def test_reference_and_hash_failures(self):
        for update in [{'sources': ['missing']}, {'sha256': '0' * 64}, {'path': '../escape.hex'}]:
            with self.subTest(update=update):
                p = self.root / 'records/fixture/ds-neutral.json'
                original = p.read_text()
                self.edit(str(p.relative_to(self.root)), **update)
                with self.assertRaises(ValueError):
                    validate(self.root)
                p.write_text(original)

    def test_measured_transport_rule_is_enforced(self):
        path = 'records/claim/ds-input.json'
        applicability = json.loads((self.root / path).read_text())['applicability']
        applicability['transport'] = 'usb'
        self.edit(path, applicability=applicability)
        with self.assertRaisesRegex(ValueError, 'ds-input.*without an experiment'):
            validate(self.root)

    def test_unjustified_physical_promotion(self):
        self.edit('records/claim/ds-input.json', status='physically_validated', experiments=['seed-inspection'])
        with self.assertRaisesRegex(ValueError, 'physical promotion'):
            validate(self.root)

    def test_copied_sources_are_not_independent(self):
        self.edit('records/claim/ds-input.json', status='independently_corroborated', sources=['kernel', 'uhid'])
        with self.assertRaisesRegex(ValueError, 'lineages'):
            validate(self.root)

    def test_transformation_records_lineage_and_rejects_overwrite(self):
        transform(self.root, 'ds-neutral', 'redacted', 1, bytes([0, 0]))
        self.assertGreater(validate(self.root), 10)
        with self.assertRaisesRegex(ValueError, 'already exists'):
            transform(self.root, 'ds-neutral', 'redacted', 1, bytes([0]))
        self.edit('records/fixture/redacted.json', parent='redacted')
        with self.assertRaisesRegex(ValueError, 'cyclic'):
            validate(self.root)

    def test_transformation_parent_is_a_fixture_id(self):
        for parent in ['', '../claim/ds-input', '/outside', 'missing', 'ds-neutral/..']:
            with self.subTest(parent=parent), self.assertRaisesRegex(ValueError, 'parent'):
                transform(self.root, parent, 'derived', 0, bytes([0]))
        self.assertFalse((self.root / 'fixtures/derived.hex').exists())
        self.assertFalse((self.root / 'records/fixture/derived.json').exists())

    def test_transformation_bounds(self):
        for offset in [-1, 64]:
            with self.assertRaisesRegex(ValueError, 'in-bounds'):
                transform(self.root, 'ds-neutral', 'bad', offset, bytes([0]))


if __name__ == '__main__':
    unittest.main()
