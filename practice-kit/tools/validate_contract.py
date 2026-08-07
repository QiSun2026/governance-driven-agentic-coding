from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from practice_kit_validator import load_document, validate_contract  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a GDAC Outcome Contract.")
    parser.add_argument("contract", type=Path)
    parser.add_argument(
        "--schema",
        type=Path,
        default=ROOT / "practice-kit" / "schemas" / "outcome-contract.schema.json",
    )
    args = parser.parse_args()

    try:
        errors = validate_contract(load_document(args.contract), load_document(args.schema))
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"INVALID: {error}", file=sys.stderr)
        return 1
    print(f"VALID: {args.contract}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
