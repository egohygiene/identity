# Identity source and publication owner packet

Status: **unqualified source draft; no publication approval requested**.
Main baseline: `19d3d16bd149ddb61a03924a2b688e8e689af68b`.
Initializer source checkpoint: `ad28ab4f99d5e6a09b7e02536cf3e788347eb4b2`
in [draft PR138](https://github.com/egohygiene/identity/pull/138).
The #98 draft is stacked for review continuity, not a new issue dependency.

## Verified source and unresolved ownership facts

[source-inventory.json](source-inventory.json) binds actual repository bytes,
Git blobs, original source locations and existing evidence. The
[candidate](candidate/README.md) uses real Identity material and deliberately
keeps unresolved rights/creative choices outside approved records.

| Material | Existing evidence | Required owner action |
| --- | --- | --- |
| Emblem, lockup, avatars, social/browser assets and reference boards | `assets/identity/manifest.json` declares the 2026-08-22 human-selected direction; production files are generated outputs | Select exact canonical masters; supply actual creator/method/source/capture evidence, artwork license/attribution/restrictions and exact subject approvals. Software MIT does not supply those permissions. |
| Kern | Existing master, byte-bound derivative manifest, CC-BY-4.0 attribution and two explicit subject approvals in `mascot/` | Preserve existing subjects and exact variants. Confirm any new v1 mapping separately; never retarget an old approval to a new asset ID. |
| Project name/repository/tagline | Existing release-publication configuration and authored README | Confirm proposed project classification and public source selection; review any reused copy as its actual governed subject. |
| Colors and typography | Current manifest palette and publication tokens, including existing Inter/system fallbacks | Select the actual organization-default snapshot, product layer and exact intended token/font facts. No organization defaults or font redistribution rights are inferred. |
| Public short/long descriptions and usage | Existing authored material and declared legacy guidance | Supply/select exact public copy, usage, legal and accessibility records with real matching decisions. The candidate contains proposals, not approvals. |

The native Rust consumer currently rejects non-SVG provenance assets, including
otherwise source-valid PNG/font records. Kern's independently governed package
exists, but adding its PNG as a native root provenance asset is not proven to
work. Keep this capability limit visible; do not strip rights, rename a PNG to
SVG, invent a new master or add a new imagery engine to evade it.

## Candidate, release and artifact ledger

Proposed version: **v1.1.0**, subject to compatibility/qualification review.
No tag or package-version bump is made here. The exact release commit is
**not selected**; neither main nor these unqualified drafts are release-ready.

| Artifact/evidence | Current disposition |
| --- | --- |
| Source/rights inventory and manually prepared v1 candidate | Reviewable files in this draft; candidate is incomplete and not canonical root source |
| Native-v1 publisher adapter | Draft source in [PR139](https://github.com/egohygiene/identity/pull/139); syntax/static checks only, no runtime pass |
| Generated self Brand Kit, publication ZIP/manifest/checksums | Unrun; no candidate output or hashes fabricated |
| Release binary/archive, SPDX SBOM, dependency license inventory, attestation | Unbuilt/unrun for the proposed release |
| Complete qualification matrix and exact qualified revision | Unrun; no qualified revision |
| Live canonical Brand Kit | Fresh site.json read still selects v1.0.0 at aaad8839104704cf57bfa846539b3b875421e03d; this is not new publication evidence |
| Rollback artifact and exercised restore | Existing historical receipts are preserved; new capture/rehearsal remains unrun |

The [source-campaign checkpoint](../116/SOURCE_PREPARATION.md) records actual
base installer/build/browser-download evidence and its limits. Those results
do not qualify this source. Keep passed, failed, skipped, unavailable and unrun
distinct in the later release ledger.

The [native handoff guide](../../publication/NATIVE_V1_DRAFT.md) specifies its
release-owned configuration, immutable native inputs and separate digest
meanings. Before release, update the real package versions compatibly, choose
actual owner-approved profiles and optional projections, generate/verify them
and install the selected config into that exact release tree. The config binds
to a verified annotated-tag selection instead of fabricating its own commit.

## Publication destinations and owners

| Surface | Responsible owner and proposed action | Gate and rollback |
| --- | --- | --- |
| GitHub Identity release | Identity maintainers: approved immutable annotated stable tag and existing artifact workflow | Current-source quality, semver/artifacts/provenance, then explicit release approval; never replace tag/assets |
| identity.egohygiene.io | Identity Pages publisher: verified native release projection plus existing Decisions composition | Explicit deployment approval, prior verified capture, exact live file/manifest proof and exercised rollback |
| egohygiene.io/identity/ | Independent organization route owner: install exact reviewed Identity composite | Confirm actual route owner/action, cross-host release agreement and independent restore; no other-repository change is authorized here |
| /intelligence/decisions/ and /decisions/ | Existing Identity/Relay composition and independent ADR source pin | Preserve routes, public filtering, navigation and separate bindings; proposed ADRs remain proposed |

Current renderer/publication/ADR-path merges automatically run Pages deployment
without an environment reviewer. Keep these drafts unmerged. Review/merge
planning must account for that side effect before authorizing any merge.

## Consumer-owner handoff

Proposed contrasting consumer: Mantle main
`0f54fa6e100c5b86af64aa383e41eed8c64e363a`, with existing governed source and
closed adoption scope [Mantle #27](https://github.com/egohygiene/mantle/issues/27).
It selects core/GitHub/docs/tokens/metadata/archive and has no adopted Press Kit,
handbook or mascot. Do not add those facts merely to make the contrast larger.

Fresh immutable reads of `.github/workflows/identity.yml` and `docs/identity.md`
confirm its current compiler pin is `v1.0.0`, Linux archive SHA-256
`f8a961790b959fc683b215729c20c743399c7b1d4d8aadf8b1a30e8c3663532a`.
Its standalone validator and repository-presentation script are separately
pinned to `3c2fd3141371b355628e81f66f63159f19d63338`, with respective hashes
`eb0c7f9df31b2bd3eb618d830c5d11d76c750d0ef51b9b79092aa72ccfdcbb4f`
and `5d73593ab3e04baf60d577119defd4049cf2da571f00a9d033d7a7d9430b7396`.
The owner's future patch must update those exact acquisition URLs and hashes,
install the full matching runtime/script dependency set, and update the
consumer documentation together. New release hashes are not invented here.

After source/quality/release gates, the Mantle owner must approve changing its
immutable tool/script/profile pins, review isolated regeneration, prove CI
detects deliberate drift without repair, and restore the preceding source/pins/
generated outputs together. Retain exact consumer/release revisions and output
inventories. Its existing historical proof is not this upgrade or adoption.
Prepare the proposed patch outside that repository; obtain explicit approval
before any other-repository write.

## Remaining gates and precise future approvals

1. Rights/creative owner supplies the missing facts in the first table against
   the exact inventory/candidate subjects. This is source review, not release
   permission or ADR acceptance.
2. The separate engineering campaign completes #80/#82/#84–#88, final #83 and
   #70, plus every #133 case, against its final source. Include native install,
   clean-room, browser/fonts/AX/visual, #106/#107 and the retained OS-error26
   investigation. Missing required reviews/platform/CI evidence remains a gate.
3. Prepare the exact merged release revision, immutable artifact checksums,
   SBOM/license inventory/provenance, native/publication handoff and recoverable
   prior site/composite. Update this single packet with actual evidence.
4. Request explicit approval for the named release/tag/commit, Pages deployment
   and rollback exercise, organization-owner action, and any Mantle write.
   No paid service or runner is selected; expenditure requires separate approval.
5. Close #98 only after actual self-dogfood, release/live/rollback and consumer
   upgrade/drift/rollback proof. Reconcile #116 last after a fresh open-issue query.

IDN-Q06 remains planned, unissued future scope under #83. Foundations overlap
does not establish a dedicated quest-line token profile. No new issue, component
library, required-files policy rollout or broader fleet migration is selected.
