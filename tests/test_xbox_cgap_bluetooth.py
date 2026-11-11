import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class XboxBluetoothConsumerGap(unittest.TestCase):
    def test_claims_remain_consumer_only_without_experiments(self):
        paths = sorted((ROOT / "records/claim").glob("xbox-cgap-*.json"))
        self.assertEqual(len(paths), 24)
        for path in paths:
            claim = json.loads(path.read_text())
            with self.subTest(record=claim["id"]):
                self.assertEqual(path.stem, claim["id"])
                self.assertEqual(claim["evidence_role"], "consumer")
                self.assertEqual(claim["applicability"]["controller"], "xbox-series")
                self.assertIn(claim["applicability"]["transport"], {"bluetooth", "source_only"})
                self.assertIn(claim["status"], {"source_supported", "inferred", "unknown"})
                self.assertEqual(claim["experiments"], [])
                self.assertTrue(claim["sources"])
                for source_id in claim["sources"]:
                    self.assertTrue((ROOT / "records/source" / f"{source_id}.json").exists())

    def test_share_mapping_is_explicit_keyboard_f12(self):
        path = ROOT / "records/claim/xbox-cgap-xpadneo-share-f12.json"
        claim = json.loads(path.read_text())
        self.assertIn("KEY_F12", claim["statement"])
        self.assertIn("keyboard node", claim["statement"])
        self.assertIn("xbox-cgap-xpadneo-header", claim["sources"])
        self.assertEqual(claim["evidence_role"], "consumer")

    def test_scope_has_no_physical_promotion(self):
        paths = (ROOT / "records/claim").glob("xbox-cgap-*.json")
        claims = [json.loads(path.read_text()) for path in paths]
        self.assertFalse(any(c["status"].startswith("physically_") for c in claims))
        self.assertEqual(
            [c["id"] for c in claims if c["status"] == "inferred"],
            ["xbox-cgap-virtual-uhid-feasibility"],
        )


if __name__ == "__main__":
    unittest.main()
