"""Create a derived hex fixture with explicit replacement and hashed lineage."""
import argparse
import hashlib
import json
from pathlib import Path
from validate import validate


def transform(root, parent_id, new_id, offset, replacement):
    root = Path(root)
    validate(root)
    if not new_id or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in new_id):
        raise ValueError('new ID must use lowercase ASCII letters, digits, or hyphens')
    if not parent_id or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in parent_id):
        raise ValueError('parent ID must use lowercase ASCII letters, digits, or hyphens')
    parent_path = root / 'records/fixture' / (parent_id + '.json')
    if not parent_path.is_file():
        raise ValueError('parent must name an existing fixture')
    parent = json.loads(parent_path.read_text())
    if parent['id'] != parent_id:
        raise ValueError('parent ID must match the fixture record')
    data = bytearray.fromhex((root / parent['path']).read_text())
    if offset < 0 or not replacement or offset + len(replacement) > len(data):
        raise ValueError('replacement must be a nonempty in-bounds range')
    path = 'fixtures/' + new_id + '.hex'
    record_path = root / 'records/fixture' / (new_id + '.json')
    if record_path.exists() or (root / path).exists():
        raise ValueError('output already exists')
    data[offset:offset + len(replacement)] = replacement
    encoded = (data.hex() + '\n').encode()
    record = dict(parent, id=new_id, kind='sanitized', path=path,
                  sha256=hashlib.sha256(encoded).hexdigest(), parent=parent_id,
                  transform=f'replace bytes [{offset}, {offset + len(replacement)}); parent sha256={parent["sha256"]}')
    (root / path).write_bytes(encoded)
    record_path.write_text(json.dumps(record, indent=2) + '\n')
    validate(root)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['root', 'parent', 'id']:
        parser.add_argument(name)
    parser.add_argument('offset', type=int)
    parser.add_argument('replacement_hex')
    args = parser.parse_args()
    transform(args.root, args.parent, args.id, args.offset, bytes.fromhex(args.replacement_hex))
