# Stabilize Identity's governance boundaries, recovery, and development workflow

Track the 18 implementation issues from the repository-health audit. Repair the confirmed public-data, validation, and recovery authority defects first; stabilize compatibility and development workflows; then refactor behind tested invariants.

Audit baseline: [`320dc5e94843198893ff7216f22d1d3d58a04be4`](https://github.com/egohygiene/identity/tree/320dc5e94843198893ff7216f22d1d3d58a04be4). Audit captured 2026-10-03T16:29:58Z under [Aether auditor spec v2.0.0](https://github.com/egohygiene/aether/blob/087bceccd936922371155e69dc92ff802aa8a029/library/organization/specs/quality/auditor.spec.md).

## Execution order

1. **Authority boundaries:** R01–R03 can start independently. Public filtering must work even for fully valid source.
2. **Compatibility and recovery:** R04–R09 establish digest, optional-input, path, transaction workspace, writer, and consumer-recovery contracts. R08/R09 first validate inferred runtime risks; the audit did not reproduce concurrent corruption or redirected writes.
3. **Reproducible development:** R10–R12 qualify browser/fonts and immutable bases before direct setup CI coverage.
4. **Documentation and cleanup:** R13–R18 reconcile current documentation, retire completed automation, and extract modules after the repaired invariants have regression coverage. Documentation inventory and workflow ownership checks can begin early.

The numbered milestones are roadmap groupings. This publisher does not create GitHub milestone objects, assign owners, invent estimates, or change repository labels.

<!-- identity-intelligence-coordination:v1 -->
## Coordination with the Identity Intelligence pilot

[Identity #69](https://github.com/egohygiene/identity/issues/69) remains the repository ADR migration and continuous-capture issue; [Pace #5](https://github.com/egohygiene/pace/issues/5) owns reviewed fleet adoption. This tracker coordinates Identity stabilization with that pilot; completing all 18 audit issues is **not** a blanket prerequisite for Observatory or read-only ADR collection.

| Activity | Scoped prerequisite |
| --- | --- |
| Read-only repository inventory, Observatory collection, and ADR collection | Honor authorized source visibility and shared input/coverage contracts. Report missing, partial, stale, or unverified evidence honestly. These activities can proceed alongside this tracker and do not require all compiler, renderer, environment, or refactoring issues to close. |
| ADR backfill, migration, and continuous capture | Retain #69's shared-system and human-authority gates and Pace #5's preview/apply/verify process. List any additional Identity repair only when the exercised operation requires it, with concrete evidence. |
| Publication of Intelligence views or Identity projections | Satisfy the applicable shared publication, privacy, immutable-input, and route-ownership contract. Determine prerequisites for the specific surface; read-only collection does not confer deployment authority. |

#83 should reconcile canonical ROADMAP.md with #70–#88 and the completed v1 pilot/release evidence in an early, bounded documentation PR; its final recovery/audience/download wording still follows #71, #76, and #77. Until that reconciliation lands, collection should expose the dated roadmap and its stale status claims instead of silently inventing a corrected intent model.

The release-backed Brand Kit, organization `/identity/` experience, and proposed Repository Intelligence views retain separate publication ownership. #83 records the exact boundaries; #69/Pace #5 adoption does not replace the Brand Kit publisher or its domain configuration.

**Verified stabilization checkpoint — 2026-10-03:** #71–#73 are closed after [PR #89](https://github.com/egohygiene/identity/pull/89) merged as [8aae2c6767d07714ea16bf0ea493e1f1ac399b6e](https://github.com/egohygiene/identity/commit/8aae2c6767d07714ea16bf0ea493e1f1ac399b6e). This is merged-main evidence, not a claim that these repairs have been included in a stable tag or deployed release. The historical audit below remains unchanged.
<!-- /identity-intelligence-coordination:v1 -->

## Completion requirements

- [ ] All 18 implementation issues meet their acceptance criteria and include actual validation evidence.
- [ ] Reproduced authority-boundary cases have regression coverage, and the qualified visual environment passes with human-owned baseline approval.
- [ ] Standalone installation, Make, Task, and supported consumer recovery are documented and exercised.
- [ ] Required checks pass; optional experience/platform gaps remain explicitly recorded rather than reported as successful validation.
- [ ] Existing strengths remain intact: approvals/drift guards, deterministic generation, immutable release identity, provenance/checksums, and meaningful offline tests.

## Deferred Realm/Aether follow-up

After stabilization, open a separate issue to design shared development-environment preparation in `egohygiene/realm`, coordinated with Aether. Inventory the actual contracts, distinguish common immutable base/toolchain preparation from repository-specific commands, map cloud restoration and standalone/Make/Task consumers, and verify representative repositories before migrating. Retain portable repository entry points. This is deferred design work, not an implemented integration; it should not delay the current repairs.

## Historical audit snapshot

The repository audit was not committed at publication time. Its complete text is included below so the issues have durable evidence without linking to a nonexistent repository file. Statements about no issues or remediation having been created describe the original audit's scope and timestamp.

<details>
<summary>Complete repository-health audit, 2026-10-03T16:29:58Z</summary>

---
audit_name: repository-health
status: complete
strategy: holistic
depth: standard
repository: egohygiene/identity
commit: 320dc5e94843198893ff7216f22d1d3d58a04be4
created_at: 2026-10-03T16:29:58Z
specification: https://github.com/egohygiene/aether/blob/087bceccd936922371155e69dc92ff802aa8a029/library/organization/specs/quality/auditor.spec.md
specification_version: 2.0.0
specification_sha256: f9f4d56673cefac4233fad4d53c78d1ba0726201b7e097bb78f67a721b81e62f
---

# Identity repository health audit

## Executive summary

Identity has a substantial, tested local compiler and projection system, clear
ownership contracts, and useful reproducibility and approval safeguards. The
highest-priority improvements concern boundaries between those systems:

1. Public-boundary Rust projections retain internal and unapproved guidance,
   even when the source passes the complete validator.
2. The v1 CLI does not enforce the source-validation precondition its adapter
   assumes. Unsupported schemas, unrelated approval subjects, and source
   symlinks can generate outputs and subsequently pass `v1-verify`.
3. Recovery trusts journal destinations enough to delete canonical source.
   A synthetic journal containing a `.identity/` create action was accepted by
   the public recovery API and deleted a temporary canonical sentinel.

These are observed local behaviors, not claims of compromise or exposure on a
deployed site. Repair the authority boundaries before broad refactors. Then
align source digests, immutable renderer inputs, recovery usability, and the
browser environment. Follow with documentation, automation, and module cleanup.

There are **14 improvement findings: 3 high, 8 medium, and 3 low**, plus **3
informational positive observations**. No critical finding is asserted.

The standard checks passed: 43 Rust tests; 85 Python tests with one additional
skip; 21 renderer unit tests; formatting, Clippy, both renderer builds, and
public package verification. Five browser checks passed and the screenshot
check failed. Passing existing tests does not cover the newly reproduced
boundary defects.

## Scope and request

- **Requested:** scan Identity for improvements, refactors, cleanup, and related
  concerns; write an audit in this repository using the Aether auditor spec.
- **Inferred defaults:** audit name `repository-health`, holistic strategy,
  standard depth, Markdown output, local evidence, and no remediation.
- **Included:** entry documentation; active architecture and governance;
  representative contracts and profiles; manifests and pins; the seven CI
  workflows; Rust source adapter/compiler/filesystem/public projections;
  Python validation and projection boundaries; renderer input handling and
  representative UI/tests; portable development setup; prior audit discovery.
- **Sampling:** quality and motion interfaces and their tests, contract families,
  large Python modules, and asset/provenance metadata were reviewed selectively.
  This is a complete standard-depth audit of that scope, not a line-by-line
  proof of every source file or an exhaustive security assessment.
- **Excluded:** generated `target/`, `node_modules/`, `dist/`, `.cache/`, browser
  reports, and bytecode from source review; exhaustive image/font inspection;
  hosted services, release publication, sibling implementations, and remote
  administrative settings. Generated evidence was inspected when relevant.
- **Constraints:** only this new report is written into the repository. No
  application, test, fixture, manifest, lockfile, workflow, or historical report
  was edited. Temporary adversarial consumers and a recovery harness were
  created under `/tmp`. No issues, commits, pushes, or releases were created.

## Repository context and historical awareness

The audited checkout is `main` at the commit recorded above and was clean before
the audit. Identity's product boundary is consumer-owned intent, deterministic
compiler/projections, and a replaceable public renderer. The CLI includes v0
commands and a v1 consumer bridge; Python owns the complete offline source
diagnostics. Rust is pinned to 1.97.1. The renderer declares pnpm 11.21.0 and
Node >=24; the separate experience declares pnpm 11.24.0 and Node >=24.15.0.

No `AGENTS.md` was found under the available `/workspace` checkouts. Repository
governance is available in `AI_CONSTITUTION.md`, architecture documents, and
ADRs. No repository-local agent/skill directory was discovered in the tracked
file inventory. Absence of local agent instructions is context, not a defect.

`audits/` did not exist before this report. Consequently every finding has
history **new**. Recurring, changed, apparently resolved, and unable-to-verify
historical classifications are not applicable. Earlier onboarding observations
in this chat are not prior repository audit reports.

## Methodology

Discovery followed the specification's order: entry documentation; architecture
and system documents; governance and decisions; specifications; agent/skill
discovery; automation; manifests; CI/CD; source; tests; remaining documentation;
and prior-audit discovery before writing the report. Previously prepared tools
were reused; dependency upgrades were not performed.

The Aether spec was fetched from `main`, then fetched again at the recorded
immutable Aether commit; the two files were byte-identical. Source evidence
refers to the audited Identity commit. Local path links below are navigation
aids; the recorded commit is the historical baseline.

Evidence labels mean:

- **Observed:** inspected source/configuration or executed local behavior.
- **Inferred:** a consequence or risk supported by observations but not
  reproduced end to end.
- **Recommended:** a proposed change, not implemented by this audit.
- **Unverified:** a validation, deployment condition, or scenario not executed.

## Overall assessment

The repository is workable for development and has strong deterministic and
contract tests. Its public/review separation and recovery source protection
are not consistently enforced across adapters. Documentation sometimes
describes historical capability state as current. Cross-language contracts and
portable setup deserve direct integration tests, rather than only tests of
their individual pieces. No coverage percentage, exploitability score, or
production-readiness certification is assigned.

## Findings summary

| ID | Title | Classification | Severity | Confidence | Status |
| --- | --- | --- | --- | --- | --- |
| AUDIT-001 | Internal guidance enters public-boundary Rust output | confirmed defect | high | high | confirmed |
| AUDIT-002 | v1 generate/verify bypass complete source validation | confirmed defect | high | high | confirmed |
| AUDIT-003 | Recovery journal can target canonical source | confirmed defect | high | high | confirmed |
| AUDIT-004 | Rust and Python disagree on legacy-file source digest | confirmed defect | medium | high | confirmed |
| AUDIT-005 | Design-system inputs are not bound to the displayed release | confirmed defect | medium | high | confirmed |
| AUDIT-006 | Generic asset paths can escape the supplied base | architectural concern | medium | high | confirmed |
| AUDIT-007 | Interrupted CLI consumers have no recovery command | documentation gap | medium | high | confirmed |
| AUDIT-008 | Transaction workspace assumes trusted, serialized access | architectural concern | medium | medium | needs-validation |
| AUDIT-009 | Screenshot environment is not fully reproducible | maintainability risk | medium | high | confirmed |
| AUDIT-010 | Portable setup entry points lack direct CI coverage | maintainability risk | low | high | confirmed |
| AUDIT-011 | Active architecture documents contradict shipped state | documentation gap | medium | high | confirmed |
| AUDIT-012 | Parallel large modules duplicate boundary semantics | maintainability risk | low | high | confirmed |
| AUDIT-013 | One-time guidance rewrite workflows remain active definitions | maintainability risk | low | high | confirmed |
| AUDIT-014 | Docker default contradicts image-digest pinning policy | confirmed defect | medium | high | confirmed |
| AUDIT-015 | Compiler guards approvals, drift, and failed rendering | positive observation | informational | high | confirmed |
| AUDIT-016 | Release publisher resolves immutable source and provenance | positive observation | informational | high | confirmed |
| AUDIT-017 | Meaningful local tests and portable setup already exist | positive observation | informational | high | confirmed |

## High-severity findings

### AUDIT-001 — Internal guidance enters public-boundary Rust output

- **Classification:** confirmed defect. **Severity:** high. **Confidence:** high.
  **Status:** confirmed. **History:** new.
- **Area:** privacy, approval governance, public projections.
  **Effort:** medium. **Impact:** high.
- **Observation:** The fully valid minimal consumer contains internal candidate,
  rejected, superseded, and legacy guidance. The Rust bridge reads its complete
  voice/usage documents, and Rust package/view-model projection preserves those
  objects rather than applying an approved/public audience boundary.
- **Evidence — observed:** `src/v1_consumer.rs:59` constructs raw guidance;
  [render.rs](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/src/brandkit/render.rs#L108) serializes voice/usage directly and
  its Markdown helper at line 427 serializes them again.
  [reference_renderer.rs](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/src/reference_renderer.rs#L189) forwards them into
  a public view model. `renderer/src/app.js:827` renders declared guidance.
  In a temporary copy of the valid fixture, validation and generation both
  exited 0. The internal candidate text `Your brand system, ready when you are.`
  appeared in `packages/guidance/README.md`, `packages/guidance/voice-and-usage.json`,
  and `packages/renderer/brand-kit.view-model.json`. The Python
  `render_guidance.py --audience public --format json` output excluded it.
- **Why it matters — inferred:** Consumers distributing these packages or
  renderer inputs can distribute unapproved/internal source material. This
  contradicts the [guidance contract](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/docs/contracts/GUIDANCE_V1.md#renderer-model)
  public-audience rule; source validity alone does not make every record public.
- **Recommendation — recommended:** Make public/review audience explicit in the
  Rust projection boundary, share the governed projection semantics, and filter
  nested records and referenced approval evidence before serialization. Preserve
  full review history only in an explicitly named review output.
- **Suggested validation — unverified repair:** From one valid mixed-lifecycle
  consumer, check JSON, Markdown, renderer model, rendered HTML, and archives
  for absence of internal/unapproved records; verify review output retains them.
- **Dependencies or risks:** Filtering must preserve schema compatibility and
  approved contextual guidance. Fixing AUDIT-002 alone does not fix this case:
  the input already passes the complete validator. No production leakage was
  inspected or asserted.

### AUDIT-002 — v1 generate/verify bypass complete source validation

- **Classification:** confirmed defect. **Severity:** high. **Confidence:** high.
  **Status:** confirmed. **History:** new.
- **Area:** source validation, approval authority, filesystem trust.
  **Effort:** medium. **Impact:** high.
- **Observation:** Both CLI commands load a raw repository and pass the same
  `V1ConsumerPipeline` as reader, validator, and resolver. Its validator returns
  a default success report based on the comment that preflight already happened.
  The CLI does not enforce that precondition. Its path helper performs textual
  checks but does not reject symlink components.
- **Evidence — observed:** [commands.rs](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/src/commands.rs#L192),
  [v1_consumer.rs](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/src/v1_consumer.rs#L146), its `approved_decisions` helper,
  and `path_field` at line 495. The complete Python resolver rejects symlinks
  at `scripts/validate_identity.py:560`. Temporary unsupported-schema,
  unrelated-approval-subject, and symlinked-token consumers each failed the
  Python validator but generated 13 projections and passed `v1-verify`.
- **Why it matters — inferred:** A successful generator/verification result can
  be mistaken for valid governed source; merely approved decision IDs do not
  establish approval of the right subject. A source symlink also permits
  following content outside the consumer tree. The probe used only synthetic
  local token bytes, not private machine files.
- **Recommendation — recommended:** Enforce complete preflight at the CLI and
  reusable adapter boundary, or require a trustworthy validated-source input
  bound to the current source digest. Reuse authoritative diagnostics and safe
  path semantics rather than adding another incomplete schema validator.
- **Suggested validation — unverified repair:** Require nonzero generate and
  verify exits for all three reproduced invalid cases, stale layer digests,
  missing override approvals, and changed source after preflight. Confirm no
  generated mutation occurs and valid standalone consumers remain supported.
- **Dependencies or risks:** The docs do instruct consumers to run validation
  first, which mitigates correctly scripted use; it does not enforce CLI/library
  use. Preserve the offline standalone distribution contract when selecting
  how to integrate the Python-owned diagnostics.

### AUDIT-003 — Recovery journal can target canonical source

- **Classification:** confirmed defect. **Severity:** high. **Confidence:** high.
  **Status:** confirmed. **History:** new.
- **Area:** recovery, source ownership, destructive authority.
  **Effort:** medium. **Impact:** high.
- **Observation:** Recovery checks the journal schema, then resolves each action
  as a portable repository-relative path and performs its operation. It does not
  reject canonical `.identity/` destinations or bind all destinations to an
  authorized generated-output scope before mutation.
- **Evidence — observed:** [filesystem.rs](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/src/compiler/filesystem.rs#L211)
  and lines 256–283; `resolve` at line 58 checks symlink traversal but not source
  ownership; `src/compiler/mod.rs:1421` checks path syntax. A temporary journal
  with `operation: create` and `path: .identity/audit-sentinel.txt` returned
  `Ok(RecoveryReport { recovered_transactions: 1, ... })`; its synthetic canonical
  sentinel no longer existed. The legitimate interruption test at
  `src/compiler/tests.rs:520` does not cover adversarial journal destinations.
- **Why it matters — inferred:** Corrupt or attacker-supplied transient recovery
  data can cross into canonical source when a caller invokes the public recovery
  API. The [compiler contract](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/docs/contracts/COMPILER_V1.md#transaction-and-recovery-boundary)
  says recovery never writes canonical source. No attacker access to a deployed
  system is assumed; the precondition is an untrusted journal plus recovery.
- **Recommendation — recommended:** Validate the complete journal and allowed
  output/manifest scope before any destructive operation. Reject canonical and
  unrelated repository paths, invalid plan identities, duplicate/conflicting
  actions, and untrusted backup paths. Treat corrupted journals as blocked
  evidence requiring explicit diagnosis.
- **Suggested validation — unverified repair:** Exercise create/replace/remove
  actions and manifest paths targeting `.identity/` and unrelated user files.
  Each must fail before any mutation, preserving sentinels and backups. Retain
  successful legitimate recovery and repeatability tests.
- **Dependencies or risks:** Existing interrupted transactions may need a
  versioned migration or explicit recovery scope. Do not expose a new convenient
  CLI recovery command before addressing this finding.

## Medium-severity findings

### AUDIT-004 — Rust and Python disagree on legacy-file source digest

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high.
  **Status:** confirmed. **History:** new.
- **Area:** cross-language compatibility, reproducibility.
  **Effort:** small. **Impact:** medium.
- **Observation:** Rust excludes root `.identity/identity.toml` from canonical
  digest input. Python's compiler-compatible digest excludes README files,
  candidates, references, and symlinks, but includes that TOML file.
- **Evidence — observed:** [v1_consumer.rs](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/src/v1_consumer.rs#L392), especially
  line 427; [render_design_system.py](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/scripts/render_design_system.py#L54).
  A valid temporary v1 consumer with a synthetic legacy TOML file validated and
  generated successfully. Rust digest was
  `1002ff75ea51f6e016929894ea30cc96565bdbbca749a0e7fff1ebd0d2f21353`;
  Python digest was
  `fd195184e41b435616ec1cb3387c7897b6471601b3c908b8322c6b40e03f6397`.
- **Why it matters — inferred:** Independently generated guidance and packages
  can disagree about the identity of the same consumer source; stricter release
  binding can reject valid mixed v0/v1 consumers.
- **Recommendation — recommended:** Specify one canonical inventory and byte
  framing, including legacy files, symlinks, Unicode paths, and exclusions; add
  shared digest vectors used by both implementations.
- **Suggested validation — unverified repair:** Compare Rust/Python digests for
  normal, legacy-coexistence, README, candidates/references, nested, and
  adversarial symlink inventories on supported operating systems.
- **Dependencies or risks:** Changing digest semantics invalidates existing
  release bindings; document/version that transition instead of silently
  recalculating historical releases. Coordinate with AUDIT-002 and AUDIT-005.

### AUDIT-005 — Design-system inputs are not bound to the displayed release

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high.
  **Status:** confirmed. **History:** new.
- **Area:** renderer, immutable release compatibility.
  **Effort:** small. **Impact:** medium.
- **Observation:** The renderer checks a design-system project's identity and
  the context digest's syntax but does not compare that digest with the Brand
  Kit release. The adjacent Press Kit integration does compare its source digest.
- **Evidence — observed:** [model.js](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/renderer/src/model.js#L51) and its
  Press Kit check at line 76; `renderer/src/design-system.js:58` validates schema
  linkage and digest syntax. A same-project design context with a digest of
  64 zeroes was accepted alongside fixture release digest
  `545e54ad462fa84807ef594110a6742bf861bdf90a7e71fd60e1729b05d58516`.
- **Why it matters — inferred:** A release page can combine current assets with
  stale design guidance and label the combination as canonical.
- **Recommendation — recommended:** Require compatible source/release identity
  for the design-system projection before rendering, consistently with the
  Press Kit boundary. Define whether the handbook also needs explicit binding.
- **Suggested validation — unverified repair:** Same project plus different
  digest must fail; a matching projection must render and download correctly.
- **Dependencies or risks:** Fix AUDIT-004 or provide an explicit compatibility
  transition so legitimate legacy consumers do not fail on inconsistent digests.

### AUDIT-006 — Generic asset paths can escape the supplied base

- **Classification:** architectural concern. **Severity:** medium. **Confidence:** high.
  **Status:** confirmed. **History:** new.
- **Area:** renderer input validation, download boundaries.
  **Effort:** small. **Impact:** medium.
- **Observation:** `joinAssetUrl` strips leading slashes but accepts parent
  traversal and URL-shaped values. Generic model validation checks basic shape
  rather than normalizing each asset/package path. Press Kit paths have more
  restrictive handling than generic assets.
- **Evidence — observed:** [model.js](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/renderer/src/model.js#L137),
  `contracts/v1/brand-kit-view-model.schema.json:281`, and
  `renderer/src/press-kit.js:102`. A direct call with base
  `https://cdn.example.test/brand/` and path `../outside.svg` returned
  `https://cdn.example.test/outside.svg`. No network request was made.
- **Why it matters — inferred:** A malformed imported view model can direct a
  download outside its intended bundle prefix. A constrained download boundary
  should be consistent across optional and core projections. No XSS, SSRF, or
  remote content execution is claimed by this probe.
- **Recommendation — recommended:** Centralize normalized artifact-path checks,
  reject dot segments and unexpected schemes, and distinguish an explicitly
  configured remote base from a path supplied by the model.
- **Suggested validation — unverified repair:** Cover parent traversal, absolute
  URLs, protocol-relative paths, encoded separators, backslashes, and valid
  route-prefixed/CDN downloads; validate imported models before rendering.
- **Dependencies or risks:** Preserve supported remote base URLs and existing
  generated package links; clarify any intentional external-download contract.

### AUDIT-007 — Interrupted CLI consumers have no recovery command

- **Classification:** documentation gap. **Severity:** medium. **Confidence:** high.
  **Status:** confirmed. **History:** new.
- **Area:** CLI usability, interrupted-generation recovery.
  **Effort:** medium. **Impact:** medium.
- **Observation:** The filesystem implementation and errors tell users to run
  explicit recovery. The public CLI has generation and verification, but no
  recovery operation. Recovery currently requires a Rust API caller.
- **Evidence — observed:** `src/compiler/filesystem.rs:342`,
  `src/compiler/filesystem.rs:496`, [cli.rs](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/src/cli.rs), and the executed
  `identity --help` inventory. The compiler contract describes an explicit
  recovery boundary without a consumer CLI recipe.
- **Why it matters — inferred:** A user of the distributed binary can be blocked
  by an interrupted workspace without a supported, reviewable route forward.
- **Recommendation — recommended:** After recovery hardening, expose a scoped
  inspection/recovery command or document a supported companion tool, with
  diagnostic context and an explicit mutation boundary.
- **Suggested validation — unverified repair:** Interrupt a temporary generation,
  inspect recovery state, recover through the documented consumer path, and
  regenerate successfully while preserving canonical and unrelated files.
- **Dependencies or risks:** Depends on AUDIT-003; avoid a blind recursive-delete
  workaround or silent automatic rollback.

### AUDIT-008 — Transaction workspace assumes trusted, serialized access

- **Classification:** architectural concern. **Severity:** medium. **Confidence:** medium.
  **Status:** needs-validation. **History:** new.
- **Area:** filesystem confinement, concurrent generation.
  **Effort:** medium. **Impact:** high.
- **Observation:** Published artifact paths receive symlink-component checks;
  transaction paths are formed by direct joins. `commit` checks recovery state
  and later calls `create_dir_all` on a plan-digest directory without an exclusive
  reservation or visible per-consumer writer lock.
- **Evidence — observed:** [filesystem.rs](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/src/compiler/filesystem.rs#L50),
  lines 58–76, 313–342, and 388–403. No lock/create-new operation was found in
  this implementation. Source checksums are rechecked, which is a useful guard
  but does not reserve the transaction namespace.
- **Why it matters — inferred:** Concurrent writers may pass the precheck before
  either creates its workspace; symlinked cache components may redirect staging
  and backups. Neither a concurrent-corruption case nor redirected-write case
  was reproduced in this audit; that runtime evidence is missing.
- **Recommendation — recommended:** Establish a single-writer contract through
  an exclusive lock/reservation, or explicitly document and enforce serialized
  use. Apply confinement checks to transaction roots, staging, and backups.
- **Suggested validation — unverified:** Coordinate two writers at the precheck
  boundary; inject cache-component symlinks to a synthetic external directory;
  require safe rejection and intact outputs/source. Include interrupted-lock
  handling without deleting another writer's workspace.
- **Dependencies or risks:** Coordinate with AUDIT-003 and preserve legitimate
  recovery. Decide how supported filesystems and externally located caches fit
  the intended contract before changing behavior.

### AUDIT-009 — Screenshot environment is not fully reproducible

- **Classification:** maintainability risk. **Severity:** medium. **Confidence:** high.
  **Status:** confirmed. **History:** new.
- **Area:** visual evidence, CI, developer experience.
  **Effort:** medium. **Impact:** medium.
- **Observation:** Playwright is pinned, but reference CI uses `ubuntu-latest`
  and Node major 24 without a fixed browser container/font environment. ADR-011
  calls for pinned browser/container conditions and fixed fonts and settings.
- **Evidence — observed:** [reference-renderer.yml](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/.github/workflows/reference-renderer.yml#L85),
  [playwright.config.js](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/renderer/playwright.config.js), and
  [ADR-011](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/docs/decisions/ADR-011-accessibility-and-visual-evidence.md).
  Fresh local E2E ran six checks: five passed, and screenshot comparison failed
  with 46,969 differing pixels on a 1440×1000 viewport. This cloud host has a
  custom generic sans-serif substitution. Earlier same-session font diagnosis
  reduced the difference to 156 pixels but did not make the test pass.
- **Why it matters — inferred:** A visual failure can reflect host rendering
  rather than product change; moving runner defaults also weakens reproducible
  baseline review. Current hosted CI results were not inspected.
- **Recommendation — recommended:** Record and pin the qualified browser image,
  fonts, locale, timezone, scale, and color settings. Use the same profile locally
  and in CI. Preserve the approved screenshot instead of relaxing assertions.
- **Suggested validation — unverified repair:** Run the unchanged baseline in
  the same qualified environment locally and in CI; then confirm a deliberate
  visual change is detected and requires review.
- **Dependencies or risks:** Baseline approval remains human-owned; record
  whether residual differences are browser/font versions or rasterization.

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

### AUDIT-014 — Docker default contradicts image-digest pinning policy

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high.
  **Status:** confirmed. **History:** new.
- **Area:** dependency policy, reproducible development images.
  **Effort:** small. **Impact:** medium.
- **Observation:** The portable Docker add-on's default base is the mutable
  `node:24-bookworm` tag. The repository's dependency policy explicitly says
  container images use digests; no exception for this default was found.
- **Evidence — observed:** [Dockerfile](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/dev/Dockerfile#L5) and
  [DEPENDENCY_POLICY.md](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/docs/DEPENDENCY_POLICY.md#security-and-supply-chain)
  line 91. Configurable `BASE_IMAGE` already permits a digest, but does not make
  the default immutable. Earlier same-session Docker verification qualified a
  specific locally prepared proxy-trusted base, not every future tagged image.
- **Why it matters — inferred:** A later build can change Node/Corepack, OS
  libraries, or fonts without changing repository files, reproducing the kinds
  of proxy/font variation already encountered in this environment.
- **Recommendation — recommended:** Use a qualified digest by default, or
  require explicit base selection and document a reviewed policy exception for
  exploratory tags. Preserve the ability to extend the user's custom base.
- **Suggested validation — unverified repair:** Build against the recorded
  immutable base; record runtime versions and run CLI/renderer smoke checks.
  Confirm a different custom base can be selected explicitly.
- **Dependencies or risks:** Digest updates need a refresh process; proxy CA
  trust and development-user permissions remain base-image responsibilities.

## Low-severity findings

### AUDIT-010 — Portable setup entry points lack direct CI coverage

- **Classification:** maintainability risk. **Severity:** low. **Confidence:** high.
  **Status:** confirmed. **History:** new.
- **Area:** setup automation, CI parity.
  **Effort:** medium. **Impact:** medium.
- **Observation:** Existing workflows validate the product with their own
  commands, but do not directly exercise `scripts/dev-env.sh`, Make, Task, or
  the Docker add-on. The helper's `check` covers product tests but omits several
  root CI integrity validators; it is not a complete CI-equivalent target.
- **Evidence — observed:** [dev-env.sh](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/scripts/dev-env.sh#L67),
  [validate.yml](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/.github/workflows/validate.yml#L50),
  [release.yml](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/.github/workflows/release.yml), and all workflow command
  inventories. No helper invocation was found. This does not negate the earlier
  successful local standalone/Make/Task/Docker verification.
- **Why it matters — inferred:** Future setup changes can pass product CI while
  breaking activation, frontend dispatch, cache ownership, or base integration.
- **Recommendation — recommended:** Add bounded setup smoke checks, argument
  dispatch/shell checks, and a representative clean-base test. Either expose a
  documented CI-equivalent check or clearly name local versus full validation.
- **Suggested validation — unverified repair:** Introduce an invalid helper
  command/version binding and show CI fails; verify repeated setup and the three
  entry points, without duplicating every expensive product suite/image build.
- **Dependencies or risks:** Keep OS privilege requirements and optional browser
  installs distinct; use the standard shared resource budget.

### AUDIT-012 — Parallel large modules duplicate boundary semantics

- **Classification:** maintainability risk. **Severity:** low. **Confidence:** high.
  **Status:** confirmed. **History:** new.
- **Area:** refactoring, cross-language contract maintenance.
  **Effort:** large. **Impact:** medium.
- **Observation:** The stdlib validator is 4,774 lines spanning tokens,
  governance, guidance, channels, social surfaces, presentation, and mascots.
  Compiler and quality modules are 1,486 and 1,451 lines; renderer `app.js` is
  1,145 lines. Size alone is not the defect: distinct implementations already
  disagree on public audience handling and canonical source inventory.
- **Evidence — observed:** `scripts/validate_identity.py:1033`, line 1268 and
  line 4688; `src/v1_consumer.rs:392`; `scripts/render_design_system.py:54`;
  `src/brandkit/render.rs:108`; `scripts/render_guidance.py:56`. Reproductions
  in AUDIT-001 and AUDIT-004 establish semantic duplication costs.
- **Why it matters — inferred:** Changes to a contract require updates across
  large modules and language boundaries, making partial fixes easier to miss.
- **Recommendation — recommended:** Stabilize the reproduced invariants first,
  then extract source I/O/digest, tokens, governance, projection audience, and
  presentation components behind existing entry points. Share conformance
  vectors rather than coupling unrelated v0/v1 profiles or introducing a new
  runtime dependency solely for code organization.
- **Suggested validation — unverified repair:** Keep CLI imports, diagnostic
  codes/order, fixture behavior, and generated bytes stable throughout small
  refactor steps; run shared cross-language fixtures after each extraction.
- **Dependencies or risks:** Avoid a broad rewrite before high-severity repairs.
  Stdlib/offline operation and extraction-provenance checks constrain moves.

### AUDIT-013 — One-time guidance rewrite workflows remain active definitions

- **Classification:** maintainability risk. **Severity:** low. **Confidence:** high.
  **Status:** confirmed. **History:** new.
- **Area:** CI cleanup, least privilege, historical documentation automation.
  **Effort:** small. **Impact:** low.
- **Observation:** Two workflows target `feat/13-brand-guidance-v1`, embed
  historical prose replacements, grant `contents: write`, commit README/ROADMAP
  changes, and push to that feature branch.
- **Evidence — observed:** [refine-guidance-docs.yml](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/.github/workflows/refine-guidance-docs.yml#L4)
  lines 11–22 and 177–178;
  [refine-guidance-docs-v2.yml](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/.github/workflows/refine-guidance-docs-v2.yml#L4)
  lines 11–22 and 176–177. These are not general-purpose doc validators.
- **Why it matters — inferred:** One-time automation adds persistent maintenance
  and write-capability surface with little current development value. Whether
  the remote branch still exists or these workflows currently execute is unverified.
- **Recommendation — recommended:** Confirm no ongoing owner needs them, then
  retire/archive the rewrite logic and retain current documentation validation
  in read-only workflows. Preserve history through Git, not executable rewrites.
- **Suggested validation — unverified repair:** Inventory retained workflow
  triggers/permissions and confirm guidance/documentation checks still run.
- **Dependencies or risks:** Check for outstanding historical branch work before
  removal; this audit did not change or trigger either workflow.

## Positive observations

### AUDIT-015 — Compiler guards approvals, drift, and failed rendering

- **Classification:** positive observation. **Severity:** informational.
  **Confidence:** high. **Status:** confirmed. **History:** new.
- **Area:** compiler authority, deterministic generation.
  **Effort:** small. **Impact:** high.
- **Observation:** The general compiler explicitly plans unmanaged replacement,
  drift, removal approvals, adapter compatibility, and rendering verification
  before mutation; normal interruption recovery has coverage.
- **Evidence — observed:** `docs/contracts/COMPILER_V1.md:61`,
  `src/compiler/tests.rs:265`, line 428 and line 520; corresponding Rust tests
  passed in this audit, including deterministic and incremental scenarios.
- **Why it matters — inferred:** These existing seams and tests support focused
  boundary repairs instead of replacing the compiler architecture.
- **Recommendation — recommended:** Preserve the explicit stage/approval model
  and add the adversarial source/journal scenarios to its conformance suite.
- **Suggested validation — unverified future regression:** Require current
  approval, drift, deterministic, incremental, and interruption tests to remain
  green while correcting AUDIT-001–AUDIT-003.
- **Dependencies or risks:** This strength applies to the general compiler,
  not every adapter precondition or malformed recovery journal.

### AUDIT-016 — Release publisher resolves immutable source and provenance

- **Classification:** positive observation. **Severity:** informational.
  **Confidence:** high. **Status:** confirmed. **History:** new.
- **Area:** publication, supply-chain provenance.
  **Effort:** small. **Impact:** high.
- **Observation:** Publication resolves stable release tags/commits and checks
  release-bound configuration; release packaging has license inventory, SBOM,
  checksums, and build-provenance attestation steps. Actions are SHA-pinned.
- **Evidence — observed:** [.github/workflows/publish-brand-kit.yml](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/.github/workflows/publish-brand-kit.yml),
  [.github/workflows/release.yml](https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/.github/workflows/release.yml),
  `scripts/verify_publication_release_configs.py`, and the passing local public
  package/configuration checks. Workflow definitions were inspected, not run.
- **Why it matters — inferred:** Release identity and provenance can remain
  stable while development setup and renderer internals are improved.
- **Recommendation — recommended:** Keep immutable release/source checks and
  extend them to every optional renderer projection.
- **Suggested validation — unverified future regression:** Continue negative
  tests for wrong tag/commit/config bindings; exercise any release process only
  in a separately authorized release task.
- **Dependencies or risks:** Workflow source is not proof of successful hosted
  runs, correct administrative settings, or current live artifact integrity.

### AUDIT-017 — Meaningful local tests and portable setup already exist

- **Classification:** positive observation. **Severity:** informational.
  **Confidence:** high. **Status:** confirmed. **History:** new.
- **Area:** developer experience, testing, standalone operation.
  **Effort:** small. **Impact:** high.
- **Observation:** The repository has executable deterministic/compiler tests,
  Python contract and projection tests, cross-language renderer integration,
  browser accessibility checks, and a shared standalone/Make/Task setup helper.
- **Evidence — observed:** `tests/v1_consumer.rs`,
  `renderer/tests/design-system.integration.test.js`,
  `renderer/tests/press-kit.integration.test.js`, `scripts/dev-env.sh`, and the
  executed results in the validation notes. Test runners executed real tests;
  renderer configuration sets `passWithNoTests: false`.
- **Why it matters — inferred:** Refactors can be guided by executable evidence
  and installed offline dependencies instead of manual reproduction alone.
- **Recommendation — recommended:** Extend those suites at adapter crossings
  and make the qualified visual environment reproducible.
- **Suggested validation — unverified future regression:** Preserve meaningful
  test counts/targets and report skips/failures independently after changes.
- **Dependencies or risks:** Existing positive test results do not establish
  exhaustive input coverage or qualify the separate Holon experience.

## Opportunities by area

| Area | Improvement direction | Findings |
| --- | --- | --- |
| Governance/privacy | One explicit public/review projection contract | AUDIT-001, AUDIT-002 |
| Filesystem/recovery | Validate recovery scope first; safe consumer recovery; reserve writer state | AUDIT-003, AUDIT-007, AUDIT-008 |
| Compatibility | Shared digest vectors and immutable optional-input binding | AUDIT-004, AUDIT-005 |
| Renderer | Consistent model/path validation and qualified visual evidence | AUDIT-005, AUDIT-006, AUDIT-009 |
| Developer tooling | Direct setup CI, documented check coverage, immutable base identity | AUDIT-010, AUDIT-014 |
| Documentation | Reconcile current capability/route ownership; label historical context | AUDIT-011 |
| Refactoring/cleanup | Domain extraction after invariant fixes; retire one-time rewrites | AUDIT-012, AUDIT-013 |

The eventual Realm/Aether development-environment refactor discussed during
setup should remain deferred until these workflows stabilize. Record the
shared base/toolchain responsibilities versus repository-specific commands
before migrating the portable helper. This is a future design direction, not
an implemented integration or an invented Realm/Aether API. It should not delay
public-data and recovery fixes.

## Suggested issue backlog

These are proposed issues only; none was created.

| Priority | Candidate | Source findings | Dependencies | Outcome and acceptance criteria |
| --- | --- | --- | --- | --- |
| P1 | Enforce public/review guidance isolation in Rust | AUDIT-001 | Stable guidance contract | Valid mixed-lifecycle input produces no internal/unapproved data in public JSON, Markdown, HTML, view models, or archives; review history remains available |
| P1 | Require validated source for v1 CLI/library execution | AUDIT-002 | Standalone distribution design | Invalid schema/approval subject/symlink/layer digest fails before generated writes; valid consumers retain stable diagnostics |
| P1 | Constrain recovery journal mutation authority | AUDIT-003 | Generated-scope contract | Malformed actions and manifest destinations cannot mutate canonical/unrelated files; full preflight precedes all mutations; legitimate recovery still passes |
| P2 | Publish shared source-digest conformance vectors | AUDIT-004 | Source inventory/version decision | Rust/Python agree for mixed legacy, transient, and adversarial inventories; compatibility transition is explicit |
| P2 | Bind optional design-system guidance to the release | AUDIT-005 | AUDIT-004 | Same-project wrong-digest projection is rejected; matching projection works |
| P2 | Validate generic artifact paths before rendering | AUDIT-006 | Download-path contract | Traversal/unexpected URL inputs fail while route-prefixed and explicit CDN bases work |
| P2 | Add safe CLI recovery and workspace serialization | AUDIT-007, AUDIT-008 | AUDIT-003 | Consumer can inspect/recover interrupted state; concurrency/cache-redirection scenarios are either safely supported or explicitly rejected |
| P2 | Qualify one reproducible browser/font profile | AUDIT-009 | Human baseline review | Existing screenshot passes in qualified local/CI environments; real visual changes remain detectable |
| P2 | Reconcile active capability and route documentation | AUDIT-011 | Maintainer ownership decision | Current docs agree with implementation and publication configs; historical observations remain clearly dated |
| P2 | Pin the default development base identity | AUDIT-014 | Base refresh policy | Qualified immutable base builds/smokes; custom base override remains supported |
| P3 | Exercise portable setup entry points in CI | AUDIT-010 | Representative base/profile | Standalone/Make/Task and repeated setup are covered without excessive duplicate builds; local/full validation coverage is documented |
| P3 | Extract focused validator/projection/presentation modules | AUDIT-012 | High/P2 invariant fixes | Existing entry points, diagnostics, generated bytes, and cross-language conformance remain stable |
| P3 | Retire completed feature-branch doc rewrite workflows | AUDIT-013 | Confirm historical owner/branch work | Remaining workflows retain current checks and least required permissions |

## Deferred or out-of-scope observations

- No live deployment, organization route, GitHub branch protection, release
  attestation verification, or hosted CI run was inspected. Repository
  definitions alone do not establish those external outcomes.
- No fresh third-party advisory database, Cargo audit, npm audit, fuzzing,
  exhaustive schema-conformance review, or performance/memory benchmark was
  run. No vulnerability count or exploitability claim is derived from prior
  Git push notices or dependency versions.
- macOS/Windows release jobs and standalone release-smoke packaging were not
  executed during this audit; native Linux checks do not qualify those targets.
- Full Holon composition and Chromium/Firefox/WebKit experience tests require
  the separate exact-pinned source/runtime workflow; they were not run here.
  The Python suite's one skip is the absent local experience artifact.
- Quality's publication renderer checks remain explicit review-required/skipped
  evidence in `src/quality/mod.rs:554`. This is documented progressive coverage,
  not itself a new defect. Wiring structured browser evidence into that report
  is a possible follow-up; this audit does not claim the current release
  workflow consumes the quality evaluator's release decision.
- Process-interruption recovery is not a proven power-loss durability contract.
  No fsync/power-loss qualification was attempted; do not expand the advertised
  guarantees without targeted testing.
- Automatic source repair, broad dependency upgrades, repository-wide module
  rewrites, issue creation, publication, and Realm/Aether centralization are
  outside this audit's authorized actions.

## Uncertainties and clarifications

1. Is complete validation intended to be a documented caller responsibility,
   or an enforced CLI boundary? The present API accepts raw source while its
   implementation assumes prevalidated input; either contract needs an explicit,
   testable authority boundary.
2. Are any generic model downloads intentionally permitted outside their asset
   base? If so, encode that as an explicit variant rather than accepting arbitrary
   path syntax by accident.
3. Is the artifact store explicitly single-writer, and are external cache roots
   supported? AUDIT-008 needs runtime stress/confinement evidence.
4. Which exact font/browser/container combination approved the checked-in
   screenshot? The local rendering mismatch is observed; its full original
   qualification context and current hosted outcome remain unverified.
5. Current canonical site versus organization `/identity/` integration ownership
   should be confirmed while updating active docs. Do not rewrite historical
   ADR intent based only on this audit's inference.

## Evidence index

For immutable source navigation, use
`https://github.com/egohygiene/identity/blob/320dc5e94843198893ff7216f22d1d3d58a04be4/<path>#L<line>`.
The line starts recorded below were read from this checkout; generated sizes and
line counts are observations at this commit, not future thresholds.

| Evidence | Source / observation | Supports |
| --- | --- | --- |
| E01 | README:359; PURPOSE:85; SYSTEM inventory; ARCHITECTURE:102; AI_CONSTITUTION; DECISIONS | Context, AUDIT-011 |
| E02 | GUIDANCE_V1 public/review rules; compiler transaction/recovery contract; IDENTITY_V1 layer rules | AUDIT-001–AUDIT-004 |
| E03 | src/v1_consumer.rs:146, 169, 392, 495; src/commands.rs:192 | AUDIT-002, AUDIT-004 |
| E04 | src/brandkit/render.rs:108, 427; src/reference_renderer.rs:189; renderer/src/app.js:827 | AUDIT-001 |
| E05 | src/compiler/filesystem.rs:50, 58, 211, 256, 313, 328, 388, 496; compiler/tests.rs:520 | AUDIT-003, AUDIT-007, AUDIT-008, AUDIT-015 |
| E06 | scripts/render_design_system.py:54; scripts/render_guidance.py:56; validate_identity.py:560 | AUDIT-001, AUDIT-002, AUDIT-004 |
| E07 | renderer/src/model.js:51, 137; design-system.js:58; press-kit.js path validation | AUDIT-005, AUDIT-006 |
| E08 | Playwright config/tests; reference-renderer.yml:85; ADR-011 | AUDIT-009 |
| E09 | scripts/dev-env.sh:67; Makefile; Taskfile.yml; dev/Dockerfile:5; DEPENDENCY_POLICY:91 | AUDIT-010, AUDIT-014 |
| E10 | validate_identity.py 4,774 lines; compiler/mod.rs 1,486; quality/mod.rs 1,451; app.js 1,145 | AUDIT-012 |
| E11 | Both refine-guidance-docs workflows:4, 11, 22 and final push commands | AUDIT-013 |
| E12 | Release/Pages workflow definitions and local public/config verification | AUDIT-016 |
| R01 | Temporary valid fixture: internal candidate retained in three Rust outputs; Python public output excludes it | AUDIT-001 |
| R02 | Unsupported schema, wrong subjects, symlinked token: validator rejects; generator/verify accept | AUDIT-002 |
| R03 | Synthetic recovery journal: API returns success; canonical sentinel deleted | AUDIT-003 |
| R04 | Added legacy TOML: valid source; unequal Rust/Python digests | AUDIT-004 |
| R05 | Same-project zero digest accepted by renderer design-system validator | AUDIT-005 |
| R06 | joinAssetUrl accepts ../outside.svg and returns a URL outside /brand/ | AUDIT-006 |
| R07 | Fresh standard check and six integrity validators pass; browser 5 pass/1 fail | AUDIT-009, AUDIT-015–AUDIT-017 |

## Reproduction notes

All mutation-based probes operated in fresh temporary copies of
`tests/fixtures/v1/valid/minimal`, never in tracked fixtures. Build the existing
CLI first if necessary, then run the normal validator, `v1-generate`, and
`v1-verify` against the temporary root. Inspect the generated manifest's
`sourceDigest` and compare it with
`render_design_system.canonical_source_digest(root)` from the existing Python
module. Keep any generated output inside that temporary root.

| Probe | Temporary input alteration | Validator | Generate | Verify / additional result |
| --- | --- | --- | --- | --- |
| Public guidance | None; fixture already includes mixed review states | 0 | 0, 13 projections | Internal candidate appears in Rust guidance/model; Python public projection excludes it |
| Unsupported schema | Set identity.json schema to identity.project/v999 | 1, IDN1002 | 0, 13 projections | Verify 0 |
| Approval subject | Set each decision subject to asset:unrelated-audit-subject while retaining status/IDs | 1, includes IDN1404/IDN1602/IDN2002 | 0, 13 projections | Verify 0 |
| Source symlink | Move one token file's identical bytes to another temporary path and replace its declared path with a symlink | 1, IDN1003 | 0, 13 projections | Verify 0; Rust/Python digest disagreement also occurs |
| Legacy digest | Add `.identity/identity.toml` containing `# synthetic legacy file` and a newline | 0 | 0, 13 projections | Verify 0; digests differ as recorded in AUDIT-004 |

The recovery reproduction used a temporary Rust harness linked to the already
built Identity library, importing `ArtifactStore` and `LocalArtifactStore` and
calling `LocalArtifactStore::new(temporary_root).unwrap().recover()`. A fresh
temporary root contained `.identity/audit-sentinel.txt` and this journal under
`.cache/identity/transactions/` followed by 64 `a` characters:

```json
{
  "schema": "identity.compiler-transaction/v1",
  "planDigest": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "manifestPath": "assets/identity/.identity-manifest.json",
  "manifestExisted": false,
  "actions": [{"path": ".identity/audit-sentinel.txt", "operation": "create"}]
}
```

Do not reproduce that journal in a real consumer. The observed temporary
result was success with one recovered transaction and the sentinel removed.

The Node input probes directly imported `assertBrandKitViewModel`,
`createDesignSystemView`, and `joinAssetUrl`. For the design-system case, a copy
of `renderer/fixtures/example.brand-kit.view-model.json` received a same-project
handbook/context with empty supported arrays, correct schemas/schema linkage,
and `context.source.digest = "0".repeat(64)`; assertion returned the model.
For the URL case the exact call was:

```js
joinAssetUrl("https://cdn.example.test/brand/", "../outside.svg")
// Observed: "https://cdn.example.test/outside.svg"
```

## Validation notes

All results below were actually executed during this audit unless expressly
labeled earlier-session evidence. Commands were run from `/workspace/identity`
using the prepared tools. `IDENTITY_DEV_PREFIX=/workspace/.identity-tools`
activated the shared helper; no dependency-refresh/setup command was needed.

| Check | Observed outcome |
| --- | --- |
| `bash scripts/dev-env.sh check` | Exit 0 |
| `cargo fmt --all --check` | Passed |
| `cargo clippy --locked --all-targets --all-features -- -D warnings` | Passed |
| `cargo test --locked --all-features` | 43 passed, 0 failed; binary/doc targets contained 0 tests and are not counted as coverage |
| Python unittest discovery | 86 discovered: 85 passed, 1 skipped; skip is absent optional local experience artifact |
| Minimal v1 fixture validation | Passed |
| Renderer syntax/source check | 17 JavaScript source files checked; syntax only |
| Renderer Vitest | 21 tests passed across 6 files |
| Renderer standard build | Passed |
| Public build and verification | Passed; release v1.0.0, 36 packaged files |
| `verify_release.py` | Passed; explicit tag verification was not requested |
| `verify_docs.py` | Passed before report creation; report links rechecked after writing |
| `verify_mascot.py` | Passed; 3 variants, RGBA transparency |
| `verify_publication_architecture.py` | Passed |
| `verify_publication_release_configs.py` | Passed |
| `verify_extraction.py` | Passed: 17 byte-identical and 3 provenance-tracked evolved files, 8 v0 profiles, 45 targets |
| `bash scripts/dev-env.sh e2e` | Exit 1: 5 passed, exact screenshot failed; 46,969 differing pixels |
| Synthetic boundary probes and guidance projection comparison | Results recorded in R01–R06; observed defects, not passing regression tests |

The browser command rebuilt the fixture renderer after public verification,
so the suite exercised the intended fixture rather than a stale public bundle.
Browser traces/screenshots and command logs remain transient generated
evidence; salient outcomes and reproduction inputs are captured here so this
report does not rely on their retention. No screenshots were approved or
updated. Source/fixture/manifests remained unchanged; the only intended
repository addition is this timestamped report.

## Specification acceptance checklist

- [x] Request and inferred defaults recorded.
- [x] Scope, sampling, and exclusions explicit.
- [x] Discovery order and missing context recorded.
- [x] Prior audits checked; all findings classified as new.
- [x] Canonical finding fields and normalized models used.
- [x] Observed, inferred, recommended, and unverified evidence distinguished.
- [x] Positive observations included.
- [x] Uncertainty, deferred scope, and continuation needs visible.
- [x] Complete status applies to the declared standard-depth scope; external
  and exhaustive qualifications are explicitly unverified.
- [x] Historical reports remain immutable; no historical report existed here.
- [x] No unauthorized remediation, repository mutation, or external action.

This report is an immutable snapshot. Record later remediation or new evidence
in a new timestamped audit rather than editing these findings into retrospective
success claims.


</details>

<!-- identity-audit-roadmap:20261003T162958Z:TRACKER -->

<!-- identity-roadmap-links:start -->
## Roadmap links

### Milestone 1: Authority boundaries

- [x] #71 — Enforce public/review guidance isolation in Rust projections (R01, P1)
- [x] #72 — Enforce complete source preflight for v1 CLI and library execution (R02, P1)
- [x] #73 — Constrain recovery journal mutation authority before any filesystem change (R03, P1)

### Milestone 2: Compatibility and recovery

- [ ] #74 — Specify canonical source inventory and share Rust/Python digest vectors (R04, P2)
- [ ] #75 — Bind optional design-system projections to the displayed release (R05, P2)
- [ ] #76 — Validate generic artifact paths and preserve configured download bases (R06, P2)
- [ ] #77 — Expose supported CLI inspection and recovery for interrupted consumers (R07, P2)
- [ ] #78 — Validate and confine transaction caches, staging, and backup paths (R08, P2)
- [ ] #79 — Establish exclusive writer serialization for generation and recovery (R09, P2)

### Milestone 3: Reproducible development

- [ ] #80 — Qualify a reproducible browser, font, and screenshot environment (R10, P2)
- [ ] #81 — Pin and qualify the default development Docker base identity (R11, P2)
- [ ] #82 — Exercise standalone, Make, Task, and Docker setup entry points in CI (R12, P3)

### Milestone 4: Documentation and cleanup

- [ ] #83 — Reconcile active architecture, capability, and publication documentation (R13, P2)
- [ ] #84 — Retire completed one-time guidance rewrite workflows (R14, P3)
- [ ] #85 — Extract focused validator modules behind stable offline entry points (R15, P3)
- [ ] #86 — Share Python projection boundary utilities without changing outputs (R16, P3)
- [ ] #87 — Extract focused Rust compiler, quality, and motion modules (R17, P3)
- [ ] #88 — Extract renderer components and input adapters with stable behavior (R18, P3)


<!-- identity-roadmap-links:end -->
