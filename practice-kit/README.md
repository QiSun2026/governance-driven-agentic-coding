# GDAC Practice Kit

This directory contains small, copyable tools for applying
**Governance-Driven Agentic Coding** in real work.

It is a non-normative companion to public GDAC v1.4. It does not change the
method version, create v1.5, or make every field mandatory for every task.

Except where otherwise noted, the kit is licensed with the rest of the
repository under [CC BY 4.0](../NOTICE.md).

## What is included

| File | Use it when |
|---|---|
| [`templates/outcome-contract.yaml`](templates/outcome-contract.yaml) | A material Agent task needs a measurable outcome, explicit authority, budgets, stop conditions, and evidence requirements before work begins. |
| [`templates/project-closeout.md`](templates/project-closeout.md) | A project should stop, pause, or narrow without losing its evidence or turning sunk cost into a reason to continue. |
| [`templates/method-change-retest.md`](templates/method-change-retest.md) | A project lesson may improve the shared method, but must be compared with the current baseline before promotion. |
| [`cases/harness-closeout.md`](cases/harness-closeout.md) | You want a worked example of closing an engineered product hypothesis while retaining reusable governance practice. |

## Smallest useful workflow

1. Copy the Outcome Contract only for a material or delegated task. Delete
   fields that are genuinely inapplicable; do not fill them ceremonially.
2. When the product or project no longer earns continued investment, complete
   the Project Closeout record before starting replacement work.
3. If the project exposed a potentially reusable rule, preregister a Method
   Change Re-test. Compare the existing method and candidate using the same
   contemporaneous evidence.
4. Promote nothing automatically. A passing test supports a decision; it does
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

The versioned v1.4 HTML and PDF artifacts remain governed by the repository-root
`SHA256SUMS.txt`. This Practice Kit is a repository supplement, not part of
those frozen v1.4 artifact bytes. Its files have a separate
[`SHA256SUMS.txt`](SHA256SUMS.txt).
