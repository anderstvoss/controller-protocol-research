"""Structural publication backstop: rejects files and values that should never be public.

Passing does not prove a fixture is safe to publish; it only catches leaks with
a recognisable shape (paths, addresses, credentials, oversized or unexpected files).
"""
import json
import re
import sys
from pathlib import Path

MAX_FILE_BYTES = 256 * 1024
ALLOWED_TOP_LEVEL = {
    '.githooks', '.github', '.gitignore', '.pre-commit-config.yaml', 'CHANGELOG.md',
    'CONTRIBUTING.md', 'LICENSE', 'LICENSE-DATA', 'NOTICE', 'README.md',
    'SECURITY.md', 'docs', 'evidence', 'fixtures', 'records', 'requirements-dev.in',
    'requirements-dev.txt', 'ruff.toml', 'schemas', 'scripts', 'tests', 'tools',
}
FIXTURE_SUFFIXES = {'.hex'}
FORBIDDEN_KEYS = {'serial', 'serial_number', 'uniq', 'phys', 'mac', 'mac_address',
                  'bluetooth_address', 'bt_address', 'hostname', 'username'}
PATTERNS = [
    ('host path', re.compile(r'(?<![\w.])(/home/|/Users/|/root/|[A-Za-z]:\\\\?Users\\\\?)')),
    ('MAC or Bluetooth address', re.compile(r'\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b')),
    ('evdev phys path', re.compile(r'\b(?:usb|pci)-[0-9a-f]{4}:[0-9a-f]{2}:[0-9a-f]{2}')),
    ('private IPv4 address', re.compile(r'\b(?:10|127|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}(?:\.\d{1,3})?\b')),
    ('email address', re.compile(r'\b[\w.+-]+@[\w-]+\.[\w.-]+\b')),
    ('private key', re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----')),
    ('GitHub token', re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})')),
]
# License texts are verbatim third-party documents.
SKIP_CONTENT = {'LICENSE', 'LICENSE-DATA'}
# The guard and its tests necessarily contain the patterns they look for.
SKIP_PATTERNS = {'tools/publication_guard.py', 'tests/test_publication_guard.py',
                 'tools/history_guard.py', 'tests/test_history_guard.py',
                 '.githooks/pre-push', '.pre-commit-config.yaml'}


def forbidden_keys(value, trail=''):
    if isinstance(value, dict):
        for key, child in value.items():
            here = trail + '.' + key if trail else key
            if key.lower() in FORBIDDEN_KEYS:
                yield here
            yield from forbidden_keys(child, here)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from forbidden_keys(child, trail + '[' + str(index) + ']')


def check(root):
    root = Path(root).resolve()
    problems = []
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root)
        parts = relative.parts
        if parts[0] in {'.git', '.venv', '.ruff_cache'} or '__pycache__' in parts or not path.is_file():
            continue
        name = relative.as_posix()
        if parts[0] not in ALLOWED_TOP_LEVEL:
            problems.append(name + ': unexpected top-level entry')
        size = path.stat().st_size
        if size > MAX_FILE_BYTES:
            problems.append(name + ': ' + str(size) + ' bytes exceeds ' + str(MAX_FILE_BYTES))
        if parts[0] == 'fixtures' and path.suffix not in FIXTURE_SUFFIXES:
            problems.append(name + ': fixtures must be reviewed hex text')
        problems.extend(content_problems(name, path.read_bytes()))
    return problems


def content_problems(name, data):
    """Identifying content in one file, shared by the tree and history scans."""
    if name in SKIP_CONTENT:
        return []
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        return [name + ': binary files are not accepted']
    problems = []
    if name not in SKIP_PATTERNS:
        for label, pattern in PATTERNS:
            match = pattern.search(text)
            if match:
                line = text.count('\n', 0, match.start()) + 1
                problems.append(name + ':' + str(line) + ': ' + label)
    if name.endswith('.json'):
        try:
            value = json.loads(text)
        except ValueError:
            return problems + [name + ': invalid JSON']
        for key in forbidden_keys(value):
            problems.append(name + ': identifying key ' + key)
    return problems


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    problems = check(root)
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        sys.exit(1)
    print('Publication guard passed')


if __name__ == '__main__':
    main()
