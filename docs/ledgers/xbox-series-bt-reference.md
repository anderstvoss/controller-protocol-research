# Xbox Series Bluetooth report map and local UHID experiment

The physical reference paired with Linux
7.3.0-1-mainline via BlueZ as Xbox Wireless Controller, bus 5, VID:PID
`045e:0b13`. The Linux HID driver was `microsoft`. Evdev version was
`0x0523`. The model label and installed firmware remain unconfirmed.

The [captured HID report map](../../fixtures/xsphys-bt-descriptor.hex)
is 283 bytes and matches the published xpadneo descriptor byte for byte.
The digest of the decoded bytes is
`a681e2cb8b5d9466f258e2f07f0fcc518ec438231af1b61b125c213d2c62e165`.
The capture contains the report descriptor only. Raw report reads were denied
by the hidraw ACL. This map declares a 17-byte numbered input report `0x01`
and a nine-byte numbered force-feedback output report `0x03` including their
IDs. It declares neither a battery nor a separate Guide report. Guide is
represented within the primary input report in the qualified Linux mapping.
[xpadneo descriptor](https://github.com/atar-axis/xpadneo/blob/master/docs/descriptors/xbxs.md)

A scratch UHID device reproduced the descriptor and Bluetooth bus identity
with a synthetic physical path. The kernel bound it to `microsoft`.
SDL 3.4.18 (`g829a65d76`) opened exactly one associated evdev node with
`SDL_JOYSTICK_HIDAPI=0`. It saw press and release masks `0xffff`, axis mask
`0x3f`, Share as `misc1`, Guide separately, and final neutral. SDL closed,
reopened, and closed the device. UHID observed main rumble report
`03 03 00 00 19 32 ff 00 ff` and a zero-magnitude stop with the same mask.
Explicit UHID destruction removed the owned HID device. Physical and virtual
devices coexisted during the test. The virtual hidraw ACL prevented direct
HIDAPI qualification.

The scratch run saw START, OPEN, and unacknowledged OUTPUT messages. It did
not observe GET_REPORT or SET_REPORT. Production tests need exact replies
and lifecycle coverage even for requests a given consumer does not send.
Raw physical reports, battery behavior outside this map, independent trigger
actuation, Steam Input and virtual radio pairing remain unqualified.

## xpadneo v0.10.5 alternative consumer

A later physical Bluetooth connection bound the reference to xpadneo
v0.10.5. Its gamepad input ID used product `028e` and version `1130`,
while the parent Bluetooth HID remained `045e:0b13`. The sweep observed
all 11 gamepad buttons, all stick axes, both triggers and eight D-pad
directions plus center. The capture contained 360 completed frames and zero
dropped frames. SDL 3.4.18 opened the exact event path with HIDAPI disabled,
reported six axes and 15 standard buttons, and accepted main rumble.

The operator felt welcome rumble and thought it included trigger pulses.
Kernel diagnostics reported weak, strong and trigger motor welcome stages.
Individual left/right trigger actuation remains unqualified. Share was
absent from the SDL gamepad mapping. Keyboard, mouse and consumer-control
interfaces were split out by the driver, and this caller lacked read access
to them, so Share remained unverified.

## Relation to source research

The descriptor is device evidence for this unit and physically corroborates
`xbox-cgap-descriptor-example` from research #124. Driver binding,
split input interfaces, product rewriting, SDL mapping and reverse rumble
are consumer observations. The independent source records stay
source-supported. This session does not establish a universal descriptor
for all Series firmware.

The fixture passed `tools/sanitize.py review-descriptor`. Manual byte
review found only the standard HID descriptor items shown by the published
example, with no device strings, addresses or pairing material. Raw
captures and PCM remain outside the corpus.
