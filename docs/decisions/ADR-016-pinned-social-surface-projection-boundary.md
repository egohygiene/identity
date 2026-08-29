# ADR-016: Project social surfaces from pinned external facts

- **Status:** Accepted
- **Date:** 2026-08-29
- **Tracking:** [Identity issue #52](https://github.com/egohygiene/identity/issues/52), [Aether issue #52](https://github.com/egohygiene/aether/issues/52)
- **Decision owners:** Identity maintainers and consumer identity owners

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

## Consequences

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

## Alternatives rejected

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

## Reconsider when

Revisit if Aether publishes a new incompatible catalog major, Identity adopts
a separately reviewed copy-localization contract, or a consumer-owned renderer
needs a versioned final-media contract beyond these publish-ready inputs.
