import copy
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from validate import validate


class AcceptanceRun(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'corpus'
        shutil.copytree(Path(__file__).resolve().parents[1], self.root,
                        ignore=shutil.ignore_patterns('.git', '.venv', '__pycache__'))
        self.record_path = self.root / 'records/fixture/acceptance-dualsense-uinput-n1-c2.json'
        self.record = json.loads(self.record_path.read_text())
        self.run = json.loads((self.root / self.record['path']).read_text())

    def save(self, run=None):
        if run is not None:
            data = json.dumps(run).encode()
            (self.root / self.record['path']).write_bytes(data)
            self.record['sha256'] = hashlib.sha256(data).hexdigest()
        self.record_path.write_text(json.dumps(self.record))

    def test_measured_runs_validate(self):
        self.assertGreater(validate(self.root), 0)

    def test_cannot_label_virtual_run_physical(self):
        self.record['kind'] = 'physical'
        self.save()
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_fake_backend_cannot_be_measured_host_evidence(self):
        run = copy.deepcopy(self.run)
        run['environment']['synthetic'] = True
        run['environment']['backend'] = 'fake'
        self.save(run)
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_stage_cannot_have_both_measurement_and_missing_reason(self):
        run = copy.deepcopy(self.run)
        run['samples'][0]['stages']['api_call']['reason'] = 'contradicts measured value'
        self.save(run)
        with self.assertRaises(Exception):
            validate(self.root)

    def test_virtual_experiment_required(self):
        self.record['experiments'] = ['seed-inspection']
        self.save()
        with self.assertRaises(ValueError):
            validate(self.root)


if __name__ == '__main__':
    unittest.main()
