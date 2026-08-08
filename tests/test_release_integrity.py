from __future__ import annotations

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "docs"
METHOD = ROOT / "method"
KIT = ROOT / "practice-kit"
ARCHIVE = ROOT / "archive" / "releases" / "v1-series"

CURRENT_SITE_PAGES = [
    "index.html",
    "zh.html",
    "harness.html",
    "eval-rules.html",
    "continuity.html",
    "related-work.html",
    "practice-kit/index.html",
    "practice-kit/closeout.html",
    "practice-kit/golden-case.html",
]


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
        SITE / "SHA256SUMS.txt",
        ARCHIVE / "SHA256SUMS-v1.4.txt",
        KIT / "SHA256SUMS.txt",
    ],
)
def test_checksum_manifest_matches_files(manifest: Path) -> None:
    entries = manifest_entries(manifest)
    assert len({path for _, path in entries}) == len(entries)
    for expected, path in entries:
        assert re.fullmatch(r"[0-9a-f]{64}", expected)
        assert "__pycache__" not in path.parts
        assert path.suffix != ".pyc"
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
    page = SITE / filename
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
    english = (SITE / "index.html").read_text(encoding="utf-8")
    chinese = (SITE / "zh.html").read_text(encoding="utf-8")
    legacy_english = (SITE / "en.html").read_text(encoding="utf-8")

    assert '<html lang="en">' in english
    assert 'hreflang="zh-Hans" href="https://qisun2026.github.io/governance-driven-agentic-coding/zh.html"' in english
    assert '<html lang="zh-CN">' in chinese
    assert 'hreflang="en" href="https://qisun2026.github.io/governance-driven-agentic-coding/"' in chinese
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
    text = (SITE / filename).read_text(encoding="utf-8")
    assert text.count('<script type="application/ld+json">') == 1
    assert not re.search(r"<script\b[^>]*\bsrc=", text, flags=re.IGNORECASE)
    assert "fonts.googleapis.com" not in text
    assert "fonts.gstatic.com" not in text
    assert "unpkg.com" not in text

    stylesheet = (SITE / "site.css").read_text(encoding="utf-8")
    assert "@import" not in stylesheet
    assert "http://" not in stylesheet
    assert "https://" not in stylesheet


@pytest.mark.parametrize("filename", ["index.html", "zh.html"])
def test_reader_navigation_uses_designed_pages(filename: str) -> None:
    text = (SITE / filename).read_text(encoding="utf-8")

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
    english = (SITE / "index.html").read_text(encoding="utf-8")
    chinese = (SITE / "zh.html").read_text(encoding="utf-8")

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
    text = (SITE / filename).read_text(encoding="utf-8")
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
        METHOD / "harness.md",
        METHOD / "evaluation-rules.md",
        METHOD / "continuity-v1.3.md",
        SITE / "index.html",
        SITE / "zh.html",
        SITE / "harness.html",
        SITE / "eval-rules.html",
        SITE / "continuity.html",
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
        (KIT / "examples/dry-run-outcome-contract.example.yaml").read_text(
            encoding="utf-8"
        )
    )
    plan = yaml.safe_load(
        (KIT / "examples/eval-plan.example.yaml").read_text(
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
        (KIT / "examples/golden-dry-run/write-trace.json").read_text(
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
    text = (SITE / filename).read_text(encoding="utf-8")
    missing_scope = re.findall(r"<th\b(?![^>]*\bscope=)[^>]*>", text, flags=re.IGNORECASE)
    assert not missing_scope, f"table headers without scope in {filename}: {missing_scope}"


def test_eval_class_and_grader_type_remain_separate_in_public_sources() -> None:
    specification = (METHOD / "evaluation-rules.md").read_text(encoding="utf-8")
    eval_class_field = specification.split("- `eval_class`:", 1)[1].split(
        "- `grader`:", 1
    )[0]
    schema = (KIT / "schemas/eval-plan.schema.json").read_text(
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
def test_archived_v1_5_pdf_has_pdf_signature(filename: str) -> None:
    path = ARCHIVE / filename
    assert path.stat().st_size > 50_000
    assert path.read_bytes()[:5] == b"%PDF-"


def test_pre_v2_release_artifacts_are_outside_current_site() -> None:
    assert not list(SITE.glob("*v1.*.pdf"))
    assert not (SITE / "versions").exists()

    expected = {
        "Governance-Driven-Agentic-Coding-EN-v1.3.pdf",
        "Governance-Driven-Agentic-Coding-EN-v1.4.pdf",
        "Governance-Driven-Agentic-Coding-EN-v1.5.pdf",
        "Governance-Driven-Agentic-Coding-v1.2.pdf",
        "Governance-Driven-Agentic-Coding-v1.4.pdf",
        "Governance-Driven-Agentic-Coding-v1.5.pdf",
        "SHA256SUMS-v1.4.txt",
        "versions/v1.4/en.html",
        "versions/v1.4/index.html",
    }
    archived = {
        path.relative_to(ARCHIVE).as_posix()
        for path in ARCHIVE.rglob("*")
        if path.is_file()
    }
    assert archived == expected


def test_public_boundaries_cover_release_review_findings() -> None:
    related_work = (METHOD / "related-work.md").read_text(encoding="utf-8")
    review_result = (KIT / "examples/freeze-review/review-result.md").read_text(
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
    entry_points = [ROOT / "README.md", SITE / "index.html", SITE / "en.html", SITE / "zh.html"]
    for path in entry_points:
        text = path.read_text(encoding="utf-8").lower()
        assert "owner review candidate" not in text
        assert "working candidate" not in text
        assert "unreleased" not in text
        assert "publication:** not authorized" not in text
        assert "v1.5-rc1" not in text


def test_repository_root_separates_method_site_runtime_and_history() -> None:
    published_root_html = [
        path for path in ROOT.glob("*.html") if not path.name.startswith("design-preview-")
    ]
    assert not published_root_html
    assert not list(ROOT.glob("*.pdf"))
    for directory in (
        "docs",
        "method",
        "practice-kit",
        "gdac",
        "tests",
        "contributing",
        "archive",
    ):
        assert (ROOT / directory).is_dir()

    assert (SITE / "index.html").is_file()
    assert (METHOD / "harness.md").is_file()
    assert (METHOD / "evaluation-rules.md").is_file()
    assert (ROOT / "gdac" / "validation.py").is_file()
    assert (KIT / "examples" / "freeze-review" / "review-result.md").is_file()


def test_current_pages_have_complete_unique_discovery_metadata() -> None:
    titles: set[str] = set()
    canonicals: set[str] = set()

    for filename in CURRENT_SITE_PAGES:
        text = (SITE / filename).read_text(encoding="utf-8")
        title = re.search(r"<title>([^<]+)</title>", text)
        description = re.search(
            r'<meta name="description" content="([^"]+)">', text
        )
        canonical = re.search(r'<link rel="canonical" href="([^"]+)">', text)
        og_url = re.search(r'<meta property="og:url" content="([^"]+)">', text)
        json_ld = re.search(
            r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
            text,
            flags=re.DOTALL,
        )

        assert title and title.group(1) not in titles
        assert description and 50 <= len(description.group(1)) <= 200
        assert canonical and canonical.group(1).startswith(
            "https://qisun2026.github.io/governance-driven-agentic-coding/"
        )
        assert og_url and og_url.group(1) == canonical.group(1)
        assert '<meta property="og:site_name" content="Governance-Driven Agentic Coding">' in text
        assert '<meta name="twitter:card" content="summary">' in text
        assert '<meta name="keywords"' not in text.lower()
        assert json_ld

        structured = json.loads(json_ld.group(1))
        assert structured["@context"] == "https://schema.org"
        assert structured["url"] == canonical.group(1)
        assert structured["creator" if structured["@type"] == "WebSite" else "author"]["name"] == "Qi Sun"

        titles.add(title.group(1))
        canonicals.add(canonical.group(1))

    assert len(titles) == len(CURRENT_SITE_PAGES)
    assert len(canonicals) == len(CURRENT_SITE_PAGES)


def test_public_source_and_download_links_point_to_current_repository_files() -> None:
    repository_prefixes = (
        "https://github.com/QiSun2026/governance-driven-agentic-coding/blob/main/",
        "https://raw.githubusercontent.com/QiSun2026/governance-driven-agentic-coding/main/",
    )

    for filename in CURRENT_SITE_PAGES:
        parser = LinkCollector()
        parser.feed((SITE / filename).read_text(encoding="utf-8"))
        for href in parser.hrefs:
            matching_prefix = next(
                (prefix for prefix in repository_prefixes if href.startswith(prefix)),
                None,
            )
            if not matching_prefix:
                continue
            repository_path = unquote(
                href.removeprefix(matching_prefix).split("#", 1)[0].split("?", 1)[0]
            )
            assert (ROOT / repository_path).is_file(), (
                f"stale repository link in {filename}: {href}"
            )


def test_multilingual_entry_points_use_absolute_reciprocal_hreflang() -> None:
    english = (SITE / "index.html").read_text(encoding="utf-8")
    chinese = (SITE / "zh.html").read_text(encoding="utf-8")
    expected = [
        'hreflang="en" href="https://qisun2026.github.io/governance-driven-agentic-coding/"',
        'hreflang="zh-Hans" href="https://qisun2026.github.io/governance-driven-agentic-coding/zh.html"',
        'hreflang="x-default" href="https://qisun2026.github.io/governance-driven-agentic-coding/"',
    ]
    for value in expected:
        assert value in english
        assert value in chinese


def test_sitemap_and_robots_publish_only_canonical_current_pages() -> None:
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap = ET.parse(SITE / "sitemap.xml")
    listed = {
        element.text
        for element in sitemap.findall("s:url/s:loc", namespace)
        if element.text
    }
    expected = set()
    for filename in CURRENT_SITE_PAGES:
        text = (SITE / filename).read_text(encoding="utf-8")
        canonical = re.search(r'<link rel="canonical" href="([^"]+)">', text)
        assert canonical
        expected.add(canonical.group(1))

    assert listed == expected
    robots = (SITE / "robots.txt").read_text(encoding="utf-8")
    assert "User-agent: *" in robots
    assert "Allow: /" in robots
    assert (
        "Sitemap: https://qisun2026.github.io/governance-driven-agentic-coding/sitemap.xml"
        in robots
    )


def test_github_entry_metadata_is_present_in_repository_files() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    citation_record = yaml.safe_load(citation)

    assert "A governance harness and evaluation protocol" in readme
    assert "https://qisun2026.github.io/governance-driven-agentic-coding/" in readme
    assert "repository-code: \"https://github.com/QiSun2026/governance-driven-agentic-coding\"" in citation
    assert 'version: "2.0"' in citation
    assert "license: CC-BY-4.0" in citation
    assert citation_record["cff-version"] == "1.2.0"
    assert citation_record["title"] == "Governance-Driven Agentic Coding"
    assert citation_record["version"] == "2.0"
    assert citation_record["authors"] == [
        {"family-names": "Sun", "given-names": "Qi"}
    ]


@pytest.mark.parametrize(
    "document",
    [
        ROOT / "README.md",
        METHOD / "harness.md",
        METHOD / "evaluation-rules.md",
        METHOD / "continuity-v1.3.md",
        METHOD / "related-work.md",
        KIT / "README.md",
        ROOT / "archive" / "README.md",
    ],
)
def test_current_markdown_has_no_broken_relative_links(document: Path) -> None:
    text = document.read_text(encoding="utf-8")
    for href in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = urlsplit(href)
        if target.scheme or target.netloc or not target.path:
            continue
        linked = (document.parent / unquote(target.path)).resolve()
        if linked.is_dir():
            continue
        assert linked.is_file(), f"broken link in {document.relative_to(ROOT)}: {href}"
