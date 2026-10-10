# Identity decision validation

Identity [#69](https://github.com/egohygiene/identity/issues/69) adopts shared
validation in advisory mode while historical decision dispositions remain under
human review. [The policy](../.config/egolint/repository-intelligence.toml)
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
The workflow declares adoption `legacy` because migration is incomplete. These
are different dimensions: a successful job cannot accept a historical decision
or promote legacy coverage to conformance. Metadata, missing approval, lineage,
and index findings remain visible warnings. Roadmap, commit history, repository
contracts, and diagrams remain unknown in this bounded check.

Expected outcomes are `legacy` or `nonconformant` with `warning`, depending on
the inspected corpus. Runtime, acquisition, unsafe input, or evidence-retention
failure still fails execution. No skipped or unavailable check counts as a
pass. Inspect the retained semantic status, coverage, and actual artifact-upload
outcome separately. An ordinary PR represents GitHub's merge candidate SHA;
record it separately from the branch head. Hosted checks and live publication
are not established by these configuration files or local results.

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
        "repository-contracts": "unknown", "architecture-records": "legacy",
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
`collect_repository_adrs.py collect --adoption legacy` documented in Relay's
[ADR collector guide](https://github.com/egohygiene/relay/blob/4137cb07a017b7bbae2ee38fe9b039c58b0b17eb/docs/repository-adr-collector.md).
Its output must be `adr-collection.review.json` outside Identity. Exit `2`
retains partial/invalid evidence; exit `3` denotes a runtime/input denial.
Every review envelope remains `publication: denied` and is not a site snapshot.

After explicit disposition review and complete source validation, review a
separate opt-in to the shared `collect-adrs: true` build. It requires complete,
fresh validated ADR coverage; it cannot publish the current legacy review
envelope. Consumer-owned hosting, routes, composition, deployment receipts and
rollback remain separate acceptance work. Preserve the release-backed Brand Kit
at `identity.egohygiene.io` and the independent organization `/identity/`
experience described in the [publication guide](publication/IDENTITY_PAGES.md).
Record the Intelligence host before adding its canonical `/intelligence/decisions/`
route and consumer-owned `/decisions/` redirect; neither existing host is
reassigned by this adoption.

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
