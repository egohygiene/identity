# Mascot and character system v1

## Outcome and authority

`identity.mascot-source/v1` makes a reviewed mascot reusable without turning
an image-generation prompt, a web page, or a generated crop into canonical
brand intent. A consumer opts in with `documents.mascot`; the referenced local
document owns the character's name, role, visual invariants, meanings,
accessibility, usage, motion limits, license, canonical asset, and human
approval.

The trust boundary is:

```text
reviewed character source + governed canonical asset + approvals
                              ↓
                   deterministic projections
                              ↓
      full / portrait / icon assets + package manifest + Brand Kit
```

The mascot is additive. Consumers without `documents.mascot` remain valid.
Candidates remain under the existing candidate boundary and cannot become an
approved mascot merely by appearing in a generated package.

## Kern reference character

Kern is Identity's first dogfooded character system. He is a calm, hooded
guide whose form reinforces the product contract:

| Element | Meaning | Invariant |
| --- | --- | --- |
| Three warm-white eyes | Observe context, reflect intent, verify projection | Exactly three; featureless; no pupils or irises |
| Chest identity kernel | Governed identity is carried as part of the system | Integrated into the garment; never detached or orbiting |
| Open hands | Guidance without replacing human authority | Retain in the approved full, portrait, and icon crops |
| Charcoal, violet, blue, and gold robe | Identity's approved visual direction | No unreviewed recoloring or copied third-party visual language |

Floating props, orbit rings, particle trails, extra facial features, and
detached emblems are explicitly prohibited. The complete reviewed source is
[`mascot/kern.character.json`](../../mascot/kern.character.json).

## Variant contract

The canonical asset is content-addressed. A variant declares its role, crop,
aspect ratio, minimum width, and alt text before a packaged file can claim that
role. `identity.mascot-package/v1` then binds each public derivative to exact
bytes, dimensions, media type, size, license, and source digest.

Kern provides three reviewed projections:

| Variant | Dimensions | Minimum width | Intended use |
| --- | ---: | ---: | --- |
| Full | 768 × 1152 | 320 CSS px | Hero art and spacious editorial layouts |
| Portrait | 512 × 512 | 160 CSS px | Cards, callouts, and profile introductions |
| Icon | 256 × 256 | 96 CSS px | Compact avatars and small square surfaces |

Below 320 pixels, use the supplied portrait or icon instead of shrinking or
recropping the full figure. The compact crop deliberately preserves all three
eyes, both hands, and the chest kernel.

## Accessibility and meaning

Kern is never the sole carrier of a heading, label, status, instruction,
navigation target, or approval state. Use the variant's reviewed alt text when
the character adds information. Use an empty alt attribute when the same
information is already adjacent and Kern is decorative.

Do not encode success, failure, risk, or lifecycle state only through eye glow,
pose, color, or motion. Text and semantic UI state remain authoritative.

## Motion

The v1 character is static by default. A later reviewed motion profile may add
a gentle eye glow or subtle breathing-scale shift. Reduced-motion presentation
always uses the static approved bytes. Orbiting objects, particles, detached
emblems, rapid flashes, and perpetual rotation are prohibited even in motion
derivatives.

## Provenance, rights, and approval

The canonical asset must already exist under the consumer's approved source
directory and resolve to one `identity.provenance/v1` record with matching path
and SHA-256. That provenance record owns the artwork license, origin,
accessibility description, restrictions, and its asset-level approval. The
mascot source separately links the human decision approving the complete
character system for `mascot:<id>`.

Identity's Kern artwork and approved derivatives use `CC-BY-4.0`; the required
attribution and trademark boundary are recorded in
[`mascot/LICENSE.md`](../../mascot/LICENSE.md). The source-generation and
technical transparency/crop record is preserved in
[`mascot/generation-record.md`](../../mascot/generation-record.md).

## Public Brand Kit and `/identity` handoff

The public Brand Kit packager already includes every reviewed file under
`assets/identity/`, including the offline mascot usage guide, package manifest,
and three PNG variants. The renderer treats PNGs as immutable downloadable
assets rather than trying to embed binary bytes as text. Publication reads its
asset configuration from the selected release source, so a default-branch
config can never claim a mascot that is absent from the pinned stable release.

The future Zensical and LaunchKit `/identity` experience tracked by issues #56
and #57 consumes these files and semantics. It may compose Kern into a page,
but it does not rename him, reinterpret the three eyes, detach the chest kernel,
or become a second source of usage truth.

## Validation and rollback

```bash
python3 scripts/validate_identity.py \
  --repository-root "path/to/consumer" \
  --format "human"

python3 scripts/verify_mascot.py \
  --repository-root "."
```

`IDN2001` covers character structure and semantic invariants. `IDN2002` covers
character approval. `IDN2003` covers canonical asset, provenance, digest, and
license relationships. Identity's self-hosting verifier additionally parses
PNG chunks with the Python standard library and requires real RGBA transparency
with both transparent and opaque pixels.

Rollback restores the previous approved source, provenance, approval, package
manifest, and exact derivative bytes together. Never roll back only the image
while leaving a mismatched digest or a newer character declaration in place.
