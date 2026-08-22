---
schema: aether.architecture-document/v1
id: identity-system
title: Identity System
kind: architecture-document
version: 1.0.0
status: active
owners:
  - egohygiene
created: 2026-08-19
updated: 2026-08-22
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
| Proposed | A roadmap issue defines the target, but its acceptance criteria are not complete |
| Deferred | The capability is intentionally outside the current boundary or awaits explicit dependencies |

The product contract, extracted CLI foundation, v1 source contract, compiler
core, built-in projection adapters, package contracts, and shared quality
release-evidence harness are implemented or accepted with validation evidence.
Astryx/motion validation, voice/usage/approval guidance, the reference renderer,
studio, consumer proof, and publication remain proposed or deferred until their
owning issues land.

## System inventory

| System | State | Responsibility | Inputs | Outputs | Tracking |
| --- | --- | --- | --- | --- | --- |
| Product contract | Accepted | Defines the Brand Kit product, ownership, authority, lifecycle states, and stable interfaces | Reviewed architecture decisions | Versioned architecture documents | #6 |
| CLI foundation | Implemented | Initializes and validates v0 consumer intent, resolves deterministic plans, and creates provenance-aware creative handoffs | Consumer repository and `.identity/` v0 source | Diagnostics, 45-target plan, candidate template, and handoff manifest | #8 |
| Identity source contract | Implemented | Models content-addressed organization defaults, intentional product overrides, DTCG semantic tokens, target profiles, approvals, licenses, provenance, and reserved voice/usage paths | `.identity/identity.json` and declared local documents | Stable diagnostics and validated resolved-token evidence | #1, #9 |
| Compiler core | Implemented | Executes deterministic read, validate, resolve, plan, render, verify, manifest, transaction, and recovery boundaries behind replaceable ports | Resolved identity, target requests, adapter capabilities, and generated-state evidence | Stable plans, compatibility diagnostics, verified artifacts, manifests, checksums, and recovery evidence | #2, #10 |
| Projection adapters | Implemented | Render DTCG/CSS/JS/TypeScript/Tailwind tokens, SVG/PNG assets, metadata, guidance, PWA/GitHub/social surfaces, and archives behind compiler ports | Resolved Brand Kit model, approved source bytes, and versioned target profiles | Verified target-specific artifacts with adapter evidence | #7, #11 |
| Validation and evidence | Implemented in this change | Evaluate accessibility, dimensions, visual integrity, licensing, provenance, reproducibility, budgets, visual baselines, explicit skips, and human-review boundaries without mutation | Resolved Brand Kit model, compiler manifest, generated artifacts, baselines, review evidence | `identity.quality-report/v1`, release decision, coverage, source/generated context, and recovery guidance | #12 |
| Visual-motion validation | Proposed | Extend the shared evidence model with Astryx-derived motion, animation, and generated-imagery consistency rules | Quality policy, motion assets, animation fixtures, provenance | Additional stable checks in the same quality report | #3 |
| Package distribution | Implemented | Assemble versioned token, metadata, guidance, asset, index, checksum, and download bundles without exposing repository internals | Verified profile artifacts and resolved source digest | Portable package files, SHA-256 indexes, and deterministic ZIP bundle | #2, #11 |
| Brand Kit renderer | Proposed | Present the generated view model as an accessible, framework-replaceable public reference experience | Versioned Brand Kit view model | Static/reference Brand Kit and downloads | #14 |
| Asset studio | Proposed | Preview intent and candidates, compare results, and apply approved changes without making preview state canonical | Source, candidates, presets, view model | Preview, plan, approval record, handoff | #15 |
| Publication handoff | Deferred | Deliver an immutable approved artifact to a consumer-owned deployment boundary | Released Brand Kit bundle | Versioned integration and rollback metadata | #16 |

## Named public interfaces

| Interface | Authority | Contract |
| --- | --- | --- |
| Source interface | Consumer | Versioned `.identity/` directory; canonical human-reviewed intent |
| CLI interface | Identity | `init`, `validate`, `plan`, and `handoff` retain extraction-parity behavior; package generation remains a library/application boundary until an explicit CLI design is accepted |
| Compiler library interface | Identity | Implemented v1 Rust ports and models for validation, resolution, mutation-free planning, adapter compatibility, rendering, verification, manifests, transactional apply, and recovery |
| Package interface | Identity | Implemented v1 profile/version selection plus generated tokens, assets, metadata, guidance, checksums, package indexes, compatibility behavior, and deterministic archive contract |
| Brand Kit view-model interface | Identity | Framework-neutral representation consumed by renderers and public surfaces |
| Renderer interface | Identity | Reference static/public experience over an immutable view model |
| Consumer interface | Consumer repository | Pinned package or release integration; no access to Identity internals |
| Publication interface | Owning website or product | Explicit promotion of a verified immutable release with rollback data |
| Evidence interface | Identity, Relay, Observatory | `identity.quality-report/v1`, stable diagnostics, compiler manifests, coverage/skips, review evidence, and health signals as documented by [QUALITY_GATES_V1.md](docs/contracts/QUALITY_GATES_V1.md) |

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

Select compatible output-profile IDs and versions, apply an accepted plan transactionally, render deterministic targets through offline adapters, validate format/dimension/package invariants, and emit a manifest. The shared #12 quality harness then evaluates accessibility, visual integrity, provenance/licensing, reproducibility, budgets, baselines, skips, and human-review requirements without mutation. Partial coverage cannot be reported as verified success; Astryx/motion-specific consistency remains #3 work.

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
