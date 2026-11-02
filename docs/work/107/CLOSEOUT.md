# Issue #107 static mascot delivery — 2026-11-02

Reviewed Identity base: `349b3de76bfbec5483bbb7d5de3489abe93b9fa0`.
Scope: [#107](https://github.com/egohygiene/identity/issues/107), with broader
testing/CI and release work deferred by the maintainer.

## Selected actual consumer and category

Reuse Identity's existing approved **static Kern mascot illustration**. The
canonical character, approval, provenance, rights and three exact derivatives
already exist. No category extension, new art, crop, source approval, runtime
animation engine or model is needed. The
[reference consumer](../../../examples/visuals/kern-static/README.md) renders
the reviewed portrait and links the existing packaged files directly.

This is the existing dedicated mascot contract/package, not newly authored
root `.identity/` source. Native v1 producer capability limits and root v1
self-adoption/rights remain independent #98 work. The example does not force
PNG material through the SVG-only native source bridge.

## Acceptance coverage

| Issue criterion | Delivered result |
| --- | --- |
| Inventory all requested categories | The [inventory](../../consumers/OPTIONAL_VISUALS.md) records existing icons/marks, illustrations/photos/patterns, mascots, screenshots/capture, layout and motion owners/contracts. |
| Extend only a demonstrated missing category | The selected static mascot category is already implemented, so no category/schema extension is required. Unselected categories remain optional. |
| Approved source, usage, attribution and rights | Existing Kern character/provenance/approval and package manifests bind the actual master and variants. Required CC BY 4.0 attribution, original usage and trademark boundaries are retained. |
| Accessible alternatives and reduced motion | The static page uses exact reviewed alt text, visible descriptive text, meaningful native links and the portrait's reviewed minimum width. It introduces no script or motion; the approved static image is the reduced-motion presentation. |
| Demonstrate an agreed optional source-to-kit category | Under the maintainer's direction to execute #107, the selected real Identity/Kern use case traces canonical source and prior approval to the three-variant Brand Kit asset package and offline consumer. Existing package verification passed. |
| Clean omission and preserved authoritative sources | Examples are opt-in; no mandatory field, default gallery or generation behavior changes. Existing minimal/expanded v1 source, visual/token source, artwork, rights, approvals and package bytes remain unchanged. |

## Actual bounded evidence

```bash
python3 scripts/verify_mascot.py --repository-root .
```

This existing product verifier exited 0 and reported
`character=kern, variants=3, transparency=rgba`. It checks the canonical
source/approval/provenance bindings, package source and guidance hashes,
variant inventory, exact bytes, sizes, dimensions and real RGBA transparency.
The full variant remains the exact approved master. All eleven consumed files
are unchanged. [The bounded record](static-mascot.json) retains their hashes,
variant metadata, source revision and the static example hash.

HTML/source inspection checks the exact portrait alt text and 160 CSS-pixel
display size, required attribution, local download/source links and absence of
scripts/animation. This is not a browser/axe, assistive-technology, contrast,
visual-regression or whole-repository conformance result. Those remain under
#70/#80 with the existing broader sweep.

## Release and follow-up boundary

GitHub's actual annotated `v1.0.0` tag object is
`9540ad6076ccc34b6dbbafc0e2fc72ee6ad4d02f`, targeting
`aaad8839104704cf57bfa846539b3b875421e03d`. Inspection of that exact release
tree found no `mascot/` or `assets/identity/mascot/` files. The current source
package is therefore a local source-checkout demonstration, not proof that
Kern is already in that published release. No tag, release, site or deployment
was created or changed. Existing #98 already owns a new reviewed stable release
and real source/rights/dogfood evidence; no duplicate release issue is needed.

New captures remain conditionally owned by Relay #8 when actually selected.
Other photos, patterns, illustrations and motion profiles remain possibilities
requiring real supplied source and review. No unrequested follow-up is created.
The deferred initializer is already #133; quality/refactoring retains #70.

## Decision impact

ADR not required: apply existing accepted mascot/projection/accessibility
boundaries (ADRs 0011, 0015 and 0021) to unchanged approved material. No new
contract, rights, dependency, policy or human disposition is introduced, and
all ADR sources/lifecycles remain unchanged.
