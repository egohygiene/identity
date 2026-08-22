# Astryx motion-pattern evaluation

## Decision status

This evaluation supports Identity issue #3. It records what Identity adopts,
adapts, and rejects from Astryx without making Astryx a runtime dependency or a
second source of truth for the Ego Hygiene design system.

Evaluation date: 2026-08-22

Pinned upstream revision used for implementation research:
`facebook/astryx@f1d403475708d58a0a17bff063350101f6abf7c8`

## Upstream sources reviewed

- Astryx repository: https://github.com/facebook/astryx
- Motion foundation documentation:
  https://github.com/facebook/astryx/blob/f1d403475708d58a0a17bff063350101f6abf7c8/packages/cli/assets/docs/motion.doc.mjs
- Motion-scale expansion:
  https://github.com/facebook/astryx/blob/f1d403475708d58a0a17bff063350101f6abf7c8/packages/core/src/theme/expandMotionScale.ts
- Entry-animation behavior:
  https://github.com/facebook/astryx/blob/f1d403475708d58a0a17bff063350101f6abf7c8/packages/core/src/hooks/useEntryAnimation.ts
- Container reveal/reduced-motion behavior:
  https://github.com/facebook/astryx/blob/f1d403475708d58a0a17bff063350101f6abf7c8/packages/core/src/hooks/containerReveal.stylex.ts
- Design conventions:
  https://github.com/facebook/astryx/wiki/Design-Conventions
- License:
  https://github.com/facebook/astryx/blob/main/LICENSE

## License decision

Astryx is distributed under the MIT License, copyright Meta Platforms, Inc.
Identity may legally study, adapt, and reuse compatible ideas or code under the
license terms. This issue intentionally **does not copy Astryx component source
or StyleX implementation**. We adopt design-system concepts and encode them in
Identity-owned framework-neutral contracts.

If future work copies a substantial portion of Astryx source, the required MIT
copyright and permission notice must accompany that copied material. Nothing in
this evaluation transfers Astryx trademarks or visual identity into Ego Hygiene.

## Adopt / adapt / reject matrix

| Astryx pattern | Decision | Identity interpretation |
| --- | --- | --- |
| Motion exists to clarify state/change rather than perform | **Adopt** | Every declared motion asset records a purpose; decorative movement without a product reason is rejected or requires an explicit human exception. |
| Tokenized duration bands | **Adopt concept** | Identity owns semantic bands for micro-interaction, transition, landing sequence, continuous status, and demo capture. Astryx numeric defaults are research input, not canonical Identity tokens. |
| Fast micro-interactions and medium entrances/exits | **Adapt** | Default release budgets are ≤200 ms for micro-interactions and ≤500 ms for UI transitions. Longer landing/demo media uses separate bounded classes instead of stretching UI tokens. |
| Standard decelerating easing | **Adopt** | Identity accepts standard/ease-out decelerating curves and rejects bounce/elastic easing by default. |
| Prefer `transform` and `opacity` over layout-property animation | **Adopt** | UI-motion manifests may declare only `transform` and `opacity` unless a versioned exception is reviewed. Width/height/margin/top/left and similar layout-driven motion fail closed. |
| `prefers-reduced-motion` collapses movement to an instant state | **Adopt** | Interactive motion must define an instant or static fallback. Pre-rendered landing/demo assets require a static or paired reduced-motion artifact. |
| Reduced motion preserves intent timing when timing is not itself movement | **Adapt** | Hover dwell or deliberate state delay may remain when semantically necessary, but visual movement must still collapse. |
| Do not animate initial static page content by default | **Adapt** | Product UI should avoid gratuitous first-paint animation. A public landing surface may use one bounded, purposeful hero sequence when a static reduced-motion projection exists and the sequence does not delay interaction. |
| Direction/origin should match user action and trigger context | **Adopt with human review** | Direction/origin are recorded as explicit review checks because semantic correctness is contextual and should not be auto-approved. |
| Exit motion only when it preserves orientation | **Adopt** | Motion assets declare whether an exit is semantically necessary; symmetry is preferred when an exit exists. |
| Motion must never delay the next interaction | **Adopt** | `blocksInteraction=true` is a release-blocking failure. |
| Brand theming through Astryx packages / StyleX | **Reject as Identity dependency** | Identity remains framework-neutral. Astryx can be a consumer/component option later, but it is not canonical token or motion truth. |
| Astryx component/source swizzling | **Reject for this capability** | Identity owns contracts and evidence, not copied React component implementations. |
| Bounce/elastic or attention-seeking decorative motion | **Reject by default** | These conflict with the calm, meaning-first motion contract and require a future explicit exception if ever justified. |

## Identity v1 motion budgets

The default `identity.motion-policy/v1` policy uses these upper bounds:

| Purpose | Maximum duration | Maximum generated asset size | Notes |
| --- | ---: | ---: | --- |
| Micro interaction | 200 ms | 256 KiB | Hover/toggle/selection/state feedback. Usually CSS rather than pre-rendered media. |
| UI transition | 500 ms | 512 KiB | Dialog/panel/expand/collapse transitions. Must not block interaction. |
| Landing sequence | 2,000 ms | 1 MiB | Purposeful public hero/brand sequence. Muted if autoplaying, no infinite loop, static reduced-motion fallback required. |
| Continuous status cycle | 2,000 ms per cycle | 512 KiB | Spinner/progress-like semantic status only. Reduced-motion fallback required. |
| Demo capture | 15,000 ms | 4 MiB | Documentation/product demo asset intended for Relay #8 capture. Deterministic viewport/fixture/provenance required. |
| Static imagery | n/a | 1 MiB | Generated/derived imagery uses the same provenance and visual-baseline contract. |

Cross-cutting defaults:

- maximum frame rate: 60 fps;
- maximum output dimension: 3,840 px on either axis;
- capture network mode: `offline` or `recorded-fixture` only;
- capture data: synthetic/privacy-safe only;
- autoplay: muted; landing sequences only; never interaction-blocking;
- reduced motion: `instant`, `static-fallback`, or `paired-reduced-capture`;
- allowed UI animated properties: `transform`, `opacity`;
- default easing family: standard decelerating/ease-out curves;
- visual/motion baseline changes require human review with source and generated context.

These budgets are release defaults, not universal laws. A future profile may
version a different budget when a product requirement justifies it. Exceptions
must remain explicit and reviewable rather than silently widening the global
policy.

## Source-to-asset provenance

Identity defines `identity.visual-motion-manifest/v1` as the handoff contract for
animation, generated imagery, landing sequences, and Relay-produced demo
captures. Each asset records:

- creator and origin method;
- source reference and SHA-256 digest;
- source license and human approval identifier;
- repository/commit/script/fixture lineage when the asset is a deterministic
  capture;
- generator/tool identifier and version;
- output path, media type, checksum, byte count, dimensions, frame rate, and
  duration where applicable;
- motion purpose, animated properties, easing, autoplay/loop/interaction flags,
  and reduced-motion behavior;
- deterministic capture context: viewport, locale, timezone, network mode,
  privacy-safe state, and synthetic-data state;
- visual baseline target used for review.

Relay issue #8 (`REL-07`) owns the website/demo capture implementation. Relay
should emit this Identity-owned manifest rather than inventing a second motion
provenance format.

## Human-review boundaries

Automation can determine file size, dimensions, frame rate, hashes, policy
membership, reduced-motion metadata, and capture determinism. It cannot safely
approve whether a motion communicates the right meaning or moves in the right
semantic direction.

Identity therefore requires explicit review evidence for:

- `motion.meaning.<asset-id>`
- `motion.direction.<asset-id>`
- `visual.regression.<baseline-target-id>` when generated bytes differ from an
  approved baseline.

The quality report remains the single release decision. Motion validation does
not introduce a parallel pass/fail system.

## Follow-up ownership

- **Identity #3:** motion contracts, policy, validation checks, provenance, and
  fixtures.
- **Relay #8 / REL-07:** deterministic browser/demo capture and optimized
  MP4/WebM/GIF/image-sequence production that emits Identity-compatible
  evidence.
- **Identity #14:** browser-level renderer interaction and reduced-motion
  behavior for the public Brand Kit.
- **LaunchKit/Zensical consumers:** choose presentation mechanics while consuming
  the released Identity policy and assets; they do not become motion-policy
  owners.
