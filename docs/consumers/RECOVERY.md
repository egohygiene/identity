# Inspect and recover interrupted v1 generation

These commands are available in current source. Use an exact reviewed Identity
commit or a release that includes them; the earlier stable `v1.0.0` does not
gain commands when a later PR merges. Installation and source pinning follow
the [adoption guide](ADOPTION.md).

## Inspect before recovery

```bash
identity v1-inspect --repository-root "path/to/consumer"
```

Inspection does not create cache directories or a lock file, change file bytes,
repair a journal or remove an orphan workspace. It performs the same complete
journal, backup, destination and cross-transaction conflict preflight as recovery
and reports validated workspace names and proposed restore/remove paths. It
prints pending-transaction and empty-workspace counts. Valid pending state is a
successful inspection; an active writer, corrupt evidence or unsupported scope
is a nonzero failure with its existing diagnostic and recovery guidance.

An existing regular `.cache/identity/writer.lock` is opened read-only and held
with a shared native lock during preflight. Participating generation/recovery
writers cannot mutate that namespace during the observation. If no lock exists,
inspection remains an explicitly **uncoordinated observation**. It rechecks for
a newly appearing lock and repeats under shared ownership when available;
absence cannot promise future inactivity. Inspection never grants authority for
a later rollback. Recovery obtains exclusive ownership and preflights again.

The output is for people, not a new versioned JSON interface. There is no
`--output` option that could turn inspection into a file write.

## Explicitly roll back, then regenerate

Stop any active writer and review the inspection result. For the default
`assets/identity/` output root:

```bash
identity v1-recover --repository-root "path/to/consumer"
identity v1-generate --repository-root "path/to/consumer"
identity v1-verify --repository-root "path/to/consumer"
```

Recovery rolls back interrupted generated-state transactions. It restores
replaced/removed files and the old manifest from validated backups and removes
files newly created by the interrupted plan. It does not resume that plan or
silently generate a new one. Canonical `.identity/` source and unrelated files
are outside its mutation authority. A destination changed to unrelated bytes
blocks rollback instead of overwriting the edit.

The command shares the exclusive writer lock with generation across all output
roots. It validates the complete retained batch before any rollback or cleanup;
one damaged or conflicting workspace prevents the batch from being changed.
Its success summary lists recovered plan digests. A repeated successful recovery
reports zero transactions. Empty orphan workspaces may be removed explicitly by
recovery; populated workspaces without a valid journal remain for diagnosis.

Recovery may create only the persistent empty lock file and parent directories
when no coordination file existed, including an empty recovery or a later
preflight failure. It never truncates, replaces or deletes an existing lock.
The file's presence, age or contents do not establish live ownership.

Inspection and recovery operate on the artifact store directly. They require
neither Python nor valid/present canonical brand source. Repair source separately
before regeneration; generation and verification retain their full source
preflight requirements.

## Authorize a custom output root consistently

Supply the original independently selected root to every command:

```bash
identity v1-inspect \
  --repository-root "path/to/consumer" \
  --output-root "generated/branding"
identity v1-recover \
  --repository-root "path/to/consumer" \
  --output-root "generated/branding"
identity v1-generate \
  --repository-root "path/to/consumer" \
  --output-root "generated/branding"
identity v1-verify \
  --repository-root "path/to/consumer" \
  --output-root "generated/branding"
```

The default is always `assets/identity/`; a journal cannot choose a different
root or broaden authority. A wrong-root inspection/recovery fails while retaining
the evidence. Canonical `.identity/`, `.git/`, `.cache/`, traversal and unsafe
portable path aliases are refused. Linked/reparse/special cache paths remain
unsupported. No external cache option or automatic migration is added.

## Diagnose safely

| Observation | Supported next action |
| --- | --- |
| `IDN2346`: another operation owns the namespace | Wait for generation, inspection or recovery to finish, then retry. Never remove the lock or another operation's workspace. |
| `IDN2347`: native lock acquisition fails | Check local path permissions and native filesystem lock support. No unlocked fallback is attempted. |
| `IDN2325`: legacy v1 journal | Preserve the workspace and follow the compiler contract's reviewed manual restoration procedure. Do not relabel it as v2. |
| Invalid/missing backup, corrupt journal, conflicting batch or unrelated destination bytes | Preserve all evidence and review the reported path/diagnostic. Inspection and recovery do not repair damaged evidence. |
| Pending transaction blocks generation (`IDN2301`) | Inspect, explicitly recover with the same repository/output root, then regenerate and verify. |

The [compiler contract](../contracts/COMPILER_V1.md) owns journal authority,
legacy compatibility and confinement. Proposed
[ADR-0026](../decisions/ADR-0026-local-writer-serialization.md) describes the
native ownership protocol and retains null approval. Participating local tools
share it; older binaries and arbitrary filesystem writers do not. Stop writers
before manual cache work. No hostile-directory-replacement, network-filesystem
or power-loss durability is promised.
