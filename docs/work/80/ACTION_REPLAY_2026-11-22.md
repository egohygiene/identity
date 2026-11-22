# Original Docker and local workflow browser proof — 2026-11-22

Issues: [#80](https://github.com/egohygiene/identity/issues/80) and its
[#88](https://github.com/egohygiene/identity/issues/88) prerequisite.
Executed clean source: `a56399b33548cab075e4442e64605035bccd973f`.
Integration base: `75ca39f3fc7e5e9e0b5578af58c966cd2590a652`.

The **original Docker browser path now passes directly and from both browser
steps of the unchanged reference-renderer workflow through local act**.
Each execution passes nine positive cases, rejects the deliberate screenshot
change, then passes the restored comparison. There are zero skips or retries.
The approved PNG, tolerance, browser profile, fonts and workflow are unchanged.

The **whole local act job exits 1**: after both browser steps pass, its artifact
server rejects the unchanged upload action's `CreateArtifact` `mime_type` field.
This is retained as a local act transport failure. No GitHub-hosted CI,
successful artifact publication, release or creative approval is claimed.

## Exact source and results

All three receipts bind clean source `a56399b…`, the same 423-file inventory
`07bb513dd71ad84f2980fed5479cf683a7689b749c7700d35f92a322ffbd3726`,
and the original baseline SHA-256
`53d7d144734ac63ceb730e95c7a39acc47d3fa64c5429f752233978289088543`.
They observe native Linux/amd64 Docker 28.4 with `overlay2`; no derived rootfs
or emulated browser replaces the original Docker path.

| Actual invocation | Context recorded by qualifier | Result |
| --- | --- | --- |
| Direct default command, optional environment CA | `local-host` | 9 positives → 1 intended screenshot failure → 1 restored pass |
| Original workflow CI browser step | `local-act-ci` | Same complete pass |
| Original workflow default local-entrypoint step | `local-act-local-entrypoint-replay` | Same complete pass |

The same actual workflow also passes 51 JavaScript source parses, all 424
Vitest tests in 19 files, the renderer build and public-output validation.
Its outer setup-node action selects Node 24.22.3; pnpm is 11.21.0. The qualified
browser image independently retains Node 24.18.1, Playwright 1.62.1 and Chromium
151.0.7922.34/revision 1234. The two runtime contexts are not conflated.

The [summary](action-replay-2026-11-22/qualification-summary.json) links the
three full raw packets, each containing its host receipt and sixteen artifacts:

- [Direct original Docker](action-replay-2026-11-22/original-docker/host-qualification.json).
- [Original workflow CI step](action-replay-2026-11-22/original-workflow-ci/host-qualification.json).
- [Original workflow local step](action-replay-2026-11-22/original-workflow-local/host-qualification.json).
- [Actual whole-workflow result and limits](action-replay-2026-11-22/actual-act-final.json).
- [Sanitized complete workflow log](action-replay-2026-11-22/actual-act-final.log).
- [Retained file hashes](action-replay-2026-11-22/SHA256-MANIFEST.json).

Each raw host receipt verifies the exact profile, image index/config binding,
font packages/files, browser executable/process/settings and unchanged baseline.
It also hashes its own artifact files. The outer manifest hashes retained
bytes; sanitized workflow logs separately identify their original raw-log and
retained sanitized-log hashes. No raw receipt or trace was rewritten to hide
the deliberately failed visual comparison.

## Repairs and actual caller configuration

The prior act attempt failed acquiring the public harden-runner commit through
GoGit before any step. The new bounded
[preparer](../../../scripts/prepare_local_actions.py) verifies all four exact
public action archives against a reviewed size/SHA-256 lock and independently
reconstructs their complete Git trees, including file modes. The locked trees
match exact public Git commit API observations. It refuses unexpected workflow
bytes/selections, mutable pins, traversal, links, special files, duplicate
paths/JSON keys and excessive archives. It never executes actions.

The [source observations](action-replay-2026-11-22/action-source-observations.json)
and [preparation receipt](action-replay-2026-11-22/action-mirrors.json) retain
all four repository/commit/tree/archive identities. Explicit act
`--local-repository` selections use those exact mirrors. The original hosted
workflow and action pins are not changed. An actual strict dry-run first
passed source planning; that limited result is distinct from the subsequent
actual step execution.

The original storage guard first correctly rejected the physical workspace.
Source, evidence and the isolated daemon's real data root were then placed on
the same observable task-owned tmpfs and native `overlay2` backend. Its
unchanged non-VFS guard requires 4 GiB free at each observed path; these are
three observations of one shared filesystem, not three independent reserves.
No storage guard was lowered. Only the owned nested images/cache were cleaned
between heavy browser/development qualification slots; the shared default
daemon and unrelated containers/configuration were not pruned or changed.

The disposable helper uses the immutable runner image
`ghcr.io/catthehacker/ubuntu@sha256:19619a010b204f44c5340bff7d39b68551109fe6a56a53f75201ea91e05d4270`,
two CPUs and 12 GiB memory, without privileged mode. Act 0.2.97 runs its host
executor inside that task helper (`ubuntu-latest=-self-hosted`); the actual
browser steps still build and run the original Docker image with network
disabled during qualification. This is not GitHub's Ubuntu runner image.

Namespace-correct proxy values are passed through a private, mode-0600 local
environment file. Node's supported `NODE_USE_ENV_PROXY=1` enables Corepack's
fetches. `IDENTITY_BROWSER_PROXY_CA` selects the same existing BuildKit CA-secret
transport as explicit `--proxy-ca`, allowing the original workflow command to
run on this managed network. Explicit CLI input wins; unset/empty behavior is
unchanged. Missing/non-file/looping and comma/quote/control-character paths fail
before output allocation or Docker, without disclosing private paths. TLS and
all font/archive checksums remain enabled. The private environment file and
an unused experimental image-cache completion marker were removed afterward.

Original harden-runner pre/main/post steps execute and identify the supported
self-hosted context; they do not establish hosted-runner protection. Act uses
its default local checkout copy; no authenticated GitHub checkout or GitHub
secret is supplied. The upload action executes unchanged against a loopback
local artifact server and fails its actual protocol request. It is not skipped
or turned into a forced pass.

## Acceptance and remaining limits

The requested original qualified browser path and matching current-source
local-workflow browser steps are now actually evidenced. This supplies the
previously missing browser evidence for reviewing #80 and #88; closing issues
remains a maintainer review decision. The full local act workflow remains red
until its artifact-server protocol supports this pinned uploader. No overall
CI-green or GitHub-hosted claim follows from the passing browser steps.

The final path has 22 passing focused Python boundary tests and independent
read-only review. Earlier acquisition, Corepack and missing-CA failures remain
in the packet with their own exact sources; they are not relabeled final-head
results. Subsequent integration does not change the represented source of
these receipts. Native platform/release qualification, manual contrast/design
review and other roadmap gates remain owned by their existing issues.

Decision impact: reference accepted
[ADR-0011](../../decisions/ADR-0011-accessibility-and-visual-evidence.md).
These local acquisition/trust repairs preserve its existing environment and
human-owned baseline contract; they add no new authority or lifecycle decision.
