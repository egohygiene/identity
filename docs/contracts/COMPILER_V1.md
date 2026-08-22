# Identity compiler v1 contract

## Purpose

The compiler core is the framework-neutral execution boundary behind the Brand Kit generator. It owns deterministic orchestration and mutation authority; concrete token, vector, raster, font, metadata, archive, and publication behavior lives behind replaceable adapters.

The v1 application flow is:

```text
read → validate → resolve → plan → render → verify → manifest
                                      │
                                      └─ apply only after explicit approval
```

`init`, `validate`, `plan`, and `handoff` remain the existing CLI surface. This compiler slice intentionally exposes a Rust library contract first; #11 supplies real projection adapters and package profiles before generation commands become a supported CLI promise.

## Core ownership

The compiler core owns:

- pure intent, resolved-identity, target, plan, diagnostic, evidence, and manifest models;
- ordered stage orchestration through `IdentityReader`, `IdentityValidator`, and `IdentityResolver` ports;
- adapter discovery and compatibility checks;
- deterministic input fingerprints and plan digests;
- mutation-free planning of creates, replacements, removals, unchanged files, warnings, and approvals;
- render/verify isolation before generated state can change;
- a transactional artifact-store port and local filesystem implementation;
- recovery evidence for interrupted generated-state transactions.

The compiler core does not own:

- DTCG source semantics already governed by the v1 source contract;
- Style Dictionary, `resvg`, font tooling, or any other projection implementation;
- networked creative generation;
- package/profile contents owned by #11;
- publication authority owned by consumer repositories.

## Adapter SDK

`ProjectionAdapter` exposes four operations:

1. `descriptor` — stable id, version, kind, compiler API major, determinism/offline guarantees, and capabilities;
2. `plan` — target-specific warnings and required approvals without mutation;
3. `render` — bytes from an immutable `ResolvedIdentity` and `ProjectionTarget`;
4. `verify` — bounded diagnostics and evidence over rendered bytes.

The registry rejects duplicate or malformed adapter identities. Planning blocks adapters that:

- target another compiler API major;
- do not guarantee deterministic output; or
- require network access in the compiler-owned path.

Provider-backed creation therefore remains an explicit creative-handoff concern rather than a hidden render side effect.

## Plan contract

`identity.compiler-plan/v1` is defined by [`compiler-plan.schema.json`](../../contracts/v1/compiler-plan.schema.json). A plan records:

- canonical project and source digests;
- the complete requested output root and manifest path;
- one ordered action per selected or stale generated artifact;
- adapter compatibility and version evidence;
- current and previous checksums where available;
- deterministic input fingerprints;
- warnings and stable diagnostics; and
- every approval identifier required before apply.

Plans are read-only. Existing untracked files require `replace-unmanaged:<path>` approval. Drifted managed files require `replace-drifted:<path>`. Stale generated files require `remove:<path>` before deletion. An unsupported adapter produces a visible `blocked` action rather than partial success.

## Incremental rebuilds

Each target fingerprint hashes:

- the canonical source digest;
- the normalized target request; and
- the complete adapter descriptor.

A generated file is `unchanged` only when:

1. its current checksum still matches the previous manifest;
2. its previous input fingerprint matches the new fingerprint; and
3. its adapter version is unchanged.

Anything else is explicitly created, replaced, removed, blocked, or reported as drift. The compiler never infers success from file existence alone.

## Render and verification boundary

Execution refuses plans with blocking diagnostics or missing approvals. All create/replace targets render and verify before the artifact store receives mutation authority. A verification failure therefore leaves generated state untouched. If one transient in-memory render succeeds before another render/verify failure, the command reports `partial` coverage but still applies nothing.

Target byte budgets are enforced before transaction entry. Adapter evidence is included in the manifest and remains distinct from later #12 accessibility/visual release gates.

## Manifest contract

`identity.compiler-manifest/v1` is defined by [`compiler-manifest.schema.json`](../../contracts/v1/compiler-manifest.schema.json). It records:

- project/source/plan digests;
- every selected generated output;
- output checksum and byte size;
- target/profile/media type;
- adapter id/version and target input fingerprint;
- the exact adapter descriptors used; and
- deterministic verification evidence.

No timestamp, random id, absolute machine path, ambient environment value, or network result is included. The same normalized input, adapter/tool version, and target request therefore produce byte-stable structured output where the adapter format permits it.

## Transaction and recovery boundary

`LocalArtifactStore` keeps transient state under:

```text
.cache/identity/transactions/<plan-digest>/
```

Before mutation it:

1. rechecks every planned current checksum to reject stale plans;
2. stages all verified writes;
3. backs up every replacement/removal and any existing manifest; and
4. writes a recovery journal.

Only then are staged files atomically promoted one path at a time. The manifest is promoted last and all manifested output checksums are re-read after apply.

A process interruption can leave the recovery journal behind. New plan/apply operations fail closed while any transaction workspace exists. Recovery is an explicit authority boundary: it restores replacements/removals from backups, removes newly created files, restores/removes the manifest as appropriate, and never writes under canonical `.identity/` source.

## Failure states and diagnostic families

Compiler diagnostics extend the existing `IDN` namespace:

| Range | Boundary |
| --- | --- |
| `IDN2000`–`IDN2099` | compiler request, source, and resolved-model invariants |
| `IDN2100`–`IDN2199` | adapter registration and compatibility |
| `IDN2200`–`IDN2299` | rendering, verification, serialization, and artifact budgets |
| `IDN2300`–`IDN2399` | drift, approvals, transaction, and recovery |

The stable failure states remain `invalid`, `unsupported`, `blocked`, `partial`, `failed`, and `drifted`. No partial or unsupported result is reported as verified success.

## Validation evidence

The compiler unit suite uses only local memory, temporary directories, and fixture adapters. It proves:

- mutation-free plans enumerate create/replace/remove operations, warnings, and approvals;
- identical normalized inputs produce identical output and manifest bytes;
- a second identical build resolves to unchanged output without rewriting its manifest;
- missing/networked adapters are visible and blocked;
- verification failures mutate nothing;
- an injected mid-transaction interruption is recoverable while canonical `.identity/` bytes remain unchanged; and
- duplicate adapter identities are rejected.

Actual DTCG/CSS/Tailwind/metadata/vector/raster/package golden fixtures belong to #11, which consumes this library boundary rather than changing it implicitly.
