# ADR-004: Use DTCG 2025.10 as the token contract

- **Status:** Accepted
- **Date:** 2026-08-20
- **Issue:** [#7](https://github.com/egohygiene/identity/issues/7)

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

## Consequences

- Token exchange remains tool-neutral and DTCG-compatible.
- Style Dictionary's incomplete 2025.10 support is isolated from canonical
  semantics.
- The core must implement and test DTCG rules it claims to support.
- Additional Brand Kit concepts require explicit Identity schemas.

## Exit strategy

A token transformer can replace Style Dictionary by passing normalized-token
contract fixtures. A future DTCG module is adopted through a versioned parser
and migration; canonical source is never rewritten for a transformer alone.

## Evidence

- [DTCG Format Module 2025.10](https://www.designtokens.org/tr/2025.10/format/)
- [Style Dictionary DTCG support status](https://styledictionary.com/info/dtcg/)
- [Style Dictionary configuration and hooks](https://styledictionary.com/reference/config/)

