# DualSense LED inventory

The DualSense has three LED functions, each with its own output field and valid bit: an RGB lightbar, five player-indicator LEDs and a microphone-mute LED. This is source evidence (community protocol documents plus Linux and SDL consumer code); nothing here is a physical observation.

Pinned sources: Linux `hid-playstation.c` at 4056b3c (`audio-linux-hid-playstation`), SDL `SDL_hidapi_ps5.c` at 535d80b (`audio-sdl-ps5`), VIIPER `docs/devices/dualsense.md` at a370903 (`ds-community-viiper-protocol`), nondebug `dualsense-explorer.html` at 0233835 (`ds-community-nondebug-explorer`). Kernel and SDL code is cited and restated, never excerpted.

## Inventory

| LED | Field (common offset) | USB 0x02 byte | BT 0x31 byte | Valid bit | Values | Claims |
| --- | --- | --- | --- | --- | --- | --- |
| RGB lightbar | `lightbar_red/green/blue` (44-46) | 45-47 | 47-49 | valid_flag1 bit 2 | 0-255 per channel | `ds-l0-led-inventory`, `ds-l0-led-common-offsets` |
| Lightbar setup | `lightbar_setup` (41) | 42 | 44 | valid_flag2 bit 1 | bit 1 = fade light out (Linux) | `ds-l0-led-lightbar-setup` |
| Player indicators | `player_leds` (43) | 44 | 46 | valid_flag1 bit 4 | bits 0-4 one LED each, bit 2 centre; bit 5 likely instant change | `ds-l0-led-player-led-bits`, `ds-l0-led-player-led-instant-bit` (inferred) |
| Mic-mute LED | `mute_button_led` (8) | 9 | 11 | valid_flag1 bit 0 | 0 off, 1 on; 2 likely pulse | `ds-l0-led-mute-led-off-on`, `ds-l0-led-mute-pulse-mode` (inferred) |
| LED brightness | `led_brightness` (42) | 43 | 45 | none identified | unknown | `ds-l0-led-led-brightness-levels` (unknown) |
| Release / reset LEDs | flag only | - | - | valid_flag1 bit 3 | consumer-defined | `ds-l0-led-valid-flags` |

Linux presents these as one multicolor `rgb:indicator` LED plus five white player LEDs, and drives the mute LED itself from the mute button (`ds-l0-led-kernel-registration`). Connect-time LED writes by Linux and SDL are in `ds-l0-led-consumer-connect-sequence`; Bluetooth framing in `ds-l0-led-bt31-offsets`.

## Sources disagree on names, not offsets

SDL calls byte 41 `ucLedAnim` and VIIPER `LightFade` where Linux says `lightbar_setup`; SDL calls valid_flag1 bit 3 "reset LED state" where Linux says "release LEDs". The offsets and bits agree in every source.

## No evidence

- Physical brightness, colour accuracy, fade timing and the controller's own startup animation.
- Values and scope of `led_brightness`. Source pending: a July 2026 Linux patch reportedly describes player-indicator brightness levels; it is not yet pinned or hashed.
- Physical left-to-right player LED order beyond the centre bit.
- The device's reaction to valid_flag1 bit 3.

## Physical LED-only check list

For an owner-approved check on a physical USB DualSense. Each step sends USB output report 0x02 with valid_flag0 = 0 (no rumble, trigger or audio changes), only the LED valid bits listed, and every other byte zero. The owner watches the controller and reports what he sees.

| Step | valid_flag1 / valid_flag2 | Field values | Confirms |
| --- | --- | --- | --- |
| L1 | flag1 0x04 | RGB 255,0,0 then 0,255,0 then 0,0,255 | Lightbar channel order (`common-offsets`) |
| L2 | flag2 0x02 | lightbar_setup 0x02 | Fade-out behaviour (`lightbar-setup`) |
| L3 | flag1 0x10 | player_leds 0x01, 0x02, 0x04, 0x08, 0x10 in turn | Physical position of each bit (`player-led-bits`) |
| L4 | flag1 0x10 | player_leds 0x04, 0x0A, 0x15, 0x1B, 0x1F | Centred patterns |
| L5 | flag1 0x10 | player_leds 0x00 then 0x1F, with and without 0x20 | Fade versus instant change (`player-led-instant-bit`) |
| L6 | flag1 0x01 | mute_button_led 0, 1, 2 | Off, solid, pulse (`mute-led-off-on`, `mute-pulse-mode`) |
| L7 | flag1 0x10 | player_leds 0x1F, led_brightness 0, 1, 2 | Whether brightness affects the player LEDs (`led-brightness-levels`) |
| L8 | flag1 0x08 | none | Reaction to release/reset LEDs |

Restore the kernel driver and its default LED state afterwards. Record no identifiers, serials or device-originated bytes.
