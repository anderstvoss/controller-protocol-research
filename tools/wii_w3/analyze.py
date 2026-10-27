"""Reduce owned virtual UHID trace rows without paths or application log text."""
from collections import Counter


def summarize(rows, start_ns, end_ns, attach_marker_ns):
    rows = [r for r in rows if start_ns <= r['ns'] < end_ns]
    counts = Counter((r['direction'], r['hex'][:2]) for r in rows)
    selected = []
    want_data = False
    for row in rows:
        packet = bytes.fromhex(row['hex'])
        if not packet:
            continue
        report = packet[0]
        keep = (row['direction'] == 'host-output' and report in [0x12, 0x15, 0x16, 0x17]) or (
            row['direction'] == 'device-input' and report in [0x20, 0x21, 0x22])
        if keep and report in [0x12, 0x20]:
            want_data = True
        if row['direction'] == 'device-input' and report >= 0x30 and want_data:
            keep, want_data = True, False
        if keep:
            selected.append({'relative_ns': row['ns'] - start_ns,
                             'direction': row['direction'], 'hex': row['hex']})
    # Marker follows attach +300ms service; /proc/uptime quantization is10ms.
    candidates = [r for r in rows if attach_marker_ns - 500_000_000 <= r['ns'] <= attach_marker_ns
                  and r['direction'] == 'device-input' and r['hex'].startswith('20')]
    transition = None
    if candidates:
        status = candidates[0]
        mode = next((r for r in rows if status['ns'] < r['ns'] < status['ns'] + 100_000_000
                     and r['direction'] == 'host-output' and r['hex'].startswith('12')), None)
        data = next((r for r in rows if mode and mode['ns'] < r['ns'] < mode['ns'] + 100_000_000
                     and r['direction'] == 'device-input' and int(r['hex'][:2], 16) >= 0x30), None)
        if mode and data:
            transition = {'status_relative_ns': status['ns'] - start_ns,
                          'status_hex': status['hex'], 'mode_hex': mode['hex'],
                          'mode_delay_ns': mode['ns'] - status['ns'],
                          'data_delay_after_mode_ns': data['ns'] - mode['ns'],
                          'data_hex': data['hex']}
    return {'report_counts': [{'direction': k[0], 'report_id_hex': k[1], 'count': v}
                              for k, v in sorted(counts.items())],
            'selected_reports': selected, 'nunchuk_status_resume': transition}
