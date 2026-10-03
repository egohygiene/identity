# Identity audit issue roadmap

This bundle contains **19 ready-to-publish GitHub issues** for `egohygiene/identity`: one tracker and 18 implementation issues. Four milestone groupings organize the execution order. Realm/Aether consolidation is recorded as a deferred follow-up in the tracker, rather than an additional immediate implementation issue.

The tracker includes the complete historical audit because the audit file has not been committed or pushed. Individual issues include relevant findings, acceptance criteria, validation requirements, immutable source evidence, and dependency links. Local IDs such as R01 are planning IDs, not actual GitHub issue numbers.

No issues have been created from this workspace: the GitHub API CONNECT request is blocked by the environment proxy with HTTP 403. The GitHub CLI also reports that it cannot authenticate the current token. Run the publisher from a machine with working GitHub API access and an authenticated `gh` CLI that can create issues in this repository.

From the extracted `identity-issue-roadmap` directory, preview without network access:

```sh
python3 publish.py --dry-run
```

From that directory, publish using an authenticated GitHub CLI:

```sh
python3 publish.py --publish
```

The publisher reads all existing open and closed issues before any write. It reuses issues with matching roadmap markers and stops on an unmarked exact-title collision. It records created issue URLs in `published.json` after each write, so partial runs can resume. After all issues exist it resolves tracker, dependency, and reverse-dependency references. Reruns preserve text outside the generated links section and avoid creating duplicate marked issues. Run only one publisher at a time.

The script creates issues and updates their generated link sections. It does not create GitHub milestone objects, assign owners, add labels, commit files, or modify the immutable audit. Current roadmap milestone groupings and priority are recorded directly in issue bodies.

## Files

- `roadmap.json`: all issue titles, finding mappings, priorities, milestone groupings, and dependency edges.
- `issues/TRACKER.md`: tracker draft and complete historical audit evidence.
- `issues/R01.md` through `issues/R18.md`: implementation issue drafts.
- `audit.md`: exact original audit snapshot.
- `publish.py`: standard-library Python publisher; requires GitHub CLI for publication.
