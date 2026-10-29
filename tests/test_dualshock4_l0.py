import json
import sys
import unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import status as status_module


class DualShock4L0Ledger(unittest.TestCase):
    def claims(self):
        return [json.loads(p.read_text()) for p in
                (ROOT / "records/claim").glob("ds4-l0-*.json")]

    def test_claim_counts_scopes_and_conflict(self):
        claims = self.claims()
        self.assertEqual(len(claims), 26)
        self.assertEqual(Counter(c["evidence_role"] for c in claims),
                         {"device": 13, "consumer": 13})
        self.assertEqual(Counter(c["status"] for c in claims),
                         {"source_supported": 17, "unknown": 8, "conflicted": 1})
        self.assertTrue(all(c["applicability"]["controller"] == "dualshock4"
                            and c["applicability"]["transport"] == "source_only"
                            and c["sources"] and c["experiments"] == [] for c in claims))
        conflict = next(c for c in claims if c["status"] == "conflicted")
        self.assertEqual(conflict["id"], "ds4-l0-device-touch-count-conflict")
        self.assertEqual(conflict["conflicts_with"],
                         ["ds4-l0-consumer-kernel-touch-report-buffer-count"])
        self.assertTrue(all(c["status"] not in {"physically_observed", "physically_validated"}
                            for c in claims))

    def test_new_sources_are_pinned_and_distinct(self):
        lead = json.loads((ROOT / "records/source/ds4-community-playstation-protocol.json").read_text())
        legacy = json.loads((ROOT / "records/source/ds4-linux-hid-sony-v61.json").read_text())
        self.assertEqual(lead["kind"], "research_lead")
        self.assertEqual(lead["lineage"], "noisyloop-game-research")
        self.assertEqual(lead["sha256"],
                         "61101df2bc188bcfbb52d882d52b5076318138553b94cc428d27b01577e05bcb")
        self.assertEqual(legacy["kind"], "kernel_source")
        self.assertEqual(legacy["sha256"],
                         "297b84f9fb1093511590bbaf57f89119cdbf998ca3650099b045b5fb0204b88d")

    def test_status_before_after_e(self):
        load = status_module.load
        def without_e(root, category):
            all_records = load(root, category)
            if category == "claim":
                return [c for c in all_records if not c["id"].startswith("ds4-l0-")]
            return all_records
        with patch.object(status_module, "load", side_effect=without_e):
            before = next(c for c in status_module.status(ROOT)
                          if c["id"] == "dualshock4")
        after = next(c for c in status_module.status(ROOT)
                     if c["id"] == "dualshock4")
        self.assertEqual(before["category"], after["category"])
        self.assertEqual(before["consumer_category"], after["consumer_category"])
        self.assertEqual(sum(after["claims"].values()) - sum(before["claims"].values()), 26)
        print("\n| Controller | Device before → after | Consumer before → after | Claims before → after |")
        print("| --- | --- | --- | --- |")
        print(f"| dualshock4 | {before['category']} → {after['category']} | "
              f"{before['consumer_category']} → {after['consumer_category']} | "
              f"{sum(before['claims'].values())} → {sum(after['claims'].values())} |")


if __name__ == "__main__":
    unittest.main()
