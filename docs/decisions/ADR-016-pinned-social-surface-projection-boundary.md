---
schema: egohygiene.architecture-decision/v1
id: ADR-016
title: Project social surfaces from pinned external facts
status: accepted
date: "2026-10-10"
decision_scope: repository
visibility: public
owners:
  - egohygiene/identity
issue: https://github.com/egohygiene/identity/issues/52
pull_request: https://github.com/egohygiene/identity/pull/55
related: []
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/identity]
affected_contracts: []
implementation_status: in_progress
evidence:
  - type: approval
    url: https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806
    description: Explicit human approval of R1 at packet 418aa9757898b6c09b4f01eface522778cff90e8, retaining this direction now with its listed clarifications and scope limits.
  - type: documentation
    url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-016-pinned-social-surface-projection-boundary.md
    description: Immutable original record; historical prose, metadata and dates are preserved separately from the current human disposition.
  - type: documentation
    url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/contracts/SOCIAL_SURFACES_V1.md
    description: Inspected contract and implementation boundary at the reviewed source revision; no new runtime or publication verification is implied.
  - type: implementation
    url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/scripts/render_social_surfaces.py
    description: Inspected bounded implementation at the reviewed source revision.
  - type: documentation
    url: https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md
    description: Exact R1 recommendations, dated clarifications and scope qualifiers approved by the human disposition.
approval:
  date: "2026-10-10"
  by: szmyty
  evidence: https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806
exceptions: []
---

# ADR-016: Project social surfaces from pinned external facts

The canonical date records the explicit human disposition on 2026-10-10.
Original source prose and metadata are preserved below as historical evidence;
the approved R1 clarifications and scope limits govern their current reading.

## Context

Social profile, header, post, and video requirements change independently of
brand source. Copying those requirements into Identity would make Identity a
second owner of third-party facts. Fetching them during compilation would make
builds mutable, non-reproducible, and dependent on network availability and
unclear redistribution rights. Conversely, a generic catalog cannot decide
which approved brand asset or copy a product should use.

## Decision

Keep the boundaries separate. Aether owns a reusable, rights-aware, versioned
social-surface catalog and its collection skill. Identity consumes only a
repository-local artifact locked by ID, version, and digest after confirming
that the catalog is stable, rights-approved, and included in its release.

Identity adds an optional reviewed selection source. Organization defaults map
catalog records to approved Identity assets and project metadata; products
must explicitly adopt each selection and may make separately approved bounded
overrides or exclusions. Generated output is an immutable renderer-neutral
package with catalog/source provenance, exact constraints, honest unknowns,
manifest, checksums, and a Press Kit handoff. It always denies publication
authority.

## Alternatives considered and rejected

- **Vendor platform specs into Identity:** creates duplicate ownership and
  update work while expanding third-party redistribution risk.
- **Fetch live specs during generation:** breaks offline reproducibility and
  makes the same reviewed source produce different output.
- **Generate every platform by default:** invents product intent and creates an
  unreviewable surface matrix.
- **Guess missing dimensions or safe zones:** makes unsupported facts look
  authoritative.
- **Let the Press Kit read `.identity/` directly:** turns a public consumer into
  a second source compiler and bypasses the generated integrity boundary.

These are the alternatives recorded in the historical source. No additional
contemporaneous alternatives or rationale are inferred.

## Consequences and tradeoffs

- Identity builds stay offline and deterministic.
- Platform facts have one reusable owner and brand facts remain canonical in
  Identity.
- No surface appears unless a project explicitly adopts it.
- Catalog rights or lifecycle rejection prevents projection even when the
  bytes and selected IDs otherwise look usable.
- Unknown safe zones and absent limits remain visible instead of becoming
  invented design guidance.
- Press Kits can consume one integrity-checked package rather than duplicate
  social metadata or assets.
- Current production use depends on a future Aether catalog release containing
  independently gathered, rights-approved official records.

## Implementation and evidence links

The inspected social-surface compiler and synthetic first-party fixtures
implement the contract boundary. Production catalog availability and freshness
were not established by this review, so end-to-end implementation remains
`in_progress`. No platform publication or fresh catalog verification is claimed.

[Original implementation PR #55](https://github.com/egohygiene/identity/pull/55),
[inspected contract](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/contracts/SOCIAL_SURFACES_V1.md), and
[implementation source](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/scripts/render_social_surfaces.py)
provide the bounded evidence. Human approval is recorded separately in the
[explicit R1 disposition](https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806).

## Replacement or exit strategy

Revisit if Aether publishes a new incompatible catalog major, Identity adopts
a separately reviewed copy-localization contract, or a consumer-owned renderer
needs a versioned final-media contract beyond these publish-ready inputs.

## Follow-up work

Review an admissible production catalog and exact consumer lock before
production use. Keep current-fact verification, final media rendering, account
selection, and publication with their respective owners.

## Historical metadata and provenance

The following metadata is reproduced from the original record. Its status
and dates are historical claims, not the date or proof of the current
approval.

- **Status:** Accepted
- **Date:** 2026-08-29
- **Tracking:** [Identity issue #52](https://github.com/egohygiene/identity/issues/52), [Aether issue #52](https://github.com/egohygiene/aether/issues/52)
- **Decision owners:** Identity maintainers and consumer identity owners

Preserved from [immutable source `434f60c8b829c695b3bcd1a45faf5e0c114d37cf`](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-016-pinned-social-surface-projection-boundary.md).
The present disposition transcribes `szmyty`'s explicit approval of
[R1 at `418aa9757898b6c09b4f01eface522778cff90e8`](https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md);
it does not backdate acceptance or convert implementation into verification.

## Approved R1 clarification — 2026-10-10

### N016 — External catalog availability

The admission rule remains stable, rights-approved, release-included catalog
input with an exact identity/version/digest lock. Identity's inspected fixtures
use synthetic first-party records. This review does not establish availability
or freshness of a production catalog; the original future-release wording is a
historical implementation statement.

Evidence: [social-surface contract](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/contracts/SOCIAL_SURFACES_V1.md).
