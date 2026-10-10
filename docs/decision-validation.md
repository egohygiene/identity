# Identity decision validation

Identity [#69](https://github.com/egohygiene/identity/issues/69) adopts shared
validation in advisory mode after the explicit
[2026-10-10 human disposition](decision-ratification-2026-10-10.md). [The policy](../.config/egolint/repository-intelligence.toml)
selects EgoLint's existing rules; [the workflow](../.github/workflows/decision-validation.yml)
calls Relay without copying its validator or acquiring publication authority.

## Pins and expected results

| Input | Reviewed immutable source |
| --- | --- |
| Relay workflow and local adapter | `4137cb07a017b7bbae2ee38fe9b039c58b0b17eb` |
| Hygiene ADR policy | `c589587395750cd1c79c6fa0bef010189c547249` |
| EgoLint architecture validator | `933472b6322d2060c487e5a8a6f0bc5197696af0` |
| Holon materialization contract | `660b941f99618806fcadd589bcdae61c519f96e4` |

Relay's `1.0.0-alpha.2` architecture profile verifies source artifact digests.
This is reviewed source adoption, not a claim that every input is released.
The separately pinned roadmap/projection contract entries in the TOML retain
their proposed authority; the accepted ADR policy does not promote them.

The TOML declares ADR source `present` so the native validator inspects it.
The workflow now declares adoption `present` for the canonical corpus. These
are different dimensions: a successful job cannot accept a historical decision
or turn source presence into conformance. Metadata, approval, lineage,
and index findings remain visible if a future change introduces them. Roadmap, commit history, repository
contracts, and diagrams remain unknown in this bounded check.

The intended ADR-domain result is valid metadata and complete observed
collection after the approved migration. Repository-contract, roadmap/history
and diagram domains remain explicitly uncollected; whole-repository status may
therefore remain incomplete/warning. Report actual results for each immutable
source and domain without promoting those gaps to conformance. Runtime, acquisition, unsafe input, or evidence-retention
failure still fails execution. No skipped or unavailable check counts as a
pass. Inspect the retained semantic status, coverage, and actual artifact-upload
outcome separately. An ordinary PR represents GitHub's merge candidate SHA;
record it separately from the branch head. Hosted checks and live publication
are not established by these configuration files or local results.

## Ratified corpus checkpoint — 2026-10-10

The [ratified-source receipt](evidence/identity-adrs-ratified-2026-10-10.json)
binds source `12227dad43c90b02e14971030f22242f3a205c9d` and observation
`2026-10-10T15:43:57Z`. Immutable ADR collection exited 0, reported ready,
and collected all 21 accepted decisions with complete/current coverage.
Hygiene and coverage checks were valid, Observatory normalized the input,
and EgoLint retained incomplete status for uncollected domains.

Architecture validation exited 0 with incomplete/warning status: five warnings
for unknown surfaces, unavailable diagram semantics and the bounded history
scan; no ADR metadata, lifecycle, index or lineage findings remain. Two native
replays were byte-identical. This is ADR-domain admission, not complete
repository-wide conformance.

The shared production action also ran locally against two clean full-history
checkouts. Its fresh ADR admission and bundle validation passed; all 19 output
files were byte-identical. The Decisions page has 21 records, declared approval
evidence and immutable canonical source links, with no broken local links or
anchors. Acceptance does not imply implementation completion: twelve records
are implemented, seven in progress and two not started.

That checkpoint did not deploy the generated artifact. It remains an immutable
receipt for the 21-record source above, not evidence for later source changes.
The publication implementation now selects the existing Brand Kit host for
`/intelligence/decisions/` and its consumer-owned `/decisions/` alias as described
below. New proposed ADR-022 makes the candidate corpus 22 records; it requires
fresh native admission and production-build evidence. The earlier receipt and
its bytes remain unchanged.

## Local validation through the same adapter

Use trusted source checkouts outside Identity at the exact pins above. Follow
Relay's pinned [runtime preparation instructions](https://github.com/egohygiene/relay/blob/4137cb07a017b7bbae2ee38fe9b039c58b0b17eb/docs/repository-architecture-validation.md#prepare-the-trusted-runtime)
for CPython 3.12/Linux x86_64, hash-locked Python packages and Rust 1.85.1.
Acquire dependencies explicitly, then prepare and validate offline. An ADR
collector runtime receipt is **not** an architecture-validator receipt.

```bash
python3 "/trusted/relay/scripts/run_repository_architecture_validation.py" prepare \
  --hygiene-source "/trusted/hygiene" \
  --egolint-source "/trusted/egolint" \
  --holon-source "/trusted/holon" \
  --output "/trusted/architecture-runtime"
```

Create a request outside the consumer from Relay's unchanged profile. Replace
the example paths and use a full Identity commit for reproducible evidence.
Before committing, `working-tree` explicitly selects the candidate and cannot
establish immutable-revision acceptance.

```bash
python3 - "/trusted/relay" "/review/identity-architecture-request.json" "working-tree" <<'PYTHON'
import hashlib
import json
from pathlib import Path
import sys

profile_bytes = (Path(sys.argv[1]) / "catalog/repository-architecture-validation.json").read_bytes()
request = {
    "schema_version": "relay.repository-architecture-validation-request/v1",
    "profile": {
        "version": json.loads(profile_bytes)["version"],
        "sha256": hashlib.sha256(profile_bytes).hexdigest(),
    },
    "repository": {
        "id": "egohygiene/identity", "visibility": "public", "root": ".",
        "represented_revision": sys.argv[3],
    },
    "mode": "advisory",
    "adoption": {
        "repository-contracts": "unknown", "architecture-records": "present",
        "diagram-sources": "unknown",
    },
    "inputs": {
        "repository_contracts": [],
        "repository_intelligence_policy": ".config/egolint/repository-intelligence.toml",
        "diagram_roots": [],
    },
    "bounds": {
        "maximum_findings": 256, "maximum_scanned_files": 10000,
        "maximum_scanned_bytes": 104857600,
    },
    "output": {"format": "json", "path": ".reports/architecture-validation/result.json"},
}
Path(sys.argv[2]).write_text(json.dumps(request, indent=2) + "\n", encoding="utf-8")
PYTHON

python3 "/trusted/relay/scripts/run_repository_architecture_validation.py" run \
  --repository-root "/sources/identity" \
  --request "/review/identity-architecture-request.json" \
  --runtime "/trusted/architecture-runtime"
```

The adapter retains bounded JSON/SARIF evidence under `.reports/architecture-validation/`.
It reads consumer source without executing it or rewriting ADRs. Keep generated
reports out of canonical source unless separately reviewing a bounded evidence
record. The [shared workflow contract](https://github.com/egohygiene/relay/blob/4137cb07a017b7bbae2ee38fe9b039c58b0b17eb/docs/repository-architecture-workflow.md)
defines the equivalent CI parameters and retention behavior.

## Review collection and later publication

For normalized review evidence, use the separately prepared runtime and
`collect_repository_adrs.py collect --adoption present` documented in Relay's
[ADR collector guide](https://github.com/egohygiene/relay/blob/4137cb07a017b7bbae2ee38fe9b039c58b0b17eb/docs/repository-adr-collector.md).
Its output must be `adr-collection.review.json` outside Identity. Exit `2`
retains partial/invalid evidence; exit `3` denotes a runtime/input denial.
Every review envelope remains `publication: denied` and is not a site snapshot.

The selected implementation extends the existing Brand Kit publisher on
`identity.egohygiene.io` with the Relay `collect-adrs: true` build pinned to
`f19b65b3f8bd8466884dee5529fa77f2430440b6`. This publication pin includes
[Relay PR #138](https://github.com/egohygiene/relay/pull/138)'s baseline path-order
repair and [Relay PR #141](https://github.com/egohygiene/relay/pull/141)'s shared
hidden-card styling repair for [Relay #139](https://github.com/egohygiene/relay/issues/139).
It also adopts [Relay PR #142](https://github.com/egohygiene/relay/pull/142)'s
shared organization/GitHub navigation marks and organization favicon.
The advisory validation adoption retains its separate
`4137cb07a017b7bbae2ee38fe9b039c58b0b17eb` source above. Historical receipts keep
their original source pins; the
[filtering checkpoint](evidence/identity-decisions-filtering-2026-10-10.json)
records the repaired canary's verification. The later shared navigation and
organization-favicon update requires its own publication and live asset checks.
[Proposed ADR-022](decisions/ADR-022-decisions-publication-composition.md) records
this new composition choice; the earlier R1 approval covers only ADR-001–021.
The production build requires complete, fresh validated ADR coverage at its
full source commit and does not publish a review envelope. Proposed records
remain proposed in the generated view.

Capture every existing Brand Kit file before adding `intelligence/` and the
consumer-owned `/decisions/` alias. Require byte-preserved Brand Kit content,
collision-free routes, immutable source bindings and the exact composed
artifact digest. The Brand Kit still uses its separately selected stable
release; current ADRs do not become release-owned assets. The independent
organization `/identity/` experience keeps its existing owner and gates.

A successful local artifact, hosted execution, Pages deployment and live
content verification are separate results. Retain the shared composition and
deployment receipts, verify live bytes against the retained artifact, and
establish a recoverable prior deployment before claiming publication complete.
Manual replay of an ancestor ADR source still requires fresh collection.
See the [publication checkpoint](publication/IDENTITY_PAGES.md#decisions-composition-checkpoint--2026-10-10)
for routes, source identities and rollback requirements. Deployment results and
maintainer feedback remain required before fleet follow-up.

Two existing architecture-preview references in
`publication/identity-experience.content.json` need a later reviewed correction:

- `ADR-013-public-identity-reference-page.md` does not exist. The intended
  renderer theme belongs to `ADR-010-reference-renderer-boundary.md`, with its
  actual immutable-view-model title and supported summary.
- `ADR-006-authoring-generated-state-boundary.md` does not exist. The intended
  deterministic/generative boundary belongs to
  `ADR-003-deterministic-projection-boundary.md`, with its actual title and summary.

The content file is digest-bound by `experience/visual-baselines.json`, whose
review rules require human review of fresh wide/narrow screenshots before a
baseline update. This checkpoint preserves those bytes and the recorded review;
it neither substitutes new content under the old digest nor claims the links
work. Reconcile the content, source links, screenshots and baseline together
during publication follow-up.

## Upgrade and rollback

Review one exact Relay pin change with its profile, owner schema compatibility,
local replay and retained CI evidence. Update policy tuples only when the
selected owner catalog supports them. Preserve historical records, dispositions
and the migration map; never enable required mode because an advisory run is
green. A reviewed revert of the workflow/policy change removes this check
without modifying Brand Kit publication, ADR history or deployment rollback.
