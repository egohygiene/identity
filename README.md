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

## The three product layers

| Layer | Responsibility | Primary outputs |
| --- | --- | --- |
| Compiler and contracts | Model, validate, resolve, plan, render, and verify reviewed identity intent | Diagnostics, plans, manifests, and evidence |
| Generated Brand Kit | Project the resolved identity into portable assets and packages | Tokens, marks, metadata, guidance, archives, and typed packages |
| Reference experience | Present and safely preview the generated Brand Kit | Public renderer, downloads, and approval-aware asset studio |

Frameworks, renderers, and providers remain replaceable adapters around these stable layers.

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

The Brand Kit product contract is accepted by this documentation. Runtime behavior remains proposed until its owning issue lands in this repository. The incubated CLI is observed in Empathy but is not yet an implemented capability of this repository.

| Capability | State | Tracking |
| --- | --- | --- |
| Brand Kit product contract | Accepted | [#6](https://github.com/egohygiene/identity/issues/6) |
| Toolchain decisions | Accepted | [#7](https://github.com/egohygiene/identity/issues/7), [evaluation](docs/evaluations/brand-kit-foundations.md), [ADRs](DECISIONS.md) |
| Independent CLI | Proposed | [#8](https://github.com/egohygiene/identity/issues/8) |
| v1 identity schema | Proposed | [#9](https://github.com/egohygiene/identity/issues/9) |
| Compiler and packages | Proposed | [#10](https://github.com/egohygiene/identity/issues/10), [#11](https://github.com/egohygiene/identity/issues/11) |
| Quality and governance | Proposed | [#12](https://github.com/egohygiene/identity/issues/12), [#13](https://github.com/egohygiene/identity/issues/13) |
| Renderer and asset studio | Proposed | [#14](https://github.com/egohygiene/identity/issues/14), [#15](https://github.com/egohygiene/identity/issues/15) |
| Public `/identity` route | Deferred until its dependencies land | [#16](https://github.com/egohygiene/identity/issues/16) |
| Stable v1.0.0 release | Deferred until all v1 gates pass | [#18](https://github.com/egohygiene/identity/issues/18) |

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
- [Roadmap](ROADMAP.md)

The [roadmap issue](https://github.com/egohygiene/identity/issues/5) is the execution source of truth. Architecture documents define durable intent and boundaries; individual issues own implementation detail and evidence.
