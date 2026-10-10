# Architecture decisions

This is Identity's canonical human index. Markdown records own the rationale;
derived views do not grant decision authority. The
[policy reference](policy-reference.json) selects Hygiene ADR policy v1.1.0.

Maintainer `szmyty` explicitly retained ADR-001–018 with the approved R1
clarifications and separately accepted ADR-019–021 on 2026-10-10. The
[human disposition record](../decision-ratification-2026-10-10.md) links the
exact reviewed packet and durable approval. All records now use canonical
metadata and anatomy; source validation and publication remain separately
evidenced. Implementation states remain in each record and do not follow
from acceptance alone. ADR-022 separately proposes the consumer publication
composition and has no lifecycle approval; the corpus contains 21 accepted
records and one proposed record.

| ID | Title | Decision status | Date | Canonical record |
| --- | --- | --- | --- | --- |
| ADR-001 | Keep creative approval human-owned | accepted | 2026-10-10 | [ADR-001](ADR-001-creative-approval-human-owned.md) |
| ADR-002 | Store consumer assets beneath a stable identity contract | accepted | 2026-10-10 | [ADR-002](ADR-002-stable-identity-contract.md) |
| ADR-003 | Separate deterministic projection from generative creation | accepted | 2026-10-10 | [ADR-003](ADR-003-deterministic-projection-boundary.md) |
| ADR-004 | Use DTCG 2025.10 as the token contract | accepted | 2026-10-10 | [ADR-004](ADR-004-dtcg-token-contract.md) |
| ADR-005 | Publish curated JSON Schemas and validate them offline | accepted | 2026-10-10 | [ADR-005](ADR-005-json-schema-contract.md) |
| ADR-006 | Use a pinned Rust vector and raster stack | accepted | 2026-10-10 | [ADR-006](ADR-006-rust-rendering-stack.md) |
| ADR-007 | Separate font inspection, rendering, subsetting, and approval | accepted | 2026-10-10 | [ADR-007](ADR-007-font-tooling-boundaries.md) |
| ADR-008 | Encode platform metadata as versioned first-party profiles | accepted | 2026-10-10 | [ADR-008](ADR-008-platform-profile-contracts.md) |
| ADR-009 | Keep Storybook at the consumer integration boundary | accepted | 2026-10-10 | [ADR-009](ADR-009-storybook-consumer-adapter.md) |
| ADR-010 | Render from a framework-neutral immutable view model | accepted | 2026-10-10 | [ADR-010](ADR-010-reference-renderer-boundary.md) |
| ADR-011 | Layer normative, exact, browser, and human quality evidence | accepted | 2026-10-10 | [ADR-011](ADR-011-accessibility-and-visual-evidence.md) |
| ADR-012 | Use local, layered Identity v1 source contracts | accepted | 2026-10-10 | [ADR-012](ADR-012-local-layered-identity-v1.md) |
| ADR-013 | Preserve guidance lifecycle state in every projection | accepted | 2026-10-10 | [ADR-013](ADR-013-preserve-guidance-lifecycle.md) |
| ADR-014 | Keep design-system handbooks as governed projections | accepted | 2026-10-10 | [ADR-014](ADR-014-design-system-projection-boundary.md) |
| ADR-015 | Keep Press Kits as governed public projections | accepted | 2026-10-10 | [ADR-015](ADR-015-press-kit-projection-boundary.md) |
| ADR-016 | Project social surfaces from pinned external facts | accepted | 2026-10-10 | [ADR-016](ADR-016-pinned-social-surface-projection-boundary.md) |
| ADR-017 | Compose Identity's dogfood experience without moving brand authority | accepted | 2026-10-10 | [ADR-017](ADR-017-zensical-launchkit-publication-architecture.md) |
| ADR-018 | Project repository presentation without evaluating repository truth | accepted | 2026-10-10 | [ADR-018](ADR-018-repository-presentation-projection-boundary.md) |
| ADR-019 | Preserve an independent immutable Identity release contract | accepted | 2026-10-10 | [ADR-019](ADR-019-immutable-release-contract.md) |
| ADR-020 | Separate channel governance, account lifecycle, and verification | accepted | 2026-10-10 | [ADR-020](ADR-020-channel-registry-governance.md) |
| ADR-021 | Keep mascot source and approved derivatives behind a governed package | accepted | 2026-10-10 | [ADR-021](ADR-021-governed-mascot-package.md) |
| ADR-022 | Compose current Decisions evidence beneath the existing Brand Kit publisher | proposed | 2026-10-10 | [ADR-022](ADR-022-decisions-publication-composition.md) |

## Ongoing capture

Use the pinned authoring guidance in [AGENTS.md](../../AGENTS.md) before
implementation and at PR handoff. Consult existing records first, keep new
records proposed, and cite the decision-impact result in the PR template.
See [validation and upgrade commands](../decision-validation.md).

The index dates identify the current 2026-10-10 disposition for migrated legacy
records, the reconstruction date for ADR-019–021 and the proposal date for
ADR-022. Original declared dates,
status claims and substantive prose remain preserved in each record with
immutable source provenance. Approval uses its actual current date; no historical
approval is inferred. No ID, filename or compatibility anchor was changed.
