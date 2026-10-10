---
schema: "egohygiene.architecture-decision/v1"
id: "ADR-005"
title: "Publish curated JSON Schemas and validate them offline"
status: "accepted"
date: "2026-10-10"
decision_scope: "repository"
visibility: "public"
owners: ["egohygiene/identity"]
issue: "https://github.com/egohygiene/identity/issues/69"
pull_request: "https://github.com/egohygiene/identity/pull/92"
related: ["ADR-004", "ADR-012"]
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
    url: "https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-005-json-schema-contract.md"
    description: "Immutable pre-canonicalization record preserving its historical wording, date, status claim, and provenance."
  - type: "commit"
    url: "https://github.com/egohygiene/identity/commit/13c0824090755587efc3f65dca4638f6d8186374"
    description: "Original record introduction; evidence of recorded history rather than proof of historical human approval."
  - type: "implementation"
    url: "https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/src/v1_consumer/preflight.rs"
    description: "Inspected implementation or governing source contract; bounded evidence, not a newly executed verification result."
approval:
  date: "2026-10-10"
  by: "szmyty"
  evidence: "https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806"
exceptions: []
---

# ADR-005: Publish curated JSON Schemas and validate them offline

## Context

The source contract needs validation, editor completion, stable diagnostics,
and migrations across a Rust CLI and JavaScript consumers. Structural schema
validation cannot express every filesystem, semantic, or approval invariant.

## Decision

Adopt JSON Schema Draft 2020-12 for published `.identity/` contracts. Curate the
public schemas directly and bind them to explicit version identifiers. Adapt
the Rust `jsonschema` crate behind an offline validation port, disabling remote
resolution and unused network/TLS features. Vendor referenced schemas and
meta-schemas with checksums.

Layer first-party semantic validation after structural validation. Keep
migrations as explicit plan/apply domain use cases with rollback evidence.
Reject generated schemas and generic transformation libraries as the canonical
contract or migration authority.

## Alternatives considered and rejected

The original Decision section above preserves its rejected alternatives verbatim. No additional contemporaneous alternatives or rejection rationale were established by this migration.

## Consequences and tradeoffs

- Editors and non-Rust consumers can understand the public contract.
- Rust types and schemas need drift/conformance fixtures.
- Offline reference resolution and stable diagnostic mapping are required.
- Schema-valid input may still fail semantic, license, provenance, or approval
  checks.

## Implementation and evidence links

- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12)
- [Rust `jsonschema`](https://github.com/Stranger6667/jsonschema)

The inspected runtime embeds the Python standard-library validator selected by ADR-012. Cargo.toml does not include the originally intended Rust jsonschema port. The curated schemas and offline boundary are present, while the intended port and full vendoring/conformance requirements remain in progress as clarified by N005 below.

[Inspected source](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/src/v1_consumer/preflight.rs). The front-matter implementation status is independent of human acceptance. No new runtime, browser, release, or deployment verification is claimed.

[PR #20](https://github.com/egohygiene/identity/pull/20) introduced the original record in [commit `13c0824090755587efc3f65dca4638f6d8186374`](https://github.com/egohygiene/identity/commit/13c0824090755587efc3f65dca4638f6d8186374) on 2026-08-20. That introduction does not prove a historical approval date.

## Replacement or exit strategy

Another Draft 2020-12 validator may replace `jsonschema` if it passes the shared
valid/invalid corpus and diagnostic contract. Changing schema drafts or public
keywords requires a compatibility decision and migration.

## Follow-up work

Validate the final canonical corpus and index through the pinned shared tools at an immutable source revision. Preserve current implementation limitations and obtain separate evidence for future capability, release, and publication claims. Acceptance of this direction does not require completing every planned adapter before ADR source admission.

## Current human disposition — 2026-10-10

Maintainer `szmyty` explicitly retained this direction now under [R1 at `418aa9757898b6c09b4f01eface522778cff90e8`](https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md). The [durable approval](https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806) was recorded by Codex on the maintainer's behalf. The canonical date and approval date record this current human disposition; they do not backdate acceptance to the legacy record date or establish additional implementation or publication authority.

## Approved clarification — 2026-10-10

The following N005 text is preserved verbatim from the approved R1 packet.

### N005 — Intended Rust validator and current v1 authority

Retain curated Draft 2020-12 schemas, offline validation, and separate semantic
and migration authority. Rust `jsonschema` remains the original intended but
unimplemented validation port. Current v1 validation uses the Python
standard-library validator selected by ADR-012 and embedded in Rust preflight.
Generic Draft 2020-12 engine equivalence and completed schema/meta-schema
vendoring are not claimed. Replacing the intended port requires the documented
conformance evidence and a reviewed decision.

This recommendation preserves the intended Rust port; it neither cancels it
nor schedules its implementation in the ADR publication checkpoint. A
maintainer preference to abandon that port needs a separately explicit change.

Evidence: [ADR-012](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-012-local-layered-identity-v1.md),
[preflight](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/src/v1_consumer/preflight.rs) and
[dependency manifest](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/Cargo.toml).

## Historical metadata and provenance

The following original metadata is preserved as historical evidence. Its status and date lines are legacy claims, not the current approval record. [Original record at `434f60c8b829c695b3bcd1a45faf5e0c114d37cf`](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-005-json-schema-contract.md).

- **Status:** Accepted
- **Date:** 2026-08-20
- **Issue:** [#7](https://github.com/egohygiene/identity/issues/7)
