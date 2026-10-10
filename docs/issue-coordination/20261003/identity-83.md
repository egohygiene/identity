# Problem and intended outcome

Update current-state documentation against shipped implementation and publication configuration. Start inventory early; finish recovery documentation after R07 and review audience/path wording after R01 and R06.

**Roadmap:** R13 · milestone 4 · P2. Planning IDs are not GitHub issue numbers.

**Audit baseline:** `egohygiene/identity@320dc5e94843198893ff7216f22d1d3d58a04be4`; report `repository-health-20261003T162958Z.md`, captured 2026-10-03T16:29:58Z. The evidence below is a historical observation, not a claim about the current deployed site or a completed repair.

## Acceptance criteria

- [ ] ROADMAP.md represents #70–#88 through stable canonical steps and issue links, reconciles IDN-Q05 against the completed #17/#18 exit evidence, and preserves existing step IDs and historical records.
- [ ] Roadmap frontmatter, execution-snapshot dates, machine-readable status/dependency/issue fields, and prose agree with reviewed evidence; collection time is not substituted for source-review freshness.
- [ ] Merged implementation, tagged release, deployed publication, and accepted decision status remain distinct; #71–#73's merged-main evidence is not reported as an already deployed release.
- [ ] Brand Kit, organization `/identity/`, and proposed Intelligence publication boundaries have an explicit ownership/route/validation/rollback matrix. Unknown Intelligence host or deployment choices remain proposed or unverified rather than borrowing an existing surface's authority.
- [ ] #70, #69, and Pace #5 distinguish independent read-only collection from gated migration/publication; no blanket dependency on all 18 audit issues is introduced.
- [ ] README, PURPOSE, SYSTEM, ARCHITECTURE, DECISIONS, and ROADMAP consistently describe shipped CLI/renderer/studio capabilities.
- [ ] Canonical standalone site versus organization integration ownership is confirmed and recorded without inventing live-deployment evidence.
- [ ] Historical ADR intent and observations remain intact and clearly dated.
- [ ] Documentation/link/publication architecture validators pass; recovery and public/download boundary wording matches the repaired contracts.

<!-- identity-intelligence-coordination:v1 -->
## Roadmap freshness and publication coordination

At main commit [8aae2c6](https://github.com/egohygiene/identity/commit/8aae2c6767d07714ea16bf0ea493e1f1ac399b6e), ROADMAP.md's dated execution snapshot omits #70–#88 and still labels IDN-Q05 `active`, although #17/#18 are closed and its listed exit criteria are checked. Recheck the latest default branch and concurrent PRs before editing, then ship this bounded roadmap reconciliation early rather than waiting for unrelated stabilization/refactor completion. Reconcile completion from exit criteria and durable evidence, not closed issue state alone; retain historical observations and stable step identifiers.

Inventory can begin now. Final documentation of public audience, downloads, and recovery must follow the actual contracts established by #71, #76, and #77 respectively. The repaired preflight's Python requirement and legacy-journal handling also need accurate current-build wording without rewriting historical release claims.

Preserve the publication ownership established by ADR-017 and the publication machine contracts:

| Surface | Boundary to retain |
| --- | --- |
| Release-backed Brand Kit at `identity.egohygiene.io` | Existing immutable-release renderer/publisher, downloads, manifests, domain association, and rollback by release identity. |
| Organization product experience at `egohygiene.io/identity/` | Separately reviewed content-addressed composite; organization route owner installs the approved artifact under its own deployment/rollback authority. |
| Proposed Repository Intelligence / Decisions views | Consume shared Relay/Observatory contracts through #69 and [Pace #5](https://github.com/egohygiene/pace/issues/5). Record approved host, routes, publisher, privacy, and rollback authority explicitly; do not infer permission to replace the Brand Kit root, CNAME, or organization experience. |

A successful local build, proposed route, merged source change, or closed renderer issue is not proof of a live deployment. Keep repository-owned Markdown as source; generated dashboards and ledgers remain projections with source revision, freshness, and partial-coverage evidence. Do not rewrite ADR history or create a separate roadmap source in GitHub issue prose.
<!-- /identity-intelligence-coordination:v1 -->

## Validation and safeguards

Add focused behavioral regressions for the stated outcomes, then run the affected existing suites and required integrity checks. Record actual commands/results and explain skips or unsupported platforms. Preserve explicit approvals and drift protection, immutable release/source bindings, provenance/checksums, deterministic output, and offline standalone operation. Follow the tracker dependencies before merging the final behavior.

## Audit evidence

### AUDIT-011 — Active architecture documents contradict shipped state

- **Classification:** documentation gap. **Severity:** medium. **Confidence:** high.
  **Status:** confirmed. **History:** new.
- **Area:** architecture, capability discovery, publication ownership.
  **Effort:** small. **Impact:** medium.
- **Observation:** README records implemented renderer/studio/consumer proof
  and the standalone canonical site. Active/provisional architecture context
  still includes present-tense extraction and pre-renderer statements.
- **Evidence — observed:** [PURPOSE.md](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/PURPOSE.md#evidence-and-uncertainty)
  line 87 says the CLI has not been extracted;
  [SYSTEM.md](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/SYSTEM.md#system-inventory) lists renderer/studio as proposed;
  [ARCHITECTURE.md](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/ARCHITECTURE.md#public-route-boundary) line 104 names the
  organization route as canonical, while `README.md:27` and lines 382–385
  describe the standalone site and implemented renderer. Some ADRs are
  intentionally historical; this finding concerns documents presented as
  current architecture/capability context.
- **Why it matters — inferred:** Maintainers and agents can choose obsolete
  interfaces, duplicate shipped work, or misunderstand route/deployment owners.
- **Recommendation — recommended:** Amend current-state summaries, explicitly
  date historical observations, and link the implemented evidence. Reconcile
  canonical site versus organization integration without rewriting ADR history.
- **Suggested validation — unverified repair:** Review README, PURPOSE, SYSTEM,
  ARCHITECTURE, DECISIONS, and ROADMAP together against source and publication
  configuration; run link/architecture validators and verify consistent state.
- **Dependencies or risks:** Route ownership requires maintainer confirmation;
  do not infer live deployment state solely from repository prose.

<!-- identity-audit-roadmap:20261003T162958Z:R13 -->

<!-- identity-roadmap-links:start -->
## Roadmap links

Tracker: #70.

Final documentation depends on: #71, #76, #77. Inventory and evidence-backed roadmap reconciliation can start independently now; this issue is not a blanket gate for read-only Intelligence collection.

<!-- identity-roadmap-links:end -->
