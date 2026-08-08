# Governance-Driven Agentic Coding

Governance-Driven Agentic Coding (GDAC) is a portable Harness architecture and
evaluation protocol for important software work delegated to AI agents. It
defines the result before execution, limits what Agents may change, preserves a
shared evidence record, evaluates frozen claims against an exact candidate, and
leaves the final decision with an accountable Owner.

## Status

- **Current release:** GDAC v2.0, Owner-authorized and published on 2026-08-08.
- **Previous release:** GDAC v1.5 remains available at commit
  [`39ff3cd`](https://github.com/qisun2026/governance-driven-agentic-coding/tree/39ff3cd).
- **Version scope:** v2.0 is a material method release. It restores the fuller
  control architecture of v1.3, adds explicit Harness and Eval rules, and
  closes the machine-checkable record chain through the Gate Record.

## What v2.0 defines

| Layer | Question it answers |
|---|---|
| Outcome Contract | What result matters, what is out of scope, what may change, and when must work stop? |
| Bounded execution | Which temporary responsibilities may act, with what context, write scope, and whole-task budget? |
| Record and evidence plane | Which frozen records, attempts, diffs, tests, findings, limits, and unknowns survive the work? |
| Eval Plan | Which claims will be tested, by which grader, with which evidence, before the result is known? |
| Harness Gate | Do all blocking evals pass with no open material finding? |
| Owner disposition | Does the accountable person accept, set conditions, request rework, pause, or stop? |
| Controlled learning | Which failure-backed rule may be tested, activated for a declared scope, or retired? |

The technical eval result, the aggregate Harness Gate, and the Owner disposition are
deliberately separate. Passing tests cannot authorize deployment, publication,
compliance claims, or another external action.

## When to use it

| Mode | Use it when | Minimum record |
|---|---|---|
| Full | The Agent can make a material, hard-to-reverse, security-sensitive, privacy-sensitive, or externally visible change. | Frozen Contract and Eval Plan, separated review, complete Gate Record, Owner disposition. |
| Light | The change is reversible but still merits delegated write access or a maintained claim. | Short Contract, direct acceptance and authority checks, candidate binding, compact Gate Record. |
| Skip | The task is read-only, trivial, locally reversible, and already covered by normal repository controls. | Use the repository's existing issue, tests, review, and branch rules. |

The method should remove ceremony when the risk is low. It should not create a
parallel project-management system.

In a normal Git workflow, GDAC sits around existing controls:

`Issue or Contract -> checked-in Eval Plan -> commit SHA -> CI evidence -> Gate Record -> maintainer/Owner disposition`

Branch protection, CODEOWNERS, required checks, and provenance tools keep their
jobs; GDAC binds their outputs to the delegated authority and acceptance claim.

## Read v2.0

- [Main English guide](./index.html)
- [Harness Architecture](./harness.html)
- [Evaluation Rules](./eval-rules.html)
- [What changed from v1.3](./continuity.html)
- [Practice Kit](./practice-kit/index.html)
- [Related work and boundaries](./related-work.html)
- [中文导读](./zh.html)
- [Non-normative editorial interface prompt](./DESIGN_LANGUAGE_PROMPT.md)

The normative working sources remain available as
[`HARNESS.md`](./HARNESS.md), [`EVAL_RULES.md`](./EVAL_RULES.md), and
[`V1_3_CONTINUITY.md`](./V1_3_CONTINUITY.md). The HTML pages are the designed
reading experience; the Markdown files are inspection sources.

## Try one governed task

The paired example governs a `--dry-run` option whose primary claim is that,
inside the declared candidate-process and fixture boundary, it initiates no
filesystem write through the write-capable APIs used by the bundled candidate.
Run from the repository root:

```text
python -m pip install -r requirements-dev.txt
python practice-kit/tools/validate_contract.py practice-kit/examples/dry-run-outcome-contract.example.yaml
python practice-kit/tools/validate_eval_plan.py practice-kit/examples/eval-plan.example.yaml --contract practice-kit/examples/dry-run-outcome-contract.example.yaml
python -m pytest -q practice-kit/examples/golden-dry-run/test_candidate.py
python practice-kit/tools/validate_gate_record.py practice-kit/examples/golden-dry-run/gate-record.example.yaml --contract practice-kit/examples/dry-run-outcome-contract.example.yaml --eval-plan practice-kit/examples/eval-plan.example.yaml
python -m pytest -c pytest.ini
```

The validators check structure, canonical Contract-to-Plan binding, material
claim and risk coverage, principal/context separation, budgets, evidence
binding, the result truth table, deterministic gate aggregation, and the
precondition for an accepting Owner disposition. They do not execute an Agent,
enforce the operating-system sandbox, or authenticate an Owner.

## What this repository ships

The repository currently includes:

- readable Harness and Eval specifications;
- portable Outcome Contract, Eval Plan, and Gate Record schemas;
- templates and a complete golden record-chain example;
- deterministic pre-work and post-build validators;
- tests for valid and fail-closed cases; and
- static English-first and Chinese-secondary reading pages.

It does not include a general Agent runner, scheduler, persistent database,
execution sandbox, deployment system, Owner identity service, or automatic
compliance certification.

## Continuity from v1.3

The v2.0 method keeps v1.3's human-in-command model, bounded delegation,
risk-based review, durable project and decision records, separated challenge,
Owner acceptance, organizational learning, and lean-control discipline. It
replaces the AI-company metaphor and standing offices with runtime-independent
Harness functions. It then adds the missing claim-to-evidence protocol:
pre-build Eval Plans, post-build candidate binding, explicit grader authority,
invalidation rules, bounded retries, and fail-closed gates.

See the [control-by-control continuity map](./continuity.html) for the full
accounting.

## Evidence boundary

Unless a specific record states otherwise, the author produced, recorded, and
evaluated the current artifacts, examples, tests, reviews, and conclusions with
AI assistance. Repository checks demonstrate the declared schema and validator
behavior on the included cases. They do not establish external adoption,
production effectiveness, independent assurance, reduced risk, lower cost,
organizational value, or legal compliance.

## Published history

- [Previous English v1.5 PDF](./Governance-Driven-Agentic-Coding-EN-v1.5.pdf)
- [Previous Chinese v1.5 PDF](./Governance-Driven-Agentic-Coding-v1.5.pdf)
- [Historical English v1.4 HTML](./versions/v1.4/en.html)
- [Historical Chinese v1.4 HTML](./versions/v1.4/index.html)
- [Historical English v1.3 PDF](./Governance-Driven-Agentic-Coding-EN-v1.3.pdf)

Historical release artifacts remain unchanged. Matching checksums establish
file identity, not correctness, semantic sufficiency, or effectiveness.

## License

Original repository material is licensed under
[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
See [LICENSE](./LICENSE) and [NOTICE.md](./NOTICE.md).
