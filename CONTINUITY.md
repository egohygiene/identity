---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/identity
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-22T18:44:56.584461+00:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Record the task-owned isolated Docker backend and observed capability/transport repair for
    original Identity
  includes:
  - Actual overlay2 engine, measured shared tmpfs capacity, bounded helper resources and source-bound
    observations.
  - Runnable scoped procedure and specific repaired runc/network/proxy failures without credentials.
  excludes:
  - Shared-daemon configuration changes, global pruning, raw host devices, unrelated user files and private
    credentials.
  - Profile/pin/guard changes, inferred full product acceptance, hosted CI, new approval, source adoption
    or release.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - docs/decisions/ADR-0011-accessibility-and-visual-evidence.md
  - docs/work/80/ISOLATED_DOCKER_2026-11-22.md
  - docs/work/80/evidence-2026-11-22/isolated-docker-runtime.json
  - https://github.com/egohygiene/identity/issues/80
  - https://github.com/egohygiene/identity/issues/82
work:
  objective: Record the task-owned isolated Docker backend and observed capability/transport repair for
    original Identity
  success_conditions:
  - Preserve unchanged original profiles, immutable image pins and actual storage gates.
  - Establish real isolated Docker image/run/build capabilities and repair namespace-specific transport
    with TLS enabled.
  - Keep runtime probes distinct from browser/dev source-bound qualification and human or hosted acceptance.
  active_issue:
    provider: github
    id: egohygiene/identity#80
    url: https://github.com/egohygiene/identity/issues/80
  next:
    kind: action
    id: original-profile-workflow-then-dev
    description: Browser owner replays original workflow locally, then clean only owned nested images/cache
      and run full dev default/nonroot setup-twice qualification. Preserve actual receipt outcomes.
    readiness: ready
    references:
    - https://github.com/egohygiene/identity/issues/80
    - https://github.com/egohygiene/identity/issues/82
    depends_on: []
state:
  base:
    revision: edca416d58d15b06ccc05029b0803bc27e65fe18
    ref: refs/heads/codex/70-rfc3339-review-times-20261122
    verified_at: '2026-11-22T18:44:56.584461+00:00'
  candidate:
    branch: codex/80-qualified-browser-stack-20261122
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-22T18:44:56.584461+00:00'
    default_branch_revision: 75ca39f3fc7e5e9e0b5578af58c966cd2590a652
    issue_state: open
    pull_request_state: not-applicable
    notes: Main remains 75ca39f; six Identity finish issues remain open. Earlier158 through162 and Aether140
      are merged. Parent drafts 163 are open; this next child PR does not yet exist. No new sprint PR
      is merged or published.
  parallel_changes:
  - provider: github
    id: egohygiene/identity#163
    url: https://github.com/egohygiene/identity/pull/163
  - provider: github
    id: egohygiene/aether#142
    url: https://github.com/egohygiene/aether/pull/142
review:
  status: partial
  reviewed_at: '2026-11-22T18:43:27.562510+00:00'
  reviewed_by: Codex
  evidence:
  - command: Own Docker 28.4 overlay2 generated-image import/run/cgroup/BuildKit capability probes
    outcome: passed
    observed_at: '2026-11-22T18:43:27.562510+00:00'
    notes: Tiny controlled workload only; UID 1234 ownership and UID 0/1000 execution preserved. Not product-profile
      acceptance.
  - command: Namespace-correct proxy normalization then Docker exact digest manifest inspect
    outcome: passed
    observed_at: '2026-11-22T18:43:27.562510+00:00'
    notes: Pinned Playwright and Node metadata retrieved with TLS enabled. Initial actual MCR pull timeout
      and combined Node tag/digest manifest CLI failure remain recorded.
  - command: Client/daemon actual data-root measurements and scoped helper inspect
    outcome: passed
    observed_at: '2026-11-22T18:43:27.562510+00:00'
    notes: Same device/inode, shared 9.44 GB tmpfs;12 GiB helper and narrower parent cgroup budget recorded.
      Source/evidence/data are one pool.
  environment_limitations:
  - Original direct browser pass is owned by its clean 9d11d99 receipt; local workflow replay and full
    dev run are separate active work.
  - Runtime capability and metadata evidence supply no hosted/native/human acceptance or full WCAG claim.
  - Browser first, dev second; original non-VFS reserves remain unchanged and actual capacity is measured
    before each run.
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

This scoped handoff records an actual isolated Docker runtime, subordinate to user instructions, repository contracts and live trackers. It does not adopt source or approve product outputs.

## Resume protocol

Read AGENTS and the runtime note/receipt. Recheck live main/issues and coordinate the single heavy-image slot. Local origin/main is 75ca39f. Existing owner choices, tokens, rights and native-record gaps from work98 remain unchanged.

## Current objective and success conditions

Use real overlay2 capacity for original browser/dev qualification while retaining profile, image pins, storage guards, TLS and exact source binding. Keep engine probes separate from product acceptance.

## State snapshot

Stack base is `codex/70-rfc3339-review-times-20261122` at `edca416d58d15b06ccc05029b0803bc27e65fe18`. Candidate `codex/80-qualified-browser-stack-20261122` is a draft child with no containing-revision or pre-PR self-reference. Main remains `75ca39f3fc7e5e9e0b5578af58c966cd2590a652`. Domain receipts retain their exact independently represented source; stacking does not relabel earlier runs as tests of later code.

## Completed and material changes

Real import/run/build/ownership/cgroup/network probes pass. Protected runc reexec works after a byte-identical normal-file copy; own network/cgroup views are scoped writable. Namespace-correct proxy normalization fixes actual Docker metadata transport with TLS enabled. The original browser qualifier has passed on clean 9d11d99; its separate checkpoint owns acceptance.

## Validation and review evidence

The JSON receipt records engine/executable hashes, measured shared filesystem, helper constraints, capability scope and exact image metadata results. Initial capacity refusal, runc/netns failures and MCR timeout remain explicit in the procedure. Pinned Aether decision-authoring v2.1.0 was read from Git object dc8a16851f452763ef4f7fbe4bf057d4500b1921; governing ADR is 0011.

## Blockers, risks, unknowns, and deferred work

Workflow replay and complete dev default/nonroot setup-twice execution are independently owned and active. Tmpfs consumes the same finite memory budget; source/evidence/data are not separate reserves. Hosted/native/human and source/adoption/release gates remain independent. Never infer acceptance from the tiny generated image.

## Next dependency-ready work

Finish browser workflow replay, preserve small source-bound evidence durably, then remove only own nested images/cache before dev's unchanged 8 GiB non-VFS guard. Stop on genuine failures and preserve their scope. No global prune or implicit profile/pin change.

## Parallel changes and reconciliation

This checkpoint follows parent draft PRs #163. The engineering parent enforces existing approval timestamp validity and retains unknown actual-owner review times. Each browser, development-image and source-assembly record retains its own represented source and qualification limits. Review parents before children; keep source adoption and actual release/deployment separate. Aether metadata projection and installed-host verification retain their separate draft chain under Aether38.

## Privacy and redaction

Retain public source/tool hashes, bounded observed capacities and failure classes. Exclude proxy values, credentials, private certificates/keys, user paths and unrelated data. The public CA bundle was read-only; TLS remains enabled.

## Handoff update protocol

Validate docs/JSON/whitespace and pinned continuity metadata, exact twelve headings and 16384-byte/240-line budgets. Decision impact: reference accepted ADR-0011 for scoped execution/evidence; no new contract, runtime default, policy or human lifecycle is selected.

## Compaction and supersession

The runtime recipe and source-bound owners retain detailed results. Preserve prior approvals and exact issue IDs. Teardown only owned helper state after evidence is saved; shared daemon configuration/cached image remain intact, with helper lifecycle recorded through it.
