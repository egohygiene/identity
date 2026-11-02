---
schema: egohygiene.architecture-decision/v1
id: ADR-0031
title: Keep product components outside the Identity foundations contract
status: proposed
date: "2026-11-02"
decision_scope: repository
visibility: public
owners: [egohygiene/identity]
issue: https://github.com/egohygiene/identity/issues/109
pull_request: null
related: [ADR-0003, ADR-0004, ADR-0009, ADR-0010, ADR-0014, ADR-0030]
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/identity]
affected_contracts: []
implementation_status: implemented
evidence:
  - type: issue
    url: https://github.com/egohygiene/identity/issues/109
    description: Requests a bounded ownership decision rather than a mandatory component library.
  - type: implementation
    url: https://github.com/egohygiene/identity/blob/d247487379569c3701a8cefe6d6136502657fa64/renderer/package.json
    description: The existing renderer is a private reference package, not a downstream component distribution.
approval: null
exceptions: []
---

# ADR-0031: Keep product components outside the Identity foundations contract

## Context

Identity already supplies governed tokens, handbook/context projections and a
reference renderer. Its private renderer contains buttons, navigation and
studio forms. Issue #109 asks whether concrete consumer needs justify a
separately maintained product design system; it explicitly permits a bounded
decision without building one. No shared product interaction gap is identified
in the issue. The [scope inventory](../consumers/PRODUCT_DESIGN_SYSTEM_SCOPE.md)
separates demonstrated needs from possible future work.

## Decision

Propose keeping the existing foundation boundary. Identity owns approved brand
facts, tokens, projection contracts and its reference experience. A consumer
owns application interactions and any selected component dependency. Holon
retains reusable scaffolding. A future shared component system requires a
named consumer, concrete gap, accountable owner and independently versioned API.
No new library or mandatory source section is introduced here.

This proposal remains unaccepted. Its implementation status describes the
already-existing private-renderer/foundation separation and the supplied
inventory; it does not indicate human disposition or verified new behavior.

## Alternatives considered and rejected

- Extract renderer markup as a public component package now: no demonstrated
  shared product API or compatibility promise supports that extraction.
- Mandate one external UI library: #109 identifies neither a selected consumer
  nor a reviewed provider; selecting one would invent a dependency.
- Expand #88 into a component project: that issue preserves existing renderer
  behavior and does not own new product interactions.

## Consequences and tradeoffs

Consumers can reuse brand foundations with their chosen accessible UI. Their
interaction tests and dependency versions remain local. This leaves shared
product components for a later evidenced request and provides no turnkey
application UI promise from the Brand Kit.

## Implementation and evidence links

The scope inventory cites current renderer and foundation paths. Existing
ADRs 0003, 0004, 0009, 0010 and 0014 retain their accepted dispositions. No prior
ADR bytes, public interface, release or deployment changes. Behavioral tests
and pinned ADR validation are deferred with this sprint's other checks; source
inspection is not validation evidence for future consumer behavior.

## Replacement or exit strategy

If the maintainer selects a concrete component pilot, author a bounded owner
proposal with API, platform, accessibility, token compatibility and rollback
requirements. Preserve this proposal and its eventual human disposition rather
than silently converting the reference renderer into a public dependency.

## Follow-up work

Review #109 and choose the bounded scope or a concrete pilot. Record human
approval before closing the decision issue. No speculative component follow-up
is created by this proposal.
