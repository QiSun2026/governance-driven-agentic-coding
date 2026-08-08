# GDAC Practice Kit

Small, copyable tools for applying GDAC v2.0 to one bounded software task.

Status: published supporting kit for GDAC v2.0. The kit does not run an Agent,
enforce a sandbox, or authenticate an Owner. It validates the pre-work records
and deterministically aggregates a supplied post-build Gate Record.

Except where otherwise noted, the kit is licensed with the rest of the
repository under [CC BY 4.0](../NOTICE.md).

## What is included

| File | Use it when |
|---|---|
| [`templates/outcome-contract.yaml`](templates/outcome-contract.yaml) | A delegated task needs a measurable outcome, explicit authority, a whole-task budget, stop conditions, and evidence requirements. |
| [`schemas/outcome-contract.schema.json`](schemas/outcome-contract.schema.json) | Another tool needs the machine-readable structure for Outcome Contract 2.0. |
| [`examples/outcome-contract.example.yaml`](examples/outcome-contract.example.yaml) | You want the original filled example for the contract validator work. |
| [`examples/dry-run-outcome-contract.example.yaml`](examples/dry-run-outcome-contract.example.yaml) | You want the Outcome Contract paired with the end-to-end dry-run Eval example. |
| [`tools/validate_contract.py`](tools/validate_contract.py) | You need to reject malformed or semantically inconsistent YAML or JSON contracts. |
| [`templates/eval-plan.yaml`](templates/eval-plan.yaml) | A material claim needs a pre-build subject-selection rule, grader, pass rule, evidence, separation, retry, and retention policy. |
| [`schemas/eval-plan.schema.json`](schemas/eval-plan.schema.json) | Another tool needs the machine-readable structure for Eval Plan 2.0. |
| [`examples/eval-plan.example.yaml`](examples/eval-plan.example.yaml) | You want a filled medium-risk plan for a dry-run claim bounded to inventoried application write APIs. |
| [`tools/validate_eval_plan.py`](tools/validate_eval_plan.py) | You need to validate an Eval Plan alone or cross-check it against its Outcome Contract. |
| [`schemas/gate-record.schema.json`](schemas/gate-record.schema.json) | Another tool needs the post-build Candidate Binding, evidence, result, finding, gate, and Owner-disposition structure. |
| [Golden dry run](https://qisun2026.github.io/governance-driven-agentic-coding/practice-kit/golden-case.html) | A reader wants the designed walkthrough before opening the source YAML and evidence files. |
| [`examples/golden-dry-run/gate-record.example.yaml`](examples/golden-dry-run/gate-record.example.yaml) | You want one complete, digest-bound record chain with a retained failed attempt. |
| [`tools/validate_gate_record.py`](tools/validate_gate_record.py) | You need to verify artifacts and evidence by digest, derive the Harness Gate, and reject an invalid accepting disposition. |
| [Closeout and controlled learning](https://qisun2026.github.io/governance-driven-agentic-coding/practice-kit/closeout.html) | You want the designed reading guide for project closeout, method-change re-testing, and the worked negative case. |
| [`templates/project-closeout.md`](templates/project-closeout.md) | A task or project should stop, pause, or narrow without losing retained evidence. |
| [`templates/method-change-retest.md`](templates/method-change-retest.md) | A project lesson may improve the shared method but must be tested prospectively before activation. |
| [`cases/harness-closeout.md`](cases/harness-closeout.md) | You want the negative-result case that led to this smaller architecture and rule set. |

## Smallest useful workflow

1. Choose one important, reversible, testable task.
2. Freeze its Outcome Contract before delegated implementation.
3. Freeze the Eval Plan before a candidate result exists. Define how the later
   candidate will be selected and bound to each evidence record.
4. Validate the plan and contract together. A material contract criterion must
   map to a blocking eval with compatible grader and evidence requirements.
5. Give the Builder only the declared write paths and whole-task budget.
6. Bind the completed work to one exact candidate reference, then run the
   declared evals and preserve every required result.
7. Record every eval state and derive `blocked` or `ready` without turning missing or
   failed evidence into a pass.
8. Record a separate Owner disposition and closeout. A passing technical gate
   supports that decision; it does not make it.

## Run the examples

From the repository root:

```text
python -m pip install -r requirements-dev.txt
python practice-kit/tools/validate_contract.py practice-kit/examples/dry-run-outcome-contract.example.yaml
python practice-kit/tools/validate_eval_plan.py practice-kit/examples/eval-plan.example.yaml --contract practice-kit/examples/dry-run-outcome-contract.example.yaml
python -m pytest -q practice-kit/examples/golden-dry-run/test_candidate.py
python practice-kit/tools/validate_gate_record.py practice-kit/examples/golden-dry-run/gate-record.example.yaml --contract practice-kit/examples/dry-run-outcome-contract.example.yaml --eval-plan practice-kit/examples/eval-plan.example.yaml
python -m pytest -c pytest.ini
```

The second validator checks more than YAML shape. It rejects, among other
cases:

- material claims with no blocking eval;
- Owner decisions inserted as eval claims or graders;
- a post-build candidate reference inserted into the pre-build plan;
- a frozen plan that is not bound to the canonical contract digest;
- a medium/high-risk plan with no principal/context-bound separated Verifier;
- a declared baseline with no regression eval;
- a high-risk plan without adversarial coverage, or an overlay without its
  triggered specialist eval;
- a separated reviewer with write access or no actual principal/context separation;
- a model grader with no calibration reference, a human grader with no
  qualification reference, or a material claim graded only by a model;
- risk, criterion, grader, evidence, rerun, or trial-budget drift between the
  contract and plan;
- repeated-trial pass selection on blocking regression, adversarial, security,
  privacy, or governance checks; and
- required technical evidence that does not fail closed.

The Gate Record validator additionally checks exact candidate and evidence
digests, result-to-plan coverage, contradiction handling, retained attempts,
budget use, deterministic gate aggregation, and the Owner-disposition
precondition. It checks recorded evidence; it does not prove that an untrusted
producer told the truth. Identity enforcement, sandboxing, and external actions
remain with the named platform and repository controls.

## Operating boundary

- Facts, inferences, assumptions, unknowns, and Owner decisions stay separate.
- The Eval Plan exists before the candidate; the exact candidate binding exists
  after implementation.
- Missing, failed, stale, conflicting, or unbound required evidence blocks the
  current candidate.
- Technical evaluation, the aggregate Harness Gate, and Owner disposition are three
  separate layers.
- The producer of an object cannot be the sole grader of its material
  non-deterministic claim.
- Builder attempts, evaluator reruns, and stochastic trials use different
  budgets and records.
- A project may propose and test a cross-project rule but cannot activate it by
  itself.

## Provenance and limits

The kit includes controls extracted from the closeout of the experimental
AI-Native Systems Harness, then reconciled with the fuller architecture of GDAC
v1.3. The standalone runtime, adapters, dashboards, synthetic pass rates, and
product hypothesis remain closed. The retained result is a runtime-independent
Harness architecture, Eval rule set, and machine-checkable validation kit.

Repository tests demonstrate validator behavior on declared positive and
negative cases. They do not establish external demand, adoption, production
effectiveness, improved delivery, independent assurance, or compliance.

## Integrity and versioning

The current GDAC v2.0 release is governed by the repository-root
`SHA256SUMS.txt`. The previous v1.5 release remains available at commit
`39ff3cd`, and archived v1.4 artifacts remain governed by the original
[`SHA256SUMS-v1.4.txt`](../archive/releases/v1-series/SHA256SUMS-v1.4.txt). Practice Kit files also have a directory-level
[`SHA256SUMS.txt`](SHA256SUMS.txt), regenerated for the v2.0 release source set.
