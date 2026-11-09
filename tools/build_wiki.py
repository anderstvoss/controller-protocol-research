"""Generate an additive, read-only Markdown wiki from the validated evidence corpus.

The JSON records are the source of truth. This program neither edits nor creates
records, claims, fixtures, source pins, experiments, or pre-existing research notes.
Generated pages are a navigational snapshot, not a new authority.
"""
import argparse
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote

from status import status as corpus_status

CATEGORIES = ("controller", "claim", "source", "experiment", "fixture", "report")
REPO_URL = "https://github.com/anderstvoss/controller-protocol-research"
TICK = chr(96)


def code(value):
    return TICK + str(value).replace(TICK, "") + TICK


def cell(value):
    return str(value).replace("|", r"\|").replace("\n", " ")


def read_records(root):
    records = {}
    for category in CATEGORIES:
        records[category] = {}
        for path in sorted((root / "records" / category).glob("*.json")):
            record = json.loads(path.read_text(encoding="utf-8"))
            if record["id"] in records[category]:
                raise ValueError("duplicate " + category + " ID: " + record["id"])
            records[category][record["id"]] = (record, path.relative_to(root).as_posix())
    return records


def git_revision(root):
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=False,
    )
    sha = result.stdout.strip()
    return sha if result.returncode == 0 and len(sha) == 40 else "main"


class Writer:
    def __init__(self, root, revision, records):
        self.root = root
        self.revision = revision
        self.records = records
        self.pages = {}
        self.claims_by_controller = defaultdict(list)
        for claim, _ in records["claim"].values():
            self.claims_by_controller[claim["applicability"]["controller"]].append(claim)
        for claims in self.claims_by_controller.values():
            claims.sort(key=lambda claim: claim["id"])

    def blob(self, path):
        return REPO_URL + "/blob/" + quote(self.revision, safe="") + "/" + quote(path, safe="/")

    def evidence(self, category, record_id):
        _, path = self.records[category][record_id]
        return "[" + code(record_id) + "](" + self.blob(path) + ")"

    def links(self, category, ids):
        return ", ".join(self.evidence(category, record_id) for record_id in ids) if ids else "none"

    def page(self, path, body):
        self.pages[path] = body.rstrip() + "\n"

    def header(self, title):
        return (
            "# " + title + "\n\n"
            "> Generated from corpus revision " + code(self.revision) + ". "
            "The linked JSON records, not this rendered page, are authoritative. "
            "Evidence categories describe support, not implementation readiness.\n\n"
        )

    def controllers(self, rows):
        summary = {row["id"]: row for row in rows}
        index = [
            self.header("Controller evidence"),
            "Claims are grouped by controller, evidence role and transport. "
            "A consumer observation cannot elevate the device evidence category. "
            "Unknown, inferred, rejected and conflicted claims remain visible.\n\n",
            "| Controller | Device evidence | Consumer evidence | Claims |\n",
            "| --- | --- | --- | ---: |\n",
        ]
        for controller_id, (controller, _) in sorted(
            self.records["controller"].items(), key=lambda item: item[1][0]["name"].casefold()
        ):
            row = summary[controller_id]
            link = "[{}](controllers/{}.md)".format(cell(controller["name"]), controller_id)
            index.append(
                "| {} | {} | {} | {} |\n".format(
                    link, row["category"], row["consumer_category"],
                    len(self.claims_by_controller[controller_id]),
                )
            )
            detail = [self.header(controller["name"])]
            detail.append("**Registry:** " + self.evidence("controller", controller_id) + "  \n")
            detail.append("**Kind:** " + code(controller["kind"]) + "  \n")
            if controller["parent"]:
                parent = controller["parent"]
                detail.append("**Parent:** [" + code(parent) + "](" + parent + ".md)  \n")
            if controller["tracking"]:
                repo, issue = controller["tracking"].split("#", 1)
                detail.append("**Tracking:** [issue #" + issue + "](https://github.com/" + repo + "/issues/" + issue + ")  \n")
            detail.append("**Registry notes:** " + controller["notes"] + "\n\n")
            detail.append("**Device evidence:** " + row["category"] + "  \n")
            detail.append("**Consumer evidence:** " + row["consumer_category"] + "\n\n")
            detail.append("## Evidence by transport\n\n")
            detail.append("| Role | Transport | Strongest category | Claims |\n| --- | --- | --- | ---: |\n")
            claims = self.claims_by_controller[controller_id]
            for role in ("device", "consumer"):
                subset = [c for c in claims if c.get("evidence_role", "device") == role]
                counter = Counter(c["applicability"]["transport"] for c in subset)
                transport_levels = row["transports"] if role == "device" else row["consumer_transports"]
                for transport in sorted(counter):
                    detail.append(
                        "| {} | {} | {} | {} |\n".format(
                            role, code(transport), transport_levels[transport], counter[transport]
                        )
                    )
            if not claims:
                detail.append("\nNo claims are recorded for this controller.\n")
            for role in ("device", "consumer"):
                subset = [c for c in claims if c.get("evidence_role", "device") == role]
                if not subset:
                    continue
                detail.append("\n## " + role.title() + " claims\n\n")
                by_transport = defaultdict(list)
                for claim in subset:
                    by_transport[claim["applicability"]["transport"]].append(claim)
                for transport, grouped in sorted(by_transport.items()):
                    detail.append("### " + transport + "\n\n")
                    for claim in grouped:
                        scope = claim["applicability"]
                        detail.append("#### " + claim["id"] + "\n\n")
                        detail.append("**Claim record:** " + self.evidence("claim", claim["id"]) + "  \n")
                        detail.append("**Status:** " + code(claim["status"]) + "  \n")
                        detail.append("**Revision:** " + scope["revision"] + "  \n")
                        detail.append("**Firmware:** " + scope["firmware"] + "  \n")
                        detail.append("**Scope:** " + scope["scope"] + "\n\n")
                        detail.extend("> " + line + "\n" for line in claim["statement"].splitlines())
                        detail.append("\n**Pinned sources:** " + self.links("source", claim["sources"]) + "  \n")
                        detail.append("**Experiments:** " + self.links("experiment", claim["experiments"]) + "  \n")
                        detail.append("**Conflicts with:** " + self.links("claim", claim["conflicts_with"]) + "  \n")
                        detail.append("**Supersedes:** " + self.links("claim", claim["supersedes"]) + "  \n")
                        if claim["rejection_scope"]:
                            detail.append("**Rejection scope:** " + claim["rejection_scope"] + "  \n")
                        detail.append("\n")
            detail.append(
                "---\n\n[All controllers](../index.md) | "
                "[Source index](../sources/index.md) | "
                "[Experiments](../experiments/index.md) | "
                "[Research documents](../research-documents.md)\n"
            )
            self.page("controllers/" + controller_id + ".md", "".join(detail))
        self.page("index.md", "".join(index) + "\n"
                  "## Reference indexes\n\n"
                  "- [All claims](claims.md) — every individual statement, status and evidence link\n"
                  "- [Pinned sources](sources/index.md) — original URL, revision, digest, lineage and locator\n"
                  "- [Experiments](experiments/index.md) — procedure, outcome and associated fixtures\n"
                  "- [Fixtures](fixtures/index.md) — reviewed payload metadata and transformation lineage\n"
                  "- [Report shapes](reports.md) — measured or source-scoped report descriptions\n"
                  "- [Research documents](research-documents.md) — existing narrative investigations, unchanged\n\n"
                  "A physically observed host/consumer path is not proof of physical device fidelity. "
                  "The original records retain their precise status and transport applicability.\n")
        claim_index = [
            self.header("All claims"),
            "| Claim | Controller | Role | Transport | Status | Sources | Experiments |\n",
            "| --- | --- | --- | --- | --- | ---: | ---: |\n",
        ]
        for claim_id, (claim, _) in sorted(self.records["claim"].items()):
            controller_id = claim["applicability"]["controller"]
            claim_index.append(
                "| [{}](controllers/{}.md#{}) | [{}](controllers/{}.md) | {} | {} | {} | {} | {} |\n".format(
                    code(claim_id), controller_id, claim_id,
                    code(controller_id), controller_id,
                    claim.get("evidence_role", "device"),
                    code(claim["applicability"]["transport"]), code(claim["status"]),
                    len(claim["sources"]), len(claim["experiments"]),
                )
            )
        self.page("claims.md", "".join(claim_index))

    def paged_index(self, category, heading, render, page_size=40):
        entries = sorted(self.records[category].items())
        index = [self.header(heading)]
        for offset in range(0, len(entries), page_size):
            part = offset // page_size + 1
            filename = "part-{:02d}.md".format(part)
            index.append(
                "### [Records {}–{}]({})\n\n".format(
                    offset + 1, min(offset + page_size, len(entries)), filename
                )
            )
            part_lines = [self.header(heading + " — part " + str(part))]
            for record_id, (record, _) in entries[offset:offset + page_size]:
                index.append("- [" + code(record_id) + "](" + filename + "#" + record_id + ")\n")
                part_lines.append("## " + record_id + "\n\n" + render(record) + "\n\n")
            index.append("\n")
            part_lines.append("[Back to " + heading.lower() + "](index.md)\n")
            self.page(category + "s/" + filename, "".join(part_lines))
        if not entries:
            index.append("No records.\n")
        self.page(category + "s/index.md", "".join(index))

    def sources(self):
        def render(src):
            return (
                "**Record:** " + self.evidence("source", src["id"]) + "  \n"
                "**Kind:** " + code(src["kind"]) + "  \n"
                "**Lineage:** " + code(src["lineage"]) + "  \n"
                "**Revision:** " + code(src["revision"]) + "  \n"
                "**SHA-256:** " + code(src["sha256"]) + "  \n"
                "**Upstream:** [" + src["url"] + "](" + src["url"] + ")  \n"
                "**Locator:** " + src["locator"]
            )
        self.paged_index("source", "Pinned sources", render)

    def experiments(self):
        def render(exp):
            return (
                "**Record:** " + self.evidence("experiment", exp["id"]) + "  \n"
                "**Kind:** " + code(exp["kind"]) + "  \n"
                "**Status:** " + code(exp["status"]) + "  \n"
                "**Sources:** " + self.links("source", exp["sources"]) + "  \n"
                "**Fixtures:** " + self.links("fixture", exp["fixtures"]) + "\n\n"
                "**Procedure:** " + exp["procedure"] + "\n\n"
                "**Semantic outcome:** " + (exp["semantic_outcome"] or "not recorded")
            )
        self.paged_index("experiment", "Experiments", render)

    def fixtures(self):
        def render(fix):
            return (
                "**Record:** " + self.evidence("fixture", fix["id"]) + "  \n"
                "**Kind:** " + code(fix["kind"]) + "  \n"
                "**Format:** " + code(fix["format"]) + "  \n"
                "**Fixture file:** [" + code(fix["path"]) + "](" + self.blob(fix["path"]) + ")  \n"
                "**SHA-256:** " + code(fix["sha256"]) + "  \n"
                "**Sources:** " + self.links("source", fix["sources"]) + "  \n"
                "**Experiments:** " + self.links("experiment", fix["experiments"]) + "  \n"
                "**Claims:** " + self.links("claim", fix["claims"]) + "  \n"
                "**Parent:** " + (self.evidence("fixture", fix["parent"]) if fix["parent"] else "none") + "  \n"
                "**Transformation:** " + (fix["transform"] or "none")
            )
        self.paged_index("fixture", "Fixtures", render)

    def reports(self):
        lines = [self.header("Report shapes")]
        for record_id, (rep, _) in sorted(self.records["report"].items()):
            lines.append("## " + record_id + "\n\n")
            lines.append("**Record:** " + self.evidence("report", record_id) + "  \n")
            lines.append("**Claim:** " + self.evidence("claim", rep["claim"]) + "  \n")
            scope = rep["applicability"]
            lines.append("**Applies to:** " + self.evidence("controller", scope["controller"]) +
                         ", " + code(scope["transport"]) + ", " + scope["scope"] + "  \n")
            for field in ("revision", "firmware", "direction", "logical_id", "raw_includes_id",
                          "length", "offset_origin", "bit_numbering", "endian",
                          "signedness", "units", "coordinate_frame", "values"):
                value = scope[field] if field in scope else rep[field]
                lines.append("**" + field.replace("_", " ").title() + ":** " + code(value) + "  \n")
            lines.append("\n")
        self.page("reports.md", "".join(lines))

    def documents(self):
        lines = [
            self.header("Research documents"),
            "These are the repository's existing narrative research notes and ledgers. "
            "They are linked intact; record-level evidence is authoritative for claim status.\n\n",
        ]
        docs = sorted(self.root.glob("docs/*.md")) + sorted(self.root.glob("docs/ledgers/*.md"))
        for path in docs:
            relative = path.relative_to(self.root).as_posix()
            lines.append("- [" + code(relative) + "](" + self.blob(relative) + ")\n")
        self.page("research-documents.md", "".join(lines))

    def build(self, rows):
        self.controllers(rows)
        self.sources()
        self.experiments()
        self.fixtures()
        self.reports()
        self.documents()
        return self.pages


def write_pages(output, pages, check=False):
    expected = set(pages)
    existing = {p.relative_to(output).as_posix() for p in output.rglob("*.md")} if output.exists() else set()
    stale = existing - expected
    differing = [
        relative for relative, content in pages.items()
        if not (output / relative).exists()
        or (output / relative).read_text(encoding="utf-8") != content
    ]
    if check:
        if stale or differing:
            raise ValueError("wiki out of date: missing/changed " + repr(differing) +
                             "; unexpected " + repr(sorted(stale)))
        return
    if stale:
        raise ValueError("unexpected generated pages (not deleted automatically): " + repr(sorted(stale)))
    for relative, content in sorted(pages.items()):
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--ref", default=None, help="commit SHA for immutable evidence links")
    parser.add_argument("--check", action="store_true", help="verify existing generated files")
    args = parser.parse_args()
    root = args.root.resolve()
    rows = corpus_status(root)  # includes full schema/fixture/lineage validation
    records = read_records(root)
    revision = args.ref or git_revision(root)
    if revision != "main" and (len(revision) != 40 or any(c not in "0123456789abcdef" for c in revision)):
        parser.error("--ref must be a lowercase full commit SHA (or main for a non-git test corpus)")
    output = args.output or root / "docs/wiki/generated"
    pages = Writer(root, revision, records).build(rows)
    write_pages(output, pages, check=args.check)
    print("{} wiki pages {} ({} claims, {} sources)".format(
        len(pages), "checked" if args.check else "generated",
        len(records["claim"]), len(records["source"]),
    ))


if __name__ == "__main__":
    main()
