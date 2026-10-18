---
schema: egohygiene.architecture-decision/v1
id: ADR-023
title: Preserve and specify a shared canonical source digest
status: proposed
date: '2026-10-18'
decision_scope: repository
visibility: public
owners:
- egohygiene/identity
issue: https://github.com/egohygiene/identity/issues/74
pull_request: https://github.com/egohygiene/identity/pull/111
related:
- ADR-012
- ADR-014
- ADR-019
supersedes: []
superseded_by: []
affected_repositories:
- egohygiene/identity
affected_contracts:
- egohygiene.identity.source-digest/v1
implementation_status: in_progress
evidence:
- type: issue
  url: https://github.com/egohygiene/identity/issues/74
  description: Audit records legacy TOML disagreement and requests shared vectors and a release-binding migration.
approval: null
exceptions: []
---

# ADR-023: Preserve and specify a shared canonical source digest

## Context

ADR-012 governs local digest-pinned source, ADR-014 governs derived handbooks,
and ADR-019 preserves immutable releases. They do not specify the complete
cross-language inventory algorithm. Python includes a root legacy TOML entry
that Rust excludes; native path spelling and ordering also differ on Windows.
Changing the framing or ordering without a compatibility boundary can invalidate
release bindings even when source intent is unchanged.

## Decision

Propose [egohygiene.identity.source-digest/v1](../contracts/SOURCE_DIGEST_V1.md): retain the
historical Rust/Unix inventory exclusions, UTF-8 component ordering and NUL
framing, serialize repository-relative paths with `/`, and use identical fixed
vectors for Rust and Python. Reject included links/reparse points, non-regular
entries and nonportable/non-UTF-8 names. Apply the same inventory validation
before source preflight; excluded entries remain subject to their explicitly
declared source constraints.

Keep Python helpers inside the standalone stdlib validator already embedded in
the CLI. All Python projections delegate through their existing digest entry
point. Preserve closed generated model shapes and old artifacts. Corrected
producers must be selected by an exact new tool release; affected consumers
regenerate and review their complete package/projection set together.

## Alternatives considered and rejected

- Include root legacy TOML everywhere: changes existing compiler identities for
  valid coexisting v0/v1 sources.
- Sort whole path strings or introduce new framing immediately: changes hashes
  for ordinary nested Unix inventories without repairing the reported mismatch
  more safely. A future major digest contract can define a new serialization.
- Keep native paths, skip links or lossily convert names: allows platform drift
  or partial source identities and conflicts with authoritative preflight.
- Rewrite old release hashes or accept alternate hashes automatically: obscures
  the actual producer and violates immutable release evidence.

## Consequences and tradeoffs

Supported Unix compiler identities and existing goldens remain stable. Python
legacy coexistence and historical Windows output can require a new bound set.
Inventory validation becomes stricter for previously omitted invalid entries.
The inherited v1 framing is not self-describing, and its inventory excludes
external declared file bytes; complete preflight snapshots and immutable
source/artifact evidence remain necessary. A future expanded or length-framed
identity requires a new version rather than silently changing v1.

## Implementation and evidence links

The candidate implements the contract in
[`source_digest.rs`](../../src/v1_consumer/source_digest.rs) and the embedded
[`validate_identity.py`](../../scripts/validate_identity.py), with the
[`shared vectors`](../../tests/fixtures/source-digest-v1.json), Python
conformance suite and full consumer regression. The existing release workflow
executes both suites on Linux, macOS and Windows. Actual local and hosted
results belong in the PR and current continuity checkpoint; implementation or
CI does not grant lifecycle approval.

## Replacement or exit strategy

Retain historical tool releases, source revisions and whole artifact sets for
rollback. A replacement algorithm needs its own major identifier, model/binding
migration, shared vectors and human-reviewed release. Do not reinterpret old
bare hashes as a new algorithm or overwrite a published asset.

## Follow-up work

Review this proposal and the documented compatibility boundary. Issue #75 owns
optional guidance/release enforcement; #85–#87 consume this inventory during
later refactoring. Release and consumer owners separately approve publication
and atomic upgrades. Existing ADRs and their dispositions remain unchanged.
