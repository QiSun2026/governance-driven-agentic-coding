from __future__ import annotations

from pathlib import Path

from candidate import cleanup


def _fixture(root: Path) -> None:
    (root / "nested").mkdir(parents=True)
    (root / "keep.txt").write_text("keep", encoding="utf-8")
    (root / "one.tmp").write_text("one", encoding="utf-8")
    (root / "nested" / ".hidden.tmp").write_text("hidden", encoding="utf-8")


def _snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_dry_run_attempts_no_application_write(tmp_path: Path, monkeypatch) -> None:
    _fixture(tmp_path)
    before = _snapshot(tmp_path)
    unlink_calls: list[str] = []
    original_unlink = Path.unlink

    def record_unlink(path: Path, *args, **kwargs) -> None:
        unlink_calls.append(path.relative_to(tmp_path).as_posix())
        original_unlink(path, *args, **kwargs)

    monkeypatch.setattr(Path, "unlink", record_unlink)
    preview = cleanup(tmp_path, dry_run=True)

    assert preview == ["nested/.hidden.tmp", "one.tmp"]
    assert unlink_calls == []
    assert _snapshot(tmp_path) == before


def test_preview_matches_normal_execution_on_equivalent_fixture(tmp_path: Path) -> None:
    preview_root = tmp_path / "preview"
    execute_root = tmp_path / "execute"
    _fixture(preview_root)
    _fixture(execute_root)

    preview = cleanup(preview_root, dry_run=True)
    removed = cleanup(execute_root, dry_run=False)

    assert preview == removed
    assert _snapshot(preview_root) == {
        "keep.txt": b"keep",
        "nested/.hidden.tmp": b"hidden",
        "one.tmp": b"one",
    }
    assert _snapshot(execute_root) == {"keep.txt": b"keep"}
