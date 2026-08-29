# Example Product design-system handbook

This is a deterministic projection of validated, reviewed local Identity source.

Source: https://example.invalid/example-product

Source digest: `1002ff75ea51f6e016929894ea30cc96565bdbbca749a0e7fff1ebd0d2f21353`

## Inheritance

- Organization layers: example-organization
- Product layer: `example-product`

### Reviewed overrides

- `color.brand.primary` — Give the product a distinct violet technical accent. (approval: `approve-product-primary`)

## Enabled output profiles

- `core@1.0.0`
- `metadata@1.0.0`
- `tokens@1.0.0`

## Design principles

### Accessible expression

Brand character reinforces meaning without becoming the only way users can understand or operate a surface.

#### Make meaning survive styling changes

Pair visual distinction, motion, and mascot expression with readable content and supported accessibility alternatives.

Why: A recognizable system remains useful when motion is reduced, colors vary, or imagery is unavailable.

Applies to: product, repository

### Reviewed foundations

Use semantic tokens and reviewed guidance as the shared starting point for every product surface.

#### Start with semantic intent

Choose tokens by the role they serve before choosing a visual treatment.

Why: Semantic intent keeps product overrides reviewable and preserves accessibility across themes.

Applies to: organization, product, repository

## Resolved source facts

### accessibility

Status: **declared**

Rationale: Identity expression must preserve perceivable content, readable text, operable controls, and understandable status without relying on brand styling alone.

```json
{
  "governance": {
    "approval": "approve-usage-core",
    "provenance": {
      "capturedAt": "2026-08-21T12:15:00Z",
      "method": "human-authored",
      "source": ".identity/brief.md"
    },
    "state": "approved",
    "subject": "usage:core-guidance",
    "visibility": "public"
  },
  "rules": [
    "Use reviewed contrast pairings",
    "Provide contextual alternative text",
    "Honor reduced motion",
    "Never encode state by color alone"
  ],
  "summary": "Identity expression must preserve perceivable content, readable text, operable controls, and understandable status without relying on brand styling alone."
}
```

### asset:mark

Status: **declared**

Rationale: Approved for current product, documentation, and repository use.

```json
{
  "availability": "public",
  "downloadName": "example-product-mark.svg",
  "governance": {
    "approval": "approve-primary-mark",
    "provenance": {
      "capturedAt": "2026-08-21T12:00:00Z",
      "method": "human-authored",
      "source": ".identity/governance/provenance.json#mark"
    },
    "state": "approved",
    "subject": "mark",
    "visibility": "public"
  },
  "id": "mark",
  "kind": "mark",
  "label": "Primary mark",
  "notes": "Approved for current product, documentation, and repository use.",
  "path": ".identity/sources/mark.svg",
  "replacement": null,
  "status": "active"
}
```

### legal

Status: **declared**

Rationale: Preserve attribution from the governed provenance record when distributing an asset.

```json
{
  "attribution": "Preserve attribution from the governed provenance record when distributing an asset.",
  "copyright": "Copyright 2026 Example. Source assets retain their recorded copyright and license terms.",
  "governance": {
    "approval": "approve-usage-core",
    "provenance": {
      "capturedAt": "2026-08-21T12:15:00Z",
      "method": "human-authored",
      "source": ".identity/governance/provenance.json"
    },
    "state": "approved",
    "subject": "usage:core-guidance",
    "visibility": "public"
  },
  "thirdPartyLicenses": [
    {
      "attribution": "Copyright 2026 Example",
      "name": "Example Product fixture assets",
      "spdx": "MIT"
    }
  ],
  "trademark": "Example Product names and marks may be used only to identify the project without implying endorsement."
}
```

### profile:core

Status: **declared**

Rationale: Enabled versioned output profile selected by the reviewed project source.

```json
{
  "id": "core",
  "version": "1.0.0"
}
```

### profile:metadata

Status: **declared**

Rationale: Enabled versioned output profile selected by the reviewed project source.

```json
{
  "id": "metadata",
  "version": "1.0.0"
}
```

### profile:tokens

Status: **declared**

Rationale: Enabled versioned output profile selected by the reviewed project source.

```json
{
  "id": "tokens",
  "version": "1.0.0"
}
```

### token:color.action.primary

Status: **declared**

Rationale: Resolved from the reviewed semantic token source.

```json
{
  "approval": null,
  "constraints": {},
  "overrideReason": null,
  "path": "color.action.primary",
  "sourceLayer": "example-product",
  "type": "color",
  "value": {
    "alpha": 1,
    "colorSpace": "srgb",
    "components": [
      0.42,
      0.2,
      0.72
    ]
  }
}
```

### token:color.brand.primary

Status: **declared**

Rationale: Resolved from the reviewed semantic token source.

```json
{
  "approval": "approve-product-primary",
  "constraints": {
    "contrast": {
      "intent": "decorative",
      "minimumRatio": 1,
      "pairedWith": []
    },
    "override": {
      "approval": "approve-product-primary",
      "reason": "Give the product a distinct violet technical accent."
    }
  },
  "overrideReason": "Give the product a distinct violet technical accent.",
  "path": "color.brand.primary",
  "sourceLayer": "example-product",
  "type": "color",
  "value": {
    "alpha": 1,
    "colorSpace": "srgb",
    "components": [
      0.42,
      0.2,
      0.72
    ]
  }
}
```

### token:color.canvas

Status: **declared**

Rationale: Resolved from the reviewed semantic token source.

```json
{
  "approval": null,
  "constraints": {
    "contrast": {
      "intent": "background",
      "minimumRatio": 7,
      "pairedWith": [
        "color.text"
      ]
    }
  },
  "overrideReason": null,
  "path": "color.canvas",
  "sourceLayer": "example-organization",
  "type": "color",
  "value": {
    "alpha": 1,
    "colorSpace": "srgb",
    "components": [
      0.98,
      0.98,
      1
    ]
  }
}
```

### token:color.text

Status: **declared**

Rationale: Resolved from the reviewed semantic token source.

```json
{
  "approval": null,
  "constraints": {
    "contrast": {
      "intent": "foreground",
      "minimumRatio": 7,
      "pairedWith": [
        "color.canvas"
      ]
    }
  },
  "overrideReason": null,
  "path": "color.text",
  "sourceLayer": "example-organization",
  "type": "color",
  "value": {
    "alpha": 1,
    "colorSpace": "srgb",
    "components": [
      0.05,
      0.06,
      0.1
    ]
  }
}
```

### token:motion.duration.reduced

Status: **declared**

Rationale: Resolved from the reviewed semantic token source.

```json
{
  "approval": null,
  "constraints": {},
  "overrideReason": null,
  "path": "motion.duration.reduced",
  "sourceLayer": "example-organization",
  "type": "duration",
  "value": {
    "unit": "ms",
    "value": 0
  }
}
```

### token:motion.duration.standard

Status: **declared**

Rationale: Resolved from the reviewed semantic token source.

```json
{
  "approval": null,
  "constraints": {
    "motion": {
      "reducedMotion": "motion.duration.reduced"
    }
  },
  "overrideReason": null,
  "path": "motion.duration.standard",
  "sourceLayer": "example-organization",
  "type": "duration",
  "value": {
    "unit": "ms",
    "value": 180
  }
}
```

### token:typography.body.family

Status: **declared**

Rationale: Resolved from the reviewed semantic token source.

```json
{
  "approval": null,
  "constraints": {
    "typography": {
      "languages": [
        "en"
      ],
      "legibility": "Prefer open counters and a minimum 16px body size.",
      "license": "OFL-1.1"
    }
  },
  "overrideReason": null,
  "path": "typography.body.family",
  "sourceLayer": "example-organization",
  "type": "fontFamily",
  "value": [
    "Inter",
    "system-ui",
    "sans-serif"
  ]
}
```

### usage:illustration-purpose

Status: **declared**

Rationale: Illustration should clarify a concept or add deliberate warmth.

```json
{
  "category": "illustration",
  "contexts": [
    "documentation",
    "marketing"
  ],
  "details": [
    "Prefer one clear focal idea",
    "Keep visual metaphors culturally reviewable"
  ],
  "governance": {
    "approval": "approve-usage-core",
    "provenance": {
      "capturedAt": "2026-08-21T12:15:00Z",
      "method": "human-authored",
      "source": ".identity/brief.md"
    },
    "state": "approved",
    "subject": "usage:core-guidance",
    "visibility": "public"
  },
  "id": "illustration-purpose",
  "instruction": "Do not add illustration solely to fill space or obscure an incomplete explanation.",
  "kind": "dont",
  "rationale": "Illustration should clarify a concept or add deliberate warmth."
}
```

### usage:imagery-provenance

Status: **declared**

Rationale: Visual polish never replaces lawful, accessible use.

```json
{
  "category": "imagery",
  "contexts": [
    "documentation",
    "social-card"
  ],
  "details": [
    "Record creator and source",
    "Avoid decorative alt text that repeats nearby copy"
  ],
  "governance": {
    "approval": "approve-usage-core",
    "provenance": {
      "capturedAt": "2026-08-21T12:15:00Z",
      "method": "human-authored",
      "source": ".identity/brief.md"
    },
    "state": "approved",
    "subject": "usage:core-guidance",
    "visibility": "public"
  },
  "id": "imagery-provenance",
  "instruction": "Use imagery with approved licensing, source provenance, and context-specific alternative text.",
  "kind": "do",
  "rationale": "Visual polish never replaces lawful, accessible use."
}
```

### usage:localization-review

Status: **declared**

Rationale: Literal translation can alter tone, meaning, or trademark use.

```json
{
  "category": "localization",
  "contexts": [
    "all"
  ],
  "details": [
    "Expose coverage status",
    "Never label machine translation as reviewed"
  ],
  "governance": {
    "approval": "approve-usage-core",
    "provenance": {
      "capturedAt": "2026-08-21T12:15:00Z",
      "method": "human-authored",
      "source": ".identity/guidance/voice.json#localization"
    },
    "state": "approved",
    "subject": "usage:core-guidance",
    "visibility": "public"
  },
  "id": "localization-review",
  "instruction": "Keep approved product names stable and request human review for uncovered language contexts.",
  "kind": "do",
  "rationale": "Literal translation can alter tone, meaning, or trademark use."
}
```

### usage:mark-clear-space

Status: **declared**

Rationale: Clear space and contrast preserve recognition at small sizes.

```json
{
  "category": "mark",
  "contexts": [
    "repository-readme",
    "product-ui",
    "social-card"
  ],
  "details": [
    "Minimum standalone size: 16 CSS pixels",
    "Preferred backgrounds: surface canvas or brand primary"
  ],
  "governance": {
    "approval": "approve-usage-core",
    "provenance": {
      "capturedAt": "2026-08-21T12:15:00Z",
      "method": "human-authored",
      "source": ".identity/governance/provenance.json#mark"
    },
    "state": "approved",
    "subject": "usage:core-guidance",
    "visibility": "public"
  },
  "id": "mark-clear-space",
  "instruction": "Keep one quarter of the mark width clear on every side and use an approved high-contrast background.",
  "kind": "do",
  "rationale": "Clear space and contrast preserve recognition at small sizes."
}
```

### usage:mark-transformations

Status: **declared**

Rationale: Unreviewed transformations fragment the identity and can reduce legibility.

```json
{
  "category": "mark",
  "contexts": [
    "all"
  ],
  "details": [
    "Do not add shadows",
    "Do not place the mark over busy imagery"
  ],
  "governance": {
    "approval": "approve-usage-core",
    "provenance": {
      "capturedAt": "2026-08-21T12:15:00Z",
      "method": "human-authored",
      "source": ".identity/governance/provenance.json#mark"
    },
    "state": "approved",
    "subject": "usage:core-guidance",
    "visibility": "public"
  },
  "id": "mark-transformations",
  "instruction": "Do not stretch, rotate, crop, outline, or recolor the mark outside approved semantic tokens.",
  "kind": "dont",
  "rationale": "Unreviewed transformations fragment the identity and can reduce legibility."
}
```

### usage:mascot-behavior

Status: **declared**

Rationale: Personality can reinforce understanding but must not gate it.

```json
{
  "category": "mascot",
  "contexts": [
    "product-ui",
    "documentation"
  ],
  "details": [
    "Pair expression with text",
    "Avoid emotional reactions that blame the user"
  ],
  "governance": {
    "approval": "approve-usage-core",
    "provenance": {
      "capturedAt": "2026-08-21T12:15:00Z",
      "method": "human-authored",
      "source": ".identity/brief.md"
    },
    "state": "approved",
    "subject": "usage:core-guidance",
    "visibility": "public"
  },
  "id": "mascot-behavior",
  "instruction": "Use the mascot as a supportive guide, never as the sole carrier of warnings or required instructions.",
  "kind": "do",
  "rationale": "Personality can reinforce understanding but must not gate it."
}
```

### usage:readable-type

Status: **declared**

Rationale: A brand typeface is not usable where its license, glyphs, or reading size fail.

```json
{
  "category": "typography",
  "contexts": [
    "product-ui",
    "documentation"
  ],
  "details": [
    "Preserve fallback order",
    "Test long translated labels before release"
  ],
  "governance": {
    "approval": "approve-usage-core",
    "provenance": {
      "capturedAt": "2026-08-21T12:15:00Z",
      "method": "human-authored",
      "source": ".identity/defaults/organization.tokens.json"
    },
    "state": "approved",
    "subject": "usage:core-guidance",
    "visibility": "public"
  },
  "id": "readable-type",
  "instruction": "Use the licensed family, supported language coverage, and documented legibility constraints.",
  "kind": "do",
  "rationale": "A brand typeface is not usable where its license, glyphs, or reading size fail."
}
```

### usage:reduced-motion

Status: **declared**

Rationale: Motion is expressive only when users can safely reduce it.

```json
{
  "category": "motion",
  "contexts": [
    "product-ui",
    "brand-kit-renderer"
  ],
  "details": [
    "Honor prefers-reduced-motion",
    "Keep state changes understandable without animation"
  ],
  "governance": {
    "approval": "approve-usage-core",
    "provenance": {
      "capturedAt": "2026-08-21T12:15:00Z",
      "method": "human-authored",
      "source": ".identity/defaults/organization.tokens.json"
    },
    "state": "approved",
    "subject": "usage:core-guidance",
    "visibility": "public"
  },
  "id": "reduced-motion",
  "instruction": "Pair every branded transition with its declared reduced-motion alternative.",
  "kind": "do",
  "rationale": "Motion is expressive only when users can safely reduce it."
}
```

### usage:semantic-color

Status: **declared**

Rationale: Semantic pairs preserve meaning and measurable readability across themes.

```json
{
  "category": "color",
  "contexts": [
    "product-ui",
    "documentation",
    "social-card"
  ],
  "details": [
    "Meet the declared minimum ratio",
    "Do not infer contrast from hue names"
  ],
  "governance": {
    "approval": "approve-usage-core",
    "provenance": {
      "capturedAt": "2026-08-21T12:15:00Z",
      "method": "human-authored",
      "source": ".identity/defaults/organization.tokens.json"
    },
    "state": "approved",
    "subject": "usage:core-guidance",
    "visibility": "public"
  },
  "id": "semantic-color",
  "instruction": "Choose semantic foreground and background pairs with their declared contrast intent.",
  "kind": "do",
  "rationale": "Semantic pairs preserve meaning and measurable readability across themes."
}
```

### voice:characteristic:clear

Status: **declared**

Rationale: Lead with the useful outcome and make recovery paths concrete.

```json
{
  "description": "Lead with the useful outcome and make recovery paths concrete.",
  "governance": {
    "approval": "approve-voice-core",
    "provenance": {
      "capturedAt": "2026-08-21T12:10:00Z",
      "method": "human-authored",
      "source": ".identity/brief.md"
    },
    "state": "approved",
    "subject": "voice:core-guidance",
    "visibility": "public"
  },
  "id": "clear",
  "label": "Clear"
}
```

### voice:characteristic:considerate

Status: **declared**

Rationale: Treat constraints and mistakes as shared design problems, never personal failures.

```json
{
  "description": "Treat constraints and mistakes as shared design problems, never personal failures.",
  "governance": {
    "approval": "approve-voice-core",
    "provenance": {
      "capturedAt": "2026-08-21T12:10:00Z",
      "method": "human-authored",
      "source": ".identity/brief.md"
    },
    "state": "approved",
    "subject": "voice:core-guidance",
    "visibility": "public"
  },
  "id": "considerate",
  "label": "Considerate"
}
```

### voice:characteristic:grounded

Status: **declared**

Rationale: Prefer evidence and precise limits over hype or vague certainty.

```json
{
  "description": "Prefer evidence and precise limits over hype or vague certainty.",
  "governance": {
    "approval": "approve-voice-core",
    "provenance": {
      "capturedAt": "2026-08-21T12:10:00Z",
      "method": "human-authored",
      "source": ".identity/brief.md"
    },
    "state": "approved",
    "subject": "voice:core-guidance",
    "visibility": "public"
  },
  "id": "grounded",
  "label": "Grounded"
}
```

### voice:foundation

Status: **declared**

Rationale: A transparent, local-first system for turning reviewed intent into reusable identity guidance.

```json
{
  "audience": [
    "repository maintainers",
    "product contributors",
    "downstream integrators"
  ],
  "governance": {
    "approval": "approve-voice-core",
    "provenance": {
      "capturedAt": "2026-08-21T12:10:00Z",
      "method": "human-authored",
      "source": ".identity/brief.md"
    },
    "state": "approved",
    "subject": "voice:core-guidance",
    "visibility": "public"
  },
  "personality": [
    "clear",
    "considerate",
    "grounded",
    "quietly playful"
  ],
  "positioning": "A transparent, local-first system for turning reviewed intent into reusable identity guidance.",
  "purpose": "Help maintainers make governed brand choices with confidence."
}
```

### voice:incident-update

Status: **declared**

Rationale: State impact, known facts, next update, and recovery without deflection.

```json
{
  "avoidedLanguage": [
    "minor issue",
    "user error",
    "obviously",
    "soon"
  ],
  "context": "incident-update",
  "preferredVocabulary": [
    "impact",
    "confirmed",
    "investigating",
    "next update",
    "recovery"
  ],
  "tone": "Calm, direct, accountable, and time-specific."
}
```

### voice:localization

Status: **declared**

Rationale: Keep product names unchanged and request human review when a locale is not covered.

```json
{
  "fallback": "Keep product names unchanged and request human review when a locale is not covered.",
  "governance": {
    "approval": "approve-voice-core",
    "provenance": {
      "capturedAt": "2026-08-21T12:10:00Z",
      "method": "human-authored",
      "source": ".identity/brief.md"
    },
    "state": "approved",
    "subject": "voice:core-guidance",
    "visibility": "public"
  },
  "sourceLanguage": "en-US",
  "supportedLanguages": [
    {
      "coverage": "reviewed",
      "notes": "Canonical source guidance.",
      "tag": "en-US"
    },
    {
      "coverage": "partial",
      "notes": "Product naming is reviewed; full messaging review remains required.",
      "tag": "es"
    }
  ]
}
```

### voice:repository-readme

Status: **declared**

Rationale: Orient quickly, establish trust, and make the next action obvious.

```json
{
  "avoidedLanguage": [
    "magic",
    "revolutionary",
    "effortless",
    "guaranteed"
  ],
  "context": "repository-readme",
  "preferredVocabulary": [
    "reviewed",
    "local",
    "deterministic",
    "evidence",
    "recovery"
  ],
  "tone": "Concise, capable, welcoming, and specific."
}
```

## Capability boundaries

| Capability | Owner | State | Notes |
| --- | --- | --- | --- |
| Product layout implementation | consumer | not-declared | Each product owns layout decisions while consuming approved identity constraints and bounded overrides. |
| Reusable application components | holon | not-declared | Identity records component-facing constraints but does not define or distribute component implementations. |
| Semantic token guidance | identity | declared | Identity owns the reviewed DTCG token source, inheritance evidence, and generated platform projections. |

## Reviewed external references

### greptile-design

Source: https://www.greptile.com/design

Captured: `2026-08-22T10:05:00Z`

Decision: **adapt**

Patterns:

- Concise public guidance that combines visual assets, typography, color, and usage context.
- Clear presentation of downloadable approved assets without making a website the source of truth.

Notes: Study the information architecture only. Identity keeps its source, renderer, accessibility, and provenance contracts independent.

Rights: Do not copy, download, redistribute, or imply permission to use Greptile trademarks, assets, or proprietary copy.
