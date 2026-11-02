# Optional imagery and motion: existing capabilities

Inventory and bounded adoption guide for
[#107](https://github.com/egohygiene/identity/issues/107). Reuse the following
source and projection paths before adding a new category or engine.

The selected first category is Identity's existing approved **static Kern
mascot illustration**. The [complete local example](../../examples/visuals/kern-static/README.md)
traces the character source and approval through the existing Brand Kit asset
package to an offline static consumer. The [delivery record](../work/107/CLOSEOUT.md)
separates that proof from release, root-v1 adoption and browser qualification.

| Category | Existing source/implementation | What is still an owner choice |
| --- | --- | --- |
| Icons, favicons, avatars, marks and wordmarks | Native selected profiles, approved marks/renditions and [practical downloads](PRESENTATION_PROFILES.md) | Which approved master/composition and output profiles the project actually needs. |
| Illustrations, photography and patterns | Existing provenance `imagery`/`illustration` asset kinds, approved public usage records and selected Press Kit assets | Supply an actual image and rights; a pattern can use an existing asset kind and label rather than a new mandatory schema category. |
| Mascots | [Governed mascot source/package](../contracts/MASCOT_SYSTEM_V1.md), approved variants and alternative text | Character/creative approval and the exact adopted public variants; no new artwork is generated here. |
| Screenshots and captures | Existing `demo-capture` visual-motion evidence and replaceable capture producer boundary | The real capture purpose, synthetic/privacy-safe inputs, source rights and human visual review. A screenshot is not automatically a public brand asset. |
| Layout and visual usage conventions | Governed handbook, usage and reference-experience projections | Supplied usage guidance and the consumer's accessible layout. The renderer's private components are not a product UI library. |
| Animation and motion | [Visual-motion policy/evidence](../contracts/VISUAL_MOTION_V1.md), semantic motion tokens and creative-direction guidance | Purpose, baseline approval and actual reduced-motion fallback. No animation runtime is introduced. |

## Selected static mascot example

Identity already supplies [Kern's character source](../../mascot/kern.character.json),
[prior approval](../../mascot/approval.json), [provenance](../../mascot/provenance.json)
and a [three-variant package](../../assets/identity/mascot/manifest.json).
The source checkout's Brand Kit asset tree contains the exact full, portrait
and icon PNGs plus its usage guide. No missing category implementation is
needed for this selected use case.

The [offline consumer](../../examples/visuals/kern-static/index.html) uses the
existing portrait at 160 CSS pixels, its exact reviewed alternative text,
visible descriptive text, required CC BY 4.0 attribution and the source's
trademark boundary. It links all three approved variants and original guidance.
It uses the existing dedicated mascot contract; v1 source/producer capability
limits and root self-adoption remain independent work.

Static artwork is the selected motion scope. The same approved PNG is already
the reduced-motion presentation; no animation, transition, autoplay or script
is introduced. Other visual categories remain available through their existing
contracts when a project actually selects them. The example adds no mandatory
source field, placeholder gallery or new artwork.

The existing `verify_mascot.py` command passed for all three RGBA variants and
their source/approval/manifest bindings. All eleven consumed files remain
unchanged. The actual stable `v1.0.0` source predates Kern: including this source
package in a new published release remains #98. Local availability does not
change that immutable release or establish deployment.

## One bounded optional illustration path

For a project that actually selects a supporting illustration, use an existing
approved image rather than creating artwork or an approval in this task:

1. Keep the exact source bytes beneath that consumer's `.identity/` asset
   boundary. Record its existing provenance kind, digest, license/origin and
   real review evidence using the [authoring worksheet](AUTHORING.md).
2. Adopt its approved public usage record, including alternative text,
   attribution, restrictions and minimum-size/safe-zone guidance. A provenance
   entry alone does not authorize public use.
3. Explicitly select that existing asset through the adopted Press Kit source.
   Candidate/internal/unselected assets remain absent. Do not add new category
   requirements to the minimal source.
4. Generate the existing governed Press Kit and pass it to the
   [complete kit](COMPLETE_BRAND_KIT.md). The kit's existing source-digest and
   selected-file checks bind that projection to the native output. The public
   kit exposes only the selected public download and supplied rights.
5. Optionally select the same public Press Kit ID for an
   [announcement draft](LAUNCH_DOCUMENTS.md). That optional tool
   retains exact image bytes, alternative text, license and restrictions.
   It does not animate the illustration or approve new release claims.

With no adopted illustration selection, no placeholder gallery, fabricated
rights, new artwork or mandatory imagery inventory is added. Ordinary native
generation and a minimal kit remain useful.

## Accessibility and reduced motion

Static imagery needs meaningful supplied alternative text, with relevant text
or data available without the image. Do not communicate state through color,
imagery or animation alone. The existing renderer keeps keyboard navigation,
static essential content and its reduced-motion CSS behavior.

For actual motion, use the existing purpose/budget/quality contract. Landing,
continuous-status and demo-capture assets need their real digest-bound fallback;
a prose instruction is not a rendered reduced-motion artifact. Captures must
retain privacy-safe/synthetic context and immutable producer inputs. Automation
does not supply semantic or creative approval.

## Review status

This delivery inventories all requested categories and demonstrates the
selected real static mascot source-to-kit-to-consumer path with the existing
package verifier. Other photographs, patterns, captures or animation needs
remain unselected possibilities. Broader source/renderer/browser/accessibility,
reduced-motion and visual-regression suites remain deferred under #70/#80;
the local package result does not claim those checks passed. Existing #98
retains actual release and root self-source/rights/dogfood acceptance.

ADR not required: this guide references existing accepted projection, rights
and mascot boundaries (ADRs 0001, 0003, 0011, 0015 and 0021). It changes no
source field, policy, existing asset bytes or human disposition.
