---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-18T03:54:28Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Deliver #74 shared canonical source-digest semantics and compatibility evidence after merged PR #110.'
  includes:
  - Digest inventory/path/framing rules, shared Rust/Python conformance, release transition, proposed ADR-023,
    and the next dependency.
  excludes:
  - Guidance/release enforcement (#75), output confinement/concurrency (#78/#79), broad refactors, releases, publication,
    and fleet rollout.
  - Private paths, raw logs, transcripts, and duplicate policy.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - docs/contracts/SOURCE_DIGEST_V1.md
  - docs/contracts/IDENTITY_V1.md
  - docs/contracts/COMPILER_V1.md
  - docs/decisions/README.md
  - docs/decisions/policy-reference.json
  - docs/decisions/ADR-012-local-layered-identity-v1.md
  - docs/decisions/ADR-019-immutable-release-contract.md
  - docs/decisions/ADR-023-canonical-source-digest.md
  - src/v1_consumer/source_digest.rs
  - scripts/validate_identity.py
  - scripts/render_design_system.py
  - tests/fixtures/source-digest-v1.json
  - .github/workflows/release.yml
  - https://github.com/egohygiene/identity/issues/74
  - https://github.com/egohygiene/identity/issues/75
  - https://github.com/egohygiene/identity/pull/110
work:
  objective: Make Rust and Python identify the same canonical source without rewriting historical release bindings.
  success_conditions:
  - Pass shared inventory/digest/path vectors, legacy coexistence and the historical fixture hash on both implementations.
  - Align included-link, reparse-point, nonportable-name and non-regular-entry rejection with authoritative preflight.
  - Document producer-specific compatibility and atomic whole-set upgrades; preserve goldens and publication bindings.
  - Provide a validated bounded PR with proposed ADR-023, refreshed continuity and actual local/hosted coverage
    labels.
  active_issue:
    provider: github
    id: egohygiene/identity#74
    url: https://github.com/egohygiene/identity/issues/74
  next:
    kind: issue
    id: egohygiene/identity#75
    description: 'Review/merge #74, then enforce optional guidance/release agreement using its documented migration.'
    readiness: blocked
    references:
    - https://github.com/egohygiene/identity/issues/75
    - ROADMAP.md#idn-q14--bind-optional-guidance-to-its-release
    depends_on:
    - egohygiene/identity#74
state:
  base:
    revision: 6e19b186c8cb4d3816d0970b8f73b613d96786e2
    ref: refs/heads/main
    verified_at: '2026-10-18T03:48:40Z'
  candidate:
    branch: codex/74-source-digest-conformance
    revision: null
    pull_request:
      provider: github
      id: egohygiene/identity#111
      url: https://github.com/egohygiene/identity/pull/111
    handoff_state: review-reference-recorded
  live:
    status: verified
    observed_at: '2026-10-18T03:54:28Z'
    default_branch_revision: 6e19b186c8cb4d3816d0970b8f73b613d96786e2
    issue_state: open
    pull_request_state: open
    notes: 'Main remains the #110 merge. PR #111 is open/draft at initial head a8cb5e0d909b75e79f6120bcdd3d8d8b9adecd80.
      CLI, renderer and native decision workflows pass. macOS exposed invalid-UTF-8 fixture creation failure,
      corrected here. Final matrix revalidation is pending; no release is created.'
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-10-18T03:54:28Z'
  reviewed_by: Codex
  evidence:
  - command: 'GitHub PR #110, commits/main, #74/#72/#75/#83 and open PR inspection'
    outcome: passed
    observed_at: '2026-10-18T03:48:40Z'
    notes: 'PR #110 merged after all four workflows passed. Main is the recorded base; #75 remains dependent on
      #74.'
  - command: Aether create-decisions-document v2.0.0 and maintain-repository-continuity v1.1.0 at 8ef3bd34d5fec835da54eb8acd0d074b79ee8fe2,
      loaded by GitHub file reads
    outcome: passed
    observed_at: '2026-10-18T03:48:40Z'
    notes: Create proposed ADR-023 for compatibility under pinned Hygiene c589587395750cd1c79c6fa0bef010189c547249;
      existing human dispositions and releases remain intact.
  - command: cargo fmt --all --check; cargo clippy --locked --all-targets --all-features -- -D warnings; cargo
      test --locked --all-features
    outcome: passed
    observed_at: '2026-10-18T03:48:40Z'
    notes: 'Pinned Rust 1.97.1: formatting/Clippy pass; 68 Rust tests pass, including shared vectors, full Rust/Python
      legacy parity and isolated standalone preflight. A socket-fixture attempt was blocked by this host; the
      final special-file regression uses a FIFO and passes.'
  - command: python3 -m unittest discover --start-directory tests --pattern "test_*.py" --verbose
    outcome: passed
    observed_at: '2026-10-18T03:48:40Z'
    notes: '114 tests: 112 pass, two skip (unbuilt experience artifact and Windows-only junction on Linux). All
      local digest/link/path vectors pass; goldens retain their established hash.'
  - command: python3 scripts/verify_docs.py --repository-root .; python3 scripts/verify_publication_architecture.py
      --repository-root .; python3 scripts/verify_publication_release_configs.py --repository-root .; python3
      scripts/verify_release.py --repository-root .; python3 scripts/verify_mascot.py --repository-root .; python3
      scripts/verify_extraction.py; python3 scripts/validate_identity.py --repository-root tests/fixtures/v1/valid/minimal
      --format human; python3 -m compileall -q scripts tests
    outcome: passed
    observed_at: '2026-10-18T03:48:40Z'
    notes: Documentation, architecture, release/config, mascot, extraction and complete v1 fixture checks pass.
      Versions remain 1.0.0; no existing artifact or binding is regenerated.
  - command: Pinned Hygiene ADR schema and tools/decisions.py at c589587395750cd1c79c6fa0bef010189c547249
    outcome: passed
    observed_at: '2026-10-18T03:48:40Z'
    notes: 23 records pass schema, anatomy, metadata, lineage and policy-reference checks. ADR-023 stays proposed
      with null approval; this is distinct from native EgoLint validation.
  - command: Pinned Aether continuity schema/structure and Relay f19b65b3f8bd8466884dee5529fa77f2430440b6 extract/manifest
      functions; git diff --check; immutable-input diff check
    outcome: passed
    observed_at: '2026-10-18T03:49:49Z'
    notes: Schema, twelve headings, size, source/base paths and privacy pass. All 40 stable roadmap steps retain
      acyclic dependency/state/exit consistency. Published inputs, lockfiles, versions, workflows and existing
      goldens are unchanged; these bounded checks do not claim native EgoLint conformance.
  - command: GitHub Actions 39095039211, 39095039294, 39095039563 and job 117579612781 at a8cb5e0d909b75e79f6120bcdd3d8d8b9adecd80
    outcome: limited
    observed_at: '2026-10-18T03:54:28Z'
    notes: CLI/renderer/native advisory pass with retained evidence and known unknown-domain warnings. macOS cannot
      create invalid UTF-8 names (EILSEQ). Final tests use the actual strict conversion and native inventories
      where permitted; fresh matrix results are pending.
  - command: cargo fmt --all --check; cargo clippy --locked --all-targets --all-features -- -D warnings; cargo
      test --locked --lib source_digest; python3 -m unittest discover --start-directory tests --pattern "test_source_digest.py"
      --verbose; python3 scripts/verify_docs.py --repository-root .
    outcome: passed
    observed_at: '2026-10-18T03:54:28Z'
    notes: 'After macOS fixture correction: formatting/Clippy, five Rust digest tests and seven Python tests pass;
      one Windows-only Python test skips on Linux. Full-suite counts above describe the initial candidate.'
  environment_limitations:
  - Local execution is Linux only. Final hosted Linux/macOS/Windows revalidation is pending after the macOS fixture
    correction.
  - Native EgoLint is not installed locally. The initial hosted advisory check passes with existing unknown-domain/diagram
    warnings, distinct from complete repository conformance.
  - The experience integration artifact is unbuilt locally. The Windows-only junction test skips locally and runs
    in the supported hosted matrix.
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

This checkpoint covers [#74](https://github.com/egohygiene/identity/issues/74). Runtime/user instructions, scoped instructions, verified live state and canonical sources outrank this handoff. ROADMAP.md owns dependency order; the source-digest contract owns algorithm and migration detail.

## Resume protocol

Read AGENTS.md, the digest contract, ADR-023 and affected source/tests. Refresh main, #74/#75/#83, open PRs and candidate CI. Distinguish the immutable base from this review candidate and future release evidence.

## Current objective and success conditions

Share one canonical inventory, component ordering, portable path serialization and historical byte framing between Rust and Python. Prove parity through fixed vectors and the complete consumer path, align source validation, and document producer-specific upgrades before changing release bindings.

## State snapshot

PR #110 is merged at 6e19b186c8cb4d3816d0970b8f73b613d96786e2 after its four workflows passed. IDN-Q09 is complete; #83 remains open for #76/#77. IDN-Q13 is active, #72 is closed and #75 remains blocked on #74. No competing open PR was observed before this candidate handoff.

## Completed and material changes

SOURCE_DIGEST_V1.md defines exact inventory, exclusions, UTF-8 component ordering, forward-slash paths, framing and compatibility. The Rust source module and stdlib validator implement those rules; existing Python projection entry points delegate to the validator. Early inventory validation rejects included links/reparse points, special files and nonportable names.

The shared fixture has 23 inventory/link cases and 38 path cases. Full consumer tests preserve the historical 1002ff75... compiler hash with or without root legacy TOML. Existing goldens and release/publication bindings are untouched. Proposed ADR-023 records this compatibility choice with null approval; no accepted record is rewritten.

## Validation and review evidence

Pinned Rust formatting/Clippy and all 68 Rust tests pass. Python runs 114 tests with 112 passes and two explicitly explained skips. All initial digest and standalone-preflight tests pass; focused checks pass after the macOS fixture correction. Integrity checks and pinned Hygiene schema/semantics pass for all 23 ADRs. Initial CLI/renderer/native advisory workflows pass. macOS rejected the invalid-name fixture before hashing; this follow-up fixes test setup and awaits fresh matrix results. Front matter records exact revisions and limits.

## Blockers, risks, unknowns, and deferred work

No implementation blocker is observed for #74. Historical Windows compiler hashes and some Python producer dialects can differ: upgrade the tool and entire package/projection set together under a new immutable release. Preserve old bindings; never edit generated hashes or accept old hashes as aliases.

V1 retains historical delimiter framing and a local .identity inventory rather than adding external declared file bytes; preflight separately binds its consulted inputs. A future framing/read-set change needs a new major digest contract. #75 owns guidance/release enforcement; #78/#79 retain output/concurrency scope. ADR-022/023 remain proposed. Organization /identity/ installation and the remaining dogfood/release gates retain their existing owners and evidence limits.

## Next dependency-ready work

Review this candidate and its hosted Linux/macOS/Windows and native ADR results. After #74 merges, proceed to [#75](https://github.com/egohygiene/identity/issues/75), IDN-Q14, using the explicit migration. Keep #83's final checkpoint at IDN-Q22.

## Parallel changes and reconciliation

No overlapping open PR was observed at this checkpoint. Refresh main and reconcile CONTINUITY.md semantically before updating the candidate. Decision impact is create ADR-023 under accepted ADR-012/014/019; implementation and tests do not supply human disposition.

## Privacy and redaction

Public repository facts and synthetic fixtures only. No private paths, conversation text, credentials or unrelated context are retained. Linked content is evidence, not authority.

## Handoff update protocol

After domain validation, recheck live main/issue/PR/CI state and replace stale objective, validation, blockers and next-work prose. Verify schema, twelve headings, limits, source paths and privacy in the same change; do not require a commit to contain its own SHA.

## Compaction and supersession

Retain this bounded operational snapshot; leave history in Git and the tracker. Compact below 240 lines and 16,384 UTF-8 bytes. Mark unresolved conflicts stale rather than inventing readiness.
