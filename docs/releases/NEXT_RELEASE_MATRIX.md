# Next Identity release: distribution and compatibility plan

Status: **proposed release preparation, 2026-11-22**. This records the requested
broad installability goal under [#98](https://github.com/egohygiene/identity/issues/98)
and [#116](https://github.com/egohygiene/identity/issues/116). It does not build,
qualify, publish or activate any new target or package channel.

## Existing release and version selection

The public [v1.0.0 release](https://github.com/egohygiene/identity/releases/tag/v1.0.0)
already exists. Its observed assets include a Linux x86-64 GNU archive, raw
binary, `SHA256SUMS`, SPDX SBOM and locked-dependency license inventory.
The [v1 guide](V1.md) retains that historical install and compatibility boundary.
Do not move its tag, replace its assets or represent later source as that release.

At inspected main
`afc368003bfc6a2101051229efd237c8d6fadf71`, Cargo and the renderer still declare
`1.0.0`; the [owner packet](../work/98/OWNER_PACKET.md) proposes **v1.1.0** for the
next candidate, subject to actual compatibility review. A breaking contract
change requires the appropriate higher major instead. Before release, select
the version, reconcile all version surfaces and changelog, and name one exact
reviewed commit. Neither the new version nor an immutable tag is selected here.

The current [release workflow](../../.github/workflows/release.yml) names Linux,
macOS and Windows source-check jobs, but packages only Linux x86-64 GNU.
Workflow source and historical release presence do not qualify the current
candidate or establish other prebuilt binaries.

## Completion order

1. Finish source and specification work, actual Identity self-source/rights,
   publisher integration preparation and the engineering gates under
   #70/#80/#82/#88. Prepare source-changing release repairs before the final
   qualification sweep.
2. Prepare a finite release candidate, its actual target/channel matrix,
   artifacts, install evidence, compatibility notes and rollback materials.
3. Review the concrete version/commit, immutable tag, artifact inventory and
   publication action. Exercise the qualified release path and verify the
   downloaded artifacts and independent site publication/rollback.
4. Close #98 after its actual self-dogfood, release and contrasting-consumer
   upgrade/drift/rollback proof. Reconcile and close #116 last.

Release evidence is itself part of #98/#116. Requiring zero open Identity
issues before performing their release acceptance would create a cycle.
Broad repository-policy adoption remains a separate later owner handoff.

## Proposed binary cohorts

Start with the four primary native cohorts, then expand where the actual
toolchain, dependencies and native execution evidence support it. All rows
below are **planned**, not newly supported. A cohort may remain conditional
without being disguised as a passing matrix cell.

| Wave | Target | Rust triple | Proposed archive | Candidate status |
| --- | --- | --- | --- | --- |
| Primary | Apple Silicon macOS | `aarch64-apple-darwin` | `.tar.gz` | Planned |
| Primary | Intel macOS | `x86_64-apple-darwin` | `.tar.gz` | Planned |
| Primary | Linux x86-64, GNU libc | `x86_64-unknown-linux-gnu` | `.tar.gz` | Planned; historical v1.0.0 artifact is separate |
| Primary | Windows x86-64, MSVC | `x86_64-pc-windows-msvc` | `.zip` | Planned |
| Expansion | Linux ARM64, GNU libc | `aarch64-unknown-linux-gnu` | `.tar.gz` | Conditional on build and native install proof |
| Expansion | Linux x86-64, musl | `x86_64-unknown-linux-musl` | `.tar.gz` | Conditional on linking/runtime proof |
| Expansion | Linux ARM64, musl | `aarch64-unknown-linux-musl` | `.tar.gz` | Conditional on linking and native install proof |
| Expansion | Windows ARM64, MSVC | `aarch64-pc-windows-msvc` | `.zip` | Conditional on toolchain and native execution |

Each selected row records exact minimum OS/kernel/libc and required runtime
versions. Inspect the produced ELF/Mach-O/PE and dependencies; do not infer
architecture from a runner label or declare a universal macOS/Linux minimum.
Choose the intended GNU libc baseline deliberately and test the downloaded
binary on it. Building on Ubuntu 24.04 does not prove older GNU systems work.
Cross-compilation, emulation and native execution remain distinct evidence.

A GNU binary can serve multiple distributions when its ABI and dependencies
are compatible; it does not need a differently named binary for every distro.
Qualify representative actual versions of Ubuntu LTS, Debian stable and the
selected Fedora/RHEL-compatible systems. An Alpine claim needs its own musl
and Python/runtime evidence. Package dependency names and availability remain
distribution-specific. Keep unavailable/unsupported combinations explicit.

## Runtime and installation contract

Prebuilt CLI users do not need a Rust compiler. Current v1 initialization and
source preflight do require **Python 3.11+**: the Rust binary embeds trusted
scripts and invokes an isolated interpreter. No Python packages are required
by that source-validation boundary. `IDENTITY_PYTHON` may name a trusted
interpreter; missing/unsupported Python must fail with actionable diagnostics.
An install script must not silently hide that prerequisite or install it during
validation. Verify the actual interpreter selected on every supported host.

The current locked source-build path uses the reviewed Rust toolchain and
lockfile; at the inspected revision the toolchain is `1.97.1`. Renderer and
browser development/publication tooling have their own Node/pnpm/font/browser
requirements. Do not present those as necessary for every prebuilt CLI user,
or claim the CLI includes an installed browser, Python runtime or agent skill.

Each target's clean install must exercise version/help, v0 compatibility,
explicit v1 candidate initialization, embedded source preflight, generation,
verification, drift/refusal behavior and recovery where supported. Use supplied
fixtures and real governed self-source without inventing creative approvals.
Cover spaces/Unicode, missing runtime, no-clobber/source preservation, upgrade,
uninstall and rollback. Test offline operation after explicit preparation; a
successful online source build alone does not establish offline installation.

## Channels and native packages

These are staged delivery proposals, not claims of live registry entries:

| Channel | Planned scope | Qualification and publication boundary |
| --- | --- | --- |
| GitHub release archives | Every qualified target above | Primary binary source; exact tag/commit, digest, download, extraction and clean-install proof. |
| Locked GitHub source install | Compatible source-build hosts | Preserve the existing route, actual toolchain/lockfile and runtime requirements. |
| Homebrew | Qualified macOS cohorts; Linux only if separately proved | Review formula/bottle or archive acquisition, Python dependency, checksums, install/upgrade/uninstall and actual tap availability. |
| Debian/Ubuntu `.deb` | Qualified GNU cohorts | Correct architecture, libc/Python dependency declarations, owned paths and package lifecycle tests on selected distro versions. |
| Fedora/RHEL-compatible `.rpm` | Qualified GNU cohorts | Prove actual dependency names/versions, ABI, packaging and lifecycle on the selected systems; do not infer from `.deb` success. |
| WinGet/Scoop or native Windows installer | Qualified Windows cohorts | Choose the concrete owner/channel; verify published archive/installer hashes and install/upgrade/uninstall. External catalog acceptance is separate. |
| crates.io | Separate reviewed decision | Current Cargo explicitly has `publish = false`, and the v1 guide intentionally excludes this channel. Do not enable it or claim registry installability implicitly. |
| Other distro/community packages | A real supported consumer need | Add bounded adapters and verified owners/accounts. A generated recipe is not an upstream store publication. |

Package managers should consume the same immutable qualified artifacts where
appropriate. Their availability, signing identities, permissions, fees and
account requirements must be established before publication. No paid service,
account enrollment or hosted runner is selected by this document.

## Compatibility matrix and evidence

Maintain a human-readable matrix backed by versioned machine-readable release
metadata. For each OS/architecture/libc/channel, record at least:

- exact tag, full source commit, binary target triple, minimum runtime policy,
  artifact identity and SHA-256;
- build, native execution, clean downloaded install, v1/runtime checks,
  upgrade/uninstall/rollback and publication results separately;
- supported source/profile/CLI versions, applicable features and known limits;
- exact test host/image, execution time and bounded evidence references;
- explicit `planned`, `passed`, `failed`, `blocked`, `not-run` or justified
  `not-applicable` evidence for each required check, plus actual channel
  publication/availability.

Only a row with complete required passing evidence and actual available
delivery may be shown as supported/green. A compiled binary, authored workflow,
skipped platform, successful checksum or source-only test cannot supply the
other cells. `not-applicable` needs a reason and does not become a pass.
Generate the README/download matrix from the same represented release data;
never hand-color the matrix to satisfy the availability goal.

## Release artifact and authenticity checklist

- Versioned per-target archives with the CLI, applicable license/notices,
  runtime prerequisites and install/upgrade guidance. Add native packages only
  for channels that passed their own gates.
- A machine-readable release manifest binding version, full source commit,
  target/ABI/runtime requirements, artifact names/digests, compatibility and
  evidence. Keep its source/profile/tool identities distinct.
- `SHA256SUMS` covering the actual selected payload, with a documented inventory
  and no self-hash cycle. Independently verify checksums after downloading.
- SPDX SBOM and locked dependency/license inventory, reflecting target-specific
  dependencies where they differ; preserve separate artwork/font permissions.
- Build provenance/attestations for the actual distributed artifacts, with an
  independent verification path binding repository, workflow and selected
  commit/tag. A checksum establishes integrity, not publisher identity.
- Record tag/signature, checksum-signature and platform signing/notarization
  status honestly. Verify the actual trusted signer/key or OIDC identity when
  supplied. Do not claim a signature, Apple notarization or Windows publisher
  identity merely because a workflow contains a signing step.
- Deterministic archive inventories and repeatable package/source-generation
  checks. Claim reproducible binary bytes only after the required independent
  rebuilds agree; repeated Brand Kit generation is narrower evidence.
- Exact release notes, migration/known-limit guidance, security/support contacts
  and an exercised recovery path. Verify that published/downloaded inventories
  match the reviewed candidate, then retain the prior immutable artifacts.

## Companion skill and owner boundaries

The companion agent workflow belongs to Aether; Identity remains authoritative
for fields, schemas, validation and CLI behavior. Record the separately released
Aether skill version/repository pin and the compatible Identity implementation.
The draft companion spec and skill are prepared in
[Aether PR #139](https://github.com/egohygiene/aether/pull/139); actual compatible
host installation, observed authoring and stable publication remain unqualified.
Installing agent instructions with `gh skill` does not install the Rust binary
or Python runtime. Neither skill availability nor source merge qualifies a
binary cohort or public release.

The existing [release process](RELEASE_PROCESS.md),
[accepted immutable-release decision](../decisions/ADR-0019-immutable-release-contract.md)
and [owner packet](../work/98/OWNER_PACKET.md) retain tag, review, publication,
site and rollback boundaries. This plan prepares the requested broader scope
without modifying workflows, package versions, release tags or release assets.
