# GDAC v2.0 Evaluation Rules

Status: normative evaluation rules for GDAC v2.0, Owner-authorized and
published on 2026-08-08. These rules define the evaluation layer of the GDAC
Harness Architecture.

## Start from a claim

An evaluation does not ask whether the work looks convincing. It asks whether a
frozen claim about an exact subject is supported by the evidence that claim
required before implementation began.

The evaluation layer can block work or mark it ready for an Owner decision. It
cannot create authority, accept the work, deploy it, publish it, or certify it.

The three result layers stay separate:

- a technical eval returns `pass`, `fail`,
  `insufficient_evidence`, or `not_evaluated`;
- the Harness Gate derives `blocked` or `ready`; and
- the Owner separately records `accept`,
  `accept_with_conditions`, `rework`, `pause`, or `stop`.

Owner acceptance is not an eval claim and must not receive a pass score.

## Eval Plan

Material delegated work requires an Eval Plan before implementation. A frozen
plan is valid only when `contract_ref` binds the canonical Outcome Contract ID,
revision, and SHA-256 digest. The plan records one base risk tier, independent
risk overlays, the baseline decision, and a `subject.selection_rule` plus
`subject.binding_rule`: how the post-build candidate will be selected and how
each result must bind to its exact immutable reference. Each eval entry records:

- `eval_id`: stable identifier;
- `claim_ids` and `risk_ids`: the exact statements and material failure modes
  being tested;
- `eval_class`: contract, capability, regression, adversarial, security,
  privacy, or governance;
- `grader`: deterministic code, deterministic rule, model, or qualified
  human;
- `procedure`: inputs, environment, fixtures, and steps;
- `pass_rule`: objective threshold or decision rule;
- `required_evidence`: evidence types that must all be present;
- `risk_trigger`: why this eval is proportionate to the task;
- `conflict_rule`: unresolved contradictory evidence becomes
  `insufficient_evidence`, never a convenient pass;
- `max_evaluator_reruns`: permitted evaluator reruns after a recorded
  infrastructure error, not new Builder attempts;
- `trial_policy`: `single`, `pass-at-k`, or `pass-power-k`, with declared `k`,
  independence rule, complete-trial retention, and selection rule;
- `blocking`: whether failure prevents a positive Harness Gate;
- `insufficient_action`: `block` for required technical evidence;
- `producer_constraints`: who may author, run, review, or change the eval
  and which combinations are forbidden.

The plan-level `reporting` rule always retains stable evidence references and
all attempts. It separately records whether sensitive inputs or raw outputs are
retained, the redaction basis, the retention period, and whether token and cost
data are required, recorded when observable, or not applicable. Redaction may
remove sensitive content; it may not remove the digest, stable reference,
result, or limitation needed to reproduce a maintained claim.

The Eval Plan is frozen with the Outcome Contract. A material change to a claim,
subject-selection rule, pass rule, required evidence, producer constraint, or
authority creates a new Eval Plan version and requires every affected eval to
run again.

The exact candidate does not yet exist when the pre-build plan is frozen. After
implementation, a Candidate Binding resolves the subject-selection rule to one
immutable artifact digest and source revision. Evaluation results attach to that binding, not to
an unversioned description.

## Evaluation types

### Contract and plan validation

Checks whether the outcome is specific and testable, non-goals are explicit,
authority is bounded, budgets and stop rules exist, and every material claim has
an Eval Plan entry.

This is a pre-execution Harness gate, not an Owner decision. Failure blocks
execution.

### Capability eval

Checks whether the claimed new behavior occurs on the declared execution path.
A provider interface, fixture, mock, configuration, or code path does not prove
that live execution occurred.

Capability evidence must match the actual claim. A unit test may show local
logic. It cannot prove an external provider ran unless the execution record
supports that statement.

### Regression eval

Checks whether previously accepted behavior still works on the new snapshot.
The baseline, protected behavior, environment, and allowable change must be
identified before the run.

A required regression failure blocks the current candidate. If the Owner
changes the protected baseline or contract, that change creates a new version.
The failed result remains preserved, and every affected gate must run again
against the new version.

### Adversarial eval

Actively searches for material failure modes, including abnormal input,
permission overreach, hidden write paths, unsafe fallback, evidence substitution,
prompt or tool misuse, and ways to bypass a stop condition.

Adversarial evals are selected by risk. Test volume is not the objective. Each
case should cover a plausible failure that could change acceptance or risk.

### Security and privacy eval

Checks threats and data handling that require specialist methods or accountable
human judgment. Automated checks may support the result. They do not replace
the required security, privacy, legal, or Owner decision authority.

## Grader rules

### Model grader rules

A model is a grader, not an evaluation type. Use one when the claim cannot be
captured adequately by deterministic or rule checks. The record includes model
and configuration, prompt, inputs, outputs, rubric, sampling settings, failures,
limitations, and any human adjudication.

A model grader records a configuration reference and a calibration reference
for the declared claim distribution. It must not be the sole blocking grader
for any material claim. It cannot grade an Owner-reserved decision.

### Human review and the Owner boundary

Human review is used for ambiguous material judgment, security acceptance,
regulated interpretation, usability, and cases where context cannot be reduced
to a reliable mechanical rule.

A qualified human records both the review configuration and a qualification
reference for the declared domain. The Owner decision remains outside the Eval
Plan. It records whether the result, evidence, unknowns, conditions, and
residual risk are accepted for a specific purpose and version.

### Choosing the grader

Use deterministic code or rules when they directly answer the claim. Use a
model only when the judgment cannot be reduced reliably and its limitations can
be recorded. Use a qualified human when accountable domain judgment is
required. Use the Owner only for decisions reserved by authority, not as a
substitute for missing technical evidence.

No grader may approve a claim outside its declared competence or authority.

## Evidence records

Every evidence record states:

- the claim it supports or contradicts;
- the exact subject and snapshot;
- evidence type and producer;
- procedure, environment, and configuration;
- raw result or stable reference;
- integrity information when available;
- pass, fail, or observed value;
- limitations and unresolved unknowns; and
- whether the producer is separated in context or independent in party.

Evidence is bound to the run and subject. Evidence from another version, task,
environment, or claim cannot be silently reused.

The evidence producer must satisfy the Eval Plan's producer constraints. All
required evidence must be present. One convenient result cannot stand in for
another required result.

## Technical eval states

Each eval produces exactly one state under this truth table:

| State | Required condition |
|---|---|
| `pass` | The declared procedure is valid, every required evidence item is valid and bound to the candidate, and the frozen pass rule is met. |
| `fail` | The declared procedure is valid, the required evidence is valid and bound, and the frozen pass rule is not met. |
| `insufficient_evidence` | Missing, invalid, stale, unbound, or unadjudicated contradictory evidence prevents the pass rule from being decided. |
| `not_evaluated` | The declared evaluation was not run. |

A valid result that directly shows the pass rule was not met is a `fail`.
Conflicting records that have not been adjudicated are
`insufficient_evidence`; the evaluator may not choose the favorable record.

The Harness Gate then derives one of two states:

- `blocked`: at least one blocking eval is `fail`,
  `insufficient_evidence`, or `not_evaluated`, or a material
  unresolved finding remains; or
- `ready`: every blocking eval passes and the Gate Record retains the required
  results, limitations, unknowns, and remaining risk.

The Owner records a separate disposition. Owner acceptance is neither a
technical eval state nor a Harness Gate state.

## Six gate-check categories

| Gate check | Question | Required material | Failure consequence |
|---|---|---|---|
| Contract | Is the outcome testable and frozen? | Outcome Contract, non-goals, authority, acceptance, Eval Plan | Block before execution. |
| Authority | Is every action within permission and budget? | Write scope, forbidden actions, retry and stop rules | Stop and escalate. |
| Build integrity | Is the change minimal and technically clean? | Diff and applicable type, lint, security, or clean-environment checks | Rework or stop. |
| Capability and regression | Does the intended path work without breaking accepted behavior? | Frozen capability and regression evidence | Fail or insufficient evidence. |
| Challenge and review | Were material assumptions and failure paths checked without inheriting the Builder's reasoning? | Adversarial cases, findings, dispositions, original evidence | Block unresolved material findings. |
| Decision readiness | Is the evidence bundle complete for the Owner's declared question? | Gate results, limits, unknowns, residual risk, handoff | Ready for Owner or remain blocked. |

These are six categories of checks feeding one aggregate Harness Gate; they are
not six competing state machines. Passing every required check means only that
the declared evidence is complete enough for decision readiness. It does not
create Owner acceptance.

## Subject selection, binding, and invalidation

Before implementation, each eval freezes a subject-selection rule. It may name
the component, interface, path, behavior, baseline, or evidence record that will
be tested, but it does not pretend that the future candidate already exists.

After implementation, a Candidate Binding resolves that rule to the exact
snapshot under review. Each result records both the frozen Eval Plan version and
the Candidate Binding.

If the artifact, contract, Eval Plan, fixture, grader procedure, or relevant
environment changes during evaluation:

1. preserve the original result;
2. mark which results are invalidated;
3. create a new Candidate Binding or Eval Plan version; and
4. rerun every affected required eval.

Do not edit the object of measurement and continue the same review as if nothing
changed.

## Risk tiers and overlays

The Outcome Contract selects one base tier. Regression is required whenever the
plan declares an accepted baseline, regardless of tier.

| Base tier | Evaluation minimum |
|---|---|
| Low | Contract validation, blocking technical acceptance, and a governance eval bound to a material authority risk. |
| Medium | Low tier plus a read-only Verifier with a distinct review context on a material target and explicit handoff. |
| High | Medium tier plus an adversarial eval bound to a material risk and an Owner checkpoint before irreversible action. |

Overlays are independent triggers, not a fourth tier:

| Overlay | Added minimum |
|---|---|
| `security` | Blocking security eval bound to a material security risk. |
| `privacy` | Blocking privacy eval bound to a material data-handling risk. |
| `regulated` | Separated qualified-human grading, legal-role and classification unknowns, and evidence mapping to the applicable obligation. |

The Owner may strengthen the profile. A weaker profile requires a recorded
Owner decision and must not be presented as equivalent evidence. The regulated
overlay cannot determine legal role, conformity, or compliance.

## Retries, repeated trials, and retention

Keep these events distinct:

- a **retry** changes implementation, configuration, or another material input
  and creates a new attempt and Candidate Binding;
- a **rerun** repeats the same procedure on the same candidate after a declared
  execution error or when repetition is part of the plan; and
- a **trial** is one predeclared sample in a repeated-trial reliability question.

The Outcome Contract separately sets `max_build_retries`,
`max_total_eval_reruns`, and `max_total_trials`; each eval also limits its own
reruns and trials. Every material attempt retains its input or stable reference,
output or digest, failure, usage, and reason. Repeated identical blockers stop
the work. A later pass does not delete earlier evidence or known limitations.

The retention rule is frozen before execution. At minimum, retain the applicable
Outcome Contract and Eval Plan versions, subject-selection rule, Candidate
Bindings, raw evidence references, eval results, grader configuration, failed
attempts, gate state, and Owner disposition through project closeout. Evidence
supporting a public or release claim remains traceable for as long as that claim
is maintained.

### Optional repeated-trial metrics

Use `pass@k` only when at least one success in `k` genuinely repeated trials is
the declared reliability question. Use `pass^k` only when all `k` trials must
succeed. Record the model, configuration, input distribution, independence of
trials, sampling, `k`, failures, latency, cost, and token usage when observable.

Do not use repeated-trial pass selection for blocking regression, adversarial,
security, privacy, or governance checks. Do not report pass@k, pass^k, or a
percentage from one run. Do not adopt a generic threshold without declaring why
it matches the claim and risk.

## Model and human review rules

For model or human graders:

- freeze the rubric and decision rule before exposing the result;
- separate source material from the Builder's conclusion where feasible;
- require evidence citations or exact record references;
- record disagreement and adjudication;
- treat ambiguous output as insufficient evidence or require adjudication;
- do not let the Builder dismiss a material finding alone; and
- keep technical findings separate from the Owner's acceptance decision.

Context separation may reduce shared reasoning bias. Only a genuinely separate
party with suitable authority and competence may be called independent.

## Example: a dry-run option

Suppose the Owner wants a cleanup command to add `--dry-run`. It must
report the exact planned changes and perform no application-initiated
filesystem write.

The frozen claims could be:

1. Within the declared candidate-process and fixture boundary, `--dry-run`
   initiates no filesystem write through the write-capable APIs used by the
   candidate, including temporary-file creation, rename, deletion, or metadata
   modification when those APIs are present.
2. The preview matches the changes normal execution would make.
3. Existing behavior without the flag still passes regression tests.
4. Interruption, permission errors, and hidden paths do not trigger a write or
   produce a misleading preview.

Suitable graders:

- instrumented filesystem-write tracing for claims 1 and 4;
- deterministic preview-to-change-set comparison for claim 2;
- existing regression suite for claim 3; and
- adversarial cases with Verifier or Red Team review for claim 4.

The declared scope is: **no application-initiated filesystem write through the
inventoried write-capable APIs within the candidate process and fixture
boundary**. The evidence must list the API inventory, the instrumented subset,
and any uncovered path. An uncovered write path produces
`insufficient_evidence`, not a pass. A before-and-after filesystem snapshot is
supporting evidence. It is not sufficient by itself because a temporary write
could be removed before the final snapshot.

A model grader adds no value when deterministic evidence answers the claim. If
claim 1 fails or its evidence is missing, the task is blocked. If all technical
claims pass, the Harness Gate may return `ready`. The
Owner then records a separate disposition.

This example explains the rule. It is not evidence that the method improves a
real project.

## Eval report

The final report contains:

- Outcome Contract and Eval Plan versions;
- subject-selection rule and Candidate Binding;
- each eval result and evidence reference;
- all failed, insufficient, and not-evaluated items;
- retry and budget usage;
- Verifier and Red Team findings with disposition;
- limitations, unknowns, and residual risk;
- Harness Gate state; and
- Owner decision still required or recorded.

The report is a read-only view of the source records. It is not a new source of
truth.

## Anti-patterns

Reject or rework an evaluation design that:

- writes tests after the result and quietly changes the pass rule;
- lets the Builder grade or accept its own final work;
- measures only happy paths;
- adds model graders where deterministic evidence is available;
- chooses test volume instead of material risk coverage;
- averages away a required failed gate;
- replaces missing evidence with a default score or zero;
- changes the artifact during review without invalidation;
- reports synthetic pass rates as real-world effectiveness; or
- treats a technical pass as permission to deploy, publish, or claim compliance.

## Relation to the Harness

These rules supply the evaluation layer described in [HARNESS.md](./HARNESS.md).
The Outcome Contract defines what matters and who has authority. The Eval Plan
defines how material claims will be judged. The Evidence Bundle records what
happened. The Harness Gate derives blocked or ready for Owner decision. The
Owner decides what happens next.
