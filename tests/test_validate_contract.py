from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from practice_kit_validator import load_document, validate_contract


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "practice-kit" / "schemas" / "outcome-contract.schema.json"
EXAMPLE = ROOT / "practice-kit" / "examples" / "outcome-contract.example.yaml"


@pytest.fixture()
def valid_contract() -> dict[str, object]:
    return yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))


def test_filled_example_matches_schema(valid_contract: dict[str, object]) -> None:
    assert validate_contract(valid_contract, load_document(SCHEMA)) == []


def test_missing_owner_is_rejected(valid_contract: dict[str, object]) -> None:
    candidate = copy.deepcopy(valid_contract)
    del candidate["authority"]["owner"]  # type: ignore[index]

    errors = validate_contract(candidate, load_document(SCHEMA))

    assert any("authority" in error and "owner" in error for error in errors)


def test_unknown_grader_is_rejected(valid_contract: dict[str, object]) -> None:
    candidate = copy.deepcopy(valid_contract)
    candidate["acceptance_criteria"][0]["grader"] = "vibes"  # type: ignore[index]

    errors = validate_contract(candidate, load_document(SCHEMA))

    assert any("acceptance_criteria.0.grader" in error for error in errors)


def test_unknown_field_is_rejected(valid_contract: dict[str, object]) -> None:
    candidate = copy.deepcopy(valid_contract)
    candidate["self_authorized"] = True

    errors = validate_contract(candidate, load_document(SCHEMA))

    assert any("self_authorized" in error for error in errors)


def test_evidence_must_reference_a_declared_criterion(valid_contract: dict[str, object]) -> None:
    candidate = copy.deepcopy(valid_contract)
    candidate["evidence_requirements"][0]["claim_id"] = "undeclared"  # type: ignore[index]

    errors = validate_contract(candidate, load_document(SCHEMA))

    assert any("unknown claim_id 'undeclared'" in error for error in errors)


def test_malformed_criteria_shape_is_reported_not_crashed(
    valid_contract: dict[str, object],
) -> None:
    candidate = copy.deepcopy(valid_contract)
    candidate["acceptance_criteria"] = "not-a-list"

    errors = validate_contract(candidate, load_document(SCHEMA))

    assert any("acceptance_criteria" in error for error in errors)
