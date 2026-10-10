---
schema: egohygiene.architecture-decision/v1
id: ADR-014
title: Keep design-system handbooks as governed projections
status: accepted
date: "2026-10-10"
decision_scope: repository
visibility: public
owners:
  - egohygiene/identity
issue: https://github.com/egohygiene/identity/issues/35
pull_request: https://github.com/egohygiene/identity/pull/48
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
    url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-014-design-system-projection-boundary.md
    description: Immutable original record; historical prose, metadata and dates are preserved separately from the current human disposition.
  - type: documentation
    url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/contracts/DESIGN_SYSTEM_V1.md
    description: Inspected contract and implementation boundary at the reviewed source revision; no new runtime or publication verification is implied.
  - type: implementation
    url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/scripts/render_design_system.py
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

# ADR-014: Keep design-system handbooks as governed projections

The canonical date records the explicit human disposition on 2026-10-10.
Original source prose and metadata are preserved below as historical evidence;
the approved R1 clarifications and scope limits govern their current reading.

## Context

Identity needs a useful design-system handbook for humans and concise context
for automation, while remaining a brand-source compiler rather than a UI
framework. Existing token, voice, usage, provenance, and approval contracts
already establish human-reviewed local source. Free-form handbook prose,
untracked inspiration, or agent-maintained instructions would create another
authority and make review, ownership, and reproducibility unclear.

## Decision

Add an optional local `documents.handbook` source boundary to Identity v1.
Validate a reviewed design-system source and a reviewed external-reference
catalog under the existing lifecycle and approval model. Define two derived
contracts: a human handbook and a compact AI-readable design context.

Both projections are generated outside `.identity/`, carry a stable resolved
source digest, and identify a fixed projection version rather than a runtime
timestamp. They expose explicit capability status and ownership. Identity owns
brand contracts and projections; Holon owns reusable components; consumers own
layouts; Aether and other tools consume the compact context without becoming
canonical authors.

Reference catalogs describe observations and rights constraints only. They do
not fetch, copy, redistribute, or grant permission to use third-party assets,
marks, or copy.

## Alternatives considered and rejected

- **Make a Markdown handbook canonical:** lacks closed structure, lifecycle,
  and machine-readable ownership information.
- **Put components in Identity:** duplicates Holon's responsibility and couples
  the brand compiler to one UI implementation.
- **Allow agents to maintain their own brand context:** makes review and
  provenance impossible to establish.
- **Scrape reference sites during rendering:** creates network, licensing,
  reproducibility, and availability dependencies.

These are the alternatives recorded in the historical source. No additional
contemporaneous alternatives or rationale are inferred.

## Consequences and tradeoffs

- Existing v1 consumers remain valid until they explicitly adopt handbook
  source.
- A handbook can show what is absent or owned elsewhere instead of implying a
  fictitious component library.
- Automation receives concise, verifiable source facts rather than a mutable
  prompt document.
- The renderer implementation has an exact output contract and an auditable
  deterministic boundary.
- Authors must create approval records for handbook principles and reference
  decisions before they can appear publicly.

## Implementation and evidence links

The inspected optional handbook source contract and handbook/context
projection implementation are present. This establishes the bounded source and
projection capability, not delivery of Holon components, consumer layouts, or
fresh runtime or visual verification.

[Original implementation PR #48](https://github.com/egohygiene/identity/pull/48),
[inspected contract](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/contracts/DESIGN_SYSTEM_V1.md), and
[implementation source](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/scripts/render_design_system.py)
provide the bounded evidence. Human approval is recorded separately in the
[explicit R1 disposition](https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806).

## Replacement or exit strategy

Revisit if a future component contract proves that Identity must own a
framework-neutral interface, or if the organization accepts a versioned,
reviewable external-reference ingestion process with stronger rights evidence.

## Follow-up work

Keep capability ownership and unavailable capabilities explicit in downstream
adoption. Review source changes and external-reference rights independently;
this retention supplies neither new rights nor component implementation.

## Historical metadata and provenance

The following metadata is reproduced from the original record. Its status
and dates are historical claims, not the date or proof of the current
approval.

- **Status:** Accepted
- **Date:** 2026-08-28
- **Tracking:** [issue #35](https://github.com/egohygiene/identity/issues/35)
- **Decision owners:** Identity maintainers and consumer identity owners

Preserved from [immutable source `434f60c8b829c695b3bcd1a45faf5e0c114d37cf`](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-014-design-system-projection-boundary.md).
The present disposition transcribes `szmyty`'s explicit approval of
[R1 at `418aa9757898b6c09b4f01eface522778cff90e8`](https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md);
it does not backdate acceptance or convert implementation into verification.

## Approved R1 scope qualifier — 2026-10-10

Retain now; this grants no new external-reference rights or component capabilities.
