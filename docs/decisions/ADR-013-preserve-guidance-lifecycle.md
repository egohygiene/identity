# ADR-013: Preserve guidance lifecycle state in every projection

- **Status:** Accepted
- **Date:** 2026-08-21
- **Decision owners:** Identity maintainers and consumer identity owners
- **Tracking:** IDN-11 / issue #13

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

## Consequences

- Consumer applications can select tone and rules by stable context ID.
- Public renderers receive normalized do/don't, download, lifecycle, and
  provenance data without bespoke content parsing.
- Golden Markdown, HTML, and JSON prove that the three views share one source.
- Rejected and superseded work remains auditable without becoming public.
- Source authors must provide structured records and explicit decisions rather
  than relying on implicit meaning in prose.

## Alternatives rejected

- **Free-form Markdown as the machine contract:** easy to author, but forces
  every consumer to parse presentation text and infer lifecycle state.
- **Only publish approved records and discard the rest:** smaller outputs, but
  removes migration, rejection, provenance, and review evidence.
- **Let renderers rewrite voice for each surface:** superficially flexible, but
  bypasses human authority and makes outputs irreproducible.

## Reconsider when

Revisit if v2 introduces a separately versioned content-addressed decision
ledger or if a renderer can prove an equally portable model without weakening
human authority, provenance, or deterministic output.
