# ADR-018: Project repository presentation without evaluating repository truth

- **Status:** Accepted
- **Date:** 2026-08-30
- **Tracking:** [Identity issue #54](https://github.com/egohygiene/identity/issues/54), [Hygiene issue #22](https://github.com/egohygiene/hygiene/issues/22)
- **Decision owners:** Identity maintainers and repository identity owners

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

## Consequences

- Holon and repository tooling can consume one stable, renderer-neutral
  manifest without importing Identity internals.
- Hosted image and badge providers are optional because local SVG and PNG
  artifacts are complete.
- Organization defaults are visible in provenance, and product overrides need
  exact human approval.
- Private and missing-evidence cases remain explicit instead of silently
  disappearing or rendering as passing.
- Profile upgrades require a reviewed lock update rather than a runtime fetch.

## Alternatives rejected

- **Let Identity run Hygiene validation:** transfers conformance authority to a
  brand renderer and couples release timing.
- **Fetch the profile or evidence during rendering:** breaks offline,
  reproducible generation and makes builds depend on mutable external state.
- **Emit a hosted badge URL only:** introduces an avoidable availability and
  privacy dependency and weakens local fallback behavior.
- **Rewrite README files from Identity:** crosses the visual-asset boundary and
  risks deleting repository-owned explanation.

## Reconsider when

Revisit when Hygiene activates or replaces the profile, when a new major
changes evidence semantics, or when a consumer needs an additional immutable
asset format. Do not loosen the evidence-authority or README-ownership
boundaries as part of a visual-only upgrade.
