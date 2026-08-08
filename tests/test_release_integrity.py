from __future__ import annotations

import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]


def manifest_entries(manifest: Path) -> list[tuple[str, Path]]:
    entries = []
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if line.strip():
            digest, relative_path = line.split(maxsplit=1)
            entries.append((digest, manifest.parent / relative_path))
    return entries


@pytest.mark.parametrize(
    "manifest",
    [
        ROOT / "SHA256SUMS.txt",
        ROOT / "SHA256SUMS-v1.4.txt",
        ROOT / "practice-kit" / "SHA256SUMS.txt",
    ],
)
def test_checksum_manifest_matches_files(manifest: Path) -> None:
    for expected, path in manifest_entries(manifest):
        assert path.is_file(), f"missing manifest file: {path}"
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == expected, f"checksum mismatch: {path}"


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        if tag == "a" and values.get("href"):
            self.hrefs.append(values["href"] or "")


@pytest.mark.parametrize(
    "filename",
    [
        "index.html",
        "en.html",
        "zh.html",
        "harness.html",
        "eval-rules.html",
        "continuity.html",
        "related-work.html",
        "practice-kit/index.html",
        "practice-kit/closeout.html",
        "practice-kit/golden-case.html",
    ],
)
def test_current_html_has_no_broken_local_links_or_ai_dash(filename: str) -> None:
    page = ROOT / filename
    text = page.read_text(encoding="utf-8")
    assert "—" not in text
    assert "–" not in text

    parser = LinkCollector()
    parser.feed(text)
    for href in parser.hrefs:
        target = urlsplit(href)
        if target.scheme or target.netloc:
            continue
        if not target.path:
            assert unquote(target.fragment) in parser.ids
            continue
        linked = (page.parent / unquote(target.path)).resolve()
        if linked.is_dir():
            linked = linked / "index.html"
        assert linked.is_file(), f"broken link in {filename}: {href}"


def test_english_is_default_and_chinese_is_secondary() -> None:
    english = (ROOT / "index.html").read_text(encoding="utf-8")
    chinese = (ROOT / "zh.html").read_text(encoding="utf-8")
    legacy_english = (ROOT / "en.html").read_text(encoding="utf-8")

    assert '<html lang="en">' in english
    assert 'hreflang="zh-Hans" href="zh.html"' in english
    assert '<html lang="zh-CN">' in chinese
    assert 'hreflang="en" href="index.html"' in chinese
    assert 'http-equiv="refresh" content="0; url=index.html"' in legacy_english


@pytest.mark.parametrize(
    "filename",
    [
        "index.html",
        "zh.html",
        "harness.html",
        "eval-rules.html",
        "continuity.html",
        "related-work.html",
        "practice-kit/index.html",
        "practice-kit/closeout.html",
        "practice-kit/golden-case.html",
    ],
)
def test_public_web_guides_are_static_and_self_contained(filename: str) -> None:
    text = (ROOT / filename).read_text(encoding="utf-8")
    assert "<script" not in text.lower()
    assert "fonts.googleapis.com" not in text
    assert "fonts.gstatic.com" not in text
    assert "unpkg.com" not in text

    stylesheet = (ROOT / "site.css").read_text(encoding="utf-8")
    assert "@import" not in stylesheet
    assert "http://" not in stylesheet
    assert "https://" not in stylesheet


@pytest.mark.parametrize("filename", ["index.html", "zh.html"])
def test_reader_navigation_uses_designed_pages(filename: str) -> None:
    text = (ROOT / filename).read_text(encoding="utf-8")

    assert 'href="practice-kit/README.md"' not in text
    assert 'href="RELATED_WORK.md"' not in text
    assert 'href="HARNESS.md"' not in text
    assert 'href="EVAL_RULES.md"' not in text
    assert 'href="practice-kit/"' in text
    assert 'href="related-work.html"' in text
    assert 'href="harness.html"' in text
    assert 'href="eval-rules.html"' in text
    assert 'href="continuity.html"' in text
    assert '<details class="quick-check">' in text
    assert '<details class="quick-check" open>' not in text


def test_v2_release_is_explicit_and_preserves_v1_5_history() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    english = (ROOT / "index.html").read_text(encoding="utf-8")
    chinese = (ROOT / "zh.html").read_text(encoding="utf-8")

    assert "Current release:** GDAC v2.0" in readme
    assert "Owner-authorized and published on 2026-08-08" in readme
    assert "Previous release:** GDAC v1.5" in readme
    assert "39ff3cd" in readme
    assert "## GDAC v2.0 - 2026-08-08" in changelog
    assert "accepted for publication by the Owner" in changelog
    assert "GDAC v2.0 · released 2026-08-08" in english
    assert "GDAC v2.0 · 2026-08-08 发布" in chinese


@pytest.mark.parametrize(
    ("filename", "prefix"),
    [
        ("index.html", ""),
        ("harness.html", ""),
        ("eval-rules.html", ""),
        ("continuity.html", ""),
        ("related-work.html", ""),
        ("practice-kit/index.html", "../"),
        ("practice-kit/closeout.html", "../"),
        ("practice-kit/golden-case.html", "../"),
    ],
)
def test_primary_navigation_is_consistent(filename: str, prefix: str) -> None:
    text = (ROOT / filename).read_text(encoding="utf-8")
    expected = [
        (f'href="{prefix}index.html"', "Overview"),
        (f'href="{prefix}harness.html"', "Harness"),
        (f'href="{prefix}eval-rules.html"', "Eval Rules"),
        (f'href="{prefix}practice-kit/"' if not prefix else 'href="./"', "Practice Kit"),
        (f'href="{prefix}related-work.html"', "Related Work"),
        (f'href="{prefix}zh.html"', "中文"),
    ]
    nav = text.split('<nav class="nav"', 1)[1].split("</nav>", 1)[0]
    for href, label in expected:
        assert href in nav
        assert label in nav


def test_v2_terms_and_bounded_example_claim_do_not_drift() -> None:
    sources = [
        ROOT / "README.md",
        ROOT / "HARNESS.md",
        ROOT / "EVAL_RULES.md",
        ROOT / "V1_3_CONTINUITY.md",
        ROOT / "index.html",
        ROOT / "zh.html",
        ROOT / "harness.html",
        ROOT / "eval-rules.html",
        ROOT / "continuity.html",
    ]
    joined = "\n".join(path.read_text(encoding="utf-8") for path in sources)
    for stale_term in (
        "ready_for_owner_decision",
        "Technical Evidence Gate",
        "Evidence Gate",
        "Owner Gate",
        "six Harness gates",
        "Contract gate",
        "Authority gate",
        "accept, conditions",
        "accept、conditions",
    ):
        assert stale_term not in joined

    contract = yaml.safe_load(
        (ROOT / "practice-kit/examples/dry-run-outcome-contract.example.yaml").read_text(
            encoding="utf-8"
        )
    )
    plan = yaml.safe_load(
        (ROOT / "practice-kit/examples/eval-plan.example.yaml").read_text(
            encoding="utf-8"
        )
    )
    contract_claim = next(
        criterion["description"]
        for criterion in contract["acceptance_criteria"]
        if criterion["criterion_id"] == "no-write"
    )
    plan_claim = next(
        claim["statement"] for claim in plan["claims"] if claim["claim_id"] == "no-write"
    )
    assert contract_claim == plan_claim
    assert "declared candidate-process and fixture boundary" in contract_claim

    trace = json.loads(
        (ROOT / "practice-kit/examples/golden-dry-run/write-trace.json").read_text(
            encoding="utf-8"
        )
    )
    assert trace["candidate_write_api_inventory"] == trace["instrumented_operations"]
    assert trace["uncovered_write_apis"] == []


@pytest.mark.parametrize(
    "filename",
    [
        "index.html",
        "zh.html",
        "harness.html",
        "eval-rules.html",
        "continuity.html",
        "related-work.html",
        "practice-kit/index.html",
        "practice-kit/closeout.html",
        "practice-kit/golden-case.html",
    ],
)
def test_public_tables_have_explicit_header_scope(filename: str) -> None:
    text = (ROOT / filename).read_text(encoding="utf-8")
    missing_scope = re.findall(r"<th\b(?![^>]*\bscope=)[^>]*>", text, flags=re.IGNORECASE)
    assert not missing_scope, f"table headers without scope in {filename}: {missing_scope}"


def test_eval_class_and_grader_type_remain_separate_in_public_sources() -> None:
    specification = (ROOT / "EVAL_RULES.md").read_text(encoding="utf-8")
    eval_class_field = specification.split("- `eval_class`:", 1)[1].split(
        "- `grader`:", 1
    )[0]
    schema = (ROOT / "practice-kit/schemas/eval-plan.schema.json").read_text(
        encoding="utf-8"
    )

    assert "model" not in eval_class_field
    assert "human" not in eval_class_field
    assert '"type": {"enum": ["deterministic", "rule", "model", "human"]}' in schema


@pytest.mark.parametrize(
    "filename",
    [
        "Governance-Driven-Agentic-Coding-v1.5.pdf",
        "Governance-Driven-Agentic-Coding-EN-v1.5.pdf",
    ],
)
def test_current_pdf_has_pdf_signature(filename: str) -> None:
    path = ROOT / filename
    assert path.stat().st_size > 50_000
    assert path.read_bytes()[:5] == b"%PDF-"


def test_public_boundaries_cover_release_review_findings() -> None:
    related_work = (ROOT / "RELATED_WORK.md").read_text(encoding="utf-8")
    review_result = (ROOT / "examples/freeze-review/review-result.md").read_text(
        encoding="utf-8"
    )

    for required_reference in (
        "protected branches",
        "CODEOWNERS",
        "Open Policy Agent",
        "Inspect",
        "SLSA provenance",
        "AGENTS.md",
        "EU AI Act",
    ):
        assert required_reference in related_work
    assert "production-outcome evidence remain open" in related_work
    assert "No real defect was caught in this example" in review_result


def test_current_entry_points_are_not_unreleased_candidates() -> None:
    for filename in ("README.md", "index.html", "en.html", "zh.html"):
        text = (ROOT / filename).read_text(encoding="utf-8").lower()
        assert "owner review candidate" not in text
        assert "working candidate" not in text
        assert "unreleased" not in text
        assert "publication:** not authorized" not in text
        assert "v1.5-rc1" not in text
