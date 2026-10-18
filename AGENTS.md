# Identity repository instructions

Read [CONTINUITY.md](CONTINUITY.md) and verify its mutable state before selecting
work. The canonical program log is
[egohygiene/.github#30](https://github.com/egohygiene/.github/issues/30);
[Identity#69](https://github.com/egohygiene/identity/issues/69) owns this migration.

The managed block below is copied byte-for-byte from Aether
`dc8a16851f452763ef4f7fbe4bf057d4500b1921`,
`library/organization/projections/templates/decision-impact.AGENTS.md`
(module 0.3.0, draft). Its authoring skill is
[create-decisions-document v2.1.0](https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/library/organization/skills/architecture/create-decisions-document/SKILL.md).
Consult that exact source when no reviewed host installation is available;
record how it was loaded. This file does not install the skill or claim host
discovery. See [adoption and validation](docs/decision-validation.md) for the
local pins, commands and upgrade/rollback procedure.

<!-- BEGIN AETHER DECISION-IMPACT -->
<!-- aether-instruction {"id":"decision-impact","inherits":[{"contract":"egohygiene.architecture-decision/v1","policy_version":"1.2.0","revision":"a05b14f8b9e2772124f879f818e09a911e996ad8","source_url":"https://github.com/egohygiene/hygiene/blob/a05b14f8b9e2772124f879f818e09a911e996ad8/docs/decisions/POLICY.md","status":"accepted","approval_url":"https://github.com/egohygiene/hygiene/pull/72"},{"contract":"egohygiene.repository-intelligence/v1","contract_version":"1.0.0-alpha.1","revision":"5e0602265b6ac5e5165b89f418e55a3fd12f8a64","source_url":"https://github.com/egohygiene/hygiene/blob/5e0602265b6ac5e5165b89f418e55a3fd12f8a64/docs/ecosystem/REPOSITORY_INTELLIGENCE.md","status":"proposed"}],"status":"draft","version":"0.3.0","skill":"create-decisions-document"} -->
## Decision-impact checkpoint

Before implementation, inspect scoped instructions, pinned ecosystem context,
the local policy reference, roadmap, local ADRs and relevant organization ADRs.
Load `create-decisions-document` from the reviewed pinned Aether installation.
Apply its significance test and choose `create`, `update`, `supersede`,
`reference`, or `ADR not required` within the current role's permissions.

- **Create:** author a proposed ADR for a consequential choice not already governed.
  Historical reconstruction preserves evidence, uncertainty and distinct dates.
- **Update:** correct evidence or append dated outcomes without rewriting history.
- **Supersede:** propose a replacement; preserve the old record pending human
  disposition and validate lineage through the selected owner tools.
- **Reference:** cite the governing record when implementing an existing design.
- **ADR not required:** give one concise reason for routine work; create no duplicate.

Before issue completion or PR handoff, repeat the check against the actual diff.
Cite the governing/new/updated ADR or `ADR not required` with its reason. Preserve
known roadmap references; use real stable IDs and qualify cross-repository references:

```text
Roadmap-Step: AET-Q07
ADR-Ref: egohygiene/hygiene#ADR-0002
```

New records use four-digit `ADR-NNNN` IDs and stay proposed. Authorized padding migrations record each old/new ID and path while preserving the decision number and human disposition. Automated agents never mark an ADR accepted or assign
another non-proposed lifecycle state. Preserve human-authored dispositions;
implementation, merge and verification do not supply approval or rationale.
Use `docs/decisions/README.md` and the repository policy reference; preserve legacy
`DECISIONS.md` content until reviewed migration. Read-only roles remain read-only.

If the skill is missing, report it and prepare only an authorized evidence
inventory/draft; do not claim skill execution or completed consequential review.
This block preserves consumer-authored instructions and does not install or
guarantee enforcement on every PR. The skill owns detailed authoring procedures.

The module remains draft. It inherits the accepted
[Hygiene ADR policy v1.2.0](https://github.com/egohygiene/hygiene/blob/a05b14f8b9e2772124f879f818e09a911e996ad8/docs/decisions/POLICY.md)
with [recorded ratification](https://github.com/egohygiene/hygiene/pull/72).
The independent
[Repository Intelligence v1.0.0-alpha.1](https://github.com/egohygiene/hygiene/blob/5e0602265b6ac5e5165b89f418e55a3fd12f8a64/docs/ecosystem/REPOSITORY_INTELLIGENCE.md)
retains its proposed authority and existing immutable pin.
<!-- END AETHER DECISION-IMPACT -->
