---
schema: aether.architecture-document/v1
id: identity-roadmap
title: Identity Roadmap
kind: architecture-document
version: 1.0.0
status: active
owners:
  - egohygiene
created: 2026-08-19
updated: 2026-08-22
governed_by:
  - architecture-roadmap
depends_on:
  - identity-vision
  - identity-pillars
  - identity-architecture
  - identity-decisions
related:
  - identity-purpose
  - identity-principles
  - identity-manifesto
  - identity-epistemology
supersedes: []
---

# Identity Roadmap

## Strategic context

Identity is evolving from an incubated product-identity CLI into a standalone Brand Kit generator. This document maps durable capability evolution to the executable [roadmap issue #5](https://github.com/egohygiene/identity/issues/5). It describes dependency order and release evidence, not promised dates.

## Umbrella outcomes

The original portfolio issues remain outcome-level anchors:

- [#1](https://github.com/egohygiene/identity/issues/1) — canonical identity and design-token schema;
- [#2](https://github.com/egohygiene/identity/issues/2) — compiler and distributable packages;
- [#3](https://github.com/egohygiene/identity/issues/3) — visual-motion validation.

They close only when the refining issues below provide implementation and validation evidence.

## Dependency-ordered waves

| Wave | Outcome | Issues | Exit evidence |
| --- | --- | --- | --- |
| 0 — Product and foundations | Accept the Brand Kit boundary and select replaceable foundations | #6, #7 | Active product contract, boundary review, toolchain ADRs, dependency policy, proof of high-risk integrations |
| 1 — Extraction and canonical contracts | Establish an independent CLI and versioned consumer-owned source | #8, #9 | Parity tests, migration fixtures, published schemas, deterministic merge/override diagnostics |
| 2 — Compiler and packages | Produce reproducible projections through stable adapter contracts | #10, #11 | Offline core tests, adapter contract tests, deterministic outputs, packages, manifests, checksums |
| 3 — Trust and governance | Make quality, accessibility, provenance, voice, and approval testable | #12, #13 | Release-blocking validation, human-review evidence, usage/voice schemas, recovery guidance |
| 4 — Public product experience | Present, preview, approve, download, and publish a Brand Kit | #14, #15, #16 | Accessible renderer, mutation-safe studio, immutable publication contract, deployed route checks |
| 5 — Proof and release | Prove variation across consumers and publish v1.0.0 | #17, #18 | Empathy/OptiFlow pilots, clean-room quickstart, compatibility suite, attestations, stable release |

## Current wave

Wave 0 is complete. Wave 1 has the independently extracted CLI from #8 and the
implemented v1 source/schema/validation boundary from #9; Empathy's pinned
consumer transition remains the final cross-repository extraction gate.

Wave 2 implementation is complete in Identity after #10 and #11. #10 provides
the deterministic offline compiler core, adapter SDK, mutation-free plans,
manifests, transactional generated-state apply, and explicit recovery. #11 adds
nine versioned Brand Kit output profiles, concrete
token/web/document/metadata/vector/raster/archive adapters, deterministic
package indexes/checksums, subset compatibility, and byte-identical package
proof across clean repositories.

Wave 3 is now substantially implemented. #12 established the shared
`identity.quality-report/v1` evidence harness, package/publication scopes,
release-blocking accessibility/provenance/license/reproducibility/visual checks,
visual baselines, explicit skipped coverage, and human-review evidence. This #3
change adds framework-neutral visual-motion governance to that same release
decision: Astryx-informed adopt/adapt/reject rules, purpose budgets,
reduced-motion fallbacks, deterministic capture/provenance contracts, motion
fixtures, and semantic human-review boundaries. #13 is now the remaining Wave 3
gate before the public renderer and consumer pilots.

The umbrella #2 remains open despite the Wave 2 implementation milestone. Its
remaining acceptance evidence is the real Empathy and OptiFlow consumer proof
owned by #17 after the required quality/governance and renderer dependencies
land. This prevents package implementation from being mistaken for successful
fleet consumption.

Wave 0 establishes decisions that constrain every implementation PR:

### #6 — Brand Kit product contract

**Exit criteria:**

- ownership and non-ownership are explicit;
- compiler, packages, renderer, studio, consumer, evidence, and publication interfaces are named;
- canonical, generated, transient, and published authority are distinct;
- personas, workflows, surfaces, failure states, and measurable signals are documented;
- `/identity` is canonical and `/brand-kit` is a redirect;
- capabilities use implemented, accepted, proposed, and deferred honestly;
- architecture links, document front matter, and repository boundaries validate.

### #7 — Standards, libraries, and framework adapters

**Exit criteria:**

- adopt/adapt/reject decisions are evidence-backed;
- dependencies have bounded purposes and replacement strategies;
- local and CI output assumptions are proven;
- no framework or library becomes canonical domain truth.

**Accepted evidence:**

- [foundation comparison matrix](docs/evaluations/brand-kit-foundations.md);
- [toolchain and boundary ADRs](DECISIONS.md);
- [dependency policy](docs/DEPENDENCY_POLICY.md);
- [deterministic DTCG projection-boundary proof](experiments/dtcg-projection-boundary/README.md).

## v1 capability map

| v1 promise | Owning issues | Required tests/evidence |
| --- | --- | --- |
| Initialize or migrate a project-owned identity | #8, #9 | Command parity, schema, valid/invalid fixtures, migration and rollback tests |
| Resolve organization defaults and product overrides | #9, #17 | Merge/conflict diagnostics and contrasting consumer snapshots |
| Plan before mutation | #10 | Mutation-free plan tests covering writes, replacements, removals, warnings, and approvals |
| Generate deterministic target profiles | #10, #11 | Offline unit/integration tests, adapter contracts, byte-identical outputs/manifests, checksum stability |
| Block inaccessible, unlicensed, or untraceable releases | #3, #12, #13 | #12 quality-report/accessibility/provenance/license/visual/reproducibility gates and #3 visual-motion/capture/provenance gates are implemented; #13 guidance/approval integration remains |
| Distribute portable Brand Kit packages | #11, #18 | Versioned profile/package contracts, checksums, deterministic archive, consumer installation, clean-room build, and release provenance |
| Render and preview an understandable Brand Kit | #14, #15 | Accessibility, responsive, link, download, visual regression, and mutation-isolation tests |
| Publish the organization Brand Kit at `/identity` | #16 | Immutable handoff, metadata, redirect, deployment smoke test, and rollback evidence |
| Preserve product variation within a family | #17 | Empathy and OptiFlow inheritance/override evidence |
| Release a supportable v1.0.0 | #18 | Platform matrix, documentation, SBOM/license inventory, checksums, attestations, and all release gates |

## Cross-cutting requirements

Every wave must preserve:

- human authority, privacy, accessibility, licensing, and provenance;
- canonical/generated/transient/publication boundaries;
- deterministic local and CI behavior for supported projections;
- versioned cross-repository contracts and immutable dependencies;
- implementation, documentation, tests, migration, and rollback agreement;
- visible uncertainty, partial coverage, unsupported behavior, and deferred work.

## Deferred direction

Managed collaboration, enterprise controls, marketplaces, provider-specific generative systems, and a conversational organization compiler remain outside v1. The architecture preserves ports for later work without making those services prerequisites or implying support before evidence exists.

## Execution policy

Work one scoped PR at a time. Architecture and specification changes land before dependent implementation. Pause after each wave for review. If work belongs to another repository, open a follow-up there instead of expanding Identity's boundary.
