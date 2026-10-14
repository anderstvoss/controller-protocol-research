"""Disclosure scan over every blob and commit identity reachable from any ref.

Publishing a repository publishes its whole history, including branches and
pull-request refs, so the tree-level publication guard is not enough. This
applies the same content checks to every historical file version and reports
commit author/committer emails that are not GitHub or bot noreply addresses.
"""
import argparse
import subprocess
import sys
from pathlib import Path
from publication_guard import content_problems

NOREPLY_SUFFIXES = ('@users.noreply.github.com',)
NOREPLY_ADDRESSES = {'noreply@github.com', 'noreply@anthropic.com'}


def git(root, *args, data=None):
    return subprocess.run(['git', '-C', str(root), *args], input=data, check=True,
                          capture_output=True).stdout


def blobs(root, refs):
    """Yield (path, blob id) once per distinct blob reachable from refs."""
    seen = set()
    for line in git(root, 'rev-list', '--objects', *refs).decode().splitlines():
        sha, _, path = line.partition(' ')
        if path and sha not in seen:
            seen.add(sha)
            yield path, sha


def content_scan(root, refs):
    entries = list(blobs(root, refs))
    if not entries:
        return []
    types = git(root, 'cat-file', '--batch-check=%(objecttype)',
                data=''.join(sha + '\n' for _, sha in entries).encode()).decode().split()
    files = [(path, sha) for (path, sha), kind in zip(entries, types) if kind == 'blob']
    problems = []
    for path, sha in files:
        data = git(root, 'cat-file', 'blob', sha)
        problems.extend(p + ' (blob ' + sha[:12] + ')' for p in content_problems(path, data))
    return problems


def identity_scan(root, refs):
    commits = {}
    log = git(root, 'log', '--format=%h%x00%ae%x00%ce', *refs).decode()
    for line in log.splitlines():
        commit, author, committer = line.split('\0')
        for email in {author, committer}:
            if email not in NOREPLY_ADDRESSES and not email.endswith(NOREPLY_SUFFIXES):
                commits.setdefault(email, []).append(commit)
    return ['commit email ' + email + ' in ' + str(len(ids)) + ' commit(s): ' + ' '.join(sorted(ids))
            for email, ids in sorted(commits.items())]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', default=Path(__file__).resolve().parents[1])
    parser.add_argument('--identities', choices=['fail', 'warn'], default='fail',
                        help='whether non-noreply commit emails fail the scan')
    args = parser.parse_args()
    refs = ['--all']
    content = content_scan(args.root, refs)
    identities = identity_scan(args.root, refs)
    for problem in content:
        print(problem, file=sys.stderr)
    for problem in identities:
        print(('error: ' if args.identities == 'fail' else 'warning: ') + problem, file=sys.stderr)
    if content or (identities and args.identities == 'fail'):
        sys.exit(1)
    print('History guard passed' + (' with identity warnings' if identities else ''))


if __name__ == '__main__':
    main()
