---
schema: egohygiene.architecture-decision/v1
id: ADR-0035
title: Scope Identity logo reuse to truthful identification and distinct derivatives
status: proposed
date: "2026-11-22"
decision_scope: repository
visibility: public
owners: [egohygiene/identity]
issue: https://github.com/egohygiene/identity/issues/98
pull_request: null
related: [ADR-0001, ADR-0003, ADR-0007, ADR-0012, ADR-0021, ADR-0028]
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/identity]
affected_contracts: []
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/identity/issues/98
    description: Existing owner intake tracks selected logo masters, actual provenance, reuse policy, credit and the separate self-source/release/adoption gates.
  - type: documentation
    url: https://github.com/egohygiene/identity/blob/b687df51649226882f2b218178c7b10933f48a74/mascot/LICENSE.md
    description: Kern already has an independent CC-BY-4.0 grant and attribution; that permission does not establish the logo masters' license.
approval: null
exceptions: []
---

# ADR-0035: Scope Identity logo reuse to truthful identification and distinct derivatives

## Context

The #98 owner intake selected the existing emblem and horizontal logo masters
and reports ChatGPT-assisted creation under maintainer guidance. Other brand
kits were consulted mainly for dimensions and coverage; exact external source
and generation records remain unidentified. Those facts do not establish
exclusive copyright, third-party permissions or a registered trademark.

The owner selected a policy allowing truthful display and integration of
Identity, including bundled font icons, while preventing the unchanged or
confusingly similar branding from becoming another tool's own identity.
Genuinely distinct derivatives may represent another project under a different
name. The selected credit is **Ego Hygiene — Identity**.

Policy selection is distinct from this architecture record's lifecycle. The
[owner-answer record](../work/98/OWNER_ANSWERS_2026-11-22.md) records the actual
answers; this new ADR remains proposed with null approval. Prior source-asset,
mascot and architecture decisions keep their own evidence and disposition.

## Decision

Propose the scoped
[Identity logo use permission](../../assets/identity/brand/LOGO_USE.md), identified
as `LicenseRef-EgoHygiene-Identity-Logo-Use-1.0`, for the two byte-bound masters
and faithful logo/icon adaptations traceable to them.

Permit copying, distribution, format and glyph conversion, monochrome and
similar presentation adaptations when identifying the actual Identity tool,
including commercial integrations. Permit genuinely distinct renamed
derivatives without a misleading claim of affiliation. Preserve the selected
credit in a sensible package notice instead of requiring it beside every icon.

Do not silently adopt a broad standard artwork license and then append
incompatible copyright restrictions. Keep this scoped permission separate from
software licensing, Kern's existing CC-BY-4.0 grant, external font terms and
brand/nonendorsement guidance. Do not claim trademark registration, universal
font-pack compatibility or permissions the project does not hold.

## Alternatives considered and rejected

- A plain CC-BY-4.0 or CC0 artwork grant would not itself express the selected
  restriction on unrelated-product branding. Adding that copyright restriction
  while presenting the result as ordinary CC-BY would misstate its terms.
- Brand/trademark guidance alone would not clearly grant the requested copying,
  glyph conversion and redistribution rights or establish any unproven rights.
- Withholding all reuse would conflict with the selected reference,
  integration and font-icon uses.
- Treating a minor recolor or format conversion as a new product identity would
  not preserve the selected distinction between useful adaptation and confusing
  reuse of the existing mark.

These alternatives describe this proposal's design tradeoffs, not a fabricated
historical legal review or a claim that the owner selected an unmentioned
standard license.

## Consequences and tradeoffs

The covered artwork has an explicit permission and credit while the source
facts and creative selection remain separately inspectable. Consumers can
redistribute integration icons under the recorded conditions; a font/package
integrator still has to check its receiving license and must not assume the
scoped permission is an unrestricted open-font license.

The genuine-distinction/nonconfusion boundary needs human judgment. It is not
proved by a pixel threshold, an automated check, a new filename or omission of
the product name. The policy makes no blanket copyright claim about AI output
and no guarantee of trademark registration or enforceability. Missing external
provenance remains visible instead of being filled with plausible facts.

## Implementation and evidence links

This candidate authors the policy and records it alongside the
[owner-answer intake](../work/98/OWNER_ANSWERS_2026-11-22.md). Exact master hashes
appear in the policy and existing candidate inventory. The old masters, prior
ADRs, software license and Kern license are preserved.

Document/schema/link validation is narrower than legal review, real v1 source
acceptance, packaging or publication. Record actual checks and later integration
under #98 and CONTINUITY.md. No architecture acceptance, new release or live
distribution is established by this draft.

## Replacement or exit strategy

Preserve this dated policy/version and the terms accompanying existing
distributed copies. Review future license expansion, replacement, special
permissions and affected package compatibility as an explicit change. Do not
rewrite historical asset/approval records or assume a new policy silently
relicenses third-party material or earlier immutable releases.

## Follow-up work

Keep actual provenance gaps, covered source hashes, selected credit and
same-subject creative approval evidence together during #98's real self-source
and package preparation. Check each selected distribution's attribution and
license compatibility. Preserve Kern's separate license and any third-party
font/material notices. #70 retains engineering qualification; #98 retains real
release, publication/rollback and consumer proof. Formal human disposition of
this ADR is a separate step.
