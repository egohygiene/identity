---
schema: egohygiene.architecture-decision/v1
id: ADR-0027
title: Reuse Press Kit boilerplates for optional paragraph descriptions
status: proposed
date: "2026-10-20"
decision_scope: repository
visibility: public
owners: [egohygiene/identity]
issue: https://github.com/egohygiene/identity/issues/100
pull_request: https://github.com/egohygiene/identity/pull/124
related: [ADR-0001, ADR-0003, ADR-0005, ADR-0010, ADR-0013, ADR-0015, ADR-0025]
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/identity]
affected_contracts: []
implementation_status: implemented
evidence:
  - type: pull_request
    url: https://github.com/egohygiene/identity/pull/124
    description: Candidate implements readable governed profiles and optional paragraph reuse; focused checks and review are recorded without implying human ADR acceptance or full CI qualification.
  - type: issue
    url: https://github.com/egohygiene/identity/issues/100
    description: Requests supplied one-sentence, paragraph and longer descriptions while preserving existing copy authority and public filtering.
  - type: documentation
    url: https://github.com/egohygiene/identity/blob/2d18ed114d3799da3867260d69d8c70bf05d428d/contracts/v1/press-kit.schema.json
    description: Existing governed boilerplate records accept only short and long kinds; no separately supplied paragraph kind exists at this base.
  - type: documentation
    url: https://github.com/egohygiene/identity/blob/2d18ed114d3799da3867260d69d8c70bf05d428d/docs/consumers/AUTHORING.md
    description: Existing authoring guidance reuses voice and Press Kit authorities and rejects a competing project-profile copy catalog.
approval: null
exceptions: []
---

# ADR-0027: Reuse Press Kit boilerplates for optional paragraph descriptions

## Context

Issue #100 requires reusable supplied descriptions at three editorial lengths.
The existing Press Kit owns approved short and long descriptions, governed facts,
links and contacts. Its closed boilerplate enum cannot represent a separately
approved paragraph. Adding profile fields to the closed project manifest or
writing page-only copy would create another authority for the same material.

Accepted ADR-0015 governs the optional Press Kit projection, ADR-0013 public
lifecycle filtering, and ADR-0001 human approval. Proposed ADR-0025 describes
reuse of existing copy homes; it remains proposed and supplies no acceptance
for this extension.

## Decision

Propose one optional `paragraph` kind in the existing
`identity.press-kit-source/v1` and `identity.press-kit/v1` boilerplate records.
Require unique kinds and retain exactly one short and one long source record.
Public generation still requires both approved/public descriptions; paragraph
is included only when its own governance passes the same boundary.

Keep existing schema identifiers and projection version for this bounded enum
extension. Pin compatible schemas, validator, producer and renderer together;
the identifier alone does not promise support in older implementations.

Reuse each supplied text verbatim in the page's copy control, JSON, Markdown
and ZIP. Omit an absent or withheld paragraph without synthesizing it from
another description. Short/paragraph/long are editorial labels, not automatic
length rules. The optional Press Kit stays optional for core consumers.

Continue using governed voice foundation/contexts for purpose, positioning,
audience, personality and naming rules. Optional labeled Press Kit facts can
carry supplied short names, distinct mission statements, values or pronunciation
without machine interpretation of their labels. No renderer permission, legal
claim or source field is inferred from that presentation.

## Alternatives considered and rejected

- Add a project-profile or copy document: duplicates existing authorities for
  this demonstrated description-length gap.
- Encode the paragraph as an ordinary fact: loses its explicit description role
  and forces consumers to infer semantics from a fact label or stable ID.
- Generate a paragraph from short/long copy: creates unapproved wording.
- Make all three lengths mandatory: forces new material on existing valid kits.

These alternatives were considered for this proposal; they do not reconstruct
the rationale of earlier decisions.

## Consequences and tradeoffs

Existing short/long-only sources retain their validation and public-content
requirements. The new kind carries the existing provenance and subject-matched
approval envelope, with no extra publication authority or factual approval.

The extension is additive for these existing sources, but older closed schemas
and producers can reject paragraph records; older renderers can reject or omit
them. Adoption therefore requires a reviewed compatible tool set and rebuilt,
source-bound handoffs. A future immutable release must identify that support;
this proposal does not claim an older stable release includes it.

This does not create translated copy, a communications CMS, new trademark
permissions, or a generic semantic profile-fact registry. Those remain separate
consumer needs and require their own review when demonstrated.

## Implementation and evidence links

The candidate extends the existing source/projection schemas, source validator,
Press Kit projector and renderer. Focused checks must exercise exact supplied
text, optional omission, unique kinds and exclusion of internal/unapproved
records across public output. Record executed results and the reviewed source
in the PR and CONTINUITY.md; implementation, tests or merge do not accept this
proposal. No final-head CI, release or publication result is asserted here.

## Replacement or exit strategy

Retain earlier immutable schema/tool/package sets for rollback. Consumers that
do not need paragraph copy can keep the original short/long-only source. To
return a paragraph-adopting consumer to older tooling, remove that optional
record through its normal reviewed source change and regenerate the complete
digest-bound package set; do not edit generated packages or relabel approved
text to bypass validation.

## Follow-up work

Issue #100 owns the current readable profile/copy presentation and focused
public-filtering evidence. Issue #70 retains the deferred final full quality
pass. Issue #98 owns the later complete-kit release, self-dogfood and adoption
acceptance. Human disposition of this proposed decision remains separate.
