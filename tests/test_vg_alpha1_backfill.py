import json
import sys
import unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import status as status_module


def b_claims():
    return [json.loads(p.read_text()) for p in (ROOT / "records/claim").glob("*.json")
            if p.name.startswith(("ds-vg-", "ds4-vg-", "swpro-vg-", "x360-vg-", "vg-alpha1-"))]


class VirtualgamepadHistoricalBackfill(unittest.TestCase):
    def test_source_pins_and_explicit_claim_roles(self):
        claims = b_claims()
        self.assertEqual(len(claims), 31)
        self.assertEqual(Counter(c["evidence_role"] for c in claims),
                         {"consumer": 30, "device": 1})
        self.assertEqual({c["id"] for c in claims if c["evidence_role"] == "device"},
                         {"ds-vg-exp0015-physical-usb-hid"})
        self.assertTrue(all(c["status"] == "source_supported" for c in claims))
        self.assertTrue(all(c["sources"] for c in claims))
        self.assertIn("maintainer-reported physical observation, not corpus physical validation",
                      next(c for c in claims if c["evidence_role"] == "device")["applicability"]["scope"])
        sources = {p.stem: json.loads(p.read_text())
                   for p in (ROOT / "records/source").glob("vg-alpha1-*.json")}
        self.assertEqual(len(sources), 13)
        self.assertTrue(all(s["lineage"] == "virtualgamepad" and
                            s["kind"] == "research_lead" and len(s["sha256"]) == 64
                            for s in sources.values()))
        self.assertEqual(sources["vg-alpha1-exp0015"]["revision"],
                         "c60c16409e91e39ddba56a78475bdabe3780d1d0")
        self.assertEqual(len(list((ROOT / "records/source").glob("audio-vg-exp0023.json"))), 1)

    def test_historical_run_statuses_and_invalid_attempts(self):
        exps = {p.stem: json.loads(p.read_text()) for p in
                (ROOT / "records/experiment").glob("*.json")
                if p.name.startswith(("ds-vg-", "ds4-vg-", "swpro-vg-",
                                      "x360-vg-", "vg-alpha1-"))}
        self.assertEqual(len(exps), 18)
        self.assertEqual(Counter(x["status"] for x in exps.values()),
                         {"passed": 16, "failed": 1, "blocked": 1})
        self.assertEqual(exps["ds4-vg-exp0012-compound-host-run"]["status"], "blocked")
        self.assertEqual(exps["ds4-vg-exp0011-evdev-discovery-host-run"]["status"], "failed")
        self.assertTrue(all(x["kind"] == "virtual_host_run" and not x["fixtures"]
                            and "Historical" in x["procedure"] for x in exps.values()))
        self.assertFalse(any("rebuild" in p or "dpad-failure" in p
                             for p in exps))

    def test_status_before_and_after_using_status_module(self):
        # Before = same repository minus B claims only, retaining its validated sources and runs.
        load = status_module.load
        def without_b(root, category):
            data = load(root, category)
            if category == "claim":
                exclude = {c["id"] for c in b_claims()}
                return [c for c in data if c["id"] not in exclude]
            return data
        with patch.object(status_module, "load", side_effect=without_b):
            before = {r["id"]: r for r in status_module.status(ROOT)}
        after = {r["id"]: r for r in status_module.status(ROOT)}
        print("\n| Controller | Device before → after | Consumer before → after | Claims before → after |")
        print("| --- | --- | --- | --- |")
        for controller in ("dualsense", "dualshock4", "switch-pro", "xbox360"):
            a, b = before[controller], after[controller]
            self.assertEqual(a["category"], b["category"])
            self.assertEqual(a["consumer_category"], b["consumer_category"])
            n0, n1 = sum(a["claims"].values()), sum(b["claims"].values())
            self.assertGreater(n1, n0)
            print(f"| {controller} | {a['category']} → {b['category']} | "
                  f"{a['consumer_category']} → {b['consumer_category']} | {n0} → {n1} |")
        self.assertEqual(after["switch-pro"]["category"], "No evidence")
        self.assertEqual(after["xbox360"]["category"], "No evidence")


if __name__ == "__main__":
    unittest.main()
