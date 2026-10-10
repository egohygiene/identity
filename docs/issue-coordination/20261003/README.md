# Identity / Repository Intelligence coordination edits

Prepared 2026-10-03 from public issue bodies and Identity main at 8aae2c6.
These are proposed edits to five existing issues. GitHub updates have not been applied.

- **Identity #83:** Reconcile canonical ROADMAP.md with #70–#88; reconcile IDN-Q05 using #17/#18's completed exit evidence; preserve stable IDs/history and truthful review timestamps. Ship the bounded roadmap reconciliation early. Final audience/download/recovery documentation explicitly depends on #71, #76, and #77. Keep merged, released, deployed, and decision-accepted states separate.
- **Identity #88:** Explicit dependencies become #71, #75, #76, #80; preserve the public/review fixtures added in PR #89.
- **Identity #70:** Link #69 and Pace #5 as scoped pilot coordination, not an all-18-issues blocking dependency. Mark #71–#73 completed with PR #89 / 8aae2c6 evidence; retain the audit snapshot unchanged.
- **Identity #69 and Pace #5:** Add reciprocal links to #70/#83. Read-only Observatory/ADR collection may proceed in parallel with truthful visibility, freshness, and coverage reporting. Preserve existing shared-system and human-authority gates for backfill, migration, continuous capture, and publication. Require an Identity repair only when the exercised operation actually depends on it.
- **Publication ownership in #83 and pilot cross-links:** Keep the immutable Brand Kit at identity.egohygiene.io, the organization /identity/ experience, and proposed Repository Intelligence views distinct. Record approved publisher, host/routes, privacy, validation, and rollback authority; unknown Intelligence deployment choices remain proposed. Do not replace Brand Kit Pages/CNAME ownership as a side effect of adoption.

Full proposed bodies are `<repository>-<issue>.md`; original bodies are `.before.md`.
Review [coordination.patch](coordination.patch) for exact changes. Historical audit evidence is unchanged.

`python3 apply.py` previews targets. `python3 apply.py --publish` requires authenticated
GitHub CLI access and checks every live issue body before sending any edits. It stops
if another chat changed a body. Updates to multiple issues are not atomic; the script
also rechecks each issue immediately before editing and reports each completed update.

Run from the repository root:

```bash
python3 docs/issue-coordination/20261003/apply.py
python3 docs/issue-coordination/20261003/apply.py --publish
```

Opening or merging this PR does not apply the GitHub issue edits. Publication is
an explicit operation against the five issues in [updates.json](updates.json).
The original bodies are retained for stale-edit checks and historical evidence;
the proposed bodies are review artifacts, not another canonical roadmap. The
actual ROADMAP.md reconciliation remains implementation work owned by #83.

The updater does not change titles, labels, assignees, milestones, or issue state.
It does not close the pilot or shared-system gates. If any concurrent edit is
observed, reconcile the proposal against the latest issue body and review it
again before publishing. GitHub issue edits are not an atomic multi-issue
transaction; another editor can still change an issue after the last check.
