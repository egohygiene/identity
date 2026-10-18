---
schema: aether.architecture-document/v1
id: identity-system
title: Identity System
kind: architecture-document
version: 1.0.1
status: active
owners:
  - egohygiene
created: 2026-08-19
updated: 2026-10-18
governed_by:
  - architecture-system
depends_on:
  - identity-foundations
  - identity-ontology
related:
  - identity-purpose
  - identity-vision
  - identity-principles
  - identity-pillars
supersedes: []
---

# Identity System

## Purpose and scope

Identity is a Brand Kit generator with three product layers: compiler and contracts, generated Brand Kit data/packages, and a reference public renderer with an approval-aware asset studio. This document names the logical systems and their responsibilities. [ARCHITECTURE.md](ARCHITECTURE.md) owns their structure and dependency direction.

## Capability-state vocabulary

| State | Evidence required |
| --- | --- |
| Implemented | Runtime behavior and validation evidence exist on the default branch |
| Accepted | A reviewed contract constrains later implementation |
| Released | An immutable published tag and its artifacts provide versioned distribution evidence |
| Deployed | A named deployment and served-content verification establish publication at that checkpoint |
| Proposed | A roadmap issue defines the target, but its acceptance criteria are not complete |
| Deferred | The capability is intentionally outside the current boundary or awaits explicit dependencies |

The independent CLI, v1 source contract, compiler/packages, quality and motion
validation, governed guidance, reference renderer, and studio are implemented.
Empathy and OptiFlow supplied the representative consumer proof, and `v1.0.0`
is released. The standalone Brand Kit publisher has deployed evidence; the
organization `/identity/` composite retains its separate stable-release,
installation, and live-verification gates. [ROADMAP.md](ROADMAP.md) records
current stabilization and kit-completion work. Current-main repairs do not
change the contents of an earlier release.

## System inventory

| System | State | Responsibility | Inputs | Outputs | Tracking |
| --- | --- | --- | --- | --- | --- |
| Product contract | Accepted | Defines the Brand Kit product, ownership, authority, lifecycle states, and stable interfaces | Reviewed architecture decisions | Versioned architecture documents | #6 |
| CLI foundation | Implemented | Initializes and validates v0 consumer intent, resolves deterministic plans, and creates provenance-aware creative handoffs | Consumer repository and `.identity/` v0 source | Diagnostics, 45-target plan, candidate template, and handoff manifest | #8 |
| Identity source contract | Implemented | Models content-addressed organization defaults, intentional product overrides, DTCG semantic tokens, target profiles, approvals, licenses, provenance, and governed voice/usage | `.identity/identity.json` and declared local documents | Stable diagnostics and validated resolved-token evidence | #1, #9, #13 |
| Compiler core | Implemented | Executes deterministic read, validate, resolve, plan, render, verify, manifest, transaction, and recovery boundaries behind replaceable ports | Resolved identity, target requests, adapter capabilities, and generated-state evidence | Stable plans, compatibility diagnostics, verified artifacts, manifests, checksums, and recovery evidence | #2, #10 |
| Projection adapters | Implemented | Render DTCG/CSS/JS/TypeScript/Tailwind tokens, SVG/PNG assets, metadata, guidance, PWA/GitHub/social surfaces, and archives behind compiler ports | Resolved Brand Kit model, approved source bytes, and versioned target profiles | Verified target-specific artifacts with adapter evidence | #7, #11 |
| Validation and evidence | Implemented | Evaluate accessibility, dimensions, visual integrity, licensing, provenance, reproducibility, budgets, visual baselines, explicit skips, and human-review boundaries without mutation | Resolved Brand Kit model, compiler manifest, generated artifacts, baselines, review evidence | `identity.quality-report/v1`, release decision, coverage, source/generated context, and recovery guidance | #12 |
| Visual-motion validation | Implemented | Govern animation, generated imagery, landing sequences, status motion, and deterministic demo captures through purpose budgets, reduced-motion fallbacks, provenance, capture determinism, visual baselines, and human semantic review | `identity.motion-policy/v1`, `identity.visual-motion-manifest/v1`, generated assets, quality input, review evidence | Motion checks appended to the same `identity.quality-report/v1` release decision | #3 |
| Package distribution | Implemented | Assemble versioned token, metadata, guidance, asset, index, checksum, and download bundles without exposing repository internals | Verified profile artifacts and resolved source digest | Portable package files, SHA-256 indexes, and deterministic ZIP bundle | #2, #11 |
| Governed guidance | Implemented | Preserve approval lifecycle and explicit public/review audience boundaries | Reviewed voice, usage, and approval records | Deterministic JSON, Markdown, HTML, and package guidance | #13, #71 |
| Brand Kit renderer | Implemented | Present the generated view model as an accessible, framework-replaceable public reference experience | Versioned Brand Kit view model | Static/reference Brand Kit and downloads | #14 |
| Asset studio | Implemented | Preview candidates and export explicit reviewed handoffs without silently changing canonical or generated state | Source, candidates, presets, immutable view model | Preview, plan, approval record, handoff | #15 |
| Standalone Brand Kit publication | Deployed checkpoint | Build and deploy one release-backed Brand Kit with separately bound current Decisions evidence | Immutable stable Brand Kit release and full ADR source revision | Static site, downloads, source bindings, composition and deployment receipts | #16, #69, PR #97 |
| Organization experience handoff | Implemented candidate | Build the reviewed `/identity/` composite for the organization route owner; stable release and installation remain separately gated | Pinned Holon profiles, reviewed content, Identity outputs | Content-addressed composite and verification evidence | #56, #57 |
| Consumer adoption and release | Released | Prove independent consumption and provide an immutable installation/upgrade boundary | Empathy/OptiFlow pilots, release evidence | `v1.0.0`, consumer pins, documented adoption and rollback | #17, #18 |

## Named public interfaces

| Interface | Authority | Contract |
| --- | --- | --- |
| Source interface | Consumer | Versioned `.identity/` directory; canonical human-reviewed intent |
| CLI interface | Identity | `init`, `validate`, `plan`, and `handoff` retain v0 extraction parity; `studio-review` checks an explicitly approved handoff; `v1-generate` and `v1-verify` expose the v1 package boundary |
| Compiler library interface | Identity | Implemented v1 Rust ports and models for validation, resolution, mutation-free planning, adapter compatibility, rendering, verification, manifests, transactional apply, and recovery |
| Package interface | Identity | Implemented v1 profile/version selection plus generated tokens, assets, metadata, guidance, checksums, package indexes, compatibility behavior, and deterministic archive contract |
| Brand Kit view-model interface | Identity | Framework-neutral representation consumed by renderers and public surfaces |
| Renderer interface | Identity | Reference static/public experience over an immutable view model |
| Consumer interface | Consumer repository | Pinned package or release integration; no access to Identity internals |
| Publication interface | Owning website or product | Explicit promotion of a verified immutable release with rollback data |
| Evidence interface | Identity, Relay, Observatory | `identity.quality-report/v1` plus `identity.motion-policy/v1` and `identity.visual-motion-manifest/v1`, stable diagnostics, compiler manifests, coverage/skips, review evidence, and health signals as documented by [QUALITY_GATES_V1.md](docs/contracts/QUALITY_GATES_V1.md) and [VISUAL_MOTION_V1.md](docs/contracts/VISUAL_MOTION_V1.md) |

On current source, both v1 commands and `V1ConsumerPipeline::load` invoke the
embedded authoritative validator and require Python 3.11+. See the
[source contract](docs/contracts/IDENTITY_V1.md). Recovery is currently a Rust
artifact-store API, not a distributed CLI command: #77 follows transaction
workspace and writer hardening in #78/#79. Legacy v1 transaction journals fail
closed because they lack recovery authority evidence; preserve their workspace
and use independently reviewed backups rather than relabelling the journal.
The [compiler contract](docs/contracts/COMPILER_V1.md) owns that current rule.

## Canonical, generated, transient, and published state

| State | Storage boundary | Mutation authority | Distribution rule |
| --- | --- | --- | --- |
| Canonical | Consumer-owned `.identity/` | Explicit human-approved change | Versioned as source; private material remains excluded |
| Generated | `assets/identity/` or package build output | Deterministic compiler after plan approval | Distributed with manifest, version, checksums, and provenance |
| Transient | Ignored implementation workspace, cache, preview, candidate, or `.cache/identity/transactions/` state | Active CLI/compiler/studio session | Never distributed or promoted implicitly; compiler transactions require explicit recovery when interrupted |
| Published | Consumer deployment or public route | Owning repository/service | References one immutable verified release and supports rollback |

## Primary workflows

### Initialize or migrate

Create a versioned source contract, preserve provenance, validate it, and present migration decisions before replacing existing identity state.

### Validate and plan

Resolve defaults and overrides, validate requirements, discover adapters, and enumerate writes, replacements, removals, warnings, approvals, and unsupported targets without mutation.

### Generate and verify

Select compatible output-profile IDs and versions, apply an accepted plan transactionally, render deterministic targets through offline adapters, validate format/dimension/package invariants, and emit a manifest. The shared #12 quality harness evaluates accessibility, visual integrity, provenance/licensing, reproducibility, budgets, baselines, skips, and human-review requirements without mutation; #3 adds governed motion/capture/provenance checks to that same report and release decision. Partial coverage cannot be reported as verified success.

### Review creative candidates

Compare candidates with approved sources, retain provider and source lineage, record a human decision, then regenerate deterministic projections from the accepted state.

### Package and publish

Assemble the versioned package index, checksums, and deterministic Brand Kit archive from verified projections, then apply downstream release gates before handing an immutable release to a consumer-owned publication boundary. Generation never publishes as an implicit side effect.

## Failure model

| Failure state | Required behavior |
| --- | --- |
| Invalid | Reject the affected source with stable diagnostics and paths |
| Unsupported | Identify the missing capability without claiming partial support |
| Blocked | Preserve state and identify the dependency, authority, or approval required |
| Partial | Isolate incomplete output, report coverage, and withhold verification |
| Failed | Preserve canonical state, provide evidence, and offer a recoverable retry or rollback |
| Drifted | Identify differences between source, generated state, package, or published release |

Destructive, publication, privacy, security, license, and approval boundaries fail closed.
