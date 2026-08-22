<p align="center">
  <img src="assets/identity/brand/banner-readme.svg" alt="identity — brand kit generator" width="100%" />
</p>

# Identity

🪪 Identity is an open-source Brand Kit generator that turns reviewed brand intent into reproducible design tokens, creative guidance, platform assets, distributable packages, and a public Brand Kit.

## Product contract

A consumer owns its identity source. Identity validates that source, plans deterministic projections, generates derived artifacts, verifies the result, and records evidence without replacing human creative authority.

```text
project-owned .identity/ intent
        ↓
Identity validate → resolve → plan → render → verify
        ↓
assets/identity/ + versioned packages + Brand Kit view model
        ↓
product consumers + public Brand Kit
```

The canonical Ego Hygiene Brand Kit will be published at `https://egohygiene.io/identity`. The descriptive `/brand-kit` route will redirect to the canonical `/identity` route.

## Brand Kit preview

The first human-approved self-hosting visual direction now lives under [`assets/identity/`](assets/identity/README.md). These are generated projections—not a replacement for the future canonical `.identity/` source contract.

<p align="center">
  <img src="assets/identity/guidelines/color-palette.svg" alt="identity color palette" width="92%" />
</p>

<p align="center">
  <a href="assets/identity/guidelines/design-system.svg">design system board</a> ·
  <a href="assets/identity/guidelines/usage-guidelines.svg">usage guidelines</a> ·
  <a href="assets/identity/manifest.json">asset manifest</a>
</p>

## The three product layers

| Layer | Responsibility | Primary outputs |
| --- | --- | --- |
| Compiler and contracts | Model, validate, resolve, plan, render, and verify reviewed identity intent | Diagnostics, plans, manifests, and evidence |
| Generated Brand Kit | Project the resolved identity into portable assets and packages | Tokens, marks, metadata, guidance, archives, and typed packages |
| Reference experience | Present and safely preview the generated Brand Kit | Public renderer, downloads, and approval-aware asset studio |

Frameworks, renderers, and providers remain replaceable adapters around these stable layers.

## CLI foundation

The independently buildable Rust CLI currently preserves four local-first
commands from the Empathy incubation:

```bash
cargo run -- init \
  --repository-root "path/to/consumer" \
  --project-id "consumer" \
  --display-name "Consumer"

cargo run -- validate --repository-root "path/to/consumer"

cargo run -- plan \
  --repository-root "path/to/consumer" \
  --format "markdown"

cargo run -- handoff \
  --repository-root "path/to/consumer" \
  --output-directory ".cache/identity/handoff"
```

`init` creates consumer-owned `.identity/` intent. `validate` checks the v0
project and profile contracts. `plan` resolves eight profiles and 45 targets
without generating them. `handoff` creates a deterministic, provenance-aware
creative source-pack request whose candidates remain unapproved by default.

Raster/vector rendering, asset application, packaging, and publication remain
outside this extracted CLI vertical slice. See the
[Empathy extraction evidence](docs/migration/EMPATHY_EXTRACTION.md).

## Identity v1 source

The v1 contract adds content-addressed organization defaults, intentional
product overrides, DTCG-compatible semantic tokens, versioned target profiles,
asset provenance/licensing, and human approvals beneath `.identity/`.

```bash
python3 scripts/validate_identity.py \
  --repository-root "tests/fixtures/v1/valid/minimal" \
  --format "human"

python3 scripts/plan_v0_migration.py \
  --repository-root "tests/fixtures/migration/empathy-v0" \
  --format "human"
```

Both tools are standard-library-only, offline, and non-mutating. The complete
[v1 contract](docs/contracts/IDENTITY_V1.md) documents topology, merge order,
aliases, compatibility, diagnostics, migration, and rollback.

## Compiler core

The Rust library exposes the deterministic framework-neutral compiler boundary
behind the Brand Kit generator:

```text
read → validate → resolve → plan → render → verify → manifest
                                      │
                                      └─ transactional apply after approval
```

The compiler provides mutation-free plans, adapter capability/compatibility
records, stable diagnostics, SHA-256 fingerprints and manifests, incremental
unchanged detection, pre-apply verification, and explicit recovery for
interrupted generated-state transactions. Network-dependent or nondeterministic
projection adapters are rejected from the compiler-owned path.

The [compiler v1 contract](docs/contracts/COMPILER_V1.md) documents the public
Rust ports plus `identity.compiler-plan/v1` and
`identity.compiler-manifest/v1`. Generation remains a library/application
boundary until a later CLI design explicitly exposes it; the existing four CLI
commands keep their extraction-parity contract.

## Brand Kit packages

The built-in package layer implements nine versioned output profiles over the
compiler ports: `core`, `web`, `pwa`, `github`, `docs`, `social`, `tokens`,
`metadata`, and `archive`.

Those profiles can deterministically project a resolved identity into:

- DTCG JSON, CSS custom properties, JavaScript, TypeScript declarations, and a
  Tailwind-compatible theme;
- document CSS, public metadata, Open Graph markup, PWA icon metadata, and
  explicit voice/usage guidance state;
- approved SVG marks plus PNG favicon, PWA, maskable, social-card, and GitHub
  preview assets through the offline `resvg` adapter boundary;
- package metadata, SHA-256 indexes/checksums, and a deterministic downloadable
  ZIP with fixed ordering and timestamps.

Consumers select profile IDs and compatible versions; selecting a subset does
not generate unrelated profiles. The compiler manifest remains the transaction
and evidence record for the exact selected build. The
[Brand Kit packages v1 contract](docs/contracts/BRAND_KIT_PACKAGES_V1.md)
defines the stable generated interface, compatibility rules, archive semantics,
and consumer boundary.

## State and authority

| State | Owner | Meaning |
| --- | --- | --- |
| Canonical | Consumer | Human-reviewed intent under `.identity/` |
| Generated | Identity | Reproducible outputs under `assets/identity/` and released packages |
| Transient | Active interface | Preview, cache, candidate, and work state that cannot silently become canonical |
| Published | Owning surface | An immutable approved release integrated and deployed by the website or consumer repository |

## What Identity owns

- brand contracts, schemas, inheritance, overrides, and compatibility;
- semantic design tokens, voice guidance, metadata, usage rules, and target profiles;
- deterministic asset planning, projection, validation, manifests, and provenance;
- distributable Brand Kit packages and a framework-neutral view model;
- the reference Brand Kit renderer and approval-aware asset studio contract.

## What Identity does not own

- product UI components and templates, which belong to Holon;
- organization policy, which belongs to Hygiene;
- shared agent instructions and architecture schemas, which belong to Aether;
- reusable CI/CD implementation, which belongs to Relay;
- consumer source intent or the website deployment shell;
- raw asset archives, generic logo generation, or silent publication of generated creative work.

## Current capability state

The Brand Kit product contract and toolchain decisions are accepted. The
extracted CLI, v1 source contract, and deterministic compiler core are
implemented. This change adds the concrete built-in projection adapters and
versioned distributable package layer; quality/governance and public-product
layers remain the next gates.

| Capability | State | Tracking |
| --- | --- | --- |
| Brand Kit product contract | Accepted | [#6](https://github.com/egohygiene/identity/issues/6) |
| Toolchain decisions | Accepted | [#7](https://github.com/egohygiene/identity/issues/7), [evaluation](docs/evaluations/brand-kit-foundations.md), [ADRs](DECISIONS.md) |
| Independent CLI | Implemented | [#8](https://github.com/egohygiene/identity/issues/8) |
| v1 identity schema | Implemented | [#9](https://github.com/egohygiene/identity/issues/9), [contract](docs/contracts/IDENTITY_V1.md) |
| Compiler core | Implemented | [#10](https://github.com/egohygiene/identity/issues/10), [contract](docs/contracts/COMPILER_V1.md) |
| Projection adapters and packages | Implemented in this change | [#11](https://github.com/egohygiene/identity/issues/11), [contract](docs/contracts/BRAND_KIT_PACKAGES_V1.md) |
| Quality and governance | Proposed | [#12](https://github.com/egohygiene/identity/issues/12), [#13](https://github.com/egohygiene/identity/issues/13) |
| Renderer and asset studio | Proposed | [#14](https://github.com/egohygiene/identity/issues/14), [#15](https://github.com/egohygiene/identity/issues/15) |
| Public `/identity` route | Deferred until its dependencies land | [#16](https://github.com/egohygiene/identity/issues/16) |
| Stable v1.0.0 release | Deferred until all v1 gates pass | [#18](https://github.com/egohygiene/identity/issues/18) |

The umbrella [#2](https://github.com/egohygiene/identity/issues/2) remains open
until the required Empathy and OptiFlow consumer proof lands through #17.

## Architecture

- [Purpose](PURPOSE.md)
- [Vision](VISION.md)
- [Principles](PRINCIPLES.md)
- [Pillars](PILLARS.md)
- [System responsibilities](SYSTEM.md)
- [Architecture and boundaries](ARCHITECTURE.md)
- [Design system contract](DESIGN_SYSTEM.md)
- [Architecture decisions](DECISIONS.md)
- [Brand Kit foundations evaluation](docs/evaluations/brand-kit-foundations.md)
- [Dependency policy](docs/DEPENDENCY_POLICY.md)
- [Identity v1 source contract](docs/contracts/IDENTITY_V1.md)
- [Compiler v1 contract](docs/contracts/COMPILER_V1.md)
- [Brand Kit packages v1 contract](docs/contracts/BRAND_KIT_PACKAGES_V1.md)
- [Roadmap](ROADMAP.md)

The [roadmap issue](https://github.com/egohygiene/identity/issues/5) is the execution source of truth. Architecture documents define durable intent and boundaries; individual issues own implementation detail and evidence.
