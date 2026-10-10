---
schema: egohygiene.architecture-decision/v1
id: ADR-021
title: Keep mascot source and approved derivatives behind a governed package
status: accepted
date: '2026-10-10'
decision_scope: repository
visibility: public
owners:
- egohygiene/identity
issue: https://github.com/egohygiene/identity/issues/50
pull_request: https://github.com/egohygiene/identity/pull/58
related:
- ADR-001
- ADR-003
- ADR-013
- ADR-017
supersedes: []
superseded_by: []
affected_repositories:
- egohygiene/identity
affected_contracts: []
implementation_status: implemented
evidence:
- type: pull_request
  url: https://github.com/egohygiene/identity/pull/58
  description: Implements optional mascot source and package contracts with exact asset provenance, approval,
    rights, accessibility, and derivative bindings.
- type: documentation
  url: https://github.com/egohygiene/identity/blob/8aae2c6767d07714ea16bf0ea493e1f1ac399b6e/docs/contracts/MASCOT_SYSTEM_V1.md
  description: Inspected source, package, publication, validation, and rollback boundaries for the mascot
    capability.
- type: issue
  url: https://github.com/egohygiene/identity/issues/50
  description: Issue containing explicit human approval of a specific visual selection and governed promotion;
    does not ratify this reconstructed architecture ADR.
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

# ADR-021: Keep mascot source and approved derivatives behind a governed package

The original reconstruction below is preserved as pre-approval history. Its
proposed-state and pending-review wording describes that earlier checkpoint;
the current human disposition is recorded in front matter and the dated note
below.

## Context

A mascot must carry reviewed identity, rights, provenance, accessibility,
usage, and approval when reused across a Brand Kit and product pages. An image
prompt or a generated crop cannot supply those authorities. The implemented
mascot source/package contracts add a durable optional boundary beyond the
general human-approval and projection choices in ADR-001 and ADR-003.

## Decision

Keep character identity and constraints in the optional local
`identity.mascot-source/v1` selected by `documents.mascot`. Bind its canonical
asset to explicit provenance, exact SHA-256, rights, and asset approval;
retain the distinct human decision for the character system.

Project reviewed variants into `identity.mascot-package/v1`, retaining exact
bytes, dimensions, media type, license, source identity, and usage metadata.
Public renderers consume these immutable artifacts and never become a second
source for names, visual invariants, approvals, or rights. Consumers without
the mascot document remain valid. Candidate imagery remains separate from
approved source and cannot promote itself through a generated package.

## Alternatives considered and rejected

The existing contract excludes using a prompt, page, or generated crop as
canonical brand intent, silently approving candidate imagery through package
inclusion, and publishing assets absent from the selected stable release.
No broader contemporaneous alternatives study was located. This record does
not infer one or retroactively approve additional character designs.

## Consequences and tradeoffs

One reviewed character can be reused consistently across products while
maintaining rights and provenance. Variant creation and later motion changes
require their own reviewed constraints and evidence. Mascots cannot be the
sole carrier of status, instructions, or navigation; accessible text remains
necessary. More explicit metadata creates maintenance work, but page styling
cannot silently alter brand authority.

## Implementation and evidence links

[PR #58](https://github.com/egohygiene/identity/pull/58) implements the source,
package, validation and renderer handoff. The
[mascot contract](../contracts/MASCOT_SYSTEM_V1.md) and
[Kern source](../../mascot/kern.character.json) document the existing reference.
The [human comment in issue #50](https://github.com/egohygiene/identity/issues/50#issuecomment-5463168075)
approves the specific visual selection and promotion through existing governance;
it is not evidence that this later architecture ADR was accepted. No asset, rights, rendering or
publication check was rerun for this reconstruction.

## Replacement or exit strategy

Change character contracts through an explicit reviewed version/migration.
Restore previous source, provenance, approvals, manifest and derivative bytes
together when rolling back. Replacing a renderer must preserve package
integrity and character authority. A changed character direction needs its
own human disposition rather than editing historical approvals.

## Follow-up work

Obtain explicit disposition of this proposed architecture record. Preserve
the existing source and visual-selection approval while any new character,
derivative, motion, or publication change follows its actual owner contract.

## Reconstruction note

Reconstructed on 2026-10-10 from main revision
`8aae2c6767d07714ea16bf0ea493e1f1ac399b6e`. The implementation commit
`e4ee943442a492127d600761fe622714ede10be5` and recorded human visual selection
are dated 2026-08-29. Neither establishes an acceptance date for this new ADR.
Existing `identity.*` contract IDs remain unchanged in the prose; no new
organization contract registration is implied by this record.

## Human disposition — 2026-10-10

Maintainer `szmyty` explicitly accepted ADR-021 as a separate proposed-record
choice in [recommendation set R1](https://github.com/egohygiene/identity/blob/418aa9757898b6c09b4f01eface522778cff90e8/docs/decision-disposition-review-2026-10-10.md).
The [durable disposition](https://github.com/egohygiene/identity/pull/92#issuecomment-6099135806) records
that approval on 2026-10-10. The original reconstruction text and evidence
remain intact; implementation stays `implemented`, with no new runtime,
release, creative-asset, account or deployment verification inferred.
