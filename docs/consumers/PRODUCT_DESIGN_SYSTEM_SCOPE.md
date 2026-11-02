# Identity specification and future component scope

Maintainer-selected scope for [#109](https://github.com/egohygiene/identity/issues/109),
2026-11-02: Identity specifies and validates a project's comprehensive identity,
including its naming, copy, visual foundations, assets, rights, provenance and
usage guidance under the adopted contracts. Validation and generation tooling
support that specification; the Brand Kit is a consumer-facing presentation.

Existing foundations and reference behavior suffice for this checkpoint.
Components remain a possible future capability, including a future Identity
component scope if justified. This decision introduces no component library,
new requirement or permanent prohibition. [ADR-0031](../decisions/ADR-0031-product-component-ownership.md)
retains the original proposal and a dated scope clarification; its formal
lifecycle remains proposed.

## Concrete needs and current support

| Need | Current implementation | Ownership and compatibility |
| --- | --- | --- |
| Brand colors, typography, spacing and reduced-motion choices | Versioned v1 tokens and the governed handbook/context projections | Identity owns the source and existing token/projection contracts. Consumers pin a compatible Identity version. |
| Copy/download buttons, section navigation and responsive kit layout | `renderer/src/app.js`, `client.js` and `styles.css` | Private reference-experience implementation, not an exported component API. |
| Forms and interaction patterns for reviewing candidate assets | Existing renderer studio and the approved studio-review handoff | Review controls remain separate from public kits and do not approve canonical source. |
| Real product buttons, validation, data-entry forms and application navigation | No concrete shared consumer requirement is identified by #109 | The product owner selects accessible components and behavior; Identity can supply brand tokens. |
| Reusable repository/site starting points | Existing Holon profiles consumed through an explicit immutable selection | Holon owns scaffolding. A template is not an Identity component package or a silent fleet rollout. |

## Selected current scope

Keep Identity's shipped foundations and reference experience. Do not create a
new universal component library for this checkpoint. Existing button or studio
markup is not evidence that downstream products need the same interactions.
The renderer's private package and source paths carry no general React,
framework or product-component compatibility promise.

A consumer can use the approved token package with its selected accessible UI
implementation. Bind its package version independently; keep application state,
form validation, navigation semantics and interaction tests in that consumer.
Do not add component source, engineering policy or mutable sibling-repository
imports to `.identity/` to make this work.

## A future request needs

- A named consumer and demonstrated interaction gap, including keyboard,
  focus, validation/error and reduced-motion behavior.
- An accountable component owner, supported framework/platform and versioned
  public API; Hygiene resolves cross-repository ownership if it is unclear.
- A tested mapping to a selected Identity token version, with fallback,
  upgrade and rollback boundaries.
- A separate bounded issue. Do not broaden renderer cleanup #88 into a
  component-system project or create speculative implementation issues now.

The maintainer selected the current specification/validation focus and
authorized closing #109 with future components left open. No concrete shared
interaction gap or component implementation is selected, so no speculative
implementation follow-up is created. Revisit ownership and compatibility when
an actual component need is scoped. This disposition supplies no new runtime,
release or deployment evidence.
