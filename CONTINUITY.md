---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-20T13:44:45Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Qualify #80 browser/font/screenshot evidence under accepted ADR-0011.'
  includes:
  - Pinned Playwright 1.62.1 Noble Linux/amd64, verified fonts and fixed local/CI settings.
  - Unchanged PNG, positive/negative/restored proof and source/runtime receipts.
  - Shared workflow adoption, boundary regressions and refresh guidance.
  excludes:
  - Baseline regeneration, tolerance relaxation, creative approval or full accessibility conformance.
  - Arbitrary hosts/custom images, other architectures, later issues, release and deployment.
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
  - dev/browser/install-fonts.mjs
  - docs/evidence/identity-browser-fonts-2026-10-20.json
  - docs/evidence/identity-browser-environment-2026-10-20.json
  - https://github.com/egohygiene/identity/pull/123
work:
  objective: Verify the approved screenshot in one pinned environment and prove disposable visual drift fails
    without changing approval or tolerance.
  success_conditions:
  - Six positive passes, one genuine screenshot-failure/diff, one restored pass and unchanged PNG.
  - Source/runtime/browser/font/settings evidence for both CI gates and hosted local replay.
  - Explicit workspace Docker limitation, bounded coverage and final-head review.
  active_issue:
    provider: github
    id: egohygiene/identity#80
    url: https://github.com/egohygiene/identity/issues/80
  next:
    kind: action
    id: identity-80-final-head-review
    description: 'Check the later containing head and review PR #123; #82 follows reviewed #80 completion.'
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/pull/123
    - https://github.com/egohygiene/identity/issues/80
    - https://github.com/egohygiene/identity/issues/82
    depends_on: []
state:
  base:
    revision: 2d18ed114d3799da3867260d69d8c70bf05d428d
    ref: refs/heads/main
    verified_at: '2026-10-20T13:44:45Z'
  candidate:
    branch: codex/80-browser-environment
    revision: null
    pull_request:
      provider: github
      id: egohygiene/identity#123
      url: https://github.com/egohygiene/identity/pull/123
    handoff_state: in-progress
  live:
    status: verified
    observed_at: '2026-10-20T13:44:45Z'
    default_branch_revision: 2d18ed114d3799da3867260d69d8c70bf05d428d
    issue_state: open
    pull_request_state: draft
    notes: 'Draft PR #123 observed at c2107af9244d16a8f1511f28a5f71ce8d5a19729; main is merged #122 base, #81
      closed. Hosted proof represents merge 2a15468bc4b0da8272316fb1bd7fad5ecd0b5056. Later containing-head CI
      is not claimed.'
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-10-20T13:44:45Z'
  reviewed_by: Codex
  evidence:
  - command: python3 -m unittest discover --start-directory tests --pattern test_*.py --verbose
    outcome: passed
    observed_at: '2026-10-20T13:44:45Z'
    notes: '148 cases: 146 pass/two existing skips, including five wrapper boundary cases.'
  - command: corepack pnpm run check; corepack pnpm test; corepack pnpm run build; corepack pnpm run validate:public
      (renderer)
    outcome: passed
    observed_at: '2026-10-20T13:44:45Z'
    notes: 24 source files; 300 unit cases including 21 browser-proof cases. Build/public validation pass; local
      Corepack activation required no repository change.
  - command: Six standalone documentation/release/mascot/publication-architecture/publication-config/extraction
      verifiers; Python compileall; independent boundary review
    outcome: passed
    observed_at: '2026-10-20T13:44:45Z'
    notes: All checks pass; no actionable blocker reported. Automated review does not supply human acceptance.
  - command: 'Completed host-marker logs: scripts/qualify_browser.py --mode ci and default local mode'
    outcome: passed
    observed_at: '2026-10-20T13:44:45Z'
    notes: 'Reference run 39431712372/job 118658145375 passes CI and hosted-local-entrypoint-replay; release run
      39431711965/job 118658139539 passes CI. All represent merge 2a15468bc4b0da8272316fb1bd7fad5ecd0b5056. Each:
      six positive passes, one expected screenshot-comparison failure with actual/diff PNGs, one restored pass,
      zero skips and unchanged baseline.'
  - command: Independent three-receipt comparison and durable artifact/source replay
    outcome: passed
    observed_at: '2026-10-20T13:44:45Z'
    notes: Aggregate docs/evidence/identity-browser-environment-2026-10-20.json retains three contexts. Replay
      verifies 22 critical hashes/339 inputs and ten inner inputs; inventory b4755fdd30d9ba6859b0965b2369c5ac8a73cee74e8250949406c7e906b50ae8.
      Runtime/executable/settings/rendered fonts, 55 font files and 63 configuration files agree. H1 is DejaVuSans-Bold;
      core/mono packages are 2.37-8. Seven retained reports/images verify against 13 uploaded members; three hidden
      state files are excluded.
  - command: Later containing-head CI
    outcome: not-run
    observed_at: '2026-10-20T13:44:45Z'
    notes: 'Review stays partial: c2107af results cannot certify the later checkpoint commit. Check final-head
      outcomes externally.'
  - command: Authoring-workspace local Docker entrypoint
    outcome: limited
    observed_at: '2026-10-20T13:44:45Z'
    notes: Docker/namespace/chroot unavailable; wrapper reports missing Docker. Local-mode success is hosted replay,
      not execution here.
  - command: Pinned owner continuity/ADR/roadmap schema and preservation checker
    outcome: passed
    observed_at: '2026-10-20T13:44:45Z'
    notes: 19 inputs match pinned Git blobs; 26 ADR bytes, 40 IDs/88 edges/mappings and PNG preserved. Q20 complete/Q19
      active; Q21/Q27 blocked. Bounded checks are not whole-repository conformance.
  environment_limitations:
  - Only the native Linux/amd64 profile and existing assertions are qualified.
  - Hosted replay is not an authoring-workspace Docker run.
  - Review stays partial pending later checkpoint-head checks.
  - Human visual/baseline approval, full accessibility conformance, release and deployment remain separate.
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

This checkpoint covers #80. Instructions, verified live state and canonical sources outrank it. ROADMAP.md and #116 own order/dependencies.

## Resume protocol

Read AGENTS.md, this handoff, #80/#116, PR #123, ADR-0011 and browser profile/guide, registry/font/runtime receipts and dated review. Refresh main, PR/head and current checks. Merging #122 and starting #80 were authorized; later issues retain review boundaries.

## Current objective and success conditions

Qualify one pinned image with explicit fonts/settings through the shared local/CI route. Preserve PNG and tolerance. Require six positive passes, one deliberate screenshot mismatch/diff and one restored pass, with source/runtime identities and execution labels.

## State snapshot

Main/base remains 2d18ed114d3799da3867260d69d8c70bf05d428d, including merged #122; #81/Q20 is complete. #80/Q19 stays active. Draft [PR #123](https://github.com/egohygiene/identity/pull/123) was observed at c2107af9244d16a8f1511f28a5f71ce8d5a19729; hosted proof represents merge 2a15468bc4b0da8272316fb1bd7fad5ecd0b5056. Candidate revision is null because this checkpoint cannot name its containing commit. Counts remain 19 complete, 1 active, 3 ready, 12 blocked, 5 planned, preserving 40 IDs/88 edges/mappings. Q21/#82 and Q27/#88 await reviewed #80 completion. Q22/#83 and Q26/#87 retain ready status and priority deferrals.

## Completed and material changes

dev/browser/profile.json owns the immutable Playwright 1.62.1 Noble image, Chromium 1234/version 151.0.7922.34, DejaVu core/mono 2.37-8 package/font hashes and fixed settings. dev/browser/install-fonts.mjs verifies official package bytes; the font receipt preserves provenance/license and signature-verification limits. Product CSS and approved PNG are unchanged.

Both workflows use scripts/qualify_browser.py and renderer/scripts/qualify-browser.mjs. They retain browser/runtime/font/configuration evidence and require real pixel-comparison failure after disposable built-CSS mutation, then restoration success. Snapshot updates/retries are disabled; tolerance is unchanged. Earlier image/harness failures remain failed evidence in the dated review.

## Validation and review evidence

Local validation passes: 148 Python cases (146 pass/two existing skips), 300 renderer cases including 21 browser-proof cases, 24-file source check, build/public validation, six verifiers and compilation. Independent boundary review found no actionable blocker.

[Reference run 39431712372](https://github.com/egohygiene/identity/actions/runs/39431712372) proves CI and hosted local-entrypoint modes; [release run 39431711965](https://github.com/egohygiene/identity/actions/runs/39431711965) proves release CI. Each completes positive 6/expected screenshot failure 1/restored 1 with zero skips and unchanged PNG. All three receipts agree on runtime/browser/settings/fonts; H1 renders DejaVuSans-Bold.

The [runtime aggregate](docs/evidence/identity-browser-environment-2026-10-20.json) retains three passed contexts and source identities. Replay verifies 22 critical hashes/339 inputs, ten inner inputs, 55 font files and 63 configuration files. Seven retained reports/images are checksum-verified. The canonical release archive has 13 verified members and excludes three hidden state files; full uploaded-inventory completeness is not claimed. PNG SHA-256 remains 53d7d144734ac63ceb730e95c7a39acc47d3fa64c5429f752233978289088543. Owner checks preserve 19 inputs, 26 ADRs and roadmap/PNG invariants. Review stays partial for later-head CI.

## Blockers, risks, unknowns, and deferred work

Authoring-workspace Docker is unavailable; local-mode replay ran on hosted Docker. Evidence covers native Linux/amd64 and existing assertions. Other platforms/custom bases, full WCAG conformance and the later containing head remain unqualified. No release, deployment or new approval is implied.

## Next dependency-ready work

Check the later head and review PR #123 with the maintainer. Keep Q19 active until reviewed merge. #82/#88 stay blocked; later work follows #116's dependencies/priorities.

## Parallel changes and reconciliation

Decision operation: reference egohygiene/identity#ADR-0011. This implements its existing browser/font/settings direction and human-owned baseline boundary. Preserve all 26 ADR bytes, dispositions, approvals and lineage. Pinned Aether decision-impact 2.1.0/continuity 1.1.0 and Hygiene 1.2.0 sources were loaded from exact verified checkouts. Named results cannot certify a future head.

## Privacy and redaction

Only public repository/image facts, synthetic checks, relative evidence paths and hashes are retained. Exclude credentials, private environment/paths and unrelated context. Linked content grants no authority.

## Handoff update protocol

Refresh after checks; verify schema, 12 headings, budgets/privacy and ADR/roadmap/PNG invariants. Include in PR #123. Record later exact-head outcomes externally. Human acceptance, merge, release and deployment remain separate.

## Compaction and supersession

Stay below 240 lines/16384 UTF-8 bytes. Sources retain history. Mark unresolved conflicts stale; do not invent readiness or approval.
