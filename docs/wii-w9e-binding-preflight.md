# W9e per-device binding preflight

The owner approved a per-device hid-wiimote detach and hid-generic bind for
test and dev builds. Release use remains gated on virtualgamepad #258.
The agent applied no root operations. No global driver knob, blacklist,
persistent rule or binding-mode creation option was added.

The fresh exact-owned original Wii virtual HID on Linux
6.12.113+deb13-arm64 had wiimote bound, five input companions and no
`driver_override` sysfs attribute. The owner ran the guarded explicit
per-device unbind/bind sequence. The generic bind write failed with
`No such device`; the failure handler restored wiimote immediately.
The agent independently verified the exact identity, original driver link
and all five input companions before idempotent close. HID, hidraw and
LED nodes were verified removed. No raw data, machine identity or local
script is published.

The private producer used code e394ae6, whose runtime matches merged main
1c810c5; the additional changes are evidence text only. Both creation shims
were on, with the same caller EEPROM and imported synthetic MP and Nunchuk
blocks as W9. No native Dolphin consumer was launched. The 2503 MP+Nunchuk
arm and MP-only control are **not run**; their common host preflight is
**blocked**. The first unpassed checkpoint is generic binding, before F6.
A40020/32, A40040/16, decoded Nunchuk/gyro, and the presence or absence of
non-Dolphin A400F0=55 are **unmeasured** in W9e. The expected absence of
kernel evdev, MotionPlus and xwiimote access under hid-generic remains
**unmeasured**, since that binding was never established. Restored
wiimote companions do not establish this trade-off.

Paraphrased upstream stable v6.12.113 HID source inspections explain why
an explicit generic bind is insufficient while a special driver matches.
They are version-matched source evidence, not the Debian kernel binary
or an exhaustive audit of alternative per-device mechanisms. Neither
global ignore-special settings nor matching quirks were changed.

No adoption PR is warranted: MP+Nunchuk did not pass in this binding.
Further host mechanism or model work needs a separate owner decision.
Earlier W9 bound-kernel results remain intact; no physical, radio, rate,
game or challenge claims follow.
