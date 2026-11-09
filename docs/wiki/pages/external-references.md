# External reference shelf (not yet corpus-reviewed)

These sources supplement the technical context and may guide **future evidence additions**. Their current webpages are not being treated as pinned, hashed corpus source records; they do not justify changing existing claim statuses.

| Source | Useful for | Boundary |
| --- | --- | --- |
| [SDL3 HIDAPI configuration](https://wiki.libsdl.org/SDL3/SDL_HINT_JOYSTICK_HIDAPI) | Driver enablement and selection controls | Configuration documentation, not a measured consumer run |
| [SDL3 enhanced-report policy](https://wiki.libsdl.org/SDL3/SDL_HINT_JOYSTICK_ENHANCED_REPORTS) | Distinguishing optional sensor / output modes | Version-dependent consumer policy |
| [SDL3 PS5 HIDAPI hint](https://wiki.libsdl.org/SDL3/SDL_HINT_JOYSTICK_HIDAPI_PS5) | Sony backend selection | Not physical DualSense behavior |
| [Linux current hid-nintendo source](https://github.com/torvalds/linux/blob/master/drivers/hid/hid-nintendo.c) | Identify post-pin changes to Switch 1/2 support | Moving `master`; use a **pinned commit** before adding a corpus claim |
| [ndeadly Switch 2 research](https://github.com/ndeadly/switch2_controller_research) | Public BLE, command, memory and HID research leads | Community documentation; firmware/revision and independent corroboration require review |
| [MkDocs](https://www.mkdocs.org/) and [Material](https://squidfunk.github.io/mkdocs-material/) | Reader navigation, search and static hosting | Presentation only; no protocol evidence |

The corpus itself already contains many **pinned external sources**, including kernel, SDL, Dolphin, OpenPuck, HHD and other researchers. Follow the exact `sources` IDs in individual claim JSON. This shelf does **not** duplicate those records or assert they have been re-reviewed.

To incorporate a new external finding, first register a source with URL, immutable revision, SHA-256, lineage and locator; add a claim of appropriate role/status and run corpus validation. Only then cite the new claim in the next wiki snapshot.
