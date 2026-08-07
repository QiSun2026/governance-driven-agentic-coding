# GDAC Practice Kit

This directory contains small, copyable tools for applying
**Governance-Driven Agentic Coding** in real work.

It is a non-normative companion to current GDAC v1.5. It does not make every
field mandatory for every task.

Except where otherwise noted, the kit is licensed with the rest of the
repository under [CC BY 4.0](../NOTICE.md).

## What is included

| File | Use it when |
|---|---|
| [`templates/outcome-contract.yaml`](templates/outcome-contract.yaml) | A material Agent task needs a measurable outcome, explicit authority, budgets, stop conditions, and evidence requirements before work begins. |
| [`schemas/outcome-contract.schema.json`](schemas/outcome-contract.schema.json) | A machine-readable JSON Schema for Outcome Contract version 1.0. |
| [`examples/outcome-contract.example.yaml`](examples/outcome-contract.example.yaml) | A filled contract for the schema and validator work in this repository. |
| [`tools/validate_contract.py`](tools/validate_contract.py) | A small validator that accepts YAML or JSON and fails non-zero on invalid contracts. |
| [`templates/project-closeout.md`](templates/project-closeout.md) | A project should stop, pause, or narrow without losing its evidence or turning sunk cost into a reason to continue. |
| [`templates/method-change-retest.md`](templates/method-change-retest.md) | A project lesson may improve the shared method, but must be compared with the current baseline before promotion. |
| [`cases/harness-closeout.md`](cases/harness-closeout.md) | You want a worked example of closing an engineered product hypothesis while retaining reusable governance practice. |

## Smallest useful workflow

1. Install the small validation dependencies with
   `python -m pip install -r requirements-dev.txt`.
2. Copy the Outcome Contract only for a material or delegated task. Delete
   optional content that is genuinely inapplicable; do not fill it ceremonially.
3. Freeze and validate it before work begins:
   `python practice-kit/tools/validate_contract.py your-contract.yaml`.
4. When the product or project no longer earns continued investment, complete
   the Project Closeout record before starting replacement work.
5. If the project exposed a potentially reusable rule, preregister a Method
   Change Re-test. Compare the existing method and candidate using the same
   contemporaneous evidence.
6. Promote nothing automatically. A passing test supports a decision; it does
   not make the decision or change the published method.

## Operating boundary

- Facts, inferences, assumptions, unknowns, and Owner decisions stay separate.
- Missing evidence does not become a pass, zero, approval, or readiness.
- Technical verification is not Owner acceptance or release authority.
- A project may propose a cross-project rule but cannot activate it by itself.
- Templates should shrink for low-risk work and fail closed for material work.
- The producer of an object should not be the sole authority deciding whether
  a material change can bypass re-review.

## Provenance and limits

The kit was extracted from the controlled closeout of the experimental
AI-Native Systems Harness. That project produced bounded internal engineering
evidence but did not establish external demand, adoption, production
effectiveness, or a distinct standalone product need.

The transfer review did not justify importing the Harness runtime, adapters,
dashboards, synthetic pass rates, or proposed method changes into canonical
GDAC. The useful residue was smaller: explicit task contracts, disciplined
project closeout, and prospective method-change testing.

See the [case note](cases/harness-closeout.md) for the negative result and the
claims that remain prohibited.

## Integrity and versioning

The current v1.5 release is governed by the repository-root `SHA256SUMS.txt`.
Historical v1.4 artifacts remain governed by `SHA256SUMS-v1.4.txt`. The Practice
Kit files also have a directory-level [`SHA256SUMS.txt`](SHA256SUMS.txt).
