"""The superproject runs corpus tests from outside the research checkout."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class WiiW7CemuImport(unittest.TestCase):
    def test_cemu_tests_discover_from_an_unrelated_working_directory(self):
        with tempfile.TemporaryDirectory() as scratch:
            result = subprocess.run(
                [sys.executable, '-m', 'unittest', 'discover', '-s', str(ROOT / 'tests'),
                 '-p', 'test_wii_w7_cemu_appimage.py'],
                cwd=scratch, text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('Ran 3 tests', result.stderr)
