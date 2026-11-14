# Source-campaign documentation and deferred qualification

This is the bounded documentation draft for
[#83](https://github.com/egohygiene/identity/issues/83), not its final closure.
Main remains `19d3d16bd149ddb61a03924a2b688e8e689af68b`. The draft stack is:

| Draft | Exact product source checkpoint | Result |
| --- | --- | --- |
| [PR138 / #133](https://github.com/egohygiene/identity/pull/138) | `ad28ab4f99d5e6a09b7e02536cf3e788347eb4b2` | Initializer source compiles; behavior/acceptance unrun |
| [PR139 / #98](https://github.com/egohygiene/identity/pull/139) | `413aae01f53205312cdba4fdae60222f9f16d605` | Native publisher source parses; no round-trip or publication proof |

The containing documentation commit has its own source revision; it must be
read from the PR/provider instead of inventing a self-hash. The stack is for
review continuity and does not alter issue prerequisites. No PR is merged.

## Exact evidence and its limits

| Command/inspection | Revision/platform | Outcome and limits |
| --- | --- | --- |
| `bash scripts/dev-env.sh setup` | main 19d3d16, Linux x86_64; Node 24.19.0 / Python 3.12.14 | Passed; Rust 1.97.1, pnpm 11.21.0, embedded-validator drift guard and CLI/reference build. Source/locks unchanged. |
| `bash scripts/dev-env.sh browsers` | Same base/host | Passed downloads of Chromium/Headless Shell 151.0.7922.34 revision1234 and FFmpeg 1011; host fonts/browser behavior unqualified. |
| Git fetch/main lookup, authenticated GitHub user/repo reads | Same managed session | Passed using injected authentication. No credential values inspected. |
| Managed Docker socket info | Same host | Passed with execution permission; first sandbox-only attempt denied. No image/container/browser qualification run. |
| Root `corepack pnpm --version` probe | Same host | Failed unpinned default lookup under sandbox networking; corrected renderer-directory probe passed 11.21.0. No preset/policy change. |
| Initializer AST/new-schema JSON parsing, bounded rustfmt and `cargo build --locked --offline` | PR138 source above, Linux x86_64 | Passed syntax/build evidence only; initializer never executed. |
| Publication Python AST, changed JS `node --check`, JSON/YAML and whitespace | PR139 source above | Passed syntax/static evidence only; publisher/source-validator paths never executed. |
| `bash scripts/dev-env.sh build` | Documentation checkpoint `d7a2be8d264c51d550722a2c20f1cd8d6700a469`, Linux x86_64 | Passed standalone-bundle drift guard, CLI build and reference-fixture render/Vite build of the combined source stack; no initializer/native publisher path or test suite executed. |
| Pinned continuity metadata JSON Schema, twelve headings and size | Draft source stack | Structural evidence only; official native owner-domain conformance remains unrun. |
| Byte/source preservation | Draft stack versus main 19d3d16 | All original roadmap machine blocks, original ADR files/dispositions, 43 inventoried source/package files, legacy release config/index and approved PNG preserved; candidate master copies match. |

At `2026-11-05T06:07:32Z`, a fresh HTTPS `site.json` observation still selected
`v1.0.0` at `aaad8839104704cf57bfa846539b3b875421e03d`, inventory digest
`b757ea1a341638098b9b0ef28bb3be035838f33cc996820e133f9551a18f4d79`.
This is a manifest-binding observation, not full live-byte verification,
deployment or rollback proof. The documentation checkpoint also had zero
Actions runs when queried. [PR140](https://github.com/egohygiene/identity/pull/140)
retains the final documentation handoff.

No regression, unit/integration, Clippy, browser/AX/visual, native platform,
consumer upgrade, release/deployment or hosted CI qualification ran. No check
is silently skipped to pass acceptance. Required unrun evidence remains a gate.
The qualified revision is **none**. Artifact hashes for unbuilt kits/releases
are **not available**, not placeholders or old receipts.

## Later campaign matrix

Keep original issue dependencies and run appropriate checks after each repair.
Qualify the exact resulting source at the end; a previous pass cannot qualify
newer source merely because it is nearby in history.

| Work | Required later evidence | Current outcome |
| --- | --- | --- |
| #80 | Actual Linux/amd64 authoring-host Docker and matching CI browser profile; exact fonts/settings/source, every current positive case, deliberate visual failure and restored pass | Unrun; browser installation and daemon health are insufficient |
| #84 | Fresh historical owner/branch disposition, retired writers absent, retained triggers/permissions and read-only docs validation | Source already merged; acceptance unrun |
| #85 → #86 | Standalone drift, CLI/import/diagnostic ordering, authority/digest/embedded consumer cases; exact projection bytes/public-review/path/failure and cross-language vectors | Source already merged; acceptance unrun |
| #87 / #88 | Original bounded Rust and renderer extractions; approvals, adapter verification, deterministic/incremental output, confinement, serialization/recovery, public/audience/release/path and static/download/keyboard/AX/visual cases | Refactors deferred; preserve original prerequisites |
| #133 | All seven original criteria and absent/v0/v1/repeat/unsafe/conflict/invalid/missing-fact/failure-preservation/completed-source/copied-binary cases | Draft only; no criterion closed |
| #82 | Standalone/Make/Task/Docker setup, repeat/frozen versions/cache ownership/dispatch and deliberate helper/version fault; bounded clean base | CI/runtime acceptance unrun; #80 remains prerequisite |
| #83 | Docs/link/publication architecture and current final interfaces, recovery/public/download and source/release/deployment distinctions | Source docs prepared; final tested-source reconciliation unrun |
| #70 | Full pinned lint/format, Rust/Python/renderer/schema/contract/provenance and clean-room/determinism checks; source-install Linux/macOS/Windows release matrix and actual architectures | Unrun on these drafts |
| #106 / #107 under #70 | Existing launch positive/negative source/package regressions; real Kern alt text, minimum widths, attribution, keyboard/focus, narrow layout, rights/download bytes and reduced motion | Historical source/package receipts retained; new qualification unrun |
| #98 | Actual owner-complete root source, native/publisher integration, semver/artifacts/SBOM/licenses/provenance, quickstart, self-dogfood, live/rollback and contrasting-consumer upgrade/drift/rollback | Owner facts, qualification and approvals pending |
| #116 | Reconcile all original and necessary bounded work, #133 and both parents, no unmerged completion PR; fresh issue query | Keep open and close last |

Use the existing release matrix (`ubuntu-24.04`, `macos-15`, `windows-2025`)
and qualified `linux/amd64` browser image; record actual runtime architectures
and any unavailable runner evidence. `task check`/the shared helper does not
cover every integrity, native-platform, browser, release or publication gate.
Run the existing owner-pinned advisory checks without converting incomplete
domain coverage into conformance or accepting ADRs automatically.

Investigate the retained Linux `ExecutableFileBusy`/OS-error26 first attempt
from [CLI run 39472257919](https://github.com/egohygiene/identity/actions/runs/39472257919),
job 118799319728, source 5502106f301ed69c62396ccf4033342078412a46.
The historical retry supplied no diagnosis. Preserve failed evidence and
qualify the actual repair if one is required.

## Publication, owner review and rollback

The [single owner packet](../98/OWNER_PACKET.md) owns missing rights/creative
facts, proposed version/artifacts, destinations, consumer-owner actions and
precise future approvals. Existing main renderer/publication/ADR-path merges
can deploy Pages without a reviewer, so the draft stack stays unmerged.

The standalone Brand Kit, Decisions composition and independent organization
`/identity/` composite retain separate source/release/deployment/rollback
bindings. Select and retain the actual previous verified bytes before an
approved rollout, then prove live content and exercised restoration. A newly
published stable Identity release also triggers Pages: release approval must
explicitly account for that coupled deployment. No other repository changed.
No paid execution, release, deployment or environment snapshot was requested.

## IDN-Q06

Disposition: **planned, unissued future scope; not implemented or qualified**.
Preserve `issues: []`, existing ID/dependency and both unchecked exits.

| Existing overlap | What it does not establish |
| --- | --- |
| Typed color/typography/motion tokens and native token exports | A dedicated roadmap profile with governed mappings for complete/active/ready/blocked/planned/deferred states |
| Reference-renderer focus styles, status labels and reduced-motion behavior | A selected quest-line consumer with non-color state distinctions and reviewed icon/motion semantics |
| Existing contrast/determinism/visual checks | Current-source proof for a separately versioned roadmap package and its actual consumer |

Targeted source inventory found Q06's roadmap/docs references but no dedicated
profile or quest-line implementation in this repository's renderer/contracts/
profiles/Rust source. No concrete consumer was selected in this campaign.
Retain it for a future bounded owner selection; invent no issue number and add
no component library, renderer project or ecosystem rollout to resolve it.

## Decision impact

Reference the existing source, recovery and publication contracts plus proposed
ADR-0033/0034 for the new draft interfaces. No additional ADR is required for
this documentation: it corrects capability wording and records actual evidence
and deferred scope without adopting new runtime authority. Original ADR bytes,
human dispositions and dated receipts remain preserved. Final #83 closure
still requires its original complete acceptance and tested-source evidence.
