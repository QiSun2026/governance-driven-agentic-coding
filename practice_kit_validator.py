from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


EVIDENCE_BY_GRADER = {
    "deterministic": "deterministic_test",
    "rule": "rule_check",
    "model": "model_grade",
    "human": "human_review",
}
EVIDENCE_BY_CLASS = {
    "regression": "regression_test",
    "adversarial": "adversarial_result",
    "security": "security_check",
    "privacy": "privacy_check",
}
RISK_EVAL_CLASSES = {"adversarial", "security", "privacy", "governance"}
REPEATED_TRIAL_PROHIBITED_CLASSES = {
    "regression",
    "adversarial",
    "security",
    "privacy",
    "governance",
}


def load_document(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        data = json.loads(text) if path.suffix.lower() == ".json" else yaml.safe_load(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON: {exc}") from exc
    except yaml.YAMLError as exc:
        raise ValueError(f"{path}: invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a mapping at the document root")
    return data


def canonical_digest(document: dict[str, Any]) -> str:
    """Return a stable digest of the parsed document, independent of YAML layout."""
    payload = json.dumps(
        document,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _schema_errors(document: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    errors = []
    for issue in sorted(validator.iter_errors(document), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in issue.absolute_path) or "$"
        errors.append(f"{location}: {issue.message}")
    return errors


def _items(document: dict[str, Any], key: str) -> list[Any]:
    value = document.get(key, [])
    return value if isinstance(value, list) else []


def _string_ids(items: list[Any], key: str) -> list[str]:
    return [
        value
        for item in items
        if isinstance(item, dict) and isinstance((value := item.get(key)), str)
    ]


def _duplicate_error(items: list[Any], key: str, location: str) -> list[str]:
    values = _string_ids(items, key)
    return [f"{location}: {key} values must be unique"] if len(values) != len(set(values)) else []


def _contract_roles(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    authority = contract.get("authority")
    authority = authority if isinstance(authority, dict) else {}
    roles = authority.get("roles", [])
    roles = roles if isinstance(roles, list) else []
    return {
        role["role_id"]: role
        for role in roles
        if isinstance(role, dict) and isinstance(role.get("role_id"), str)
    }


def validate_contract(contract: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors = _schema_errors(contract, schema)
    criteria = _items(contract, "acceptance_criteria")
    requirements = _items(contract, "evidence_requirements")
    risks = _items(contract, "risks")
    authority = contract.get("authority")
    authority = authority if isinstance(authority, dict) else {}
    roles_data = authority.get("roles", [])
    roles = roles_data if isinstance(roles_data, list) else []

    errors.extend(_duplicate_error(criteria, "criterion_id", "acceptance_criteria"))
    errors.extend(_duplicate_error(requirements, "claim_id", "evidence_requirements"))
    errors.extend(_duplicate_error(risks, "risk_id", "risks"))
    errors.extend(_duplicate_error(roles, "role_id", "authority.roles"))

    criterion_ids = set(_string_ids(criteria, "criterion_id"))
    claim_ids = set(_string_ids(requirements, "claim_id"))
    for claim_id in sorted(claim_ids - criterion_ids):
        errors.append(f"evidence_requirements: unknown claim_id {claim_id!r}")
    for criterion_id in sorted(criterion_ids - claim_ids):
        errors.append(
            f"acceptance_criteria: criterion_id {criterion_id!r} has no evidence requirement"
        )

    return errors


def _material_targets(
    eval_item: dict[str, Any],
    claims_by_id: dict[str, dict[str, Any]],
    risks_by_id: dict[str, dict[str, Any]],
) -> bool:
    claim_ids = eval_item.get("claim_ids", [])
    risk_ids = eval_item.get("risk_ids", [])
    claim_ids = claim_ids if isinstance(claim_ids, list) else []
    risk_ids = risk_ids if isinstance(risk_ids, list) else []
    return any(
        isinstance(claim_id, str)
        and claims_by_id.get(claim_id, {}).get("material") is True
        for claim_id in claim_ids
    ) or any(
        isinstance(risk_id, str)
        and risks_by_id.get(risk_id, {}).get("material") is True
        for risk_id in risk_ids
    )


def _separation_is_valid(
    constraints: dict[str, Any], roles: dict[str, dict[str, Any]]
) -> bool:
    producer_role = constraints.get("producer_role")
    producer = roles.get(producer_role) if isinstance(producer_role, str) else None
    allowed = constraints.get("allowed_grader_roles", [])
    allowed = allowed if isinstance(allowed, list) else []
    separation = constraints.get("separation_requirement")
    if not isinstance(producer, dict) or separation not in {"context", "party"}:
        return False
    for role_id in allowed:
        grader = roles.get(role_id) if isinstance(role_id, str) else None
        if not isinstance(grader, dict) or grader.get("can_write") != []:
            continue
        context_separated = grader.get("context_ref") != producer.get("context_ref")
        party_separated = grader.get("principal_id") != producer.get("principal_id")
        if separation == "context" and context_separated:
            return True
        if separation == "party" and context_separated and party_separated:
            return True
    return False


def _validate_contract_binding(
    plan: dict[str, Any], contract: dict[str, Any], evals: list[Any]
) -> list[str]:
    errors: list[str] = []
    contract_ref = plan.get("contract_ref")
    contract_ref = contract_ref if isinstance(contract_ref, dict) else {}
    if contract_ref.get("contract_id") != contract.get("contract_id"):
        errors.append("contract_ref.contract_id does not match Outcome Contract")
    if contract_ref.get("revision") != contract.get("revision"):
        errors.append("contract_ref.revision does not match Outcome Contract")
    if contract_ref.get("sha256") != canonical_digest(contract):
        errors.append("contract_ref.sha256 does not match canonical Outcome Contract digest")
    if plan.get("risk_tier") != contract.get("risk_tier"):
        errors.append("risk_tier does not match Outcome Contract")
    if plan.get("risk_overlays") != contract.get("risk_overlays"):
        errors.append("risk_overlays do not match Outcome Contract")
    if plan.get("status") == "frozen" and contract.get("status") != "frozen":
        errors.append("frozen Eval Plan requires a frozen Outcome Contract")

    plan_claims = _items(plan, "claims")
    claims_by_id = {
        claim["claim_id"]: claim
        for claim in plan_claims
        if isinstance(claim, dict) and isinstance(claim.get("claim_id"), str)
    }
    criteria = _items(contract, "acceptance_criteria")
    criteria_by_id = {
        criterion["criterion_id"]: criterion
        for criterion in criteria
        if isinstance(criterion, dict) and isinstance(criterion.get("criterion_id"), str)
    }
    risks = _items(contract, "risks")
    risk_ids = set(_string_ids(risks, "risk_id"))
    roles = _contract_roles(contract)

    blocking_by_claim: dict[str, list[dict[str, Any]]] = {}
    for index, eval_item in enumerate(evals):
        if not isinstance(eval_item, dict):
            continue
        constraints = eval_item.get("producer_constraints")
        constraints = constraints if isinstance(constraints, dict) else {}
        role_fields = {
            "producer_role": [constraints.get("producer_role")],
            "allowed_grader_roles": constraints.get("allowed_grader_roles", []),
            "prohibited_grader_roles": constraints.get("prohibited_grader_roles", []),
        }
        for field, values in role_fields.items():
            values = values if isinstance(values, list) else []
            for role_id in values:
                if isinstance(role_id, str) and role_id not in roles:
                    errors.append(
                        f"evals.{index}.{field}: role {role_id!r} is not declared in Outcome Contract authority"
                    )

        for risk_id in eval_item.get("risk_ids", []) if isinstance(eval_item.get("risk_ids"), list) else []:
            if isinstance(risk_id, str) and risk_id not in risk_ids:
                errors.append(f"evals.{index}: unknown risk_id {risk_id!r}")

        if eval_item.get("blocking") is True:
            claim_refs = eval_item.get("claim_ids", [])
            claim_refs = claim_refs if isinstance(claim_refs, list) else []
            for claim_id in claim_refs:
                if isinstance(claim_id, str):
                    blocking_by_claim.setdefault(claim_id, []).append(eval_item)

    requirements = _items(contract, "evidence_requirements")
    evidence_by_claim = {
        requirement["claim_id"]: requirement
        for requirement in requirements
        if isinstance(requirement, dict) and isinstance(requirement.get("claim_id"), str)
    }
    for criterion_id, criterion in criteria_by_id.items():
        plan_claim = claims_by_id.get(criterion_id)
        if not isinstance(plan_claim, dict) or plan_claim.get("material") is not True:
            errors.append(
                f"Outcome Contract criterion {criterion_id!r} has no material Eval Plan claim"
            )
            continue
        if plan_claim.get("statement") != criterion.get("description"):
            errors.append(f"claim {criterion_id!r} statement differs from Outcome Contract")

        blocking_evals = blocking_by_claim.get(criterion_id, [])
        contract_grader = criterion.get("grader")
        if not any(
            isinstance(eval_item.get("grader"), dict)
            and eval_item["grader"].get("type") == contract_grader
            for eval_item in blocking_evals
        ):
            errors.append(
                f"Outcome Contract criterion {criterion_id!r} has no blocking Eval Plan grader of type {contract_grader!r}"
            )

        requirement = evidence_by_claim.get(criterion_id)
        if not isinstance(requirement, dict):
            continue
        required_types = requirement.get("required_types", [])
        required = {item for item in required_types if isinstance(item, str)} if isinstance(required_types, list) else set()
        planned: set[str] = set()
        for eval_item in blocking_evals:
            evidence = eval_item.get("required_evidence", [])
            if isinstance(evidence, list):
                planned.update(item for item in evidence if isinstance(item, str))
        missing = sorted(required - planned)
        if missing:
            errors.append(
                f"claim {criterion_id!r} is missing contract evidence types: {', '.join(missing)}"
            )

    for claim_id, claim in claims_by_id.items():
        if claim.get("material") is True and claim_id not in criteria_by_id:
            errors.append(
                f"Eval Plan material claim {claim_id!r} has no technical Outcome Contract criterion"
            )

    budget = contract.get("budget")
    budget = budget if isinstance(budget, dict) else {}
    planned_reruns = sum(
        item.get("max_evaluator_reruns", 0)
        for item in evals
        if isinstance(item, dict) and isinstance(item.get("max_evaluator_reruns"), int)
    )
    planned_trials = sum(
        policy.get("k", 0)
        for item in evals
        if isinstance(item, dict)
        and isinstance((policy := item.get("trial_policy")), dict)
        and isinstance(policy.get("k"), int)
    )
    max_reruns = budget.get("max_total_eval_reruns")
    max_trials = budget.get("max_total_trials")
    if isinstance(max_reruns, int) and planned_reruns > max_reruns:
        errors.append(
            f"planned evaluator reruns {planned_reruns} exceed Outcome Contract budget {max_reruns}"
        )
    if isinstance(max_trials, int) and planned_trials > max_trials:
        errors.append(
            f"planned trials {planned_trials} exceed Outcome Contract budget {max_trials}"
        )

    return errors


def validate_eval_plan(
    plan: dict[str, Any],
    schema: dict[str, Any],
    contract: dict[str, Any] | None = None,
) -> list[str]:
    errors = _schema_errors(plan, schema)
    claims = _items(plan, "claims")
    evals = _items(plan, "evals")
    claim_ids = _string_ids(claims, "claim_id")
    eval_ids = _string_ids(evals, "eval_id")
    declared_claims = set(claim_ids)
    claims_by_id = {
        item["claim_id"]: item
        for item in claims
        if isinstance(item, dict) and isinstance(item.get("claim_id"), str)
    }
    contract_risks = _items(contract, "risks") if contract is not None else []
    risks_by_id = {
        item["risk_id"]: item
        for item in contract_risks
        if isinstance(item, dict) and isinstance(item.get("risk_id"), str)
    }
    roles = _contract_roles(contract) if contract is not None else {}

    errors.extend(_duplicate_error(claims, "claim_id", "claims"))
    errors.extend(_duplicate_error(evals, "eval_id", "evals"))
    if plan.get("status") == "frozen" and contract is None:
        errors.append("frozen Eval Plan requires --contract for canonical binding validation")

    blocking_by_claim: dict[str, list[dict[str, Any]]] = {}
    valid_material_separation = False
    has_material_governance = False
    has_material_regression = False
    has_material_adversarial = False
    has_material_security = False
    has_material_privacy = False
    has_qualified_human = False

    for index, eval_item in enumerate(evals):
        if not isinstance(eval_item, dict):
            continue
        claim_refs = eval_item.get("claim_ids", [])
        claim_refs = claim_refs if isinstance(claim_refs, list) else []
        for claim_id in claim_refs:
            if isinstance(claim_id, str) and claim_id not in declared_claims:
                errors.append(f"evals.{index}: unknown claim_id {claim_id!r}")

        grader = eval_item.get("grader")
        grader = grader if isinstance(grader, dict) else {}
        grader_type = grader.get("type")
        if plan.get("status") == "frozen" and not isinstance(grader.get("configuration_ref"), str):
            errors.append(f"evals.{index}: frozen plan requires grader configuration_ref")
        if grader_type == "model" and not isinstance(grader.get("calibration_ref"), str):
            errors.append(f"evals.{index}: model grader requires calibration_ref")
        if grader_type == "human" and not isinstance(grader.get("qualification_ref"), str):
            errors.append(f"evals.{index}: human grader requires qualification_ref")

        constraints = eval_item.get("producer_constraints")
        constraints = constraints if isinstance(constraints, dict) else {}
        producer = constraints.get("producer_role")
        allowed = constraints.get("allowed_grader_roles", [])
        prohibited = constraints.get("prohibited_grader_roles", [])
        allowed = allowed if isinstance(allowed, list) else []
        prohibited = prohibited if isinstance(prohibited, list) else []
        allowed_roles = {role for role in allowed if isinstance(role, str)}
        prohibited_roles = {role for role in prohibited if isinstance(role, str)}
        for role in sorted(allowed_roles & prohibited_roles):
            errors.append(
                f"evals.{index}: grader role {role!r} cannot be both allowed and prohibited"
            )
        separation = constraints.get("separation_requirement")
        if separation in {"context", "party"}:
            if isinstance(producer, str) and producer in allowed_roles:
                errors.append(
                    f"evals.{index}: separated review cannot allow producer role {producer!r}"
                )
            if isinstance(producer, str) and producer not in prohibited_roles:
                errors.append(
                    f"evals.{index}: separated review must prohibit producer role {producer!r}"
                )
            if contract is not None and not _separation_is_valid(constraints, roles):
                errors.append(
                    f"evals.{index}: declared {separation} separation is not established by principal_id, context_ref, and read-only grader scope"
                )

        evidence = eval_item.get("required_evidence", [])
        evidence = evidence if isinstance(evidence, list) else []
        eval_class = eval_item.get("eval_class")
        required_class_evidence = EVIDENCE_BY_CLASS.get(eval_class)
        if required_class_evidence and required_class_evidence not in evidence:
            errors.append(
                f"evals.{index}: {eval_class} eval requires {required_class_evidence} evidence"
            )
        required_grader_evidence = EVIDENCE_BY_GRADER.get(grader_type)
        if required_grader_evidence and required_grader_evidence not in evidence:
            errors.append(
                f"evals.{index}: {grader_type} grader requires {required_grader_evidence} evidence"
            )

        material_target = _material_targets(eval_item, claims_by_id, risks_by_id)
        if contract is None:
            material_target = any(
                isinstance(claim_id, str)
                and claims_by_id.get(claim_id, {}).get("material") is True
                for claim_id in claim_refs
            )
        risk_refs = eval_item.get("risk_ids", [])
        risk_refs = risk_refs if isinstance(risk_refs, list) else []
        if eval_class in RISK_EVAL_CLASSES and contract is not None:
            if not any(
                isinstance(risk_id, str)
                and risks_by_id.get(risk_id, {}).get("material") is True
                for risk_id in risk_refs
            ):
                errors.append(
                    f"evals.{index}: {eval_class} eval must bind a material Outcome Contract risk"
                )

        trial_policy = eval_item.get("trial_policy")
        trial_policy = trial_policy if isinstance(trial_policy, dict) else {}
        if (
            eval_item.get("blocking") is True
            and eval_class in REPEATED_TRIAL_PROHIBITED_CLASSES
            and trial_policy.get("kind") != "single"
        ):
            errors.append(
                f"evals.{index}: blocking {eval_class} eval cannot use repeated-trial pass selection"
            )

        if eval_item.get("blocking") is True:
            for claim_id in claim_refs:
                if isinstance(claim_id, str):
                    blocking_by_claim.setdefault(claim_id, []).append(eval_item)
            if material_target and contract is not None and _separation_is_valid(constraints, roles):
                valid_material_separation = True
            if material_target:
                has_material_governance |= eval_class == "governance"
                has_material_regression |= eval_class == "regression"
                has_material_adversarial |= eval_class == "adversarial"
                has_material_security |= eval_class == "security"
                has_material_privacy |= eval_class == "privacy"
                has_qualified_human |= (
                    grader_type == "human"
                    and isinstance(grader.get("qualification_ref"), str)
                    and (contract is None or _separation_is_valid(constraints, roles))
                )

    for claim in claims:
        if not isinstance(claim, dict):
            continue
        claim_id = claim.get("claim_id")
        if claim.get("material") is True and claim_id not in blocking_by_claim:
            errors.append(f"claims: material claim {claim_id!r} has no blocking eval")
            continue
        blocking = blocking_by_claim.get(claim_id, [])
        grader_types = {
            grader.get("type")
            for item in blocking
            if isinstance(item, dict)
            and isinstance((grader := item.get("grader")), dict)
        }
        if claim.get("material") is True and grader_types == {"model"}:
            errors.append(
                f"claims: material claim {claim_id!r} cannot rely only on a model grader"
            )

    baseline = plan.get("baseline")
    baseline = baseline if isinstance(baseline, dict) else {}
    risk_tier = plan.get("risk_tier")
    overlays = plan.get("risk_overlays", [])
    overlays = {item for item in overlays if isinstance(item, str)} if isinstance(overlays, list) else set()
    if not has_material_governance:
        errors.append(f"risk profile {risk_tier!r} requires a governance eval bound to a material risk")
    if baseline.get("regression_applicable") is True and not has_material_regression:
        errors.append("declared baseline requires a regression eval bound to a material target")
    if risk_tier in {"medium", "high"} and not valid_material_separation:
        errors.append(f"risk profile {risk_tier!r} requires a separated verifier on a material target")
    if risk_tier == "high" and not has_material_adversarial:
        errors.append("risk profile 'high' requires an adversarial eval bound to a material risk")
    if "security" in overlays and not has_material_security:
        errors.append("security overlay requires a security eval bound to a material risk")
    if "privacy" in overlays and not has_material_privacy:
        errors.append("privacy overlay requires a privacy eval bound to a material risk")
    if "regulated" in overlays and not has_qualified_human:
        errors.append("regulated overlay requires a separated, qualified human grader")

    if contract is not None:
        errors.extend(_validate_contract_binding(plan, contract, evals))
    return errors


def derive_harness_gate(record: dict[str, Any], plan: dict[str, Any]) -> str:
    """Derive the aggregate technical gate; this never makes the Owner decision."""
    results = _items(record, "eval_results")
    result_by_id = {
        item["eval_id"]: item
        for item in results
        if isinstance(item, dict) and isinstance(item.get("eval_id"), str)
    }
    for eval_item in _items(plan, "evals"):
        if not isinstance(eval_item, dict) or eval_item.get("blocking") is not True:
            continue
        result = result_by_id.get(eval_item.get("eval_id"))
        if not isinstance(result, dict):
            return "blocked"
        if result.get("status") != "pass":
            return "blocked"
        if result.get("invalidated") is True or result.get("conflict_status") == "unresolved":
            return "blocked"
    for finding in _items(record, "findings"):
        if (
            isinstance(finding, dict)
            and finding.get("material") is True
            and finding.get("status") == "open"
        ):
            return "blocked"
    return "ready"


def _verify_artifact_digest(
    artifact_ref: Any, expected_digest: Any, base_dir: Path, location: str
) -> list[str]:
    if not isinstance(artifact_ref, str) or not isinstance(expected_digest, str):
        return []
    path = (base_dir / artifact_ref).resolve()
    try:
        path.relative_to(base_dir.resolve())
    except ValueError:
        return [f"{location}: artifact_ref escapes the declared base directory"]
    if not path.is_file():
        return [f"{location}: artifact {artifact_ref!r} does not exist"]
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    return [] if actual == expected_digest else [f"{location}: sha256 does not match {artifact_ref!r}"]


def validate_gate_record(
    record: dict[str, Any],
    schema: dict[str, Any],
    contract: dict[str, Any],
    plan: dict[str, Any],
    base_dir: Path | None = None,
) -> list[str]:
    errors = _schema_errors(record, schema)
    contract_ref = record.get("contract_ref")
    contract_ref = contract_ref if isinstance(contract_ref, dict) else {}
    plan_ref = record.get("eval_plan_ref")
    plan_ref = plan_ref if isinstance(plan_ref, dict) else {}
    if contract_ref.get("document_id") != contract.get("contract_id"):
        errors.append("contract_ref.document_id does not match Outcome Contract")
    if contract_ref.get("revision") != contract.get("revision"):
        errors.append("contract_ref.revision does not match Outcome Contract")
    if contract_ref.get("sha256") != canonical_digest(contract):
        errors.append("contract_ref.sha256 does not match canonical Outcome Contract digest")
    if plan_ref.get("document_id") != plan.get("eval_plan_id"):
        errors.append("eval_plan_ref.document_id does not match Eval Plan")
    if plan_ref.get("revision") != plan.get("revision"):
        errors.append("eval_plan_ref.revision does not match Eval Plan")
    if plan_ref.get("sha256") != canonical_digest(plan):
        errors.append("eval_plan_ref.sha256 does not match canonical Eval Plan digest")

    attempts = _items(record, "attempts")
    evidence = _items(record, "evidence")
    results = _items(record, "eval_results")
    errors.extend(_duplicate_error(attempts, "attempt_id", "attempts"))
    errors.extend(_duplicate_error(evidence, "evidence_id", "evidence"))
    errors.extend(_duplicate_error(results, "eval_id", "eval_results"))
    attempt_ids = set(_string_ids(attempts, "attempt_id"))
    evidence_by_id = {
        item["evidence_id"]: item
        for item in evidence
        if isinstance(item, dict) and isinstance(item.get("evidence_id"), str)
    }
    result_by_id = {
        item["eval_id"]: item
        for item in results
        if isinstance(item, dict) and isinstance(item.get("eval_id"), str)
    }
    plan_evals = {
        item["eval_id"]: item
        for item in _items(plan, "evals")
        if isinstance(item, dict) and isinstance(item.get("eval_id"), str)
    }
    candidate = record.get("candidate_binding")
    candidate = candidate if isinstance(candidate, dict) else {}
    candidate_ref = candidate.get("candidate_ref")
    roles = _contract_roles(contract)

    for index, evidence_item in enumerate(evidence):
        if not isinstance(evidence_item, dict):
            continue
        role_id = evidence_item.get("produced_by_role")
        role = roles.get(role_id) if isinstance(role_id, str) else None
        if not isinstance(role, dict):
            errors.append(f"evidence.{index}: producer role {role_id!r} is not declared")
        elif evidence_item.get("produced_by_principal_id") != role.get("principal_id"):
            errors.append(f"evidence.{index}: producer principal does not match Outcome Contract role")
        if base_dir is not None:
            errors.extend(
                _verify_artifact_digest(
                    evidence_item.get("artifact_ref"),
                    evidence_item.get("sha256"),
                    base_dir,
                    f"evidence.{index}",
                )
            )

    if base_dir is not None:
        errors.extend(
            _verify_artifact_digest(
                candidate.get("artifact_ref"),
                candidate.get("sha256"),
                base_dir,
                "candidate_binding",
            )
        )

    for eval_id in sorted(set(plan_evals) - set(result_by_id)):
        errors.append(f"eval_results: planned eval {eval_id!r} has no recorded result")
    for eval_id in sorted(set(result_by_id) - set(plan_evals)):
        errors.append(f"eval_results: unknown eval_id {eval_id!r}")

    for index, result in enumerate(results):
        if not isinstance(result, dict):
            continue
        eval_id = result.get("eval_id")
        eval_item = plan_evals.get(eval_id) if isinstance(eval_id, str) else None
        if not isinstance(eval_item, dict):
            continue
        if result.get("candidate_ref") != candidate_ref:
            errors.append(f"eval_results.{index}: candidate_ref does not match Candidate Binding")
        for attempt_id in result.get("attempt_ids", []) if isinstance(result.get("attempt_ids"), list) else []:
            if isinstance(attempt_id, str) and attempt_id not in attempt_ids:
                errors.append(f"eval_results.{index}: unknown attempt_id {attempt_id!r}")
        evidence_ids = result.get("evidence_ids", [])
        evidence_ids = evidence_ids if isinstance(evidence_ids, list) else []
        for evidence_id in evidence_ids:
            if isinstance(evidence_id, str) and evidence_id not in evidence_by_id:
                errors.append(f"eval_results.{index}: unknown evidence_id {evidence_id!r}")
        if result.get("status") == "pass":
            present_types = {
                evidence_by_id[evidence_id].get("evidence_type")
                for evidence_id in evidence_ids
                if isinstance(evidence_id, str) and evidence_id in evidence_by_id
            }
            required = eval_item.get("required_evidence", [])
            required = {item for item in required if isinstance(item, str)} if isinstance(required, list) else set()
            missing = sorted(required - present_types)
            if missing:
                errors.append(
                    f"eval_results.{index}: pass is missing required evidence types: {', '.join(missing)}"
                )
        if result.get("invalidated") is True and result.get("status") == "pass":
            errors.append(f"eval_results.{index}: invalidated result cannot pass")
        contradictions = result.get("contradiction_refs", [])
        contradictions = contradictions if isinstance(contradictions, list) else []
        if result.get("conflict_status") == "unresolved" and result.get("status") != "insufficient_evidence":
            errors.append(
                f"eval_results.{index}: unresolved contradiction must be insufficient_evidence"
            )
        if contradictions and result.get("conflict_status") == "none":
            errors.append(f"eval_results.{index}: contradiction_refs require a conflict status")
        policy = eval_item.get("trial_policy")
        policy = policy if isinstance(policy, dict) else {}
        expected_trials = 0 if result.get("status") == "not_evaluated" else policy.get("k")
        if isinstance(expected_trials, int) and result.get("trial_count") != expected_trials:
            errors.append(
                f"eval_results.{index}: trial_count must equal declared trial policy k={expected_trials}"
            )

    budget = contract.get("budget")
    budget = budget if isinstance(budget, dict) else {}
    build_attempts = sum(
        1 for item in attempts if isinstance(item, dict) and item.get("kind") == "build"
    )
    evaluator_reruns = sum(
        1
        for item in attempts
        if isinstance(item, dict) and item.get("kind") == "evaluator_rerun"
    )
    total_trials = sum(
        item.get("trial_count", 0)
        for item in results
        if isinstance(item, dict) and isinstance(item.get("trial_count"), int)
    )
    max_build_retries = budget.get("max_build_retries")
    max_eval_reruns = budget.get("max_total_eval_reruns")
    max_trials = budget.get("max_total_trials")
    if isinstance(max_build_retries, int) and max(0, build_attempts - 1) > max_build_retries:
        errors.append("attempts exceed Outcome Contract build retry budget")
    if isinstance(max_eval_reruns, int) and evaluator_reruns > max_eval_reruns:
        errors.append("attempts exceed Outcome Contract evaluator rerun budget")
    if isinstance(max_trials, int) and total_trials > max_trials:
        errors.append("eval_results exceed Outcome Contract total trial budget")

    derived = derive_harness_gate(record, plan)
    harness_gate = record.get("harness_gate")
    harness_gate = harness_gate if isinstance(harness_gate, dict) else {}
    if harness_gate.get("state") != derived:
        errors.append(f"harness_gate.state must be derived as {derived!r}")

    authority = contract.get("authority")
    authority = authority if isinstance(authority, dict) else {}
    owner = authority.get("owner")
    owner = owner if isinstance(owner, dict) else {}
    disposition = record.get("owner_disposition")
    disposition = disposition if isinstance(disposition, dict) else {}
    decision = disposition.get("decision")
    if disposition.get("owner_id") != owner.get("owner_id"):
        errors.append("owner_disposition.owner_id does not match Outcome Contract Owner")
    if derived == "blocked" and decision in {"accept", "accept_with_conditions"}:
        errors.append("blocked Harness Gate cannot have an accepting Owner disposition")
    if decision == "accept_with_conditions" and not disposition.get("conditions"):
        errors.append("accept_with_conditions requires at least one recorded condition")

    return errors
