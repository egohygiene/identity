# Identity owner answers and asset review — 2026-11-22

Status: **brand choices captured; exact source/governance and baseline review in preparation**.
The maintainer supplied these answers in chat and asked the assistant to capture
them in the repository. [Issue #98](https://github.com/egohygiene/identity/issues/98)
contains the durable capture. The assistant recorded the answers; no public
chat-transcript URL was supplied. Brand choices do not approve a release,
deployment or ADR lifecycle transition.

## Selected masters and origin

The maintainer confirmed that the existing emblem and horizontal logo look
good, selecting both as the canonical-master candidates:

| Subject | Existing source | Selected SHA256 |
| --- | --- | --- |
| `mark` | `assets/identity/brand/emblem.svg` | `20e5cd2edaac53f81343ec5c8e6557ab049339e0c907d9641a822eab7554d97c` |
| `horizontal-lockup` | `assets/identity/brand/lockup-horizontal.svg` | `5cece16fe478fdd42a1a91f47546db3fe860ec7af07682e68397977a28e41eed` |

Both files remain unchanged from inspected main
`afc368003bfc6a2101051229efd237c8d6fadf71`.

Owner-reported origin: ChatGPT created the artwork under the maintainer's
guidance. Open-source brand kits were consulted mainly for dimensions and
comprehensiveness. Exact kit names, reference URLs, generation records,
model/version and creation date were not supplied. This does not establish
that particular third-party artwork was copied or licensed; retain the unknown
details rather than inventing source history.

## Selected logo-use policy and credit

The maintainer selected the proposed scoped policy: display or bundle the logo
to represent Identity, including icon-font use; do not imply endorsement or use
it as another product's brand; a genuinely distinct derivative may use a
different name. They selected the practical credit **Ego Hygiene — Identity**.

The [draft logo-use wording](../../../assets/identity/brand/LOGO_USE.md) translates
that selection into scoped reference, integration, glyph-adaptation and
redistribution permissions. It does not select CC-BY for the logos, assert
registered trademark rights, guarantee a receiving font project's acceptance,
or relicense code, third-party material or Kern. Software MIT and Kern's
separately governed CC-BY-4.0 package retain their existing scope.

The exact policy and same-subject v1 governance records still need integration
and verification. The associated ADR remains proposed; the chat answer selected
brand terms, not an ADR lifecycle transition.

## Selected public copy and design direction

| Choice | Owner-selected value |
| --- | --- |
| Name | `identity` (lowercase) |
| Tagline | `project identity specification` |
| Short description | Identity specifies and validates a project's identity, then turns reviewed source into reproducible design tokens, creative guidance, assets and a Brand Kit. |
| Longer description | The selected short description followed by: Each project owns its `.identity/` source and creative approvals. |
| Voice | Clear, precise, present. |
| Principles | Clarity in form. Alignment in purpose. Essence in everything. |
| Reviewer | `szmyty`, explicitly confirmed for the exact two masters and selected brand choices. |
| Palette | Retain existing purple/blue/dark palette and current publication roles. Do not invent a new role for the existing gold swatch. |
| Typography | Retain Inter with `system-ui` and `sans-serif` fallbacks. No font files are redistributed by this choice. |
| Defaults | Prepare an explicitly Identity-local token baseline **for review** until an approved organization-default source is identified. This is not organization policy or approval of unreviewed token bytes. |
| Mascot | Retain Kern as the existing optional, separately governed package. |

The owner confirmed the longer description, voice/principles and reviewer in
the follow-up answers. Draft alt text, minimum-use and other usage records
remain review candidates. The existing selected masters and
legacy derived artwork are not silently rewritten to contain the new tagline;
review and regenerate the applicable derived outputs against the actual source.

## Avatar inspection

`avatar-square.svg` draws a dark `#0a0a0e` rounded tile (`rx="86"`) within its
512×512 viewBox. It has no white background outside that tile: the rounded
outside corners are transparent. The checkerboard/white visible in GitHub is
the transparency preview. The maintainer's acceptance was conditional on those
corners being transparent; inspection confirms that condition. Avatar bytes
are unchanged by this checkpoint.

## README raster repair

The maintainer reported a visibly glitched `banner-readme.webp`. Independent
Pillow decoding reproduces the stored visual defect. FFmpeg reports no decode
error, so its original cause is unproven; it is not just GitHub preview.

The existing `banner-hires.webp` is intact at **1500×500**. This checkpoint copies
those exact bytes to `banner-readme.webp`; it does not generate new artwork,
recompress, enlarge or alter the selected masters. The current manifest records
both raster geometries accurately and binds the replacement README blob.

- Replacement bytes: 12,898.
- SHA256: `48b5c8f91538362856f21dfca16b274bbf2dddad23a228905a8d95074f32c60f`.
- Git blob: `8256dbbc83a6e632f5e391635e580904b37af8b7`.
- Previous glitched README blob: `ddf31f1b0489d242fcba7b8d5fd8c5864cf2661b`,
  preserved in Git history and dated source inventories.

README/publication still select the separate 1536×512 SVG. Historical
`source-inventory.json` and publication rollback bindings retain their original
bytes. This repair retains the intact raster's existing wording; the selected
tagline requires a separate reviewed derivative update.

The current publication descriptor also mislabeled the selected horizontal
lockup as 1536×512 viewBox units. Its actual unchanged SVG is 1200×400; this
checkpoint corrects that descriptive metadata without altering the artwork.

## Coverage and remaining work

The inventory includes mark/avatar/lockup/banner/social/Open Graph, favicon and
Apple/PWA-related assets. Presence does not prove a complete generated kit.
Choose actual profiles and verify their full output inventories, dimensions,
background/alpha behavior, byte budgets, provenance, rights and source binding.

- If repository-presentation is selected, its light/dark/high-contrast banner
  sizes and SVG/PNG outputs need their real package proof; one legacy banner
  does not satisfy that profile.
- If PWA is selected, verify its full declared raster/maskable icon set rather
  than treating a 192px PNG and SVG variants as equivalent evidence.
- Additional monochrome, standalone wordmark, ICO and platform-specific social
  variants are conditional on a real selected surface, not universal new work.
- Retain Kern's independent rights/approval package and the current native
  producer's PNG capability limit; do not invent a supported mapping.

The [questionnaire](QUESTIONNAIRE.md) and [owner packet](OWNER_PACKET.md) retain
exact source/governance, baseline review, qualification, release,
publication/rollback and contrasting-consumer acceptance. This intake and
raster repair do not complete those gates.
