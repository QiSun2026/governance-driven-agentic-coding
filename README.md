# Governance-Driven Agentic Coding

A small governance protocol for material software work delegated to AI agents.
It connects a verifiable outcome, bounded authority, context-independent review,
claim-level evidence, and an accountable Owner decision.

## Status

- **Current method:** v1.5, published on 2026-08-07.
- **Historical version:** v1.4 remains available with unchanged HTML and PDF
  artifact bytes.
- **Evidence:** author-run projects and repository tests. No independent
  replication or validated delivery, safety, cost, or governance improvement.

## Read

### Current v1.5

- [在线阅读中文版](./index.html)
- [中文版 PDF](./Governance-Driven-Agentic-Coding-v1.5.pdf)
- [Read the English edition](./en.html)
- [English PDF](./Governance-Driven-Agentic-Coding-EN-v1.5.pdf)
- [Related work and boundaries](./RELATED_WORK.md)
- [Practice Kit](./practice-kit/README.md)

The current HTML, PDFs, executable contract tools, tests, and supporting records
are governed by [`SHA256SUMS.txt`](./SHA256SUMS.txt).

### Historical v1.4

- [中文版 HTML](./versions/v1.4/index.html)
- [中文版 PDF](./Governance-Driven-Agentic-Coding-v1.4.pdf)
- [English HTML](./versions/v1.4/en.html)
- [English PDF](./Governance-Driven-Agentic-Coding-EN-v1.4.pdf)

The historical artifacts are governed by
[`SHA256SUMS-v1.4.txt`](./SHA256SUMS-v1.4.txt).

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

## Why v1.5 is smaller

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
schema has no domain-specific fields. Current practice evidence comes from two
author-run private projects that external readers cannot inspect. It has not
been independently validated across domains.

## License

Original repository material is licensed under
[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
See [LICENSE](./LICENSE) and [NOTICE.md](./NOTICE.md).

Earlier historical PDFs remain available:

- [中文版 v1.2](./Governance-Driven-Agentic-Coding-v1.2.pdf)
- [English v1.3](./Governance-Driven-Agentic-Coding-EN-v1.3.pdf)
