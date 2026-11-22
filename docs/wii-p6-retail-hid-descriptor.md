# P6 retail Wii Remote Plus HID descriptor

The owner reported the case model RVL-036. Nintendo identifies that model as
Wii Remote Plus. The Bluetooth name was Nintendo RVL-CNT-01. The experiment
covers this unit and Bluetooth identity. Other revisions remain unmeasured.
[Nintendo model identification](https://en-americas-support.nintendo.com/app/answers/detail/a_id/2956/p/50/c/898)

Two BlueZ SDP queries and a Linux hidraw read with the `wiimote` driver bound
returned the same 217 bytes. Only descriptor bytes were retained. BlueZ device
removal was verified after each pairing. The raw SHA-256 is
`4d40cb52850ded69a8c1474fff35dfd3e102d4b10ad3579258ab37f4a36fb3ef`.

## Comparison

| Descriptor | Top-level application | Vendor page 0xFF00 fields | Speaker output IDs |
| --- | --- | --- | --- |
| Retail RVL-036 / RVL-CNT-01 | Generic Desktop / Game Pad | Data, Array, Absolute (0x00) | 0x14, 0x18, 0x19 |
| Current interim synthetic | Generic Desktop / Game Pad | Data, Variable, Absolute (0x02) | 0x14, 0x18, 0x19 |
| rnconrad candidate structure | Generic Desktop / Game Pad | Data, Array, Absolute (0x00) | 0x14, 0x18, 0x19 |

The rnconrad structure record's raw digest matches the retail capture exactly.
The fixture was obtained from the retail device. The historical C5 synthetic
fixture uses a vendor top-level collection and omits all three speaker outputs.

The retail and current interim descriptors agree on the following payload lengths,
excluding the report ID. The candidate digest also establishes the following table.

| Direction | Report IDs and payload lengths in bytes |
| --- | --- |
| Input | 0x20 = 6, 0x21 = 21, 0x22 = 4, 0x30 = 2, 0x31 = 5, 0x32 = 10, 0x33 = 17, 0x34–0x37 = 21 each, 0x3D–0x3F = 21 each |
| Output | 0x10 = 1, 0x11 = 1, 0x12 = 2, 0x13 = 1, 0x14 = 1, 0x15 = 1, 0x16 = 21, 0x17 = 6, 0x18 = 21, 0x19 = 1, 0x1A = 1 |
| Feature | None |

The capture establishes descriptor structure. Report framing beyond the declared
payload lengths, speaker behavior and virtual consumer acceptance require separate
evidence.

- Experiment `wii-p6-retail-hid-descriptor-run`
- Fixture `wii-p6-retail-plus-rvl-cnt-01-descriptor`
- Claims `wii-p6-retail-plus-rvl-cnt-01-descriptor-observed` and
  `wii-p6-retail-plus-rvl-cnt-01-descriptor-comparison`
