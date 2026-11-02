---
schema: egohygiene.architecture-decision/v1
id: ADR-0032
title: Generate optional announcement drafts from approved copy and explicit facts
status: proposed
date: "2026-11-02"
decision_scope: repository
visibility: public
owners: [egohygiene/identity]
issue: https://github.com/egohygiene/identity/issues/106
pull_request: null
related: [ADR-0001, ADR-0003, ADR-0011, ADR-0015, ADR-0028, ADR-0030]
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/identity]
affected_contracts: []
implementation_status: implemented
evidence:
  - type: issue
    url: https://github.com/egohygiene/identity/issues/106
    description: Requests an optional concrete template with approved copy/assets and project-supplied changing facts.
approval: null
exceptions: []
---

# ADR-0032: Generate optional announcement drafts from approved copy and explicit facts

## Context

The public Brand Kit and Press Kit already provide approved facts, copy and
assets. Issue #106 asks for optional launch/presentation/document templates,
starting with a concrete consumer selection. A small release-announcement
draft is proposed for review; a social publishing system is not required.

## Decision

Propose one opt-in standard-library tool that validates current canonical
source through the existing Press Kit projection, selects public boilerplate
and assets, and combines them with explicit owner-supplied version/date/link
and change claims. A closed request and draft-only receipt keep changing facts
separate from canonical brand source. Existing Brand Kit generation is unchanged.
The output is a Markdown review draft and selected unchanged asset bytes, with
deterministic reconstruction/inventory verification. It never posts, schedules,
approves claims, reads hosted release state or generates artwork.

## Alternatives considered and rejected

- Build all slide, document and campaign templates now: no concrete demand
  establishes those formats or their ongoing maintenance.
- Infer claims from Git or a version tag: that supplies no owner review of the
  actual message, date or feature claims.
- Treat a valid public boilerplate as approval of the whole announcement:
  brand-source approval does not cover new changing facts.

## Consequences and tradeoffs

The prototype is small and works offline with prepared local source. Consumers
must explicitly adopt a Press Kit, choose existing records and supply facts.
The neutral template is a starting point for voice/destination review. It
offers no compatibility with arbitrary presentation engines or external social
catalogs. Receipt hashes are integrity evidence rather than signatures or
creative/legal approval.

## Implementation and evidence links

See [the consumer guide](../consumers/LAUNCH_DOCUMENTS.md),
`scripts/render_launch_document.py`, the two launch-document schemas and focused
regression source. Implementation exists as an unvalidated candidate. Test
execution and CI are deferred at the maintainer's request; no runtime success,
real consumer acceptance or publication is claimed. Existing ADRs and human
dispositions remain unchanged.

## Replacement or exit strategy

The command is optional and writes only a new generated directory; omitting it
leaves ordinary source and Brand Kit behavior intact. A future template needs
a real consumer, explicit input/rights boundaries and a separately scoped
versioned change. Remove only reviewed owned draft output when abandoning a
candidate; do not rewrite canonical facts or immutable released artifacts.

## Follow-up work

Review the proposed template selection and run the deferred focused/source
suites. Demonstrate a real agreed consumer before closing #106. Final claim,
voice and destination review plus any posting remain with the owner. This
proposal stays unaccepted with null approval.
