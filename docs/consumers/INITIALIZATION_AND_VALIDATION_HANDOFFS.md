# Identity initialization and delegated validation handoffs

This records the bounded initialization and EgoLint handoffs for
[Identity #99 checkpoint 3](https://github.com/egohygiene/identity/issues/99).
It distinguishes executable interfaces from future integration requirements.
It does not install a validator, adopt an EgoLint policy or assert that an
adapter already exists. [Identity #108](https://github.com/egohygiene/identity/issues/108)
completed its bounded [coordination handoff](../work/108/CLOSEOUT.md); its closed
state does not establish downstream implementation. The explicit initializer
was delivered under [Identity #133](https://github.com/egohygiene/identity/issues/133).
The current finish campaign remains [#116](https://github.com/egohygiene/identity/issues/116).

The Identity interfaces below were inspected at checkpoint 2 merge
[`03eaeac72e2cf69c7bf205dd80f53ca25d1629e4`](https://github.com/egohygiene/identity/commit/03eaeac72e2cf69c7bf205dd80f53ca25d1629e4)
on 2026-10-19. The [authoring worksheet](AUTHORING.md),
[examples](../../examples/v1/README.md) and
[adoption guide](ADOPTION.md) are the supported v1 authoring route.

## Current checkpoint — 2026-11-21

At inspected main
[`afc368003bfc6a2101051229efd237c8d6fadf71`](https://github.com/egohygiene/identity/commit/afc368003bfc6a2101051229efd237c8d6fadf71),
the [explicit v1 initializer](V1_INITIALIZATION.md) is merged. Its
[local acceptance](../work/133/CLOSEOUT.md) covers fourteen Python cases and a
copied-binary Linux case, preserving existing source and missing human facts.
`v1-init` prepares a separate candidate; it does not adopt source, grant creative
approval or generate a Brand Kit. It remains absent from published `v1.0.0`.
Full engineering acceptance remains #70 and actual self-source, rights,
release and adoption remain #98. Manual authoring is still supported.

[EgoLint #35](https://github.com/egohygiene/egolint/issues/35) and
[#36](https://github.com/egohygiene/egolint/issues/36), its general capability
and enforcement issues, are now closed.
At inspected EgoLint
[`dcd4fc2e91c72e7bdafc002f2e5e55ab7e58478e`](https://github.com/egohygiene/egolint/commit/dcd4fc2e91c72e7bdafc002f2e5e55ab7e58478e),
its complementary-tool registry and capability selection still contain no
Identity adapter. General infrastructure delivery is not delegated Identity
validation. The machine-boundary and policy decisions below remain unresolved;
do not treat historical issue links as open implementation owners.

## Existing initialization and authoring

`identity init` initializes **v0**, writing `.identity/identity.toml`,
`.identity/brief.md` and `.identity/sources/README.md`. Its `--force` option
permits replacement of those initialized files; it is not a v1 migration or
approval operation. `identity validate`, `plan` and `handoff` also retain their
v0 purpose. At the historical 2026-10-19 inspection, `v1-init` did not exist;
the current explicit command is a separate operation, as described above.

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

## Ownership and historical coordination

The following issues were inspected on 2026-10-19. Their responsibilities remain
useful context; their historical scheduling and open state are not current
implementation claims or a blanket prerequisite for manual authoring.

| Owner and existing issue | Responsibility retained |
| --- | --- |
| [Identity #108](https://github.com/egohygiene/identity/issues/108) | Coordinate authoritative sources/consumers and the later bounded integration example; retain this handoff and resolve owner decisions before implementation. |
| [EgoLint #35](https://github.com/egohygiene/egolint/issues/35) | General capability infrastructure, now closed; not a delivered Identity adapter. |
| [EgoLint #36](https://github.com/egohygiene/egolint/issues/36) | General enforcement/evidence infrastructure, now closed; not a delivered Identity adapter or duplicated policy in Identity. |
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
scoped issue searches at that 2026-10-19 observation. #108 served as intake
for that checkpoint. At its 2026-11-02 closeout, the initializer requirements
were transferred to #133 after a fresh duplicate search. Delegated validation
was coordinated through EgoLint #35/#36 and Relay #49 at that dated checkpoint.
The current observation above supersedes those two EgoLint open-state claims.
That coordination did not implement a specific Identity adapter or complete
producer report boundary.
Repository-required files, engineering conformance, contribution enforcement
and installation remain external responsibilities, not new `.identity/` facts.

### Repository contract adoption boundaries

Identity specifies and validates consumer-owned identity. It does not decide
which repositories must adopt it. The current cross-owner gap is separate from
the existing finish campaign:

[Hygiene #128](https://github.com/egohygiene/hygiene/issues/128) captures the
later applicability, baseline, delegated-checking and adoption work. It does
not make that rollout a new prerequisite for Identity's original completion
criteria or existing manual consumer proof.

| Concern | Canonical owner and observed boundary |
| --- | --- |
| Required Identity applicability and exceptions | Hygiene. Its [presentation profile](https://github.com/egohygiene/hygiene/blob/e296539a8891ba75ebe3f9816fb7aec5c7c1fc21/catalog/repository-presentation-profile.json) remains proposed `1.0.0-alpha.1`; a public repository banner requirement is not comprehensive v1 source compliance. |
| Composed repository baseline and golden proof | Empathy. Its [foundation catalog](https://github.com/egohygiene/empathy/blob/e6dbd6b2693786ef331e7f11638ebbbd7a57bfa6/foundation/catalog.json) still selects `.identity/identity.toml` for the product profile. Presence of that v0 file does not prove v1 validity. |
| New-repository materialization | Holon; reuse its reviewed scaffolding and presentation seams rather than making Identity a repository-file generator. |
| Delegated checking and evidence execution | EgoLint and Relay respectively. The proposed conditions above require an actual compatible adapter before enforcement. |
| Existing-repository adoption | Pace and each consumer; preview, review, verify and retain rollback rather than bulk-apply an unreviewed profile. |

These observations do not activate a required-files policy or update any
consumer pin. A later applicability contract must keep source validity,
selected-output verification and complete public-kit readiness separate. A
small repository need not publish every optional surface to validate the
identity it actually declares. Human facts, rights and same-subject approvals
cannot be supplied by a passing check.

## Initializer acceptance requirements and retained integration

The following requirements scoped #133 and are retained for compatibility.
Its implementation and local acceptance are linked above; they are not a new
initializer backlog. Full platform/CI acceptance remains with the existing
quality owners, and manual v1 authoring remains supported:

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

The original disposition fulfilled #99's handoff-scoping requirement. The
initializer now has its own local acceptance; the EgoLint adapter and
cross-owner rollout remain future reviewed work. The selected public-asset
and kit-assembly scopes under [#101](https://github.com/egohygiene/identity/issues/101)
and [#105](https://github.com/egohygiene/identity/issues/105) are closed. Actual
Identity self-source, rights, release and dogfood remain with #98; neither a
passing source check nor this handoff completes them.
