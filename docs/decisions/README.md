# Architecture decisions

This is Identity's canonical human index. Markdown records own the rationale;
derived views do not grant decision authority. The
[policy reference](policy-reference.json) selects Hygiene ADR policy v1.1.0.

Adoption is **legacy and incomplete**. ADR-001–018 preserve historical accepted
claims whose human disposition is unresolved. That index annotation is not a
new lifecycle status. ADR-019–021 are new proposed historical reconstructions;
implementation evidence does not make them accepted. See the
[migration and disposition packet](../decision-migration-2026-10-10.md).

| ID | Title | Decision status | Date | Canonical record |
| --- | --- | --- | --- | --- |
| ADR-001 | Keep creative approval human-owned | Legacy accepted claim; unresolved | 2026-08-19 | [ADR-001](ADR-001-creative-approval-human-owned.md) |
| ADR-002 | Store consumer assets beneath a stable identity contract | Legacy accepted claim; unresolved | 2026-08-19 | [ADR-002](ADR-002-stable-identity-contract.md) |
| ADR-003 | Separate deterministic projection from generative creation | Legacy accepted claim; unresolved | 2026-08-19 | [ADR-003](ADR-003-deterministic-projection-boundary.md) |
| ADR-004 | Use DTCG 2025.10 as the token contract | Legacy accepted claim; unresolved | 2026-08-20 | [ADR-004](ADR-004-dtcg-token-contract.md) |
| ADR-005 | Publish curated JSON Schemas and validate them offline | Legacy accepted claim; unresolved | 2026-08-20 | [ADR-005](ADR-005-json-schema-contract.md) |
| ADR-006 | Use a pinned Rust vector and raster stack | Legacy accepted claim; unresolved | 2026-08-20 | [ADR-006](ADR-006-rust-rendering-stack.md) |
| ADR-007 | Separate font inspection, rendering, subsetting, and approval | Legacy accepted claim; unresolved | 2026-08-20 | [ADR-007](ADR-007-font-tooling-boundaries.md) |
| ADR-008 | Encode platform metadata as versioned first-party profiles | Legacy accepted claim; unresolved | 2026-08-20 | [ADR-008](ADR-008-platform-profile-contracts.md) |
| ADR-009 | Keep Storybook at the consumer integration boundary | Legacy accepted claim; unresolved | 2026-08-20 | [ADR-009](ADR-009-storybook-consumer-adapter.md) |
| ADR-010 | Render from a framework-neutral immutable view model | Legacy accepted claim; unresolved | 2026-08-20 | [ADR-010](ADR-010-reference-renderer-boundary.md) |
| ADR-011 | Layer normative, exact, browser, and human quality evidence | Legacy accepted claim; unresolved | 2026-08-20 | [ADR-011](ADR-011-accessibility-and-visual-evidence.md) |
| ADR-012 | Use local, layered Identity v1 source contracts | Legacy accepted claim; unresolved | 2026-08-21 | [ADR-012](ADR-012-local-layered-identity-v1.md) |
| ADR-013 | Preserve guidance lifecycle state in every projection | Legacy accepted claim; unresolved | 2026-08-21 | [ADR-013](ADR-013-preserve-guidance-lifecycle.md) |
| ADR-014 | Keep design-system handbooks as governed projections | Legacy accepted claim; unresolved | 2026-08-28 | [ADR-014](ADR-014-design-system-projection-boundary.md) |
| ADR-015 | Keep Press Kits as governed public projections | Legacy accepted claim; unresolved | 2026-08-28 | [ADR-015](ADR-015-press-kit-projection-boundary.md) |
| ADR-016 | Project social surfaces from pinned external facts | Legacy accepted claim; unresolved | 2026-08-29 | [ADR-016](ADR-016-pinned-social-surface-projection-boundary.md) |
| ADR-017 | Compose Identity's dogfood experience without moving brand authority | Legacy accepted claim; unresolved | 2026-08-30 | [ADR-017](ADR-017-zensical-launchkit-publication-architecture.md) |
| ADR-018 | Project repository presentation without evaluating repository truth | Legacy accepted claim; unresolved | 2026-08-30 | [ADR-018](ADR-018-repository-presentation-projection-boundary.md) |
| ADR-019 | Preserve an independent immutable Identity release contract | proposed | 2026-10-10 | [ADR-019](ADR-019-immutable-release-contract.md) |
| ADR-020 | Separate channel governance, account lifecycle, and verification | proposed | 2026-10-10 | [ADR-020](ADR-020-channel-registry-governance.md) |
| ADR-021 | Keep mascot source and approved derivatives behind a governed package | proposed | 2026-10-10 | [ADR-021](ADR-021-governed-mascot-package.md) |

## Ongoing capture

Use the pinned authoring guidance in [AGENTS.md](../../AGENTS.md) before
implementation and at PR handoff. Consult existing records first, keep new
records proposed, and cite the decision-impact result in the PR template.
See [validation and upgrade commands](../decision-validation.md).

The dates in legacy rows are the dates declared by their original records;
they are not new approval dates. New reconstruction dates are distinguished
from historical evidence in each proposed ADR. No IDs or filename widths were
changed, reused or aliased to a different decision.
