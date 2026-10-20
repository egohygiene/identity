# Identity compiler v1 contract

## Purpose

The compiler core is the framework-neutral execution boundary behind the Brand Kit generator. It owns deterministic orchestration and mutation authority; concrete token, vector, raster, font, metadata, archive, and publication behavior lives behind replaceable adapters.

The v1 application flow is:

```text
read → validate → resolve → plan → render → verify → manifest
                                      │
                                      └─ apply only after explicit approval
```

`init`, `validate`, `plan`, and `handoff` remain the existing v0 CLI surface.
The v1 consumer boundary includes `v1-generate` and `v1-verify`: the former uses
the published source adapter and selected versioned profiles to apply one
transactional package build, while the latter is read-only and fails on missing
or drifted generated state. Both commands and `V1ConsumerPipeline::load` invoke
the embedded copy of `scripts/validate_identity.py`, preserving its diagnostic
codes, paths, messages, and recovery guidance. Python 3.11+ is required at runtime
(`python3` on Unix, `python` on Windows, or the executable in `IDENTITY_PYTHON`).
Isolated mode disables consumer imports and site packages; the executable needs
neither a source checkout nor network access. There is no unchecked fallback.

`v1-inspect` and `v1-recover` use the artifact store directly with the same
`--repository-root` and `--output-root` scope. They require neither canonical
source nor Python, so source damage cannot prevent interruption diagnosis or
validated rollback. They provide human output, with nonzero failures retaining
the existing diagnostic codes and recovery guidance; no new JSON report is
introduced. Use a reviewed source/release containing these commands.

Source preflight and producer capability are separate: a governed PNG/font can
be valid canonical input while unsupported by the SVG-only Rust source bridge.
The bridge checks every provenance asset and reports `IDN3304` with failure state
`unsupported` before UTF-8 decoding unsupported formats. Non-UTF-8 bytes at an
`.svg` path remain invalid producer input (`IDN3301`), even if their governed
bytes pass format-agnostic source validation. See the [capability table](IDENTITY_V1.md#source-authority-and-producer-capabilities).
Independently null voice/usage declarations use the existing optional guidance
model; selected outputs remain subject to their actual profile prerequisites.

Preflight snapshots all consulted files and declared directories, including
inputs outside `.identity/`. The pipeline rejects stale bytes, replaced paths,
and mismatched intents at its reader, validator, and resolver boundaries. The
compiler rechecks source after planning, before rendering, and immediately before
commit. Reusing a prepared compilation after changing source requires a fresh
load and plan. These checks detect drift; exclusive writer serialization is a
separate concern.

The [canonical source digest contract](SOURCE_DIGEST_V1.md) specifies the common
Rust/Python inventory and preserves historical Rust/Unix byte framing and
component ordering. It documents the legacy Python and Windows compatibility
transition without rewriting published release bindings.

## Core ownership

The compiler core owns:

- pure intent, resolved-identity, target, plan, diagnostic, evidence, and manifest models;
- ordered stage orchestration through `IdentityReader`, `IdentityValidator`, and `IdentityResolver` ports;
- adapter discovery and compatibility checks;
- deterministic input fingerprints and plan digests;
- mutation-free planning of creates, replacements, removals, unchanged files, warnings, and approvals;
- render/verify isolation before generated state can change;
- a transactional artifact-store port and local filesystem implementation;
- recovery evidence for interrupted generated-state transactions.

The compiler core does not own:

- DTCG source semantics already governed by the v1 source contract;
- Style Dictionary, `resvg`, font tooling, or any other projection implementation;
- networked creative generation;
- package/profile contents owned by #11;
- publication authority owned by consumer repositories.

## Adapter SDK

`ProjectionAdapter` exposes four operations:

1. `descriptor` — stable id, version, kind, compiler API major, determinism/offline guarantees, and capabilities;
2. `plan` — target-specific warnings and required approvals without mutation;
3. `render` — bytes from an immutable `ResolvedIdentity` and `ProjectionTarget`;
4. `verify` — bounded diagnostics and evidence over rendered bytes.

The registry rejects duplicate or malformed adapter identities. Planning blocks adapters that:

- target another compiler API major;
- do not guarantee deterministic output; or
- require network access in the compiler-owned path.

Provider-backed creation therefore remains an explicit creative-handoff concern rather than a hidden render side effect.

## Plan contract

`identity.compiler-plan/v1` is defined by [`compiler-plan.schema.json`](../../contracts/v1/compiler-plan.schema.json). A plan records:

- canonical project and source digests;
- the complete requested output root and manifest path;
- one ordered action per selected or stale generated artifact;
- adapter compatibility and version evidence;
- current and previous checksums where available;
- deterministic input fingerprints;
- warnings and stable diagnostics; and
- every approval identifier required before apply.

Plans are read-only. Existing untracked files require `replace-unmanaged:<path>` approval. Drifted managed files require `replace-drifted:<path>`. Stale generated files require `remove:<path>` before deletion. An unsupported adapter produces a visible `blocked` action rather than partial success.

## Incremental rebuilds

Each target fingerprint hashes:

- the canonical source digest;
- the normalized target request; and
- the complete adapter descriptor.

A generated file is `unchanged` only when:

1. its current checksum still matches the previous manifest;
2. its previous input fingerprint matches the new fingerprint; and
3. its adapter version is unchanged.

Anything else is explicitly created, replaced, removed, blocked, or reported as drift. The compiler never infers success from file existence alone.

## Render and verification boundary

Execution refuses plans with blocking diagnostics or missing approvals. All create/replace targets render and verify before the artifact store receives mutation authority. A verification failure therefore leaves generated state untouched. If one transient in-memory render succeeds before another render/verify failure, the command reports `partial` coverage but still applies nothing.

Target byte budgets are enforced before transaction entry. Adapter evidence is included in the manifest and remains distinct from later #12 accessibility/visual release gates.

## Manifest contract

`identity.compiler-manifest/v1` is defined by [`compiler-manifest.schema.json`](../../contracts/v1/compiler-manifest.schema.json). It records:

- project/source/plan digests;
- every selected generated output;
- output checksum and byte size;
- target/profile/media type;
- adapter id/version and target input fingerprint;
- the exact adapter descriptors used; and
- deterministic verification evidence.

No timestamp, random id, absolute machine path, ambient environment value, or network result is included. The same normalized input, adapter/tool version, and target request therefore produce byte-stable structured output where the adapter format permits it.

## Transaction and recovery boundary

`LocalArtifactStore` keeps coordination and transient state under:

```text
.cache/identity/writer.lock
.cache/identity/transactions/<plan-digest>/
```

### Supported local cache paths

The cache root is fixed at `.cache/identity/transactions/` beneath the
canonicalized repository directory supplied by the caller. There is no separate
cache-root option or environment override. Externally located caches reached
through a symlink, Windows junction or another reparse point are unsupported;
use a real local directory tree. Selecting the repository itself through a
caller-supplied alias still resolves that repository before this boundary.

Every existing component must be inspectable and have the expected directory
or regular-file kind. Inspection failures are errors, not evidence of absence.
Generation checks cache/workspace paths, reserves a new plan directory and
creates staging, backup and pending-journal files without overwriting an
existing leaf. Each transaction operation rechecks its confined path; recovery
checks the complete retained tree before rollback or cleanup. Unsupported
preexisting cache-root or lock paths are rejected before creating coordination
metadata; deeper invalid transaction evidence is preserved as described below.
No fallback cache, automatic relocation, installation or journal migration is
performed.

These checks apply to cooperating local operations. They do not make pathname
checks atomic against another process replacing directory components between
inspection and use; protection against hostile concurrent filesystem mutation
is not claimed. Promotion still
requires filesystem rename support between staging and output; an unsupported
move retains transaction evidence for recovery.

### Exclusive writer ownership

Generation and recovery share a nonblocking native exclusive file lock on
`.cache/identity/writer.lock` beneath the canonical repository root. All output
roots share this ownership boundary. Mutation-free request/path validation precedes
acquisition; pending-workspace checks, current-checksum validation, staging,
backups, journal publication, output changes, verification and cleanup happen
while the guard is held. No-op commits and empty recovery acquire ownership too.

The coordination file is persistent and is not a transaction workspace. Its
presence is not proof of an active or stale owner. Create a missing regular file
exclusively; open an existing regular file without truncating or writing bytes.
Never unlink, replace or edit it to unblock a writer. Existing hard-linked
regular files retain their aliases and bytes; they may serialize multiple
repositories. Symlinks, Windows reparse points and special entries remain
unsupported. Lock and transaction-root paths are checked before any mkdir.

Contention fails as `blocked` / `IDN2346` without changing the active owner's
workspace, journal, backups or outputs. Wait for that process to finish, then
retry. Acquisition errors use `IDN2347`; unavailable native locking is
`unsupported`, with no unlocked fallback. The supported environment must
provide the native locking semantics used by Rust's `File::try_lock`.

Ordinary guard cleanup explicitly unlocks, then closes its handle. Process
termination closes its handles; ownership ends after all inherited or duplicated
handles are closed. The store does not clone its guard handle. There is
no PID/age heuristic, lock stealing or automatic workspace deletion. After an
interruption, the next owner still encounters pending transaction evidence and
must explicitly recover before generation. The empty coordination file and its
parents may newly exist after an empty recovery or a failure after acquisition;
this is the only added coordination metadata, not permission to alter rejected
transaction evidence or generated/canonical files.

Construction, reads, `recovery_required`, preparation and `v1-verify` do not
acquire this exclusive guard or create cache metadata. Their observations are
not consistent snapshots while a writer is active; commit rechecks its plan
under ownership. Cooperating writers must use this protocol. Do not run older
binaries or other uncoordinated writers concurrently, or manually change cache
state while any writer is active. Network filesystem qualification, hostile
filesystem mutation and power-loss durability are outside this contract.
See proposed [ADR-0026](../decisions/ADR-0026-local-writer-serialization.md).

### Read-only interruption inspection

`LocalArtifactStore::inspect_recovery` and `identity v1-inspect` create no files
or directories, write no bytes and clean no workspaces. An existing regular
coordination file is opened read-only and held with a nonblocking native shared
lock while inspecting. This excludes participating generation/recovery writers;
an active writer returns `IDN2346` without touching its evidence. Shared
inspection also temporarily excludes exclusive writers; wait and retry.

If the file is absent, inspection is explicitly an uncoordinated observation.
It checks again afterward and repeats full preflight under a shared guard if
the lock appeared. Remaining absence cannot guarantee future inactivity. Neither
inspection result nor plan digest grants later rollback authority.

Inspection and recovery reuse complete enumeration, journal/backup/destination
preflight and cross-transaction conflict detection. Inspection reports validated
workspace names, pending and empty-orphan counts, plan digests and proposed
restore/remove paths, without exposing backup bytes. Invalid, conflicting,
legacy or wrong-root evidence fails while preserving the entire tree, including
absence of coordination metadata. Valid pending state is a successful report.

Before publishing generated output, the store:

1. rechecks every planned current checksum to reject stale plans;
2. stages all verified writes;
3. backs up every replacement/removal and any existing manifest; and
4. writes a recovery journal.

Only then are staged files atomically promoted one path at a time. The manifest is promoted last and all manifested output checksums are re-read after apply.

A process interruption can leave the recovery journal behind. New plan/apply operations fail closed while any transaction workspace exists. Recovery is an explicit authority boundary: it restores replacements/removals from backups, removes newly created files, restores/removes the manifest as appropriate, and never writes under canonical `.identity/` source.

### Recovery authority and journal compatibility

`LocalArtifactStore::new(root)` authorizes only `assets/identity/`. Custom roots
must be supplied independently through `LocalArtifactStore::with_output_root(root,
"generated/branding")`, both when committing and when recovering. The CLI wires
its explicit `--output-root` into that constructor. A journal cannot grant itself
a broader root. Canonical `.identity/`, `.git/`, and `.cache/` roots are refused.

New transactions use `identity.compiler-transaction/v2`. Journals bind the full
compiler plan to the transaction directory digest, each action to its planned
operation/current checksum, and staged writes to their resulting checksums.
The manifest is exactly `<authorized-root>/.identity-manifest.json`. Portable
paths reject traversal, Windows drive/stream/device aliases, case collisions,
and conflicting parent/child destinations. Transaction, backup, and destination
paths must not traverse symlinks.

Recovery preflights **all** transaction workspaces before any rollback or cleanup.
It validates plan identities, scope, unique actions, the manifest, every required
backup checksum, and current destinations. A destination must be absent or match
the recorded before/after bytes; unrelated edits block rollback. Backups are read
into memory during preflight. Invalid or incomplete evidence leaves outputs,
source files, backups, journals, and other workspaces untouched; acquisition may
create only the coordination metadata described above. Recovery can be
retried after interruption; calling it again after successful recovery is a no-op.
Only empty orphan workspaces are automatically removed. A populated workspace
without a journal is retained for diagnosis.

Legacy `identity.compiler-transaction/v1` journals are rejected with `IDN2325`
and preserved. They lack the independent output scope and checksum evidence
required for safe automatic migration. Before upgrading, complete recovery of
any trusted pending transaction. If an older or damaged journal remains, preserve
a copy of the workspace, independently identify the intended generated root and
review the original plan/manifest, compare each destination and backup, then
explicitly restore only reviewed generated files. Remove the retained workspace
only after verifying that restoration. Do not relabel a v1 journal as v2 or run
an older recovery implementation against unreviewed journal data.

Plan hashes detect inconsistent evidence; the independently supplied output root
limits mutation authority. Journals are not authenticated signatures, and this
boundary relies on the separately held native lock to serialize cooperating
generation and recovery writers. `identity v1-recover` explicitly invokes the
same library rollback, acquires exclusive ownership and preflights again. It
does not resume the interrupted plan, validate brand source or generate new
output. After reviewing rollback, run `v1-generate` and `v1-verify` with the same
repository/output root. See the [consumer procedure](../consumers/RECOVERY.md).

## Failure states and diagnostic families

Compiler diagnostics extend the existing `IDN` namespace:

| Range | Boundary |
| --- | --- |
| `IDN2000`–`IDN2099` | compiler request, source, and resolved-model invariants |
| `IDN2100`–`IDN2199` | adapter registration and compatibility |
| `IDN2200`–`IDN2299` | rendering, verification, serialization, and artifact budgets |
| `IDN2300`–`IDN2399` | drift, approvals, transaction, and recovery |

The stable failure states remain `invalid`, `unsupported`, `blocked`, `partial`, `failed`, and `drifted`. No partial or unsupported result is reported as verified success.

## Validation evidence

The compiler unit suite uses only local memory, temporary directories, and fixture adapters. It proves:

- mutation-free plans enumerate create/replace/remove operations, warnings, and approvals;
- identical normalized inputs produce identical output and manifest bytes;
- a second identical build resolves to unchanged output without rewriting its manifest;
- missing/networked adapters are visible and blocked;
- verification failures mutate nothing;
- an injected mid-transaction interruption is recoverable while canonical `.identity/` bytes remain unchanged; and
- duplicate adapter identities are rejected.

The [dated writer review](../reviews/writer-serialization-2026-10-19.md) records
controlled pre-fix behavior and independent child-process contention, ownership
release and recovery evidence. These bounded checks do not claim power-loss or
hostile-filesystem durability.

Actual DTCG/CSS/Tailwind/metadata/vector/raster/package golden fixtures belong to #11, which consumes this library boundary rather than changing it implicitly.
