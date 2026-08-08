from __future__ import annotations

import copy
import subprocess
import sys
from pathlib import Path

import pytest

from practice_kit_validator import derive_harness_gate, load_document, validate_gate_record


ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "practice-kit" / "examples" / "golden-dry-run"
RECORD = CASE / "gate-record.example.yaml"
SCHEMA = ROOT / "practice-kit" / "schemas" / "gate-record.schema.json"
CONTRACT = ROOT / "practice-kit" / "examples" / "dry-run-outcome-contract.example.yaml"
PLAN = ROOT / "practice-kit" / "examples" / "eval-plan.example.yaml"
CLI = ROOT / "practice-kit" / "tools" / "validate_gate_record.py"


@pytest.fixture()
def valid_record() -> dict[str, object]:
    return load_document(RECORD)


@pytest.fixture()
def contract() -> dict[str, object]:
    return load_document(CONTRACT)


@pytest.fixture()
def plan() -> dict[str, object]:
    return load_document(PLAN)


def validate(
    record: dict[str, object], contract: dict[str, object], plan: dict[str, object]
) -> list[str]:
    return validate_gate_record(record, load_document(SCHEMA), contract, plan, CASE)


def test_golden_record_chain_is_valid(
    valid_record: dict[str, object], contract: dict[str, object], plan: dict[str, object]
) -> None:
    assert validate(valid_record, contract, plan) == []
    assert derive_harness_gate(valid_record, plan) == "ready"
    assert valid_record["owner_disposition"]["decision"] == "pending"  # type: ignore[index]


def test_failed_attempt_is_retained(valid_record: dict[str, object]) -> None:
    assert any(item["outcome"] == "rejected" for item in valid_record["attempts"])  # type: ignore[index]


@pytest.mark.parametrize("status", ["fail", "insufficient_evidence", "not_evaluated"])
def test_non_pass_blocking_result_blocks_gate(
    valid_record: dict[str, object], plan: dict[str, object], status: str
) -> None:
    candidate = copy.deepcopy(valid_record)
    candidate["eval_results"][0]["status"] = status  # type: ignore[index]
    if status == "not_evaluated":
        candidate["eval_results"][0]["trial_count"] = 0  # type: ignore[index]

    assert derive_harness_gate(candidate, plan) == "blocked"


def test_gate_state_must_match_deterministic_derivation(
    valid_record: dict[str, object], contract: dict[str, object], plan: dict[str, object]
) -> None:
    candidate = copy.deepcopy(valid_record)
    candidate["eval_results"][0]["status"] = "fail"  # type: ignore[index]

    assert "harness_gate.state must be derived as 'blocked'" in validate(candidate, contract, plan)


def test_unresolved_contradiction_is_insufficient_evidence(
    valid_record: dict[str, object], contract: dict[str, object], plan: dict[str, object]
) -> None:
    candidate = copy.deepcopy(valid_record)
    result = candidate["eval_results"][0]  # type: ignore[index]
    result["contradiction_refs"] = ["write-trace-conflict"]
    result["conflict_status"] = "unresolved"

    errors = validate(candidate, contract, plan)
    assert any("unresolved contradiction must be insufficient_evidence" in error for error in errors)
    assert any("derived as 'blocked'" in error for error in errors)


def test_pass_requires_every_declared_evidence_type(
    valid_record: dict[str, object], contract: dict[str, object], plan: dict[str, object]
) -> None:
    candidate = copy.deepcopy(valid_record)
    candidate["eval_results"][0]["evidence_ids"] = ["pytest-result"]  # type: ignore[index]

    assert any("pass is missing required evidence types: log" in error for error in validate(candidate, contract, plan))


def test_candidate_binding_applies_to_every_result(
    valid_record: dict[str, object], contract: dict[str, object], plan: dict[str, object]
) -> None:
    candidate = copy.deepcopy(valid_record)
    candidate["eval_results"][0]["candidate_ref"] = "different-candidate"  # type: ignore[index]

    assert any("candidate_ref does not match Candidate Binding" in error for error in validate(candidate, contract, plan))


def test_invalidated_pass_is_rejected(
    valid_record: dict[str, object], contract: dict[str, object], plan: dict[str, object]
) -> None:
    candidate = copy.deepcopy(valid_record)
    candidate["eval_results"][0]["invalidated"] = True  # type: ignore[index]

    errors = validate(candidate, contract, plan)
    assert any("invalidated result cannot pass" in error for error in errors)
    assert any("derived as 'blocked'" in error for error in errors)


def test_owner_cannot_accept_a_blocked_gate(
    valid_record: dict[str, object], contract: dict[str, object], plan: dict[str, object]
) -> None:
    candidate = copy.deepcopy(valid_record)
    candidate["eval_results"][0]["status"] = "fail"  # type: ignore[index]
    candidate["harness_gate"]["state"] = "blocked"  # type: ignore[index]
    candidate["owner_disposition"] = {  # type: ignore[index]
        "decision": "accept",
        "owner_id": "Repository Owner",
        "decision_ref": "owner-decision-1",
        "conditions": [],
    }

    assert "blocked Harness Gate cannot have an accepting Owner disposition" in validate(candidate, contract, plan)


def test_open_material_finding_blocks_gate(
    valid_record: dict[str, object], plan: dict[str, object]
) -> None:
    candidate = copy.deepcopy(valid_record)
    candidate["findings"][0]["material"] = True  # type: ignore[index]
    candidate["findings"][0]["status"] = "open"  # type: ignore[index]

    assert derive_harness_gate(candidate, plan) == "blocked"


def test_artifact_digest_is_verified(
    valid_record: dict[str, object], contract: dict[str, object], plan: dict[str, object]
) -> None:
    candidate = copy.deepcopy(valid_record)
    candidate["evidence"][0]["sha256"] = "0" * 64  # type: ignore[index]

    assert any("sha256 does not match 'pytest-result.txt'" in error for error in validate(candidate, contract, plan))


def test_cli_validates_complete_chain() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(CLI),
            str(RECORD),
            "--contract",
            str(CONTRACT),
            "--eval-plan",
            str(PLAN),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "VALID GATE RECORD (ready):" in result.stdout
