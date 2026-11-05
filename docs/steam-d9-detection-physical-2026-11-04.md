# D9 wired Steam detection: physical feature comparison

Observed 2026-11-04 on bare-metal EndeavourOS x86-64, kernel
`7.3.0-1-mainline`, direct wired `28de:1302`, TShark 4.7.4. Anders operated
root-only usbmon capture. SDL and Dolphin were closed. No injected physical
feature command, firmware update, receiver/Bluetooth investigation or bootloader
experiment was performed. Owner disclosure authorization is virtualgamepad #159
comment 6645358188; model-value replay is compat, not universal physical fidelity.

Both sessions have `bcdDevice=0404`, a USB device-version marker. Attribute 4
reports firmware build timestamp `0x6ACFF323`; this matches Steam's own
`FWTimestamp` label, not an inferred firmware version string. Attribute 9 is
HWID `72` (`0x48`). No update prompt or other issue was reported by the owner.

## Sessions and completeness

- S1: Steam closed; 45-second capture started before one controller unplug/replug,
  then idle. Six feature exchanges, all successful: serial SET/GET, attributes
  SET/GET, restore mapping and restore settings.
- S3: 90-second capture started with Steam closed, then Stable Steam `1792618285`
  started, the controller was unplugged/replugged once, listed, idled for at
  least ten seconds and Steam closed normally. 218 feature exchanges.

Requests and completion events were paired privately by USB bus/device/URB ID.
The observed control sequence has zero unmatched submissions/completions. This
is not proof of zero capture loss: no capture drop counter was supplied.
Two addresses per session represent the connected device before/after replug;
addresses and URB IDs are omitted. Relative times use the first captured control
transfer as their origin. Kernel and userspace requests interleave in S3, so
per-request origin is not established.

The full sanitized sequence is `evidence/steam-d9-feature-exchanges.json`.
All raw captures remain outside the repositories. No serial, USB string,
account field, machine path, address or absolute capture timestamp is published.
Unknown feature payloads and serial replies are withheld, not replaced with fake
physical bytes. Only independently reviewed model fields are retained.

## Exact attribute reply

All ten observed attribute GETs return the same 63-byte USB data payload,
including report ID 1. It starts `01 83 1e`, contains six five-byte entries
(one-byte ID plus little-endian u32), then thirty zero padding bytes.
The exact selected frame is `fixtures/steam-d9-1302-attributes.hex`.

| ID | Source-backed meaning | Observed value |
| --- | --- | --- |
| 1 | Product ID | `0x1302` |
| 2 | Capabilities | `0` |
| 10 | Bootloader build timestamp | `0x68D2F92E` |
| 4 | Firmware build timestamp | `0x6ACFF323` |
| 9 | Hardware ID | `0x48` |
| 11 | Connection interval, microseconds | `4000` |

No unique-ID or radio-ID attribute appears in this frame. These six values are
model/version-scoped evidence, not calibration or proof of another unit's defaults.

## Settings writes accepted by the transport

S3 includes 55 command `0x87` SETs, each 64 bytes including report ID and each
completed with status 0. Their exact frames, in order, are selected in
`fixtures/steam-d9-steam-settings.hex`. Bytes outside the declared settings
payload are zero. Duplicate keys within a request are preserved.

| Key | Observed u16 value |
| --- | --- |
| 7, 8 | 7 |
| 9, 24, 46, 48, 84, 85 | 0 |
| 34, 45 | 100 |
| 35 | 80 |
| 49 | 2 |
| 50 | 900 |
| 52, 53 | 65535 |
| 82 | 3 |

Status 0 proves observed USB completion, not retention, readback, valid ranges,
factory defaults or physical effects. In particular, setting 50 was accepted
in this run; its name/effect is not inferred from that result alone.

## Other observed exchanges

All requests asked for 64 bytes. All observed GET completions returned 63 bytes,
including report ID 1, despite the descriptor's 63-body-byte maximum. Serial
replies declare inner length 20; the NUL-terminated string has 13 characters.
Selector 1 has the character-class pattern `UUUDDDDDDDUUD`, and selector 0
has `UUUDUDDDDDDDD` (`U` uppercase ASCII, `D` decimal digit). These patterns
contain no actual serial characters. Observed serial SET header fragments are
`01 ae 16 01`, `01 ae 15 01`, `01 ae 15 00`, and `01 ae 01 01`.
Several requests have opaque nonzero tails; full serial requests and replies
remain withheld.

The three `0xED` GETs declare inner lengths 1, 24, and 0, in that order,
after SETs declaring 24, 9, and 11. The first meaningful one-byte reply is
`00`, a non-identifying single value; its reviewed four-byte prefix is
`01 ed 01 00`. This does **not** establish that all ED replies have length 1.
Opaque bytes outside that first declared payload and the other ED bodies
remain withheld. Replaying the reviewed value with fresh zero padding is a
compat choice, not an exact replay of the entire physical frame.

The two `0xDC` SETs declare length 2 and body `01 02`; the two `0xE2`
SETs declare length 2 and body `01 20`. These small command parameters are
non-identifying. A successful completion establishes acknowledgement only;
it does not establish command semantics or retained state.

| S3 command | SET count/status | GET count/status |
| --- | --- | --- |
| `0x83` | 9 / 0 | 9 / 0 |
| `0xAE` | 11 / 0 | 11 / 0 |
| `0x87` | 55 / 0 | none observed |
| `0x81` | 7 / 0 | none observed |
| `0xC1` | 100 / -32 (STALL) | none observed |
| `0xDC`, `0xE2` | 2 each / 0 | none observed |
| `0x85`, `0x8E` | 3 each / 0 | none observed |
| `0xED` | 3 / 0 | 3 / 0 |

These outcomes do not authorize sending unknown commands or establish their
semantics. None of the forbidden bootloader/shutdown commands was generated by
the agent. No feature report 2 exchange appears in these bounded observations.

## Comparison with virtualgamepad C6

- C6's attribute reply contains no attribute entries and declares inner length 2;
  the real reply declares 30 and supplies the six entries above.
- C6 GET replies are 64 bytes. Observed physical GET replies are 63 bytes. The
  replay profile can match the attribute frame without changing the descriptor.
- The physical unit serial is deliberately withheld. C6's synthetic lifetime
  identity remains an intentional difference; do not copy a real serial.
- C6 accepts setting keys 9/48/71. The capture accepts sixteen keys, fourteen of
  which C6 currently rejects, including 50. Completion does not prove storage.
- C6 rejects DC/E2/ED as unsupported; the physical trace completes them normally.
  C1 stalls physically. No success reply or semantic behavior for these commands
  should be invented from command names alone.
- Fresh C6 log/UI comparison: virtual was not listed, with 306 controller-info
  read failures, six failed info results and no successful info record. The real
  controller listed with no such failures and HWID72/FWTimestamp0x6ACFF323.

The populated attributes are therefore a concrete compatibility lead, not proof
that they alone determine listing. The opt-in virtual replay and its UI/input
acceptance belong in the separate implementation PR.

## Reducer changes and safety

The reducer still withholds all feature payload bytes by default. Opt-in
`--model-attributes` permits IDs 1/2/3/4/5/9/10/11, excluding unique-ID 0 and
radio IDs 6/7; `--model-settings` permits only the sixteen reviewed keys above.
Unknown IDs/keys, malformed lengths, wrong report/command framing or truncated
model frames fail closed. Serial bytes remain withheld with both options enabled.
Regression fixtures for this safety logic use fake values. Public physical
fixtures contain only the explicitly reviewed non-identifying data.
