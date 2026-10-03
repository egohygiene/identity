# Problem and intended outcome

Update current-state documentation against shipped implementation and publication configuration. Start inventory early; finish recovery documentation after R07 and review audience/path wording after R01 and R06.

**Roadmap:** R13 · milestone 4 · P2. Planning IDs are not GitHub issue numbers.

**Audit baseline:** `egohygiene/identity@320dc5e94843198893ff7216f22d1d3d58a04be4`; report `repository-health-20261003T162958Z.md`, captured 2026-10-03T16:29:58Z. The evidence below is a historical observation, not a claim about the current deployed site or a completed repair.

## Acceptance criteria

- [ ] README, PURPOSE, SYSTEM, ARCHITECTURE, DECISIONS, and ROADMAP consistently describe shipped CLI/renderer/studio capabilities.
- [ ] Canonical standalone site versus organization integration ownership is confirmed and recorded without inventing live-deployment evidence.
- [ ] Historical ADR intent and observations remain intact and clearly dated.
- [ ] Documentation/link/publication architecture validators pass; recovery and public/download boundary wording matches the repaired contracts.

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

Depends on: #77.

<!-- identity-roadmap-links:end -->
