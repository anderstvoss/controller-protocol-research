# Transports, host layers and virtual-device realization

A controller identity is not a protocol. An application may observe an **evdev** mapping, SDL HIDAPI gamepad, Steam Input presentation or HID feature exchange depending on driver ownership and the device's bus/interface topology. Those consumers need not agree, and the same physical device can present multiple nodes.

## Model the full path

1. **Physical transport and descriptor:** USB device/configuration/interface/endpoint topology, or Bluetooth discovery and HID transport. A wireless receiver may route several controllers through one composite USB device.
2. **Kernel driver:** generic HID/hid-input, a specialized HID driver, a vendor USB driver (for example `xpad`), or userspace libusb may claim the interface.
3. **Consumer API:** `/dev/input/event*`, `/dev/hidraw*`, SDL HIDAPI/evdev, direct libusb, Steam Input or Dolphin. Permission to read evdev alone does not imply permission to open hidraw or USB device nodes.
4. **Application behavior:** mapping and detection, gyro/touch, output/feature requests, ownership and coexistence.

Compare [`steam-puck-interface-selection`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-puck-interface-selection.json) (SDL requires receiver interfaces 2–5), [`x360-l0-device-xusb-nonhid-interface`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-device-xusb-nonhid-interface.json) (native Xbox wired is not generic HID) and [`gc-adapter-consumers-require-usb-device`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-consumers-require-usb-device.json) (GameCube adapter direct USB consumers).

## Virtualization strategies

| Surface | Appropriate use | Insufficiency |
| --- | --- | --- |
| `uinput` | Virtual evdev key/axis/FF nodes and application mapping experiments | Does not create physical USB/HID descriptors or native feature exchanges |
| `UHID` | Kernel-handled virtual HID reports and features | Does not necessarily reproduce USB composite interfaces, `interface_number` or radio pairing |
| `dummy_hcd` / USB gadget | Virtual **USB device** with configuration/interface/endpoint ancestry | Requires a correct descriptor and protocol implementation; USB appearance is not automatically physical fidelity |
| Bluetooth HID emulation | Actual advertising/pairing/HIDP/GATT path if implemented and tested | `BUS_BLUETOOTH` metadata on UHID alone is not discoverable Bluetooth |

The differences are material to Sony Steam gyro ([`ds-l0-dummy-hcd-steam-gyro-contrast`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-dummy-hcd-steam-gyro-contrast.json)), Puck slot discovery ([`steam-puck-interface-selection`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-puck-interface-selection.json)) and Xbox 360 native-vs-standard HID ([`x360-l0-consumer-exp0016-hid-usage-correction`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-consumer-exp0016-hid-usage-correction.json)).

## SDL and other consumers

SDL often has **separate** HIDAPI and evdev code paths. A GUID or name matching one controller family does not show that a specific native decoder handled the input. Treat startup, report modes, mapping, sensor availability and output support as independent observations. The [SDL3 HIDAPI hint](https://wiki.libsdl.org/SDL3/SDL_HINT_JOYSTICK_HIDAPI) and [enhanced-report hint](https://wiki.libsdl.org/SDL3/SDL_HINT_JOYSTICK_ENHANCED_REPORTS) document current configuration; these are **supplementary public references**, not evidence that a corpus host test used them.

## Consumer acceptance checklist

Document the exact kernel, SDL and application builds; bus, driver and interface; HIDAPI versus evdev selection; exposed input/hidraw/audio nodes; neutral/one-control-at-a-time semantics; bidirectional reports; reopen/close ordering; and cleanup. For compound devices, verify that auxiliary nodes cannot persist after the controller is gone. See [realized-controller-permissions.md](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/realized-controller-permissions.md) and [virtualgamepad-alpha1-backfill.md](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/ledgers/virtualgamepad-alpha1-backfill.md).

## Additional source-backed consumer contrasts (November 10)

[Steam Controller BLE HOGP](controllers/steam-controller-2026/bluetooth-and-uhid.md) may be locally presented as Bluetooth-bus UHID by BlueZ, but GATT Report-characteristic exchange, MTU and real pairing are separate properties. [Xbox Series Bluetooth/xpadneo](controllers/xbox-series/bluetooth-and-xpadneo.md) can expose a keyboard for Share (F12), a Guide modifier and separate synthetic evdev children; those are not stock wired xpad's shape. [Xbox Series GIP](controllers/xbox-series/wired-gip-and-receiver.md) uses vendor USB/receiver clients and can expose conditional headset PCM through xone.

**Audio is another host discovery chain:** ALSA, udev, PipeWire and WirePlumber enumerate sound cards independently of a UHID joystick. No pinned source or runtime test demonstrates automatic Steam/Proton pairing of unrelated sound and controller nodes. See [HID and audio association](audio-association.md) and [`audio-consumer-sidecar-hid-sound-association-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ce6b8d3b70fd0957135eb921ef6098988f355cb1/records/claim/audio-consumer-sidecar-hid-sound-association-unknown.json).

## November 11: consumer-versus-device evidence in practice

The [Xbox Series observations](controllers/xbox-series/physical-observations.md) illustrate three non-equivalent results: a **physical** Bluetooth report descriptor (device evidence), **physical** USB xpad evdev mapping and xone headset output (consumer observations), and a **scratch UHID** accepted by kernel/SDL without actual wireless pairing. The [virtual Steam kernel run](controllers/steam-controller-2026/virtual-kernel-evdev.md) likewise exercises host decoding and mode-gating but not retail hardware. The [Puck](controllers/steam-controller-2026-puck/receiver-lifecycle.md) and [Joy-Con Left](controllers/switch-joycon-left/source-and-consumers.md) chapters add only source-derived host protocol expectations. These levels should remain separate even when the reported buttons and axes look identical. [`xsphys-bt-descriptor-match`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/xsphys-bt-descriptor-match.json), [`xsphys-xpad-input`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/xsphys-xpad-input.json), [`steam-d9-virtual-kernel-mode-gate`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/steam-d9-virtual-kernel-mode-gate.json).
