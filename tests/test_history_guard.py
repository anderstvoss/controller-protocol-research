import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from history_guard import content_scan, identity_scan


def git(root, *args, email='someone@users.noreply.github.com'):
    subprocess.run(['git', '-C', str(root), '-c', 'user.name=Fixture', '-c', 'user.email=' + email,
                    '-c', 'commit.gpgsign=false', *args], check=True, capture_output=True)


class HistoryGuard(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        git(self.root, 'init', '-q')

    def commit(self, name, text, email='someone@users.noreply.github.com'):
        (self.root / name).write_text(text)
        git(self.root, 'add', name, email=email)
        git(self.root, 'commit', '-q', '-m', 'change', email=email)

    def test_clean_history_passes(self):
        self.commit('notes.md', 'synthetic report layout\n')
        self.assertEqual(content_scan(self.root, ['--all']), [])
        self.assertEqual(identity_scan(self.root, ['--all']), [])

    def test_removed_leak_is_still_found(self):
        self.commit('notes.md', 'paired with a4:c1:38:00:11:22\n')
        self.commit('notes.md', 'redacted\n')
        problems = content_scan(self.root, ['--all'])
        self.assertTrue(any('MAC or Bluetooth address' in p for p in problems), problems)

    def test_leak_on_side_branch_is_found(self):
        self.commit('notes.md', 'clean\n')
        git(self.root, 'checkout', '-q', '-b', 'side')
        self.commit('fixture.json', '{"serial": "x"}\n')
        git(self.root, 'checkout', '-q', '-')
        problems = content_scan(self.root, ['--all'])
        self.assertTrue(any('identifying key serial' in p for p in problems), problems)

    def test_personal_commit_email_is_reported(self):
        self.commit('notes.md', 'clean\n', email='person@example.org')
        problems = identity_scan(self.root, ['--all'])
        self.assertEqual(len(problems), 1)
        self.assertIn('person@example.org', problems[0])


if __name__ == '__main__':
    unittest.main()
