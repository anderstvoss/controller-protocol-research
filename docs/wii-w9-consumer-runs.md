# W9 compat controls with hid-wiimote bound

The run uses code PR #256 head `ebc3a030685e476242a4d6df96e17e14862e0398`,
including the owner-approved creation switches and merged F7 policy #48.
Synthetic caller EEPROM, MP and Nunchuk blocks stay private; the extension
hashes match W8. These are compat-class virtual-host results, not physical,
calibrated-rate, challenge, game or complete-controller acceptance.

| Arm | Bound | Result / first unpassed checkpoint |
| --- | --- | --- |
| Native Dolphin 2503 MP+Nunchuk, on | 180 seconds, corrected isolated-process repeat | 14,334 F6/4 reads return error 7 after non-Dolphin reinitialization; MP 20/32 and child 40/16 not reached |
| Native Dolphin 2503 MP+Nunchuk, off | 180 seconds | 14,659 F6/4 error 7 replies; same unreached calibration checkpoints |
| Native Dolphin 2503 MP-only, on | 150 seconds | Exact MP block in two successful chunks; mapping view shows changing gyro, accel and two basic IR points |
| Kernel evdev MP-only, on | 12 seconds, fresh device | ABS_RX/RY/RZ each change between two driven values; earlier reused-device preflight blocked before evtest because MP node had disappeared |

Dolphin uses Debian ARM64 `2503+dfsg-1+deb13u1`, an isolated profile per arm,
explicit bindings, UI gyro calibration period zero, emulated mapping slot 1,
no Real slots or content, and a process-only owned-I/O/radio guard. No holder
is opened by the runner during Dolphin; companion-holder preflights are empty.
Two owned devices coexist, but each consumer can open only its named raw node;
refusals for the other owned node are intentional guard effects. Native source
at tag 2503 matches the existing `wii-w8-dolphin-2503-input` hash.

## Setup and P3 attribution

Both MP+Nunchuk captures show Dolphin mapping mode 05, then combined A400F0=55
followed by inactive-bank probing. In each arm, native Dolphin makes zero
A400F0 writes after its first map, while the combined reverse stream contains
one. Native raw writes are directly attributed to Dolphin. The other output is
non-Dolphin within the capture, consistent with the bound driver. Identical
requests cannot be paired uniquely by payload alone; no kernel stack trace or
universal single-cause conclusion is claimed. Combined counts start at the
producer phase, before the consumer launch, and preserve that scope.

These observations leave the shim's active-state predicate unavailable at the
repeated F6 requests. They do not demonstrate that the live F6 mirror or child
copy succeeded. Do not widen the model state gate, alias 20/40 or unbind a driver
to force progress. The first unpassed consumer checkpoint remains F6 under
shared-kernel setup contention, not a missing imported MP or child block.
The source-pinned initial A400FE/512 usability diagnostic can return error 7
before normal setup; it is not the attach/calibration failure checkpoint.

The off mapping view shows changing accel and basic IR but no established
Nunchuk/gyro decode. The corrected on comparison has no mapping-view sample;
its excluded pilot UI is not promoted. MP-only has a separate inspected UI
oracle with changing gyro, accel and IR; raw transport alone remains labelled
not decoded. No continuous delivery or accurate rates are inferred. Cemu gyro
is excluded; wiiuse/CWiid remain source references, not runtime failures.

## Controls and cleanup limits

The first on pilot coordinator exited 143 at its timeout. Exact-profile
consumers were verified absent, but the pilot is excluded from the clean
comparison. The corrected 180-second repeat puts Dolphin in a separate process
group and records orderly cleanup before the off arm and positive control.

The first kernel preflight on the reused post-Dolphin device found only core,
accelerometer and IR nodes, so evtest never launched. Preserve that boundary.
A fresh MP-only producer, with its initial topology retained during phase
selection, exposed the MotionPlus node and passed the 12-second control.
This proves fresh-device delivery, not post-Dolphin companion recovery.

Human grants were supplied locally and confirmed, then exact identity/access
was rechecked. All owned consumer children closed between arms. All three
producers closed idempotently and their HID, raw and four LED nodes were
verified gone. Raw logs, bytes, screenshots, paths, identities and wall clocks
stay private. No persistent host change, rebinding, radio or content was used.
