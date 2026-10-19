---
schema: egohygiene.architecture-decision/v1
id: ADR-0025
title: Keep the executable authoring core independent of optional guidance
status: proposed
date: "2026-10-19"
decision_scope: repository
visibility: public
owners: [egohygiene/identity]
issue: https://github.com/egohygiene/identity/issues/99
pull_request: null
related: [ADR-0001, ADR-0012, ADR-0013, ADR-0015, ADR-0019]
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/identity]
affected_contracts: []
implementation_status: in_progress
evidence:
  - type: pull_request
    url: https://github.com/egohygiene/identity/pull/114
    description: Merged field audit demonstrates nullable-guidance disagreement and source-format/producer capability gaps without adopting implementation choices.
  - type: documentation
    url: https://github.com/egohygiene/identity/blob/1b46f01308d63f38068ce5327d36ac94b0840077/contracts/v1/project.schema.json
    description: The existing closed project schema requires voice/usage keys but permits an explicit null for either document path.
approval: null
exceptions: []
---

# ADR-0025: Keep the executable authoring core independent of optional guidance

## Context

The #99 field audit found that the published source schema permits null voice
and usage paths while the authoritative validator and Rust bridge require both
files. The existing normalized guidance and Rust package models already have
absence representations. A small source therefore needs an executable omission
contract, rather than approval-shaped placeholder prose. ADR-0012 governs local
source, ADR-0013 the lifecycle of adopted guidance, and ADR-0001 human authority.

The same audit distinguishes valid governed asset bytes from producer support:
a PNG passes source validation but fails UTF-8 loading in the SVG-only bridge.
Examples must teach both boundaries without claiming a complete public kit.

## Decision

Propose independently nullable voice and usage declarations as the executable
v1 authoring core. Keep both keys required. A non-null path still requires a
valid complete document and its existing subject-matched governance. An explicit
null means not declared: skip document loading and expose existing null/empty
projection states without manufacturing copy, rights, approval or readiness.
Adopted dependent projections retain their own prerequisites and useful errors.

Keep project facts, token layers, selected profiles, source provenance and human
decisions in their existing authoritative documents. Reuse governed voice
foundation/context naming and Press Kit boilerplates for richer copy; add no
new project-profile fields without a demonstrated consumer. Keep local pinned
token defaults and reviewed overrides, with no generic inheritance framework.

Distinguish source validity, producer support, verified selected output and public
kit readiness. The current Rust bridge requires SVG for every provenance asset;
report unsupported formats before UTF-8 decoding without globally invalidating
governed raster/font source. Supply minimal and expanded synthetic examples and
a worksheet; preserve the existing regression fixture and digest algorithm.

## Alternatives considered and rejected

- Require both guidance documents universally: contradicts the existing nullable
  schema and forces invented material into a minimum compilation path.
- Treat missing keys, empty paths or malformed documents as absence: hides
  authoring mistakes and weakens closed-contract diagnostics.
- Make all governed source SVG-only: conflates producer limitations with the
  source authority and byte-copy capabilities of optional packages.
- Add a second profile/copy catalog or generic defaults framework now: duplicates
  existing authorities before a concrete consumer establishes a missing field.

These are alternatives considered for this proposal, not reconstructed claims
about the original decisions.

## Consequences and tradeoffs

Existing valid populated sources, entry points and output behavior remain
supported. Explicit null becomes executable, but older tools may still reject
it at runtime; consumers need the exact reviewed implementation until a new
immutable release includes it. The schema major and software version are not
substitutes for source/release identity.

Absence does not waive selected-profile asset requirements or approve a public
kit. All physical canonical files remain in the existing source digest even
when a guidance declaration is null. Standalone review models permit absent
singleton records; declared records retain their schema and lifecycle rules.
Unsupported-format diagnostics do not add a raster/font decoder or discard
canonical assets automatically.

## Implementation and evidence links

The candidate aligns the source validator, Rust bridge, standalone guidance and
dependent projection errors. The source and guidance contracts describe the
bounded behavior; examples and tests exercise it. Exact executed checks and the
reviewed commit belong in the PR and CONTINUITY.md. This proposed record does
not infer human disposition from implementation, testing or a future merge.

## Replacement or exit strategy

Consumers can retain their immutable older tool/source set or restore populated
guidance with valid existing approvals. Any future change to required topology,
source-digest framing, copy authority or format support gets its own compatible
contract review; do not mutate published releases or reinterpret null as approval.

## Follow-up work

#99 checkpoint 3 proves a representative real authoring path and bounds v1
initialization/EgoLint handoffs. #100 owns further naming/copy needs; #101/#105
retain public asset selection, supported practical variants and actual advertised
downloads. #103 owns rights/policy presentation; #106–#109 retain their optional
or external scope decisions. Complete-kit release and canary proof stay with #98.
