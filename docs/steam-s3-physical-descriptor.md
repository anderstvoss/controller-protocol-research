# S3: fresh Steam Controller 2026 direct-wired descriptor

Experiment `steam-s3-physical-descriptor`: **passed, descriptor acquisition only**.
The owner attached a physical `28de:1302` through USB passthrough to a Linux
6.12 ARM64 VM. Read-only enumeration and two byte-identical sysfs reads returned
one HID interface and a 372-byte report descriptor. No feature requests, output
writes, input stream acquisition, driver changes or consumer run occurred.
Firmware version was not supplied and is not inferred from USB device version.

Fixture: `fixtures/steam-s3-1302-report-descriptor.hex`, kind **physical**.
The existing `hid_report_hex` encoding follows the corpus's HID-descriptor
fixture convention; these are descriptor bytes, not an input report.

- Raw descriptor SHA-256:
  `315a037c849ef9510d222ae520bb18c1b72552d26eb116c91b0750901a5c51fd`
- Hex text file SHA-256 (the fixture record's digest):
  `56848c99f7eb6fd9bf3a2f10a2bff90fdc91b1f9b546f0e9189cb238c4b1c563`
- Hex rendering is reversible: no bytes replaced, omitted or synthesized.
  The descriptor contains usage/report declarations, not unit strings or serial
  data. Private binary and serial-filtered enumeration remain outside the corpus.

## USB configuration

Reduced configuration bytes (device/string descriptors excluded):

```hex
09 02 29 00 01 01 00 80 fa 09 04 00 00 02 03 00 00 00 09 21 11 01 00 01 22 74 01 07 05 81 03 40 00 01 07 05 01 03 40 00 01
```

Raw configuration length **41**, SHA-256
`fabe2b688f2e7da5a123e849e9d4b112692590fbecda9ac5334e3f67beb887bc`.
One configuration, one HID interface 0, alternate setting 0, two interrupt
endpoints: `0x81` IN and `0x01` OUT, 64-byte packets, interval 1. The embedded
HID descriptor declares report length 372. This agrees with the kernel unified
interface description. Three HID application collections are not three USB
interfaces: Generic Desktop Mouse `0001:0002`, Generic Desktop Keyboard
`0001:0006`, and vendor `ff00:0001`. Endpoint interval is not measured input rate.

## Declared reports

IDs are hexadecimal; lengths are decimal. Body excludes the report ID; wire
length adds one byte. These are **fresh physical declarations**, not observation
that every report was transmitted or that its fields/effects are understood.

| Type | ID | Body | Wire | Usage page |
| --- | --- | --- | --- | --- |
| Input | 40 | 5 | 6 | 0001 Generic Desktop; 0009 Button; 000c Consumer |
| Input | 41 | 8 | 9 | 0007 Keyboard |
| Input | 42 | 53 | 54 | ff00 vendor |
| Input | 43 | 14 | 15 | ff00 vendor |
| Input | 44 | 5 | 6 | ff00 vendor |
| Input | 45 | 45 | 46 | ff00 vendor |
| Input | 79 | 1 | 2 | ff00 vendor |
| Input | 7b | 12 | 13 | ff00 vendor |
| Output | 80 | 9 | 10 | ff00 vendor |
| Output | 81 | 7 | 8 | ff00 vendor |
| Output | 82 | 3 | 4 | ff00 vendor |
| Output | 83 | 9 | 10 | ff00 vendor |
| Output | 84 | 8 | 9 | ff00 vendor |
| Output | 85 | 3 | 4 | ff00 vendor |
| Output | 86 | 3 | 4 | ff00 vendor |
| Output | 87 | 63 | 64 | ff00 vendor |
| Output | 88 | 63 | 64 | ff00 vendor |
| Output | 89 | 63 | 64 | ff00 vendor |
| Feature | 01 | 63 | 64 | ff00 vendor |
| Feature | 02 | 63 | 64 | ff00 vendor |

## Source comparison and Judgement calls

- `steam-c6-input-42`, `steam-c6-input-45`, `steam-c6-battery-43`,
  `steam-c6-output-80-81` and `steam-c6-output-82-85` lengths all match.
  The July descriptor shape notes are corroborated. Field semantics remain
  compat consumer interpretations; no historical encoder offsets are adopted.
- **Mismatch retained as conflicted:**
  `steam-s3-1302-sdl47-descriptor-conflict` records that this descriptor has no
  input `0x47`, while SDL's source decoder accepts that alternate. This is a
  deployment mismatch, not a finding that SDL's parser claim is false. Keep
  `0x47` as a test-only diagnostic outside a realization using these bytes;
  do not silently add it to the captured descriptor. A physical transaction
  trace/firmware comparison is needed before advertising that alternate.
- **Declaration versus exchange:** feature 2 is declared. This does not
  contradict `steam-c6-no-wired-feature2`, which leaves actual wired requests
  and replies unknown. Preserve the declaration; keep the unsupported policy
  until separately authorized physical transaction evidence exists.
- `0x86` through `0x89`, `0x44`, `0x79` and `0x7b` declarations do not authorize
  streaming effects, acknowledgements, receiver behavior or automatic emission.
  Desktop pointer/keyboard declarations do not authorize lizard companions.
- The descriptor must land through owner review of this research PR before
  virtualgamepad adopts it. One interface clears the interface-count check,
  but 14a still needs the implementation/fixture-hash test after adoption.
  Step 16, 14c/14d, Steam acceptance and C6 checkpoint remain gated.

The initial capture attempt before VM attachment found no matching device and
created an empty file. Its empty-file hash is not descriptor evidence and is
not imported. Only the successful repeated physical read is represented here.
