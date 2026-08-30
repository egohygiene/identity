# Identity dogfood experience

This directory contains Identity's bounded `/identity/` subpath adapter,
browser-evidence lock, adapter-only CSS, and reviewed visual baseline contract.
Reviewed product, documentation, architecture, and legal copy lives in
`publication/identity-experience.content.json`. This repository does not vendor
Holon, LaunchKit, Zensical, or canonical brand truth.

The builder consumes Holon commit
`2600baff6f6d944094da81b77e1a9a2e9e7a1cd6`, verifies the accepted
`landing-launchkit`, `docs-zensical`, and `site-suite` blueprint Git blobs and
file inventories, then materializes their reviewed LaunchKit variant in the
accepted overlay order. It resolves Kern and palette inputs from the governed
Identity package, installs Holon's hash-locked Zensical `0.0.57` graph and
frozen pnpm graph, and emits one composite under `/identity/`.

`site_suite_adapter.py` changes only the consumer boundary Holon deliberately
leaves to Identity: `/identity/` reference normalization and the pinned pnpm
command entrypoint. Holon still owns composition, generated internals, and its
four-surface verification.

## Build and verify

Check out the accepted Holon commit beside this repository, then run:

```bash
python3 scripts/build_identity_experience.py \
  --repository-root "." \
  --holon-source "../holon" \
  --output ".identity-experience-build" \
  --release-tag "v1.1.0" \
  --release-commit "<full-release-commit>"

python3 scripts/verify_identity_experience.py \
  --repository-root "." \
  --artifact-root ".identity-experience-build" \
  --expected-release-tag "v1.1.0" \
  --expected-release-commit "<full-release-commit>"
```

The tag shown above is the candidate binding until an immutable `v1.1.0`
release exists. Candidate artifacts are review evidence and must not be
installed as the canonical route. A tag-triggered build binds the exact stable
tag and commit; a subsequent manual live gate compares that binding with the
canonical Brand Kit `site.json`.

## Browser evidence

```bash
cd "experience"
corepack pnpm install --frozen-lockfile
corepack pnpm exec playwright install --with-deps chromium firefox webkit
corepack pnpm test:e2e
```

The browser suite checks keyboard focus, serious/critical accessibility
violations, no-JavaScript readability, reduced motion, high contrast, and all
four direct surfaces. Chromium captures wide and narrow landing, docs,
architecture, and legal evidence. CI uploads those screenshots with the exact
built composite. Source digests in `visual-baselines.json` block silent visual
drift and require fresh review evidence before approval.
