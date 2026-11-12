# GameCube USB adapter — descriptor and status-bit gap review (round 2)

Source-only research for `gamecube-usb-adapter`, tracking `anderstvoss/virtualgamepad#296`. No physical hardware or host testing.

## Ranked gaps and evidence ceiling

| Rank | Gap | Playable or faithful? | Evidence ceiling | Related existing record / issue |
| --- | --- | --- | --- | --- |
| 1 | Configuration, interface and endpoint descriptors | Faithful | Work in progress | `gc-adapter-descriptors-unknown`; #296 |
| 2 | Interrupt `bInterval`, HID and string descriptors | Faithful | Work in progress | `gc-adapter-descriptor-details-unconfirmed`; #296 |
| 3 | Per-port status bits beyond identified fields | Faithful | Work in progress | `gc-adapter-remaining-status-unknown`; #296 |

## Source review

Work in progress.

## Consumer expectation versus device statement

Work in progress.

## Proposed tests (not run)

Work in progress.
