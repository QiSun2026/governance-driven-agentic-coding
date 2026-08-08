from __future__ import annotations

from pathlib import Path


def cleanup(root: Path, *, dry_run: bool) -> list[str]:
    """Return the selected paths and delete them only outside dry-run mode."""
    targets = sorted(path for path in root.rglob("*.tmp") if path.is_file())
    relative = [path.relative_to(root).as_posix() for path in targets]
    if not dry_run:
        for path in targets:
            path.unlink()
    return relative
