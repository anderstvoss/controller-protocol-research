"""Per-controller evidence category, derived from claim records; no network resolution."""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from validate import validate

# Categories, weakest first. Each claim status maps to the strongest category it supports.
CATEGORIES = ['No evidence', 'Evidence in progress', 'Source evidence', 'Physical evidence']
STATUS_CATEGORY = {
    'unknown': 'Evidence in progress', 'inferred': 'Evidence in progress', 'conflicted': 'Evidence in progress', 'rejected': 'Evidence in progress',
    'source_supported': 'Source evidence', 'independently_corroborated': 'Source evidence',
    'physically_observed': 'Physical evidence', 'physically_validated': 'Physical evidence',
}


def stronger(a, b):
    return a if CATEGORIES.index(a) >= CATEGORIES.index(b) else b


def load(root, category):
    return [json.loads(p.read_text()) for p in sorted((Path(root) / 'records' / category).glob('*.json'))]


def status(root):
    validate(root)
    rows = []
    claims = load(root, 'claim')
    for controller in load(root, 'controller'):
        own = [c for c in claims if c['applicability']['controller'] == controller['id']]
        category = 'No evidence'
        transports = {}
        for claim in own:
            level = STATUS_CATEGORY[claim['status']]
            category = stronger(category, level)
            transport = claim['applicability']['transport']
            transports[transport] = stronger(transports.get(transport, 'No evidence'), level)
        rows.append({
            'id': controller['id'],
            'name': controller['name'],
            'kind': controller['kind'],
            'tracking': controller['tracking'],
            'category': category,
            'claims': dict(sorted(Counter(c['status'] for c in own).items())),
            'transports': dict(sorted(transports.items())),
        })
    return rows


def markdown(rows):
    lines = ['| Controller | Tracking | Category | Claims | By transport |', '| --- | --- | --- | --- | --- |']
    for row in rows:
        claims = ', '.join(f'{status} {count}' for status, count in row['claims'].items()) or 'none'
        transports = ', '.join(f'{t}: {c}' for t, c in row['transports'].items()) or 'none'
        lines.append(f"| {row['name']} (`{row['id']}`) | {row['tracking'] or ''} | {row['category']} | {claims} | {transports} |")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', default=Path(__file__).resolve().parents[1])
    parser.add_argument('--json', action='store_true', help='print machine-readable rows')
    args = parser.parse_args()
    try:
        rows = status(args.root)
    except (ValueError, OSError, KeyError) as error:
        sys.exit(str(error))
    print(json.dumps(rows, indent=2) if args.json else markdown(rows))


if __name__ == '__main__':
    main()
