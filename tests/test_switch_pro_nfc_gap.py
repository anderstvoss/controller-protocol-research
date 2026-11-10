import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIM_ID = "swpro-cgap-nfc-mcu-family-context"


class SwitchProNfcGap(unittest.TestCase):
    def test_device_context_claim_remains_source_only(self):
        path = ROOT / "records" / "claim" / f"{CLAIM_ID}.json"
        record = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(record["id"], CLAIM_ID)
        self.assertEqual(record["applicability"]["controller"], "switch-pro")
        self.assertEqual(record["applicability"]["transport"], "source_only")
        self.assertEqual(record["evidence_role"], "device")
        self.assertEqual(record["status"], "source_supported")
        self.assertEqual(record["experiments"], [])
        self.assertEqual(set(record["sources"]), {
            "swpro-dekunukem-bluetooth-hid-notes",
            "swpro-dekunukem-bluetooth-hid-subcommands-notes",
        })


if __name__ == "__main__":
    unittest.main()
