import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from publication_guard import check


class PublicationGuard(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'corpus'
        shutil.copytree(Path(__file__).resolve().parents[1], self.root,
                        ignore=shutil.ignore_patterns('.git', '.venv', '__pycache__'))

    def test_current_corpus_passes(self):
        self.assertEqual(check(self.root), [])

    def test_identifying_text_is_rejected(self):
        leaks = [
            'captured on /home/someone/lab',
            'paired with a4:c1:38:00:11:22',
            'phys usb-0000:00:14.0-1/input0',
            'lab host 192.168.1.20',
            'contact tester@example.com',
            '-----BEGIN OPENSSH PRIVATE KEY-----',
        ]
        for leak in leaks:
            with self.subTest(leak=leak):
                p = self.root / 'records/claim/ds-input.json'
                original = p.read_text()
                value = json.loads(original)
                value['statement'] = leak
                p.write_text(json.dumps(value))
                self.assertTrue(check(self.root))
                p.write_text(original)

    def test_identifying_keys_are_rejected(self):
        p = self.root / 'records/fixture/ds-neutral.json'
        value = json.loads(p.read_text())
        value['uniq'] = 'redacted'
        p.write_text(json.dumps(value))
        self.assertIn('records/fixture/ds-neutral.json: identifying key uniq', check(self.root))

    def test_raw_and_oversized_files_are_rejected(self):
        (self.root / 'fixtures/capture.pcapng').write_bytes(b'\x0a\x0d\x0d\x0a')
        (self.root / 'fixtures/huge.hex').write_text('00' * 200 * 1024)
        (self.root / 'captures').mkdir()
        (self.root / 'captures/raw.txt').write_text('x')
        problems = '\n'.join(check(self.root))
        self.assertIn('fixtures/capture.pcapng: fixtures must be reviewed hex text', problems)
        self.assertIn('fixtures/huge.hex', problems)
        self.assertIn('captures/raw.txt: unexpected top-level entry', problems)


if __name__ == '__main__':
    unittest.main()
