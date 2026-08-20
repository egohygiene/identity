# ADR-005: Publish curated JSON Schemas and validate them offline

- **Status:** Accepted
- **Date:** 2026-08-20
- **Issue:** [#7](https://github.com/egohygiene/identity/issues/7)

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

## Consequences

- Editors and non-Rust consumers can understand the public contract.
- Rust types and schemas need drift/conformance fixtures.
- Offline reference resolution and stable diagnostic mapping are required.
- Schema-valid input may still fail semantic, license, provenance, or approval
  checks.

## Exit strategy

Another Draft 2020-12 validator may replace `jsonschema` if it passes the shared
valid/invalid corpus and diagnostic contract. Changing schema drafts or public
keywords requires a compatibility decision and migration.

## Evidence

- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12)
- [Rust `jsonschema`](https://github.com/Stranger6667/jsonschema)

