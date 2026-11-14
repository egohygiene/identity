# Renderer component extraction — #88

Integration base: `12c8877b9b74ab02e883a74ec9349afe52eaadd0`.
The current source campaign implements the existing renderer cleanup against
the [qualified local profile](../../evidence/browser-local-2026-11-14/README.md).
#80 retains its separate current-source CI acceptance for the later `act` pass.

Twenty-four existing view functions move unchanged into seven private modules
under `renderer/src/components/`: shared presentation helpers, guidance/rights,
design-system, Press Kit, assets, foundations and downloads/provenance. The
immutable-model validation, path normalization and public/optional section
selection move verbatim into `page-input.js`. The exported `BrandKitPage`
interface, CSS, event hooks, models and browser assertions remain unchanged.
`app.js` shrinks from 1478 to 290 lines. This creates no general component
library or new source/rendering contract.

[renderer-extraction.json](renderer-extraction.json) records all twenty-four
exact function hashes and the original input-derivation hash. Every moved
function matches after extraction. Before/after reference HTML is byte-for-byte
identical.

## Validation checkpoints

- All 424 renderer unit/integration cases pass. The first run exposed a public
  site fixture that omitted `renderer/lib`, newly required by merged PR139;
  the fixture now copies the full runtime dependency directory. Its original
  rights/archive assertions are unchanged.
- Source parsing, canonical-helper CLI/renderer builds and real legacy public
  site build/verification pass. Public/review, release/path binding, optional
  outputs, download integrity and static accessibility regressions remain
  covered. Source, rights, approvals and the approved PNG are unchanged.
- The integrated Python suite completes 188 cases: 186 pass and two existing
  skips. The current helper setup and checksum-pinned Task preparation pass.
- The [fresh local Docker receipt](../../evidence/browser-local-2026-11-14/renderer-65807c6/host-qualification.json) passes at clean source
  `65807c6d65238f280fd748cede6f4a6e48275bb5`: all nine positive cases,
  required deliberate screenshot failure and restored pass; no skips/retries.
  All raw proof hashes match after retention. The approved PNG is unchanged.
  Issue88 retains its issue80/current-source CI prerequisite for the later act phase.

The browser Dockerfile combines its font/package installation into one layer
and keeps its working directory at the renderer. This reduces observed local
vfs temporary storage while preserving the same base image, exact fonts,
package pins, secret-only CA mount and offline browser runtime.

ADR not required for private behavior-preserving views. Browser qualification
references egohygiene/identity#ADR-0011; no baseline or ADR approval is supplied.
