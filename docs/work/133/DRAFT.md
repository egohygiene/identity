# Explicit v1 initializer draft

Base: `19d3d16bd149ddb61a03924a2b688e8e689af68b`.
Review: [draft PR138](https://github.com/egohygiene/identity/pull/138).
Decision: proposed [ADR-0033](../../decisions/ADR-0033-explicit-v1-initialization-candidates.md).
Interface: [v1 initialization](../../consumers/V1_INITIALIZATION.md).

## Criterion disposition

| #133 criterion | Draft source | Acceptance |
| --- | --- | --- |
| Explicit v1 invocation; preserve v0 | Separate `v1-init`; old command implementations unchanged | V0 parity and invocation regressions unrun |
| Supplied facts/profiles/defaults/reviewed source | Closed local request; computed layer pins; exclusive validated-source import | Positive/invalid/unsupported input matrix unrun |
| Reviewable candidate and missing facts | New standalone root and report; empty human-evidence arrays and no invented claims | Missing-fact and completed-real-source cases unrun |
| Paths, preservation and authority | Portable paths, link/reparse rejection, disjoint inputs, new destination; manual promotion | Conflict/repeat/failure and supported-platform cases unrun |
| Compatibility and setup separation | Actual script fingerprints, source/profile versions, embedded isolated stdlib runtime | Copied-binary/offline/runtime compatibility proof unrun |
| Full required scenario matrix | Recorded in the guide for the later campaign | Unrun; issue remains open |
| Manual fallback and owner handoffs | Same-source standalone command, worksheet, explicit review/adoption and owner references | Documentation/runtime qualification unrun |

## Limited evidence actually collected

- `python3` AST parsing of `scripts/initialize_identity.py`: passed.
- Standard JSON parsing of both new schemas and request examples: passed.
- `rustfmt --edition 2024 src/v1_initializer.rs src/cli.rs`: applied to the bounded new interface.
- `bash scripts/dev-env.sh exec cargo build --locked --offline`: passed after the initializer source changes.
- `git diff --check`: passed before the source checkpoint.
- All 40 original roadmap machine blocks are byte-identical to the base;
  approved screenshot SHA-256 remains
  `53d7d144734ac63ceb730e95c7a39acc47d3fa64c5429f752233978289088543`.
- CLI/lib extraction-evolution entries retain original baseline hashes and
  append #133 rationale/current file hashes. No runtime provenance-suite pass
  is inferred from updating that inventory.

Syntax/build results do not execute the initializer or its preservation cases.
No unit/integration/regression suite, Clippy, native platform/browser/AX check,
full owner validation or hosted CI ran. Bootstrap evidence applies to its named
base, not to this candidate. No issue closure, merge, approval, release,
deployment or real consumer adoption is supplied by this draft.

## Next work

Keep this source reviewable and preserve the deferred matrix. Prepare #98's
actual source/rights and native publisher draft independently of creative
approval. The later qualification campaign must exercise the seven original
criteria against its exact resulting source, repair failures and retain actual
platform/review/CI gaps before #133 can close.
