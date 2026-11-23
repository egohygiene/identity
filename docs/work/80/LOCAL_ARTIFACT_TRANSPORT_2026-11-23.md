# Local artifact transport qualification — 2026-11-23

The complete original reference-renderer workflow passes locally on frozen
source `5afa292c41563fe16f48f321eb5ac37459fda3dd`, including timestamp/install
parents. The optional explicitly named derivative is
`0.2.98+identity.zipmime.2`, SHA-256
`e103cd431339dd0be997d5b0a9599a7327da8d1d327ed3fe809636b8fdd2ce90`.
Official/global act, the original workflow, four action pins, security steps,
browser profile, fonts and approved PNG are unchanged.

The [workflow receipt](artifact-transport-2026-11-23/workflow-replay.json) records
whole-job exit zero, no timeout, clean source and preserved action trees. The
actual sender uploaded 4,074,757 bytes. Its printed digest and Finalize digest
equal the independently authenticated downloaded ZIP SHA-256:

```text
127fb7ed43c274ff4a15388a79569c6ac561694402e1bd4dbfbaa38e2a9f42e6
```

All 74 actual selected input files match the complete ZIP inventory, including
individual sizes/hashes. This archive is below 4 MiB; no large-artifact or
multiblock acceptance is claimed. The exact ZIP and raw workflow logs remain
private. Public receipts contain hashes/outcomes, without tokens or signed URLs.

The original frontend step passes 19 test files / 424 tests, contract checks,
build and public-output validation. Each original browser command passes nine
positive checks, observes the intended screenshot failure after disposable CSS
mutation, then passes the restored check. Source/profile/font/image bindings
remain exact; the baseline and tolerance are unchanged. Approved PNG SHA-256:
`53d7d144734ac63ceb730e95c7a39acc47d3fa64c5429f752233978289088543`.

The [browser index](artifact-transport-2026-11-23/browser-projection.json) binds
ten explicit public JSON/PNG/Markdown/trace members per entrypoint to the actual
archive and host receipt. Each byte was rehashed; private-content checks include
trace contents. Four logs per browser stay private. The original uploader's
default omits hidden files: three `.last-run.json` state files per browser are
absent from the ZIP and have only original host-receipt source hashes. These
are not claimed retained or recovered. The 74-file claim means the actual
default-selected upload inventory, not every temporary file.

The [build receipt](artifact-transport-2026-11-23/build.json),
[actual sender preflight](artifact-transport-2026-11-23/preflight.json) and
[recipe](../../LOCAL_ARTIFACT_TRANSPORT.md) bind source, sender schema, patch,
tools and output binary. The descriptor proof admits only exact typed field
six. Strict malformed/unknown/MIME cases and missing/tampered signed targets
fail. The [historical v1 failure](artifact-transport-2026-11-23/historical-v1-preflight.json)
remains separate: the actual SDK truncated a raw padded signature from 44 to
43 characters. Only the emitted signature is now URL-escaped; verification and
target bindings are unchanged.

Eleven focused Python controls passed on host and helper before the workflow.
The frozen source passed 258 of 260 Python tests, with two existing skips.
Later test-only changes separate POSIX descriptor/link/FIFO controls behind
capability gates; portable HTTP/ZIP/protobuf checks remain active. Later
test/document-only integration is not relabeled as this workflow's source.

The [runtime budget](artifact-transport-2026-11-23/runtime-resource-summary.json)
records minimum sampled free storage 5,635,366,912 bytes and zero memory max/OOM
events. Helper peak was 5,300,760,576 bytes against 12 GiB. The original 4 GiB
browser guard remained active. Final independent
[input verification](artifact-transport-2026-11-23/final-input-identity.json)
confirms all 866 tracked bytes/modes and the selected binary stayed intact.

This is local Linux amd64 execution. The unchanged hardening action reports
self-hosted context; local success does not establish GitHub-hosted protection.
No hosted dispatch, publication, release signing, broader platform support,
actual identity-source choice or new human creative/accessibility approval
occurred. Existing #70/#80/#82/#88 engineering gates remain subject to integrated
review/merge; separate source/release acceptance remains open.

Decision impact: reference ADR-0011. The optional bounded transport and later
test fixes do not accept an ADR lifecycle, creative baseline or release decision.
