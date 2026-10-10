---
schema: "egohygiene.architecture-decision/v1"
id: "ADR-004"
title: "Use DTCG 2025.10 as the token contract"
status: "accepted"
date: "2026-10-10"
decision_scope: "repository"
visibility: "public"
owners: ["egohygiene/identity"]
issue: "https://github.com/egohygiene/identity/issues/69"
pull_request: "https://github.com/egohygiene/identity/pull/92"
related: ["ADR-005", "ADR-008", "ADR-012"]
supersedes: []
superseded_by: []
affected_repositories: ["egohygiene/identity"]
affected_contracts: []
implementation_status: "in_progress"
evidence:
  - type: "approval"
    url: "https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806"
    description: "Explicit maintainer szmyty disposition on 2026-10-10 for R1; recorded by Codex on their behalf, not inferred from merge or implementation."
  - type: "documentation"
    url: "https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md"
    description: "Approved R1 recommendation set and exact scope clarifications at the reviewed immutable packet commit."
  - type: "documentation"
    url: "https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-004-dtcg-token-contract.md"
    description: "Immutable pre-canonicalization record preserving its historical wording, date, status claim, and provenance."
  - type: "commit"
    url: "https://github.com/egohygiene/identity/commit/13c0824090755587efc3f65dca4638f6d8186374"
    description: "Original record introduction; evidence of recorded history rather than proof of historical human approval."
  - type: "implementation"
    url: "https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/contracts/v1/tokens.schema.json"
    description: "Inspected implementation or governing source contract; bounded evidence, not a newly executed verification result."
approval:
  date: "2026-10-10"
  by: "szmyty"
  evidence: "https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806"
exceptions: []
---

# ADR-004: Use DTCG 2025.10 as the token contract

## Context

Identity needs interoperable design tokens without confusing tokens with the
entire Brand Kit. It also needs multiple platform projections without coupling
canonical consumer intent to a transformer implementation.

## Decision

Adopt the stable DTCG Format Module 2025.10 for token concepts in the v1
`.identity/` contract. Identity owns version negotiation, semantic validation,
inheritance across brand sources, diagnostics, and migrations. Use namespaced
DTCG extensions only where token-specific metadata cannot be represented by the
standard. Model voice, assets, target profiles, approval, licenses, and
provenance in Identity schemas outside the token document.

Adapt Style Dictionary as an optional projection adapter over the already
validated and resolved token model. It must not own parsing, merge precedence,
canonical storage, or migrations. Reject Style Dictionary and an Identity-only
token dialect as canonical token truth.

## Alternatives considered and rejected

The original Decision section above preserves its rejected alternatives verbatim. No additional contemporaneous alternatives or rejection rationale were established by this migration.

## Consequences and tradeoffs

- Token exchange remains tool-neutral and DTCG-compatible.
- Style Dictionary's incomplete 2025.10 support is isolated from canonical
  semantics.
- The core must implement and test DTCG rules it claims to support.
- Additional Brand Kit concepts require explicit Identity schemas.

## Implementation and evidence links

- [DTCG Format Module 2025.10](https://www.designtokens.org/tr/2025.10/format/)
- [Style Dictionary DTCG support status](https://styledictionary.com/info/dtcg/)
- [Style Dictionary configuration and hooks](https://styledictionary.com/reference/config/)

The inspected token schema and validator implement a bounded DTCG-shaped subset. Complete DTCG 2025.10 conformance and the optional Style Dictionary adapter are not established, so implementation remains in progress. The approved N004 clarification below governs these current-scope claims.

[Inspected source](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/contracts/v1/tokens.schema.json). The front-matter implementation status is independent of human acceptance. No new runtime, browser, release, or deployment verification is claimed.

[PR #20](https://github.com/egohygiene/identity/pull/20) introduced the original record in [commit `13c0824090755587efc3f65dca4638f6d8186374`](https://github.com/egohygiene/identity/commit/13c0824090755587efc3f65dca4638f6d8186374) on 2026-08-20. That introduction does not prove a historical approval date.

## Replacement or exit strategy

A token transformer can replace Style Dictionary by passing normalized-token
contract fixtures. A future DTCG module is adopted through a versioned parser
and migration; canonical source is never rewritten for a transformer alone.

## Follow-up work

Validate the final canonical corpus and index through the pinned shared tools at an immutable source revision. Preserve current implementation limitations and obtain separate evidence for future capability, release, and publication claims. Acceptance of this direction does not require completing every planned adapter before ADR source admission.

## Current human disposition — 2026-10-10

Maintainer `szmyty` explicitly retained this direction now under [R1 at `418aa9757898b6c09b4f01eface522778cff90e8`](https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md). The [durable approval](https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806) was recorded by Codex on the maintainer's behalf. The canonical date and approval date record this current human disposition; they do not backdate acceptance to the legacy record date or establish additional implementation or publication authority.

## Approved clarification — 2026-10-10

The following N004 text is preserved verbatim from the approved R1 packet.

### N004 — DTCG target and implemented subset

Retain DTCG Format Module 2025.10 as the target token interchange standard.
Identity v1 currently implements the bounded subset declared by its token
schema and validator; complete 2025.10 conformance is not established.
Style Dictionary remains an optional downstream adapter, not a current
runtime dependency or canonical authority.

Evidence: [token schema](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/contracts/v1/tokens.schema.json) and
[validator](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/scripts/validate_identity.py).

## Historical metadata and provenance

The following original metadata is preserved as historical evidence. Its status and date lines are legacy claims, not the current approval record. [Original record at `434f60c8b829c695b3bcd1a45faf5e0c114d37cf`](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-004-dtcg-token-contract.md).

- **Status:** Accepted
- **Date:** 2026-08-20
- **Issue:** [#7](https://github.com/egohygiene/identity/issues/7)
