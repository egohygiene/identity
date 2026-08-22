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

The product contract, extracted CLI foundation, v1 source contract, and compiler
core are implemented or accepted with validation evidence. Concrete Brand Kit
projection adapters, package distributions, renderer, studio, and publication
remain proposed or deferred until their owning issues land.

## System inventory

| System | State | Responsibility | Inputs | Outputs | Tracking |
| --- | --- | --- | --- | --- | --- |
| Product contract | Accepted | Defines the Brand Kit product, ownership, authority, lifecycle states, and stable interfaces | Reviewed architecture decisions | Versioned architecture documents | #6 |
| CLI foundation | Implemented | Initializes and validates v0 consumer intent, resolves deterministic plans, and creates provenance-aware creative handoffs | Consumer repository and `.identity/` v0 source | Diagnostics, 45-target plan, candidate template, and handoff manifest | #8 |
| Identity source contract | Implemented | Models content-addressed organization defaults, intentional product overrides, DTCG semantic tokens, target profiles, approvals, licenses, provenance, and reserved voice/usage paths | `.identity/identity.json` and declared local documents | Stable diagnostics and validated resolved-token evidence | #1, #9 |
| Compiler core | Implemented in this change | Executes deterministic read, validate, resolve, plan, render, verify, manifest, transaction, and recovery boundaries behind replaceable ports | Resolved identity, target requests, adapter capabilities, and generated-state evidence | Stable plans, compatibility diagnostics, verified artifacts, manifests, checksums, and recovery evidence | #2, #10 |
| Projection adapters | Proposed | Render tokens, vector/raster assets, metadata, guidance, and archives behind replaceable ports | Asset plan and approved sources | Target-specific artifacts | #7, #11 |
| Validation and evidence | Proposed | Test accessibility, dimensions, visual integrity, licensing, provenance, compatibility, and reproducibility | Source, outputs, manifest, fixtures | Machine report and human recovery guidance | #3, #12 |
| Package distribution | Proposed | Assemble versioned token, metadata, voice, asset, manifest, and download packages | Verified artifacts | Immutable consumer packages and checksums | #11, #18 |
| Brand Kit renderer | Proposed | Present the generated view model as an accessible, framework-replaceable public reference experience | Versioned Brand Kit view model | Static/reference Brand Kit and downloads | #14 |
| Asset studio | Proposed | Preview intent and candidates, compare results, and apply approved changes without making preview state canonical | Source, candidates, presets, view model | Preview, plan, approval record, handoff | #15 |
| Publication handoff | Deferred | Deliver an immutable approved artifact to a consumer-owned deployment boundary | Released Brand Kit bundle | Versioned integration and rollback metadata | #16 |

## Named public interfaces

| Interface | Authority | Contract |
| --- | --- | --- |
| Source interface | Consumer | Versioned `.identity/` directory; canonical human-reviewed intent |
| CLI interface | Identity | `init`, `validate`, `plan`, and `handoff` are implemented with parity evidence; generation commands remain deferred until #11 supplies concrete projection/profile contracts |
| Compiler library interface | Identity | Implemented v1 Rust ports and models for validation, resolution, mutation-free planning, adapter compatibility, rendering, verification, manifests, transactional apply, and recovery |
| Package interface | Identity | Versioned tokens, assets, metadata, voice, manifests, checksums, and compatibility metadata |
| Brand Kit view-model interface | Identity | Framework-neutral representation consumed by renderers and public surfaces |
| Renderer interface | Identity | Reference static/public experience over an immutable view model |
| Consumer interface | Consumer repository | Pinned package or release integration; no access to Identity internals |
| Publication interface | Owning website or product | Explicit promotion of a verified immutable release with rollback data |
| Evidence interface | Identity, Relay, Observatory | Stable machine-readable diagnostics, validation reports, manifests, and health signals |

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

Apply an accepted plan transactionally, render deterministic targets, validate the result, and emit a manifest and evidence. Partial output cannot be reported as verified success. Concrete Brand Kit projection adapters and profiles remain #11 work.

### Review creative candidates

Compare candidates with approved sources, retain provider and source lineage, record a human decision, then regenerate deterministic projections from the accepted state.

### Package and publish

Assemble immutable packages and a Brand Kit bundle, verify release gates, then hand the release to a consumer-owned publication boundary. Generation never publishes as an implicit side effect.

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
