# ADR-012: Use local, layered Identity v1 source contracts

- **Status:** Accepted for Identity v1
- **Date:** 2026-08-21
- **Decision owner:** `egohygiene/identity`
- **Related issues:** #1, #9

## Context

Consumers need a recognizable organization family without surrendering product
identity or depending on mutable cross-repository source. The incubated v0 TOML
contract selected profiles and creative sources, but it could not express
organization inheritance, reviewed overrides, interoperable semantic tokens,
complete provenance, or stable automation diagnostics.

## Decision

Identity v1 uses a closed JSON project manifest that pins local token layers by
SHA-256. Organization-default DTCG documents resolve first; one product layer
resolves last. Replacing an inherited token requires a reason and human
approval reference. Aliases resolve only after merge and fail closed when
missing, cyclic, or type-incompatible.

The manifest names separate local boundaries for target selection, provenance,
approvals, creative guidance, approved sources, candidates, and references.
The standard-library validator reads those boundaries without network or write
authority and emits stable `identity.diagnostics/v1` records.

## Consequences

- Consumers can review the exact organization snapshot they inherit.
- Products express intentional differences without forking the token model.
- DTCG documents remain framework-neutral source while CSS, Tailwind, and other
  formats remain projections.
- Asset licensing, provenance, accessibility metadata, usage constraints, and
  approval are available before generation.
- Updating organization defaults requires a reviewed local snapshot/digest
  change rather than an implicit default-branch read.
- The contract is more explicit than v0 and requires a review-guided migration.

## Rejected alternatives

### Resolve organization defaults from a mutable remote branch

Rejected because validation would become network-dependent and non-reproducible.

### Copy final organization tokens into every product without layer identity

Rejected because inherited values and intentional overrides would become
indistinguishable.

### Make a projection format the canonical token model

Rejected because CSS, Tailwind, Style Dictionary, and renderer needs change at
different rates and should remain replaceable adapters.

### Accept unknown fields for future flexibility

Rejected because silent typos and ambiguous meaning undermine compatibility.
Extensibility uses explicit dotted namespaces and versioned contracts.

## Reconsider when

A portable, content-addressed standard can express the same local inheritance,
override intent, human authority, asset governance, and offline diagnostics
without introducing mutable or provider-specific coupling.
