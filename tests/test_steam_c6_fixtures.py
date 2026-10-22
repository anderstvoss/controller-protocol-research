"""Synthetic Steam Controller 2026 wired host-consumer frames, not captures."""
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "steam-c6-"
LENGTHS = {
    "neutral-42": 54,
    "neutral-45": 46,
    "neutral-47": 46,
    "buttons-all-42": 54,
    "stick-trigger-max-42": 54,
    "stick-trigger-min-42": 54,
    "touch-corners-pressure-42": 54,
    "imu-extremes-42": 54,
    "full-edge-45": 46,
    "timestamp-touch-47": 46,
    "battery-43": 15,
    "output-rumble-80": 10,
    "output-pulse-81": 8,
    "output-command-82": 4,
    "output-lfo-83": 10,
    "output-sweep-84": 9,
    "output-script-85": 4,
    "feature-serial-get": 64,
    "feature-attrs-get": 64,
    "feature-lizard-enable-map": 64,
    "feature-lizard-enable-defaults": 64,
    "feature-lizard-disable-clear": 64,
    "feature-lizard-disable-kernel": 64,
    "feature-lizard-disable-sdl": 64,
    "feature-imu-on": 64,
    "feature-imu-off": 64,
    "reply-serial-empty": 64,
    "reply-attributes-empty": 64,
    "reply-attributes-short": 3,
}
OUTPUT_IDS = {
    "output-rumble-80": 0x80, "output-pulse-81": 0x81,
    "output-command-82": 0x82, "output-lfo-83": 0x83,
    "output-sweep-84": 0x84, "output-script-85": 0x85,
}
COMMANDS = {
    "feature-serial-get": [1, 0xAE, 0x15, 1],
    "feature-attrs-get": [1, 0x83, 0],
    "feature-lizard-enable-map": [1, 0x85],
    "feature-lizard-enable-defaults": [1, 0x8E],
    "feature-lizard-disable-clear": [1, 0x81],
    "feature-lizard-disable-kernel": [1, 0x87, 6, 9, 0, 0, 71, 0, 0],
    "feature-lizard-disable-sdl": [1, 0x87, 3, 9, 0, 0],
    "feature-imu-on": [1, 0x87, 3, 48, 24, 0],
    "feature-imu-off": [1, 0x87, 3, 48, 0, 0],
}


def fixture(name):
    record = json.loads((ROOT / "records/fixture" / (PREFIX + name + ".json")).read_text())
    data = (ROOT / record["path"]).read_bytes()
    return record, data, bytes.fromhex(data.decode())


def read_claim(name):
    return json.loads((ROOT / "records/claim" / (PREFIX + name + ".json")).read_text())


class SteamC6Fixtures(unittest.TestCase):
    def test_exhaustive_inventory_lengths_hashes_and_provenance(self):
        actual = {
            p.stem[len(PREFIX):]
            for p in (ROOT / "records/fixture").glob(PREFIX + "*.json")
        }
        self.assertEqual(actual, set(LENGTHS))
        for name, length in LENGTHS.items():
            rec, data, packet = fixture(name)
            self.assertEqual(rec["id"], PREFIX + name)
            self.assertEqual(rec["path"], "fixtures/" + PREFIX + name + ".hex")
            self.assertEqual(rec["format"], "hid_report_hex")
            self.assertEqual(rec["kind"], "synthetic")
            self.assertIsNone(rec["parent"])
            self.assertIsNone(rec["transform"])
            self.assertEqual(rec["experiments"], [])
            self.assertEqual(hashlib.sha256(data).hexdigest(), rec["sha256"])
            self.assertEqual(len(packet), length, name)
            self.assertTrue(rec["sources"])
            self.assertTrue(rec["claims"])
            for claim_id in rec["claims"]:
                claim = json.loads((ROOT / "records/claim" / (claim_id + ".json")).read_text())
                self.assertEqual(claim["applicability"]["controller"], "steam-controller-2026")
                self.assertEqual(claim["applicability"]["transport"], "source_only")
                self.assertEqual(claim["experiments"], [])

    def test_report_ids_and_shared_prefix(self):
        for name, report_id in {
            "neutral-42": 0x42, "neutral-45": 0x45,
            "neutral-47": 0x47, "battery-43": 0x43,
        }.items():
            self.assertEqual(fixture(name)[2][0], report_id)
        input_42 = fixture("neutral-42")[2]
        input_45 = fixture("neutral-45")[2]
        self.assertEqual(input_42[1:46], input_45[1:46])
        self.assertEqual(input_42[46:], bytes(8))
        self.assertEqual(fixture("buttons-all-42")[2][2:6], bytes([255, 255, 255, 63]))
        for name, report_id in OUTPUT_IDS.items():
            self.assertEqual(fixture(name)[2][0], report_id)

    def test_extremes_and_timestamps(self):
        max_frame = fixture("stick-trigger-max-42")[2]
        min_frame = fixture("stick-trigger-min-42")[2]
        for pos in [6, 8, 10, 12, 14, 16]:
            self.assertEqual(int.from_bytes(max_frame[pos:pos + 2], "little", signed=True), 32767)
            self.assertEqual(int.from_bytes(min_frame[pos:pos + 2], "little", signed=True), -32768)
        pressure = fixture("touch-corners-pressure-42")[2]
        self.assertEqual(pressure[4] & 0x20, 0x20)
        self.assertEqual(pressure[5] & 0x02, 0x02)
        self.assertEqual(int.from_bytes(pressure[22:24], "little"), 65535)
        self.assertEqual(int.from_bytes(pressure[28:30], "little"), 65535)
        imu = fixture("imu-extremes-42")[2]
        self.assertEqual(imu[30:34], bytes([255] * 4))
        for i in range(34, 54, 2):
            self.assertIn(int.from_bytes(imu[i:i + 2], "little", signed=True), {-32768, 32767})
        timed = fixture("timestamp-touch-47")[2]
        self.assertEqual(timed[18:20], b"\\xff\\xff")
        self.assertEqual(timed[32:34], b"\\xff\\xff")

    def test_consumer_sent_settings_and_structural_replies(self):
        for name, head in COMMANDS.items():
            packet = fixture(name)[2]
            self.assertEqual(packet[:len(head)], bytes(head))
            self.assertEqual(packet[len(head):], bytes(64 - len(head)))
        self.assertEqual(fixture("reply-serial-empty")[2][:4], bytes([1, 0xAE, 1, 1]))
        self.assertEqual(fixture("reply-attributes-empty")[2][:5], bytes([1, 0x83, 2, 0, 0]))
        self.assertEqual(fixture("reply-attributes-short")[2], bytes([1, 0x83, 1]))
        self.assertFalse((ROOT / "fixtures/steam-c6-feature2-wired.hex").exists())

    def test_no_physical_promotion_or_invented_replies(self):
        for path in (ROOT / "records/claim").glob(PREFIX + "*.json"):
            rec = json.loads(path.read_text())
            self.assertIn(rec["status"], {"source_supported", "conflicted", "unknown"})
            self.assertEqual(rec["applicability"]["transport"], "source_only")
            self.assertEqual(rec["applicability"]["controller"], "steam-controller-2026")
            self.assertFalse(rec["experiments"])
            self.assertNotIn(rec["status"], {"physically_observed", "physically_validated"})
        self.assertEqual(read_claim("no-wired-feature2")["status"], "unknown")
        self.assertEqual(read_claim("no-haptic-ack")["status"], "unknown")


if __name__ == "__main__":
    unittest.main()
