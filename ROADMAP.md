---
schema: aether.architecture-document/v1
id: identity-roadmap
title: Identity Roadmap
kind: architecture-document
version: 1.1.0
status: active
owners:
  - egohygiene
created: 2026-08-19
updated: 2026-10-18
governed_by:
  - architecture-roadmap
depends_on:
  - identity-vision
  - identity-pillars
  - identity-architecture
  - identity-decisions
related:
  - identity-purpose
  - identity-principles
  - identity-manifesto
  - identity-epistemology
supersedes: []
---

# Identity Roadmap

<!-- BEGIN ROADMAP EXECUTION SNAPSHOT -->
<!-- roadmap-manifest
schema: hygiene.roadmap/v1alpha1
repository: egohygiene/identity
visibility: public
publication: central
route: /roadmap/identity/
updated: 2026-10-18
-->
## 2026-10-18 execution snapshot

The original execution snapshot reviewed [`55d0339ba5518c7b72154a2aad54a9e5b2bf2fff`](https://github.com/egohygiene/identity/commit/55d0339ba5518c7b72154a2aad54a9e5b2bf2fff), with live issues and publication evidence rechecked on 2026-10-18 UTC. The scoped #99 field audit reviews [`063a4c70fcaccc6c15393f28ac2aabe62b34e1e7`](https://github.com/egohygiene/identity/commit/063a4c70fcaccc6c15393f28ac2aabe62b34e1e7); its findings and later checkpoint evidence are qualified below. A collector timestamp does not renew source-review freshness. Repository Markdown owns intent; generated views remain projections.

**Lifecycle:** `v1.0.0` is published. Current main includes later features and repairs; it is not a new stable release.
**Current gate:** #74/#75/#76 merged in PRs #111/#112/#113 (IDN-Q13–15). Review #99 checkpoint 1's field catalog and observed gaps before selecting compatible contract changes (IDN-Q29). #78 remains ready; its implementation is paused while this selected contract checkpoint is reviewed.
**North-star outcome:** A usable, governed Brand Kit proven against Identity's own approved source and a contrasting consumer, followed by repeatable repository adoption.

The original snapshot mapped 28 open issues. #74/#75/#76 are now closed, leaving 25: twelve audit work items (#77–#88), eleven Brand Kit children (#99–#109), and trackers #70/#98. #71–#73 merged through [PR #89](https://github.com/egohygiene/identity/pull/89); the scoped #99 review records a generic-asset selection gap that needs additional public-boundary proof. Merged repairs are not retroactively contents of `v1.0.0`. [#83](https://github.com/egohygiene/identity/issues/83) retains its final #76/#77 reconciliation gate.

### Visual roadmap publication

**Declared mode:** `central`

**Declared route:** `/roadmap/identity/`

These are roadmap publication intent, not evidence that the central roadmap route is deployed. The independently published Brand Kit at `identity.egohygiene.io` and its existing Decisions subtree retain their own single publisher. The organization `egohygiene.io/identity/` composite remains a separately gated artifact. [ARCHITECTURE.md](ARCHITECTURE.md#public-route-boundary) records the source, route, validation, and rollback matrix.

### Execution checkpoints

| Order | Work | Exit |
| --- | --- | --- |
| 0 | #83 early pass (IDN-Q09) | Current roadmap, capability summaries, continuity, and publication boundaries agree. |
| 1 | #99 checkpoints 1 → 2 → 3 | Review the field/coverage catalog, implement only agreed compatible gaps, then demonstrate guided consumer authoring. Review each checkpoint before starting the next. |
| 2 | #78 → #79 → #77 | Transaction confinement, writer and recovery behavior have actual regression evidence; #74/#75/#76 are already merged. |
| 3 | #81 → #80 → #82 → #84 → finish #83 | Qualified setup/browser environments and accurate final contract documentation. |
| 4 | #100 → #103 → #101 → #102 → #104 → #105 | A useful complete kit for a real consumer, including the field audit's generic-public-asset and advertised-download gaps; maintenance extraction is not a blanket gate. |
| 5 | #85 → #86 → #87 → #88 → close #70 | Smaller modules preserve the repaired invariants and first-kit behavior. |
| 6 | #109 → #108 → #106 → #107 | Reviewed ownership and bounded optional use cases or explicit owner dispositions. |
| 7 | Final self-dogfood, release, and canary upgrade → close #98 | Repeatable adoption is supported by current artifacts and consumer evidence. |

The sequence expresses priority. Machine-readable `depends_on` fields express required prerequisites, including the repaired input boundaries exercised by kit downloads and optional design guidance. Independent ready work can be selected deliberately without changing ownership. `planned` optional steps still require a concrete use case or scope decision.

### Cross-repository coordination

| Capability | Current relationship | Effect on this plan |
| --- | --- | --- |
| Aether social facts and campaign handoff | [Aether #52](https://github.com/egohygiene/aether/issues/52) and [#53](https://github.com/egohygiene/aether/issues/53) are closed; Identity already has pinned social-surface projections. | Reuse the appropriate immutable contract for #104/#106. No new platform matrix or publishing authority. |
| Existing consumer proof | [Empathy PR #77](https://github.com/egohygiene/empathy/pull/77), [OptiFlow PR #46](https://github.com/egohygiene/optiflow/pull/46), and [Mantle #27](https://github.com/egohygiene/mantle/issues/27) provide existing adoption evidence. | Use an existing consumer as a bounded upgrade canary; completion of unrelated consumer work is not required. |
| Realm-managed installation | [Realm #19](https://github.com/egohygiene/realm/issues/19) remains open and owns distribution-channel consumption. | Conditional for that #108 integration; current standalone installation does not wait for Realm consolidation. |
| Demo capture | [Relay #8](https://github.com/egohygiene/relay/issues/8) remains open and owns capture execution. | Conditional only if #107 selects new automated captures; Identity retains motion-policy ownership. |
| Components and templates | [Holon #4](https://github.com/egohygiene/holon/issues/4) is closed; optional [Holon #37](https://github.com/egohygiene/holon/issues/37) remains open. | #109 decides scope without requiring a component library or daisyUI adoption. |
| Accounts and channels | [Website #12](https://github.com/egohygiene/egohygiene.io/issues/12) owns real account verification. | Use verified existing channels or omit them; #103/#104 do not require creating social accounts. |
| Contribution enforcement | #108 reports queued Relay DCO work, but no matching issue or current path was found in this review. | Keep the reference unresolved until located; do not create a duplicate DCO action. |
| Intelligence and publication | Identity #69 is closed; [Pace #5](https://github.com/egohygiene/pace/issues/5) and [organization #30](https://github.com/egohygiene/.github/issues/30) coordinate reviewed follow-up. | Read-only authorized collection can proceed beside #70. The verified Decisions canary does not authorize new hosts or fleet rollout. |

No unresolved sibling issue identified above blocks the core stabilization or first usable kit. New organization `/identity/` installation still needs its route owner's accepted artifact, qualifying stable release, and deployment/live evidence.

### Quest line

<!-- roadmap-step
id: IDN-Q01
status: complete
depends_on: []
issues: []
-->
#### IDN-Q01 — Establish deterministic brand compilation

**State:** `complete`
**Depends on:** None

**Outcome:** A compiler and nine profiles generate validated brand artifacts.

**Exit criteria:**

- [x] All declared profiles compile deterministically.
- [x] Quality checks are green.

**Current evidence:**

- The audit observed a working compiler, nine profiles, and green quality checks.

<!-- roadmap-step
id: IDN-Q02
status: complete
depends_on: [IDN-Q01]
issues: [8, 13]
-->
#### IDN-Q02 — Complete voice and approval evidence

**State:** `complete`
**Depends on:** `IDN-Q01`

**Outcome:** Brand decisions include approved voice guidance and evidence rather than generated assets alone.

**Exit criteria:**

- [x] Issue #13 provides governed voice, usage, approval, and deterministic projection evidence.
- [x] Issue #8 completes Empathy's immutable consumer transition.
- [x] Approvals link to exact reviewed subjects, provenance, and lifecycle decisions.

**Current evidence:**

- Issue #13 is implemented through versioned guidance contracts, approval-aware validation, context retrieval, and deterministic JSON/Markdown/HTML projections.
- Identity's independent extraction and Empathy's immutable consumer transition
  are complete.

<!-- roadmap-step
id: IDN-Q03
status: complete
depends_on: [IDN-Q02]
issues: [14, 15]
-->
#### IDN-Q03 — Build the renderer and studio

**State:** `complete`
**Depends on:** `IDN-Q02`

**Outcome:** Issues #14 and #15 provide a usable way to inspect and generate the Brand Kit.

**Exit criteria:**

- [x] The renderer covers all nine profiles.
- [x] Studio changes round-trip through governed source files.

**Current evidence:**

- Issues #14 and #15 provide the static renderer, safe studio contract, and
  browser evidence. They do not deploy the public website route.

<!-- roadmap-step
id: IDN-Q04
status: complete
depends_on: [IDN-Q03]
issues: [16]
-->
#### IDN-Q04 — Publish the public identity route

**State:** `complete`
**Depends on:** `IDN-Q03`

**Outcome:** Issue #16 exposes an accessible, version-aware identity surface.

**Exit criteria:**

- [x] The public route is deployed through the release-backed Pages publisher.
- [x] Generated assets link back to source and release evidence.

**Current evidence:**

- Issue #16 implemented the public route.
- `identity.egohygiene.io` serves the release-backed Brand Kit over HTTPS; the
  separate organization-portal route retains its own deployment authority.

<!-- roadmap-step
id: IDN-Q05
status: complete
depends_on: [IDN-Q03]
issues: [17, 18]
-->
#### IDN-Q05 — Pilot and release Brand Kit v1

**State:** `complete`
**Depends on:** `IDN-Q03`

**Outcome:** Real consumers validate the kit before a stable v1 release.

**Exit criteria:**

- [x] Issue #17 records representative pilots and fixes.
- [x] Issue #18 closed with the tagged, provenance-rich `v1.0.0` release.

**Current evidence:**

- Merged [Empathy PR #77](https://github.com/egohygiene/empathy/pull/77) (`308d1354e77d314bb17ba84cce8008bd1f040289`) and [OptiFlow PR #46](https://github.com/egohygiene/optiflow/pull/46) (`4866089b58efd7d57f743a4cf9af8dc8c39347b6`) prove distinct immutable consumer integrations.
- `v1.0.0` passed the cross-platform, browser, provenance, SBOM, checksum, and
  automated GitHub publication gates and is published as the stable source for
  the first public Brand Kit deployment. The [#18 release closeout](https://github.com/egohygiene/identity/issues/18#issuecomment-5448834860) records source-install, clean-room, archive, checksum, SBOM, and provenance evidence separately from #16's Pages deployment.

<!-- roadmap-step
id: IDN-Q06
status: planned
depends_on: [IDN-Q02]
issues: []
-->
#### IDN-Q06 — Publish the roadmap visual token profile

**State:** `planned`  
**Depends on:** `IDN-Q02`

**Outcome:** The quest-line renderer consumes a versioned Identity profile for color, typography, motion, icons, focus, and reduced-motion behavior.

**Exit criteria:**

- [ ] Complete, active, ready, blocked, planned, and deferred states remain distinguishable without color alone.
- [ ] The token package passes contrast, reduced-motion, and deterministic compilation checks.

**Current evidence:**

- The dedicated roadmap visual token profile is not yet published and has no linked issue. Preserve this planned step; #99 inventories overlap with existing foundations and #104's concrete target selection without silently claiming completion or making it a first-kit prerequisite.

<!-- roadmap-step
id: IDN-Q07
status: complete
depends_on: [IDN-Q02]
issues: [50]
-->
#### IDN-Q07 — Establish the mascot and character system

**State:** `complete`
**Depends on:** `IDN-Q02`

**Outcome:** Identity has one human-approved, rights-aware mascot whose source,
meaning, responsive variants, accessibility, motion limits, and public package
are reusable without transferring creative authority to a renderer.

**Exit criteria:**

- [x] Issue #50 records the selected character and exact human approval evidence.
- [x] Canonical art and full, portrait, and icon variants are content-addressed and licensed.
- [x] Consumer source and package schemas fail closed on ungoverned mascot declarations.
- [x] The public Brand Kit can preview raster variants without embedding binary bytes as text.

**Current evidence:**

- Kern's approved character source binds exactly three glowing eyes, an
  outfit-integrated identity kernel, prohibited elements, and authored meaning.
- Standard-library verification checks approval, provenance, license, digests,
  dimensions, PNG structure, and real RGBA transparency offline.

<!-- roadmap-step
id: IDN-Q08
status: complete
depends_on: [IDN-Q07]
issues: [56, 57]
-->
#### IDN-Q08 — Dogfood the public Identity experience

**State:** `complete`
**Depends on:** `IDN-Q07`

**Outcome:** Identity builds a reviewed `/identity/` candidate composite through
pinned LaunchKit and Zensical profiles while the immutable Brand Kit retains
its independent publication and rollback boundary. This step's completion is
the bounded artifact implementation, not production installation.

**Exit criteria:**

- [x] Issue #56 assigns every landing, docs, manifest, download, and redirect
  route to one owner through an accepted ADR and offline-verified contract.
- [x] Framework adapters consume reviewed Identity outputs without becoming a
  second source of tokens, assets, mascot facts, provenance, or approvals.
- [x] Issue #57 builds, previews, verifies, and hands off one content-addressed
  `/identity/` composite with accessibility and release-binding evidence.

**Current evidence:**

- ADR-017 preserves the existing `identity.egohygiene.io` release publisher
  and defines `egohygiene.io/identity/` as a separate reviewed artifact.
- Holon's merged LaunchKit, Zensical, and site-suite profiles are exact-pinned;
  Identity #57 delivered only the bounded `/identity/` consumer extension and
  proof without transferring deployment authority. Its configured `v1.1.0` candidate binding is not a published stable release; organization installation and live release agreement remain unverified.

### Early current-state reconciliation

<!-- roadmap-step
id: IDN-Q09
status: complete
depends_on: []
issues: [83]
-->
#### IDN-Q09 — Reconcile current roadmap and capability evidence

**Outcome:** Current architecture, capability, publication, and roadmap summaries agree with reviewed source and live evidence.

**Exit criteria:**

- [x] PR #110 merged the bounded documentation reconciliation; #83 remains open for its final recovery/download checkpoint.

**Evidence and scope:** [#83](https://github.com/egohygiene/identity/issues/83), [PR #110](https://github.com/egohygiene/identity/pull/110), merged at `6e19b186c8cb4d3816d0970b8f73b613d96786e2`. This early pass is independent of #76/#77; their final wording belongs to IDN-Q22.

### Stabilization and invariant-preserving cleanup

<!-- roadmap-step
id: IDN-Q10
status: complete
depends_on: []
issues: [71]
-->
#### IDN-Q10 — Preserve public and review guidance isolation

**Outcome:** Public Rust projections exclude internal/unapproved records while review projections retain governed history.

**Exit criteria:**

- [x] PR #89 merged the boundary repair and regression coverage.

**Evidence and scope:** [#71](https://github.com/egohygiene/identity/issues/71). Merged at 8aae2c6767d07714ea16bf0ea493e1f1ac399b6e; not a claim of a later stable release.

<!-- roadmap-step
id: IDN-Q11
status: complete
depends_on: []
issues: [72]
-->
#### IDN-Q11 — Enforce complete v1 source preflight

**Outcome:** CLI and library execution enforce authoritative schema, approval, digest, and path validation.

**Exit criteria:**

- [x] PR #89 merged embedded preflight and source-freshness checks.

**Evidence and scope:** [#72](https://github.com/egohygiene/identity/issues/72). The current execution path requires Python 3.11+; older releases retain their own behavior.

<!-- roadmap-step
id: IDN-Q12
status: complete
depends_on: []
issues: [73]
-->
#### IDN-Q12 — Constrain recovery journal authority

**Outcome:** Recovery cannot derive mutation authority from an untrusted journal destination.

**Exit criteria:**

- [x] PR #89 merged independent output-root authority and journal preflight regressions.

**Evidence and scope:** [#73](https://github.com/egohygiene/identity/issues/73). Legacy v1 journals fail closed; do not relabel or discard recovery evidence.

<!-- roadmap-step
id: IDN-Q13
status: complete
depends_on: [IDN-Q11]
issues: [74]
-->
#### IDN-Q13 — Unify canonical source digests

**Outcome:** Rust and Python identify the same canonical consumer source.

**Exit criteria:**

- [x] Shared inventory/digest vectors pass and the release-binding transition is explicitly documented in merged PR #111.

**Evidence and scope:** [#74](https://github.com/egohygiene/identity/issues/74), [PR #111](https://github.com/egohygiene/identity/pull/111), merged at `644294e11fdcf1dde24937790bc42cc028cb099a`. Shared Rust/Python vectors and Linux/macOS/Windows release gates pass. [Digest semantics and migration](docs/contracts/SOURCE_DIGEST_V1.md) preserve historical release identities and offline operation; ADR-023 remains proposed.

<!-- roadmap-step
id: IDN-Q14
status: complete
depends_on: [IDN-Q13]
issues: [75]
-->
#### IDN-Q14 — Bind optional guidance to its release

**Outcome:** The displayed kit and optional design-system context/handbook share a compatible source identity.

**Exit criteria:**

- [x] Matching inputs render/download and wrong-project, stale, malformed, or mixed-release inputs fail.

**Evidence and scope:** [#75](https://github.com/egohygiene/identity/issues/75), [PR #112](https://github.com/egohygiene/identity/pull/112), merged at `69d55c1caaa5b3959ed2ffdbbcd1fd69357d87dc`. Exact source-binding guards, all 72 renderer tests, six hosted browser checks and cross-platform release gates pass. Use IDN-Q13's compatibility transition instead of silently changing old bindings.

<!-- roadmap-step
id: IDN-Q15
status: complete
depends_on: []
issues: [76]
-->
#### IDN-Q15 — Validate download paths and configured bases

**Outcome:** Imported artifacts remain within their declared path contract while configured local/CDN bases work.

**Exit criteria:**

- [x] Adversarial path cases fail before rendering and supported route-prefixed/CDN downloads pass.

**Evidence and scope:** [#76](https://github.com/egohygiene/identity/issues/76), [PR #113](https://github.com/egohygiene/identity/pull/113), merged at `063a4c70fcaccc6c15393f28ac2aabe62b34e1e7`. All 279 renderer tests, six hosted Chromium checks and three-platform release/clean-room gates pass. ADR-024 remains proposed. This supplies the URL-path boundary for IDN-Q31/IDN-Q35, not complete selected-file or public-asset coverage.

<!-- roadmap-step
id: IDN-Q16
status: blocked
depends_on: [IDN-Q12, IDN-Q17, IDN-Q18]
issues: [77]
-->
#### IDN-Q16 — Expose supported consumer recovery

**Outcome:** A standalone consumer can inspect interruption state and explicitly recover safely.

**Exit criteria:**

- [ ] Inspection is read-only; documented recovery/regeneration preserves canonical and unrelated files and diagnoses corrupt/active workspaces.

**Evidence and scope:** [#77](https://github.com/egohygiene/identity/issues/77). Current CLI source has no inspection/recovery command; do not advertise a future command.

<!-- roadmap-step
id: IDN-Q17
status: ready
depends_on: [IDN-Q12]
issues: [78]
-->
#### IDN-Q17 — Confine transaction workspaces

**Outcome:** Generation and recovery use a supported cache/staging/backup confinement contract.

**Exit criteria:**

- [ ] Runtime redirection evidence is recorded, unsafe paths fail before writes, and valid generation/recovery remains supported.

**Evidence and scope:** [#78](https://github.com/egohygiene/identity/issues/78). The audit risk was inferred; establish actual runtime behavior before selecting a fix.

<!-- roadmap-step
id: IDN-Q18
status: blocked
depends_on: [IDN-Q17]
issues: [79]
-->
#### IDN-Q18 — Serialize generation and recovery writers

**Outcome:** One supported writer owns each consumer transaction namespace.

**Exit criteria:**

- [ ] Coordinated writers and concurrent recovery safely reject or serialize without mixed state; interrupted locks preserve active work.

**Evidence and scope:** [#79](https://github.com/egohygiene/identity/issues/79). Record pre-fix behavior and retain bounded durability claims.

<!-- roadmap-step
id: IDN-Q19
status: ready
depends_on: []
issues: [80]
-->
#### IDN-Q19 — Qualify reproducible browser evidence

**Outcome:** Approved screenshots are checked under a reproducible browser/font/rendering environment.

**Exit criteria:**

- [ ] Unchanged approved baselines pass locally and in CI; a deliberate change fails without tolerance relaxation or automatic baseline updates.

**Evidence and scope:** [#80](https://github.com/egohygiene/identity/issues/80). Pin the qualified browser, fonts, locale, timezone, scale, and color settings.

<!-- roadmap-step
id: IDN-Q20
status: ready
depends_on: []
issues: [81]
-->
#### IDN-Q20 — Qualify an immutable development base

**Outcome:** Default development setup uses a reviewed immutable base while custom bases remain supported.

**Exit criteria:**

- [ ] The pinned base builds, smoke checks pass, and refresh/trust/cache/permission ownership is documented.

**Evidence and scope:** [#81](https://github.com/egohygiene/identity/issues/81). Independent of browser qualification and deferred Realm consolidation.

<!-- roadmap-step
id: IDN-Q21
status: blocked
depends_on: [IDN-Q19, IDN-Q20]
issues: [82]
-->
#### IDN-Q21 — Check portable setup directly in CI

**Outcome:** Standalone, Make, Task, and Docker setup remain usable through the shared helper.

**Exit criteria:**

- [ ] Bounded setup, repeated activation, representative dispatch, and qualified clean-base checks pass and catch an intentional fault.

**Evidence and scope:** [#82](https://github.com/egohygiene/identity/issues/82). Distinguish local check coverage from full integrity validation.

<!-- roadmap-step
id: IDN-Q22
status: blocked
depends_on: [IDN-Q09, IDN-Q10, IDN-Q15, IDN-Q16]
issues: [83]
-->
#### IDN-Q22 — Finish current contract and recovery documentation

**Outcome:** Current documentation describes the repaired public/download/recovery contracts consistently.

**Exit criteria:**

- [ ] Final #76/#77 behavior is documented across help, consumer guides, architecture, and publication boundaries; relevant validators pass.

**Evidence and scope:** [#83](https://github.com/egohygiene/identity/issues/83). IDN-Q09 can merge early. This final checkpoint keeps #83 open until the actual download/recovery behavior exists.

<!-- roadmap-step
id: IDN-Q23
status: ready
depends_on: []
issues: [84]
-->
#### IDN-Q23 — Retire completed documentation rewrites

**Outcome:** Only current-purpose documentation workflows retain write capability.

**Exit criteria:**

- [ ] Historical branch ownership is checked, completed rewrites are retired, and read-only documentation validation remains.

**Evidence and scope:** [#84](https://github.com/egohygiene/identity/issues/84). Preserve Git history and do not remove outstanding owned work blindly.

<!-- roadmap-step
id: IDN-Q24
status: blocked
depends_on: [IDN-Q11, IDN-Q13]
issues: [85]
-->
#### IDN-Q24 — Extract focused Python validation modules

**Outcome:** Validator responsibilities are smaller behind stable offline entry points.

**Exit criteria:**

- [ ] Diagnostics, fixture behavior, conformance vectors, extraction provenance, and standalone embedded-validator execution remain stable.

**Evidence and scope:** [#85](https://github.com/egohygiene/identity/issues/85). Moving modules must not make the distributed CLI depend on an Identity checkout.

<!-- roadmap-step
id: IDN-Q25
status: blocked
depends_on: [IDN-Q10, IDN-Q13, IDN-Q24]
issues: [86]
-->
#### IDN-Q25 — Share Python projection boundaries

**Outcome:** Truly shared source, digest, audience, and path semantics are reused consistently.

**Exit criteria:**

- [ ] Public/review and cross-language conformance remain covered with unchanged repaired output bytes.

**Evidence and scope:** [#86](https://github.com/egohygiene/identity/issues/86). Keep distinct v0/v1 profile semantics and standard-library operation.

<!-- roadmap-step
id: IDN-Q26
status: blocked
depends_on: [IDN-Q12, IDN-Q13, IDN-Q17, IDN-Q18]
issues: [87]
-->
#### IDN-Q26 — Extract Rust compiler and quality modules

**Outcome:** Compiler, quality, and motion responsibilities are bounded behind existing interfaces.

**Exit criteria:**

- [ ] Formatting, Clippy, behavior, deterministic output, approvals, drift, confinement, writer, recovery, and provenance checks pass.

**Evidence and scope:** [#87](https://github.com/egohygiene/identity/issues/87). Use small extractions after invariant repairs, without stronger durability claims.

<!-- roadmap-step
id: IDN-Q27
status: blocked
depends_on: [IDN-Q10, IDN-Q14, IDN-Q15, IDN-Q19]
issues: [88]
-->
#### IDN-Q27 — Extract renderer components and adapters

**Outcome:** The renderer separates inputs, presentation, and downloads without changing its contract.

**Exit criteria:**

- [ ] Release/audience/path regressions, accessibility, keyboard/routing, downloads, and qualified visual checks remain green.

**Evidence and scope:** [#88](https://github.com/egohygiene/identity/issues/88). Schedule after the first assembled kit so extraction protects its complete behavior.

<!-- roadmap-step
id: IDN-Q28
status: blocked
depends_on: [IDN-Q10, IDN-Q11, IDN-Q12, IDN-Q13, IDN-Q14, IDN-Q15, IDN-Q16, IDN-Q17, IDN-Q18, IDN-Q19, IDN-Q20, IDN-Q21, IDN-Q22, IDN-Q23, IDN-Q24, IDN-Q25, IDN-Q26, IDN-Q27]
issues: [70]
-->
#### IDN-Q28 — Close the stabilization audit

**Outcome:** All eighteen stabilization issues have acceptance and validation evidence.

**Exit criteria:**

- [ ] #71–#88 are complete, environment/consumer recovery proof is recorded, and remaining optional coverage is explicit.

**Evidence and scope:** [#70](https://github.com/egohygiene/identity/issues/70). This tracker is not a blanket prerequisite for read-only collection or first-kit work.

### Brand Kit completion and optional scope

<!-- roadmap-step
id: IDN-Q29
status: active
depends_on: []
issues: [99]
-->
#### IDN-Q29 — Define the minimal Brand Kit source

**Outcome:** Existing source formats and projections map to a small compatible core with deliberate optional sections.

**Exit criteria:**

- [ ] Coverage/ownership inventory, minimal/expanded fixtures, compatibility, useful diagnostics, and only demonstrated source gaps are complete.

**Evidence and scope:** [#99](https://github.com/egohygiene/identity/issues/99) is the selected current priority after IDN-Q13–15. [Checkpoint 1](docs/reviews/identity-fields-2026-10-18.md) inventories source/schema/entry-point/consumer coverage and records synthetic gap probes; its field-layout and requiredness recommendations await review. Checkpoint 2 handles agreed compatible contract/examples; checkpoint 3 proves guided authoring and scopes initializer/EgoLint handoff follow-ups. No schema or runtime change is part of checkpoint 1. Root self-brand source remains a later explicit adoption task.

<!-- roadmap-step
id: IDN-Q30
status: blocked
depends_on: [IDN-Q29]
issues: [100]
-->
#### IDN-Q30 — Publish approved profile and copy

**Outcome:** Contributors can reuse supplied approved naming, positioning, and descriptions.

**Exit criteria:**

- [ ] Public pages/exports contain approved public copy, consistent naming, and clean omission of optional missing text.

**Evidence and scope:** [#100](https://github.com/egohygiene/identity/issues/100). Preserve IDN-Q10's audience boundary; never invent product claims.

<!-- roadmap-step
id: IDN-Q31
status: blocked
depends_on: [IDN-Q29, IDN-Q15]
issues: [101]
-->
#### IDN-Q31 — Deliver useful approved mark downloads

**Outcome:** Consumers obtain suitable existing marks, favicons, and avatars with traceable usage guidance.

**Exit criteria:**

- [ ] Advertised release-bound files exist; required formats, provenance/rights, configured bases, and missing-variant handling work.

**Evidence and scope:** [#101](https://github.com/egohygiene/identity/issues/101). #99 is the source prerequisite; #76 supplies the exercised download-path boundary. New artwork is not required.

<!-- roadmap-step
id: IDN-Q32
status: blocked
depends_on: [IDN-Q29, IDN-Q14]
issues: [102]
-->
#### IDN-Q32 — Publish color and typography foundations

**Outcome:** Displayed colors, intended contrast combinations, and typography agree with authoritative source and exports.

**Exit criteria:**

- [ ] Role/value examples, supported combinations, font/fallback availability and licensing, and release-matched guidance are verified.

**Evidence and scope:** [#102](https://github.com/egohygiene/identity/issues/102). #99 defines the core; #74/#75 govern the optional design guidance used by this path. A component library is outside scope.

<!-- roadmap-step
id: IDN-Q33
status: blocked
depends_on: [IDN-Q29]
issues: [103]
-->
#### IDN-Q33 — Expose rights and authoritative policy references

**Outcome:** Consumers can identify asset permissions, attribution, official contacts, and policy owners.

**Exit criteria:**

- [ ] Distributed assets/fonts have traceable rights; missing optional references are omitted and unresolved permissions remain explicit.

**Evidence and scope:** [#103](https://github.com/egohygiene/identity/issues/103). Keep software license, trademark rules, third-party rights, and policy authority distinct.

<!-- roadmap-step
id: IDN-Q34
status: blocked
depends_on: [IDN-Q29, IDN-Q30, IDN-Q31, IDN-Q33]
issues: [104]
-->
#### IDN-Q34 — Add selected presentation profiles

**Outcome:** Approved copy and imagery reach a small opt-in set of real distribution targets.

**Exit criteria:**

- [ ] At least one actual target works end to end with explicit constraints, rights, and no-profile fallback.

**Evidence and scope:** [#104](https://github.com/egohygiene/identity/issues/104). Reuse pinned Aether surface facts; account management and package publication retain their owners.

<!-- roadmap-step
id: IDN-Q35
status: blocked
depends_on: [IDN-Q30, IDN-Q31, IDN-Q32, IDN-Q33, IDN-Q34, IDN-Q14, IDN-Q15]
issues: [105]
-->
#### IDN-Q35 — Assemble the usable public Brand Kit

**Outcome:** A representative consumer obtains copy, marks, foundations, rights, and selected target material from one coherent kit.

**Exit criteria:**

- [ ] Minimal/expanded consumers, release binding, downloads, accessibility, public filtering, and publication ownership evidence pass.

**Evidence and scope:** [#105](https://github.com/egohygiene/identity/issues/105). This first usable kit does not wait for IDN-Q24–IDN-Q27 or later optional scope.

<!-- roadmap-step
id: IDN-Q36
status: planned
depends_on: [IDN-Q35]
issues: [106]
-->
#### IDN-Q36 — Select optional launch and document templates

**Outcome:** A requested template reuses approved kit content and project-supplied changing facts.

**Exit criteria:**

- [ ] A concrete selected use case is demonstrated with explicit inputs, or the owner records an approved scope disposition.

**Evidence and scope:** [#106](https://github.com/egohygiene/identity/issues/106). Later scope selection is required; reuse Aether campaign-handoff capabilities where suitable.

<!-- roadmap-step
id: IDN-Q37
status: planned
depends_on: [IDN-Q29, IDN-Q33, IDN-Q35]
issues: [107]
-->
#### IDN-Q37 — Select optional imagery and motion support

**Outcome:** Needed supporting visual categories consume existing approved source and rights.

**Exit criteria:**

- [ ] A selected category is demonstrated with accessibility/reduced-motion guidance, or the owner records an approved scope disposition.

**Evidence and scope:** [#107](https://github.com/egohygiene/identity/issues/107). Inventory existing Kern/motion support first. Relay #8 is conditional only for new automated capture.

<!-- roadmap-step
id: IDN-Q38
status: planned
depends_on: [IDN-Q29, IDN-Q33, IDN-Q35]
issues: [108]
-->
#### IDN-Q38 — Connect authoritative ecosystem references

**Outcome:** A bounded integration preserves Aether, Realm, Relay, and policy ownership.

**Exit criteria:**

- [ ] Owner/source/consumer references and a bounded example are documented; the existing DCO queue is linked or explicitly unresolved.

**Evidence and scope:** [#108](https://github.com/egohygiene/identity/issues/108). Shared-default consolidation follows stabilization; not every reference integration needs every audit refactor. No duplicate DCO action or CLA service.

<!-- roadmap-step
id: IDN-Q39
status: planned
depends_on: [IDN-Q29, IDN-Q32]
issues: [109]
-->
#### IDN-Q39 — Decide product design-system scope

**Outcome:** Consumer needs and component ownership are explicitly resolved.

**Exit criteria:**

- [ ] A short reviewed decision selects sufficient foundations, external component ownership, bounded follow-up, or deferral.

**Evidence and scope:** [#109](https://github.com/egohygiene/identity/issues/109). Keep reusable components/templates with their established Holon owner unless a separately reviewed decision changes that boundary.

<!-- roadmap-step
id: IDN-Q40
status: blocked
depends_on: [IDN-Q29, IDN-Q30, IDN-Q31, IDN-Q32, IDN-Q33, IDN-Q34, IDN-Q35, IDN-Q36, IDN-Q37, IDN-Q38, IDN-Q39]
issues: [98]
-->
#### IDN-Q40 — Close complete-kit delivery and dogfood

**Outcome:** The selected kit scope is proven for Identity itself and ready for repeatable consumer adoption.

**Exit criteria:**

- [ ] All eleven children are complete or explicitly dispositioned by the owner, and the final self-consumer/release checklist below has evidence.

**Evidence and scope:** [#98](https://github.com/egohygiene/identity/issues/98). Separate merged, released, and deployed status. Optional scope decisions do not require every proposed platform or asset category.

### Final self-dogfood and release acceptance

- [ ] Establish real consumer-owned v1 source for Identity's existing approved brand, preserving source rights, provenance, and exact approval subjects. The current tracked root has no `.identity/`; generated assets and publication configuration are inventory inputs, not proof of completed self-adoption.
- [ ] Follow the documented onboarding path in a clean qualified environment. Current `init` creates v0 source; do not claim automatic v1 initialization. Generate twice, compare complete inventories/checksums, and verify drift without mutation.
- [ ] Obtain the correct copy, marks, favicon/avatar, colors, type guidance, rights, and one selected presentation output through the kit. Exercise minimal/expanded input, optional omission, public filtering, unsafe paths, and release mismatches.
- [ ] Exercise a second writer, interrupted generation, read-only inspection, explicit recovery, and regeneration while canonical/unrelated files remain intact. Check qualified browser, accessibility, keyboard/focus, reduced-motion, route-prefix/CDN downloads, and reviewed visual baselines.
- [ ] Publish a new immutable stable release containing the completed work and prove its supported clean-install/platform matrix, checksums, SBOM/license inventory, and provenance. Preserve earlier tags and distinguish Linux binary distribution from macOS/Windows source-install evidence.
- [ ] Verify the selected release through the existing Brand Kit publisher, retained artifact, live hashes, preserved Decisions routes, and rollback evidence. Organization `/identity/` handoff/installation, if selected, retains its own owner and exact release-agreement proof.
- [ ] Upgrade one contrasting reviewed consumer such as Mantle, prove deliberate overrides and CI drift detection, and rehearse its upgrade/rollback before expanding adoption. Close trackers from actual evidence and approved optional dispositions.

### Roadmap-to-issue handoff

- A step is complete only when its exit criteria and required evidence are satisfied; commit count never determines progress.
- Ready steps without an issue are candidates for the private, duplicate-aware roadmap.issue-plan.json dry run. Planned steps remain preview-only unless a reviewer explicitly opts them in with issue_policy: propose.
- Issue creation or reconciliation requires human approval or an explicitly authorized Pace operation and returns issue references through a reviewable roadmap pull request.
- Pull requests and commits should include Roadmap-Step: <ID>; historical evidence may be linked through existing issue and pull-request relationships.
- Public rendering uses only allowlisted build-time evidence and never places a GitHub token or private issue plan in the browser artifact.

<!-- END ROADMAP EXECUTION SNAPSHOT -->

## Strategic context

Identity is evolving from an incubated product-identity CLI into a standalone Brand Kit generator. This document owns durable capability evolution and execution order. The original [roadmap issue #5](https://github.com/egohygiene/identity/issues/5) is historical context; #70 and #98 coordinate the current implementation issues. It describes dependency order and release evidence, not promised dates.

## Umbrella outcomes

The original portfolio issues remain outcome-level anchors:

- [#1](https://github.com/egohygiene/identity/issues/1) — canonical identity and design-token schema;
- [#2](https://github.com/egohygiene/identity/issues/2) — compiler and distributable packages;
- [#3](https://github.com/egohygiene/identity/issues/3) — visual-motion validation.

Their original completion gates are retained as historical outcome definitions; the current execution snapshot above records the implemented/released state and remaining work.

## Dependency-ordered waves

| Wave | Outcome | Issues | Exit evidence |
| --- | --- | --- | --- |
| 0 — Product and foundations | Accept the Brand Kit boundary and select replaceable foundations | #6, #7 | Active product contract, boundary review, toolchain ADRs, dependency policy, proof of high-risk integrations |
| 1 — Extraction and canonical contracts | Establish an independent CLI and versioned consumer-owned source | #8, #9 | Parity tests, migration fixtures, published schemas, deterministic merge/override diagnostics |
| 2 — Compiler and packages | Produce reproducible projections through stable adapter contracts | #10, #11 | Offline core tests, adapter contract tests, deterministic outputs, packages, manifests, checksums |
| 3 — Trust and governance | Make quality, accessibility, provenance, voice, and approval testable | #12, #13 | Release-blocking validation, human-review evidence, usage/voice schemas, recovery guidance |
| 4 — Public product experience | Present, preview, approve, download, and publish a Brand Kit | #14, #15, #16, #50, #56, #57 | Accessible renderer, governed mascot, immutable Brand Kit, accepted dogfood architecture, and deployed route checks |
| 5 — Proof and release | Prove variation across consumers and publish v1.0.0 | #17, #18 | Empathy/OptiFlow pilots, clean-room quickstart, compatibility suite, attestations, stable release |

## Historical capability snapshot

The following pre-pilot capability narrative and original Wave 0 exit definitions
are retained as historical context. Claims such as an open #2 or unfinished
Empathy extraction describe that earlier checkpoint, not the current state.
Use the reviewed execution snapshot above for current status and dependencies.

<details>
<summary>Preserved pre-pilot wave narrative and acceptance definitions</summary>

Wave 0 is complete. Wave 1 has the independently extracted CLI from #8 and the
implemented v1 source/schema/validation boundary from #9; Empathy's pinned
consumer transition remains the final cross-repository extraction gate.

Wave 2 implementation is complete in Identity after #10 and #11. #10 provides
the deterministic offline compiler core, adapter SDK, mutation-free plans,
manifests, transactional generated-state apply, and explicit recovery. #11 adds
nine versioned Brand Kit output profiles, concrete
token/web/document/metadata/vector/raster/archive adapters, deterministic
package indexes/checksums, subset compatibility, and byte-identical package
proof across clean repositories.

Wave 3 is now substantially implemented. #12 established the shared
`identity.quality-report/v1` evidence harness, package/publication scopes,
release-blocking accessibility/provenance/license/reproducibility/visual checks,
visual baselines, explicit skipped coverage, and human-review evidence. This #3
change adds framework-neutral visual-motion governance to that same release
decision: Astryx-informed adopt/adapt/reject rules, purpose budgets,
reduced-motion fallbacks, deterministic capture/provenance contracts, motion
fixtures, and semantic human-review boundaries. #13 adds governed voice,
contextual tone, usage, accessibility/legal/localization guidance, approval
lifecycle, and deterministic public/review projections. Issue #8 remains the
final pre-renderer cross-repository gate.

The organization-channel extension from #65 is implemented as an additive v1
boundary. Identity now owns one versioned registry and deterministic public
adapters; Press Kit and social-surface projections consume the same approved
active records. The initial platform candidates remain honestly `planned`
until their real handles, URLs, ownership, and verification evidence are
reviewed.

The umbrella #2 remains open despite the Wave 2 implementation milestone. Its
remaining acceptance evidence is the real Empathy and OptiFlow consumer proof
owned by #17 after the required quality/governance and renderer dependencies
land. This prevents package implementation from being mistaken for successful
fleet consumption.

Wave 0 establishes decisions that constrain every implementation PR:

### #6 — Brand Kit product contract

**Exit criteria:**

- ownership and non-ownership are explicit;
- compiler, packages, renderer, studio, consumer, evidence, and publication interfaces are named;
- canonical, generated, transient, and published authority are distinct;
- personas, workflows, surfaces, failure states, and measurable signals are documented;
- `/identity` is canonical and `/brand-kit` is a redirect;
- capabilities use implemented, accepted, proposed, and deferred honestly;
- architecture links, document front matter, and repository boundaries validate.

### #7 — Standards, libraries, and framework adapters

**Exit criteria:**

- adopt/adapt/reject decisions are evidence-backed;
- dependencies have bounded purposes and replacement strategies;
- local and CI output assumptions are proven;
- no framework or library becomes canonical domain truth.

**Accepted evidence:**

- [foundation comparison matrix](docs/evaluations/brand-kit-foundations.md);
- [toolchain and boundary ADRs](DECISIONS.md);
- [dependency policy](docs/DEPENDENCY_POLICY.md);
- [deterministic DTCG projection-boundary proof](experiments/dtcg-projection-boundary/README.md).

</details>

## v1 capability map

| v1 promise | Owning issues | Required tests/evidence |
| --- | --- | --- |
| Initialize or migrate a project-owned identity | #8, #9 | Command parity, schema, valid/invalid fixtures, migration and rollback tests |
| Resolve organization defaults and product overrides | #9, #17 | Merge/conflict diagnostics and contrasting consumer snapshots |
| Plan before mutation | #10 | Mutation-free plan tests covering writes, replacements, removals, warnings, and approvals |
| Generate deterministic target profiles | #10, #11 | Offline unit/integration tests, adapter contracts, byte-identical outputs/manifests, checksum stability |
| Block inaccessible, unlicensed, or untraceable releases | #3, #12, #13 | #12 quality-report/accessibility/provenance/license/visual/reproducibility gates, #3 visual-motion/capture/provenance gates, and #13 guidance/approval projections are implemented |
| Distribute portable Brand Kit packages | #11, #18 | Versioned profile/package contracts, checksums, deterministic archive, consumer installation, clean-room build, and release provenance |
| Render and preview an understandable Brand Kit | #14, #15 | Accessibility, responsive, link, download, visual regression, and mutation-isolation tests |
| Publish the Identity Brand Kit at `identity.egohygiene.io` | #16 | Immutable release projection, metadata, `/brand-kit/` compatibility redirect, deployment smoke test, and rollback evidence |
| Reuse an approved mascot without losing human authority | #50 | Character/variant schemas, approval and provenance links, licensed exact bytes, accessibility and motion guidance, Brand Kit package verification |
| Dogfood Identity through LaunchKit and Zensical without duplicating brand truth | #56, #57 | Accepted route/adapter contract, immutable pins, accessible deterministic composite, release-binding proof, and independent rollback |
| Preserve product variation within a family | #17 | Empathy and OptiFlow inheritance/override evidence |
| Release a supportable v1.0.0 | #18 | Platform matrix, documentation, SBOM/license inventory, checksums, attestations, and all release gates |

## Cross-cutting requirements

Every wave must preserve:

- human authority, privacy, accessibility, licensing, and provenance;
- canonical/generated/transient/publication boundaries;
- deterministic local and CI behavior for supported projections;
- versioned cross-repository contracts and immutable dependencies;
- implementation, documentation, tests, migration, and rollback agreement;
- visible uncertainty, partial coverage, unsupported behavior, and deferred work.

## Deferred direction

Managed collaboration, enterprise controls, marketplaces, provider-specific generative systems, and a conversational organization compiler remain outside v1. The architecture preserves ports for later work without making those services prerequisites or implying support before evidence exists.

## Execution policy

Work one scoped PR at a time. Architecture and specification changes land before dependent implementation. Pause after each wave for review. If work belongs to another repository, open a follow-up there instead of expanding Identity's boundary.
