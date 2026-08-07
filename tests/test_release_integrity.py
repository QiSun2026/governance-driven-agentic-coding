from __future__ import annotations

import hashlib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pytest


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
        ROOT / "SHA256SUMS-v1.5-rc1.txt",
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


@pytest.mark.parametrize("filename", ["candidate-v1.5.html", "candidate-v1.5-en.html"])
def test_candidate_html_has_no_broken_local_links_or_ai_dash(filename: str) -> None:
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
        assert linked.is_file(), f"broken link in {filename}: {href}"


@pytest.mark.parametrize(
    "filename",
    [
        "Governance-Driven-Agentic-Coding-v1.5-rc1.pdf",
        "Governance-Driven-Agentic-Coding-EN-v1.5-rc1.pdf",
    ],
)
def test_candidate_pdf_has_pdf_signature(filename: str) -> None:
    path = ROOT / filename
    assert path.stat().st_size > 50_000
    assert path.read_bytes()[:5] == b"%PDF-"


def test_public_boundaries_cover_release_review_findings() -> None:
    related_work = (ROOT / "RELATED_WORK.md").read_text(encoding="utf-8")
    review_result = (ROOT / "examples/freeze-review/review-result.md").read_text(
        encoding="utf-8"
    )

    for required_reference in ("SR 26-2", "EU AI Act", "Inspect", "AGENTS.md"):
        assert required_reference in related_work
    assert "two author-run private projects" in related_work
    assert "No real defect was caught in this example" in review_result
