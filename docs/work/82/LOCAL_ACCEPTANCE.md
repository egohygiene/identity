# Portable entry point coverage — 2026-11-14

Base: `376232249209f3304843795f6113baf7dd504019`.
The actual shared helper is exercised through standalone Bash, Make and
checksum-pinned Task 3.45.3; no frontend reimplements setup policy.

## Actual checks

- Five protocol tests pass with both real frontends required. Each runs the
  actual helper in a disposable consumer using synthetic external tools.
  They assert repeated setup, frozen Cargo/pnpm arguments, activation and
  owned cache bindings, browser argument forwarding, unchanged consumer files,
  and rejection of a deliberately wrong pnpm version and unknown operation.
- Real `bash scripts/dev-env.sh setup` and `make setup` both pass with the
  pinned Rust 1.97.1/pnpm 11.21.0 tools, frozen dependencies and shared caches.
  Real `task browsers -- --dry-run` then passes without a TTY, reinstall or
  browser download. Source/lockfiles and unrelated files remain unchanged.
- The Task installer downloads only its exact official v3.45.3 Linux/amd64
  archive, verifies SHA-256
  `2c39d989ba8ab6ed37c025e9094e37240360fa2d69158504fc7a7486c88dc26f`,
  extracts the executable into the explicitly selected check-tools directory,
  and reports version 3.45.3. Its download is bounded to sixty seconds.
- Bash syntax, documentation and extraction/provenance checks pass.

## Demonstrated repairs

The helper now checks the activated pnpm version before dependencies/builds.
The injected `999.0.0` activation is rejected through all three frontends.

An actual Task invocation exposed pnpm 11's configuration-prefix and CI/global
virtual-store default differences: prepared dependencies attempted an implicit
reinstall and failed without a TTY. The helper now exports its owned store
using `pnpm_config_store_dir`, defaults global virtual store to false in both
contexts, and defaults dependency drift to an explicit error. Existing explicit
environment overrides remain supported. After these repairs, repeated real
setup and the ordinary non-CI Task dry run pass.

## Remaining acceptance

The normal validation workflow now installs the exact check-only Task binary
and requires actual Make/Task coverage in the existing Python test step.
No hosted workflow was dispatched. Current-source clean-base Docker and CI
execution remain for the requested later `act` campaign, alongside #80's CI
gate. #82 stays open; the implementation and local evidence do not claim that
remaining acceptance.

ADR not required: cover and repair the existing portable helper's version,
cache and dispatch behavior without changing product/source authority.

## Current-source local workflow checkpoint — 2026-11-22

Base: `ec8fce30c3c96c7781238eb0a8899d6f0cee0a40`. The new independent
`portable-entrypoints` job in the development-image workflow passed under
`act` 0.2.97 on native Linux/amd64. Its exact executed inputs, immutable cached
runner image/config, local substitutions and results are recorded in the
[portable workflow receipt](qualification-2026-11-22/portable-entrypoints.json)
and [sanitized process log](qualification-2026-11-22/portable-entrypoints-act.log).

The fresh container downloaded the actual official Task 3.45.3 archive,
verified its pinned SHA-256, installed it through the existing installer, and
passed all five tests in 2.181 seconds. Actual Bash, Make and Task invoke the
real helper against synthetic external-tool protocols. Repeated setup,
frozen dependency arguments, owned cache bindings, browser argument forwarding,
source preservation, deliberately wrong pnpm activation and unknown dispatch
are covered. This job does not download real Rust/pnpm dependencies or build
the application. The earlier real setup evidence above remains historical.

The container used the existing cached `catthehacker` runner digest, 2 CPUs,
1 GiB memory and no Docker socket. It mounted the public host CA read-only and
forwarded required proxy values without retaining them; TLS verification stayed
enabled. Exact pinned public action archives supplied local action mirrors after
`act`'s own clone failed. A disposable standalone checkout avoided `act`'s
unsupported worktree-config parsing. The main hardening step was skipped in
local emulation; its self-hosted pre-step is not hosted-runner hardening proof.
The log's emulated run 1 is not a GitHub Actions run.

## Docker storage boundary and remaining acceptance

A concurrent browser qualification attempt demonstrated that the shared VFS
Docker store could exhaust over 8 GiB before the first image-build setup step.
The original default/custom development-image gate remains unchanged. Rather
than repeat that known resource failure, the development qualifier now checks
the Docker data filesystem before pull/build, records its driver/free space,
and stops with a failed receipt when its reserve cannot be met or observed.
The documented local estimates are 24 GiB for VFS and 8 GiB for other drivers;
they are not a guarantee of sufficient capacity. Measured runners may select
another reserve; remote/inaccessible stores require independent measurement
before the explicit zero-reserve bypass.

The [actual storage refusal](qualification-2026-11-22/development-image-storage-refusal.json)
records insufficient VFS capacity and only Docker version/info/context reads,
with no pull/build. Seven qualifier boundary tests pass, including an injected
insufficient-storage run that must retain failure evidence without Docker
mutation, plus exact thresholds, remote unknowns and explicit bypass.

The standalone/Make/Task workflow checkpoint is complete locally. Full
current-source pinned default and non-root custom image qualification remains
pending on a sufficiently provisioned Docker host; cold tool/dependency
acquisition, that image's cache-user/runtime/TLS checks, browser qualification
and hosted execution are not supplied by the narrow job. **#82 stays open.**

ADR not required: add execution coverage and a measured-resource refusal to
the existing setup/qualification boundary without changing identity semantics,
source authority, supported release platforms or approval disposition. Pinned
Aether decision guidance was loaded with `git show` at
`dc8a16851f452763ef4f7fbe4bf057d4500b1921` and the existing Hygiene policy pin
`a05b14f8b9e2772124f879f818e09a911e996ad8` was retained.
