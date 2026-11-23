# Identity and Aether finishing sprint — 2026-11-23

The six preceding drafts are merged. The next five checkpoints are separate
drafts for review. No new issue, tag, release, deployment or hosted workflow
dispatch was created. Identity still has six open issues: #70, #80, #82, #88,
#98 and #116. Evidence below keeps its actual represented source; merging or
integrating later documentation does not relabel an earlier execution.

## Merged baseline and draft order

| Repository | Completed merge order | Verified main |
| --- | --- | --- |
| Identity | #163 → #164 → #165 → #166 | `ad8fca58946ca03f6f07d13be6c64046216569d0` |
| Aether | #141 → #142 | `dc3549c8a23bed5fb551a458a22605e7e0777822` |

Review and merge parents before children. The two repository stacks are
independent; do not manufacture a cross-repository merge dependency.

| Stack | Checkpoint | Review reference |
| --- | --- | --- |
| Identity 1 | Enforce the already-declared source timestamp contract | [Draft #167](https://github.com/egohygiene/identity/pull/167) |
| Identity 2 | Actual local source-candidate download, installation and rollback | [Draft #168](https://github.com/egohygiene/identity/pull/168) |
| Identity 3 | Complete original local workflow with verified artifact delivery | [This draft branch](https://github.com/egohygiene/identity/tree/codex/80-artifact-stack-20261123) |
| Aether 1 | Portable architecture governing resources | [Draft #143](https://github.com/egohygiene/aether/pull/143) |
| Aether 2 | Portable audit resources and combined default-pilot qualification | [Draft #144](https://github.com/egohygiene/aether/pull/144) |

## What is proved

- Timestamp code `d159c680e6161e85854fd45c255d4196aec5c34f` passes 119
  native Rust checks, with four explicit helper-only ignores, formatting and
  strict Clippy. Python validation now consistently checks declared source
  timestamps; date-only lifecycle/release fields and existing publisher
  string contracts are preserved. No source timestamp or approval was invented.
  See the [timestamp record](../70/timestamp-consistency-20261123/VALIDATION.md).
- The [local installation proof](../70/LOCAL_INSTALL_2026-11-23.md) actually
  downloads and verifies two controlled archives, installs into fresh isolated
  prefixes and executes 17 PATH-selected commands. Pinned Mantle source remains
  unchanged. Fresh generation, three deliberate drift cases, replacement and
  rollback pass. Both binaries print 1.0.0: this is byte-bound source-candidate
  replacement, not a published semantic-version upgrade.
- The entire original reference-renderer workflow passes locally at frozen
  `5afa292c41563fe16f48f321eb5ac37459fda3dd`. Its 424 frontend tests pass.
  Each original browser entrypoint passes all nine positives, catches the
  deliberate visual mutation, then passes after restoration. The approved PNG,
  tolerance, fonts, profile, workflow and four original action pins are unchanged.
- A named optional local act derivative supplies the narrowly reviewed strict
  ZIP MIME and emitted-signature encoding compatibility. Official/global act
  remains unchanged. Independent authenticated download verifies the actual
  **4,074,757-byte ZIP and every one of its 74 default-selected files**, including
  equality with uploader and Finalize digests. No large/multiblock or hosted
  security-parity claim follows. Twenty explicit nonlog browser evidence files
  are public; hidden state omissions and private raw logs/archive are disclosed.
  See the [workflow packet](../80/LOCAL_ARTIFACT_TRANSPORT_2026-11-23.md).
- Integrated Identity leaf `3d6542845c5f669e3d0cfe3425379378e92802cc`
  passes **266 Python checks: 264 passed, two existing skips**. Platform-specific
  permission, shebang, descriptor, FIFO and symlink controls are precisely gated;
  generic protocol checks remain active. This is Linux execution, not native
  Mac/Windows qualification. Later test/docs changes preserve frozen workflow
  provenance. Root integration adds only the consolidated handoff and continuity.
  That full run covered standalone/Make; a separate final five-test entrypoint
  check passes without skips using `IDENTITY_REQUIRE_FRONTENDS=1` and actual
  Task 3.45.3. [Root checks](finish-sprint-20261123/checks.json) retain both scopes.
- Aether code `9fd9f438d08fd88a9ba2102d1205191c91afce77` passes **440
  checks: 429 passed, 11 existing skips**. Its unchanged default three-pilot CLI
  passes all five local scenarios with all 50 package files Git-bound. Normative
  obligations, historical provenance and staged source authority are retained.
  **Overall remains not-ready** because remote scenarios are skipped. See
  [Aether's combined evidence](https://github.com/egohygiene/aether/blob/9266b6cb83bc93a97d60fbafca0bff679e0fa279/docs/work/38/pilot-integration-20261123/VALIDATION.md).

The owned local runtime was removed after evidence retention. Its resource
observation recorded no OOM; shared Docker engine, images, configuration and
unrelated containers were verified unchanged. Private receipts remain durable.

## Remaining mini-roadmap

| Order | Existing owner | Concrete next checkpoint |
| --- | --- | --- |
| 1 | #80 → #82 and #88 | Review/merge the Identity draft stack, then independently reconcile these three child acceptance checklists. The actual workflow, browser, setup and extraction evidence now supports that closeout; do not close solely from a draft or call local act hosted CI. |
| 2 | #98, coordinated with #70 | Implement and verify the proposed multi-target release packaging and machine-readable compatibility/artifact data. Prepare source-changing release repairs before the final sweep; current workflow packaging is still Linux GNU only. This engineering work can proceed while the source proposal is pending. |
| 3 | #98 and #70 | Finish Identity's own canonical `.identity/` source after concrete selection, retaining real provenance, rights and approval subjects. Generate twice, prove drift/override/omission behavior, and verify advertised downloads/publisher wiring. Then complete the final candidate's native installation/runtime/recovery checks, recording actual ABI/OS limits; keep existing Linux proof separate from unexecuted Mac/Windows rows. |
| 4 | #98 and Aether #38 | Prepare and qualify finite release artifacts, compatibility data, checksums, SBOM/license inventory and provenance. Preserve historical v1.0.0. Verify actual release-backed downloads, publication and rollback, a contrasting Mantle consumer upgrade, and the companion's remote install/update/deprecation/rollback and observed agent use. Local source archives and publish dry-runs do not satisfy these release gates. |
| 5 | #116 last | Reconcile the actual remaining gates and final documentation after #70/#98 acceptance. Keep repository-wide adoption with its existing policy/consumer owners; close no umbrella tracker from source delivery alone. |

The [release compatibility plan](../../releases/NEXT_RELEASE_MATRIX.md) already
covers primary Apple Silicon/Intel macOS, Linux GNU and Windows x64 cohorts,
conditional ARM64/musl expansion and package-channel lifecycle evidence. Those
rows are planned until the produced artifacts are actually qualified. Release
acceptance belongs inside #98/#116; requiring zero open issues first would be
circular.

## The outstanding source decision, in plain language

This is about using Identity to describe **itself**, through the same `.identity/`
files a consumer project owns. Previously confirmed artwork, reviewer, copy,
voice, principles and logo-use terms remain recorded. The concrete
[source proposal](../98/source-assembly/README.md) still needs selection of its
local token/inheritance option, newly proposed logo descriptions/spacing/sizing,
and initial output/download selection. No response asking for clarification
selects that packet or supplies a new human review timestamp. Engineering can
continue independently. The selected source still has no canonical root
`.identity/`; the assembled candidates remain review material under `docs/`.

## Decision and evidence boundaries

Reference Identity ADR-0005/0012 for declared source validation and ADR-0011/0019
for visual and immutable-release boundaries. Routine test/evidence/handoff work
requires no new ADR. Aether retains its scoped existing ADRs and AET-Q01/AET-Q05
roadmap references. No automated lifecycle, creative, accessibility, release or
organization-wide token approval is implied. Earlier dated records remain
historical rather than silently rewritten as current proof.
