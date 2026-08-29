# Example Product Brand Kit

A complete, governed Identity v1 fixture.

Source: https://example.invalid/example-product

Audience: **review**

## Foundation

**Purpose:** Help maintainers make governed brand choices with confidence.

**Positioning:** A transparent, local-first system for turning reviewed intent into reusable identity guidance.

**Audience:** repository maintainers, product contributors, downstream integrators

**Personality:** clear, considerate, grounded, quietly playful

- State: **approved · public**
- Approval: `approve-voice-core`
- Provenance: `human-authored` from `.identity/brief.md` at `2026-08-21T12:10:00Z`

## Voice characteristics

### Clear

Lead with the useful outcome and make recovery paths concrete.

- State: **approved · public**
- Approval: `approve-voice-core`
- Provenance: `human-authored` from `.identity/brief.md` at `2026-08-21T12:10:00Z`

### Grounded

Prefer evidence and precise limits over hype or vague certainty.

- State: **approved · public**
- Approval: `approve-voice-core`
- Provenance: `human-authored` from `.identity/brief.md` at `2026-08-21T12:10:00Z`

### Considerate

Treat constraints and mistakes as shared design problems, never personal failures.

- State: **approved · public**
- Approval: `approve-voice-core`
- Provenance: `human-authored` from `.identity/brief.md` at `2026-08-21T12:10:00Z`

## Tone by context

### Repository README (`repository-readme`)

**Audience:** A contributor deciding whether and how to use the repository.

**Intent:** Orient quickly, establish trust, and make the next action obvious.

**Tone:** Concise, capable, welcoming, and specific.

**Preferred vocabulary:** reviewed, local, deterministic, evidence, recovery

**Avoided language:** magic, revolutionary, effortless, guaranteed

**Naming:** Use the complete product name on first mention and the approved short name afterward.

**Capitalization:** Use sentence case for headings and preserve registered product casing.

**Punctuation:** Prefer short declarative sentences; use exclamation points only for genuine celebration.

#### Examples

> Generate a reviewed Brand Kit locally, then inspect exactly what changed.
>
> It states the outcome, authority boundary, and recovery affordance without hype.

- State: **approved · public**
- Approval: `approve-voice-core`
- Provenance: `human-authored` from `.identity/brief.md` at `2026-08-21T12:10:00Z`

> Your brand system, ready when you are.
>
> A warmer option proposed through the creative handoff and awaiting review.

- State: **candidate · internal**
- Approval: `pending human review`
- Provenance: `handoff-candidate` from `handoff:voice-friendly-candidate/v1` at `2026-08-21T12:18:00Z`

> Branding solved forever.
>
> Retained as superseded migration history and excluded from current public copy.

- State: **superseded · internal**
- Approval: `supersede-old-tagline`
- Provenance: `imported` from `guidance:old-tagline/v0` at `2025-02-01T10:00:00Z`

#### Anti-examples

> A flexible solution for all your branding needs.
>
> It names neither a concrete outcome nor the system's review boundary.

- State: **approved · public**
- Approval: `approve-voice-core`
- Provenance: `human-authored` from `.identity/brief.md` at `2026-08-21T12:10:00Z`

> The world's most revolutionary brand generator.
>
> Unprovable superlatives undermine the grounded voice.

- State: **rejected · internal**
- Approval: `reject-hype-claim`
- Provenance: `handoff-candidate` from `handoff:voice-hype-claim/v1` at `2026-08-21T12:19:00Z`

### Incident update (`incident-update`)

**Audience:** A user affected by a service or release problem.

**Intent:** State impact, known facts, next update, and recovery without deflection.

**Tone:** Calm, direct, accountable, and time-specific.

**Preferred vocabulary:** impact, confirmed, investigating, next update, recovery

**Avoided language:** minor issue, user error, obviously, soon

**Naming:** Name the affected capability exactly as it appears in the product.

**Capitalization:** Use sentence case and avoid all-caps urgency.

**Punctuation:** Use periods and timestamps; avoid exclamation points and rhetorical questions.

#### Examples

> Exports are delayed. Existing Brand Kits remain available. The next update is at 15:00 UTC.
>
> It separates impact, continuity, and the next commitment.

- State: **approved · public**
- Approval: `approve-voice-core`
- Provenance: `human-authored` from `.identity/brief.md` at `2026-08-21T12:10:00Z`

#### Anti-examples

> A few users may notice a minor issue; everything should be fine soon.
>
> It minimizes impact and makes no verifiable commitment.

- State: **approved · public**
- Approval: `approve-voice-core`
- Provenance: `human-authored` from `.identity/brief.md` at `2026-08-21T12:10:00Z`

## Usage: do / don’t

### Marks and backgrounds

Keep approved marks legible, proportionate, and visually independent.

#### Do: Keep one quarter of the mark width clear on every side and use an approved high-contrast background.

Clear space and contrast preserve recognition at small sizes.

- Minimum standalone size: 16 CSS pixels
- Preferred backgrounds: surface canvas or brand primary
- Contexts: repository-readme, product-ui, social-card
- State: **approved · public**
- Approval: `approve-usage-core`
- Provenance: `human-authored` from `.identity/governance/provenance.json#mark` at `2026-08-21T12:15:00Z`

#### Don’t: Do not stretch, rotate, crop, outline, or recolor the mark outside approved semantic tokens.

Unreviewed transformations fragment the identity and can reduce legibility.

- Do not add shadows
- Do not place the mark over busy imagery
- Contexts: all
- State: **approved · public**
- Approval: `approve-usage-core`
- Provenance: `human-authored` from `.identity/governance/provenance.json#mark` at `2026-08-21T12:15:00Z`

### Color, typography, and motion

Use semantic intent, readable type, and respectful movement across surfaces.

#### Do: Choose semantic foreground and background pairs with their declared contrast intent.

Semantic pairs preserve meaning and measurable readability across themes.

- Meet the declared minimum ratio
- Do not infer contrast from hue names
- Contexts: product-ui, documentation, social-card
- State: **approved · public**
- Approval: `approve-usage-core`
- Provenance: `human-authored` from `.identity/defaults/organization.tokens.json` at `2026-08-21T12:15:00Z`

#### Do: Use the licensed family, supported language coverage, and documented legibility constraints.

A brand typeface is not usable where its license, glyphs, or reading size fail.

- Preserve fallback order
- Test long translated labels before release
- Contexts: product-ui, documentation
- State: **approved · public**
- Approval: `approve-usage-core`
- Provenance: `human-authored` from `.identity/defaults/organization.tokens.json` at `2026-08-21T12:15:00Z`

#### Do: Pair every branded transition with its declared reduced-motion alternative.

Motion is expressive only when users can safely reduce it.

- Honor prefers-reduced-motion
- Keep state changes understandable without animation
- Contexts: product-ui, brand-kit-renderer
- State: **approved · public**
- Approval: `approve-usage-core`
- Provenance: `human-authored` from `.identity/defaults/organization.tokens.json` at `2026-08-21T12:15:00Z`

### Imagery, illustration, and mascot

Make expressive assets purposeful, attributable, and secondary to meaning.

#### Do: Use imagery with approved licensing, source provenance, and context-specific alternative text.

Visual polish never replaces lawful, accessible use.

- Record creator and source
- Avoid decorative alt text that repeats nearby copy
- Contexts: documentation, social-card
- State: **approved · public**
- Approval: `approve-usage-core`
- Provenance: `human-authored` from `.identity/brief.md` at `2026-08-21T12:15:00Z`

#### Don’t: Do not add illustration solely to fill space or obscure an incomplete explanation.

Illustration should clarify a concept or add deliberate warmth.

- Prefer one clear focal idea
- Keep visual metaphors culturally reviewable
- Contexts: documentation, marketing
- State: **approved · public**
- Approval: `approve-usage-core`
- Provenance: `human-authored` from `.identity/brief.md` at `2026-08-21T12:15:00Z`

#### Do: Use the mascot as a supportive guide, never as the sole carrier of warnings or required instructions.

Personality can reinforce understanding but must not gate it.

- Pair expression with text
- Avoid emotional reactions that blame the user
- Contexts: product-ui, documentation
- State: **approved · public**
- Approval: `approve-usage-core`
- Provenance: `human-authored` from `.identity/brief.md` at `2026-08-21T12:15:00Z`

#### Do: Keep approved product names stable and request human review for uncovered language contexts.

Literal translation can alter tone, meaning, or trademark use.

- Expose coverage status
- Never label machine translation as reviewed
- Contexts: all
- State: **approved · public**
- Approval: `approve-usage-core`
- Provenance: `human-authored` from `.identity/guidance/voice.json#localization` at `2026-08-21T12:15:00Z`

## Downloads

- [Primary mark](.identity/sources/mark.svg) — `example-product-mark.svg`
  - Approved for current product, documentation, and repository use.
  - State: **approved · public**

## Legacy assets

### Legacy wordmark — LEGACY / INTERNAL

Retained for historical migrations only; do not use in new work.

Replacement: `mark`

- State: **superseded · internal**
- Approval: `supersede-legacy-wordmark`
- Provenance: `imported` from `.identity/governance/provenance.json#legacy-wordmark` at `2025-02-01T10:00:00Z`

## Accessibility

Identity expression must preserve perceivable content, readable text, operable controls, and understandable status without relying on brand styling alone.

- Use reviewed contrast pairings
- Provide contextual alternative text
- Honor reduced motion
- Never encode state by color alone

## Legal and attribution

- Trademark: Example Product names and marks may be used only to identify the project without implying endorsement.
- Copyright: Copyright 2026 Example. Source assets retain their recorded copyright and license terms.
- Attribution: Preserve attribution from the governed provenance record when distributing an asset.

## Decision ledger

| Decision | Subject | Candidate | Status | Reviewer | Evidence |
| --- | --- | --- | --- | --- | --- |
| `approve-design-system-foundations` | `design-system:foundations` | `.identity/guidance/design-system.json` | **approved** | example-maintainer | https://example.invalid/reviews/design-system-foundations |
| `approve-greptile-design-reference` | `reference:greptile-design` | `https://www.greptile.com/design` | **approved** | example-maintainer | https://example.invalid/reviews/greptile-design-reference |
| `approve-kern-mascot` | `mascot:kern` | `.identity/guidance/mascot.json` | **approved** | example-maintainer | https://example.invalid/reviews/mascot-kern |
| `approve-kern-mascot-asset` | `mascot-kern` | `.identity/sources/kern.svg` | **approved** | example-maintainer | https://example.invalid/reviews/mascot-kern-asset |
| `approve-legacy-wordmark-source` | `legacy-wordmark` | `.identity/sources/legacy-wordmark.svg` | **approved** | example-maintainer | https://example.invalid/reviews/legacy-wordmark-source |
| `approve-legacy-wordmark-usage` | `usage-asset:legacy-wordmark` | `asset:legacy-wordmark/v0` | **approved** | example-maintainer | https://example.invalid/reviews/legacy-wordmark-v0 |
| `approve-old-tagline` | `voice-example:old-tagline` | `guidance:old-tagline/v0` | **approved** | example-maintainer | https://example.invalid/reviews/old-tagline-v0 |
| `approve-primary-mark` | `mark` | `.identity/sources/mark.svg` | **approved** | example-maintainer | https://example.invalid/reviews/primary-mark |
| `approve-product-primary` | `token:color.brand.primary` | `token:color.brand.primary@product-override` | **approved** | example-maintainer | https://example.invalid/reviews/product-primary |
| `approve-usage-core` | `usage:core-guidance` | `guidance:usage-core/v1` | **approved** | example-maintainer | https://example.invalid/reviews/usage-core |
| `approve-voice-core` | `voice:core-guidance` | `guidance:voice-core/v1` | **approved** | example-maintainer | https://example.invalid/reviews/voice-core |
| `reject-hype-claim` | `voice-example:hype-claim` | `handoff:voice-hype-claim/v1` | **rejected** | example-maintainer | https://example.invalid/reviews/hype-claim |
| `supersede-legacy-wordmark` | `usage-asset:legacy-wordmark` | `asset:legacy-wordmark/v0` | **superseded** | example-maintainer | https://example.invalid/reviews/legacy-wordmark |
| `supersede-old-tagline` | `voice-example:old-tagline` | `guidance:old-tagline/v0` | **superseded** | example-maintainer | https://example.invalid/reviews/old-tagline |
