from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from gdac.validation import load_document, validate_contract


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "practice-kit" / "schemas" / "outcome-contract.schema.json"
EXAMPLE = ROOT / "practice-kit" / "examples" / "outcome-contract.example.yaml"


@pytest.fixture()
def valid_contract() -> dict[str, object]:
    return yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))


def validate(contract: dict[str, object]) -> list[str]:
    return validate_contract(contract, load_document(SCHEMA))


def test_filled_example_matches_schema(valid_contract: dict[str, object]) -> None:
    assert validate(valid_contract) == []


def test_missing_owner_is_rejected(valid_contract: dict[str, object]) -> None:
    candidate = copy.deepcopy(valid_contract)
    del candidate["authority"]["owner"]  # type: ignore[index]

    assert any("authority" in error and "owner" in error for error in validate(candidate))


@pytest.mark.parametrize("grader", ["owner", "vibes"])
def test_owner_or_unknown_grader_is_rejected(
    valid_contract: dict[str, object], grader: str
) -> None:
    candidate = copy.deepcopy(valid_contract)
    candidate["acceptance_criteria"][0]["grader"] = grader  # type: ignore[index]

    assert any("acceptance_criteria.0.grader" in error for error in validate(candidate))


def test_owner_acceptance_is_not_a_technical_outcome_field(
    valid_contract: dict[str, object],
) -> None:
    candidate = copy.deepcopy(valid_contract)
    candidate["outcome"]["accepted_by"] = "builder"  # type: ignore[index]

    assert any("accepted_by" in error for error in validate(candidate))


def test_unknown_field_is_rejected(valid_contract: dict[str, object]) -> None:
    candidate = copy.deepcopy(valid_contract)
    candidate["self_authorized"] = True

    assert any("self_authorized" in error for error in validate(candidate))


def test_evidence_must_reference_a_declared_criterion(
    valid_contract: dict[str, object],
) -> None:
    candidate = copy.deepcopy(valid_contract)
    candidate["evidence_requirements"][0]["claim_id"] = "undeclared"  # type: ignore[index]

    assert any("unknown claim_id 'undeclared'" in error for error in validate(candidate))


def test_every_criterion_requires_evidence(valid_contract: dict[str, object]) -> None:
    candidate = copy.deepcopy(valid_contract)
    candidate["evidence_requirements"].pop()  # type: ignore[union-attr]

    assert any("has no evidence requirement" in error for error in validate(candidate))


@pytest.mark.parametrize(
    ("collection", "id_field", "message"),
    [
        ("evidence_requirements", "claim_id", "evidence_requirements: claim_id values must be unique"),
        ("risks", "risk_id", "risks: risk_id values must be unique"),
    ],
)
def test_ids_must_be_unique(
    valid_contract: dict[str, object], collection: str, id_field: str, message: str
) -> None:
    candidate = copy.deepcopy(valid_contract)
    candidate[collection].append(copy.deepcopy(candidate[collection][0]))  # type: ignore[index,union-attr]

    assert message in validate(candidate)


def test_role_ids_must_be_unique(valid_contract: dict[str, object]) -> None:
    candidate = copy.deepcopy(valid_contract)
    candidate["authority"]["roles"].append(  # type: ignore[index]
        copy.deepcopy(candidate["authority"]["roles"][0])  # type: ignore[index]
    )

    assert "authority.roles: role_id values must be unique" in validate(candidate)


def test_evidence_types_must_be_unique(valid_contract: dict[str, object]) -> None:
    candidate = copy.deepcopy(valid_contract)
    required = candidate["evidence_requirements"][0]["required_types"]  # type: ignore[index]
    required.append(required[0])

    assert any("required_types" in error and "non-unique" in error for error in validate(candidate))


def test_principal_and_context_are_required(valid_contract: dict[str, object]) -> None:
    candidate = copy.deepcopy(valid_contract)
    del candidate["authority"]["roles"][0]["principal_id"]  # type: ignore[index]
    del candidate["authority"]["roles"][1]["context_ref"]  # type: ignore[index]

    errors = validate(candidate)
    assert any("principal_id" in error for error in errors)
    assert any("context_ref" in error for error in errors)


def test_invalid_json_names_the_document(tmp_path: Path) -> None:
    invalid = tmp_path / "invalid.json"
    invalid.write_text('{"broken":', encoding="utf-8")

    with pytest.raises(ValueError, match=r"invalid\.json: invalid JSON"):
        load_document(invalid)


def test_malformed_criteria_shape_is_reported_not_crashed(
    valid_contract: dict[str, object],
) -> None:
    candidate = copy.deepcopy(valid_contract)
    candidate["acceptance_criteria"] = [{"criterion_id": {"not": "a string"}}]

    assert any("acceptance_criteria" in error for error in validate(candidate))
