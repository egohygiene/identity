# Copied executable investigation — 2026-11-22

Base source: `ec8fce30c3c96c7781238eb0a8899d6f0cee0a40`.
Issue owner: [#70](https://github.com/egohygiene/identity/issues/70).
This is a bounded test-harness investigation, not a product recovery change,
release qualification, or proof of the exact cause of a historical CI run.

## Existing diagnosis and remaining window

The [November 14 local acceptance](../116/LOCAL_ACCEPTANCE.md) already records
a reproduced Linux `ETXTBSY`/OS-error26 mechanism and the repair in
`tests/consumer_recovery.rs`. Preserve that dated evidence. Its mutex covers
the executable copy and both child-spawn sites; it is released after spawn,
so actual recovery and native writer concurrency remain exercised.

The current trace found a separate uncovered window:

| Harness | Executable writer and process lifecycle | Disposition |
| --- | --- | --- |
| `tests/consumer_recovery.rs` | `Standalone::new` copies the CLI while holding `COPY_OR_SPAWN`; `run` and `owner` hold the same mutex through child spawn. | Existing scoped repair retained unchanged. |
| `tests/v1_consumer.rs` | The standalone test copied the CLI in the multithreaded parent. Other tests call `V1ConsumerPipeline::load`, whose `src/v1_consumer/preflight.rs` spawns Python in that same process. Direct test `Command` calls also coexist. | Isolate the executable writer in a separate process. A mutex around only direct test spawns would miss library preflight. |
| `tests/v1_initializer.rs` | Its single ordinary test copies the CLI before its first child spawn. It has no competing test-copy/spawn path in that process at this source. | No change justified by this trace. Future concurrency changes need review. |
| Other Rust integration/unit harnesses | Located process workers execute the existing CLI or current test executable; fixture copies and generated artifact writes are not writes to those executable inodes. | No additional executable writer identified in this bounded source search. |

Close-on-exec does not prevent a descriptor from being inherited at fork; it
closes it when the child actually executes a new image. A child retained before
that point can keep the destination inode open for writing after the copying
thread has closed its own descriptor. Another execution of that inode can then
return `ETXTBSY`. No retry or delay establishes why that happened historically.

## Controlled Linux mechanism probe

Run the standard-library-only probe:

```bash
python3 tests/probes/executable_copy_isolation.py
```

The [retained JSON](../../evidence/executable-copy-2026-11-22/mechanism.json)
comes from Python 3.12.14 on Linux. The probe copies the system `true`
executable into a disposable directory. Pipe barriers deliberately retain
children and writable descriptors; scheduling luck is not its trigger.
Readiness, execution and child exit have finite timeouts.

| Controlled state | Observed outcome |
| --- | --- |
| Parent closes its writable descriptor, but a forked child still retains it. | Execution returns errno26. |
| That inheriting child exits; executable bytes are unchanged. | The same executable exits0. |
| A separate writer child alone holds a writable descriptor. | Execution returns errno26 while that writer remains alive. |
| The isolated writer exits, while an unrelated child forked by the parent remains alive. | Execution exits0, with unchanged bytes. |

This proves the inherited-descriptor mechanism and the isolation property. It
does not reproduce the original hosted scheduler/process trace, establish that
the uncovered consumer test has already failed on this revision, or diagnose
every possible source of `ETXTBSY`.

## Narrow harness repair

The standalone consumer test now invokes one ignored, explicitly selected
copy-worker test in a separate process, with `--test-threads=1`. The worker
performs the only executable write and the parent waits for its exit before
running the copy. Other parent tests and production preflight calls remain
concurrent; none can inherit a writable descriptor opened only in that worker.

The harness verifies that the worker actually ran in a different process and
that the independent CLI copy matches the actual binary byte-for-byte. Its
existing missing-runtime, consumer-Python isolation, generation and read-only
verification assertions remain unchanged. Worker completion is bounded to
30 seconds, with kill/wait on timeout. The helper is intentionally ignored in
ordinary test selection and is not counted as an independently passing test.

Only test code and these diagnostic records change. There is no production
mutex, library/API change, blanket serial-test requirement, assertion
relaxation, executable retry, or historical receipt rewrite.

## Validation and limitations

Actual local Linux results with pinned Rust/Cargo 1.97.1, one build job and
the existing prepared dependency cache are retained in the
[qualification record](../../evidence/executable-copy-2026-11-22/qualification.json):

| Command | Result |
| --- | --- |
| `python3 tests/probes/executable_copy_isolation.py` | Passed all four controlled descriptor/lifecycle expectations; copied bytes unchanged. |
| `cargo test --locked --offline --all-features --test v1_consumer standalone_binary_uses_embedded_preflight_and_ignores_consumer_python_code -- --exact --nocapture` | One ordinary test passed; it actually invoked and verified the separate worker. |
| `cargo test --locked --offline --all-features --test v1_consumer -- --test-threads=16` | Fourteen ordinary tests passed; one explicit worker-only ignore. No retry or assertion relaxation. |
| `cargo clippy --locked --offline --all-features --test v1_consumer -- -D warnings` | Passed. |
| `rustfmt --edition 2024 --check tests/v1_consumer.rs` and `git diff --check` | Passed. |

The isolated worker's ignore is intentional and is not a skipped product
case. Its execution is part of the ordinary standalone regression, including
different-PID and exact-byte assertions. The previously repaired recovery
harness is unchanged; this scoped run does not repeat its acceptance campaign.

The parent agent separately reported a passing full Rust baseline on
`ec8fce30c3c96c7781238eb0a8899d6f0cee0a40`, without an `ETXTBSY` incident.
That does not prove an intermittent window is absent or supply a historical
causal trace. This change has only the focused execution evidence above; a
later integrated baseline remains the parent checkpoint's responsibility.

The broader #70 audit, clean-base/CI/browser and native-platform acceptance,
real self-source/release/adoption under #98, and final #116 reconciliation
remain with their existing owners.

Decision impact: **ADR not required**. This is a localized test-fixture process
lifecycle repair under existing validation/concurrency contracts, with no
public or durable ownership boundary change. The pinned Aether
`create-decisions-document` 2.1.0 and `maintain-repository-continuity` 1.1.0
sources were read through `git show` at
`dc8a16851f452763ef4f7fbe4bf057d4500b1921`, together with the selected Hygiene
ADR policy1.2.0. The parent checkpoint owns the integrated continuity refresh.
