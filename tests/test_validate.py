import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from validate import validate
from sanitize import transform


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
