## Outcome

Bring **egohygiene/identity** to the current architectural moment under the organization ADR contract by reconstructing only consequential, evidence-backed decisions from repository history, then keep the record current through the managed agent decision-impact workflow.

This is a bounded repository-local migration. It must not redefine organization policy or build a repository-specific validation or website framework.

## Scheduling gate

This issue is intentionally queued for **after the shared ADR system is operational**. Do not begin the backfill unless the maintainer explicitly overrides the gate and the following foundations are ready:

- [ ] [Hygiene #15](https://github.com/egohygiene/hygiene/issues/15) is human-ratified and the approved policy commit is available to pin.
- [ ] [Holon #6](https://github.com/egohygiene/holon/issues/6) provides migration-safe ADR scaffolding.
- [ ] [Relay #5](https://github.com/egohygiene/relay/issues/5) provides reusable conformance validation.
- [ ] [Relay #27](https://github.com/egohygiene/relay/issues/27) and [Relay #33](https://github.com/egohygiene/relay/issues/33) provide the shared Repository Intelligence shell and publication workflow; the **/decisions/** renderer from [Relay #30](https://github.com/egohygiene/relay/issues/30) is already delivered.
- [ ] [Pace #5](https://github.com/egohygiene/pace/issues/5) is ready to coordinate reviewed fleet adoption.

<!-- identity-intelligence-coordination:v1 -->
## Coordination with Identity stabilization

Coordinate this repository pilot with [Identity #70](https://github.com/egohygiene/identity/issues/70) and [Pace #5](https://github.com/egohygiene/pace/issues/5), preserving this issue's existing shared-system scheduling gates. #70 is related stabilization work, **not** a requirement to finish all 18 audit issues before Observatory or read-only ADR collection.

Passive inventory and read-only collection are distinct from this issue's historical backfill, migration, continuous capture, and publication work. They may proceed in parallel under authorized visibility and the shared input/coverage contract, with missing, stale, partial, and unverified evidence reported honestly. They do not bypass the foundations or human authority needed for migration/publication.

The migration plan should identify only Identity repairs required by the operations it actually exercises, with concrete evidence. Unrelated compiler, renderer, development-environment, or module cleanup must not become accidental collector prerequisites. #71–#73 have merged through PR #89; do not infer a new stable release or deployment from that merge.

#83 owns reconciliation of canonical ROADMAP.md and current publication documentation. It must preserve separate ownership for the release-backed Brand Kit, the organization `/identity/` experience, and proposed Intelligence views. Adoption here must explicitly declare the Intelligence publication target and may not silently replace existing Pages/domain/route ownership.
<!-- /identity-intelligence-coordination:v1 -->

## Starting point from the 2026-09-12 fleet scan

A standard **docs/decisions/** surface exists. Preserve its inline and detailed history, map aliases explicitly, and use it as an early validate-first migration only after the foundation is accepted.

Recheck the default branch and open pull requests before implementation because this observation can become stale.

## Historical extraction workflow

1. Inspect the full reachable Git history, tags, merged pull requests, issues, release notes, roadmap, architecture documents, and existing decision logs.
2. Identify only durable choices that meet the Hygiene significance test: contracts/schemas, ownership, security/privacy/licensing/provenance, durable dependencies or frameworks, cross-repository direction, source authority, or expensive-to-reverse architecture.
3. Group evidence by decision rather than producing one ADR per commit or issue.
4. Prefer contemporaneous evidence. When the rationale or authority cannot be proven, record the gap in the migration map instead of inventing intent.
5. Preserve legacy IDs, prefixes, filenames, bodies, links, and blame context. Resolve collisions or ambiguous canonical records with a human before generation.
6. Draft new historical records as **proposed** unless durable human disposition evidence supports another policy-valid state. A merge, release, or agent conclusion is not acceptance.
7. Link implementation and validation evidence independently from decision status.
8. Submit small, reviewable pull requests and stop for maintainer review at ambiguous status, ownership, privacy, or supersession decisions.

The goal is useful synchronization with honest uncertainty—not a claim that the past has been reconstructed perfectly.

## Repository baseline and continuous capture

- [ ] Add or validate **docs/decisions/policy-reference.json** pinned to the approved Hygiene policy version and full commit.
- [ ] Establish **docs/decisions/README.md** as the canonical complete index.
- [ ] Create or migrate records at **docs/decisions/ADR-NNN-short-slug.md**, preserving documented legacy exceptions.
- [ ] Keep a pre-existing root **DECISIONS.md** only as a concise compatibility/navigation entrypoint.
- [ ] Consume the Aether-managed decision-impact guidance in repository agent instructions; do not copy and fork the global policy prose.
- [ ] Require the decision-impact check before an issue is declared complete and before PR handoff: create/update/supersede an ADR when the completed work changed a durable decision, or record **ADR not required** with one concise reason.
- [ ] Validate locally and in CI through the shared EgoLint/Relay contracts.
- [ ] Publish the validated repository decision ledger at GitHub Pages **/decisions/** through the shared Relay projection, with source revision, freshness, lineage, and evidence links.
- [ ] Keep generated indexes/site data derived and reproducible; Markdown ADRs remain repository-owned source.
- [ ] Apply public/private visibility rules and never leak protected issue text, identities, local paths, credentials, or private rationale into public output.

## Acceptance criteria

- [ ] The reviewed plan links #70 and #83, separates read-only collection from migration/publication gates, and records only operation-specific Identity prerequisites without requiring all 18 stabilization issues.
- [ ] A reviewed migration map inventories every pre-existing decision surface, ID, status claim, collision, and evidence gap.
- [ ] Material historical decisions are represented to the evidence limit; routine implementation noise is excluded.
- [ ] Every non-proposed disposition has resolvable human authority evidence, or remains explicitly blocked for human review.
- [ ] Decision status, implementation status, and verification evidence remain independent.
- [ ] The policy pin, ADR corpus, index, lineage, and legacy exceptions pass the shared validator.
- [ ] Repository agent guidance performs the decision-impact check on future issue/PR completion.
- [ ] The shared GitHub Pages build exposes a working, accessible **/decisions/** view without creating a second source of truth.
- [ ] The final migration PR documents omissions, uncertainty, privacy decisions, validation commands, and rollback.

## Non-goals

- Perfectly narrating every historical implementation choice.
- Retroactively accepting decisions based only on Git activity.
- Renumbering or silently rewriting legacy history for cosmetic consistency.
- Copying Hygiene policy, Aether guidance, Relay workflows, or visualization code into this repository.
- Completing this issue before the shared system milestone is ready.