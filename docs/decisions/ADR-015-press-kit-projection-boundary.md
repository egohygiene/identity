---
schema: egohygiene.architecture-decision/v1
id: ADR-015
title: Keep Press Kits as governed public projections
status: accepted
date: "2026-10-10"
decision_scope: repository
visibility: public
owners:
  - egohygiene/identity
issue: https://github.com/egohygiene/identity/issues/34
pull_request: https://github.com/egohygiene/identity/pull/53
related: []
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/identity]
affected_contracts: []
implementation_status: implemented
evidence:
  - type: approval
    url: https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806
    description: Explicit human approval of R1 at packet 418aa9757898b6c09b4f01eface522778cff90e8, retaining this direction now with its listed clarifications and scope limits.
  - type: documentation
    url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-015-press-kit-projection-boundary.md
    description: Immutable original record; historical prose, metadata and dates are preserved separately from the current human disposition.
  - type: documentation
    url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/contracts/PRESS_KIT_V1.md
    description: Inspected contract and implementation boundary at the reviewed source revision; no new runtime or publication verification is implied.
  - type: implementation
    url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/scripts/render_press_kit.py
    description: Inspected bounded implementation at the reviewed source revision.
  - type: documentation
    url: https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md
    description: Exact R1 recommendations, dated clarifications and scope qualifiers approved by the human disposition.
approval:
  date: "2026-10-10"
  by: szmyty
  evidence: https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806
exceptions: []
---

# ADR-015: Keep Press Kits as governed public projections

The canonical date records the explicit human disposition on 2026-10-10.
Original source prose and metadata are preserved below as historical evidence;
the approved R1 clarifications and scope limits govern their current reading.

## Context

Press and Media Kits need consistent, ready-to-download material, but they
often accumulate unreviewed launch claims, stale bios, private contacts, and
asset folders whose rights or intended use are unclear. Identity already has
local source, approval, provenance, and public-asset boundaries. A separate
hand-maintained press folder or renderer configuration would create another
authority and make public exposure hard to review.

## Decision

Add an optional local `documents.pressKit` source boundary to Identity v1.
Require reviewed short and long boilerplate and govern every optional fact,
link, contact, team biography, and selected asset. Generate the Press Kit
outside `.identity/` as a deterministic JSON, Markdown, integrity-manifest,
checksums, and ZIP package.

Selected assets may only reference assets that have already passed the active,
public, approval, provenance, and byte-integrity checks. The reference renderer
may render a supplied package only after it matches the immutable Brand Kit
project and source digest. Identity does not own website routing or publication.

## Alternatives considered and rejected

- **Maintain a free-form press folder:** no schema, approval, selection, or
  integrity boundary.
- **Let the renderer read `.identity/`:** makes publication depend on private
  source and allows renderer code to become a second content author.
- **Copy every approved asset automatically:** exposes more material than a
  given Press Kit actually needs and weakens intent.
- **Generate contacts, biographies, or claims from prompts:** cannot establish
  factual ownership, approval, or a durable correction path.

These are the alternatives recorded in the historical source. No additional
contemporaneous alternatives or rationale are inferred.

## Consequences and tradeoffs

- Existing v1 consumers remain valid until they explicitly adopt Press Kit
  source.
- Approved information can be rebuilt, checked, archived, and reused across
  release pages without another hand-maintained bundle.
- Candidate claims, private contacts, and unselected assets cannot become
  public by renderer configuration or directory copying.
- Consumers retain control of domains, routes, deployment, and social systems.
- Maintainers must create explicit reviewed records before new material appears
  in a public package.

## Implementation and evidence links

The inspected optional Press Kit compiler and immutable package contract are
present. The package remains separate from routing and deployment. This
implementation status does not claim a new package build, public asset review,
or live publication verification.

[Original implementation PR #53](https://github.com/egohygiene/identity/pull/53),
[inspected contract](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/contracts/PRESS_KIT_V1.md), and
[implementation source](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/scripts/render_press_kit.py)
provide the bounded evidence. Human approval is recorded separately in the
[explicit R1 disposition](https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806).

## Replacement or exit strategy

Revisit if Identity needs a separately versioned multi-language content
localization contract, or if a consumer-owned publication service establishes a
reviewable deployment and release manifest that can consume the same immutable
package without changing this authority boundary.

## Follow-up work

Validate consumer packages and their selected public content before each
separate publication. Preserve the distinction between this compiler capability
and the existing independently governed Brand Kit publisher.

## Historical metadata and provenance

The following metadata is reproduced from the original record. Its status
and dates are historical claims, not the date or proof of the current
approval.

- **Status:** Accepted
- **Date:** 2026-08-28
- **Tracking:** [issue #34](https://github.com/egohygiene/identity/issues/34)
- **Decision owners:** Identity maintainers and consumer identity owners

Preserved from [immutable source `434f60c8b829c695b3bcd1a45faf5e0c114d37cf`](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-015-press-kit-projection-boundary.md).
The present disposition transcribes `szmyty`'s explicit approval of
[R1 at `418aa9757898b6c09b4f01eface522778cff90e8`](https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md);
it does not backdate acceptance or convert implementation into verification.

## Approved R1 scope qualifier — 2026-10-10

Retain now; compiler output grants no publishing authority and does not revoke the separate Brand Kit publisher.
