# D9 wired input and reverse-output reference

Owner-operated physical measurements on 2026-11-04 Pacific, EndeavourOS x86-64,
kernel `7.3.0-1-mainline`, direct wired `28de:1302`. Each session records USB
`bcdDevice=0404` as a device-version marker. Firmware attributes were not re-read
by each input-only reduction; do not silently carry the earlier feature session's
firmware proof into every new batch. Steam Stable `1792618285` was the reported
client; the separate SDL runs used verified source `e0232c5` / SDL 3.5.0.

Raw captures, USB addressing and absolute operator markers remain private.
`evidence/steam-d9-native-input-reference.json` indexes 274 selected, unmodified
54-byte input `0x42` packets and 17 reviewed output packets. Selection removed
USB container metadata, not payload bytes. Only known native input fields and
known `0x80`/`0x85` output layouts are published. No feature serial, unknown
feature body, account data or unknown `0x44` body is included.

## Correspondence and limits

The labelled windows corroborate the existing native digital bit mapping for
22 controls. View has two measured presses after one operator-reported miss;
other intended digital windows have three. Some touch windows have additional
contacts. Grip windows include incidental pad contact, and rear-button windows
include controller movement. These are retained as caveats, not clean negatives.

Both sticks reach `-32767/+32767`; triggers reach `0/32767` and full-trigger
click flags rise three times each. The approximate half-travel actions are
qualitative labels, not calibrated half-scale values.

| Pad | Touch-only pressure peak | Light peak | Firmer peak |
| --- | ---: | ---: | ---: |
| Left | 946 | 1236 | 31844 |
| Right | 2073 | 4193 | 15337 |

Pad samples reach approximately `+/-32766` in X/Y. Pressure is the
source-interpreted unsigned report field. Steam's input-test scale was reported
as 0–32767; this does not prove every wire endpoint or calibrated force units.
The firmer windows set the consumer-labelled pad-click bits. Do not infer a
separate mechanical switch or a universal click threshold from those bits.

## Configuration-dependent pad/stick lockout

The owner later showed Steam's per-side **Trackpad Lockout** controls, both
enabled in the displayed view. This makes exclusivity a configuration-dependent
observation, not a fixed hardware rule to hard-code in an encoder.

In the fixed-contact right-side experiment, 4470 reports with right-stick touch
asserted had right-pad touch clear and right-pad X/Y/pressure zero. Reporting
returned when stick touch cleared while the pad finger remained. This masking
is already reflected in received USB payloads. The setting-to-feature mechanism
and disabled-setting behavior were not measured. Left-pad independence was an
owner UI observation, not a simultaneously active left-pad measurement here.

The first center window includes early stick contact. Three complicated windows
in the original right-pad batch were missed and excluded; the later countdown
and fixed-contact retries are distinct. Missing haptics on a static hold is not
proof of missing raw touch. Inner-edge holds/crossings do contain raw coordinates;
no exact 10–20% dead-zone area is established. Circle contact gaps are not all
explained by stick touch and remain unclassified.

## Motion and timing

The first Steam-running motion batch kept delivering reports but its accel,
gyro and quaternion fields stayed unchanged through the six labelled actions.
It is not a working motion reference. With Steam fully closed, the helper used
SDL's normal sensor-enable API and the repeated batch produced changing raw
accel, gyro and quaternion values. A yaw slip and accidental trigger/rear-button
press were reported; this is qualitative response, not calibrated pure-axis
motion, angles or angular rates.

The primary report median completion interval is about 4001 microseconds. The
first face batch has 29720 primary reports, with all 29719 observed sequence
deltas equal to one modulo 256. Other captures include longer gaps. These are
USB completion observations, not a universal hardware polling specification or
a zero-loss certification; drop counters were not supplied to this reduction.

## Reverse output

One Steam **Ping** produced `85 05 0c 00`, completed successfully, and the owner
felt vibration plus chirping through haptics. The raw selector is 5, script 12,
signed gain 0. No separate speaker endpoint or selector-to-actuator map is proven.
No `0x44` appeared in that bounded Ping window.

The separate normal SDL rumble calls used 4096/65535 for 250 ms, one abstract
frequency channel at a time, with explicit stops. Captured output `0x80` has
seven left-speed-only frames, seven right-speed-only frames and two zero-speed
stops, all successful. The owner felt both short trials and requested no repeat.
Eighteen input `0x44` reports occurred, nine per channel window; their count does
not establish one ACK per write or their semantics. A reported short low-channel
sensation is not a measured vibration period.

No custom physical feature injection, forbidden command, firmware update,
bootloader, receiver or Bluetooth work was performed. This physical reference
does not certify virtual Steam discovery, all controller behavior or gameplay.
