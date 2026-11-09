# Repository Intelligence source adoption

Refs [Pace #13](https://github.com/egohygiene/pace/issues/13),
[Relay #101](https://github.com/egohygiene/relay/issues/101), and the
[organization acceptance gate](https://github.com/egohygiene/.github/issues/41).
The portable presentation was adopted in [Identity #141](https://github.com/egohygiene/identity/pull/141).
The shared source implementation is [Relay #171](https://github.com/egohygiene/relay/pull/171).
The next source slice follows [Relay #151](https://github.com/egohygiene/relay/issues/151)
and [Search #102](https://github.com/egohygiene/relay/issues/102), with owner
field attribution from [Observatory #29](https://github.com/egohygiene/observatory/pull/29).

This candidate extends Identity's existing repository Intelligence subtree with
bounded public Git Journey evidence and owner-supplied Search field attribution.
The existing canonical ADR source remains enabled. It adds no organization-site
copy, new deployer or provider capture.

## Exact review boundary

| Selection | Source |
| --- | --- |
| Consumer base | `6e3010687034f7ee7825cda2dc9ebe5b1a7830df`, verified Identity `main` |
| Candidate branch | `codex/intelligence-source-identity` |
| Current builder and provenance selection | `9358083e6dd8b15a0f2a3bb23c0b1e2b3ea3b2ff` in every current action and `relay-revision`/`relay_revision` binding in [`publish-brand-kit.yml`](../../.github/workflows/publish-brand-kit.yml) |
| Previous current Relay selection | `49046d88ef6fe2e31e9a9f443a61157b598efb78` |
| Intelligence source | Existing full publisher revision, or explicitly selected verified ancestor through `intelligence_revision` |
| Stable Brand Kit source | Existing annotated stable tag/revision and release-owned configuration, unchanged |

The current builder, composition verifier and deployment receipt must agree on
the same Relay revision. This is one consumer adoption, not a fleet pin sweep.
The newer shared generator is a candidate until its source and this consumer's
output are reviewed. A committed pin does not prove a release or deployment.
The separate advisory decision-validation workflow and its local adapter remain
at `ac2600f4619f64c75a0e499e0540d8f48d516f9c`; this publisher upgrade does not
repin that lane or the owner policy/validator sources.

## Repository pages and source authority

The shared Relay action generates `renderer/dist/intelligence/` within the
existing final site tree. Identity's single `Publish Identity Brand Kit`
workflow still builds the release-backed Brand Kit first, captures its baseline,
composes the Intelligence subtree, creates the consumer-owned `/decisions/`
alias and verifies the complete site before its existing deployment boundary.

Review the resulting repository overview, graph and `/intelligence/decisions/`
at `identity.egohygiene.io`. Follow graph links to source-bound ADR evidence;
module membership and position must not become a dependency or approval claim.
The generated HTML and native graph assets belong to Relay, so Identity does
not duplicate their route definitions or client implementation. The central
organization site remains a fleet overview and drill-down entry point.

`collect-adrs: "true"` remains enabled, alongside the new explicit
`collect-journey: "true"` and `search-attribution: "true"` selections. The source
and activity ref remain the same exact publisher/selected ancestor revision.
The existing full-history checkout supplies Git objects to Relay's bounded
read-only collector; it runs no consumer code and needs no new provider scope.
Generic commit evidence does not publish raw commit subjects, authors or emails.
Native coverage, bounds, exclusions and freshness remain as actually reported;
a bounded history is not promoted to complete history or delivery progress.

Search uses Observatory's versioned approved title/key/kind/state/repository
fields and its pinned matching algorithm. Opaque older records retain explicit
unavailable attribution. A match, field label or Git event supplies no new ADR
approval, implementation completion, health score or release/deployment proof.

No Roadmap, provider Work, Health, Releases or comparison baseline is selected.
Their missing evidence remains explicit. Compare retention stays an opt-in
handoff until two real source-bound captures and an explicit baseline lease
exist; this patch manufactures neither. Identity's canonical roadmap publication
intent, all ADR text/metadata/approvals/lineage and policy pins remain unchanged.

## Preservation and recovery

The workflow's jobs, triggers, conditions, permissions, concurrency, stable
release selection, source ancestry checks, artifact handoff, canonical origin,
route requirements and alias declaration remain byte-preserved apart from the
explicit current Relay revision bindings and the two source/normalization
opt-ins. There is no additional workflow or new execution gate.

[`publication/decisions-rollback.json`](../../publication/decisions-rollback.json),
its complete forty-file inventory, historical helper pin, archive digest,
consumer revision, recorded site digest and ordering remain unchanged. Historical
evidence is not repinned to the candidate. The existing capture must continue
to retrieve and verify the recorded bytes before promotion. A later Brand Kit
release or recovery-point refresh needs separate source and review evidence;
this patch supplies neither a new rollback point nor an exercised recovery.

The consumer live verifier reads every file in the shared build manifest,
checks source-binding equality and checks all captured Brand Kit files. New
portable graph assets are therefore covered by the existing complete inventory
mechanism when that verifier is eventually run. This is static inspection of
the mechanism, not an executed byte-preservation or live check.

## Parallel Identity work

At inspection, [draft #139](https://github.com/egohygiene/identity/pull/139)
was open at `413aae01f53205312cdba4fdae60222f9f16d605`, based on draft #138.
It modifies the same publisher and publication guide while preparing a native
Brand Kit source lane. [Draft #140](https://github.com/egohygiene/identity/pull/140)
was open at `78bb6815d226b79acf7a1c927afafd5f8e39d131` and also changes root
continuity and architecture/docs. Neither draft is incorporated or superseded.

Reconcile the current Relay selection semantically with #139's publisher when
choosing merge order. Keep its native source/release choice separate from this
bounded Intelligence upgrade. Reconcile `CONTINUITY.md` with #140; do not choose
one handoff wholesale and lose the other branch's deferred obligations.

## Other consumer disposition

Akashic remains a useful later populated-roadmap canary, but
[#197](https://github.com/egohygiene/akashic/issues/197) records an unresolved
native `EGO-INTEL-ROADMAP-STATE-001` finding: `AKA-Q03` is ready while prerequisite
`AKA-Q02` remains active. The current canonical file still contains that
conflict. Do not enable native roadmap adoption, infer a new human state or
relabel that source valid merely to populate a page. Its closed publication
canary #185 and frozen historical rollback remain separate evidence.

Hygiene's original ADR-0001 source/approval boundary and Empathy's producer
revision mismatch retain their existing owners. They do not block this
already adopted Identity ADR presentation, and they are not resolved here.

## Review and deferred qualification

Only static source and diff inspection is included. No native ADR collection,
site build, typecheck, tests, CI, workflow dispatch, artifact upload, browser,
mobile/keyboard/screen-reader review, byte comparison, Pages publication or
live verification was run; the user deferred those checks. No issue is closed.

The later qualification pass must inspect the exact candidate Relay source,
run fresh same-revision ADR and Git Journey admission, review generated
overview/Decisions/Journey/graph and owner Search attribution (including Unicode,
cross-field and unavailable cases), then qualify all explicit unavailable states
and the existing composed-site
and recovery paths. After separately authorized publication, compare the exact
manifest, source bindings, canonical URLs, logos/favicon and all preserved
Brand Kit files with retained review artifacts. Source review, artifact proof,
deployment result and live proof remain distinct.

ADR disposition: reference accepted ADR-0017/ADR-0019 and the existing proposed
ADR-0022 composition record, plus Hygiene ADR-0002's delivery-history boundary.
This bounded source adoption under the existing design changes
no durable ownership or publication boundary and needs no duplicate ADR;
ADR-0022 remains proposed. The pinned Aether decision-impact 2.1.0 and continuity
1.1.0 guidance at `dc8a16851f452763ef4f7fbe4bf057d4500b1921` was read for this
handoff; no authoring/validator execution or lifecycle acceptance is claimed.
