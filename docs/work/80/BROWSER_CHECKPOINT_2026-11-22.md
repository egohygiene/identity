# Browser workflow checkpoint — 2026-11-22

Issue: [#80](https://github.com/egohygiene/identity/issues/80).
Base: `ec8fce30c3c96c7781238eb0a8899d6f0cee0a40`.
Executed repaired source: `57704aea75ee12074592ad0a6c9ad1ec692a9b9c`,
following `5cb5b91`'s caller-context correction.

**The original qualified Docker/CI gate remains open.** This checkpoint fixes
two demonstrated evidence/preparation defects, retains an actual failed local
workflow attempt, and separately records successful browser diagnostics from a
derived OCI filesystem. The latter is not relabeled Docker or hosted CI proof.

## Actual results

| Check | Result and scope |
| --- | --- |
| Browser boundary suite | Nine Python cases pass, including real host-receipt writing under the environment exposed by `act`, storage refusal, remote-context precedence and reserved failure-record writes. |
| Original Docker route before storage repair | Pinned image acquisition completed, then BuildKit preparation exhausted the shared VFS filesystem before its first build `RUN`. The wrapper exited 120 and left an empty host receipt. Other authorized checks were also writing; no isolated capacity threshold is inferred. |
| Repaired original route | Exits 1 before image acquisition because the observable VFS store is below the 16-GiB preparation budget. A valid 8,711-byte failure receipt is retained. This is successful refusal behavior, not browser qualification. |
| Actual production workflow through local `act` | The unchanged `reference-renderer.yml` / `validate` job starts on the cached immutable runner image, then fails acquiring its pinned `step-security/harden-runner` action through GoGit. No workflow step or browser gate executes. The exact action tree remains accessible through the connected GitHub REST tool; this is an acquisition-path limitation, not evidence that the pin is absent. |
| Separate derived-rootfs browser diagnostic | Nine positive cases pass; the original screenshot assertion rejects a deliberate disposable CSS change; restoring the CSS passes the assertion. Zero skips/retries; approved PNG and tolerance remain unchanged. |

## Evidence and bounded repairs

`act` sets both `ACT=true` and `GITHUB_ACTIONS=true`. The old wrapper used only
the latter and would label a local replay `github-actions-ci` or
`hosted-local-entrypoint-replay`. The wrapper now gives the explicit local marker
precedence, producing `local-act-ci` / `local-act-local-entrypoint-replay`.
The regression exercises the real failed-receipt writer without starting Docker.

The image was shown as 2.49 GB by Docker, but VFS/BuildKit materialization filled
a shared filesystem that initially had approximately 8.5 GiB free. Preparation
now observes the checkout, evidence and daemon data filesystems before pulling.
It requires a conservative 16-GiB budget for VFS or 4 GiB for other drivers, and
refuses an unobservable daemon store. These budgets do not guarantee capacity
under concurrent writers. The wrapper reserves 1 MiB for its host JSON before
image preparation and reuses that allocation for its bounded final record.
Unexpected reserved-file replacement and oversized records fail explicitly.

Independent review additionally caught a remote-daemon ambiguity: the same
`DockerRootDir` path can exist on an unrelated client filesystem. The final
helper respects `DOCKER_CONTEXT` before `DOCKER_HOST`, requires a parsed local
absolute Unix endpoint and absolute observable data root, and refuses remote
or unknown endpoints before consulting local capacity. A real-main regression
covers a remote context overriding a local host setting and a coincident local
directory. The retained `57704ae` runtime/refusal records predate this final
endpoint correction and keep their actual source identities; they are not
relabeled evidence for the later integrated code.

Only this attempt's pulled Playwright image and explicitly identified new
BuildKit cache records were removed after the storage failure. The shared local
runner image, older cache, canonical source and existing evidence were retained.
No global Docker prune was used.

## Derived filesystem diagnostic

The unchanged profile selects Playwright 1.62.1 Noble at OCI index
`sha256:dcc5531e97840b9b5e794f2814476b21571c5124a3fca2267d73041f56e7580e`.
The official index, selected Linux/amd64 manifest and config were fetched and
their raw byte digests verified. A checksum-pinned
[crane 0.20.6](https://github.com/google/go-containerregistry/releases/tag/v0.20.6)
export flattened that source into a private filesystem rather than storing
cumulative VFS snapshots. Its selected Linux x86-64 tool archive was
15,879,366 bytes, SHA-256
`c1d593d01551f2c9a3df5ca0a0be4385a839bd9b86d4a76e18d7b17d16559127`.

The export contained 35,733 entries / 2,448,817,349 declared bytes. All 684
tracked source files were copied from the clean repaired revision and compared
again after execution. The existing font installer, frozen pnpm installation
and renderer build ran in an unshared user/PID/mount namespace and chroot.
The first preparation emitted a nonfatal `/dev/null` warning while still
completing the renderer build; the runtime used the host device mount in its
private mount namespace instead. No credentials or ignored Git/tool caches were
copied. Certificate/proxy configuration was limited to preparation, and proxy
values are excluded from the records.

The existing `renderer/scripts/qualify-browser.mjs` then ran in a separate
unshared user/PID/mount/network namespace with loopback and 1-GiB shared memory.
Its raw evidence passes the existing Python receipt validator: profile,
Playwright/pnpm versions, actual Chromium executable/process, exact DejaVu
package/font hashes, rendering settings, positive/negative/restored outcomes
and fresh difference artifacts all match. Observed runtimes are Node 24.18.1,
pnpm 11.21.0, Playwright 1.62.1 and Chromium 151.0.7922.34.

**This was a derived rootfs, not the original Docker image execution.**
Extraction occurred as the task user; original OCI ownership equivalence is
not asserted. No Docker image/config equivalence, production workflow success,
GitHub-hosted CI, release or human approval follows from these browser results.
The private rootfs was removed after retaining and independently validating the
evidence, recovering approximately 2.6 GiB.

## Retained records

- [Actual local workflow attempt](evidence-2026-11-22/actual-act-attempt.json)
  and [sanitized process log](evidence-2026-11-22/actual-act-attempt.log).
- [Initial storage failure observation](evidence-2026-11-22/initial-storage-failure.json),
  explicitly reconstructed from its retained private log rather than a valid
  host receipt.
- [Actual repaired refusal receipt](evidence-2026-11-22/storage-preflight.json).
- [Derived diagnostic envelope](evidence-2026-11-22/derived-runtime-diagnostic.json)
  and [raw browser receipt](evidence-2026-11-22/derived-runtime/qualification.json).
- [Positive report](evidence-2026-11-22/derived-runtime/browser-fJyMDf/positive/report.json),
  [deliberate failure](evidence-2026-11-22/derived-runtime/browser-fJyMDf/negative/report.json)
  and [restored report](evidence-2026-11-22/derived-runtime/browser-fJyMDf/restored/report.json),
  with the original actual/diff/expected screenshots and trace beneath the
  negative phase.
- [Verified registry identities](evidence-2026-11-22/registry-verification.json),
  [bounded export record](evidence-2026-11-22/rootfs-export.json), and
  [artifact checksums](evidence-2026-11-22/SHA256-MANIFEST.json).

## Remaining acceptance

Run the original qualified Docker workflow on adequate observable storage with
working acquisition of the unchanged pinned actions. Complete its actual CI
and local-entrypoint results, preserving all image/font/source and approved
baseline bindings. Retain exact current-source evidence after any later code
integration. Local `act`, the successful derived diagnostic and authored tests
do not replace an absent hosted CI observation or the original issue criterion.
#70/#82/#88/#98/#116 keep their independent acceptance and owner facts.

ADR-Ref: egohygiene/identity#ADR-0011 (reference). These repairs enforce truthful
existing evidence boundaries; profile, font, approved screenshot and human
decision dispositions are unchanged.
