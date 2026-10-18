# Four-digit identifier migration — 2026-10-18

The maintainer selected four digits and authorized padding existing records, documenting each change and merging tested migrations. [Hygiene #73](https://github.com/egohygiene/hygiene/issues/73) tracks the shared process; policy v1.2.0 is pinned at `a05b14f8b9e2772124f879f818e09a911e996ad8`. Source inventory: `063a4c70fcaccc6c15393f28ac2aabe62b34e1e7`.

Twenty-four canonical records retain their logical numbers, rationale, dates, implementation evidence, lifecycle and human approval. Twenty-one remain accepted and three remain proposed. Historical Git messages, immutable source URLs, dated ratification/evidence and rollback bytes stay preserved. Current index, metadata, lineage, filename and references update together. No redirect framework is added.

| Previous ID | Current ID | Previous path | Current path |
| --- | --- | --- | --- |
| `ADR-001` | `ADR-0001` | `docs/decisions/ADR-001-creative-approval-human-owned.md` | `docs/decisions/ADR-0001-creative-approval-human-owned.md` |
| `ADR-002` | `ADR-0002` | `docs/decisions/ADR-002-stable-identity-contract.md` | `docs/decisions/ADR-0002-stable-identity-contract.md` |
| `ADR-003` | `ADR-0003` | `docs/decisions/ADR-003-deterministic-projection-boundary.md` | `docs/decisions/ADR-0003-deterministic-projection-boundary.md` |
| `ADR-004` | `ADR-0004` | `docs/decisions/ADR-004-dtcg-token-contract.md` | `docs/decisions/ADR-0004-dtcg-token-contract.md` |
| `ADR-005` | `ADR-0005` | `docs/decisions/ADR-005-json-schema-contract.md` | `docs/decisions/ADR-0005-json-schema-contract.md` |
| `ADR-006` | `ADR-0006` | `docs/decisions/ADR-006-rust-rendering-stack.md` | `docs/decisions/ADR-0006-rust-rendering-stack.md` |
| `ADR-007` | `ADR-0007` | `docs/decisions/ADR-007-font-tooling-boundaries.md` | `docs/decisions/ADR-0007-font-tooling-boundaries.md` |
| `ADR-008` | `ADR-0008` | `docs/decisions/ADR-008-platform-profile-contracts.md` | `docs/decisions/ADR-0008-platform-profile-contracts.md` |
| `ADR-009` | `ADR-0009` | `docs/decisions/ADR-009-storybook-consumer-adapter.md` | `docs/decisions/ADR-0009-storybook-consumer-adapter.md` |
| `ADR-010` | `ADR-0010` | `docs/decisions/ADR-010-reference-renderer-boundary.md` | `docs/decisions/ADR-0010-reference-renderer-boundary.md` |
| `ADR-011` | `ADR-0011` | `docs/decisions/ADR-011-accessibility-and-visual-evidence.md` | `docs/decisions/ADR-0011-accessibility-and-visual-evidence.md` |
| `ADR-012` | `ADR-0012` | `docs/decisions/ADR-012-local-layered-identity-v1.md` | `docs/decisions/ADR-0012-local-layered-identity-v1.md` |
| `ADR-013` | `ADR-0013` | `docs/decisions/ADR-013-preserve-guidance-lifecycle.md` | `docs/decisions/ADR-0013-preserve-guidance-lifecycle.md` |
| `ADR-014` | `ADR-0014` | `docs/decisions/ADR-014-design-system-projection-boundary.md` | `docs/decisions/ADR-0014-design-system-projection-boundary.md` |
| `ADR-015` | `ADR-0015` | `docs/decisions/ADR-015-press-kit-projection-boundary.md` | `docs/decisions/ADR-0015-press-kit-projection-boundary.md` |
| `ADR-016` | `ADR-0016` | `docs/decisions/ADR-016-pinned-social-surface-projection-boundary.md` | `docs/decisions/ADR-0016-pinned-social-surface-projection-boundary.md` |
| `ADR-017` | `ADR-0017` | `docs/decisions/ADR-017-zensical-launchkit-publication-architecture.md` | `docs/decisions/ADR-0017-zensical-launchkit-publication-architecture.md` |
| `ADR-018` | `ADR-0018` | `docs/decisions/ADR-018-repository-presentation-projection-boundary.md` | `docs/decisions/ADR-0018-repository-presentation-projection-boundary.md` |
| `ADR-019` | `ADR-0019` | `docs/decisions/ADR-019-immutable-release-contract.md` | `docs/decisions/ADR-0019-immutable-release-contract.md` |
| `ADR-020` | `ADR-0020` | `docs/decisions/ADR-020-channel-registry-governance.md` | `docs/decisions/ADR-0020-channel-registry-governance.md` |
| `ADR-021` | `ADR-0021` | `docs/decisions/ADR-021-governed-mascot-package.md` | `docs/decisions/ADR-0021-governed-mascot-package.md` |
| `ADR-022` | `ADR-0022` | `docs/decisions/ADR-022-decisions-publication-composition.md` | `docs/decisions/ADR-0022-decisions-publication-composition.md` |
| `ADR-023` | `ADR-0023` | `docs/decisions/ADR-023-canonical-source-digest.md` | `docs/decisions/ADR-0023-canonical-source-digest.md` |
| `ADR-024` | `ADR-0024` | `docs/decisions/ADR-024-renderer-artifact-paths.md` | `docs/decisions/ADR-0024-renderer-artifact-paths.md` |

The separate inline DECISIONS.md sequence has its own map in that file. Identity #114 remains an independent field-audit draft; preserve its evidence and reconcile current ID references against this map without changing audit findings. Naming authorization does not ratify proposals or complete publication.

The reviewed identity-experience content and visual baseline remain byte-preserved for the independent #114 audit. Historical Markdown notes retain their original IDs and prose; links to renamed files are bound to the exact pre-migration source revision instead of becoming broken current paths.
