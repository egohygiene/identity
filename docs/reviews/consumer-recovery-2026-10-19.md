# Consumer recovery review — 2026-10-19

Issue [#77](https://github.com/egohygiene/identity/issues/77) follows the
authorized merge of [#120](https://github.com/egohygiene/identity/pull/120) at
`44bf13bc45916d51ae5de10e9af2ce894d3be486`. The existing compiler could roll
back a validated transaction, but the distributed CLI exposed no route for
inspection or recovery. The candidate exposes that existing authority through
`v1-inspect` and `v1-recover`; it does not add a journal version or a release.

## Consumer contract

Both commands accept the same `--repository-root` and `--output-root` options
as generation and verification. They use the artifact store directly, without
canonical-source validation or Python. A missing/broken `.identity/` therefore
cannot prevent journal inspection or rollback. Generation still requires valid
source. The [consumer procedure](../consumers/RECOVERY.md) and
[compiler contract](../contracts/COMPILER_V1.md) distinguish these boundaries.

Inspection and recovery share complete enumeration, journal/backup/destination
validation and cross-transaction conflict detection. Inspection previews
validated workspaces, plan digests and restore/remove paths without exposing
backup content. It creates no metadata and performs no cleanup. An existing
coordination file is opened read-only with a native shared lock; absent
coordination remains a qualified observation and is rechecked before return.
Explicit recovery always acquires exclusive ownership and validates again.

The CLI prints human summaries. Valid pending state is a successful inspection;
active, corrupt, legacy, conflicting or wrong-root evidence returns a nonzero
failure with the existing IDN diagnostic. Transaction errors now expose their
existing path/recovery guidance at the CLI boundary. Library error formatting
and source-validation JSON diagnostics remain separate. Inspection grants no
permission token for a later rollback, and recovery never resumes generation.

## Independent output authority

Review found that the earlier CLI helper used lossy UTF-8 and globally replaced
backslashes before authorization. Reusing it for destructive recovery could
silently target a different valid output root. The candidate rejects non-UTF-8
arguments and converts backslashes only on Windows, where they are native
separators. Unix literal backslashes reach portable validation unchanged and
are rejected. All four v1 commands share the corrected helper.

The Unix CLI regression uses valid canonical source, literal-backslash and
invalid-UTF-8 arguments, both before cache creation and while a valid transaction
for the portable spelling exists. Rejection preserves the complete tree; the
correctly spelled scope still inspects, recovers, regenerates and verifies.
The extraction evolution registry records the three intentionally changed CLI
files while preserving the original Empathy extraction digests and v0 behavior.

## Distinct evidence classes

| Evidence | What it demonstrates | Limit |
| --- | --- | --- |
| Core tests | Read-only/no-cache inspection, shared ownership, whole-batch preview/rejection, legacy/scope behavior and preserved rollback | Local Rust tests; native platforms need their own execution. |
| Shipping CLI integration tests | Copied binary, help/errors, no-Python/source-independent operations, default/custom scopes, native owner contention and exact file preservation | Retained journals are explicitly synthetic fixtures built from valid plans and output bytes. They are not spontaneous interruption observations. |
| Dated runtime replay | The actual compiler/source pipeline publishes a real journal and first output, then a test-only barrier permits termination. The unmodified shipping CLI inspects, recovers and regenerates | Producer is an instrumented test build, not a pristine CLI stopped by spontaneous timing. |
| Hosted validation | Fresh CLI, source-install/clean-room gates on Linux/macOS/Windows, public smoke and advisory checks | Exact candidate head and represented merge commit belong in the PR; local success cannot establish this result. |

The [runtime receipt](../evidence/identity-consumer-recovery-2026-10-19.json)
records actual source/executable hashes, 24 CLI invocations across default and
custom roots, complete inventories and bounded results. Active contenders change
no evidence. Terminating the producer preserves its published journal; inspection
does not repair it. Explicit recovery returns the generated tree to its prior
state, repeat recovery reports zero, and regeneration/verification preserve
canonical/unrelated files. The default 14-file output inventory also matches
the prior reviewed shipping receipt, including the hidden manifest.

## Replay the dated Linux proof

Use trusted Identity source at the reviewed candidate. Compile its shipping
binary and test-only producer with the pinned Rust toolchain, then extract the
exact library test executable from Cargo's JSON artifacts:

```bash
cargo build --locked --all-features --bin "identity"
cargo test --locked --all-features --lib --no-run --message-format "json" \
  > "../identity-recovery-worker-build.jsonl"

worker_executable="$(python3 - <<'PY'
import json
from pathlib import Path
rows = [json.loads(line) for line in Path("../identity-recovery-worker-build.jsonl").read_text().splitlines()]
workers = [row["executable"] for row in rows
           if row.get("reason") == "compiler-artifact"
           and row.get("target", {}).get("kind") == ["lib"]
           and row.get("profile", {}).get("test")
           and row.get("executable")]
assert len(workers) == 1
print(workers[0])
PY
)"

python3 "docs/evidence/consumer-recovery-proof-2026-10-19.py" \
  --repository-root "." \
  --identity-binary "target/debug/identity" \
  --worker-executable "$worker_executable" \
  --receipt "../identity-consumer-recovery-replay.json"
```

The [dated replay harness](../evidence/consumer-recovery-proof-2026-10-19.py)
uses only disposable copies of the synthetic consumer and a separately copied
binary. It requires an external receipt path and makes no changes to the source
checkout. Explicit readiness, bounded waits and kill/reap cleanup replace timing
assumptions. Executable bytes can vary with build paths; source hashes and
observed invariants are separate from artifact identity.

## Review disposition and limits

Decision impact: **reference** ADR-0012, ADR-0019 and proposed ADR-0026. This is
the scoped consumer surface over the existing local source/recovery/locking
authority, with human output rather than a new durable JSON protocol. All 26
records, dispositions and approval/lineage remain unchanged; implementing or
merging #77 accepts no proposal.

Participating local processes are the boundary. Missing-lock observations are
not consistent snapshots; older/uncoordinated tools and hostile directory
replacement remain outside the protocol. No network-filesystem or power-loss
qualification, automatic rollback, creative approval, release or deployment is
claimed. Broader operational documentation reconciliation remains #83, and
the next scheduled implementation issue after reviewed #77 completion is #81.
