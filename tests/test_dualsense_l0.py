import json
import sys
import unittest
from pathlib import Path
from collections import Counter
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import status as status_module


class DualSenseL0Ledger(unittest.TestCase):
    def claims(self):
        return [json.loads(p.read_text()) for p in
                (ROOT / "records/claim").glob("ds-l0-*.json")]

    def test_role_status_and_scope(self):
        claims = self.claims()
        self.assertEqual(len(claims), 25)
        self.assertEqual(Counter(x["evidence_role"] for x in claims),
                         {"consumer": 15, "device": 10})
        self.assertEqual(Counter(x["status"] for x in claims),
                         {"source_supported": 17, "unknown": 7, "inferred": 1})
        self.assertTrue(all(x["applicability"]["controller"] == "dualsense"
                            and x["sources"] and not x["conflicts_with"]
                            for x in claims))
        self.assertTrue(all(x["applicability"]["transport"] == "source_only"
                            for x in claims if x["status"] in ("unknown","inferred") and
                            x["id"] in ("ds-l0-steam-input-mode-unmeasured",
                                        "ds-l0-uhid-gyro-association-hypothesis")))
        self.assertTrue(all(x["status"] not in ("physically_observed","physically_validated")
                            for x in claims))
        self.assertFalse(any("wip/btvirt" in x["applicability"]["scope"] for x in claims))

    def test_archived_steam_gyro_claims(self):
        claims = {x["id"]: x for x in self.claims()}
        report = claims["ds-l0-dummy-hcd-steam-gyro-contrast"]
        hypothesis = claims["ds-l0-uhid-gyro-association-hypothesis"]
        self.assertEqual(report["status"], "source_supported")
        self.assertEqual(report["evidence_role"], "consumer")
        self.assertEqual(hypothesis["status"], "inferred")
        self.assertEqual(hypothesis["evidence_role"], "consumer")
        self.assertIn("vg-alpha1-dummy-hcd-poc", report["sources"])
        self.assertIn("vg-alpha1-dummy-hcd-poc", hypothesis["sources"])
        self.assertEqual(report["experiments"],
                         ["ds-vg-dummy-hcd-steam-host-run"])
        self.assertEqual(hypothesis["experiments"],
                         ["ds-vg-dummy-hcd-steam-host-run"])

    def test_status_before_after_d(self):
        read = status_module.load
        def without_d(root, category):
            records = read(root, category)
            if category == "claim":
                return [x for x in records if not x["id"].startswith("ds-l0-")]
            return records
        with patch.object(status_module, "load", side_effect=without_d):
            previous = next(x for x in status_module.status(ROOT)
                            if x["id"] == "dualsense")
        updated = next(x for x in status_module.status(ROOT)
                       if x["id"] == "dualsense")
        self.assertEqual(previous["category"], "Source evidence")
        self.assertEqual(updated["category"], "Source evidence")
        self.assertEqual(previous["consumer_category"], "Source evidence")
        self.assertEqual(updated["consumer_category"], "Source evidence")
        self.assertEqual(sum(updated["claims"].values()) - sum(previous["claims"].values()), 25)
        print("\n| Controller | Device before → after | Consumer before → after | Claims before → after |")
        print("| --- | --- | --- | --- |")
        print(f"| dualsense | {previous['category']} → {updated['category']} | "
              f"{previous['consumer_category']} → {updated['consumer_category']} | "
              f"{sum(previous['claims'].values())} → {sum(updated['claims'].values())} |")


if __name__ == "__main__":
    unittest.main()
