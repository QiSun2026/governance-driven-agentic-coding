# Related Work and Boundaries

GDAC combines familiar controls. Its claim is not that any one component is
new. The narrower contribution is a compact operating protocol for delegating
material software work to probabilistic agents while keeping acceptance and
authority outside the producer.

| Prior work | What already exists | What GDAC adds | What GDAC does not claim |
|---|---|---|---|
| [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) | A voluntary, outcome-focused framework organized around Govern, Map, Measure, and Manage. | A repository-level contract, evidence gate, and handoff loop for agentic software work. | GDAC is not an AI risk-management standard and is not a substitute for NIST AI RMF. |
| [IIA Three Lines Model](https://www.theiia.org/en/resources/statements-of-position) | Organizational accountability, oversight, and objective assurance roles. | A small producer/reviewer separation rule for a single governed object. | Context-independent review is not organizational independence, internal audit, or third-party assurance. |
| [Federal Reserve SR 26-2](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm) | Non-prescriptive, risk-based model guidance issued on 2026-04-17 and expected to be most relevant above $30 billion in assets. Its scope explicitly excludes generative and agentic AI. | A software-delivery pattern for bounded agent delegation outside that supervisory scope. | GDAC is not supervisory guidance. SR 26-2 is not a basis for claiming that GDAC governs generative or agentic AI in regulated banks. |
| [EU AI Act, Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj?locale=en) | Legal obligations that include documentation and downstream transparency duties for providers of general-purpose AI models, with additional duties for systemic-risk models. | A repository-level evidence map and authority protocol for software work that uses agents. | GDAC does not determine legal role, risk classification, conformity, or compliance with the AI Act. |
| [Architecture Decision Records](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) | Small, version-controlled records of context, decisions, status, and consequences. | A pre-work record that also freezes acceptance, delegated authority, budgets, and stop conditions. | An Outcome Contract does not replace ADRs or justify every implementation decision. |
| [in-toto](https://in-toto.io/docs/getting-started/) and [SLSA provenance](https://slsa.dev/spec/v1.2/provenance) | Verifiable supply-chain steps, authorized functionaries, artifact identity, and provenance attestations. | Claim-to-evidence mapping that can include tests, reviews, unknowns, and human decisions. | A GDAC evidence record is not automatically authenticated provenance or a tamper-resistant attestation. |
| [Center for Open Science preregistration](https://www.cos.io/) | Time-stamped plans recorded before results are known to reduce hindsight-driven changes. | A lightweight prospective re-test for candidate governance rules. | A method re-test is not a scientific study, replication, or independent validation. |
| [Inspect](https://inspect.aisi.org.uk/) | An evaluation framework with datasets, agents, tools, scorers, logs, limits, and support for external coding agents. | An authority and acceptance wrapper around whichever evaluation system a project selects. | GDAC is not an evaluation runtime, benchmark suite, or substitute for Inspect. |
| [AGENTS.md](https://agents.md/) | A portable Markdown format for repository instructions such as setup, tests, conventions, and security guidance for coding agents. | A task-level contract for outcome, delegated authority, evidence, stop conditions, and Owner acceptance. | GDAC does not replace repository instructions or require a proprietary agent configuration format. |

## Design stance

GDAC deliberately reuses these ideas instead of inventing a parallel vocabulary.
Terms are introduced only where they change a permitted state, an authority
boundary, or the evidence required for a claim.

The construction is domain-agnostic in the limited sense that the core schema
does not require one business domain. Current evidence is not domain-neutral:
it comes from two author-run private projects that external readers cannot
inspect, and it has not been independently replicated.

## Evidence independence statement

Unless a specific record says otherwise, current GDAC artifacts, examples,
tests, reviews, and conclusions were produced, recorded, and evaluated by the
author with AI assistance. No independent third party has replicated the method
or validated improved delivery, safety, cost, or governance outcomes.
