# Xbox Series — scoped physical and virtual Linux observations

[← Xbox Series overview](index.md) · [Wired GIP/xone](wired-gip-and-receiver.md) · [Bluetooth/xpadneo](bluetooth-and-xpadneo.md)

> **2026-11-11 research, corpus e8cca52c51f7.** One physical controller was used as a **transport- and driver-specific reference**, not a universal Xbox Series specification. Device model designation and installed firmware were not confirmed. Physical, consumer and scratch-virtual observations below are separated.

## Physical wired USB with stock xpad

| Surface | Observed, scoped to Linux 7.3 / reference | Remaining limit |
| --- | --- | --- |
| Device/interface | `045e:0b12`, `bcdDevice 5.17`; three vendor-specific USB interfaces; interface 0 bound to stock `xpad` | Does not provide a complete native GIP packet/ACK transcript |
| Post-driver controls | 12 keys and 8 absolute axes match the C9 evdev capabilities; `BTN_MODE` Guide, `KEY_RECORD` Share, full sticks, triggers **0–1023**, D-pad directions/center | Stick fuzz 16 on physical xpad versus 0 in C9 uinput; observed released sticks were not necessarily exactly zero |
| Sweep/reconnect | 799 completed input frames in the controlled sweep and 22 after reconnect; no dropped frames; input node disappeared on unplug and was replaced on replug | A first user-level evtest open failed on active-seat ACL timing; a retry succeeded |
| Main rumble | Two distinct `FF_RUMBLE` uploads played/stopped/erased and produced perceived pulses | No independently measured trigger motors or raw GIP output bytes |
| Guide LED | No evdev `EV_LED` or associated LED-class node under stock xpad | Raw LED command not tested due to permissions |

The physical evdev input/reconnect observation is [`xsphys-xpad-input`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/xsphys-xpad-input.json); operator details and bounded rumble are in [wired reference ledger](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/docs/ledgers/xbox-series-wired-physical.md), with sanitized [sweep](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/fixtures/xsphys-xpad-sweep.json) and [reconnect](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/fixtures/xsphys-xpad-reconnect.json) fixtures. This **physically validates the scoped post-driver input shape**, not generic native USB fidelity.

## Real headset with two different Linux consumers

Stock `xpad` exposed no associated ALSA sound device when a 3.5-mm headset was plugged in; this tests the **stock driver configuration**, not headset impossibility. With xone 0.5.8 and the requisite gamepad/headset modules loaded, the same wired reference exposed an ALSA headset: 48-kHz S16_LE stereo playback and 24-kHz mono capture. The operator heard left/right markers and captured 120,000 microphone frames in a five-second concurrently drained repeat, without a reported xrun. The initial capture had overrun due to delayed draining. This is **bounded physical duplex support**, not sustained-use or PipeWire-routing validation. [Physical xpad and xone headset session](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/docs/ledgers/xbox-series-wired-physical.md); [`xsphys-xone-headset`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/experiment/xsphys-xone-headset.json).

## Physical Bluetooth descriptor and scratch UHID

The reference paired through BlueZ as **`045e:0b13`**, bound to kernel `microsoft`. Its captured **283-byte HID report descriptor** matches the pinned published Series example byte for byte. The map declares a numbered 17-byte input `0x01` and 9-byte output `0x03` (both lengths including IDs); it declares no separate battery or Guide report. This is a **device-side descriptor observation**, not a raw HID input capture or universal firmware assertion. [`xsphys-bt-descriptor-match`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/xsphys-bt-descriptor-match.json), [Bluetooth reference ledger](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/docs/ledgers/xbox-series-bt-reference.md), [`xsphys-bt-descriptor-read`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/experiment/xsphys-bt-descriptor-read.json).

A separate **scratch virtual** Bluetooth-bus UHID used that descriptor and synthetic path. Kernel `microsoft` bound; SDL 3.4.18 with HIDAPI disabled opened an evdev node, observed input press/release and axes, and sent main-rumble output `03 03 00 00 19 32 ff 00 ff` and a zero-magnitude stop. The UHID was destroyed cleanly. The virtual hidraw ACL prevented direct HIDAPI qualification; GET/SET report exchanges and radio pairing were **not** demonstrated. [`xsphys-bt-uhid-sdl`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/experiment/xsphys-bt-uhid-sdl.json).

## Physical Bluetooth with xpadneo

On a later xpadneo v0.10.5 connection the parent stayed `045e:0b13`, while the child gamepad advertised rewritten product `028e`. A 360-frame input sweep had no dropped frames; SDL with HIDAPI disabled saw six axes and 15 standard buttons and accepted main rumble. Separate keyboard/mouse/consumer-control nodes were present, but their ACLs prevented testing Share, so this **does not physically validate F12 Share behavior**. Welcome rumble was felt; trigger motors were not individually isolated. [Bluetooth and xpadneo ledger](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/docs/ledgers/xbox-series-bt-reference.md).

## Outstanding device and consumer gaps

Raw wired GIP and physical Bluetooth input reports, per-firmware variants, exact Guide/battery delivery outside this HID map, independent trigger actuation, Steam Input, true wireless emulation, long-duration headset behavior and receiver pairing are not closed by this work. The prior source-only claims remain valid **within their stated original scopes**, while the new physical descriptor and xpad claims add narrower validated observations.
