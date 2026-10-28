import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SwitchProL0Ledger(unittest.TestCase):
    def test_new_claims_have_explicit_roles_and_no_physical_promotion(self):
        claims = [json.loads(p.read_text()) for p in
                  (ROOT / "records/claim").glob("swpro-l0-*.json")]
        self.assertEqual(len(claims), 21)
        self.assertEqual(sum(c["evidence_role"] == "consumer" for c in claims), 12)
        self.assertEqual(sum(c["evidence_role"] == "device" for c in claims), 9)
        self.assertEqual(sum(c["status"] == "unknown" for c in claims), 5)
        self.assertEqual(sum(c["status"] == "source_supported" for c in claims), 16)
        self.assertTrue(all(c["applicability"]["controller"] == "switch-pro"
                            and c["applicability"]["transport"] == "source_only"
                            and c["sources"] and c["experiments"] == []
                            for c in claims))
        self.assertTrue(all(c["status"] not in
                            {"physically_observed", "physically_validated"} for c in claims))
        self.assertTrue(all(not any("vg-alpha1" in source for source in c["sources"])
                            for c in claims))

    def test_pinned_independent_source_is_not_retail_capture(self):
        source = json.loads((ROOT / "records/source/swpro-openpuck-mode.json").read_text())
        self.assertEqual(source["kind"], "compatibility_implementation")
        self.assertEqual(source["lineage"], "openpuck")
        self.assertEqual(source["sha256"],
                         "13f5c426b06991b44c511e0fbe51cdd0f8133a1b5072233ad8f643356202c767")
        self.assertEqual(source["revision"],
                         "29f4d1e8b85c0a7c19e0c8b977a1a56a2c42ea6d")
        existing = {"audio-linux-hid-nintendo", "audio-sdl-switch-pro"}
        self.assertTrue(all((ROOT / "records/source" / (s + ".json")).is_file()
                            for s in existing))


if __name__ == "__main__":
    unittest.main()
