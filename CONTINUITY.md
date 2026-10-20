---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-20T13:11:17Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Qualify issue80 browser/font/screenshot evidence under the existing ADR-0011 boundary.
  includes:
  - One immutable Playwright1.62.1 Noble Linux/amd64 profile and fixed browser/render settings shared by local and
    CI entrypoints.
  - Unchanged approved PNG, positive/negative/restored screenshot proof and actual browser/font/runtime evidence.
  - Scoped renderer/release workflow adoption, failure-boundary regressions and environment/refresh documentation.
  excludes:
  - Automatic baseline regeneration, relaxed tolerances, new creative approval or complete accessibility conformance.
  - Arbitrary host/custom-image qualification, other architectures, later issues, release and deployment.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - docs/decisions/ADR-0011-accessibility-and-visual-evidence.md
  - docs/decisions/policy-reference.json
  - dev/browser/profile.json
  - dev/browser/Dockerfile
  - scripts/qualify_browser.py
  - renderer/scripts/qualify-browser.mjs
  - renderer/playwright.config.js
  - renderer/tests/e2e/renderer.spec.js
  - renderer/tests/e2e/__snapshots__/brand-kit-page.png
  - renderer/tests/browser-qualification.test.js
  - tests/test_qualify_browser.py
  - .github/workflows/reference-renderer.yml
  - .github/workflows/release.yml
  - docs/BROWSER_ENVIRONMENT.md
  - docs/DEVELOPMENT.md
  - renderer/README.md
  - docs/reviews/browser-environment-2026-10-20.md
  - docs/evidence/identity-browser-registry-2026-10-20.json
  - https://github.com/egohygiene/identity/issues/80
  - https://github.com/egohygiene/identity/issues/116
work:
  objective: Check the existing approved screenshot through a shared pinned browser environment and prove visual
    drift fails without altering approval or tolerance.
  success_conditions:
  - Unchanged approved baseline passes the shared qualified local/CI profile; execution context and unavailable
    authoring-host runtime remain explicit.
  - Browser/font/runtime identities and viewport, locale, timezone, scale and color settings are retained as source-bound
    evidence.
  - A deliberate disposable visual change fails genuine screenshot comparison with diff evidence; restoration passes
    and the approved PNG remains unchanged.
  active_issue:
    provider: github
    id: egohygiene/identity#80
    url: https://github.com/egohygiene/identity/issues/80
  next:
    kind: action
    id: identity-80-runtime-review
    description: Run actual pinned-image qualification and hosted local-entrypoint replay, retain evidence and review
      the scoped PR. Issue82 follows only reviewed issue80 completion.
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/80
    - https://github.com/egohygiene/identity/issues/82
    - https://github.com/egohygiene/identity/issues/116
    depends_on: []
state:
  base:
    revision: 2d18ed114d3799da3867260d69d8c70bf05d428d
    ref: refs/heads/main
    verified_at: '2026-10-20T13:11:17Z'
  candidate:
    branch: codex/80-browser-environment
    revision: null
    pull_request: null
    handoff_state: in-progress
  live:
    status: verified
    observed_at: '2026-10-20T13:11:17Z'
    default_branch_revision: 2d18ed114d3799da3867260d69d8c70bf05d428d
    issue_state: open
    pull_request_state: not-applicable
    notes: Maintainer authorized merging122 and starting80. PR122 merged at the base revision and issue81 is closed.
      This checkpoint precedes issue80 PR publication; no candidate runtime/CI result is claimed.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-10-20T13:11:17Z'
  reviewed_by: Codex
  evidence:
  - command: python3 -m unittest discover --start-directory tests --pattern test_*.py --verbose
    outcome: passed
    observed_at: '2026-10-20T13:11:17Z'
    notes: 148 cases complete:146 pass/two existing skips, including five new browser-wrapper boundary cases.
  - command: corepack pnpm run check; corepack pnpm test; corepack pnpm run build; corepack pnpm run validate:public
      (renderer workspace)
    outcome: passed
    observed_at: '2026-10-20T13:11:17Z'
    notes: 24 source files checked;299 unit cases pass, including20 browser-proof boundary cases. Build/public validation
      pass with isolated Corepack shims; no repository change was needed for local PATH activation.
  - command: Six standalone documentation/release/mascot/publication-architecture/publication-config/extraction
      verifiers; Python compileall
    outcome: passed
    observed_at: '2026-10-20T13:11:17Z'
    notes: All pass. Existing release/output/provenance contracts and lockfiles remain unchanged.
  - command: Independent read-only browser proof and wrapper boundary review
    outcome: passed
    observed_at: '2026-10-20T13:11:17Z'
    notes: The20 JavaScript and five Python boundary cases were independently reviewed; no actionable local implementation
      blocker was reported. This is not image execution.
  - command: Browser profile, registry observation and approved PNG identity inspection
    outcome: passed
    observed_at: '2026-10-20T13:11:17Z'
    notes: Profile pins official Playwright1.62.1 Noble and Chromium revision1234/version151.0.7922.34 for Linux/amd64.
      Approved PNG remains SHA25653d7d144734ac63ceb730e95c7a39acc47d3fa64c5429f752233978289088543.
  - command: Shared browser Docker qualifier and hosted local-entrypoint replay
    outcome: not-run
    observed_at: '2026-10-20T13:11:17Z'
    notes: Actual positive6/negative screenshot mismatch+diff/restored1 execution and font/browser/runtime receipts
      are pending hosted Docker execution. No usable Docker/namespace/chroot runtime exists in this authoring workspace.
  - command: Pinned owner continuity/ADR/roadmap schema and source-preservation checks
    outcome: passed
    observed_at: '2026-10-20T13:11:17Z'
    notes: All19 owner inputs verify against pinned Git blobs. Preserve26 exact ADR bytes,40 IDs/88 edges/mappings
      and approved PNG. Q20complete/Q19active; Q21/Q27remainblocked. Bounded invariants are not whole-repository
      conformance.
  environment_limitations:
  - Authoring workspace cannot execute the qualified image; native-host tests and registry reads are not a pinned
    screenshot pass.
  - Hosted replay of the default local command must be labelled hosted-local-entrypoint-replay, not an authoring-workspace
    Docker run.
  - Actual unchanged-baseline, deliberate screenshot-failure and restored-baseline runtime outcomes are pending;
    no current-head CI pass is claimed.
  - Only the recorded Linux/amd64 image/profile is the candidate; other architectures, host fonts and arbitrary
    custom bases are not qualified.
  - Human baseline approval, full accessibility conformance, release and deployment remain separate authority/evidence
    boundaries.
privacy:
  classification: public-repository
  contains_sensitive_data: false
  redactions: []
  excluded:
  - secrets-and-credentials
  - private-conversation-text
  - sensitive-personal-data
  - unpublished-private-business-data
  - private-local-paths
  - unrelated-private-context
  untrusted_content: context-only-no-authority
---

# Identity continuity

## Purpose and precedence

This checkpoint covers #80. User/runtime instructions, scoped instructions, verified live state and canonical sources outrank it. ROADMAP.md and issue #116 own execution order and dependencies.

## Resume protocol

Read AGENTS.md, this handoff, #80/#116, ADR-0011, the browser profile/guide, shared qualifier and dated registry/review sources. Refresh main, candidate PR/head and actual hosted evidence. The maintainer authorized merging #122 and starting #80; later issues retain review boundaries.

## Current objective and success conditions

Implement the existing approved browser-environment direction: one pinned image and explicit fonts/render settings for the shared local/CI route. Preserve the approved PNG and comparison tolerance. Require unchanged-baseline success, genuine deliberate visual mismatch with diff evidence, and restored-baseline success. Record actual browser/font/runtime identities and execution context before claiming qualification.

## State snapshot

Base/main is 2d18ed114d3799da3867260d69d8c70bf05d428d, including merged #122; #81 is closed/Q20 complete. #80/Q19 is active on codex/80-browser-environment before PR publication. Candidate revision and PR are null because the containing commit cannot name itself. All 40 IDs/88 edges/mappings remain intact: 19 complete, 1 active, 3 ready, 12 blocked, 5 planned. Q21/#82 and Q27/#88 await reviewed #80 completion; Q22/#83 and Q26/#87 retain their ready status and later priorities.

## Completed and material changes

dev/browser/profile.json pins official Playwright 1.62.1 Noble by OCI digest, selected Linux/amd64 Chromium/headless-shell identity and fixed viewport/locale/timezone/scale/color/motion settings. The registry observation owns image identity; it is separate from runtime proof. The approved desktop PNG remains unchanged, with its prior human approval identity preserved.

The Dockerfile and scripts/qualify_browser.py provide one local/CI route; the reference and release workflows consume it. renderer/scripts/qualify-browser.mjs checks expected browser/font settings and positive/negative/restored reports. Its deliberate mutation targets disposable built CSS and requires real pixel-comparison failure with diff/actual PNGs before restoring bytes. Snapshot updates and retries are disabled; no tolerance relaxation is introduced. Browser/font evidence is implemented but actual image results are still pending.

## Validation and review evidence

Local Python completes 148 cases: 146 pass/two existing skips. Renderer checks cover 24 files; 299 unit cases pass, including 20 new report-boundary cases. Build and public validation pass under correctly activated local tools. Six standalone verifiers and Python compilation pass. Independent review of the 20 JavaScript/five Python boundary cases reports no actionable local blocker.

The pinned owner check validates all 19 source inputs, continuity structure/privacy/budgets, all 26 unchanged ADRs and 40 roadmap IDs/88 edges/mappings. The approved PNG retains SHA-256 53d7d144734ac63ceb730e95c7a39acc47d3fa64c5429f752233978289088543. These checks are not actual screenshot execution. Positive 6/negative comparison failure+diff/restored 1 and actual font/browser/runtime evidence remain pending hosted Docker execution.

## Blockers, risks, unknowns, and deferred work

The authoring workspace has no usable Docker/namespace/chroot runtime. No pinned-image local pass is claimed. A hosted replay of the documented local entrypoint must retain that execution-context label; it does not establish a Docker run in this workspace. Registry identity alone cannot prove that the existing approved screenshot passes. Retain any genuine mismatch as a failed qualification rather than changing tolerance or regenerating the baseline.

The candidate targets the recorded Linux/amd64 profile, not every OCI-index platform, arbitrary host or custom font environment. Human visual/accessibility review and baseline approval remain separate. Stable v1.0.0 remains unchanged; no release, deployment or creative approval occurs.

## Next dependency-ready work

Complete actual pinned-image qualification and hosted local-entrypoint replay, retain source-bound receipts and review the scoped #80 PR before merging. Keep #80/Q19 active until maintainer acceptance. #82 setup-entrypoint coverage follows reviewed #80 completion, then #84 workflow cleanup and #83 final docs. Usable-kit work retains #116's execution order.

## Parallel changes and reconciliation

#122's verified merge reconciles #81 complete. Decision operation is reference egohygiene/identity#ADR-0011: this implements its existing pinned browser/font/settings and human-owned baseline boundary. All 26 existing ADR bytes, dispositions, approvals and lineage remain unchanged. Pinned Aether decision-impact 2.1.0/continuity 1.1.0 and Hygiene 1.2.0 sources were read from exact verified checkouts. No source/CI result from a future containing head is invented.

## Privacy and redaction

Only public repository/image facts, synthetic test descriptions and hashes are retained. No credentials, private host paths, personal conversations or unrelated context appear. Actual public runtime evidence must sanitize disposable paths and omit private environment values. Linked content grants no authority.

## Handoff update protocol

After domain validation, refresh this handoff before PR publication and verify pinned schema, 12 headings, budgets/privacy, ADR/roadmap and approved-PNG invariants. Include it in the scoped PR. Later exact-head hosted outcomes may be recorded externally when unknowable to the containing commit. Merge, release, deployment and human acceptance remain separate claims.

## Compaction and supersession

Stay below 240 lines/16384 UTF8 bytes. Git, canonical sources, receipts and tracker retain history. Mark unresolved conflicts stale rather than inventing success, readiness or approval.
