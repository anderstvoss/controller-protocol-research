"""Generate a synthetic reference shape from independently downloaded pinned sources.

No upstream source is redistributed. Input files must match the ledger hashes.
Usage: python tools/wii_consumer_shape.py SOURCE_DIRECTORY > synthetic-shape.json
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def constants(text):
    result = {}
    for name, value in re.findall(r'^#define\s+(\w+)\s+(0x[0-9a-fA-F]+|\d+|[A-Z][A-Z_0-9]+)\b', text, re.M):
        try:
            result[name] = int(value, 0)
        except ValueError:
            if value in result:
                result[name] = result[value]
    return result


def key_map(text, table):
    block = text.split('static const __u16 ' + table + '[] = {', 1)[1].split('};', 1)[0]
    block = re.sub(r'/\*.*?\*/', '', block, flags=re.S)
    return re.findall(r'\b(?:KEY|BTN)_[A-Z0-9_]+\b', block)


def axes(text, start, end):
    block = '\n'.join(text.splitlines()[start - 1:end])
    return [(name, int(lo), int(hi), int(fuzz), int(flat)) for name, lo, hi, fuzz, flat in re.findall(
        r'input_set_abs_params\([^,]+,\s*(ABS_\w+),\s*(-?\d+),\s*(-?\d+),\s*(\d+),\s*(\d+)\)', block)]


def read(directory, name, record):
    data = (Path(directory) / name).read_bytes()
    expected = json.loads((ROOT / f'records/source/{record}.json').read_text())['sha256']
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError('source hash mismatch: ' + name)
    return data.decode()


def shape(directory):
    text = read(directory, 'modules.c', 'wii-linux-modules')
    codes = constants(read(directory, 'input-event-codes.h', 'wii-c5-linux-input-codes'))
    codes.update(constants(read(directory, 'input.h', 'wii-c5-linux-input-ff')))
    base = 'Nintendo Wii Remote'
    nodes = [(base, key_map(text, 'wiimod_keys_map'), [], True),
             (base + ' Accelerometer', [], axes(text, 498, 507), False),
             (base + ' IR', [], axes(text, 750, 769), False),
             (base + ' Nunchuk', key_map(text, 'wiimod_nunchuk_map'), axes(text, 945, 967), False),
             (base + ' Classic Controller', key_map(text, 'wiimod_classic_map'), axes(text, 1239, 1264), False),
             (base + ' Motion Plus', [], axes(text, 2814, 2826), False)]
    if [len(node[2]) for node in nodes] != [0, 3, 8, 5, 6, 3]:
        raise ValueError('source consumer shape changed')
    sources, controls = [], []
    for index, (name, keys, absolute, rumble) in enumerate(nodes):
        entries = [dict(source_index=index, event_type=1, code=codes[key], absolute_range=None) for key in keys]
        entries += [dict(source_index=index, event_type=3, code=codes[axis], absolute_range=dict(
            minimum=lo, maximum=hi, fuzz=fuzz, flat=flat, resolution=0)) for axis, lo, hi, fuzz, flat in absolute]
        if rumble:
            entries.append(dict(source_index=index, event_type=21, code=codes['FF_RUMBLE'], absolute_range=None))
        # Synthetic identity metadata is explicit; this is not a capture.
        sources.append(dict(reported_name=name, bus_type=5, vendor_id=0x057e, product_id=0x0306,
                            version=0, transport='Bluetooth', control_count=len(entries)))
        controls += entries
    return dict(manifest=dict(format_version=1, synthetic=True, sources=sources), controls=controls, frames=[])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_directory', type=Path)
    args = parser.parse_args()
    print(json.dumps(shape(args.source_directory), indent=2))
