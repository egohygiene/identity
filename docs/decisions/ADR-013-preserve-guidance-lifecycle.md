---
schema: egohygiene.architecture-decision/v1
id: ADR-013
title: Preserve guidance lifecycle state in every projection
status: accepted
date: "2026-10-10"
decision_scope: repository
visibility: public
owners:
  - egohygiene/identity
issue: https://github.com/egohygiene/identity/issues/13
pull_request: https://github.com/egohygiene/identity/pull/37
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
    url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-013-preserve-guidance-lifecycle.md
    description: Immutable original record; historical prose, metadata and dates are preserved separately from the current human disposition.
  - type: documentation
    url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/contracts/GUIDANCE_V1.md
    description: Inspected contract and implementation boundary at the reviewed source revision; no new runtime or publication verification is implied.
  - type: implementation
    url: https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/scripts/render_guidance.py
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

# ADR-013: Preserve guidance lifecycle state in every projection

The canonical date records the explicit human disposition on 2026-10-10.
Original source prose and metadata are preserved below as historical evidence;
the approved R1 clarifications and scope limits govern their current reading.

## Context

Voice, examples, usage rules, and assets pass through candidate, approval,
rejection, replacement, and retirement. A generated Brand Kit that presents
only final prose loses the evidence needed to distinguish reviewed guidance
from a provider suggestion or a legacy asset. Conversely, making each public
surface interpret free-form Markdown would duplicate policy and invite drift.

## Decision

Store voice and usage as separate versioned source documents. Give every
consequential record a uniform governance envelope containing subject,
lifecycle state, visibility, provenance, and approval reference.

Keep `candidate` distinct from human decisions: it carries provenance and a
null approval, remains internal, and can originate only from an explicit
handoff or authored source. `approved`, `rejected`, and `superseded` records
must resolve to a human decision for the same subject and state.

Project validated guidance into one immutable
`identity.brand-guidance/v1` model. Markdown, HTML, packages, and future public
renderers consume that model and copy reviewed text exactly. They do not
generate or silently rewrite prose.

Legacy assets remain a separate labeled collection. Unless a new decision
approves publication, they are internal or blocked, have no public download,
and name their active replacement.

## Alternatives considered and rejected

- **Free-form Markdown as the machine contract:** easy to author, but forces
  every consumer to parse presentation text and infer lifecycle state.
- **Only publish approved records and discard the rest:** smaller outputs, but
  removes migration, rejection, provenance, and review evidence.
- **Let renderers rewrite voice for each surface:** superficially flexible, but
  bypasses human authority and makes outputs irreproducible.

These are the alternatives recorded in the historical source. No additional
contemporaneous alternatives or rationale are inferred.

## Consequences and tradeoffs

- Consumer applications can select tone and rules by stable context ID.
- Public renderers receive normalized do/don't, download, lifecycle, and
  provenance data without bespoke content parsing.
- Golden Markdown, HTML, and JSON prove that the three views share one source.
- Rejected and superseded work remains auditable without becoming public.
- Source authors must provide structured records and explicit decisions rather
  than relying on implicit meaning in prose.

## Implementation and evidence links

The inspected guidance compiler and public/review audience implementation
are present. PR #89 at `8aae2c6767d07714ea16bf0ea493e1f1ac399b6e`
adds recursive public filtering and withheld singleton handling. This is
implementation evidence; no fresh runtime or visual verification is claimed.

[Original implementation PR #37](https://github.com/egohygiene/identity/pull/37),
[inspected contract](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/contracts/GUIDANCE_V1.md), and
[implementation source](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/scripts/render_guidance.py)
provide the bounded evidence. Human approval is recorded separately in the
[explicit R1 disposition](https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806).

## Replacement or exit strategy

Revisit if v2 introduces a separately versioned content-addressed decision
ledger or if a renderer can prove an equally portable model without weakening
human authority, provenance, or deterministic output.

## Follow-up work

Preserve the public/review split during future schema and renderer upgrades.
Keep canonical history separate from public serialization, and validate each
new consumer and publication path under its own acceptance requirements.

## Historical metadata and provenance

The following metadata is reproduced from the original record. Its status
and dates are historical claims, not the date or proof of the current
approval.

- **Status:** Accepted
- **Date:** 2026-08-21
- **Decision owners:** Identity maintainers and consumer identity owners
- **Tracking:** IDN-11 / issue #13

Preserved from [immutable source `434f60c8b829c695b3bcd1a45faf5e0c114d37cf`](https://github.com/egohygiene/identity/blob/434f60c8b829c695b3bcd1a45faf5e0c114d37cf/docs/decisions/ADR-013-preserve-guidance-lifecycle.md).
The present disposition transcribes `szmyty`'s explicit approval of
[R1 at `418aa9757898b6c09b4f01eface522778cff90e8`](https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md);
it does not backdate acceptance or convert implementation into verification.

## Approved R1 clarification — 2026-10-10

### N013 — Public filtering preserves canonical review history

Preserve complete lifecycle and decision history in canonical source and the
explicit internal review projection. Public projections recursively include
only approved, public records and decisions referenced by surviving guidance.
Withheld singleton records are represented as `null` in the normalized public
model and omitted from Markdown/HTML presentation; filtering never deletes or
changes canonical review history. The rejected alternative was discarding
non-public history, not filtering public output. This clarification records
the audience boundary implemented by PR #89; it does not establish the original
record's human approval or historical decision date.

Evidence: [guidance contract at PR #89's merge](https://github.com/egohygiene/identity/blob/8aae2c6767d07714ea16bf0ea493e1f1ac399b6e/docs/contracts/GUIDANCE_V1.md).
Retain the August 21 declared date separately from the August 26 introduction.
