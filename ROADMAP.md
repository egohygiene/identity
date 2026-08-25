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
updated: 2026-08-24
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

<!-- BEGIN ROADMAP EXECUTION SNAPSHOT -->
<!-- roadmap-manifest
schema: hygiene.roadmap/v1alpha1
repository: egohygiene/identity
visibility: public
publication: central
route: /roadmap/identity/
updated: 2026-08-24
-->
## 2026-08-24 execution snapshot

> This evidence-reconciled snapshot is the issue-generation and visual-roadmap handoff. The longer-horizon strategy below remains canonical context; generated HTML, JSON, progress, issue plans, and commit lists are projections.

**Lifecycle:** strong pre-release alpha  
**Current gate:** Complete voice and approval evidence in issues #13 and #8 before building the renderer and studio.  
**North-star outcome:** A deterministic, governed Brand Kit v1 whose source decisions, generated assets, and approvals remain traceable.

### Visual roadmap publication

**Mode:** `central`  
**Route:** `/roadmap/identity/`  
**Current publication evidence:** Generated artifacts through CI; no Pages site or public product route observed.

Publish the public-safe projection through egohygiene.io at /roadmap/identity/. This repository owns intent and acceptance evidence; it does not add a second site deployment.

### Quest line

<!-- roadmap-step
id: IDN-Q01
status: complete
depends_on: []
issues: []
-->
#### IDN-Q01 — Establish deterministic brand compilation

**State:** `complete`  
**Depends on:** None

**Outcome:** A compiler and nine profiles generate validated brand artifacts.

**Exit criteria:**

- [x] All declared profiles compile deterministically.
- [x] Quality checks are green.

**Current evidence:**

- The audit observed a working compiler, nine profiles, and green quality checks.

<!-- roadmap-step
id: IDN-Q02
status: active
depends_on: [IDN-Q01]
issues: [8, 13]
-->
#### IDN-Q02 — Complete voice and approval evidence

**State:** `active`  
**Depends on:** `IDN-Q01`

**Outcome:** Brand decisions include approved voice guidance and evidence rather than generated assets alone.

**Exit criteria:**

- [ ] Issues #13 and #8 meet their acceptance criteria.
- [ ] Approvals link to the exact source and generated artifact versions.

**Current evidence:**

- Issues #13 and #8 form the current evidence gate.

<!-- roadmap-step
id: IDN-Q03
status: planned
depends_on: [IDN-Q02]
issues: [14, 15]
-->
#### IDN-Q03 — Build the renderer and studio

**State:** `planned`  
**Depends on:** `IDN-Q02`

**Outcome:** Issues #14 and #15 provide a usable way to inspect and generate the Brand Kit.

**Exit criteria:**

- [ ] The renderer covers all nine profiles.
- [ ] Studio changes round-trip through governed source files.

**Current evidence:**

- Issues #14 and #15 define the renderer and studio backlog.

<!-- roadmap-step
id: IDN-Q04
status: planned
depends_on: [IDN-Q03]
issues: [16]
-->
#### IDN-Q04 — Publish the public identity route

**State:** `planned`  
**Depends on:** `IDN-Q03`

**Outcome:** Issue #16 exposes an accessible, version-aware identity surface.

**Exit criteria:**

- [ ] The public route is deployed and linked from the organization portal.
- [ ] Generated assets link back to source evidence.

**Current evidence:**

- Issue #16 tracks the public route.
- No Pages deployment was observed.

<!-- roadmap-step
id: IDN-Q05
status: planned
depends_on: [IDN-Q04]
issues: [17, 18]
-->
#### IDN-Q05 — Pilot and release Brand Kit v1

**State:** `planned`  
**Depends on:** `IDN-Q04`

**Outcome:** Real consumers validate the kit before a stable v1 release.

**Exit criteria:**

- [ ] Issue #17 records representative pilots and fixes.
- [ ] Issue #18 closes with a tagged, provenance-rich v1 release.

**Current evidence:**

- Issues #17 and #18 define pilots and the v1 milestone.

<!-- roadmap-step
id: IDN-Q06
status: planned
depends_on: [IDN-Q02]
issues: []
-->
#### IDN-Q06 — Publish the roadmap visual token profile

**State:** `planned`  
**Depends on:** `IDN-Q02`

**Outcome:** The quest-line renderer consumes a versioned Identity profile for color, typography, motion, icons, focus, and reduced-motion behavior.

**Exit criteria:**

- [ ] Complete, active, ready, blocked, planned, and deferred states remain distinguishable without color alone.
- [ ] The token package passes contrast, reduced-motion, and deterministic compilation checks.

**Current evidence:**

- Identity already has the strongest compiler and package foundation; the roadmap profile is not yet published.

### Roadmap-to-issue handoff

- A step is complete only when its exit criteria and required evidence are satisfied; commit count never determines progress.
- Ready steps without an issue are candidates for the private, duplicate-aware roadmap.issue-plan.json dry run. Planned steps remain preview-only unless a reviewer explicitly opts them in with issue_policy: propose.
- Issue creation or reconciliation requires human approval or an explicitly authorized Pace operation and returns issue references through a reviewable roadmap pull request.
- Pull requests and commits should include Roadmap-Step: <ID>; historical evidence may be linked through existing issue and pull-request relationships.
- Public rendering uses only allowlisted build-time evidence and never places a GitHub token or private issue plan in the browser artifact.

<!-- END ROADMAP EXECUTION SNAPSHOT -->

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
