# Architecture decisions

This is Identity's canonical human index. Markdown records own the rationale;
derived views do not grant decision authority. The
[policy reference](policy-reference.json) selects Hygiene ADR policy v1.2.0.

Maintainer `szmyty` explicitly retained ADR-0001–018 with the approved R1
clarifications and separately accepted ADR-0019–021 on 2026-10-10. The
[human disposition record](../decision-ratification-2026-10-10.md) links the
exact reviewed packet and durable approval. All records now use canonical
metadata and anatomy; source validation and publication remain separately
evidenced. Implementation states remain in each record and do not follow
from acceptance alone. ADR-0022 separately proposes the consumer publication
composition. ADR-0023 proposes the shared source-digest compatibility contract.
ADR-0024 proposes the renderer artifact-path compatibility rules. ADR-0025
proposes the executable minimal authoring core and nullable-guidance behavior.
ADR-0026 proposes repository-wide native writer serialization and its persistent
coordination file. These five proposals have no lifecycle approval; the corpus
contains 21 accepted records and five proposed records.

| ID | Title | Decision status | Date | Canonical record |
| --- | --- | --- | --- | --- |
| ADR-0001 | Keep creative approval human-owned | accepted | 2026-10-10 | [ADR-0001](ADR-0001-creative-approval-human-owned.md) |
| ADR-0002 | Store consumer assets beneath a stable identity contract | accepted | 2026-10-10 | [ADR-0002](ADR-0002-stable-identity-contract.md) |
| ADR-0003 | Separate deterministic projection from generative creation | accepted | 2026-10-10 | [ADR-0003](ADR-0003-deterministic-projection-boundary.md) |
| ADR-0004 | Use DTCG 2025.10 as the token contract | accepted | 2026-10-10 | [ADR-0004](ADR-0004-dtcg-token-contract.md) |
| ADR-0005 | Publish curated JSON Schemas and validate them offline | accepted | 2026-10-10 | [ADR-0005](ADR-0005-json-schema-contract.md) |
| ADR-0006 | Use a pinned Rust vector and raster stack | accepted | 2026-10-10 | [ADR-0006](ADR-0006-rust-rendering-stack.md) |
| ADR-0007 | Separate font inspection, rendering, subsetting, and approval | accepted | 2026-10-10 | [ADR-0007](ADR-0007-font-tooling-boundaries.md) |
| ADR-0008 | Encode platform metadata as versioned first-party profiles | accepted | 2026-10-10 | [ADR-0008](ADR-0008-platform-profile-contracts.md) |
| ADR-0009 | Keep Storybook at the consumer integration boundary | accepted | 2026-10-10 | [ADR-0009](ADR-0009-storybook-consumer-adapter.md) |
| ADR-0010 | Render from a framework-neutral immutable view model | accepted | 2026-10-10 | [ADR-0010](ADR-0010-reference-renderer-boundary.md) |
| ADR-0011 | Layer normative, exact, browser, and human quality evidence | accepted | 2026-10-10 | [ADR-0011](ADR-0011-accessibility-and-visual-evidence.md) |
| ADR-0012 | Use local, layered Identity v1 source contracts | accepted | 2026-10-10 | [ADR-0012](ADR-0012-local-layered-identity-v1.md) |
| ADR-0013 | Preserve guidance lifecycle state in every projection | accepted | 2026-10-10 | [ADR-0013](ADR-0013-preserve-guidance-lifecycle.md) |
| ADR-0014 | Keep design-system handbooks as governed projections | accepted | 2026-10-10 | [ADR-0014](ADR-0014-design-system-projection-boundary.md) |
| ADR-0015 | Keep Press Kits as governed public projections | accepted | 2026-10-10 | [ADR-0015](ADR-0015-press-kit-projection-boundary.md) |
| ADR-0016 | Project social surfaces from pinned external facts | accepted | 2026-10-10 | [ADR-0016](ADR-0016-pinned-social-surface-projection-boundary.md) |
| ADR-0017 | Compose Identity's dogfood experience without moving brand authority | accepted | 2026-10-10 | [ADR-0017](ADR-0017-zensical-launchkit-publication-architecture.md) |
| ADR-0018 | Project repository presentation without evaluating repository truth | accepted | 2026-10-10 | [ADR-0018](ADR-0018-repository-presentation-projection-boundary.md) |
| ADR-0019 | Preserve an independent immutable Identity release contract | accepted | 2026-10-10 | [ADR-0019](ADR-0019-immutable-release-contract.md) |
| ADR-0020 | Separate channel governance, account lifecycle, and verification | accepted | 2026-10-10 | [ADR-0020](ADR-0020-channel-registry-governance.md) |
| ADR-0021 | Keep mascot source and approved derivatives behind a governed package | accepted | 2026-10-10 | [ADR-0021](ADR-0021-governed-mascot-package.md) |
| ADR-0022 | Compose current Decisions evidence beneath the existing Brand Kit publisher | proposed | 2026-10-10 | [ADR-0022](ADR-0022-decisions-publication-composition.md) |
| ADR-0023 | Preserve and specify a shared canonical source digest | proposed | 2026-10-18 | [ADR-0023](ADR-0023-canonical-source-digest.md) |
| ADR-0024 | Separate bundle-relative artifact paths from deployment bases | proposed | 2026-10-18 | [ADR-0024](ADR-0024-renderer-artifact-paths.md) |
| ADR-0025 | Keep the executable authoring core independent of optional guidance | proposed | 2026-10-19 | [ADR-0025](ADR-0025-executable-minimal-authoring-core.md) |
| ADR-0026 | Serialize local generation and recovery with one persistent native lock | proposed | 2026-10-19 | [ADR-0026](ADR-0026-local-writer-serialization.md) |

## Ongoing capture

Use the pinned authoring guidance in [AGENTS.md](../../AGENTS.md) before
implementation and at PR handoff. Consult existing records first, keep new
records proposed, and cite the decision-impact result in the PR template.
See [validation and upgrade commands](../decision-validation.md).

The index dates identify the current 2026-10-10 disposition for migrated legacy
records, the reconstruction date for ADR-0019–021 and the proposal date for
ADR-0022; ADR-0023/024 use their actual 2026-10-18 proposal date and ADR-0025 its
2026-10-19 proposal date; ADR-0026 also uses its actual 2026-10-19 proposal date. Original declared dates,
status claims and substantive prose remain preserved in each record with
immutable source provenance. Approval uses its actual current date; no historical
approval is inferred. No ID, filename or compatibility anchor was changed.
