from __future__ import annotations

import copy
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from gdac.validation import canonical_digest, load_document, validate_eval_plan


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "practice-kit" / "schemas" / "eval-plan.schema.json"
EXAMPLE = ROOT / "practice-kit" / "examples" / "eval-plan.example.yaml"
CONTRACT = ROOT / "practice-kit" / "examples" / "dry-run-outcome-contract.example.yaml"
TEMPLATE = ROOT / "practice-kit" / "templates" / "eval-plan.yaml"
CLI = ROOT / "practice-kit" / "tools" / "validate_eval_plan.py"


@pytest.fixture()
def valid_plan() -> dict[str, object]:
    return load_document(EXAMPLE)


@pytest.fixture()
def valid_contract() -> dict[str, object]:
    return load_document(CONTRACT)


def validate(
    plan: dict[str, object], contract: dict[str, object] | None = None
) -> list[str]:
    return validate_eval_plan(plan, load_document(SCHEMA), contract)


def rebind(plan: dict[str, object], contract: dict[str, object]) -> None:
    plan["contract_ref"]["contract_id"] = contract["contract_id"]  # type: ignore[index]
    plan["contract_ref"]["revision"] = contract["revision"]  # type: ignore[index]
    plan["contract_ref"]["sha256"] = canonical_digest(contract)  # type: ignore[index]
    plan["risk_tier"] = contract["risk_tier"]
    plan["risk_overlays"] = copy.deepcopy(contract["risk_overlays"])


def test_filled_eval_plan_matches_schema_and_contract(
    valid_plan: dict[str, object], valid_contract: dict[str, object]
) -> None:
    assert validate(valid_plan, valid_contract) == []


def test_frozen_plan_requires_contract(valid_plan: dict[str, object]) -> None:
    assert "frozen Eval Plan requires --contract for canonical binding validation" in validate(valid_plan)


def test_draft_template_is_structurally_valid() -> None:
    template = yaml.safe_load(TEMPLATE.read_text(encoding="utf-8"))

    assert validate(template) == []
    assert template["reporting"]["retain_evidence_references"] is True
    assert template["reporting"]["retain_all_attempts"] is True


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("contract_id", "other-contract", "contract_ref.contract_id does not match Outcome Contract"),
        ("revision", 999, "contract_ref.revision does not match Outcome Contract"),
        ("sha256", "0" * 64, "contract_ref.sha256 does not match canonical Outcome Contract digest"),
    ],
)
def test_contract_binding_rejects_identifier_or_digest_drift(
    valid_plan: dict[str, object],
    valid_contract: dict[str, object],
    field: str,
    value: object,
    message: str,
) -> None:
    candidate = copy.deepcopy(valid_plan)
    candidate["contract_ref"][field] = value  # type: ignore[index]

    assert message in validate(candidate, valid_contract)


def test_changed_contract_invalidates_frozen_plan(
    valid_plan: dict[str, object], valid_contract: dict[str, object]
) -> None:
    contract = copy.deepcopy(valid_contract)
    contract["budget"]["max_build_retries"] = 3  # type: ignore[index]

    assert "contract_ref.sha256 does not match canonical Outcome Contract digest" in validate(valid_plan, contract)


def test_material_contract_criterion_cannot_be_removed_from_plan(
    valid_plan: dict[str, object], valid_contract: dict[str, object]
) -> None:
    candidate = copy.deepcopy(valid_plan)
    candidate["claims"].pop()  # type: ignore[union-attr]

    assert any("has no material Eval Plan claim" in error for error in validate(candidate, valid_contract))


def test_owner_decision_fields_are_rejected(valid_plan: dict[str, object]) -> None:
    candidate = copy.deepcopy(valid_plan)
    candidate["owner_disposition"] = {"decision": "accept"}

    assert any("owner_disposition" in error for error in validate(candidate))


def test_unknown_claim_and_risk_references_are_rejected(
    valid_plan: dict[str, object], valid_contract: dict[str, object]
) -> None:
    candidate = copy.deepcopy(valid_plan)
    candidate["evals"][0]["claim_ids"] = ["unknown-claim"]  # type: ignore[index]
    candidate["evals"][0]["risk_ids"] = ["unknown-risk"]  # type: ignore[index]

    errors = validate(candidate, valid_contract)
    assert any("unknown claim_id 'unknown-claim'" in error for error in errors)
    assert any("unknown risk_id 'unknown-risk'" in error for error in errors)


def test_material_claim_requires_blocking_eval(
    valid_plan: dict[str, object], valid_contract: dict[str, object]
) -> None:
    candidate = copy.deepcopy(valid_plan)
    for eval_item in candidate["evals"]:  # type: ignore[union-attr]
        if "preview-accurate" in eval_item["claim_ids"]:
            eval_item["blocking"] = False

    assert any("material claim 'preview-accurate' has no blocking eval" in error for error in validate(candidate, valid_contract))


def test_context_separation_requires_distinct_context_and_read_only_grader(
    valid_plan: dict[str, object], valid_contract: dict[str, object]
) -> None:
    contract = copy.deepcopy(valid_contract)
    roles = contract["authority"]["roles"]  # type: ignore[index]
    roles[1]["context_ref"] = roles[0]["context_ref"]
    roles[1]["can_write"] = ["src"]
    rebind(valid_plan, contract)

    assert any("context separation is not established" in error for error in validate(valid_plan, contract))


def test_party_separation_requires_distinct_principal(
    valid_plan: dict[str, object], valid_contract: dict[str, object]
) -> None:
    candidate = copy.deepcopy(valid_plan)
    contract = copy.deepcopy(valid_contract)
    candidate["evals"][0]["producer_constraints"]["separation_requirement"] = "party"  # type: ignore[index]
    contract["authority"]["roles"][1]["principal_id"] = contract["authority"]["roles"][0]["principal_id"]  # type: ignore[index]
    rebind(candidate, contract)

    assert any("party separation is not established" in error for error in validate(candidate, contract))


def test_risk_eval_must_bind_material_risk(
    valid_plan: dict[str, object], valid_contract: dict[str, object]
) -> None:
    candidate = copy.deepcopy(valid_plan)
    contract = copy.deepcopy(valid_contract)
    for risk in contract["risks"]:  # type: ignore[union-attr]
        if risk["risk_id"] == "authority-expansion":
            risk["material"] = False
    rebind(candidate, contract)

    assert any("governance eval must bind a material" in error for error in validate(candidate, contract))


def test_plan_cannot_exceed_rerun_or_trial_budget(
    valid_plan: dict[str, object], valid_contract: dict[str, object]
) -> None:
    candidate = copy.deepcopy(valid_plan)
    candidate["evals"][0]["max_evaluator_reruns"] = 3  # type: ignore[index]
    candidate["evals"][0]["trial_policy"] = {  # type: ignore[index]
        "kind": "pass-at-k",
        "k": 5,
        "retain_all_trials": True,
        "independence_rule": "Fresh fixture and process for each trial.",
        "selection_rule": "all-declared-trials-count",
    }

    errors = validate(candidate, valid_contract)
    assert any("planned evaluator reruns" in error for error in errors)
    assert any("planned trials" in error for error in errors)


@pytest.mark.parametrize(
    ("grader_type", "evidence_type"),
    [("deterministic", "deterministic_test"), ("rule", "rule_check")],
)
def test_grader_type_requires_matching_evidence(
    valid_plan: dict[str, object],
    valid_contract: dict[str, object],
    grader_type: str,
    evidence_type: str,
) -> None:
    candidate = copy.deepcopy(valid_plan)
    candidate["evals"][0]["grader"]["type"] = grader_type  # type: ignore[index]
    candidate["evals"][0]["required_evidence"] = ["log"]  # type: ignore[index]

    assert any(f"{grader_type} grader requires {evidence_type}" in error for error in validate(candidate, valid_contract))


def test_model_grader_needs_calibration_and_cannot_be_sole_material_gate(
    valid_plan: dict[str, object], valid_contract: dict[str, object]
) -> None:
    candidate = copy.deepcopy(valid_plan)
    for eval_item in candidate["evals"]:  # type: ignore[union-attr]
        if "preview-accurate" in eval_item["claim_ids"]:
            eval_item["grader"] = {
                "type": "model",
                "name": "model-judge",
                "configuration_ref": "graders/model-v1",
                "calibration_ref": None,
                "qualification_ref": None,
            }
            eval_item["required_evidence"] = ["model_grade"]

    errors = validate(candidate, valid_contract)
    assert any("model grader requires calibration_ref" in error for error in errors)
    assert any("cannot rely only on a model grader" in error for error in errors)


def test_declared_baseline_requires_regression_eval(
    valid_plan: dict[str, object], valid_contract: dict[str, object]
) -> None:
    candidate = copy.deepcopy(valid_plan)
    candidate["evals"] = [item for item in candidate["evals"] if item["eval_class"] != "regression"]  # type: ignore[index]

    assert "declared baseline requires a regression eval bound to a material target" in validate(candidate, valid_contract)


def test_high_tier_requires_adversarial_eval(
    valid_plan: dict[str, object], valid_contract: dict[str, object]
) -> None:
    candidate = copy.deepcopy(valid_plan)
    contract = copy.deepcopy(valid_contract)
    contract["risk_tier"] = "high"
    candidate["risk_tier"] = "high"
    candidate["evals"] = [item for item in candidate["evals"] if item["eval_class"] != "adversarial"]  # type: ignore[index]
    rebind(candidate, contract)

    assert "risk profile 'high' requires an adversarial eval bound to a material risk" in validate(candidate, contract)


def test_overlay_requirements_are_separate_from_risk_tier(
    valid_plan: dict[str, object], valid_contract: dict[str, object]
) -> None:
    candidate = copy.deepcopy(valid_plan)
    contract = copy.deepcopy(valid_contract)
    contract["risk_overlays"] = ["security"]
    candidate["risk_overlays"] = ["security"]
    rebind(candidate, contract)

    assert "security overlay requires a security eval bound to a material risk" in validate(candidate, contract)


def test_blocking_control_eval_cannot_use_pass_at_k(
    valid_plan: dict[str, object], valid_contract: dict[str, object]
) -> None:
    candidate = copy.deepcopy(valid_plan)
    governance = next(item for item in candidate["evals"] if item["eval_class"] == "governance")  # type: ignore[index]
    governance["trial_policy"] = {
        "kind": "pass-at-k",
        "k": 2,
        "retain_all_trials": True,
        "independence_rule": "Fresh context for every declared trial.",
        "selection_rule": "all-declared-trials-count",
    }

    assert any("blocking governance eval cannot use repeated-trial" in error for error in validate(candidate, valid_contract))


def test_cli_cross_validates_contract() -> None:
    result = subprocess.run(
        [sys.executable, str(CLI), str(EXAMPLE), "--contract", str(CONTRACT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "VALID BOUND PLAN:" in result.stdout
