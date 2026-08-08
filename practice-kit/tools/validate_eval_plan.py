from __future__ import annotations

import argparse
import sys
from pathlib import Path

from jsonschema.exceptions import SchemaError

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from practice_kit_validator import (  # noqa: E402
    load_document,
    validate_contract,
    validate_eval_plan,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a GDAC Eval Plan.")
    parser.add_argument("eval_plan", type=Path)
    parser.add_argument(
        "--schema",
        type=Path,
        default=ROOT / "practice-kit" / "schemas" / "eval-plan.schema.json",
    )
    parser.add_argument(
        "--contract",
        type=Path,
        help="Outcome Contract to bind and cross-validate against the Eval Plan.",
    )
    parser.add_argument(
        "--contract-schema",
        type=Path,
        default=ROOT / "practice-kit" / "schemas" / "outcome-contract.schema.json",
    )
    args = parser.parse_args()

    try:
        plan = load_document(args.eval_plan)
        contract = load_document(args.contract) if args.contract else None
        errors: list[str] = []
        if contract is not None:
            contract_errors = validate_contract(
                contract, load_document(args.contract_schema)
            )
            errors.extend(f"contract: {error}" for error in contract_errors)
        errors.extend(validate_eval_plan(plan, load_document(args.schema), contract))
    except (OSError, ValueError, SchemaError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"INVALID: {error}", file=sys.stderr)
        return 1
    if plan.get("status") == "draft":
        print(f"STRUCTURALLY VALID DRAFT: {args.eval_plan}")
    else:
        print(f"VALID BOUND PLAN: {args.eval_plan}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
