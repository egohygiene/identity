# Identity initialization and delegated validation handoffs

This records the bounded initialization and EgoLint handoffs for
[Identity #99 checkpoint 3](https://github.com/egohygiene/identity/issues/99).
It distinguishes executable interfaces from future integration requirements.
It does not implement an initializer, install a validator, adopt an EgoLint
policy or assert that an adapter already exists. Cross-owner integration stays
with [Identity #108](https://github.com/egohygiene/identity/issues/108).

The Identity interfaces below were inspected at checkpoint 2 merge
[`03eaeac72e2cf69c7bf205dd80f53ca25d1629e4`](https://github.com/egohygiene/identity/commit/03eaeac72e2cf69c7bf205dd80f53ca25d1629e4)
on 2026-10-19. The [authoring worksheet](AUTHORING.md),
[examples](../../examples/v1/README.md) and
[adoption guide](ADOPTION.md) are the supported v1 authoring route.

## Existing initialization and authoring

`identity init` initializes **v0**, writing `.identity/identity.toml`,
`.identity/brief.md` and `.identity/sources/README.md`. Its `--force` option
permits replacement of those initialized files; it is not a v1 migration or
approval operation. `identity validate`, `plan` and `handoff` also retain their
v0 purpose. No `v1-init` command exists at the inspected implementation.

For v1, gather actual facts and review evidence using the worksheet, author
consumer-owned source, validate it, then explicitly generate selected outputs.
The examples may be exercised in disposable consumers. Their fictional
reviewers, rights and approval records must not become evidence for a real
identity. Existing approved material remains authoritative; unresolved creative
work belongs in candidates or references until its own review.

Use an immutable reviewed implementation containing checkpoint 2 and its
matching scripts/schemas. The published `v1.0.0` binary predates executable null
guidance. A matching `identity.project/v1` schema family or unchanged Cargo
package version does not establish implementation compatibility. Record the
exact implementation revision, consumed script hashes and selected profile
versions in consumer toolchain configuration before execution.

## Supported validation interfaces

| Interface | Contract and limits |
| --- | --- |
| `python3 scripts/validate_identity.py --repository-root "path/to/consumer" --format "json"` | Authoritative v1 source diagnostics; offline and read-only. Use the script from the selected immutable implementation. |
| The same command with `--snapshot` | Additionally records digests of consulted source files and declared directory paths. This read-set is not the canonical source digest or an output-verification receipt. |
| `identity v1-verify --repository-root "path/to/consumer"` | Embedded source preflight, producer-capability checks and read-only drift verification of selected core outputs at `assets/identity/`. |
| `identity v1-generate --repository-root "path/to/consumer"` | Explicit source preflight and transactional generation of selected core outputs; never a lint-time repair operation. |
| `identity v1-inspect --repository-root "path/to/consumer"` | Read-only retained-transaction inspection, independent of source validation; human output is not a delegated source-validation classification. |
| `identity v1-recover --repository-root "path/to/consumer"` | Explicit generated-state rollback under exclusive writer ownership; never an automatic lint-time operation. See [recovery](RECOVERY.md) and use a source/release containing these commands. |
| `--output-root "generated/identity"` on either v1 command | Selects a normalized repository-relative generated root outside `.identity/`; verification must select the consumer's actual root. |
| `identity::v1_consumer::V1ConsumerPipeline::load` and compiler library APIs | Structured Rust source/producer and planning boundaries for a deliberately compiled compatible consumer; not a new stable CLI JSON interface. |

The binary embeds the authoritative source validator and requires Python 3.11+
at execution. It selects `python3` on Unix or `python` on Windows, with an
explicit `IDENTITY_PYTHON` override available. It runs the validator in isolated
mode without consumer imports, site packages, a source checkout or network.
Missing execution prerequisites fail; validation must not install them or
silently choose another implementation.

Standalone source JSON uses `identity.diagnostics/v1` with `valid`, `repository`
and sorted `diagnostics`. Each diagnostic has `code`, `path`, `severity`,
`message` and `recovery`; `--snapshot` adds `snapshot`. Source validation returns
0 for valid, 1 for diagnostics, and 2 for bad arguments. A missing manifest is
reported as `IDN1001` loading failure. A wrong source schema reports `IDN1002`;
the embedded preflight classifies source diagnostics as `invalid`, rather than
inventing a separate unsupported-schema exit code.

The v1 binary commands return 0 on success, 1 on runtime failure and 2 on
argument errors. They have no `--format "json"` or structured report option at
this implementation. `CompilerError` exposes structured `kind` and diagnostics
through the Rust library; its kinds are `invalid`, `unsupported`, `blocked`,
`partial`, `failed` and `drifted`. The command-line error display ordinarily
prints the first diagnostic rather than the full structured result. A
missing/drifted selected package can produce a generic textual error with exit
1. An integration must not recover a complete machine classification by
matching English stderr or treating all exit-1 outcomes as findings.

| Existing diagnostic | Actual boundary |
| --- | --- |
| `IDN3301` / `invalid` | Producer-side input failure, including non-UTF-8 bytes at an `.svg` path. |
| `IDN3302` / `unsupported` | Embedded source preflight cannot execute or returns an unusable response, including a missing/unsupported Python runtime. |
| `IDN3303` / `drifted` | Consulted source changed after validation; load and plan again. |
| `IDN3304` / `unsupported` | Source bridge rejects a provenance asset outside its lowercase UTF-8 `.svg` capability before UTF-8 decoding. All provenance assets are inspected, including ancillary assets. |
| `IDN2305` / `drifted` | Existing generated compiler manifest cannot be parsed as the supported manifest structure. |
| `IDN2306` / `unsupported` | Existing generated compiler manifest names an unsupported schema. |

A governed PNG/font can therefore pass source validation while failing the
selected Rust producer. Preserve the rights/provenance record and report the
capability limit; do not rename extensions, remove governance or invent an
approved SVG master to force generation to pass. See the
[source/producer capability table](../contracts/IDENTITY_V1.md#source-authority-and-producer-capabilities).

Core `v1-verify` does not verify every independent optional projection. Select
the actual optional package and its documented producer from the same reviewed
implementation. Where no dedicated read-only verification command exists,
regenerate into an isolated disposable copy, then compare complete file
inventories and hashes against committed output. Preserve the original
consumer's canonical, generated and unrelated files. A source pass, selected
core-output pass and complete public-kit result remain separate evidence.

## Proposed EgoLint handoff conditions

The following conditions describe Identity-side evidence required for future
owner review. They are **not an accepted EgoLint enum**, an implemented
adapter, an enforcement policy or a promise of a new Identity report schema.
EgoLint owns applicability, normalized findings, execution states and
manual/observe/ratchet/enforce behavior. Identity owns source semantics,
producer capabilities and generated-output verification.

| Condition to distinguish | Evidence and required disposition |
| --- | --- |
| Absent v1 source | Record absence separately from validity. Distinguish no identity source from a v0-only `.identity/identity.toml` consumer; do not silently migrate it. EgoLint policy decides optional skip versus a required-source finding. Direct v1 validation still reports a loading failure. |
| Invalid source | Retain the validator's JSON diagnostics and exit result, including exact code/path/recovery. Do not generate, suppress malformed source or convert validation failure into an optional skip. |
| Unsupported capability | Preserve any valid-source result separately from unsupported runtime, producer, schema/profile or generated-state compatibility. Use actual structured evidence where available; unsupported execution cannot pass. Wrong source schema remains the current validator's invalid result. |
| Stale selected output | Source may be valid while selected output is absent, changed or bound to older source/profile/tool evidence. Run read-only verification; report the output finding without regenerating the consumer worktree. |
| Valid selected contract | Source is valid, selected producer is supported and declared selected outputs verify for the represented source. This proves neither independent optional packages nor creative approval, complete public-kit readiness or deployment. |
| Execution error or timeout | Retain failure to execute, invalid/malformed report, pin/hash mismatch and timeout separately from source/output findings. Missing evidence is not a successful check, including in observe mode. |

Before an adapter is implemented, its owner review must resolve the machine
boundary for producer/output failures: either consume a compatible structured
library boundary deliberately or agree a versioned command report. The current
binary's success/failure exit alone cannot supply the complete matrix. Do not
invent a JSON flag, duplicate Rust logic in EgoLint or classify unknown runtime
failure as a confirmed stale-output finding.

The reviewed integration must also pin the Identity implementation/artifact,
consumed scripts, Python/runtime requirement, profile versions, represented
consumer revision and output roots. Record actual commands, exits and selected
validation coverage; retain safe relative diagnostic locations and hashes.
Choose execution budgets and publication-safe evidence through the existing
owners. No implicit tool download, source generation, worktree repair, raw
private payload publication or mutation of human approvals belongs in checking.

## Verified owners and existing work

The following live issues were inspected on 2026-10-19. They are existing
coordination paths, not proof that Identity delegation is implemented or a new
blanket prerequisite for manual authoring.

| Owner and existing issue | Responsibility retained |
| --- | --- |
| [Identity #108](https://github.com/egohygiene/identity/issues/108) | Coordinate authoritative sources/consumers and the later bounded integration example; retain this handoff and resolve owner decisions before implementation. |
| [EgoLint #35](https://github.com/egohygiene/egolint/issues/35) | Capability detection/applicability, selection and unavailable/invalid decisions. |
| [EgoLint #36](https://github.com/egohygiene/egolint/issues/36) | Enforcement modes, normalized evidence and distinct execution failures; no duplicated policy in Identity. |
| [Relay #49](https://github.com/egohygiene/relay/issues/49) | Reusable pinned execution, retention and publication of EgoLint evidence; no reimplementation of Identity or EgoLint validation. |
| [Holon #41](https://github.com/egohygiene/holon/issues/41) | Selected Identity initialization/package references in future portable organization materialization; repository scaffolding stays with its owner. |
| [Realm #19](https://github.com/egohygiene/realm/issues/19) | Verified immutable tool installation and supported distribution/fallback selection; no identity authoring or publishing authority. |

EgoLint was inspected at immutable main revision
`834a230e6c0f4ee8b080a10d6c2d469be5eb6e1b`:

- Its [README](https://github.com/egohygiene/egolint/blob/834a230e6c0f4ee8b080a10d6c2d469be5eb6e1b/README.md)
  describes a source-buildable alpha and does not claim a published Cargo
  package, GitHub release or GHCR image.
- Its [integration contract](https://github.com/egohygiene/egolint/blob/834a230e6c0f4ee8b080a10d6c2d469be5eb6e1b/integrations/contract.json)
  names canonical run JSON/SARIF and check-only integration surfaces; its
  [integration guide](https://github.com/egohygiene/egolint/blob/834a230e6c0f4ee8b080a10d6c2d469be5eb6e1b/integrations/README.md)
  preserves private adapter payload and fix-authority boundaries.
- Its [complementary tool registry](https://github.com/egohygiene/egolint/blob/834a230e6c0f4ee8b080a10d6c2d469be5eb6e1b/.config/toolchain/complementary-tools.json)
  has no Identity adapter entry. It already distinguishes `applicable`,
  `not_applicable`, `missing_dependency`, `deliberately_disabled`, `passed`,
  `failed_findings`, `execution_error` and `timed_out`. The matrix above does
  not replace those owner-defined states.

No dedicated open initializer or Identity-delegation issue was found in the
scoped issue searches at that observation. Reuse #108 and the verified owner
work for intake; create no duplicate integration ticket from this checkpoint.
Repository-required files, engineering conformance, contribution enforcement
and installation remain external responsibilities, not new `.identity/` facts.

## Bounded future v1 initializer requirements

Manual v1 authoring remains supported. A later initializer implementation needs
an explicit owner-selected scope and review under #108 coordination. Its minimum
acceptance requirements are:

- Preserve the v0 `init`/`validate` interface. Use an explicit v1 selection;
  never reinterpret or overwrite existing v0/v1 source implicitly.
- Accept actual supplied project facts, selected profiles, local defaults and
  reviewed source. Compute byte digests mechanically. Never synthesize rights,
  reviewers, approvals, organizations, policy enforcement or public claims.
- Produce a separately reviewable candidate and show missing facts or review
  decisions honestly. An incomplete starter is not a valid approved identity.
- Refuse conflicting/unsafe paths and preserve consumer-owned, generated and
  unrelated files. Keep plan/apply/recovery authority explicit; no global
  scaffold rewrite or implicit profile enabling.
- Pin implementation/schema/profile compatibility and keep setup separate.
  Initialization must not download or silently install tooling, publish assets
  or regenerate output as a side effect of validation.
- Prove absent source, v0-only and existing v1 consumers; missing human facts;
  path conflicts; invalid/unsupported material; repeated invocation; unchanged
  inputs on failure; and validation of a candidate once real required facts and
  reviewed evidence are supplied.

This disposition fulfills #99's handoff-scoping requirement. Actual initializer,
EgoLint adapter and cross-owner rollout remain future reviewed work. Public
asset selection/download repairs remain [#101](https://github.com/egohygiene/identity/issues/101)
and [#105](https://github.com/egohygiene/identity/issues/105); neither a passing
source check nor this handoff closes them.
