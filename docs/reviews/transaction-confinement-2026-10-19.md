# Transaction-path confinement review

Issue [#78](https://github.com/egohygiene/identity/issues/78) starts from
`8816294e9d9c43f250d771e9fa627c4b1861e78a`, after #99 completed through PR #118.
The [runtime receipt](../evidence/identity-transaction-confinement-2026-10-19.json)
records exact binary/source hashes, observations and limits.

## Baseline observations

The 2026-10-03 audit inferred a cache-redirection risk. The current baseline
already includes #73's path and recovery preflight guards. A freshly built
baseline CLI ran against disposable copies of the existing complete v1 fixture:

| Pre-planted Unix redirect | Exit / diagnostic | Consumer and external trees |
| --- | --- | --- |
| `.cache` | 1 / IDN2311 | Unchanged |
| `.cache/identity` | 1 / IDN2311 | Unchanged |
| `.cache/identity/transactions` | 1 / IDN2311 | Unchanged |
| Existing plan workspace | 1 / IDN2301 | Unchanged |

This does not establish a current redirected-write exploit under serialized
use. A timing probe made ten attempts without achieving its injection; it is
inconclusive and supplies no concurrency-safety result. No confirmed corruption
or deployed exposure is inferred. Windows behavior was not executed locally.

## Bounded enforcement

The [compiler contract](../contracts/COMPILER_V1.md#supported-local-cache-paths)
keeps the existing fixed repository-local cache. There is no external cache
option or implicit fallback. Symlinks, Windows junctions and other reparse
points are unsupported along generated-state paths.

`src/compiler/filesystem.rs` now checks transaction operations individually:

- Inspect every existing component and propagate inspection failures; require
  regular files/directories and lossless portable paths.
- Constrain transaction helpers to the actual transaction root and promotion
  to the independently authorized output root.
- Reserve a fresh plan directory and create staging, backup and pending-journal
  leaves with `create_new`, preserving existing files and hard-linked aliases.
- Recheck journal publication, recovery temporary files, promotion and cleanup.
  Recovery retains full-batch preflight and unlinks its temporary name before
  creating a fresh file, preserving legitimate recovery retries.

The journal remains v2. No source, approval, profile, release or output-byte
contract changes. These are pathname checks under serialized local use; they
do not prevent another process replacing a directory between inspection and
use. Per-consumer writer serialization remains #79.

## Validation

The Linux filesystem suite passes 23 tests, including every cache component,
staging/backup ancestors and leaves, pending/journal collisions, hard links,
special entries, nonmutating inspection, all interrupted-recovery points and
successful repeated/custom-root recovery. Windows-specific tests exercise
junctions at cache, workspace, staging and backup directories; their execution
belongs to hosted Windows evidence in the PR.

All 84 local Rust tests pass with all features. All 138 Python cases complete
with 136 passes and two existing skips. Formatting, strict all-target Clippy and
six repository integrity verifiers pass. Independent fresh CLI generation with
the baseline and candidate binaries produces the same 14 generated files,
including the hidden manifest; both verify successfully and preserve canonical
fixture bytes. Skips and pending platform execution are not counted as passes.

```bash
cargo test --locked --lib compiler::filesystem::tests
cargo test --locked --all-features
cargo fmt --all --check
cargo clippy --locked --all-targets --all-features -- --deny warnings
python3 -m unittest discover --start-directory "tests" --pattern "test_*.py" --verbose
```

Decision impact: reference ADR-0012 and ADR-0019. This localized enforcement of
the existing local-source/output and no-link contracts needs no new ADR; it
does not introduce another cache system or concurrency authority. All existing
ADR dispositions remain unchanged.
