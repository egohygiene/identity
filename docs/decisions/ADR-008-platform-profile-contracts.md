---
schema: egohygiene.architecture-decision/v1
id: ADR-008
title: Encode platform metadata as versioned first-party profiles
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
implementation_status: in_progress
evidence:
- type: approval
  url: https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806
  description: szmyty approved R1 at 418aa9757898b6c09b4f01eface522778cff90e8, retaining ADR-008 with its scope qualifiers and exact N008 note.
- type: documentation
  url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-008-platform-profile-contracts.md
  description: Immutable original record preserves historical wording and declared metadata; its legacy label is not the current approval evidence.
- type: documentation
  url: https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md
  description: Exact approved R1 review packet, including N008 and its evidence and implementation limits.
- type: implementation
  url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/src/brandkit/profiles.rs
  description: Versioned typed output profiles implement bounded coverage; this is not complete platform coverage.
approval:
  date: '2026-10-10'
  by: szmyty
  evidence: https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806
exceptions: []
---

# ADR-008: Encode platform metadata as versioned first-party profiles

## Context

Open Graph, favicons, manifests, repository previews, Apple icons, and
structured data overlap but have different authorities, dimensions, safe
zones, formats, and lifecycle rules.

## Decision

Adopt primary platform standards and provider documentation as evidence for
versioned Identity target profiles. Implement typed serializers and validators
as first-party adapters over the resolved model. Each requirement records its
source, profile version, applicability, format, dimensions, safe area, byte
budget, accessibility metadata, and validation behavior.

Reject a universal flat asset checklist, hard-coded folklore, and a generic
metadata library as canonical truth. Consumer profiles distinguish required,
recommended, optional, legacy, and not-applicable targets.

## Alternatives considered and rejected

The original Decision section above records its rejected or deferred
approaches. No additional historical alternatives or rationale are inferred
by this migration.

## Consequences and tradeoffs

- Platform drift becomes a profile/schema update rather than a core rewrite.
- The checklist can report missing, candidate, approved, generated, stale,
  invalid, verified, published, and not-applicable states.
- Some provider setup and subjective review remain human checklist items rather
  than schema assertions.

## Implementation and evidence links

Versioned typed profiles and serializers are implemented for a bounded set of
outputs. The complete requirement metadata, platform coverage and lifecycle
reporting described here remain in progress. See N008 for the approved Aether
ownership and coverage limits.

### Original evidence links

- [Open Graph protocol](https://ogp.me/)
- [Web Application Manifest](https://www.w3.org/TR/appmanifest/)
- [WHATWG icon link type](https://html.spec.whatwg.org/multipage/links.html#rel-icon)
- [GitHub repository social preview](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview)
- [Apple web application icons](https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/SafariWebContent/ConfiguringWebApplications/ConfiguringWebApplications.html)
- [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/)

The immutable implementation and current human-disposition sources are linked
in front matter. The accepted direction includes the dated R1 clarification
below; implementation and verification remain separate from approval.

## Replacement or exit strategy

Serializers and provider-specific validators are replaceable behind profile
contracts. A profile revision includes evidence, migration impact, fixtures,
and an effective version.

## Follow-up work

Complete the remaining profile coverage and requirement evidence without
duplicating Aether-owned social-platform facts, as qualified by N008.

## Historical metadata and provenance

These original metadata lines are preserved as historical claims. Their dates
and status wording are not backdated proof of human approval. The canonical
date and approval object record the actual 2026-10-10 disposition.

- **Status:** Accepted
- **Date:** 2026-08-20
- **Issue:** [#7](https://github.com/egohygiene/identity/issues/7)

[Original record at the reviewed source boundary](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-008-platform-profile-contracts.md).
[Explicit human disposition](https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806) approves
[R1 at its immutable packet revision](https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md).
The original substantive prose is preserved below the canonical headings;
the dated approved clarification governs the current scope where it qualifies
a historical statement. No historical approval date or new test result is inferred.

## Approved clarification — 2026-10-10

### N008 — Platform-fact ownership and coverage

“First-party” describes Identity's projection profiles, serializers and
validators; it does not transfer ownership of reusable external platform
facts from Aether. Social-surface facts follow ADR-016's pinned external-catalog
boundary. Existing versioned profiles establish bounded implementation, not
complete delivery of every requirement field, lifecycle state or platform
mentioned in this record. Historical source-verification dates are not current
platform verification.

Evidence: [typed profiles](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/src/brandkit/profiles.rs) and
[social-surface contract](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/contracts/SOCIAL_SURFACES_V1.md).
