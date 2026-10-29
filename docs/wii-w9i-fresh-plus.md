# Wii W9i: fresh-device Plus ID-style comparison

Two fresh virtual Wii Remote Plus Tr MP+Nunchuk devices run native Dolphin
2503 with independent, isolated emulated ControllerInterface profiles. Neither
has a previous consumer, activation or deactivation. The owner creates both in
one 2.034604-second brief ignore-special window, restores/readbacks 0, then
verifies generic binding and grants only the two exact hidraw nodes. The agent
rechecks identity, linkage, access and holder absence. No kernel rerun is needed
under the W9i handoff; W9h already supplies that distinct regression.

Runtime is unmodified virtualgamepad main
75edae54c06ece8f90eb812d8544089a32581352, built from a Git export. Its Wii
implementation is unchanged from W9h. Synthetic imported EEPROM, MP and Nunchuk
resources, atomic stimulus, signed stick bindings, zero Real slots, gyro
calibration period 0 and re-attach/F6/copy on are identical. Only the immutable
external-style ID creation flag differs. The guard blocks foreign raw/input/
USB and Bluetooth radio attempts as an observation aid, not a complete sandbox.

| Fresh Tr arm | Native pre-map A600FE byte | Post-map MP / child frames | First unpassed checkpoint |
| --- | --- | --- | --- |
| Default built-in ID option | 00 | 4483 / 4483 | None through decoded gyro and Nunchuk stick |
| External-style ID option | 00 | 4483 / 4482 | None through decoded gyro and Nunchuk stick |

Each consumer requests A600FE/1 and receives byte 00 before its first mode 05
activation. This is a native mode-byte readback, not a full inactive-ID readback.
A4200005 and A6200005 remain the configured source identities. Each arm re-sends
0x12, successfully reads F6 and the exact imported MP 0x20/32 and Nunchuk
0x40/16 blocks, and shows changing decoded gyro and opposite Nunchuk stick
positions. Dense capture selects both stick positions before image conversion;
independent motion-view samples establish gyro change. Raw frames do not serve
as a decoded oracle. Counts exclude pre-map data and use the full 180-second
consumer bound including setup; no physical or guaranteed rate is inferred.
Native post-map A400F0=55 and A600F0=55 counts are zero in both arms.

Both fresh mode 00 arms pass, closing the W9h retained-mode-05 sampling gap for
these bounded controls. The external-style option is not required for this
native Dolphin path. No Original or retained-mode-05 pass is inherited. No
necessity control for the other compat flags is added here. The preliminary and
reused-device W9h records retain their original scope and are not rewritten.

Both consumers exit before the next arm, and both virtual devices close
idempotently with verified HID/raw removal. No physical, radio, game, release,
timing or whole-controller qualification follows. Generic binding remains
owner-managed test/dev setup with release use gated on #258. No model, codec,
API, descriptor, host-policy or dependency change. Adoption is a separate code
PR after research merges, scoped to replacing the retained-mode caveat on the
Plus rows only.
