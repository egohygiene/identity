# ADR-008: Encode platform metadata as versioned first-party profiles

- **Status:** Accepted
- **Date:** 2026-08-20
- **Issue:** [#7](https://github.com/egohygiene/identity/issues/7)

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

## Consequences

- Platform drift becomes a profile/schema update rather than a core rewrite.
- The checklist can report missing, candidate, approved, generated, stale,
  invalid, verified, published, and not-applicable states.
- Some provider setup and subjective review remain human checklist items rather
  than schema assertions.

## Exit strategy

Serializers and provider-specific validators are replaceable behind profile
contracts. A profile revision includes evidence, migration impact, fixtures,
and an effective version.

## Evidence

- [Open Graph protocol](https://ogp.me/)
- [Web Application Manifest](https://www.w3.org/TR/appmanifest/)
- [WHATWG icon link type](https://html.spec.whatwg.org/multipage/links.html#rel-icon)
- [GitHub repository social preview](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview)
- [Apple web application icons](https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/SafariWebContent/ConfiguringWebApplications/ConfiguringWebApplications.html)
- [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/)

