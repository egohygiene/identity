## Readiness reconciliation — 2026-09-26

The [public fleet audit](https://github.com/egohygiene/pace/issues/13) identifies the existing repository ADR issues and source layouts. All public backfill issues remain open; preserve their history rather than opening duplicates.

| Shared requirement | Verified status / next owner |
| --- | --- |
| egohygiene/hygiene#15 policy | Closed and explicitly ratified; Hygiene docs/decisions/RATIFICATION.md records policy v1.1.0 and human authority |
| egohygiene/holon#6 scaffolding | Closed; use the actual supported immutable materialization contract |
| egohygiene/aether#49 guidance | Original hook delivered; egohygiene/aether#91 reconciles its older proposed-policy pin and ADR authoring behavior before adoption |
| egohygiene/egolint#24 validation | Implemented; reconcile supported pins/authority states during egohygiene/relay#99 checkpoint 1 |
| egohygiene/relay#5 reusable validation | Open; #99 already provides its six ordered checkpoints |
| egohygiene/relay#30 renderer | Delivered; egohygiene/relay#115 now owns real ADR collection and reusable Decisions build integration |
| egohygiene/relay#33 / egohygiene/relay#106 publication | Acceptance remains open |
| egohygiene/pace#5 rollout + local backfills | Open; source preservation, policy/index/lineage proof and continuous capture still required |

Do not request policy ratification again. Do not treat a numbered ADR file or closed renderer issue as full adoption. Hygiene itself owns the canonical policy rather than inheriting its own consumer policy-reference file.

**Maintainer-selected first capability (2026-09-26): ADRs and `/decisions/`, using the existing per-repository issues.** The bounded Relay #112 local collector checkpoint merged through Relay #114; #112 remains open for its publication requirements. Continue with this ADR campaign. Populated roadmaps in [#31](https://github.com/egohygiene/pace/issues/31) follow ADR completion.

Next: review [Relay PR #121](https://github.com/egohygiene/relay/pull/121) adopting the verified EgoLint #75 merge, reconcile egohygiene/egolint#73 after that Relay merge, continue egohygiene/relay#5 shared validation with hosted acceptance explicitly deferred, establish the reviewed migration plan, then prove one validate-first repository (Identity already has substantial decision source). Complete source, validation, real normalized input, declared publication and continuous capture across the existing backfills. Required decisions remain human-governed; preserve proposed states where authority is unavailable. The partial-domain normalization gap in egohygiene/observatory#25 must be considered for ADR-only collection too; a delivered renderer is not a populated live ledger.

## Registered execution gaps — 2026-09-26

The maintainer authorized these focused follow-ups. The existing per-repository backfill issues remain the consumer work items.

- [ ] [egohygiene/aether#91](https://github.com/egohygiene/aether/issues/91) — align the existing ADR authoring skill and managed decision-impact guidance with the ratified policy; preserve historical evidence and proposed/accepted distinctions.
- [ ] [egohygiene/observatory#25](https://github.com/egohygiene/observatory/issues/25) — retain truthful collection coverage for partial inputs, including ADR-only input.
- [ ] [egohygiene/relay#115](https://github.com/egohygiene/relay/issues/115) — collect canonical ADR evidence and connect it to the existing reusable Decisions build.
- [ ] [egohygiene/identity#69](https://github.com/egohygiene/identity/issues/69) — first complete repository backfill/adoption canary after its shared-system gates are ready.

**Current implementation checkpoint — 2026-09-28:** Relay #99 checkpoints 1–5 are verified merged, and parser-repair PR #120 merged as `04bd32c8ef492418f47d6df6faee425d6888f341` with the exact reviewed tree. The maintainer directed hosted acceptance to the final cleanup pass; continue meaningful local validation without claiming a hosted pass. EgoLint #75 merged the #73 policy fix as `933472b6322d2060c487e5a8a6f0bc5197696af0`; [Relay PR #121](https://github.com/egohygiene/relay/pull/121) is the open adoption checkpoint. All 103 local architecture tests and the 15-test native acceptance matrix passed, retaining 29 verified bundles. Review and verify that Relay merge before reconciling #73; #74 owns diagram semantic validators. Relay #99/#5 stay open. Aether #91 can proceed against the documented validation boundary; Observatory #25 gates partial publication, not offline validator development.

Historical reconstruction remains agent-assisted work in each repository: inspect Git/PR/issue/release evidence, group consequential decisions, preserve legacy records and uncertainty, and submit reviewable ADRs. Future agent PR handoffs must reference/create/update the appropriate ADR or explain why none is required. Instructions and skills route that work; validator evidence and explicit human decision authority remain separate.

<!-- identity-intelligence-coordination:v1 -->
## Identity pilot coordination — 2026-10-03

Continue using [Identity #69](https://github.com/egohygiene/identity/issues/69) as the existing repository backfill/adoption canary. Link its parallel stabilization tracker [Identity #70](https://github.com/egohygiene/identity/issues/70) and documentation/roadmap reconciliation [Identity #83](https://github.com/egohygiene/identity/issues/83); do not create a duplicate pilot or make all 18 audit fixes/refactors prerequisites for Observatory or read-only ADR collection.

Read-only inventory/collection can proceed with authorized source visibility and truthful freshness, partial-coverage, and uncertainty reporting. This does not waive #69's shared-system or human-authority requirements for historical migration, continuous capture, and publication. Record an Identity stabilization prerequisite only when a specific exercised operation depends on it, with supporting evidence.

#83 should ship the bounded canonical-roadmap reconciliation early, including #70–#88 and IDN-Q05's #17/#18 completion evidence; its final audience/download/recovery wording follows #71/#76/#77. Publication targets remain explicit and separate: the immutable Brand Kit host, the organization `/identity/` experience, and proposed Intelligence/Decisions views do not share deployment authority by implication. Existing ADR-first campaign scope and subsequent roadmap rollout ordering remain unchanged.
<!-- /identity-intelligence-coordination:v1 -->

## Outcome

Use Pace to adopt and continuously reconcile the canonical ADR baseline across applicable Ego Hygiene repositories without destroying existing decision history or copying policy text between repositories.

## Scope

- Discover repositories that are eligible for the ADR baseline.
- Detect current ADR structure, local conventions, and declared Hygiene ADR contract version.
- Consume the canonical policy from `egohygiene/hygiene#15` and scaffolding/materialization contract from `egohygiene/holon#6`.
- Produce a preview/plan before modifying repositories.
- Preserve and migrate existing ADRs non-destructively.
- Detect incompatible local conventions, missing indexes, broken supersession links, and stale inherited contract versions.
- Apply updates through the normal Pace synchronization/reconciliation model rather than one-off scripts.
- Verify repositories using Relay architecture validation after application.
- Record per-repository adoption state and unresolved exceptions.

## Acceptance criteria

- [ ] Pace can identify applicable repositories and their ADR adoption state.
- [ ] Repositories without the baseline receive a non-destructive adoption plan.
- [ ] Existing ADRs are preserved and mapped where feasible.
- [ ] Contract-version drift is detectable.
- [ ] Incompatible local overrides are reported rather than silently overwritten.
- [ ] Preview → apply → verify behavior is supported.
- [ ] Relay validation is used as post-apply evidence.
- [ ] Fleet status distinguishes adopted, partial, legacy, blocked, and not-applicable states.
- [ ] No repository receives a copied fork of the canonical Hygiene ADR policy.

## Dependencies

- https://github.com/egohygiene/hygiene/issues/15
- https://github.com/egohygiene/holon/issues/6
- https://github.com/egohygiene/relay/issues/5