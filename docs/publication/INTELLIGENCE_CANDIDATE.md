# Repository Intelligence source feeds and native Compare adoption

Refs [Relay #152](https://github.com/egohygiene/relay/issues/152),
[Pace #13](https://github.com/egohygiene/pace/issues/13),
[Identity #98](https://github.com/egohygiene/identity/issues/98) and
[organization #41](https://github.com/egohygiene/.github/issues/41).

The existing `Publish Identity Brand Kit` workflow remains the sole Pages
publisher. Its canonical ADR, bounded Git Journey and attributed Search sources
stay enabled. Current default-branch push/manual builds add actual bounded
Work, Health and Releases captures plus admitted declared dependencies. Optional
manual Compare follows that same native build, before consumer composition
verification and upload. The organization site remains a fleet overview linking
into each repository's site. Source delivery also references Relay
[#146](https://github.com/egohygiene/relay/issues/146),
[#149](https://github.com/egohygiene/relay/issues/149) and
[#150](https://github.com/egohygiene/relay/issues/150); declared dependency
admission references [#148](https://github.com/egohygiene/relay/issues/148).

## Exact source selection

| Selection | Source |
| --- | --- |
| Consumer base | Identity `e2457ef14b44f52faa03dc402bc3099434d7b028` |
| Candidate branch | `codex/intelligence-native-compare` |
| Current Relay producer, builder, Compare and provenance | `981ddf4367c67fcd625e54321d95bab027f6c0f2` throughout [`publish-brand-kit.yml`](../../.github/workflows/publish-brand-kit.yml) |
| Previous current Relay selection | `9358083e6dd8b15a0f2a3bb23c0b1e2b3ea3b2ff` |
| Intelligence source | Exact publisher revision, or the existing explicitly selected ancestor when Compare is off |
| Stable Brand Kit source | Existing annotated stable tag/revision and release-owned configuration |

The shared source is the reviewed [Relay #176](https://github.com/egohygiene/relay/pull/176)
revision pinned above. The producer, builder, post-build composer, composition
checks and deployment receipt agree on that immutable selection. A source pin
or merge supplies no runtime, artifact or deployment proof.
The advisory decision-validation workflow retains its separate
`ac2600f4619f64c75a0e499e0540d8f48d516f9c` selection.

## Manual modes

The existing workflow dispatch adds `intelligence_compare`, default `off`, and
`intelligence_compare_baseline`, default empty. Push and release paths keep
Compare off. The single existing build job receives `actions: read` for exact
same-run capture intake and retained-baseline selection plus `issues: read`,
`pull-requests: read` and `checks: read` for bounded provider reads. Its other
permissions and downstream job conditions remain as before.

- **off:** no snapshot retention or post-build Compare step runs. Current
  source feeds still run on matching default-branch push/manual contexts.
- **seed:** require an empty baseline record and capture one real current pair.
  Supply `expected-baseline: none`; Compare remains unavailable. Successful
  ordinary upload is a candidate handoff for a later run, not a fabricated
  historical comparison.
- **compare:** require one complete JSON selection from a real earlier
  successful ordinary upload and successful producer attempt. No name/latest
  lookup or partial selection is accepted.

Enabled modes require dispatch from the configured default branch with the
publisher, Intelligence source and event SHA all equal. A branch/head race or
historical ancestor replay is denied for Compare. Native collection and Compare
both use the provider producer's actual UTC evaluation boundary after its
captures. Existing source ancestry checks remain intact.

The JSON selection has exactly six string fields: `lease`, `artifact_id`,
`artifact_digest`, `source_commit`, `run_id`, `run_attempt`. The lease is the
action's actual `next-baseline-lease`; its ZIP digest is the actual
`artifact-digest`, with its optional `sha256:` prefix. The artifact ID, source SHA,
run and attempt must identify that exact public Identity upload. Duplicate or
extra fields are rejected. No example identifiers or baseline are supplied.
The shared action independently rechecks provider identity, successful attempt,
age, access, original pair, digest lease and normalization compatibility.

## Current provider source handoff

Capture is enabled only for push/manual dispatch on the configured default
branch when the checked-out publisher, Intelligence source and event SHA match.
Release events and existing historical ancestor replay retain their earlier
native source path, original clock and disabled dependency/provider options.
No PR or workflow-run artifact is substituted for a current capture.

The pinned producer confirms public repository/head admission, captures bounded
issue/PR, commit-matched check-run and published release evidence, and packs a
closed source bundle. Raw bodies, comments, actors, emails, logs and optional
titles are excluded. Provider failures and bounded pagination remain explicit;
an empty or partial inventory never becomes complete conformance. Release
metadata does not establish deployment or installation success.

An ordinary same-run upload retains that exact closed capture bundle. Its real
artifact ID, ZIP digest and producer evaluation clock feed the native builder's
existing authenticated intake; the builder freshly evaluates the captured
sources and combines them with canonical ADRs and Journey before attributed
Search normalization. `collect-dependencies` is enabled only on these current
capture paths. It consumes Hygiene's exact reviewed public catalog and declared
direct consumption, with runtime/package adoption still uncollected and no
additional coverage domain invented.

The bounded producer receipt is retained independently as an ordinary artifact,
including after a later build failure, and copied into the private publication
handoff on success. Private `source-binding.json` records actual capture
artifact ID/digest, run/attempt and evaluation clock. Neither raw captures nor
these operational records enter the public Intelligence tree.

## Source-preserving composition

The native action first builds `renderer/dist/intelligence` and retains its
actual original pair plus receipt under `.cache/repository-intelligence/sources`.
Compare consumes those exact files under `search-attribution-v1`. It verifies
the native receipt, represented source, immutable generator and existing
bundle, then recomposes only `compare/index.html` and its build manifest from
the admitted in-memory owner evidence. All other payload files, including
Journey, Search, Decisions and `provenance.source_collection`, keep exact bytes.
The complete bundle is validated again. Missing/incompatible/expired baseline
evidence withholds comparison honestly and preserves the old retained artifact.

The existing consumer alias and `verify-composition` steps follow Compare.
They read the **final tree and final manifest**, rather than using the earlier
native builder's manifest/digest outputs. Deployment revalidates the downloaded
final tree, and the existing live verifier derives its inventory from that final
manifest. No stale pre-composition digest becomes publication authority.

The ordinary artifact action retains its operational receipt separately.
Identity also records an optional private `compare.selection_candidate` in
the existing retained `source-binding.json` when an upload actually returned
an ID. Copy that complete record for a later selection only after the entire
producer attempt succeeds. It is null without an upload. This is no mutable
cloud pointer and no claim of global compare-and-swap. These operational fields
and the original pair never enter the public site bundle.

## Preservation and remaining evidence

The release-backed Brand Kit, product assets, canonical URL, existing source
admission, deployment/recovery jobs, concurrency, route requirements and
consumer-owned `/decisions/` alias retain their contracts. There is no new
workflow or deployer. Canonical ADR text, approvals, lineage, roadmap and
policy/validator pins remain unchanged. Other producer inputs retain their
source owners; generic GitHub check runs do not resolve an unrelated normalized
report's producer-revision mismatch or imply an organization-wide sanity pass.

[`publication/decisions-rollback.json`](../../publication/decisions-rollback.json)
and all historical evidence retain their exact bytes, digests, pins, ordering
and source identities. This slice supplies no new recovery point or exercised
rollback. Optional comparison does not turn semantic difference into causality,
human approval, delivery completion or health conformance.

No native collection, tests, builds, CI, workflow dispatch, artifact upload,
browser, publication, live verification or rollback exercise was run; the user
deferred those checks. Source/syntax review is implementation evidence only.
Real first/second compatible captures and exact provider upload identities
remain required for live Compare acceptance under Relay #152/#101 and Pace #13.
No issue closes from this source adoption.

ADR disposition: reference accepted ADR-0017/ADR-0019, the existing proposed
ADR-0022 composition record and Hygiene ADR-0002's delivery-history boundary.
This is bounded implementation of the existing composition design with an
explicit opt-in and no new durable ownership or publication authority; no
duplicate ADR is required. ADR-0022 remains proposed. The pinned Aether
decision-impact 2.1.0 and continuity 1.1.0 guidance at
`dc8a16851f452763ef4f7fbe4bf057d4500b1921` was read from Git source; no native
validator execution or human lifecycle acceptance is inferred.
