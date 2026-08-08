# Governance-Driven Agentic Coding

**A governance harness and evaluation protocol for software work delegated to AI coding agents.**

GDAC defines the expected result, delegated authority, evidence requirements,
budgets, and stop conditions before work begins. It then binds evaluation to the
exact candidate that was built and leaves final acceptance with an accountable
human Owner.

[Read the guide](https://qisun2026.github.io/governance-driven-agentic-coding/) ·
[Harness architecture](https://qisun2026.github.io/governance-driven-agentic-coding/harness.html) ·
[Evaluation rules](https://qisun2026.github.io/governance-driven-agentic-coding/eval-rules.html) ·
[Practice Kit](https://qisun2026.github.io/governance-driven-agentic-coding/practice-kit/)

## The problem it addresses

Coding agents can produce changes quickly, but speed alone does not establish
who authorized the work, whether the result meets the intended claim, which
evidence belongs to the final candidate, or who may accept the remaining risk.
GDAC adds that control layer around existing tools such as Codex, Claude, CI,
branch protection, code review, and policy as code.

```text
Outcome Contract
    -> bounded agent execution
    -> frozen Eval Plan
    -> exact candidate and retained evidence
    -> deterministic Harness Gate
    -> human Owner disposition
```

Three records carry the minimum machine-checkable chain:

| Record | Purpose |
|---|---|
| Outcome Contract | Freezes the result, scope, authority, budget, risks, and stop conditions. |
| Eval Plan | Defines claims, graders, required evidence, and retry rules before the result is known. |
| Gate Record | Binds the candidate, evidence, findings, gate state, and later Owner disposition. |

Use the full chain for material, security-sensitive, privacy-sensitive,
hard-to-reverse, or externally visible work. Shorten it for reversible work.
Skip it when ordinary repository controls already provide enough assurance.

## Try one governed task

The included dry-run case contains a Contract, Eval Plan, candidate, retained
failed attempt, evidence bundle, and Gate Record:

```bash
python -m pip install -r requirements-dev.txt
python practice-kit/tools/validate_contract.py practice-kit/examples/dry-run-outcome-contract.example.yaml
python practice-kit/tools/validate_eval_plan.py practice-kit/examples/eval-plan.example.yaml --contract practice-kit/examples/dry-run-outcome-contract.example.yaml
python -m pytest -q practice-kit/examples/golden-dry-run/test_candidate.py
python practice-kit/tools/validate_gate_record.py practice-kit/examples/golden-dry-run/gate-record.example.yaml --contract practice-kit/examples/dry-run-outcome-contract.example.yaml --eval-plan practice-kit/examples/eval-plan.example.yaml
python -m pytest -c pytest.ini
```

The validators check the declared record chain. They do not run an agent,
provide an operating-system sandbox, authenticate an Owner, or authorize a
deployment.

## Repository map

| Path | What belongs there |
|---|---|
| [`method/`](./method/) | Normative Harness and evaluation specifications, continuity, and related work. |
| [`practice-kit/`](./practice-kit/) | Schemas, templates, examples, and small validator entry points. |
| [`gdac/`](./gdac/) | Deterministic Python validation logic. |
| [`tests/`](./tests/) | Valid, invalid, adversarial, integrity, and fail-closed tests. |
| [`docs/`](./docs/) | Current static GitHub Pages source. |
| [`contributing/`](./contributing/) | Non-normative editorial and interface guidance. |
| [`archive/`](./archive/) | Byte-preserved pre-v2.0 release artifacts kept out of the current product surface. |

The readable method sources are
[`method/harness.md`](./method/harness.md) and
[`method/evaluation-rules.md`](./method/evaluation-rules.md). The designed HTML
pages are the public reading experience.

## Evidence boundary

The repository tests demonstrate the declared schema and validator behavior on
the included cases. They do not establish external adoption, production
effectiveness, independent assurance, reduced risk, lower cost, organizational
value, or legal compliance.

## Release status

- **Current release:** GDAC v2.0, Owner-authorized and published on 2026-08-08.
- **Previous release:** GDAC v1.5 remains available at commit
  [`39ff3cd`](https://github.com/QiSun2026/governance-driven-agentic-coding/tree/39ff3cd).
- **History:** See [`CHANGELOG.md`](./CHANGELOG.md) and the versioned
  [`archive/`](./archive/).

## Citation and license

Citation metadata is available in [`CITATION.cff`](./CITATION.cff). Original
repository material is licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); see
[`LICENSE`](./LICENSE) and [`NOTICE.md`](./NOTICE.md).
