# Change Log

This repository records published versions of **Governance-Driven Agentic Coding**.
Unpublished working changes and internal hypotheses are not public method versions.

## v1.5 - 2026-08-07

### Status

- Current bilingual method version, accepted for publication by the Owner.
- Frozen v1.4 HTML and PDF artifact bytes remain unchanged and have a
  version-specific checksum manifest.
- No adoption, production, compliance, or external-validation claim.

### Removed from the normative method

- GTM and narrative functions, including interview-narrative language.
- Academy, Investor Office, Strategic Board, four-flow, and five-asset taxonomies.
- RiskFirewall product branding and application positioning.
- Uninstrumented KPI lists and claims of domain-neutral evidence.

### Added or narrowed

- Three load-bearing controls: bounded delegation, context-independent review,
  and claim integrity.
- A JSON Schema, filled YAML example, validator, and negative tests for the
  Outcome Contract.
- An explicit evidence-independence statement.
- Related-work boundaries covering NIST AI RMF, the IIA Three Lines Model,
  Federal Reserve SR 26-2, the EU AI Act, ADRs, in-toto, SLSA,
  preregistration, Inspect, and AGENTS.md.
- A git-verifiable freeze-before-review example that does not overclaim reviewer
  party independence.
- A one-page prospective Method-Change Re-test.
- Two measurable metrics only when instrumented: tokens per accepted outcome and
  evidence-driven reopen rate.

### Evidence basis

Repository tests demonstrate schema validation behavior on declared positive and
negative cases. The method and conclusions remain author-produced and
author-evaluated with AI assistance. No independent replication or organizational
outcome improvement has been established.

## Repository supplement (not a method version) - 2026-08-07

### Status

- Added a non-normative GDAC Practice Kit.
- Public method version remains v1.4.
- Versioned v1.4 HTML/PDF artifacts and their root SHA-256 manifest remain
  unchanged.

### Added

- Applied the Owner-selected Creative Commons Attribution 4.0 International
  license to original repository material and added an attribution notice.
- A lightweight Outcome Contract template for material Agent work.
- An evidence-gated Project Closeout template.
- A prospective Method-Change Re-test template with explicit baseline,
  falsification, proportionality, and authority fields.
- A negative-result Harness closeout case note explaining what was retained and
  what was deliberately not transferred.

### Evidence and claim boundary

The source Harness established bounded internal engineering behavior, not
external adoption or a distinct standalone product need. Its runtime, adapters,
dashboards, synthetic pass rates, and unvalidated method candidates were not
imported into canonical GDAC.

## v1.4 — 2026-07-30

### Status

- Public bilingual method version.
- Minor governance-method release.
- Chinese and English editions now share one method version number.
- The method remains a practice-derived, iterating framework; it is not presented
  as an industry-validated standard.

### Added

- A versioned governance-learning loop:
  `Practice → Evidence → Proposed Change → Decision → Versioned Method → Re-test`.
- Explicit separation of observations, reproducible evidence, method proposals,
  decisions, versioned changes, migration impact, and unverified hypotheses.
- Review triggers for repeated cross-project friction, material control gaps or
  near misses, unclear authority boundaries, evidence that contradicts the
  current method, transferable new controls, new supervision or rollback needs,
  and major milestones with sufficient new evidence.
- Patch, minor, and major change boundaries.
- Three domain-neutral evidence rules:
  Capability Claim Attestation, Conclusion Provenance, and Derivation Integrity.
- A federated Strategic Board model: each project and the portfolio office keep
  separate challenge contexts and records; advice does not cross mandates
  automatically and never becomes management or implementation authority.
- Canonical portfolio display names:
  - `RiskFirewall AI — Product Risk Review`
    (`Complex Instruments · Second Line`)
  - `RiskFirewall AI — Risk Control Assurance`
    (`Transactions, Processes & AI Actions · Third Line`)

### Evidence basis

The three evidence rules were supported by read-only cross-project review of
authoritative ledgers and committed snapshots in two application contexts.
The applications do not implement identical systems. Private evidence references
remain in their project records and are not exposed here.

### Known limits retained

- A provider interface, fixture, mock, or `agent-ready` structure does not prove
  live Agent execution.
- No portfolio-level claim of provider-attested live execution, automated
  decision-making, production validation, or a deployed firewall is made.
- Source authenticity and semantic sufficiency may still require human review.
- A hash proves object identity and immutability, not downstream semantic
  derivation.
- Application-specific limitations and human-review maturity remain separate
  from the domain-neutral method.

### Migration impact

- Existing repository names, technical identifiers, historical version labels,
  commit references, and hashes remain valid.
- Public narratives should use the canonical portfolio display names while
  retaining repository or technical identifiers where traceability requires them.
- `RiskFirewall AI` must remain a portfolio brand, not a fourth repository or a
  capability claim.
- Existing workflows should audit execution claims, human-conclusion provenance,
  and decision-critical `raw → draft → conclusion` links in proportion to risk.
- No application project is required to adopt an identical implementation.

## English edition v1.3 — 2026-07-28

- Published the first English edition.
- Preserved the method structure and practice records from the initial Chinese
  publication.

## Chinese edition v1.2 — 2026-07-28

- Published the initial Chinese whitepaper.
- Established the Owner-led mandate, authority model, operating loop,
  organizational memory, read-only offices, practice records, and acceptance gate.
