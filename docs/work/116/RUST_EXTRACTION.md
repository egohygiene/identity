# Rust responsibility extraction — #87

Base: `e4ec2847e1a7be70f22e6dd33267498cfbfe19a0`.
Forty existing function bodies move into eight private modules:

| Parent | Private responsibilities |
| --- | --- |
| `src/compiler/mod.rs` | `validation.rs`: request/adapter/source checks; `planning.rs`: manifest loading, deterministic planning, fingerprints and manifest construction |
| `src/quality/mod.rs` | `source.rs`: source provenance/rights/approval/SVG checks; `artifacts.rs`: artifact hashes, dimensions, budgets and visual evidence; `tokens.rs`: contrast and duration checks |
| `src/motion/mod.rs` | `provenance.rs`: source/capture evidence; `behavior.rs`: motion/reduced-motion/fallback behavior; `artifacts.rs`: output/baseline checks |

Public types, traits, paths and orchestration remain in their original parent
modules. Child functions use explicit imports and parent-only visibility.
Filesystem transaction/lock/recovery implementation and its guarantees are
unchanged. No dependency, schema, diagnostic text, approval rule or baseline
is changed.

[rust-extraction.json](rust-extraction.json) records every original function
body hash and destination. All forty bodies match exactly after rustfmt.
The parent modules shrink from 1537/1451/1063 lines to 890/884/551 lines.

## Actual local validation — 2026-11-14

- `cargo fmt --all --check` and Clippy with all targets/features and denied
  warnings pass.
- `cargo test --locked --all-features`: 118 pass, three explicit helper-only
  ignores. Approval, drift, adapters, deterministic/incremental generation,
  confinement, native writer serialization, process interruption/recovery,
  embedded validator, motion and renderer-contract cases remain covered.
- The pre-extraction and rebuilt binaries each generate and verify all three
  minimal/expanded fixture/example roots. Each produces the same fourteen
  generated files byte for byte, and every input byte is preserved.
- The extraction/provenance validator passes. The original approved screenshot
  is unchanged; no new visual or native-platform qualification is claimed.

ADR not required: private, behavior-preserving extraction behind the existing
compiler, quality and motion interfaces. The broader #70 audit and `act`
campaign remain separate.
