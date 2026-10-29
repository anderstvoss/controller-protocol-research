"""Fresh physical descriptor declarations, not gameplay or consumer acceptance."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = "steam-s3-1302-report-descriptor"
EXPERIMENT = "steam-s3-physical-descriptor"


def record(category, name):
    return json.loads((ROOT / "records" / category / (name + ".json")).read_text())


def parse_descriptor(data):
    """Read short HID items, preserving report globals and collection usage."""
    globals_ = {"page": 0, "size": 0, "count": 0, "id": 0}
    stack, usages, applications = [], [], []
    bits, pages = {}, {}
    offset, depth = 0, 0
    names = {8: "input", 9: "output", 11: "feature"}
    while offset < len(data):
        prefix = data[offset]
        offset += 1
        if prefix == 0xfe:
            raise ValueError("unexpected long item in captured descriptor")
        size = [0, 1, 2, 4][prefix & 3]
        if offset + size > len(data):
            raise ValueError("truncated HID item")
        value = int.from_bytes(data[offset:offset + size], "little")
        offset += size
        kind, tag = (prefix >> 2) & 3, prefix >> 4
        if kind == 1:
            if tag in {0, 7, 8, 9}:
                globals_[{0: "page", 7: "size", 8: "id", 9: "count"}[tag]] = value
            elif tag == 10:
                stack.append(globals_.copy())
            elif tag == 11:
                globals_ = stack.pop()
        elif kind == 2 and tag == 0:
            usages.append(value if size == 4 else (globals_["page"] << 16) | value)
        elif kind == 0:
            if tag in names:
                key = (names[tag], globals_["id"])
                bits[key] = bits.get(key, 0) + globals_["size"] * globals_["count"]
                pages.setdefault(key, set()).add(globals_["page"])
            elif tag == 10:
                if depth == 0 and value == 1:
                    applications.append(usages[-1])
                depth += 1
            elif tag == 12:
                depth -= 1
            usages.clear()
    if depth or stack:
        raise ValueError("unbalanced HID collection/global stack")
    return bits, pages, applications


class SteamS3Descriptor(unittest.TestCase):
    def setUp(self):
        self.fixture = record("fixture", FIXTURE)
        self.text = (ROOT / self.fixture["path"]).read_bytes()
        self.data = bytes.fromhex(self.text.decode())

    def test_fixture_is_unmodified_physical_bytes_with_distinct_text_and_raw_hashes(self):
        self.assertEqual(self.fixture["kind"], "physical")
        self.assertEqual(self.fixture["experiments"], [EXPERIMENT])
        self.assertIsNone(self.fixture["parent"])
        self.assertIsNone(self.fixture["transform"])
        self.assertEqual(hashlib.sha256(self.text).hexdigest(), self.fixture["sha256"])
        self.assertEqual(len(self.data), 372)
        self.assertEqual(hashlib.sha256(self.data).hexdigest(),
                         "315a037c849ef9510d222ae520bb18c1b72552d26eb116c91b0750901a5c51fd")
        self.assertNotEqual(self.fixture["sha256"], hashlib.sha256(self.data).hexdigest())

    def test_every_report_type_length_and_usage_page_matches_captured_declarations(self):
        bits, pages, applications = parse_descriptor(self.data)
        expected = {}
        for kind, reports in {
            "input": {0x40: 5, 0x41: 8, 0x42: 53, 0x43: 14, 0x44: 5,
                      0x45: 45, 0x79: 1, 0x7b: 12},
            "output": {0x80: 9, 0x81: 7, 0x82: 3, 0x83: 9, 0x84: 8,
                       0x85: 3, 0x86: 3, 0x87: 63, 0x88: 63, 0x89: 63},
            "feature": {1: 63, 2: 63},
        }.items():
            expected.update({(kind, report_id): size * 8 for report_id, size in reports.items()})
        self.assertEqual(bits, expected)
        self.assertEqual(pages, {key: {1, 9, 12} if key == ("input", 0x40)
                                else {7} if key == ("input", 0x41)
                                else {0xff00} for key in expected})
        self.assertEqual(applications, [0x00010002, 0x00010006, 0xff000001])
        self.assertNotIn(("input", 0x47), bits)

    def test_configuration_has_one_hid_interface_and_two_interrupt_endpoints(self):
        doc = (ROOT / "docs/steam-s3-physical-descriptor.md").read_text()
        data = bytes.fromhex(re.search(r"```hex\n(.*?)\n```", doc, re.S).group(1))
        self.assertEqual(len(data), 41)
        self.assertEqual(hashlib.sha256(data).hexdigest(),
                         "fabe2b688f2e7da5a123e849e9d4b112692590fbecda9ac5334e3f67beb887bc")
        self.assertEqual(data[:9], bytes([9, 2, 41, 0, 1, 1, 0, 0x80, 250]))
        items, offset = [], 9
        while offset < len(data):
            length = data[offset]
            self.assertGreaterEqual(length, 2)
            items.append(data[offset:offset + length])
            offset += length
        self.assertEqual(offset, len(data))
        self.assertEqual([d for d in items if d[1] == 4], [bytes([9, 4, 0, 0, 2, 3, 0, 0, 0])])
        self.assertEqual([d for d in items if d[1] == 0x21],
                         [bytes([9, 0x21, 0x11, 1, 0, 1, 0x22, 0x74, 1])])
        self.assertEqual([d for d in items if d[1] == 5],
                         [bytes([7, 5, 0x81, 3, 64, 0, 1]), bytes([7, 5, 1, 3, 64, 0, 1])])

    def test_claim_scope_preserves_conflict_unknown_exchange_and_no_firmware_guess(self):
        experiment = record("experiment", EXPERIMENT)
        self.assertEqual(experiment["kind"], "controlled_physical")
        self.assertEqual(experiment["status"], "passed")
        for name in self.fixture["claims"]:
            claim = record("claim", name)
            self.assertEqual(claim["applicability"]["transport"], "usb")
            self.assertIn("not supplied", claim["applicability"]["firmware"])
            self.assertEqual(claim["experiments"], [EXPERIMENT])
            self.assertNotEqual(claim["status"], "physically_validated")
        conflict = record("claim", "steam-s3-1302-sdl47-descriptor-conflict")
        self.assertEqual(conflict["status"], "conflicted")
        self.assertIn("steam-c6-input-47", conflict["conflicts_with"])
        self.assertEqual(record("claim", "steam-c6-no-wired-feature2")["status"], "unknown")
        self.assertEqual(record("claim", "steam-c6-input-47")["status"], "source_supported")
        gap = record("claim", "sc2-gap-direct-usb-descriptors")
        self.assertEqual(gap["status"], "unknown")
        self.assertIn(EXPERIMENT, gap["experiments"])
        self.assertIn("Residual unknowns", gap["statement"])


if __name__ == "__main__":
    unittest.main()
