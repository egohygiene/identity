# Implementation and evidence

## Compiler core

The Rust library exposes the deterministic framework-neutral compiler boundary
behind the Brand Kit generator:

```text
read → validate → resolve → plan → render → verify → manifest
                                      │
                                      └─ transactional apply after approval
```

The compiler provides mutation-free plans, adapter capability/compatibility
records, stable diagnostics, SHA-256 fingerprints and manifests, incremental
unchanged detection, pre-apply verification, and explicit recovery for
interrupted generated-state transactions. Network-dependent or nondeterministic
projection adapters are rejected from the compiler-owned path.

The [compiler v1 contract](../docs/contracts/COMPILER_V1.md) documents the public
Rust ports plus `identity.compiler-plan/v1` and
`identity.compiler-manifest/v1`. The `v1-generate` and `v1-verify` commands
build and check the selected package flow. `v1-inspect` performs read-only
interruption inspection; `v1-recover` explicitly rolls back validated interrupted
transactions. Both use the same repository/output-root authority and operate
without requiring valid brand source or Python. See the
[consumer recovery guide](../docs/consumers/RECOVERY.md). The existing v0 CLI
commands retain their extraction-parity contract.
## Brand Kit packages

The built-in package layer implements nine versioned output profiles over the
compiler ports: `core`, `web`, `pwa`, `github`, `docs`, `social`, `tokens`,
`metadata`, and `archive`.

Those profiles can deterministically project a resolved identity into:

- DTCG JSON, CSS custom properties, JavaScript, TypeScript declarations, and a
  Tailwind-compatible theme;
- document CSS, public metadata, Open Graph markup, PWA icon metadata, and
  explicit voice/usage guidance state;
- approved SVG marks plus PNG favicon, PWA, maskable, social-card, and GitHub
  preview assets through the offline `resvg` adapter boundary;
- package metadata, SHA-256 indexes/checksums, and a deterministic downloadable
  ZIP with fixed ordering and timestamps.

Consumers select profile IDs and compatible versions; selecting a subset does
not generate unrelated profiles. The compiler manifest remains the transaction
and evidence record for the exact selected build. The
[Brand Kit packages v1 contract](../docs/contracts/BRAND_KIT_PACKAGES_V1.md)
defines the stable generated interface, compatibility rules, archive semantics,
and consumer boundary.
## Quality and release evidence

The shared quality layer evaluates a resolved Brand Kit and its compiler manifest
without mutating canonical or generated state. It emits the versioned
`identity.quality-report/v1` contract with one deterministic release decision,
coverage counts, stable check identifiers, source/generated context, and
recovery guidance.

`package` scope validates distributable output while explicitly recording
renderer-only interaction checks as skipped. `publication` scope turns those
same checks into blocking review requirements until the reference renderer owns
real browser evidence. Automated checks cover semantic contrast, reduced-motion
budgets, source integrity, licenses and provenance, SVG structure, target file
budgets, raster dimensions, manifest drift, maskable safe-zone evidence, and
visual baselines. Creative baseline changes and small-size legibility remain
explicit human decisions rather than automated approval.

The [quality gates v1 contract](../docs/contracts/QUALITY_GATES_V1.md) defines the
status vocabulary, default budgets, review evidence, failure/recovery semantics,
and the extension boundary used by visual-motion governance.
## Visual-motion governance

The visual-motion layer extends that same `identity.quality-report/v1` release
decision with versioned `identity.motion-policy/v1` and
`identity.visual-motion-manifest/v1` contracts. It validates animation,
generated imagery, landing sequences, continuous-status motion, and
deterministic demo captures without creating a second release authority.

The default policy is meaning-first and conservative: UI movement uses
`transform`/`opacity`, standard decelerating easing, bounded purpose-specific
durations and file sizes, non-blocking interaction, deterministic synthetic
capture state, and real reduced-motion fallbacks where pre-rendered motion is
used. Motion meaning, direction/origin, and intentional baseline changes remain
explicit human-review boundaries.

The [visual-motion v1 contract](../docs/contracts/VISUAL_MOTION_V1.md) defines the
stable runtime/evidence boundary. The
[Astryx evaluation](../docs/evaluations/astryx-motion-patterns.md) records the
pinned upstream research, MIT license decision, and adopt/adapt/reject matrix.
Relay #8 owns deterministic browser/demo capture and should emit this
Identity-owned provenance contract; Relay does not become motion-policy owner.
