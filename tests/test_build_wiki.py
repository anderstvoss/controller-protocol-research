"""Regression checks for the additive, record-derived Markdown wiki."""
import hashlib
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from build_wiki import Writer, read_records, write_pages  # noqa: E402
from status import status as corpus_status  # noqa: E402


class WikiGenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = read_records(ROOT)
        cls.rows = corpus_status(ROOT)
        cls.pages = Writer(ROOT, "a" * 40, cls.records).build(cls.rows)

    def test_every_controller_and_claim_has_evidence_link(self):
        claims = self.records["claim"]
        controllers = self.records["controller"]
        for controller_id in controllers:
            path = "controllers/" + controller_id + ".md"
            self.assertIn(path, self.pages)
            page = self.pages[path]
            self.assertIn("/records/controller/" + controller_id + ".json", page)
        for claim_id, (claim, _) in claims.items():
            controller_id = claim["applicability"]["controller"]
            page = self.pages["controllers/" + controller_id + ".md"]
            self.assertIn("#### " + claim_id + "\n", page)
            self.assertIn("/records/claim/" + claim_id + ".json", page)
            self.assertIn("**Status:** " + chr(96) + claim["status"] + chr(96), page)
            self.assertIn("**Pinned sources:**", page)

    def test_source_and_experiment_details_are_not_elided(self):
        combined_sources = "\n".join(
            text for path, text in self.pages.items() if path.startswith("sources/part-")
        )
        for source_id, (source, _) in self.records["source"].items():
            self.assertIn("## " + source_id + "\n", combined_sources)
            self.assertIn(source["sha256"], combined_sources)
            self.assertIn(source["lineage"], combined_sources)
        combined_experiments = "\n".join(
            text for path, text in self.pages.items() if path.startswith("experiments/part-")
        )
        for experiment_id, (experiment, _) in self.records["experiment"].items():
            self.assertIn("## " + experiment_id + "\n", combined_experiments)
            self.assertIn(experiment["procedure"], combined_experiments)
            if experiment["semantic_outcome"]:
                self.assertIn(experiment["semantic_outcome"], combined_experiments)

    def test_status_and_role_are_kept_separate(self):
        claims = self.records["claim"]
        for controller_id in self.records["controller"]:
            page = self.pages["controllers/" + controller_id + ".md"]
            for claim, _ in claims.values():
                if claim["applicability"]["controller"] != controller_id:
                    continue
                heading = "## Consumer claims" if claim.get("evidence_role") == "consumer" else "## Device claims"
                self.assertIn(heading, page)
                for other_id in claim["conflicts_with"] + claim["supersedes"]:
                    self.assertIn("/records/claim/" + other_id + ".json", page)

    def test_generation_is_read_only_and_check_detects_drift(self):
        original = {
            path: hashlib.sha256(path.read_bytes()).hexdigest()
            for category in ("claim", "source", "experiment", "fixture", "controller", "report")
            for path in (ROOT / "records" / category).glob("*.json")
        }
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            write_pages(target, self.pages)
            write_pages(target, self.pages, check=True)
            (target / "index.md").write_text("stale", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "out of date"):
                write_pages(target, self.pages, check=True)
        self.assertEqual(
            original,
            {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in original},
        )

    def test_research_document_index_does_not_duplicate_notes(self):
        documents = self.pages["research-documents.md"]
        for path in (ROOT / "docs").glob("*.md"):
            self.assertIn("/" + path.relative_to(ROOT).as_posix(), documents)


if __name__ == "__main__":
    unittest.main()
