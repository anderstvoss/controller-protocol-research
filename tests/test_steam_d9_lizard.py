"""Reviewed desktop packet shapes and the physical mode-write selection."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LizardPhysicalFixtureTests(unittest.TestCase):
    def test_whole_desktop_packets_have_only_known_descriptor_fields(self):
        packets = [bytes.fromhex(line) for line in
                   (ROOT / 'fixtures/steam-d9-lizard-desktop.hex').read_text().splitlines()]
        self.assertEqual(len(packets), len(set(packets)))
        for packet in packets:
            self.assertIn((packet[0], len(packet)), [(0x40, 6), (0x41, 9)])
            if packet[0] == 0x40:
                self.assertEqual(packet[1] & ~3, 0)
            else:
                self.assertEqual(packet[2], 0)
                self.assertTrue(all(usage <= 101 for usage in packet[3:]))
        for usage in [0x28, 0x29, 0x2b, 0x52, 0x51, 0x50, 0x4f]:
            self.assertIn(bytes([0x41, 0, 0, usage, 0, 0, 0, 0, 0]), packets)
        self.assertIn(bytes([0x41] + [0] * 8), packets)
        for buttons in [0, 1, 2]:
            self.assertIn(bytes([0x40, buttons, 0, 0, 0, 0]), packets)

    def test_mode_writes_are_complete_numbered_known_commands(self):
        packets = [bytes.fromhex(line) for line in
                   (ROOT / 'fixtures/steam-d9-lizard-mode-writes.hex').read_text().splitlines()]
        self.assertEqual({p[1] for p in packets}, {0x85, 0x8e, 0x87})
        for packet in packets:
            self.assertEqual(len(packet), 64)
            self.assertEqual(packet[0], 1)
            if packet[1] == 0x87:
                self.assertEqual(packet[2:6], bytes([3, 9, 0, 0]))
                self.assertFalse(any(packet[6:]))
            else:
                self.assertFalse(any(packet[2:]))
