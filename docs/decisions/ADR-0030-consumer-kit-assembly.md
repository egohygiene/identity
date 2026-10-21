---
schema: egohygiene.architecture-decision/v1
id: ADR-0030
title: Assemble native consumer kits with a complete offline inventory
status: proposed
date: "2026-10-21"
decision_scope: repository
visibility: public
owners: [egohygiene/identity]
issue: https://github.com/egohygiene/identity/issues/105
pull_request: https://github.com/egohygiene/identity/pull/129
related: [ADR-0001, ADR-0003, ADR-0005, ADR-0010, ADR-0011, ADR-0014, ADR-0015, ADR-0017, ADR-0019, ADR-0024, ADR-0028, ADR-0029]
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/identity]
affected_contracts: []
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/identity/issues/105
    description: Requests one usable kit, matching downloads and optional projections, source/release integrity, public filtering and explicit publication ownership.
approval: null
exceptions: []
---

# ADR-0030: Assemble native consumer kits with a complete offline inventory

## Context

The native compiler already selects governed public artwork and actual targets.
The optional handbook and Press Kit own their approved facts. The legacy
Identity publisher separately constructs a release-specific model from older
export configuration. Passing optional directories to a model-only render does
not assemble their complete files with the native outputs or establish complete
site integrity. Public visitors also see local review controls and explicit
empty sections that are useful in an authoring preview.

Accepted ADR-0010 already owns the immutable model/renderer boundary,
ADR-0014/0015 the governed optional projections, ADR-0011 layered quality,
ADR-0017 publication ownership and ADR-0019 immutable release selection.
Existing proposed path/rights/selection records retain their proposal states.
A new output receipt is a durable consumer interface, so it needs this separate
proposal; implementation or merge does not accept it.

## Decision

Propose an explicit native consumer-kit assembler alongside the existing
release-backed publisher. Read the native model and compiler manifest plus
explicitly supplied generated optional projections. Preserve project/source
binding and release metadata. Copy only verified native inventory files and
the exact optional files; never read canonical source, infer missing facts,
rewrite approved artwork or claim publication.

Use the existing renderer with a public-audience option. Hide absent sections
and the review studio while retaining essential static content and downloads.
Keep the independent preview's existing behavior and approved visual baseline.
Reuse existing native/Press Kit archives and handbook downloads. Label the
native archive as an asset package rather than implying optional exports were
added to it. No new all-in-one ZIP is introduced.

Retain the native compiler manifest/model unchanged. Compose the existing
optional model fields into a separate downloadable view model. Define
`identity.consumer-brand-kit/v1` in `kit.json`: project ID, source digest, exact
release object, artifact base, browser asset selections and a sorted map of all
output file hashes/sizes excluding itself. This receipt supplies offline
integrity, not a signature or an approval source.

Verify the entire output inventory, actual compiler binding, optional JSON/page
agreement, handbook Markdown/JSON agreement, selected download links and navigation. Reconstruct the native-only
Press Kit package to reject changed assets, extra files and ZIP member injection.
Keep external social-package admission separate. Reject input/output overlap,
canonical-source destinations and nonempty output replacement before writes.

## Alternatives considered and rejected

- Reconstruct another brand model from publication configuration: creates
  drift from the already governed native/public selection and optional facts.
- Copy entire consumer directories: can distribute neighboring private or
  unselected files outside the producer inventories.
- Render only HTML with hand-copied assets: leaves optional artifacts and
  native manifests unassembled and cannot verify every delivered file.
- Add another archive: existing packages plus one verified directory already
  meet the demonstrated consumer need without a second package format.
- Change the current stable publisher/routes: couples this integration work to
  release, deployment and organization installation authority it does not own.

These are current proposal alternatives, not reconstructed historical rationale.

## Consequences and tradeoffs

The consumer command requires actual generated inputs and a new/empty output
directory. Model-only previews remain independently usable. The new receipt
does not alias the existing published `site.json` contract. A matching reviewed
compiler, projection generator and renderer must be selected together; old
immutable releases and their readers remain intact.

Successful verification proves agreement of supplied bytes and metadata, not
complete accessibility conformance, rights authenticity, creative acceptance,
registry/account ownership, remote availability or deployment. Unresolved
legacy logo rights remain unknown; canonical self-source/release adoption
continues under #98. No accepted ADR or human approval is changed.

## Implementation and evidence links

The [assembly guide](../consumers/COMPLETE_BRAND_KIT.md),
[receipt schema](../../contracts/v1/consumer-brand-kit.schema.json),
[builder](../../renderer/scripts/build-kit.mjs) and
[verifier](../../renderer/scripts/verify-kit.mjs) describe the candidate.
The [fixture receipt](../../renderer/fixtures/complete-kit/receipt.json) binds
two independent native generations for minimal/expanded synthetic cases and
unchanged Mantle source. Runtime results, exact PR source and unavailable
checks belong in the PR and CONTINUITY.md; authored tests are not executed
evidence. This record remains proposed with null approval.

## Replacement or exit strategy

Keep earlier immutable compiler/projection/renderer sets for rollback. A future
assembler can replace this adapter when it consumes the same governed inputs
and proves equivalent integrity and public filtering. Version a breaking
receipt change explicitly. Do not repurpose a published receipt or overwrite
canonical source to manufacture compatibility.

## Follow-up work

Obtain human disposition independently. #98 retains canonical self-source,
stable release, live publication and contrasting-consumer rollout acceptance.
#70/#80 retain the broader quality and actual local-Docker campaign. #83 owns
final documentation reconciliation; optional product/imagery/template and
ecosystem coordination issues retain their existing priorities.
