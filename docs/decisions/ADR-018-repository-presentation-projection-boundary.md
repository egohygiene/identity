---
schema: egohygiene.architecture-decision/v1
id: ADR-018
title: Project repository presentation without evaluating repository truth
status: accepted
date: "2026-10-10"
decision_scope: repository
visibility: public
owners:
  - egohygiene/identity
issue: https://github.com/egohygiene/identity/issues/54
pull_request: https://github.com/egohygiene/identity/pull/64
related: []
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/identity]
affected_contracts: []
implementation_status: implemented
evidence:
  - type: approval
    url: https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806
    description: Explicit human approval of R1 at packet 418aa9757898b6c09b4f01eface522778cff90e8, retaining this direction now with its listed clarifications and scope limits.
  - type: documentation
    url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-018-repository-presentation-projection-boundary.md
    description: Immutable original record; historical prose, metadata and dates are preserved separately from the current human disposition.
  - type: documentation
    url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/contracts/REPOSITORY_PRESENTATION_V1.md
    description: Inspected contract and implementation boundary at the reviewed source revision; no new runtime or publication verification is implied.
  - type: implementation
    url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/scripts/render_repository_presentation.py
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

# ADR-018: Project repository presentation without evaluating repository truth

The canonical date records the explicit human disposition on 2026-10-10.
Original source prose and metadata are preserved below as historical evidence;
the approved R1 clarifications and scope limits govern their current reading.

## Context

Hygiene owns the repository-presentation profile, applicability, evidence-state
vocabulary, and badge claim policy. Identity owns approved visual assets and
their accessible projections. Combining those roles would allow a visual
renderer to declare that a repository passes policy, while copying profile
facts or fetching them from a moving branch would make output unverifiable.

README composition is a third authority. It belongs to repository tooling such
as Holon and Pace because those systems can preserve repository-authored prose,
show reviewable diffs, and limit changes to generated regions.

## Decision

Identity accepts two separate local inputs:

1. a reviewed `.identity/` repository-presentation source that selects an
   approved public banner asset, accessible text, organization defaults, and a
   bounded product override; and
2. an explicit Hygiene evidence document whose badge state, exact message,
   represented commit, and evidence URL are already present.

The source pins the Hygiene profile by ID, version, status, repository, full
commit, path, and normalized digest. The current compatible input is the
`1.0.0-alpha.1` proposed profile at Hygiene commit
`cb2ed63425d29abada2d2bbb43a3b3e59d11aeb8`. Consuming it does not activate
the profile.

The offline renderer validates both inputs and emits a framework-neutral JSON
descriptor, light/dark/high-contrast banner variants at 640, 1000, and 1600
pixels, static SVG and PNG files, a state-specific `Hygienic` badge, first-class
text fallbacks, an integrity manifest, and checksums. The renderer does not
collect evidence, infer a state, access the network, edit a README, or claim
that proposed policy is active.

Every non-passing state has its own exact Hygiene-owned message and rendered
bytes. The badge always binds the exact profile version, a full represented
commit, and a caller-supplied evidence destination. Prohibited certification
terms remain rejected.

## Alternatives considered and rejected

- **Let Identity run Hygiene validation:** transfers conformance authority to a
  brand renderer and couples release timing.
- **Fetch the profile or evidence during rendering:** breaks offline,
  reproducible generation and makes builds depend on mutable external state.
- **Emit a hosted badge URL only:** introduces an avoidable availability and
  privacy dependency and weakens local fallback behavior.
- **Rewrite README files from Identity:** crosses the visual-asset boundary and
  risks deleting repository-owned explanation.

These are the alternatives recorded in the historical source. No additional
contemporaneous alternatives or rationale are inferred.

## Consequences and tradeoffs

- Holon and repository tooling can consume one stable, renderer-neutral
  manifest without importing Identity internals.
- Hosted image and badge providers are optional because local SVG and PNG
  artifacts are complete.
- Organization defaults are visible in provenance, and product overrides need
  exact human approval.
- Private and missing-evidence cases remain explicit instead of silently
  disappearing or rendering as passing.
- Profile upgrades require a reviewed lock update rather than a runtime fetch.

## Implementation and evidence links

The inspected repository-presentation renderer and explicit-evidence contract
are present. The consumed Hygiene profile remains proposed. This implementation
status does not establish repository conformance, policy activation, fleet
rollout, or a freshly verified render.

[Original implementation PR #64](https://github.com/egohygiene/identity/pull/64),
[inspected contract](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/contracts/REPOSITORY_PRESENTATION_V1.md), and
[implementation source](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/scripts/render_repository_presentation.py)
provide the bounded evidence. Human approval is recorded separately in the
[explicit R1 disposition](https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806).

## Replacement or exit strategy

Revisit when Hygiene activates or replaces the profile, when a new major
changes evidence semantics, or when a consumer needs an additional immutable
asset format. Do not loosen the evidence-authority or README-ownership
boundaries as part of a visual-only upgrade.

## Follow-up work

Review profile upgrades with the owning Hygiene contract and preserve the
exact supplied evidence state. Keep README changes with repository tooling and
consumer review; do not infer passing conformance from rendered presentation.

## Historical metadata and provenance

The following metadata is reproduced from the original record. Its status
and dates are historical claims, not the date or proof of the current
approval.

- **Status:** Accepted
- **Date:** 2026-08-30
- **Tracking:** [Identity issue #54](https://github.com/egohygiene/identity/issues/54), [Hygiene issue #22](https://github.com/egohygiene/hygiene/issues/22)
- **Decision owners:** Identity maintainers and repository identity owners

Preserved from [immutable source `434f60c8b829c695b3bcd1a45faf5e0c114d37cf`](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-018-repository-presentation-projection-boundary.md).
The present disposition transcribes `szmyty`'s explicit approval of
[R1 at `418aa9757898b6c09b4f01eface522778cff90e8`](https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md);
it does not backdate acceptance or convert implementation into verification.

## Approved R1 scope qualifier — 2026-10-10

Retain now; the consumed proposed Hygiene profile remains proposed.
