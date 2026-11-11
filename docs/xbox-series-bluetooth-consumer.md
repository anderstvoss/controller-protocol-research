# Xbox Series Bluetooth-bus UHID: consumer-evidence gap review

**Scope:** Source-only research into the Bluetooth HID presentation of the standard Xbox Series controller, consumer driver selection, SDL HIDAPI and xpadneo. No connected controller, raw descriptor capture, Bluetooth radio or virtual-host run is available. Source examples are not device-side validation.

## Existing evidence to retain rather than duplicate

- [Corpus PR #116](https://github.com/anderstvoss/controller-protocol-research/pull/116) establishes the **wired xpad post-driver evdev** capability reference (12 keys, eight axes and memoryless force-feedback capabilities). It does not establish a Bluetooth HID descriptor.
- [Corpus PR #123](https://github.com/anderstvoss/controller-protocol-research/pull/123) records **wired USB GIP and Xbox Wireless Adapter** behavior in the out-of-tree xone consumer. Neither transport is Bluetooth HID.
- Existing records `xbox-series-sdl-bluetooth-rumble` and `xbox-series-sdl-bluetooth-report-roles` already pin SDL's Bluetooth output report 0x03 and fallback state/Guide/battery report IDs 0x01/0x02/0x04. This study will expand on descriptor-dependent dispatch and Linux arbitration, **not repeat those facts as new claims**.
- Existing device-side gap `xbox-series-bluetooth-device-gaps` remains **unknown**. A driver/parser source cannot prove firmware-specific report descriptors, pairing behavior or physical actuator effects.

## Evidence question

Can a Bluetooth-bus UHID device, with a **verified firmware-specific HID descriptor and report layout**, bind to the intended Linux and SDL consumer paths? What is the difference between a Bluetooth-bus UHID simulation and actual Bluetooth pairing/radio support?

Only the consumer contract is eligible for source-supported conclusions. Descriptor bytes and runtime acceptance require independent evidence; all proposed physical or virtual tests are **not run**.
