# Reference renderer dependency registry

This registry satisfies the admission requirements in
[`docs/DEPENDENCY_POLICY.md`](../docs/DEPENDENCY_POLICY.md). Exact resolved
versions and integrity hashes are committed in `pnpm-lock.yaml`.

| Dependency | Version | License | Scope | Bounded purpose | Capabilities | Replacement evidence |
| --- | ---: | --- | --- | --- | --- | --- |
| React | 19.2.8 | MIT | Runtime, distributed | Declarative rendering and hydration of the framework-neutral view model | DOM rendering only; no network or credentials | Static fixture, semantic DOM, and screenshot tests can be run against another adapter |
| React DOM | 19.2.8 | MIT | Runtime, distributed | Server rendering and browser hydration | DOM and HTML serialization | Same renderer contract and browser acceptance suite |
| Vite | 8.2.0 | MIT | Build-time | Static bundle and route-relative asset build | Build filesystem and local preview server | Any static bundler that preserves the output and test contracts |
| Vitest | 4.1.10 | MIT | Test-only | Deterministic component and contract tests | Local process and JSDOM test execution | Node test runner using the same fixtures |
| jsdom | 30.0.1 | MIT | Test-only | Static DOM inspection | In-memory DOM only | Browser-only contract tests |
| Playwright Test | 1.62.1 | Apache-2.0 | Test-only | Browser accessibility, interaction, responsive, download, and visual evidence | Local Chromium process and loopback server; no credentials | Any pinned browser runner that preserves screenshots and interactions |
| axe-core | 4.11.0 | MPL-2.0 | Test-only, not distributed | Automated accessibility rule evaluation | In-memory page inspection | Pa11y, Accessibility Insights automation, or equivalent reviewed rules |

## Distribution handling

Only React, React DOM, and Identity-owned source are bundled into the static
public output. Vite, Vitest, jsdom, Playwright, and axe-core remain development
or CI dependencies and are not redistributed with the Brand Kit bundle.
The MPL-2.0 axe-core package is therefore test-only; its source and license stay
available through the locked package graph rather than being embedded in public
artifacts.

## Network and filesystem boundary

Dependency installation and the pinned Chromium download are CI/setup
operations. Rendering, unit tests, static builds after installation, and public
runtime behavior do not contact external services. The renderer reads one local
view-model file and the generated `assets/identity/` tree.
