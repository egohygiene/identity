# Example Product design context

Schema: `identity.design-context/v1`

Source digest: `1002ff75ea51f6e016929894ea30cc96565bdbbca749a0e7fff1ebd0d2f21353`

Projection version: `1.0.0`

## Applies to

- Organization layers: example-organization
- Product layer: `example-product`
- Voice contexts: `incident-update`, `repository-readme`

## Enabled output profiles

- `core@1.0.0`
- `metadata@1.0.0`
- `tokens@1.0.0`

## Capability boundaries

| Capability | Owner | State | Notes |
| --- | --- | --- | --- |
| `product-layout` | consumer | not-declared | Each product owns layout decisions while consuming approved identity constraints and bounded overrides. |
| `reusable-components` | holon | not-declared | Identity records component-facing constraints but does not define or distribute component implementations. |
| `semantic-tokens` | identity | declared | Identity owns the reviewed DTCG token source, inheritance evidence, and generated platform projections. |

## Tokens

| Path | Type | Value | Source layer | Override |
| --- | --- | --- | --- |
| `color.action.primary` | color | `{"alpha": 1, "colorSpace": "srgb", "components": [0.42, 0.2, 0.72]}` | `example-product` | — |
| `color.brand.primary` | color | `{"alpha": 1, "colorSpace": "srgb", "components": [0.42, 0.2, 0.72]}` | `example-product` | Give the product a distinct violet technical accent. |
| `color.canvas` | color | `{"alpha": 1, "colorSpace": "srgb", "components": [0.98, 0.98, 1]}` | `example-organization` | — |
| `color.text` | color | `{"alpha": 1, "colorSpace": "srgb", "components": [0.05, 0.06, 0.1]}` | `example-organization` | — |
| `motion.duration.reduced` | duration | `{"unit": "ms", "value": 0}` | `example-organization` | — |
| `motion.duration.standard` | duration | `{"unit": "ms", "value": 180}` | `example-organization` | — |
| `typography.body.family` | fontFamily | `["Inter", "system-ui", "sans-serif"]` | `example-organization` | — |

## Voice

### incident-update

Tone: Calm, direct, accountable, and time-specific.

Prefer: impact, confirmed, investigating, next update, recovery

Avoid: minor issue, user error, obviously, soon

### repository-readme

Tone: Concise, capable, welcoming, and specific.

Prefer: reviewed, local, deterministic, evidence, recovery

Avoid: magic, revolutionary, effortless, guaranteed

## Usage

- **dont — illustration** (`illustration-purpose`): Do not add illustration solely to fill space or obscure an incomplete explanation.
  Why: Illustration should clarify a concept or add deliberate warmth.
  Contexts: `documentation`, `marketing`
- **do — imagery** (`imagery-provenance`): Use imagery with approved licensing, source provenance, and context-specific alternative text.
  Why: Visual polish never replaces lawful, accessible use.
  Contexts: `documentation`, `social-card`
- **do — localization** (`localization-review`): Keep approved product names stable and request human review for uncovered language contexts.
  Why: Literal translation can alter tone, meaning, or trademark use.
  Contexts: `all`
- **do — mark** (`mark-clear-space`): Keep one quarter of the mark width clear on every side and use an approved high-contrast background.
  Why: Clear space and contrast preserve recognition at small sizes.
  Contexts: `repository-readme`, `product-ui`, `social-card`
- **dont — mark** (`mark-transformations`): Do not stretch, rotate, crop, outline, or recolor the mark outside approved semantic tokens.
  Why: Unreviewed transformations fragment the identity and can reduce legibility.
  Contexts: `all`
- **do — mascot** (`mascot-behavior`): Use the mascot as a supportive guide, never as the sole carrier of warnings or required instructions.
  Why: Personality can reinforce understanding but must not gate it.
  Contexts: `product-ui`, `documentation`
- **do — typography** (`readable-type`): Use the licensed family, supported language coverage, and documented legibility constraints.
  Why: A brand typeface is not usable where its license, glyphs, or reading size fail.
  Contexts: `product-ui`, `documentation`
- **do — motion** (`reduced-motion`): Pair every branded transition with its declared reduced-motion alternative.
  Why: Motion is expressive only when users can safely reduce it.
  Contexts: `product-ui`, `brand-kit-renderer`
- **do — color** (`semantic-color`): Choose semantic foreground and background pairs with their declared contrast intent.
  Why: Semantic pairs preserve meaning and measurable readability across themes.
  Contexts: `product-ui`, `documentation`, `social-card`
