---
schema: egohygiene.architecture-decision/v1
id: ADR-0028
title: Project asset rights without inventing missing authority
status: proposed
date: "2026-10-20"
decision_scope: repository
visibility: public
owners: [egohygiene/identity]
issue: https://github.com/egohygiene/identity/issues/103
pull_request: null
related: [ADR-0001, ADR-0003, ADR-0007, ADR-0010, ADR-0012, ADR-0013, ADR-0015, ADR-0019]
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/identity]
affected_contracts: []
implementation_status: implemented
evidence:
  - type: issue
    url: https://github.com/egohygiene/identity/issues/103
    description: Requests traceable asset rights, explicit unresolved permissions and authoritative policy/contact references without adopting legal policy.
  - type: implementation
    url: https://github.com/egohygiene/identity/blob/4db8766ba01b742353c617720aebec6a11f88888/src/v1_consumer.rs
    description: Existing source asset loading reads provenance usage but does not carry it into source governance or the reference-renderer model.
  - type: implementation
    url: https://github.com/egohygiene/identity/blob/4db8766ba01b742353c617720aebec6a11f88888/renderer/scripts/build-public-site.mjs
    description: Existing publication projection supplies invented license, origin and approval defaults when legacy configuration omits those fields.
  - type: documentation
    url: https://github.com/egohygiene/identity/blob/4db8766ba01b742353c617720aebec6a11f88888/docs/contracts/PRESS_KIT_V1.md
    description: Existing governed Press Kit records already own approved assets, links, contacts and public lifecycle selection.
approval: null
exceptions: []
---

# ADR-0028: Project asset rights without inventing missing authority

## Context

The #103 inventory found rights already represented in local provenance and
governed usage guidance. Press Kit JSON preserves selected assets' license,
attribution, origin, usage and approval, while its page and Markdown omit much
of that evidence. The core Rust bridge discards provenance usage before the
reference renderer can present it.

The separate release-backed publisher fills absent configured rights metadata
with MIT/approved attribution, a creator/capture date and a human approval
claim. Some legacy configurations omit those fields. A build cannot establish
the missing rights or authority. The publisher also packages the selected
release tree independently of this presentation metadata, so changing a label
cannot be described as withholding its bytes.

Accepted ADR-0001 retains human approval, ADR-0003 deterministic projection,
ADR-0010 the immutable renderer port, ADR-0012 local provenance, ADR-0013 public
lifecycle filtering and ADR-0015 the governed Press Kit. ADR-0007 separately
requires approved local font bytes and license evidence; a provider URL or
family name is insufficient.

## Decision

Propose an optional per-asset `usage` object in the existing Brand Kit source
governance and `identity.brand-kit-view-model/v1` projection. Carry the existing
`safeZone`, `minimumSize` and `restrictions` strings/list verbatim. Omit the
member when a legacy input has none; do not derive numeric preview constraints
from these prose fields.

Render existing rights, attribution, origin, usage, digest and approval data
readably. Present supplied trademark, copyright and third-party notices as
distinct guidance. Reuse governed Press Kit links and contacts for authoritative
policies, support/community destinations and external font acquisition; labels
and IDs do not activate inferred policy semantics or copy policy ownership.
The Press Kit's projected asset approval remains its selection approval; the
asset ID/digest binds validated provenance without adding a second exported
source-approval field.

Preserve missing configured publication license, origin and approval as null
and expose their absence. Never manufacture an MIT license, creator, capture
date or approval. Keep the existing release publisher's byte/archive selection
unchanged in this bounded repair. Unknown permissions remain unresolved; this
proposal neither establishes them nor claims the already-selected bytes were
withheld. Governed v1 Press Kit selection retains its approved/public boundary.

Keep the existing model identifier and adapter version for the optional member,
with matching reviewed compiler/schema/renderer pins required for adoption.
This proposal grants no new legal, creative, distribution or publication
authority and implements no font download or optional font-tool adapter.

## Alternatives considered and rejected

- Infer asset rights from the repository software license or fill plausible
  defaults: creates unsupported permission and approval claims.
- Keep discarding usage constraints: leaves distributed assets without their
  existing reviewed restrictions in the renderer.
- Add another policy/reference catalog or copy external policy text: duplicates
  existing governed links and moves authority away from its actual owner.
- Redesign legacy release selection as part of this metadata repair: expands
  the change into archive/publication authority without establishing the missing
  owner evidence. The unresolved legacy metadata remains explicit for kit review.

These are alternatives considered for this proposal, not reconstructed claims
about earlier decisions.

## Consequences and tradeoffs

Existing models without per-asset usage remain valid, and omission preserves
their prior serialized shape. Models that supply usage need updated readers:
older strict Rust consumers can reject the new member despite the unchanged v1
identifier. Pin compatible producer, schema and renderer together and rebuild
the complete source-bound handoff; do not edit immutable old packages.

Human-readable exports now include supplied rights evidence that JSON already
carried. Those regenerated bytes and their package checksums change together.
The software license, trademark guidance and third-party rights remain distinct;
an empty list or missing metadata is no waiver or blanket permission.

Null legacy publication metadata makes an evidence gap visible but does not
repair it or change the archived release contents. The owner must assess actual
distributed bytes and rights before declaring a complete consumer kit ready.
Acquisition-only font links do not download or redistribute fonts.

## Implementation and evidence links

The candidate carries provenance usage through Rust source governance and the
renderer model, displays existing rights/legal fields, includes them in Press
Kit Markdown and removes fabricated publication defaults. Focused checks must
cover exact source text, absent metadata, legacy omission, public lifecycle
filtering and unchanged release selection. Record actual commands, source
revisions and results in the PR and CONTINUITY.md. Implementation, tests or a
merge do not accept this proposal or establish a release/deployment result.

## Replacement or exit strategy

Retain prior immutable tool/package sets for rollback. A consumer without usage
can continue using the older shape; one adopting the new member must keep a
compatible reader or regenerate from an earlier reviewed tool/source selection.
Do not restore invented rights to make a legacy page look complete. Resolve
missing metadata only from actual owner evidence, and review any future change
to publication/archive selection as its own authority-sensitive work.

## Follow-up work

Issue #103 owns this bounded rights presentation and reference reuse. Issue #102
retains broader typography presentation; #105/#98 retain complete-kit and actual
release/self-dogfood acceptance. Issue #70 owns the deferred final full quality
pass. Human disposition of this proposed decision remains separate.
