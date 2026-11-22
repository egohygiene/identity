# Renderer extraction acceptance checkpoint — 2026-11-22

The merged extraction remains stable at source
`ec8fce30c3c96c7781238eb0a8899d6f0cee0a40`. All 235 focused tests pass,
all 24 extracted function bodies match their recorded hashes, and 16
reference-fixture markup comparisons are byte-identical. No demonstrated
renderer boundary defect requires another refactor or runtime change.

**Issue #88 remains open.** Its retained #80/current-source matching-workflow
browser/CI prerequisite is not supplied by these source and unit checks.
The [machine-readable receipt](acceptance-2026-11-22.json) records the actual
scope, hashes, commands' outcomes and limitations. Historical local browser
proof stays in the [original extraction handoff](../116/RENDERER_EXTRACTION.md);
it is not relabeled as a new workflow result.

## Acceptance mapping

| Issue #88 boundary | Current-source evidence | Remaining limit |
| --- | --- | --- |
| Bounded private extraction and generated-model compatibility | All 24 function bodies equal integration base `12c8877b9b74ab02e883a74ec9349afe52eaadd0` and their existing extraction SHA-256 values. Input validation/selection derivation is verbatim, with the recorded `f7d5ebb...` hash. | No new public interface, schema or runtime dependency is introduced. |
| Exact renderer output | Original and current `BrandKitPage` produce identical markup for the reference model: preview/public, four deployment bases, publication absent/present (16 combinations). Template, client, styles, immutable-model module and screenshot baseline also remain byte-identical to the integration base. | This finite fixture matrix does not prove every possible model or browser rendering. |
| Public/review isolation | Four guidance integration cases exercise the current public Python projection and actual static renderer, including shared mixed-lifecycle records; withheld content is absent from both HTML and embedded model JSON. Existing UI tests retain the declared/absent guidance distinction. | `publicOnly` selects public sections; it does not replace the producer's governed public projection or sanitize an arbitrary review model. |
| Source/release and download binding | Download-integrity tests verify actual fixture bytes, checksums/sizes, source digest, project, selected renderer JSON, release tag and archive/manifest/checksum inventory. Negative cases reject altered models and mismatched or missing evidence. | Fixture integrity checks do not qualify a real new release or authenticate a publisher. |
| Confined paths, routing and download links | Path and integration cases reject traversal, encoded separators, external artifacts, invalid deployment bases and escaping symlinks. Local, parent-relative, rooted and HTTP(S) bases retain selected links; an HTTP fixture returns unchanged artifact bytes. Failed preflight preserves the existing page. | No network fetch is performed by the local artifact verifier; the integration HTTP server is disposable test infrastructure. |
| Static accessibility and metadata | Existing tests retain heading/section hierarchy, navigation, copy status, declared rights and missing-rights states; static axe and CSS policy checks pass. | Static axe disables color-contrast. Actual keyboard, visual and complete WCAG/manual acceptance require their separate browser/human evidence. |
| Unit/integration plus qualified browser/CI acceptance | Nine selected files: 235 passed, zero failed/skipped/todo; source parse checks: 51 JavaScript files passed. | Matching current-source qualified browser/workflow evidence remains the retained #80 gate. Criterion 3 is not closed by this checkpoint. |

## Commands and comparison method

Use the repository's exact pnpm 11.21.0 with Node 24.19.0. The frozen install
reused 88 packages and downloaded none; package and lockfile bytes are unchanged.
From `renderer/`:

```sh
pnpm install --frozen-lockfile
pnpm exec vitest run tests/app.test.js tests/model.test.js tests/artifact-paths.test.js tests/artifact-paths.integration.test.js tests/downloads.test.js tests/download-integrity.test.js tests/rights.test.js tests/guidance.integration.test.js tests/public-site.test.js --reporter=json --outputFile=/tmp/identity-88-focused-vitest-20261122.json
```

From the repository root, `node renderer/scripts/check-source.mjs` checked
51 JavaScript files. The first Vitest invocation encountered host `ENOSPC`
while creating its temporary config directory, before running any tests.
After shared regenerable-cache cleanup, the recorded nine-file rerun passed.
That startup failure was environmental and did not motivate a source change.

For extraction comparison, read the original app with
`git show 12c8877b9b74ab02e883a74ec9349afe52eaadd0:renderer/src/app.js`.
Compare each named function in the existing
[24-function extraction record](../116/renderer-extraction.json) to its current
component declaration, removing only its added `export ` prefix and retaining
one terminating newline for the recorded hash. Compare the original derivation
from `assertBrandKitViewModel(model)` through `sections`, before `const visible`,
to the corresponding block before `resolvePageInputs` returns its values.
All bodies, hashes and the derivation match.

For exact markup comparison, import the original app from an in-memory data URL,
resolving its imports to the current unchanged dependencies; compare its
`renderToStaticMarkup` result with the current app for the receipt's 16 prop
combinations. The supplied reference model is unchanged. The receipt retains
every resulting byte length and SHA-256. This compares markup without writing
generated HTML, updating a snapshot or installing a browser.

## Handoff and decision impact

Retain issue #88 until #80 supplies the required matching-current-source
workflow qualification, then reconcile the full unit/integration and browser
results on the final combined source. The broader suite and browser checkpoint
are coordinated separately; their future outcomes are not assumed here.

ADR not required: this checkpoint records verification of an already-merged
private extraction and preserves every public contract. Existing
[ADR-0011](../../decisions/ADR-0011-accessibility-and-visual-evidence.md) governs
the distinct exact, browser and human evidence layers. The pinned Aether
`create-decisions-document` 2.1.0 and continuity 1.1.0 skills were read from
Git objects at `dc8a16851f452763ef4f7fbe4bf057d4500b1921`; no host skill
installation or ADR lifecycle change is claimed.
