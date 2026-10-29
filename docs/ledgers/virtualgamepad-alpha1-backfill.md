# Alpha-1 virtualgamepad historical evidence backfill (Package B)

This ledger cites **maintainer-authored documents**, not newly executed experiments, physical captures or native controller acceptance. Sources are pinned to virtualgamepad main `c60c16409e91e39ddba56a78475bdabe3780d1d0` (except the historical `dummy_hcd` POC, pinned to archived `a5310c6`). The preexisting source `audio-vg-exp0023` is retained and not duplicated. No `wip/btvirt` evidence is used.

## Historical run records

| Document | Records | Outcome | Boundary |
| --- | --- | --- | --- |
| EXP-0006 | `ds-vg-exp0006-uhid-host-run` | passed | Corrected USB/UHID startup selector, three runs; prior test selector false failures excluded |
| EXP-0007 | `ds-vg-exp0007-bus-compare-host-run` | passed | Four conditions × 3 repetitions; USB/playstation vs virtual/hid-generic |
| EXP-0008 | `ds-vg-exp0008-sdl-host-run` | passed | DualSense baseline/rewrite SDL 3.2.0, strong neutral follow-up |
| EXP-0009 | `ds4-vg-exp0009-uhid-sdl-host-run`, `swpro-vg-exp0009-uhid-sdl-host-run`, `x360-vg-exp0009-uhid-sdl-host-run` | passed | Three runs per family after Xbox encoder correction |
| EXP-0010 | `vg-alpha1-exp0010-ff-host-run` | passed | Four-family conventional FF, cleanup and killed-consumer condition |
| EXP-0011 | Three passing evdev family runs, `ds4-vg-exp0011-evdev-discovery-host-run`, and `vg-alpha1-exp0011-uhid-recheck-host-run` | 4 passed, 1 failed | DS4 combined-node touchscreen classification failure retained; other families and UHID rechecks distinct |
| EXP-0012 | `ds4-vg-exp0012-compound-host-run` | **blocked** | One ten-second observation then interrupted by reported display crash; cannot attribute cause or call split touch accepted |
| EXP-0014 | `swpro-vg-exp0014-evdev-individual-host-run`, `x360-vg-exp0014-evdev-individual-host-run` | passed | 156 exact observations each; rebuilt-probe and pre-ready calibration attempts excluded |
| EXP-0015 | One `ds-vg-exp0015-physical-usb-hid` source-supported claim; **no corpus physical experiment** | source-backed | Physical 054c:0ce6 GETs and passive reports; raw contents private, damaged controls, not physical validation |
| EXP-0016 | `x360-vg-exp0016-uhid-individual-host-run` and reported Steam/Eden consumer discrepancies | passed host run; manual reports not experiments | Exact consumer builds and mappings absent, corrected Xbox SDL control matrix not Eden/Steam replay |
| EXP-0017 | `vg-alpha1-exp0017-uhid-individual-host-run` | passed | Four-family 156 exact isolated observations each; early Sony D-pad runs invalidated by readiness |
| Archived dummy_hcd POC | `ds-vg-dummy-hcd-steam-host-run` | passed as *historical reported* | Same-host virtual USB Steam gyro, Steam version unknown; not physical USB fidelity |
| EXP-0021 | Pinned document only | no live controller experiment | Gate T deterministic tests and unknown physical exposure; no new virtual run claimed |

Each historical `virtual_host_run` record reproduces the source document's passed/failed/blocked conclusion and limits. There are **16 passed, 1 failed, 1 blocked**; no new physical fixture or raw machine capture is imported.

## Evidence roles and acceptance boundaries

- Thirty source-supported `consumer` claims summarize virtual-host SDL, evdev, Steam/Eden and dummy_hcd observations. A report of a consumer API succeeding is not proof that a physical device would decode or actuate it.
- `ds-vg-exp0015-physical-usb-hid` is the one `device` claim, remaining `source_supported` and explicitly scoped **maintainer-reported physical observation, not corpus physical validation**. The original privately retained descriptor, pairing data and calibration values are not uploaded.
- Switch Pro and Xbox standard HID remain distinct: no measured Switch Pro compressed-rumble fidelity, and the Xbox virtual profile is not proprietary XInput/xpad or a physical Xbox 360.
- DS4's historical combined-node failure and interrupted split-node attempt do not establish the current production state. Touch-consumer association still needs isolated validation.
- User-reported Steam/Eden axes and neutral mismatches have no exact consumer build/backend/mapping provenance. Preserve disagreement without assuming a firmware/protocol defect.
- Historical observed kernel 6.12.105/107 and SDL 3.2.0 are not contemporary performance guarantees or blanket parity conclusions.
- Code implementation, controller descriptors and source-level host decode are outside Package B and belong in the L0 source ledgers (C–F) and later citation maps.
