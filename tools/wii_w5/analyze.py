"""Reduce W5 own-device traces; retain ambiguity rather than invent an actor."""
from collections import Counter

OFFSETS = {0x32: 3, 0x34: 3, 0x35: 6, 0x36: 13, 0x37: 16, 0x3D: 1}
EXPECTED = {(8500, 7000, 9000), (7800, 9000, 7000)}


def decode_gyro(payload):
    if len(payload) < 6 or payload[5] & 3 != 2:
        raise ValueError('not a valid gyro-marked six-byte payload')
    raw = [payload[i] | ((payload[i + 3] << 6) & 0xFF00) for i in range(3)]
    slow = [bool(payload[3] & 2), bool(payload[4] & 2), bool(payload[3] & 1)]
    return raw, slow


def interval(rows, case, arm):
    start = next(r['ns'] for r in rows if r.get('kind') == 'marker' and
                 r.get('case') == case and r.get('arm') == arm and r.get('label') == 'child_start')
    end = next(r['ns'] for r in rows if r.get('kind') == 'marker' and
               r.get('case') == case and r.get('arm') == arm and r.get('label') == 'child_end')
    return sorted((r for r in rows if start <= r['ns'] <= end), key=lambda r: r['ns']), start


def packet_checks(rows):
    """Track ACKed map/reset writes and inspect the captured active input bytes."""
    mode, pending = 0, None
    gyro, passthrough, bad = 0, 0, 0
    vectors, slow_flags, map_modes = Counter(), Counter(), Counter()
    samples, last_kind, alternation_errors = [], None, 0
    for r in rows:
        if 'hex' not in r:
            continue
        packet = bytes.fromhex(r['hex'])
        if r['kind'] == 'host-output' and len(packet) >= 7 and packet[0] == 0x16:
            pending = packet
        if r['kind'] == 'device-input' and len(packet) >= 5 and packet[0] == 0x22 and packet[3] == 0x16:
            if pending and packet[4] == 0:
                address = int.from_bytes(pending[2:5], 'big')
                if address in (0xA600FE, 0xA400FE) and pending[6] in (4, 5, 7):
                    mode = pending[6]
                    map_modes[mode] += 1
                    last_kind = None
                elif address in (0xA400F0, 0xA600F0) and pending[6] == 0x55:
                    mode = 0
                    last_kind = None
            pending = None
        if r['kind'] != 'device-input' or not packet or not mode:
            continue
        offset = OFFSETS.get(packet[0])
        if offset is None or len(packet) < offset + 6:
            continue
        payload = packet[offset:offset + 6]
        if payload[5] & 3 == 2:
            raw, slow = decode_gyro(payload)
            gyro += 1
            vectors[tuple(raw)] += 1
            slow_flags[tuple(slow)] += 1
            if tuple(raw) not in EXPECTED or slow != [True, True, True]:
                bad += 1
            kind = 'gyro'
        elif mode == 5 and payload[5] & 3 == 0:
            passthrough += 1
            kind = 'downstream'
        else:
            bad += 1
            kind = 'invalid'
        if mode == 5:
            alternation_errors += last_kind == kind
            last_kind = kind
        if len(samples) < 8 or not any(x['payload_hex'] == payload.hex() for x in samples):
            if len(samples) < 32:
                samples.append({'report_id_hex': f'{packet[0]:02x}', 'mode': mode,
                                'payload_hex': payload.hex(), 'classification': kind})
    return {'gyro_packets': gyro, 'downstream_packets': passthrough, 'invalid_or_mismatched': bad,
            'vectors': [{'raw_yaw_roll_pitch': list(k), 'count': v} for k, v in sorted(vectors.items())],
            'slow_flags': [{'yaw_roll_pitch': list(k), 'count': v} for k, v in sorted(slow_flags.items())],
            'acked_map_modes': [{'mode': k, 'count': v} for k, v in sorted(map_modes.items())],
            'mode5_alternation_errors': alternation_errors, 'examples': samples}


def transactions(rows, start):
    direct = [r for r in rows if r['kind'] == 'raw-output']
    selected = []
    for row in rows:
        if row['kind'] != 'host-output':
            continue
        p = bytes.fromhex(row['hex'])
        if len(p) < 5 or p[0] not in (0x16, 0x17):
            continue
        address = int.from_bytes(p[2:5], 'big')
        if address not in (0xA400F0, 0xA600FE, 0xA400FA, 0xA600FA, 0xA400FE, 0xA600F0):
            continue
        matches = [r for r in direct if r['hex'] == row['hex'] and abs(r['ns'] - row['ns']) < 100_000_000]
        actor = matches[0]['actor'] if len(matches) == 1 else ('ambiguous' if matches else 'kernel_or_untraced')
        selected.append({'relative_ns': row['ns'] - start, 'hex': row['hex'],
                         'address_hex': f'{address:06x}', 'actor': actor,
                         'matching_raw_writes': len(matches)})
    return selected


def observations(rows, messages, case, arm):
    """Publish semantic own-device fields, never raw logs or device identities."""
    selected, start = interval(rows, case, arm)
    summary = next(m for m in messages if m['kind'] == 'summary')
    commands = []
    for item in transactions(selected, start):
        packet = bytes.fromhex(item.pop('hex'))
        item['report_id_hex'] = f'{packet[0]:02x}'
        if packet[0] == 0x16:
            item['write_data_hex'] = packet[6:6 + packet[5]].hex()
        else:
            item['read_length'] = int.from_bytes(packet[5:7], 'big')
        commands.append(item)
    packets = packet_checks(selected)
    # Counts and independent decoded values suffice; raw packets stay private.
    packets.pop('examples')
    return {'case': case, 'arm': arm, 'summary': summary,
            'identity_readbacks': [m for m in messages if m['kind'] == 'ids'],
            'markers': [{'relative_ns': r['ns'] - start, 'label': r['label']}
                        for r in selected if r['kind'] == 'marker'],
            'transactions': commands, 'packets': packets,
            'private_cached_mode': 'not_instrumented',
            'actor_limit': 'Unique equal raw write within100ms identifies an observed writer; '
                           'multiple matches remain ambiguous; unmatched is kernel_or_untraced.',
            'api_limit': 'Markers bracket public SDL_Init/SDL_OpenJoystick, not private InitDevice. '
                         'Explicit probe and SDL same-address replies may overlap.'}
