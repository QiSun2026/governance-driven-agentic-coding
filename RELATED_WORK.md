# Related Work and Boundaries

GDAC does not invent branch protection, policy engines, evaluation runtimes,
provenance, or repository instructions. Its narrower contribution is an
operating protocol that binds those controls to one delegated task:

`frozen outcome and authority -> exact candidate -> declared evals -> evidence -> aggregate gate -> accountable disposition`

## Nearest engineering neighbors

| Existing mechanism | What it already does well | Where GDAC sits |
|---|---|---|
| [GitHub protected branches and required checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) | Enforce merge conditions, review counts, status checks, signed commits, and other repository rules. | The Outcome Contract states why a task exists and what authority was delegated; the Gate Record binds required-check output to the exact claim and candidate. GDAC should feed branch rules, not replace them. |
| [GitHub CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) | Requests review from declared owners of paths and can support required code-owner approval. | GDAC records the task-level Owner, Builder, Verifier principal/context separation, and reserved decisions. A CODEOWNERS approval is evidence or a disposition only when the plan says which. |
| [Open Policy Agent](https://www.openpolicyagent.org/docs) and its [CI/CD guidance](https://www.openpolicyagent.org/docs/cicd) | Evaluate machine-readable policy as code across services and delivery pipelines. | A GDAC validator can call or be called by policy-as-code. GDAC defines the surrounding contract, evidence binding, fail-closed state, and human disposition; it is not a competing policy language. |
| Agent permission systems, including [Claude Code CLI permissions](https://docs.anthropic.com/en/docs/claude-code/cli-usage) | Restrict tools, commands, files, or execution modes inside a specific Agent runtime. | GDAC records portable authority and stop conditions. The runtime must enforce them. A YAML write scope alone is not a sandbox. |
| [Inspect](https://inspect.aisi.org.uk/) and its [evaluation logs](https://inspect.aisi.org.uk/eval-logs.html) | Run evaluations with datasets, agents, tools, scorers, limits, and inspectable logs. | GDAC can use Inspect as an eval execution and logging layer. GDAC adds task authority, candidate/claim binding, aggregate gate rules, and the separate Owner disposition; it is not another benchmark runtime. |
| [in-toto](https://in-toto.io/docs/getting-started/), [SLSA provenance](https://slsa.dev/spec/v1.2/provenance), and [GitHub artifact attestations](https://docs.github.com/en/enterprise-cloud@latest/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations) | Bind artifacts to authenticated build steps, identities, and provenance statements. | GDAC evidence may reference attestations and digests. The starter Gate Record checks identity of files by digest but does not by itself authenticate the producer or provide tamper-resistant provenance. |
| [Architecture Decision Records](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) | Preserve context, decision, status, and consequences in version control. | ADRs explain architecture choices. An Outcome Contract freezes task result, authority, budgets, stop rules, and evidence before implementation. A project may use both. |
| [AGENTS.md](https://agents.md/) | Gives coding agents portable repository instructions for setup, tests, conventions, and security. | Repository instructions describe the environment. GDAC adds a task-level contract and post-build decision chain; it should reference, not duplicate, repository guidance. |

## Risk and regulated-environment overlays

Broader frameworks such as the [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework), the [IIA Three Lines Model](https://www.theiia.org/en/resources/statements-of-position), and the [EU AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj?locale=en) address organizational risk, accountability, assurance, or legal obligations at a different level.

GDAC may map a task's records to an organization's controls and flag missing
evidence or unresolved legal questions. It does not determine legal role or
risk classification, create organizational independence, perform internal
audit, establish conformity, or certify compliance. Review in a fresh Agent
context is context separation; only a genuinely separate qualified party may
be described as independent.

## Design stance

GDAC introduces a term only when it changes authority, object identity,
evidence sufficiency, or a permitted state transition. Its practical test is
integration: can a team connect an issue, contract, checked-in Eval Plan,
commit SHA, CI or eval output, Gate Record, and maintainer disposition without
building a second project-management system?

The repository currently demonstrates the structure and deterministic rules on
included cases. External adoption and production-outcome evidence remain open
questions rather than design claims.
