---
schema: "egohygiene.architecture-decision/v1"
id: "ADR-001"
title: "Keep creative approval human-owned"
status: "accepted"
date: "2026-10-10"
decision_scope: "repository"
visibility: "public"
owners: ["egohygiene/identity"]
issue: "https://github.com/egohygiene/identity/issues/69"
pull_request: "https://github.com/egohygiene/identity/pull/92"
related: ["ADR-012", "ADR-013", "ADR-021"]
supersedes: []
superseded_by: []
affected_repositories: ["egohygiene/identity"]
affected_contracts: []
implementation_status: "implemented"
evidence:
  - type: "approval"
    url: "https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806"
    description: "Explicit maintainer szmyty disposition on 2026-10-10 for R1; recorded by Codex on their behalf, not inferred from merge or implementation."
  - type: "documentation"
    url: "https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md"
    description: "Approved R1 recommendation set and exact scope clarifications at the reviewed immutable packet commit."
  - type: "documentation"
    url: "https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-001-creative-approval-human-owned.md"
    description: "Immutable pre-canonicalization record preserving its historical wording, date, status claim, and provenance."
  - type: "commit"
    url: "https://github.com/egohygiene/identity/commit/5ec2d88ef5c1ace7e7782bd000b48183af0e47f2"
    description: "Original record introduction; evidence of recorded history rather than proof of historical human approval."
  - type: "implementation"
    url: "https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/contracts/IDENTITY_V1.md"
    description: "Inspected implementation or governing source contract; bounded evidence, not a newly executed verification result."
approval:
  date: "2026-10-10"
  by: "szmyty"
  evidence: "https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806"
exceptions: []
---

# ADR-001: Keep creative approval human-owned

## Context

- **Context:** Repository evidence and ecosystem ownership require an explicit durable boundary.

## Decision

- **Decision:** Keep creative approval human-owned.

## Alternatives considered and rejected

The original inline record does not identify alternatives or rejection rationale. That historical information remains unknown; this migration does not invent it.

## Consequences and tradeoffs

- **Consequences:** The choice improves ownership and predictability while requiring maintained contracts, validation, and migration discipline.

## Implementation and evidence links

The inspected source contract requires approved source bytes, provenance, and a human decision for the same subject. Studio handoff separately requires a named reviewer. This supports the implemented ownership boundary; validation of a record does not itself establish actual human approval.

[Inspected source](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/contracts/IDENTITY_V1.md). The front-matter implementation status is independent of human acceptance. No new runtime, browser, release, or deployment verification is claimed.

[PR #4](https://github.com/egohygiene/identity/pull/4) introduced the original record in [commit `5ec2d88ef5c1ace7e7782bd000b48183af0e47f2`](https://github.com/egohygiene/identity/commit/5ec2d88ef5c1ace7e7782bd000b48183af0e47f2) on 2026-08-19. That introduction does not prove a historical approval date.

## Replacement or exit strategy

- **Reconsider when:** New evidence shows that the boundary prevents standalone usefulness, safety, portability, or maintainability.

## Follow-up work

Validate the final canonical corpus and index through the pinned shared tools at an immutable source revision. Preserve current implementation limitations and obtain separate evidence for future capability, release, and publication claims. Acceptance of this direction does not require completing every planned adapter before ADR source admission.

## Current human disposition — 2026-10-10

Maintainer `szmyty` explicitly retained this direction now under [R1 at `418aa9757898b6c09b4f01eface522778cff90e8`](https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md). The [durable approval](https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806) was recorded by Codex on the maintainer's behalf. The canonical date and approval date record this current human disposition; they do not backdate acceptance to the legacy record date or establish additional implementation or publication authority.

## Historical metadata and provenance

The following original metadata is preserved as historical evidence. Its status and date lines are legacy claims, not the current approval record. [Original record at `434f60c8b829c695b3bcd1a45faf5e0c114d37cf`](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-001-creative-approval-human-owned.md).

- **Status:** Accepted as the current architectural direction
- **Date:** 2026-08-19

### Migration provenance recorded before the current disposition

The following preserved migration wording describes the earlier unresolved state. The current human disposition above resolves that authority gap without changing the original claim or inventing an earlier approval.

Extracted on 2026-10-10 without changing the original record body or status
claim. The legacy acceptance claim lacks durable human disposition evidence;
it is unresolved under the pinned Hygiene policy, not canonical acceptance.
See the [migration map](../decision-migration-2026-10-10.md).

[Original inline record and history](https://github.com/egohygiene/identity/blob/8aae2c6767d07714ea16bf0ea493e1f1ac399b6e/DECISIONS.md#adr-001-keep-creative-approval-human-owned).
