# Continuity from GDAC v1.3

Status: explanatory record for GDAC v2.0, published on 2026-08-08. The previous
v1.5 release remains available at commit `39ff3cd`.

GDAC v2.0 uses GDAC v1.3 as its architecture baseline. It keeps the parts
that controlled authority, execution, records, challenge, Owner decisions, and
learning. It replaces the AI-company metaphor with runtime-independent Harness
functions and adds an explicit Eval Plan.

## What remains

| GDAC v1.3 | Harness and Eval form | What is preserved |
|---|---|---|
| Human-in-command | Owner authority and disposition | A person defines the limits, understands material assumptions and unknowns, and makes the final decision. |
| Investor Mandate | Outcome Contract | Outcome, non-goals, resources, risk, acceptance, stop conditions, and reserved decisions are fixed before work. |
| Operating Constitution | Non-negotiable Harness rules | No fabricated result, silent scope expansion, overwritten history, self-approval, or irreversible action without authority. |
| Managing Director | Orchestrator, Builder, and Integrator responsibilities | Planning, bounded implementation, ordinary repair, records, and handoff remain one controlled execution path. |
| Specialist Agents | Temporary bounded tasks | A role exists for a declared purpose, scope, input, output, budget, completion condition, and escalation rule, then exits. |
| Strategic Board and red teams | Verifier and risk-triggered Red Team | A separate evaluation path challenges the exact candidate and original evidence without modifying the work. |
| Project Ledger | Attempt Record and task state | Current work, blockers, next state, usage, failures, and unresolved items remain resumable. |
| Decision Ledger | Versioned decision records | Context, alternatives, disagreement, evidence, authority, and later correction remain append-only. |
| Raw Logs | Proportionate run and evidence records | Material commands, tests, failures, repairs, and their order remain available; full chat retention is not required. |
| Executive Summary | Owner read-only view | A compressed view shows material change, risk, blockers, and decisions without replacing the source records. |
| Standard Operating Loop | Contract to Eval Plan to bounded work to Harness Gate to Owner | Delegation, execution, challenge, escalation, and acceptance remain one explicit path. |
| Risk-tier review | Risk-based evaluation profile | More review is added only for a material risk, evidence source, specialist capability, or different challenge perspective. |
| Acceptance Gate | Aggregate Harness Gate plus Owner disposition | Technical sufficiency and human acceptance are separate decisions. |
| Closed learning loop | Candidate to validated to active to retired | A failure may propose a rule, but no Agent may activate a cross-project rule. |
| Lean discipline | Progressive context, whole-task budgets, and bounded retries | Coordination and evaluation cost must stay proportionate to the task. |

## What is added

v1.3 described evaluation at a high level but did not fully specify how a claim
becomes a gate result. GDAC v2.0 adds:

- an Eval Plan frozen before implementation;
- a trace from `claim -> eval -> grader -> evidence -> gate`;
- deterministic, regression, adversarial, security, model, and qualified-human
  evaluation rules;
- an exact candidate binding after implementation;
- explicit `pass`, `fail`, `insufficient_evidence`, and `not_evaluated` states;
- one deterministic `blocked` or `ready` Harness Gate fed by six categories of
  gate checks;
- subject invalidation when the work or evaluation rule changes;
- separate build retries, evaluator reruns, and stochastic trial budgets;
- canonical Contract-to-Plan digests, principal/context separation, and
  risk-bound evals;
- a post-build Gate Record covering Candidate Binding, evidence, results,
  findings, aggregation, and separate Owner disposition; and
- machine-checkable Outcome Contract, Eval Plan, and Gate Record examples.

## What is reshaped

The following v1.3 functions remain, but not as standing AI offices:

- Investor Office becomes an Owner read-only view.
- Academy becomes a controlled learning view and prospective re-test.
- GTM and Narrative becomes an evidence-backed public view with a separate
  publication decision.
- The Managing Director becomes a set of execution responsibilities rather
  than a permanent executive Agent.
- Independent challenge is described as context separation unless a genuinely
  separate qualified party exists.

This preserves the control function without requiring role play, permanent
Agents, or unnecessary coordination.

## What is not carried forward

GDAC v2.0 does not retain:

- a mandatory AI-company organization;
- a fixed number of red teams or standing departments;
- claims that every project automatically creates Owner capability, market
  assets, adoption, lower cost, or improved delivery;
- uninstrumented organizational KPIs;
- a full Agent runtime, scheduler, sandbox, deployment system, or compliance
  certification layer; or
- automatic activation of lessons or global rules.

These removals do not reduce the control architecture. They remove metaphors,
product scope, or outcome claims that the current evidence cannot support.

## The resulting method

In one sentence:

> Define the outcome and authority, lock the evidence rules, let Agents work
> inside the boundary, challenge the exact result through a separate path, and
> give the full record to the Owner for a final decision.
