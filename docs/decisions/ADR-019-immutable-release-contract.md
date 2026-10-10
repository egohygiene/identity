---
schema: egohygiene.architecture-decision/v1
id: ADR-019
title: Preserve an independent immutable Identity release contract
status: accepted
date: '2026-10-10'
decision_scope: repository
visibility: public
owners:
- egohygiene/identity
issue: https://github.com/egohygiene/identity/issues/18
pull_request: https://github.com/egohygiene/identity/pull/43
related:
- ADR-003
- ADR-011
- ADR-012
- ADR-017
supersedes: []
superseded_by: []
affected_repositories:
- egohygiene/identity
affected_contracts: []
implementation_status: implemented
evidence:
- type: pull_request
  url: https://github.com/egohygiene/identity/pull/43
  description: Introduces the release candidate, version pairing, supported source-install matrix, archive,
    SBOM, license inventory, checksums, and attestation path.
- type: documentation
  url: https://github.com/egohygiene/identity/blob/8aae2c6767d07714ea16bf0ea493e1f1ac399b6e/docs/releases/RELEASE_PROCESS.md
  description: Immutable inspected release procedure and rollback boundary; implementation evidence rather
    than human ADR ratification.
- type: implementation
  url: https://github.com/egohygiene/identity/blob/8aae2c6767d07714ea16bf0ea493e1f1ac399b6e/.github/workflows/release.yml
  description: Repository-owned release workflow at the audited source revision; not a newly executed
    release or validation result.
- type: approval
  url: https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806
  description: Explicit maintainer acceptance on 2026-10-10 of R1 at 418aa9757898b6c09b4f01eface522778cff90e8;
    recorded by Codex on the maintainer's behalf.
approval:
  date: '2026-10-10'
  by: szmyty
  evidence: https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806
exceptions: []
---

# ADR-019: Preserve an independent immutable Identity release contract

The original reconstruction below is preserved as pre-approval history. Its
proposed-state and pending-review wording describes that earlier checkpoint;
the current human disposition is recorded in front matter and the dated note
below.

## Context

Identity's CLI, source contracts, generated packages, and reference renderer
need a versioned distribution boundary that consumers can pin independently
of a website deployment. ADR-017 records the two public presentation surfaces;
it does not fully record the preceding release artifact and compatibility
decision. The inspected release procedure and workflow already implement this
boundary. This historical reconstruction proposes documenting that choice;
it supplies no missing human ratification or permission to publish a release.

## Decision

Retain one immutable annotated `v<package-version>` selection whose version
matches both the Rust package and reference renderer. Distinguish release
candidates from stable releases. Bind the Linux archive, SHA-256 checksums,
SPDX SBOM, locked-dependency license inventory, and build-provenance
attestation to that exact release selection.

Keep Linux, macOS, and Windows source-install and clean-room evidence explicit;
the Linux binary archive does not imply equivalent binary distributions for
every platform. A released CLI can be used independently. Brand Kit deployment
is separately evidenced and consumes the selected immutable stable release.
Consumer pin changes and site publication retain their respective owners.

## Alternatives considered and rejected

The inspected procedure rules out moving a release tag or replacing a bad
asset under the same version: publish a corrected higher version and retain
an explicit warning or support disposition instead. It also separates release
source from a mutable default-branch asset tree. Contemporaneous discussion of
other distribution designs was not located; no additional historical motives
or alternatives are inferred.

## Consequences and tradeoffs

Consumers receive a reproducible version and rollback point, while release
operators must maintain compatibility, support documentation, artifact
integrity, and platform-specific evidence. Site and CLI status can differ and
must be reported separately. A workflow implementation or old successful run
does not establish current release readiness.

## Implementation and evidence links

[PR #43](https://github.com/egohygiene/identity/pull/43) introduced the candidate
path; [PR #44](https://github.com/egohygiene/identity/pull/44) corrected its
tag checkout, and [PR #45](https://github.com/egohygiene/identity/pull/45)
prepared the stable source. The immutable source links in front matter and
the existing [release procedure](../releases/RELEASE_PROCESS.md) support
`implemented`. No release, download, clean-room build, or hosted check was
rerun for this record, so its implementation status is not `verified`.

## Replacement or exit strategy

Move release execution to a reviewed reusable Relay contract only after its
artifact, version, trust, compatibility, and rollback behavior are proven
equivalent. Preserve historical tags and artifacts. A change to those durable
guarantees needs a proposed replacement or amendment with explicit evidence.

## Follow-up work

Obtain explicit human disposition of this proposed record. Reconcile future
release claims with exact current source, runs, artifacts, and consumer pins
under the release owner's existing acceptance process.

## Reconstruction note

Reconstructed on 2026-10-10 from main revision
`8aae2c6767d07714ea16bf0ea493e1f1ac399b6e` and public PR evidence. The first
release-candidate implementation is present in commit
`156841076affd8967297476f6a4a360f6602feca` dated 2026-08-27. That source date
does not prove a historical approval date. This ADR remains proposed.

## Human disposition — 2026-10-10

Maintainer `szmyty` explicitly accepted ADR-019 as a separate proposed-record
choice in [recommendation set R1](https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md).
The [durable disposition](https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806) records
that approval on 2026-10-10. The original reconstruction text and evidence
remain intact; implementation stays `implemented`, with no new runtime,
release, creative-asset, account or deployment verification inferred.
