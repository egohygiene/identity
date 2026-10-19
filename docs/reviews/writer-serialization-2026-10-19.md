# Local writer serialization review — 2026-10-19

Issue [#79](https://github.com/egohygiene/identity/issues/79) follows confinement
[PR #119](https://github.com/egohygiene/identity/pull/119), merged at
`417865a449678f887237d94aaa019a10bcc16612`. This is a bounded local writer
coordination change, not a release or a recovery CLI implementation.

## What the baseline demonstrates

The [baseline receipt](../evidence/identity-writer-serialization-baseline-2026-10-19.json)
binds the frozen source above, exact source hashes and a
[replayable test-only patch](../evidence/identity-writer-serialization-baseline-2026-10-19.patch).
Two independent stores run in separate threads. Explicit barriers expose real
precheck/preflight boundaries and then release each operation in order. These
are instrumented test builds, not observations of spontaneous shipping-runtime
timing or independent processes.

| Controlled schedule | Observed result | Evidence limit |
| --- | --- | --- |
| Both writers pass pending/current checks; first completes before second resumes | First succeeds. Second fails `IDN2339` after staging and leaves a populated workspace without a journal. Pending-state detection becomes true; recovery rejects it with `IDN2324`. | The second writer leaves final generated output unchanged. No output corruption was observed. |
| Both recoverers preflight the same interrupted journal; first completes before second resumes | Both report one recovered transaction, although the first already removed the workspace. | Final generated files agree and canonical/external sentinels remain intact. This establishes duplicate recovery reporting under this schedule. |

Shared checks are not exclusive ownership. The original audit's possible mixed
journals or corruption remain inferences; these tests do not upgrade them to
reproduced facts.

## Candidate ownership contract

One independent RAII `File` handle holds a nonblocking native exclusive lock on
`.cache/identity/writer.lock`. Commit and recovery share it across all output
roots beneath one canonical repository. Mutation-free request/path validation precedes
acquisition; all pending/current-state checks and transaction/recovery mutation
run under the guard through final verification and cleanup. No-op commits own
the same boundary.

The regular coordination file persists. Acquisition never writes its bytes,
truncates it or removes its name. Presence, PID or age never grants permission
to steal ownership or delete a workspace. Existing hard-linked regular files
retain their aliases and bytes. Unsupported linked/reparse/special cache-root or lock paths fail
before coordination metadata is created; native lock failures have no unlocked
fallback. A contender receives blocked `IDN2346`; acquisition failures use
`IDN2347` with the actual failure kind.

Ordinary guard cleanup explicitly unlocks before closing its handle. Process
termination closes its handles; native ownership ends after all inherited or
duplicated handles are closed. It does not declare a journal safe
or discard it. The next generation attempt remains blocked by pending recovery,
and explicit library recovery performs the existing complete preflight and
rollback. An empty recovery or later failure can create only the empty lock file
and its parent directories. This coordination metadata exception does not permit
changing canonical source, outputs, journals or backups on rejection.

The [compiler contract](../contracts/COMPILER_V1.md) describes the operator
boundary. [ADR-0026](../decisions/ADR-0026-local-writer-serialization.md) remains
proposed with null approval; implementation and tests grant no human authority.

## Validation boundary

The candidate adds opt-in, test-only checkpoints on individual stores. An
independent child test process pauses after native ownership or after a recorded
mutation. Parent processes wait for an explicit readiness line, release through
stdin, or terminate and reap the child. Time limits detect failed coordination;
elapsed time is never treated as evidence that ownership was acquired.

Final executed results and source hashes are recorded in the
[candidate receipt](../evidence/identity-writer-serialization-2026-10-19.json).
Fresh hosted platform and advisory evidence belongs to the exact PR head and
its represented merge candidate; local Linux checks alone establish no native
Windows/macOS result.

## Limits and next owner

This protocol coordinates participating local writers. Construction, reads,
planning and read-only verification remain mutation-free and do not promise a
snapshot while a writer is active. Commit revalidates optimistic destination
checksums under ownership. Older binaries or arbitrary filesystem writers do
not participate; stop all writers before manual cache work or protocol changes.

There is no qualification for network filesystems, hostile directory replacement,
fairness, automatic waiting, all possible schedules or power-loss durability.
Journal v2, generated formats, source authority and deterministic output remain
the existing contracts. [#77](https://github.com/egohygiene/identity/issues/77)
owns supported read-only inspection and explicit recovery commands; no such CLI
command is added or advertised here.
