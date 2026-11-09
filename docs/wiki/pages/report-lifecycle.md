# Reading and implementing a controller protocol lifecycle

A convincing controller emulation must model more than the next input report. Not every controller uses every phase, and the phases below are an **engineering checklist**, not a universal on-wire state machine.

## 1. Discovery and ownership

Determine whether the consumer enumerates USB HID, Bluetooth HID, a vendor USB interface, or multiple receiver slots. Record interfaces, report descriptor, endpoints, permissions, drivers and how another application can take ownership. For the Puck, consult [`steam-puck-interface-selection`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-puck-interface-selection.json); for GameCube WUP-028, [`gc-adapter-consumers-require-usb-device`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-consumers-require-usb-device.json).

## 2. Initialization and feature/command exchange

Many consumers probe firmware, calibration, capabilities, device information or settings *before* treating input as usable. Responses can be mandatory, optional or version-dependent. A source read of one consumer's probe must not be made a universal requirement. Compare DualSense [`ds-l0-kernel-feature05-calibration`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-kernel-feature05-calibration.json), Switch Pro [`swpro-l0-consumer-kernel-open-order`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-consumer-kernel-open-order.json) and Wii Remote [`wii-kernel-status-ack-flow`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-kernel-status-ack-flow.json).

## 3. Input and topology

For each report, identify wire length including/excluding report ID, endian/bit order, one-control maps, analog calibration and sensor frames. Isolate state transitions (connected/disconnected, extension attached, lizard/native, Bluetooth simple/enhanced). Avoid equating axis normalization or a host's remapping with native device units.

## 4. Output and reverse feature paths

Rumble, lighting, touch/IMU enable, memory, audio and firmware metadata have independent semantics. Decode the command and return required ACKs, but do not invent physical motor transfer functions. See [`swpro-l0-device-rumble-word-tables`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-device-rumble-word-tables.json), [`ds-l0-device-usb02-valid-flags`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-device-usb02-valid-flags.json), and [`steam-d9-pcm-framing-feedback`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-d9-pcm-framing-feedback.json) for deliberately different evidentiary levels.

## 5. Lifetime, reconnect and cleanup

Check neutral before activity, reinit after consumer close, unplug/replug, slot loss, kernel-driver handoff, FIFO/ACK expiry, error path and terminal cleanup. An accepted USB descriptor alone proves none of these.

## Implementation evidence acceptance

Use separate tests for (a) byte-exact codec fixtures, (b) deterministic state machine transitions, (c) host-selected consumer behavior, and (d) controlled physical comparison. Record which gates actually ran. A fabricated synthetic fixture cannot be promoted to hardware truth; a virtual-host passed run does not establish physical parity. See [methodology](methodology.md).
