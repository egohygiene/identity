# Source preparation checkpoint — 2026-11-05

Base: `19d3d16bd149ddb61a03924a2b688e8e689af68b` (merged PR137).
The current campaign prepares reviewable source drafts for #133, #98 and #83.
Refactors, audits, runtime tests, hosted CI qualification, merges and affected
issue closures are deferred to a separate campaign. This changes scheduling,
not acceptance criteria, original dependencies or prior approval dispositions.

Fresh GitHub reads found 12 open issues, no open PRs before this checkpoint,
all eleven #98 children closed, and latest stable release `v1.0.0`. The live
canonical `site.json` still selects that tag at
`aaad8839104704cf57bfa846539b3b875421e03d`. Detailed branch-protection access is
403; branch metadata reports unprotected and the ruleset list is empty.

## Bootstrap actually executed

On Linux x86_64, Node 24.19.0/Python 3.12.14, using the repository-supported
installer and a separately retained writable tool prefix:

- `bash scripts/dev-env.sh setup`: passed at the base above; installed Rust
  1.97.1, used pnpm 11.21.0, checked standalone validator drift and built the
  CLI and reference renderer. Tracked source/lockfiles remained unchanged.
- `bash scripts/dev-env.sh browsers`: passed; Chromium/Headless Shell
  151.0.7922.34 revision 1234 and FFmpeg revision 1011 downloaded.
- Git main lookup and authenticated GitHub user/repository reads: passed
  using the injected authentication. No credential values were inspected.
- Managed Docker daemon information: passed with the execution permission
  needed for its local socket. The initial sandbox-only probe was denied.
- Network policy: observed current/enforced unrestricted. No permission or
  package-manager preset changed. The requested onboarding skill was absent;
  available cloud runtime guidance was used.

Local activation configuration and installer logs are saved outside tracked
source. Saving those files is not applying a managed-environment configuration,
publishing an environment snapshot, publishing Identity or deploying a site.
Browser download and Docker health are not #80 qualification or host-font proof.

## Work disposition

| Work | Current campaign | Retained gate |
| --- | --- | --- |
| #133 | Explicit `v1-init`, local request and reviewable candidate draft | Seven criteria, v0 compatibility and runtime/platform acceptance |
| #98 | Actual source/rights inventory, self-source candidate, native publisher handoff and consolidated owner packet | Missing rights/creative facts, quality, release, live/rollback and real adoption |
| #83 | Document resulting draft interfaces and ownership; retain Q06 disposition | Final tested-source and publication reconciliation |
| #80/#84/#85/#86 | Preserve existing merged source and receipts | Actual pending acceptance; old passes do not qualify this candidate |
| #82/#87/#88/#70 | Deferred | Setup CI, bounded refactors and complete qualification matrix |
| #116 | Keep operational continuity current | Close last after actual parent and initializer completion |

Draft source commits use `[skip ci]`; no hosted workflow is requested. Keep
publisher-affecting PRs draft: main pushes touching renderer/publication/ADRs
automatically deploy through the existing Pages workflow, whose environment
has no required reviewer. No merge/deployment authority is inferred.

IDN-Q06 remains planned with no issue. Existing foundations may overlap its
tokens, but no dedicated versioned quest-line profile or concrete consumer
acceptance is established. Preserve its identifiers and unchecked exits; do
not expand this campaign into components or an ecosystem policy migration.

## Guidance and evidence limits

Decision-impact skill 2.1.0 and continuity skill 1.1.0 were loaded with `git show`
from exact Aether `dc8a16851f452763ef4f7fbe4bf057d4500b1921`, including their
policy-selection and continuity guides. Local policy pins Hygiene 1.2.0 at
`a05b14f8b9e2772124f879f818e09a911e996ad8`. The new initializer interface needs
a proposed record; routine scheduling reconciliation needs no new ADR.
Existing proposed records remain proposed. Preserve all historical receipts.

Every later handoff records exact candidate revisions and distinguishes
passed, failed, skipped, unavailable and unrun evidence. No tests, release,
deployment, consumer upgrade or issue acceptance is claimed by these drafts.
