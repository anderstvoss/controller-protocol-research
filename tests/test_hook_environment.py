"""Git hook context must never redirect fixture or cache commands into the checkout."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class HookEnvironment(unittest.TestCase):
    def test_both_hooks_clear_repository_local_git_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            clean = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
            subprocess.run(['git', 'init', '-q', str(root / 'outer')], env=clean, check=True)
            (root / 'bin').mkdir()
            # Only the hook's tooling is stubbed; real git reports its local variables.
            (root / 'bin/gitleaks').write_text('#!/bin/sh\nexit 0\n')
            (root / 'bin/pre-commit').write_text('#!/usr/bin/env python3\nimport json, os\nfrom pathlib import Path\nPath(os.environ["W1_ENV_RESULT"]).write_text(json.dumps({k:v for k,v in os.environ.items() if k in ["GIT_DIR","GIT_WORK_TREE","GIT_COMMON_DIR","GIT_INDEX_FILE","GIT_PREFIX"]}))\n')
            for tool in (root / 'bin').iterdir():
                tool.chmod(0o700)
            for name in ['pre-commit', 'pre-push']:
                result = root / (name + '.json')
                env = dict(clean, PATH=str(root / 'bin') + os.pathsep + clean['PATH'],
                           W1_ENV_RESULT=str(result), GIT_DIR=str(root / 'outer/.git'),
                           GIT_WORK_TREE=str(root / 'outer'), GIT_COMMON_DIR=str(root / 'outer/.git'),
                           GIT_INDEX_FILE=str(root / 'outer/.git/index'), GIT_PREFIX='')
                subprocess.run(['bash', str(ROOT / '.githooks' / name)], cwd=root / 'outer',
                               env=env, input=b'', check=True, capture_output=True)
                self.assertEqual(json.loads(result.read_text()), {}, name)
