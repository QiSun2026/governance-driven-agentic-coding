# Governance-Driven Agentic Coding

A small governance protocol for material software work delegated to AI agents.
It connects a verifiable outcome, bounded authority, context-independent review,
claim-level evidence, and an accountable Owner decision.

## Status

- **Published method:** v1.4, frozen and unchanged.
- **Working candidate:** v1.5, under Owner review and not a public release.
- **Evidence:** author-run projects and repository tests. No independent
  replication or validated delivery, safety, cost, or governance improvement.

## Read

### v1.5 Owner review candidate

- [中文候选页面](./candidate-v1.5.html)
- [English candidate](./candidate-v1.5-en.html)
- [Related work and boundaries](./RELATED_WORK.md)
- [Practice Kit](./practice-kit/README.md)

### Current published v1.4

- [在线阅读中文版](https://qisun2026.github.io/governance-driven-agentic-coding/)
- [中文版 PDF](./Governance-Driven-Agentic-Coding-v1.4.pdf)
- [Read the English edition](https://qisun2026.github.io/governance-driven-agentic-coding/en.html)
- [English PDF](./Governance-Driven-Agentic-Coding-EN-v1.4.pdf)

The published entry pages and versioned PDFs remain governed by the root
[`SHA256SUMS.txt`](./SHA256SUMS.txt).

## The v1.5 kernel

1. **Bounded delegation:** freeze outcome, acceptance, write scope, budget,
   retries, stop conditions, and Owner-reserved decisions before work.
2. **Context-independent review:** review the frozen object and original evidence
   without inheriting the Producer's reasoning. This is context separation, not
   third-party or organizational independence.
3. **Claim integrity:** keep facts, inferences, assumptions, unknowns, and Owner
   decisions distinct. Missing evidence fails closed.

Complex projects may map these responsibilities to an Orchestrator, Builder,
Verifier, Red Team, or Integrator. Those roles are optional implementation
choices, not additional layers every project must create.

## Run the executable contract check

```text
python -m pip install -r requirements-dev.txt
python practice-kit/tools/validate_contract.py \
  practice-kit/examples/outcome-contract.example.yaml
python -m pytest -c pytest.ini
```

The schema is at
[`practice-kit/schemas/outcome-contract.schema.json`](./practice-kit/schemas/outcome-contract.schema.json).
The filled example describes the actual validator work in this repository.

## What the candidate removes

v1.5 removes GTM, narrative, academy, investor-office, portfolio-brand, and
asset-taxonomy material from the normative method. It also replaces the
"Strategic Board" label with the narrower term "context-independent review."

The method-change re-test is reduced to one page. The method keeps only controls
that change authority, permitted state, or evidence required for a claim.

## Evidence boundary

Unless a specific record states otherwise, GDAC artifacts, examples, tests,
reviews, and conclusions were produced, recorded, and evaluated by the author
with AI assistance. Current repository tests verify bounded technical behavior.
They do not establish external adoption, product need, production effectiveness,
or compliance.

The construction is domain-agnostic only in the limited sense that its core
schema has no domain-specific fields. It has not been independently validated
across domains.

## License

Original repository material is licensed under
[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
See [LICENSE](./LICENSE) and [NOTICE.md](./NOTICE.md).

Historical PDFs remain available:

- [中文版 v1.2](./Governance-Driven-Agentic-Coding-v1.2.pdf)
- [English v1.3](./Governance-Driven-Agentic-Coding-EN-v1.3.pdf)
