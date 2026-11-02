# Optional imagery and motion: existing capabilities

Inventory and bounded adoption guide for
[#107](https://github.com/egohygiene/identity/issues/107). Reuse the following
source and projection paths before adding a new category or engine.

| Category | Existing source/implementation | What is still an owner choice |
| --- | --- | --- |
| Icons, favicons, avatars, marks and wordmarks | Native selected profiles, approved marks/renditions and [practical downloads](PRESENTATION_PROFILES.md) | Which approved master/composition and output profiles the project actually needs. |
| Illustrations, photography and patterns | Existing provenance `imagery`/`illustration` asset kinds, approved public usage records and selected Press Kit assets | Supply an actual image and rights; a pattern can use an existing asset kind and label rather than a new mandatory schema category. |
| Mascots | [Governed mascot source/package](../contracts/MASCOT_SYSTEM_V1.md), approved variants and alternative text | Character/creative approval and the exact adopted public variants; no new artwork is generated here. |
| Screenshots and captures | Existing `demo-capture` visual-motion evidence and replaceable capture producer boundary | The real capture purpose, synthetic/privacy-safe inputs, source rights and human visual review. A screenshot is not automatically a public brand asset. |
| Layout and visual usage conventions | Governed handbook, usage and reference-experience projections | Supplied usage guidance and the consumer's accessible layout. The renderer's private components are not a product UI library. |
| Animation and motion | [Visual-motion policy/evidence](../contracts/VISUAL_MOTION_V1.md), semantic motion tokens and creative-direction guidance | Purpose, baseline approval and actual reduced-motion fallback. No animation runtime is introduced. |

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
   [announcement draft](LAUNCH_DOCUMENTS.md). That proposed optional tool
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

This checkpoint inventories implemented surfaces and the existing optional
source-to-kit route; it claims no new runtime proof. No actual new illustration,
photograph, pattern, mascot or motion use case was selected by the owner during
this sprint. Review the inventory and select a concrete consumer/category or
explicitly approve the current scope before closing #107. New category code,
artwork and an animation engine remain unstarted. Broader source, renderer,
accessibility and visual tests are deferred to the agreed sweep.

ADR not required: this guide references existing accepted projection, rights
and mascot boundaries (ADRs 0001, 0003, 0011, 0015 and 0021). It changes no
source field, policy, output bytes or human disposition.
