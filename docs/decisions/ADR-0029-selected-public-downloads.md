---
schema: egohygiene.architecture-decision/v1
id: ADR-0029
title: Bind public downloads to governed assets and selected outputs
status: proposed
date: "2026-10-21"
decision_scope: repository
visibility: public
owners: [egohygiene/identity]
issue: https://github.com/egohygiene/identity/issues/101
pull_request: https://github.com/egohygiene/identity/pull/126
related: [ADR-0001, ADR-0003, ADR-0010, ADR-0012, ADR-0013, ADR-0015, ADR-0019, ADR-0024, ADR-0025, ADR-0028]
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/identity]
affected_contracts: []
implementation_status: implemented
evidence:
  - type: pull_request
    url: https://github.com/egohygiene/identity/pull/126
    description: Implements governed public selection, selected download metadata, existing SVG master copies, explicit browser assets and offline artifact verification; implementation does not accept this proposal.
  - type: commit
    url: https://github.com/egohygiene/identity/commit/3f03f9b10dd0a7e6e2c292cadabb737e7902e56f
    description: Exact candidate source for the completed CLI, renderer and decision workflow evidence below; subsequent evidence-only changes require their own final-head checks.
  - type: workflow_run
    url: https://github.com/egohygiene/identity/actions/runs/39574561355
    description: Completed CLI workflow passes at the cited candidate source, including Rust/Python checks and extracted-source provenance verification; not release or deployment acceptance.
  - type: workflow_run
    url: https://github.com/egohygiene/identity/actions/runs/39574561241
    description: Completed reference-renderer workflow passes at the cited candidate source; this is bounded hosted evidence, not actual authoring-workspace Docker qualification.
  - type: workflow_run
    url: https://github.com/egohygiene/identity/actions/runs/39574562283
    description: Completed decision workflow passes at the cited candidate source; its advisory warnings do not supply missing human acceptance or replace pinned-owner preservation checks.
  - type: issue
    url: https://github.com/egohygiene/identity/issues/101
    description: Requests practical approved logo, wordmark, favicon and avatar downloads without creating new artwork or approval authority.
  - type: implementation
    url: https://github.com/egohygiene/identity/blob/828d38b86edcc5015fa1bc27f843870c3b5233fb/src/reference_renderer.rs
    description: Inspected base projects every source asset and a fixed package catalog without binding the renderer to selected compiler targets.
  - type: implementation
    url: https://github.com/egohygiene/identity/blob/828d38b86edcc5015fa1bc27f843870c3b5233fb/renderer/index.template.html
    description: Inspected base declares browser asset paths unconditionally, independently of the selected output profiles.
  - type: implementation
    url: https://github.com/egohygiene/identity/blob/828d38b86edcc5015fa1bc27f843870c3b5233fb/src/brandkit/profiles.rs
    description: Existing profiles already define mechanical source SVG and favicon, PWA, maskable and social raster targets.
  - type: documentation
    url: https://github.com/egohygiene/identity/blob/828d38b86edcc5015fa1bc27f843870c3b5233fb/docs/contracts/GUIDANCE_V1.md
    description: Existing governed usage assets own explicit public selection and lifecycle metadata; source provenance retains byte and rights authority.
approval: null
exceptions: []
---

# ADR-0029: Bind public downloads to governed assets and selected outputs

## Context

The #101 inventory found usable exports already present in native profiles and
legacy release assets. The generic reference-renderer model nevertheless embeds
all resolved source artwork, including internal or superseded records, and
advertises fixed package paths even when profiles were not selected. Selected
favicon/PWA PNGs lack a practical download inventory. Browser icon/manifest
references assume files exist, and a model-only render does not verify output
bytes.

Accepted ADR-0001 keeps creative approval human-owned, ADR-0003 separates
mechanical projection from creation, ADR-0010 owns the immutable renderer port,
ADR-0012 local source/provenance, ADR-0013 lifecycle selection, ADR-0015 the
governed Press Kit and ADR-0019 immutable release selection. Existing proposed
ADR-0024, ADR-0025 and ADR-0028 describe implemented path, nullable-input and
rights context; their proposal state supplies no accepted authority.

## Decision

Propose a bounded public-source and selected-output handoff. The generic
renderer may include an asset only when its matching existing usage `assets[]`
record is approved/public, active and publicly available, bound by validated
asset ID/path to local provenance. Keep complete source/review state local.
Absent usage yields no public assets/downloads while independently nullable
local core generation remains supported. Source approval alone does not select
public display or distribution.

Bind the actual `CompilerRequest` targets into the reference-renderer target
parameters. Add optional `downloads[]` with `id`, `label`, `path`, `mediaType`,
`profile`, `sourceAssetId`, `sourceSha256` and `dimensions`. Copy optional asset
`kind` and `notes`, and the selected label, from existing governed usage.
The source hash identifies the master bytes; derived output checksums belong
to the generated manifest. A bare model without selected targets must not
invent generated file links. Packages/downloads refer only to matching
selected targets, and an archive is not advertised when its underlying mark
is not public.

With `core` selected, use the existing source SVG adapter to copy distinct
selected public masters to safe `brand/<downloadName>` paths. Reuse existing
matching targets and reject collisions before writes. Expose selected native
favicon/PWA/maskable/social PNGs with their actual profile and dimensions.
Infer no variant role, theme, new artwork or creative rule from identifiers.
This adds no universal ICO/avatar adapter; explicitly configured existing
legacy release files remain independently usable.

Make browser icon, Apple-touch icon and web-manifest references explicit
optional configuration, using safe bundle-relative paths and the existing
asset base. Supply optional artifact-root and artifact-manifest verification
for advertised local files, inventory hashes/sizes and source binding. Reject
missing files and paths escaping their artifact root. Never fetch a configured
download/CDN URL. Model-only previews remain possible without execution proof.

The separate release-backed publisher selects actual immutable release files
and verifies advertised outputs against its inventory. Preserve the #103
missing-rights behavior: absent legacy license/origin/approval stays null and
does not establish permissions or withhold existing selected archive bytes.
This proposal grants no legal, creative, publication or release authority.

## Alternatives considered and rejected

- Treat source rights approval as public selection: loses the existing usage
  lifecycle/visibility boundary and can expose internal or superseded artwork.
- Advertise the profile catalog or construct plausible paths: produces links
  for unselected or failed outputs and provides no byte evidence.
- Infer logo variants, derive artwork or add a new asset-role catalog: changes
  creative/source authority beyond the existing governed records.
- Require artifact files for every model-only preview: removes the independent
  immutable renderer port; explicit local verification provides the stronger
  check when actual outputs are supplied.

These are alternatives considered for this proposal, not reconstructed claims
about historical deliberations.

## Consequences and tradeoffs

Public pages lose implicit access to locally approved assets until owners
explicitly select them in governed usage. Local generation and complete review
state remain available. Selected-target metadata describes the requested
outputs; successful generation plus artifact verification establishes their
actual bytes. Neither result proves complete-kit suitability or human review.

The optional fields retain `identity.brand-kit-view-model/v1` and the existing
adapter version. Models omitting them remain supported, but older strict Rust
readers may reject them. Consumers must pin matching reviewed compiler, schema
and renderer revisions and regenerate the complete source-bound handoff.
Never edit immutable historical artifacts or confuse a source checksum with a
derived output checksum.

Explicit browser metadata can be absent. Existing files can be verified
offline without proving their network availability, browser appearance,
deployment or unresolved legacy rights. Preserving a model-only preview means
its lack of filesystem proof must remain visible in the evidence record.

## Implementation and evidence links

Issue #101 and [PR #126](https://github.com/egohygiene/identity/pull/126) own the
candidate implementation. The
[renderer contract](../contracts/BRAND_KIT_RENDERER_V1.md),
[authoring worksheet](../consumers/AUTHORING.md) and
[publication guide](../publication/IDENTITY_PAGES.md) describe the bounded ports.
Focused checks cover public lifecycle selection, nullable absence,
selected versus unselected outputs, distinct master copies, compatible old
models, safe deployment bases and actual missing/tampered/source-mismatched
artifact rejection. At candidate source
`3f03f9b10dd0a7e6e2c292cadabb737e7902e56f`, the completed CLI, reference-renderer
and decision workflows linked above pass. These results bind that exact source;
later evidence-only changes require separately recorded final-head checks.
Exact commands, revisions, outcomes and limitations belong in the PR and
CONTINUITY.md. The implementation state is implemented, while human disposition
remains proposed with no approval. This evidence does not claim a completed
release workflow, image workflow, live deployment, full #70 quality campaign
or actual authoring-workspace Docker qualification.

## Replacement or exit strategy

Retain earlier immutable tool/package sets for rollback. A consumer adopting
the optional members must keep a compatible reader or regenerate from an
earlier reviewed producer/source selection. Do not restore all-source public
projection or fabricated links to hide an empty selection. Broader variant
semantics, native formats and publication policy need separate reviewed work.

## Follow-up work

Issue #105 retains complete consumer-kit readiness; #98 retains actual
release/self-dogfood acceptance and #102 broader typography presentation.
Issue #70 owns the deferred full lint/testing/CI and Docker quality pass.
Human disposition of this proposed decision remains separate.
