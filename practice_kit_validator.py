from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


def load_document(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        data = json.loads(text) if path.suffix.lower() == ".json" else yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise ValueError(f"{path}: invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a mapping at the document root")
    return data


def validate_contract(contract: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    errors = []
    for issue in sorted(validator.iter_errors(contract), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in issue.absolute_path) or "$"
        errors.append(f"{location}: {issue.message}")

    criteria_data = contract.get("acceptance_criteria", [])
    claims_data = contract.get("evidence_requirements", [])
    criteria_items = criteria_data if isinstance(criteria_data, list) else []
    claim_items = claims_data if isinstance(claims_data, list) else []
    criteria = [item.get("criterion_id") for item in criteria_items if isinstance(item, dict)]
    claims = [item.get("claim_id") for item in claim_items if isinstance(item, dict)]
    for claim_id in claims:
        if claim_id not in criteria:
            errors.append(f"evidence_requirements: unknown claim_id {claim_id!r}")
    if len(criteria) != len(set(criteria)):
        errors.append("acceptance_criteria: criterion_id values must be unique")

    return errors
