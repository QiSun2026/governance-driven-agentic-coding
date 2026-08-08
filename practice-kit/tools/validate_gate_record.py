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
    validate_gate_record,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a GDAC Gate Record and derive its Harness Gate."
    )
    parser.add_argument("gate_record", type=Path)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--eval-plan", type=Path, required=True)
    parser.add_argument(
        "--schema",
        type=Path,
        default=ROOT / "practice-kit" / "schemas" / "gate-record.schema.json",
    )
    parser.add_argument(
        "--contract-schema",
        type=Path,
        default=ROOT / "practice-kit" / "schemas" / "outcome-contract.schema.json",
    )
    parser.add_argument(
        "--eval-plan-schema",
        type=Path,
        default=ROOT / "practice-kit" / "schemas" / "eval-plan.schema.json",
    )
    args = parser.parse_args()

    try:
        contract = load_document(args.contract)
        plan = load_document(args.eval_plan)
        record = load_document(args.gate_record)
        errors = [
            *(f"contract: {error}" for error in validate_contract(
                contract, load_document(args.contract_schema)
            )),
            *(f"eval_plan: {error}" for error in validate_eval_plan(
                plan, load_document(args.eval_plan_schema), contract
            )),
            *validate_gate_record(
                record,
                load_document(args.schema),
                contract,
                plan,
                base_dir=args.gate_record.resolve().parent,
            ),
        ]
    except (OSError, ValueError, SchemaError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"INVALID: {error}", file=sys.stderr)
        return 1
    print(
        f"VALID GATE RECORD ({record['harness_gate']['state']}): {args.gate_record}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
