---
schema: egohygiene.architecture-decision/v1
id: ADR-007
title: Separate font inspection, rendering, subsetting, and approval
status: accepted
date: '2026-10-10'
decision_scope: repository
visibility: public
owners:
- egohygiene/identity
issue: https://github.com/egohygiene/identity/issues/69
pull_request: https://github.com/egohygiene/identity/pull/92
related: []
supersedes: []
superseded_by: []
affected_repositories:
- egohygiene/identity
affected_contracts: []
implementation_status: not_started
evidence:
- type: approval
  url: https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806
  description: szmyty approved R1 at 418aa9757898b6c09b4f01eface522778cff90e8, retaining ADR-007 with its scope qualifiers and exact N007 note.
- type: documentation
  url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-007-font-tooling-boundaries.md
  description: Immutable original record preserves historical wording and declared metadata; its legacy label is not the current approval evidence.
- type: documentation
  url: https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md
  description: Exact approved R1 review packet, including N007 and its evidence and implementation limits.
- type: documentation
  url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/README.md
  description: Current v1 runtime requires Python independently of the planned optional font adapters.
approval:
  date: '2026-10-10'
  by: szmyty
  evidence: https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806
exceptions: []
---

# ADR-007: Separate font inspection, rendering, subsetting, and approval

## Context

Fonts are both untrusted binary inputs and licensed creative works. Inspection,
text shaping, subsetting, and legal approval have different failure and
authority boundaries.

## Decision

Adapt Fontations `read-fonts`/`skrifa` for metadata inspection and use the font
stack selected transitively with `resvg` for rendering. Adapt an exactly pinned
fontTools `pyftsubset` subprocess only for profiles that request subsetting and
whose license evidence explicitly permits modification/subsetting.

Do not download fonts during a build. Canonical source identifies approved font
bytes and license evidence by checksum. Reject license inference from a family
name, provider URL, or embedded metadata alone. Defer a Rust-native subsetter
until corpus parity establishes equivalent OpenType behavior.

## Alternatives considered and rejected

The original Decision section above records its rejected or deferred
approaches. No additional historical alternatives or rationale are inferred
by this migration.

## Consequences and tradeoffs

- Rendering and inspection remain native while mature subsetting remains
  available behind an isolated optional adapter.
- Python is not required for profiles that do not subset fonts.
- Subsetting failures cannot silently fall back to shipping an unapproved full
  font.
- Font fixtures need malicious-input, language-coverage, variations, shaping,
  and reproducibility tests.

## Implementation and evidence links

The optional Fontations inspection and fontTools subsetting adapters are not
started in the inspected source. This status concerns those selected adapters,
not the separate existing renderer or embedded v1 source validator. See N007
for the approved Python-runtime correction and its exact source evidence.

### Original evidence links

- [Google Fonts Fontations](https://github.com/googlefonts/fontations)
- [fontTools documentation](https://fonttools.readthedocs.io/en/latest/)

The immutable implementation and current human-disposition sources are linked
in front matter. The accepted direction includes the dated R1 clarification
below; implementation and verification remain separate from approval.

## Replacement or exit strategy

Replace either inspection or subsetting independently through their ports. A
Rust subsetter can replace fontTools after matching the approved corpus,
metadata preservation, checksum stability, and license evidence behavior.

## Follow-up work

Implement the optional font adapters only with exact dependency pins and
reviewed corpus evidence, preserving the rights and failure boundaries in N007.

## Historical metadata and provenance

These original metadata lines are preserved as historical claims. Their dates
and status wording are not backdated proof of human approval. The canonical
date and approval object record the actual 2026-10-10 disposition.

- **Status:** Accepted
- **Date:** 2026-08-20
- **Issue:** [#7](https://github.com/egohygiene/identity/issues/7)

[Original record at the reviewed source boundary](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-007-font-tooling-boundaries.md).
[Explicit human disposition](https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806) approves
[R1 at its immutable packet revision](https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md).
The original substantive prose is preserved below the canonical headings;
the dated approved clarification governs the current scope where it qualifies
a historical statement. No historical approval date or new test result is inferred.

## Approved clarification — 2026-10-10

### N007 — Python requirement and optional font adapters

Skipping font subsetting does not require the fontTools adapter. Identity v1
execution nevertheless requires Python 3.11+ for its embedded, isolated
standard-library source validator; the earlier blanket no-Python consequence
is inaccurate for current v1. Fontations inspection and exactly pinned
fontTools subsetting remain planned optional adapters, not implemented
capabilities established by the current source and dependency manifests.
Retain the separate inspection, rendering, subsetting and rights boundaries,
approved local bytes, explicit subsetting permission and fail-closed behavior.
Adoption of either font adapter still requires exact pins and corpus evidence.

Evidence: [runtime requirements](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/README.md),
[preflight](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/src/v1_consumer/preflight.rs) and
[dependencies](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/Cargo.toml).
