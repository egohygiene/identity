---
schema: aether.architecture-document/v1
id: identity-dependency-policy
title: Identity Dependency Policy
kind: policy
version: 1.0.0
status: active
owners:
  - egohygiene
created: 2026-08-20
updated: 2026-08-20
governed_by:
  - identity-architecture
depends_on:
  - identity-brand-kit-foundations-evaluation
related:
  - identity-decisions
supersedes: []
---

# Dependency policy

## Purpose

Identity bootstraps from mature standards and tools without allowing them to
become unbounded product architecture. This policy governs selection, pinning,
updates, security review, reproducibility, and replacement.

## Admission requirements

Every direct dependency or external tool must have a registry entry in the
owning workspace documentation or manifest that records:

- its bounded purpose and owning port or adapter;
- project URL, source registry, version, license, and lock/checksum evidence;
- runtime, build-time, test-only, or optional classification;
- network, filesystem, process, native-code, and credential capabilities;
- maintained alternatives and a concrete replacement strategy;
- fixtures or contract tests that permit replacement;
- the approving issue or decision record.

A dependency is not admitted solely because a reference website, template, or
sibling repository uses it.

## Pinning and locks

- Commit `Cargo.lock` for the CLI/workspace and the pnpm lockfile for JavaScript
  tools and reference surfaces.
- Pin direct build tools, subprocess adapters, container images, GitHub Actions,
  schemas, fonts, and browser binaries to immutable versions or digests.
- Reusable library manifests may publish compatible semantic-version ranges,
  but release and CI evidence must resolve through committed lockfiles.
- Vendor normative schemas and offline resources by version and checksum.
- Never discover fonts, schemas, converters, or renderers from the network
  during validation, planning, rendering, verification, or packaging.
- Record tool, target, and font checksums in reproducibility evidence; do not
  embed wall-clock timestamps or absolute machine paths in generated assets.

## License and provenance review

Before admission or upgrade:

1. identify the package and all distributed transitive licenses;
2. confirm compatibility with the repository's MIT license and intended binary,
   package, container, and public-asset distribution;
3. preserve copyright notices and source obligations;
4. review font-specific embedding, modification, subsetting, attribution, and
   Reserved Font Name terms independently of code licensing;
5. reject unknown, untraceable, non-redistributable, or unapproved inputs.

Permissive licenses such as MIT, Apache-2.0, BSD, and ISC are normally eligible.
Weak-copyleft test dependencies such as MPL-2.0 require documented distribution
handling. GPL, AGPL, SSPL, source-available, commercial-only, or ambiguous terms
require an explicit architecture and legal/licensing decision; they are not
silently admitted.

## Security and supply chain

- Minimize features and disable default network/TLS features when the adapter is
  offline by contract.
- Run the ecosystem's lockfile-aware vulnerability and license checks in CI;
  publish machine-readable evidence through Relay when that integration exists.
- Generate an SBOM and license inventory for releases that distribute binaries,
  containers, packages, fonts, or bundled JavaScript.
- Prefer memory-safe in-process Rust libraries over shell-outs. When a subprocess
  is justified, pass an argument vector rather than a shell string, isolate its
  filesystem, set resource limits, and capture its exact version.
- Treat SVG, font, archive, image, JSON, and YAML inputs as untrusted. Enforce
  size/depth limits, reject external resource loading, and fuzz parsers at the
  core trust boundaries.
- GitHub Actions use immutable commit SHAs. Container images use digests.

## Update cadence

- Automation may propose grouped monthly maintenance updates after #8 establishes
  manifests and tests.
- Security fixes are triaged promptly according to exploitability, reachability,
  and distribution exposure; urgent fixes do not wait for the monthly group.
- Major versions, renderer/encoder changes, schema validators, font tooling,
  browser engines, and token transformers require an explicit compatibility PR.
- Every update runs offline tests, contract fixtures, golden artifacts, license
  review, vulnerability review, and clean-room builds before promotion.
- Baseline changes must show human-reviewable diffs. Updating a golden file is
  not evidence that the new result is correct.

## Replacement protocol

An adapter may be replaced when the candidate:

1. consumes the same normalized application input;
2. emits the same versioned output contract or an explicit migration;
3. passes the shared fixture and diagnostic suite;
4. meets or improves licensing, security, accessibility, performance, size, and
   cross-platform gates;
5. demonstrates rollback to the previous adapter and lock.

Canonical `.identity/` source must not be rewritten merely to accommodate a
replacement projection library.

## Exceptions

Exceptions are time-bounded decision records. They name the owner, risk,
affected distributions, compensating controls, expiry condition, and removal
issue. An exception cannot weaken human approval, provenance, license, privacy,
offline-core, or publication authority boundaries.

