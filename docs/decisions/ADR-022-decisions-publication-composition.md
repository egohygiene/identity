---
schema: egohygiene.architecture-decision/v1
id: ADR-022
title: Compose current Decisions evidence beneath the existing Brand Kit publisher
status: proposed
date: '2026-10-10'
decision_scope: repository
visibility: public
owners:
- egohygiene/identity
issue: https://github.com/egohygiene/identity/issues/69
pull_request: null
related:
- ADR-011
- ADR-017
- ADR-018
- ADR-019
supersedes: []
superseded_by: []
affected_repositories:
- egohygiene/identity
affected_contracts: []
implementation_status: in_progress
evidence:
- type: implementation
  url: https://github.com/egohygiene/identity/blob/642d096e60b729060e5880e5222d7b57184b735e/.github/workflows/publish-brand-kit.yml
  description: Existing single Pages publisher selects an immutable stable Brand Kit release and verifies its canonical domain.
- type: documentation
  url: https://github.com/egohygiene/identity/blob/642d096e60b729060e5880e5222d7b57184b735e/docs/decisions/ADR-017-zensical-launchkit-publication-architecture.md
  description: Accepted two-surface architecture and N017 leave Decisions hosting and deployment as a separate consumer choice.
- type: validation
  url: https://github.com/egohygiene/identity/blob/e23fad23227b933f524e6677ea1e195cf1ba1788/docs/evidence/identity-adrs-ratified-2026-10-10.json
  description: Prior 21-record corpus passed immutable native collection and repeatable local production builds; this is not deployment evidence.
- type: implementation
  url: https://github.com/egohygiene/relay/tree/cabbf5b3b658d585b4d56ef0c99917969a96eed2/actions/repository-intelligence
  description: Pinned shared production action provides fresh validated ADR collection and the Intelligence subtree.
- type: implementation
  url: https://github.com/egohygiene/relay/tree/cabbf5b3b658d585b4d56ef0c99917969a96eed2/actions/repository-intelligence-deployment-provenance
  description: Pinned shared action captures the consumer baseline, verifies composition and records a separate deployment receipt.
- type: pull_request
  url: https://github.com/egohygiene/relay/pull/138
  description: Repairs baseline path ordering for mixed brand/ and brand-kit/ paths without changing the inventory or site-digest contract.
approval: null
exceptions: []
---

# ADR-022: Compose current Decisions evidence beneath the existing Brand Kit publisher

## Context

Identity's canonical ADR migration is merged, and its 21-record source has
bounded native and local production-build evidence. That evidence does not
choose a host or demonstrate deployment. ADR-017 preserves the release-backed
Brand Kit at `identity.egohygiene.io` and the separately owned organization
`/identity/` experience; its approved N017 clarification leaves Decisions
hosting open. Current repository decisions also have a different update cycle
from the immutable stable Brand Kit release.

The publication work is authorized separately from ADR lifecycle disposition.
This record proposes the durable composition boundary and remains proposed;
implementation, a merge, and deployment do not accept it. Existing ADR-001–021
and their explicit human dispositions remain unchanged.

## Decision

Extend Identity's existing `Publish Identity Brand Kit` workflow as the sole
Pages publisher for `https://identity.egohygiene.io/`. Build the stable-release
Brand Kit first, then compose the pinned Relay production action's output at
`renderer/dist/intelligence`. Publish Decisions at `/intelligence/decisions/`
and add the consumer-owned `/decisions/` redirect to that route. Do not move
the Brand Kit root or install anything beneath the organization `/identity/`
route.

Keep three source identities explicit: the trusted publisher commit, the
annotated stable Brand Kit release tag/commit, and the full Git commit used for
ADR collection. The default ADR source is the exact publisher revision. An
optional manual `intelligence_revision` may select a full ancestor commit,
which must undergo fresh validated collection; an old review envelope is not
publishable input. Preserve the existing stable-release restrictions and do not
describe current decisions as contents of `v1.0.0`.

Capture the complete Brand Kit path/byte inventory before composition, reject
collisions or changes to those files, verify required routes and the alias,
and retain the exact composed artifact with source bindings and digests.
After deployment, verify the live Decisions subtree and preserved Brand Kit
bytes against that artifact. Record the Pages deployment result separately
from live verification so successful upload or deployment cannot conceal a
failed domain/content proof.

## Alternatives considered and rejected

- A second Pages publisher for the same repository would compete with the
  existing site's whole-artifact deployment. Use one composed artifact instead.
- Installing Decisions on the organization `/identity/` experience adds a
  separate route owner and product-experience release gate to this bounded
  consumer implementation. Preserve that independently governed surface.
- Building current ADRs from the `v1.0.0` release tree, or labelling current ADR
  bytes as release-owned assets, would conflate two different source contracts.
- Publishing the retained review envelope or a previous unvalidated projection
  would bypass the production action's complete/current ADR admission gate.

## Consequences and tradeoffs

One publisher preserves the existing domain and release assets while allowing
decisions to follow reviewed repository history. It also couples availability
of a new Brand Kit deployment to successful fresh Intelligence collection and
composition; failure stops the whole candidate artifact from being deployed.
The consumer owns its alias, source bindings and live checks, while Relay owns
the reusable collection and projection mechanics.

The generated projection must retain the source record's actual lifecycle and
implementation states, including this proposed record. Acceptance of the
earlier 21 records is not transferred to this proposal. A public projection
remains derived evidence and cannot replace canonical Markdown or human
disposition authority.

## Implementation and evidence links

The implementation extends the [existing publisher](../../.github/workflows/publish-brand-kit.yml)
with the two Relay actions pinned above. The
[publication guide](../publication/IDENTITY_PAGES.md#decisions-composition-checkpoint--2026-10-10)
defines the route, evidence and recovery boundary; the
[validation guide](../decision-validation.md#review-collection-and-later-publication)
distinguishes the previous immutable 21-record receipt from fresh validation of
this 22-record candidate.

The prior receipt demonstrates source admission and local artifact generation
only. No hosted deployment, live composition proof, completed rollback exercise
or maintainer feedback is asserted by this proposed record. Attach those
results to the implementation handoff at their exact source revision.

## Replacement or exit strategy

Retain a verified prior deployment inventory and digest before installing the
composed site. The earlier Pages artifact may have expired; a workflow run ID
alone is not recoverable artifact evidence. Preserve the exact current
composition for later re-promotion and separately verify any reconstructed
earlier recovery artifact against its recorded inventory.

The [rollback capture](../../publication/decisions-rollback.json) records the
40 files retrieved from the live site on 2026-10-10 using the previous upload
log's complete path inventory. Its site digest is
`sha256:c690803f5eda55c7b61d7ae34a1df3e109d2dad9aad9a34ef086207d4cd0fd88`.
This establishes a new capture of the served site, not recovery or independent
reverification of the expired original Actions ZIP. The consumer's
`capture-rollback` operation freshly checks all 40 paths against that record and
emits `rollback-site.tar`, `rollback-record.json` and `rollback-capture.json`.
Retain those outputs before deployment. Using the capture for a later rollback
remains a separate delivery step.

Manual release rollback still selects an already-published stable annotated
tag. Decisions replay uses the independent full ancestor source commit and
fresh collection gate. If the new Intelligence path cannot pass its gates,
restore a reviewed, byte-verified prior Brand Kit-only artifact through the
existing owner rather than bypassing validation. Record the actual rollback
deployment and live verification separately; availability of a plan does not
establish that a rollback was exercised.

## Follow-up work

- Validate the full candidate corpus, composition and retained handoff at the
  exact immutable implementation revision.
- Retain the recovered prior-site bytes with their inventory/digest, then
  deploy and retain the actual receipt plus live verification results.
- Show the deployed Decisions page to the maintainer for feedback before
  continuing the repository-by-repository fleet rollout.
- Obtain a separate explicit human disposition for ADR-022; do not infer it
  from implementation/deployment authorization or the earlier R1 approval.

