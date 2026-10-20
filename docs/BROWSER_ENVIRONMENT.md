# Qualified browser and screenshot environment

The approved desktop screenshot is checked through one profile in
[dev/browser/profile.json](../dev/browser/profile.json), shared by the reference
renderer and release smoke workflows. It implements the existing
[ADR-0011](decisions/ADR-0011-accessibility-and-visual-evidence.md) requirement;
automated browser passes do not replace human visual/accessibility review.

## Run the qualified command

On a Docker host, from a checkout:

```bash
python3 scripts/qualify_browser.py \
  --output-directory /tmp/identity-browser-evidence
```

Use a new or empty output directory outside the checkout. The wrapper checks
the approved PNG/hash, frozen Playwright/pnpm versions, immutable image identity
and selected Linux/amd64 configuration before building. It copies the checkout
into a disposable image; the source checkout is not mounted writable. The
browser runs with fixed CI settings, UTC and 1 GiB shared memory. Its network is
disabled except for loopback, where the local static preview/downloads run.
Installation happens separately during the frozen image build.

The profile selects the official Playwright 1.62.1 Noble image by OCI digest,
matching the locked test package. Only the recorded Linux/amd64 execution is
qualified by retained evidence. An arm64 Docker engine may emulate this image;
the receipt records that distinction and its actual comparisons must pass.
Other architectures/custom images are not qualified by index availability.

The same command accepts --mode ci for an invocation label; settings, image,
fonts and assertions remain identical. The reference workflow runs CI mode
and also replays the default local entrypoint on its Docker host. That is a
hosted local-entrypoint replay, not proof that this authoring workspace ran
Docker. This workspace has no usable container engine; native host tests remain
separate evidence.

## Fixed settings and font evidence

The profile fixes locale en-US, timezone UTC, scale 1, light color scheme,
no-preference motion and the 1440×1000 screenshot viewport. The existing
assertion disables animations and captures only the viewport. Chromium's
existing sRGB launch switch is verified. No pixel-threshold relaxation,
max-difference allowance or browser/font package update is introduced to make
a comparison pass.

The image freezes browser binaries, system libraries and installed fonts.
Runtime receipts record actual Node, pnpm, Playwright, Chromium/headless-shell
versions and executable hashes; font files and fontconfig configuration hashes;
fc-match substitutions; and representative rendered fonts through Chromium's
platform-font inspection. The fixture declares Inter/system-ui/sans-serif but
does not bundle Inter. Its actual fallback is recorded rather than inferred
from a CSS family name. No font is downloaded while rendering.

## Positive and deliberate-drift proof

Qualification runs the existing six E2E checks against the unchanged baseline.
It then changes only disposable built CSS, reruns the original screenshot
assertion and requires a real comparison failure with a fresh diff image.
A timeout or unrelated failure is not accepted as drift detection. The CSS
bytes are restored and the screenshot assertion must pass again. The approved
PNG hash is checked throughout; update-snapshot mode is disabled.

The approved PNG remains SHA-256
53d7d144734ac63ceb730e95c7a39acc47d3fa64c5429f752233978289088543,
last changed by the human baseline commit
[85f650f936950094a608f5c477b9a59d4be29a87](https://github.com/egohygiene/identity/commit/85f650f936950094a608f5c477b9a59d4be29a87).
A deliberate product change requires a human-reviewed visual diff and explicit
baseline update. Qualification never regenerates or approves a baseline.

Receipts, positive/negative/restored reports and diff/actual screenshots go to
the external output directory and CI artifact. Keep durable source-bound
receipts with the PR; temporary CI artifacts alone may expire. See the
[qualification review](reviews/browser-environment-2026-10-20.md).

## Development, refresh and rollback

Ordinary renderer unit/public-build checks remain separate from the qualified
browser environment. Raw pnpm test:e2e or an existing development image can be
used diagnostically, but host fonts/browser libraries may differ. Use the
qualified command for approved-baseline evidence; do not repair host mismatches
by relaxing tolerance or replacing the PNG.

Maintainers refresh Playwright/package locks, image/profile and a new dated
registry receipt together in a reviewed PR. Record immutable upstream source,
selected manifest/config identity and raw digest verification; update the
profile's registry pointer. Re-run both entrypoints and deliberate-drift proof,
inspect runtime/font changes and preserve the existing PNG unless humans
explicitly approve a product/baseline change. Git retains the previous profile,
locks and evidence for rollback.

The browser Dockerfile reuses image-provided Corepack, with the repository's
existing pinned 0.34.6 fallback if absent, and installs frozen dependencies.
It is separate from the portable development add-on; custom development bases
and their ownership/trust responsibilities remain in
[DEVELOPMENT.md](DEVELOPMENT.md). Broader standalone/Make/Task/Docker setup
coverage stays #82; final documentation reconciliation stays #83.
