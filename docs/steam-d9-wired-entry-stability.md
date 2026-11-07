# Wired Steam entry stability on D9

This study separates a Steam UI replacement from successful input-test opening.
The latter succeeded even in both failing baseline runs. All public times below
are relative to a fresh session origin. Raw captures and consumer logs remain
outside the repository.

## Comparison

| Runs | Profile | Owner observation | Raw handle reopen | Begin Test |
| --- | --- | --- | --- | --- |
| Physical A2/A3 | Retail wired, fresh Steam each | Stable list/details | None around UI path | Opened twice |
| Virtual B1/B2 | Root main `baf9d4e`, full default compatibility | Entry replaced on opening Controller list | Both runs | Opened twice |
| Virtual B3/B4 | Same profile, exact named-record reads return synthetic absent state | Both lists stable; B3 details visually unclear, B4 details stable | Neither run | Opened twice |

A1 is excluded from the clean comparison: its first UI attempt preceded USB
attachment, and System Settings later retained a raw handle after Steam exited.
Closing that consumer allowed the native nodes to return. Only Steam held the
raw descriptor in the qualifying physical runs.

The baseline virtual trace shows Steam releasing and reopening the same layered
hidraw node. Four native input children return and disappear in the gap. The
parent UHID lifecycle does not close in that interval. Both discovery entries
refer to hidraw; this does **not** establish that a reappearing evdev node itself
was the UI entry. Physical normal Steam shutdown also restores native nodes,
but neither clean physical UI transition causes this release/reopen cycle.

Every repeated AE and 83 reply is byte-identical within each baseline instance.
Measured dequeue-to-reply submission maxima are 1420 and 965 microseconds.
These measurements do not cover time queued before provider dequeue, so they
cannot exclude every timing hypothesis.

## Named-setting difference

The baseline repeatedly rejects ED requests declaring length 9 before Steam logs
a controller-info failure. Pinned replacement-firmware sources identify ED as a
named-setting read. Reanalysis of the prior physical Steam feature session gives:

| Request path | SET declared length | GET inner length | GET wire length | Content treatment |
| --- | ---: | ---: | ---: | --- |
| `user/wireless_transport` | 24 | 1 | 63 | Reviewed scalar zero; opaque tail withheld |
| `esb/bond` | 9 | 24 | 63 | Entire populated content withheld |
| `esb/bond_2` | 11 | 0 | 63 | No meaningful content; opaque tail withheld |

Every listed SET and GET completed status zero. No physical command was injected
by the agent. The physical feature session observed firmware build attribute
`0x6ACFF323`, with device-version marker `0404`; that attribute was not re-read in
every later UI-only run.

The private candidate accepts only the two exact named-record paths and returns
63 bytes: report ID 1, command ED, inner length zero, then fresh zero padding.
Both records are absent as **synthetic wired compatibility policy**. The primary
physical record was populated and is never replayed. This is no receiver,
Bluetooth, pairing-write, arbitrary-path or host-filesystem implementation.
Transport selection continues to return the previously reviewed scalar zero.

In both counterfactual runs, rejected ED requests, the controller-info failure
and raw reopen disappeared. This supports the absent-read workaround within
this client/profile scope. It does not establish a universal discovery contract.
B3 had a long idle before UI; B4 reproduced promptly with fresh Steam/instance.

## Additional bounded observations

Physical/virtual rear-button indicators correspond: L4 upper left, L5 lower
left, R4 upper right, R5 lower right. Left then right virtual grip grab/release
changed the matching fan and reverse-line indicators, consistent with the owner
physical observations. Physical left touch timing is qualified by switching to
reverse view with L4; no independent analog grip axes are established.

In Advanced Grip Sense, virtual left release caused report 81 with selector 3;
right release caused selector 4. Both used on/off 300 microseconds, count 1.
Grab-phase pulses also occurred. These are observed reverse-output requests,
not claims of a physical click felt from the virtual controller.

A separate normal demo close after creating one Steam UHID controller exited
the original process and removed the owned HID. The previously reported idle
process was not reproduced in this single bounded check.

Machine-readable projections and measurement limits:
[`steam-d9-wired-stability.json`](../evidence/steam-d9-wired-stability.json).
