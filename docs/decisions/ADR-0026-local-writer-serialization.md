---
schema: egohygiene.architecture-decision/v1
id: ADR-0026
title: Serialize local generation and recovery with one persistent native lock
status: proposed
date: "2026-10-19"
decision_scope: repository
visibility: public
owners: [egohygiene/identity]
issue: https://github.com/egohygiene/identity/issues/79
pull_request: null
related: [ADR-0012, ADR-0019]
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/identity]
affected_contracts: []
implementation_status: implemented
evidence:
  - type: documentation
    url: https://github.com/egohygiene/identity/blob/417865a449678f887237d94aaa019a10bcc16612/docs/contracts/COMPILER_V1.md
    description: Reviewed confinement contract distinguishes serialized pathname checks from the still-open writer coordination boundary.
approval: null
exceptions: []
---

# ADR-0026: Serialize local generation and recovery with one persistent native lock

## Context

#78 confines transaction paths but does not reserve ownership across processes.
The #79 instrumented baseline coordinates two independent stores after their
real prechecks. One writer completes; the other resumes stale prechecks and
leaves an unjournaled workspace. Two recoverers can both preflight and report
recovering the same journal. Neither bounded schedule shows output corruption.
The shared transaction namespace needs one owner before state-dependent checks,
including recovery and commits whose plan currently has no mutations.

The supported toolchain is Rust 1.97.1. Its standard library supplies a native
nonblocking exclusive file lock without a new dependency or a PID liveness
protocol. This record captures the choice considered for #79 now; it does not
reconstruct historical motives or grant lifecycle approval.

## Decision

Propose a repository-wide exclusive `File::try_lock` guard on
`.cache/identity/writer.lock`, shared by generation and recovery and independent
of the selected output root. Canonicalize the repository and apply #78's path
checks before creating coordination metadata. Validate request/path inputs without mutation
before acquisition; under ownership, recheck pending transactions and current
checksums before reserving or mutating workspaces. Hold the guard through
verification and cleanup, including no-op commits and recovery.

Keep the coordination file persistent. Create it exclusively when absent; open
an existing regular file for reading and writing without truncation or content
writes. Never unlink or replace it, write owner/PID bytes, steal it by age, or
implement timeout cleanup. Its presence says nothing about live ownership.
Existing hard-linked regular files retain their bytes and aliases; those aliases
may coordinate more than one repository. Reject linked/reparse/special paths.

Report contention as blocked `IDN2346`. Fail closed on unavailable native
locking or acquisition errors (`IDN2347`); do not fall back to a second lock or
an unlocked write. Ordinary guard cleanup explicitly unlocks before closing its
handle. Process termination releases native ownership after all inherited or
duplicated handles are closed; the store does not clone the guard handle. A
retained transaction journal still requires explicit recovery before generation
may proceed.

## Alternatives considered and rejected

- A create/delete sentinel: owner death leaves ambiguous ownership, and deleting
  a live sentinel can let two writers lock different files.
- PID or age-based stealing: process reuse and delayed writers cannot establish
  that it is safe to remove another owner's workspace.
- A lock per output root or only around directory creation: recovery shares the
  repository transaction namespace, and stale state checks would remain outside
  exclusive ownership.
- A process-local mutex or documentation alone: does not exclude another CLI
  process using the same repository.
- A new platform wrapper dependency or hard-link identity FFI: not needed for
  the bounded std-only protocol; preserving an existing regular lock's bytes
  retains the existing alias-preservation boundary.

## Consequences and tradeoffs

Cooperating processes safely reject contention without waiting or touching the
active transaction. A killed process needs no ownership cleanup; journal
validation and rollback remain separate. The persistent empty coordination file
and its parents may be created even when recovery is empty or a later check
fails. This exception does not permit changing retained journals, backups,
canonical source or generated state on rejection.

The guard serializes participating local writers, not readers or arbitrary
filesystem calls. Preparation and read-only verification remain mutation-free
and may observe an active writer; commit revalidates its optimistic plan under
the guard. Older binaries and other tools must not write concurrently. No
consistent reader snapshot, hostile directory-replacement protection, network
filesystem qualification, fairness, automatic waiting or power-loss durability
is promised. Generated bytes, plan digests and journal v2 remain unchanged.

## Implementation and evidence links

The implementation belongs in `src/compiler/filesystem.rs`; the
[compiler contract](../contracts/COMPILER_V1.md) specifies scope and diagnostics.
The [dated #79 review](../reviews/writer-serialization-2026-10-19.md) and
[receipt](../evidence/identity-writer-serialization-2026-10-19.json) distinguish instrumented baseline outcomes,
independent child-process regressions and platform evidence. Rust's
[File documentation](https://doc.rust-lang.org/std/fs/struct.File.html#method.try_lock)
describes native locking and handle lifetime. Exact executed checks and the
reviewed commit belong in the implementation PR and CONTINUITY.md. Implementation
and test success do not accept this proposed decision.

## Replacement or exit strategy

Any replacement must coordinate with this same persistent lock during migration;
changing or deleting the file while a participant is active can split ownership.
Stop every writer before changing protocols or manually managing cache state.
Preserve and explicitly recover reviewed journals with a compatible implementation
before rollback to older binaries. A distributed or hostile-filesystem use case
requires its own reviewed protocol and evidence.

## Follow-up work

#77 exposes supported read-only interruption inspection and explicit recovery.
#87 may extract modules after preserving these contracts and process regressions.
Release/install qualification and final operational reconciliation retain their
existing roadmap owners. No release or rollout is authorized by this proposal.
