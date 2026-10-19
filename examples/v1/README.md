# Identity v1 authoring examples

These are executable, **fictional** examples, not approved identities for a real
project. All reviewers, review evidence, dates, rights statements, contacts and
artwork describe synthetic test data. Replace them with actual source and human
decisions before adopting an identity. Passing validation does not grant approval
or publication authority.

| Example | Canonical source | Selected core profiles |
| --- | --- | --- |
| [minimal](minimal/.identity/identity.json) | One approved SVG, one semantic token, two pinned local layers, explicit `null` voice/usage. The final product layer replaces no tokens and needs no override decision. | `core`, `tokens`, `metadata` |
| [expanded](expanded/.identity/identity.json) | The same small foundation plus a reviewed token override, contextual voice, public usage and governed Press Kit copy, website and media contact. | `core`, `tokens`, `metadata` |

Both omit optional handbook, mascot, channel, social-surface and repository
presentation sources. Expanded demonstrates one useful optional package rather
than requiring every available feature. Reusable descriptions and contact details
live in the Press Kit source; tone and contextual naming live in voice guidance.
The project manifest owns only its existing project metadata.

The older `tests/fixtures/v1/valid/minimal` directory is an expanded historical
regression corpus. Its name, source bytes and expected projections remain stable;
these new examples are the authoring entry point.

## Try a consumer

Copy the chosen example's entire `.identity/` directory into a disposable consumer
repository. The checked-in `$schema` paths resolve within this checkout; for an
independent consumer, replace those editor references with the equivalent schema
files from the same immutable Identity source pin. Manifest document paths and
layer digests remain consumer-relative. Keep candidates and references separate
from approved sources.

From this Identity checkout, validate, generate and verify the copied source:

```bash
python3 scripts/validate_identity.py \
  --repository-root "path/to/consumer" \
  --format "human"
cargo run --locked --bin identity -- v1-generate \
  --repository-root "path/to/consumer"
cargo run --locked --bin identity -- v1-verify \
  --repository-root "path/to/consumer"
```

These examples require the checkpoint 2 implementation in this source revision;
the `v1.0.0` release does not support their nullable guidance end to end. Pin the
exact reviewed commit until these changes ship in an immutable release. The
legacy `init` and `validate` CLI commands still target v0 TOML.

Generation writes selected outputs under `assets/identity/`. It preserves
`.identity/`; verification is read-only. The minimal metadata guidance projection
contains explicit absence instead of invented voice or usage text. Expanded's
optional Press Kit is a separate projection command:

```bash
python3 scripts/render_guidance.py \
  --repository-root "path/to/consumer" \
  --audience "public" \
  --format "json"
python3 scripts/render_press_kit.py \
  --repository-root "path/to/expanded-consumer" \
  --output-directory "assets/identity/press-kit"
```

The source contract requires two layers, at least one selected profile and the
declared source/candidate/reference directories. The current Brand Kit producer
also requires a nonempty resolved token set and an approved SVG source. These
examples meet that producer boundary; they do not claim to be the only valid
source shape or a complete public Brand Kit. Selected-output verification does
not verify optional packages, public-kit readiness or a deployed website. Review
the [field audit](../../docs/reviews/identity-fields-2026-10-18.md) for separately
tracked producer and public-download findings.
