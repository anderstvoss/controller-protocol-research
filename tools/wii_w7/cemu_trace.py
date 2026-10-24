"""Reduce an owned Cemu raw-I/O trace; never treat delivered packets as decoded gyro."""
import collections
import json


def reduce_trace(events):
    counts = collections.Counter()
    modes = collections.Counter()
    reports = collections.Counter()
    reads = collections.Counter()
    writes = collections.Counter()
    read_errors = collections.Counter()
    addressed_errors = collections.Counter()
    for event in events:
        kind = event['kind']
        if kind == 'owned-open' and event['fd'] >= 0:
            counts['owned_raw_opens'] += 1
        elif kind.startswith('owned-enumerated-caller-'):
            counts['owned_enumeration_observations'] += 1
        elif kind == 'raw-write':
            data = bytes.fromhex(event['hex'])
            # Failed/partial writes do not prove a request was sent.
            if not data or event['result'] != len(data):
                counts['failed_or_partial_writes'] += 1
                continue
            counts['native_raw_writes'] += 1
            if data[0] == 0x15:
                counts['status_requests'] += 1
            elif data[0] == 0x12 and len(data) >= 3:
                modes[f'{data[2]:02x}'] += 1
            elif data[0] == 0x17 and len(data) >= 7:
                address = int.from_bytes(data[2:5], 'big')
                size = int.from_bytes(data[5:7], 'big')
                reads[f'{address:06x}/{size}'] += 1
            elif data[0] == 0x16 and len(data) >= 6:
                size = data[5]
                if len(data) < 6 + size:
                    counts['truncated_memory_writes'] += 1
                    continue
                # Only protocol register addresses and one-byte values are public.
                if size == 1:
                    writes[f'{int.from_bytes(data[2:5], "big"):06x}/{data[6]:02x}'] += 1
        elif kind == 'raw-read':
            data = bytes.fromhex(event['hex'])
            if not data or event['result'] != len(data):
                continue
            reports[f'{data[0]:02x}'] += 1
            if data[0] == 0x21 and len(data) >= 6:
                read_errors[f'{data[3] & 15:x}'] += 1
                addressed_errors[f'{int.from_bytes(data[4:6], "big"):04x}/{data[3] & 15:x}'] += 1
    return {
        'counts': dict(sorted(counts.items())),
        'native_report_modes': dict(sorted(modes.items())),
        'native_memory_reads': dict(sorted(reads.items())),
        'native_single_byte_register_writes': dict(sorted(writes.items())),
        'received_report_ids': dict(sorted(reports.items())),
        'memory_read_reply_errors': dict(sorted(read_errors.items())),
        'memory_read_address_errors': dict(sorted(addressed_errors.items())),
        'decoded_gyro_observed': False,
        'gyro_oracle': 'raw transport observations only; no decoded application-state oracle',
    }


if __name__ == '__main__':
    import sys
    from pathlib import Path

    print(json.dumps(reduce_trace(json.loads(line) for line in Path(sys.argv[1]).read_text().splitlines()),
                     indent=2, sort_keys=True))
