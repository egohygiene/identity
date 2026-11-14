# Using Identity

Run the examples from the repository root. Consumer commands keep an explicit
`--repository-root`; Task commands are checkout development shortcuts. See
[development setup](DEVELOPMENT.md) for the pinned tool environment.

## CLI foundation

The independently buildable Rust CLI currently preserves four local-first
commands from the Empathy incubation:

```bash
cargo run -- init \
  --repository-root "path/to/consumer" \
  --project-id "consumer" \
  --display-name "Consumer"

cargo run -- validate --repository-root "path/to/consumer"

cargo run -- plan \
  --repository-root "path/to/consumer" \
  --format "markdown"

cargo run -- handoff \
  --repository-root "path/to/consumer" \
  --output-directory ".cache/identity/handoff"

cargo run -- studio-review \
  --repository-root "path/to/consumer" \
  --handoff "review/identity-approved-handoff.json" \
  --release-view-model "assets/identity/brand-kit-view-model.json" \
  --output ".cache/identity/studio-review.json" \
  --format "markdown"
```

`init` creates consumer-owned `.identity/` intent. `validate` checks the v0
project and profile contracts. `plan` resolves eight profiles and 45 targets
without generating them. `handoff` creates a deterministic, provenance-aware
creative source-pack request whose candidates remain unapproved by default.
`studio-review` accepts only a named, explicitly approved local-studio handoff
that matches an immutable Brand Kit release; it resolves the selected existing
CLI profiles into a deterministic review plan. It does not write canonical
`.identity/` source or generated assets; an optional saved review record must
remain outside both locations.

Raster/vector rendering, asset application, packaging, and publication remain
outside the extracted v0 vertical slice. The separate v1 package commands are
documented below. See the
[Empathy extraction evidence](../docs/migration/EMPATHY_EXTRACTION.md).
## Identity v1 source

The unqualified [#133 initializer draft](consumers/V1_INITIALIZATION.md) adds
explicit `v1-init --repository-root ROOT --request FILE --output-directory DIR`
source-candidate preparation. It does not change v0 `init`/`validate`, promote
source or generate assets. It is absent from published `v1.0.0`; runtime
acceptance and CI are deferred. Manual v1 authoring remains supported.

Validator maintenance uses focused canonical modules under
[`scripts/identity_validation/`](../scripts/identity_validation/README.md).
Regenerate `scripts/validate_identity.py` with
`python3 scripts/build_identity_validator.py` after editing those modules.
The public script/import path and the Rust-embedded standalone payload retain
their existing offline boundary.

The v1 contract adds content-addressed organization defaults, intentional
product overrides, DTCG-compatible semantic tokens, versioned target profiles,
asset provenance/licensing, and human approvals beneath `.identity/`.

```bash
python3 scripts/validate_identity.py \
  --repository-root "tests/fixtures/v1/valid/minimal" \
  --format "human"

python3 scripts/plan_v0_migration.py \
  --repository-root "tests/fixtures/migration/empathy-v0" \
  --format "human"
```

Both tools are standard-library-only, offline, and non-mutating. The complete
[v1 contract](../docs/contracts/IDENTITY_V1.md) documents topology, merge order,
aliases, compatibility, diagnostics, migration, and rollback.

Validated v1 consumers can use the explicit package boundary without importing
compiler internals:

```bash
cargo run -- v1-generate --repository-root "path/to/consumer"
cargo run -- v1-verify --repository-root "path/to/consumer"
```

`v1-generate` resolves the selected versioned profiles, writes a transactional
package and compiler manifest beneath `assets/identity/`, and never writes
canonical `.identity/` source. `v1-verify` is read-only; it fails when the
selected package is missing, stale, or drifted. Both commands and the public
`V1ConsumerPipeline::load` library API run the complete authoritative source
validator automatically, including schema, approval, digest, and path checks.

V1 execution requires Python 3.11+ (`python3` on Unix, `python` on Windows;
`IDENTITY_PYTHON` can select an explicit executable). The binary embeds the
standard-library validator and runs it in isolated mode: no Identity checkout,
Python packages, or network access is needed. Missing Python fails before writes.
Validated input files are checked again after planning and before applying a
build; source changes require loading and planning again. The standalone
validator remains available for diagnostic-only use.
## Governed brand guidance

To assemble native downloads, an optional handbook and an optional Press Kit
into one usable public page, follow the
[complete Brand Kit guide](../docs/consumers/COMPLETE_BRAND_KIT.md). The builder
checks actual generated files and source agreement, preserves static content,
omits absent sections/review controls, and emits an offline-verifiable kit.
Building a kit remains separate from releasing or deploying it.

Voice, contextual tone, vocabulary, examples, anti-examples, usage rules,
accessibility, legal notes, localization, legacy assets, and approval state are
first-class Identity v1 source. Public output includes only approved public
records; the review projection preserves candidate, approved, rejected, and
superseded decisions with their human-review evidence.

```bash
python3 scripts/render_guidance.py \
  --repository-root "tests/fixtures/v1/valid/minimal" \
  --audience "public" \
  --format "html" \
  --output "build/brand-guidance.html"

python3 scripts/render_guidance.py \
  --repository-root "tests/fixtures/v1/valid/minimal" \
  --audience "review" \
  --context "support" \
  --format "json"
```

The renderer validates source before projection, never invents brand prose,
and refuses to write beneath canonical `.identity/`. The
[guidance v1 contract](../docs/contracts/GUIDANCE_V1.md) defines authority,
lifecycle, context retrieval, deterministic JSON/Markdown/HTML outputs, and
legacy-asset publication policy.
## Press and Media Kits

Consumers can opt into a governed Press Kit source without making publication
or deployment part of their canonical identity contract. Identity projects only
approved public boilerplate, facts, links, contacts, supplied team biographies,
and explicitly selected approved assets into a deterministic package:

```bash
python3 scripts/render_press_kit.py \
  --repository-root "path/to/consumer" \
  --output-directory "assets/identity/press-kit"
```

The output includes JSON, Markdown, an integrity manifest, checksums, selected
assets, and a deterministic ZIP. It is ready for a consumer-owned release or
site deployment step, but does not publish anything itself. See the
[Press Kit and Media Kit contract](../docs/contracts/PRESS_KIT_V1.md).
## Social-surface packages

Consumers can explicitly map approved Identity assets and project metadata to
stable records in a repository-local, digest-pinned Aether catalog:

```bash
python3 scripts/render_social_surfaces.py \
  --repository-root "path/to/consumer" \
  --output-directory "assets/identity/social-surfaces"
```

Identity never fetches platform facts or generates an implicit platform
matrix. The package retains exact dimensions, media constraints, safe-zone
state, source verification, approvals, provenance, a manifest, checksums, and
a deterministic archive. It is renderer-ready input with publication authority
explicitly denied. See the
[social-surface projection contract](../docs/contracts/SOCIAL_SURFACES_V1.md).
## Organization channels

Identity owns one versioned registry for official Ego Hygiene social accounts
and community channels. Consumers can render the complete reviewed lifecycle
view plus public adapters that include only badge-approved active channels:

```bash
python3 scripts/render_channel_registry.py \
  --repository-root "path/to/consumer" \
  --output-directory "assets/identity/channels"
```

Planned and reserved candidates remain explicit without invented handles.
Press Kit social links and social-surface targets consume this same registry,
while credentials and recovery material remain outside the public contract.
See the [organization channel registry contract](../docs/contracts/CHANNEL_REGISTRY_V1.md).
## Repository presentation packages

Consumers can project canonical README banners and local evidence badges from
reviewed `.identity/` visuals plus one explicit Hygiene evidence document:

```bash
python3 scripts/render_repository_presentation.py \
  --repository-root "path/to/consumer" \
  --evidence "evidence/repository-presentation.json" \
  --output "assets/identity/repository-presentation"
```

The output includes light, dark, high-contrast, and narrow banner variants;
static SVG and PNG `Hygienic` badges; accessible textual fallbacks; a
framework-neutral descriptor; integrity manifest; and checksums. Identity pins
the proposed Hygiene profile by full commit and digest, but never evaluates
evidence, activates policy, fetches the web, or edits a consumer README. See
the [repository-presentation contract](../docs/contracts/REPOSITORY_PRESENTATION_V1.md).
