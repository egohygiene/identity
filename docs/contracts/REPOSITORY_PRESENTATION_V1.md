# Repository presentation v1

## Contract boundary

`identity.repository-presentation-source/v1` is optional reviewed `.identity/`
input for canonical repository banners and badge presentation. It owns visual
selection, accessibility text, inheritance, licensing, approvals, and an exact
Hygiene profile lock. It does not own repository conformance.

The renderer additionally receives one explicit
`egohygiene.repository-presentation-evidence/v1` document. Identity reads the
state and exact profile-owned message from that document; it never derives a
state from slots, workflows, repository contents, or the web.

| Authority | Owns | Must not do |
| --- | --- | --- |
| Hygiene | Profile, applicability, evidence semantics, state, and claim limits | Define brand visuals |
| Identity | Approved assets, variants, textual fallbacks, manifests, and checksums | Evaluate or imply conformance |
| Holon/repository tooling | Generated README regions and preview/diff behavior | Replace repository-authored prose |
| Repository | Purpose, status, commands, links, final review, and evidence destination | Present missing evidence as passing |

## Source

Add `documents.repositoryPresentation` to `.identity/identity.json` and point it
to a document matching
[`repository-presentation.schema.json`](../../contracts/v1/repository-presentation.schema.json).

The source contains:

- an immutable Hygiene profile lock: canonical repository, full commit, ID,
  version, status, local path, and `sha256-utf8-lf` digest;
- one organization-default banner asset selected from active, approved public
  Identity usage/provenance records;
- reviewed alt text and a readable textual fallback;
- exact license and attribution copied from governed asset provenance;
- separate human approvals for the banner and badge visual profile; and
- repository visibility plus an optional product override limited to asset ID
  and alt text, with a reason and product-specific approval.

An override is not implicit inheritance. The generated descriptor exposes
whether the organization default was inherited and identifies every approval.

## Explicit evidence input

The evidence document must bind:

- `egohygiene.repository-presentation-profile/v1` at the locked version and
  status;
- one of the ten profile states;
- the exact profile-owned message for that state;
- label `Hygienic`;
- a full 40-character represented commit; and
- a non-empty evidence URL or repository-relative evidence destination.

The state in `assessment.state` and `badge.state` must already agree. Rejecting
an inconsistent document is input validation, not evidence evaluation. Identity
does not inspect slot results to choose a replacement state.

Supported states are `unknown`, `evaluating`, `advisory`, `passing`, `failing`,
`partial`, `stale`, `exempt`, `not_applicable`, and `blocked`. Every state is
rendered with text as well as color. `unknown`, `stale`, `failing`, and every
other non-passing state cannot reuse passing text or bytes.

## Generated package

Run:

```bash
python3 scripts/render_repository_presentation.py \
  --repository-root "path/to/consumer" \
  --evidence "evidence/repository-presentation.json" \
  --output "assets/identity/repository-presentation"
```

Output includes:

- `repository-presentation.json`, the framework-neutral consumer descriptor;
- nine banner variants: light, dark, and high-contrast at 640, 1000, and 1600
  pixels, each as SVG and PNG;
- one state-specific local `Hygienic` badge as SVG and PNG;
- `repository-presentation-manifest.json`, with source, profile, evidence, and
  file integrity bindings; and
- `SHA256SUMS`.

The 640-pixel variant is the narrow baseline. SVGs expose intrinsic dimensions,
`role="img"`, a title, and a description. PNGs have deterministic intrinsic
dimensions. The descriptor contains alt text, textual fallback, destination,
license, source identity, approval lineage, profile status, and every artifact
path. A hosted badge service may wrap the descriptor later but is never
required.

The package explicitly states:

- `editsReadme: false`;
- `evaluatesEvidence: false`;
- `networkRequired: false`; and
- `generatedRegionsOnly: true`.

## Regeneration

Regenerate only after the `.identity/` source, selected asset bytes, profile
lock, or explicit evidence input changes. Run the renderer twice and compare
the complete trees or `SHA256SUMS`; identical inputs must be byte-identical.
The renderer refuses output beneath `.identity/` and does not touch README
files.

## Upgrade

For a Hygiene profile update:

1. review the upstream diff and its status;
2. replace the local profile artifact;
3. update ID, version, full commit, and digest together;
4. update state/message compatibility tests before accepting new vocabulary;
5. regenerate into a new work directory and review descriptor plus images;
6. update downstream immutable package pins only after approval.

A `proposed` profile remains visibly proposed. Identity never converts profile
consumption into activation.

## Rollback

Restore the previous `.identity/` source, local profile artifact, explicit
evidence document, and generated package as one checksum-bound set. Re-run the
renderer and verifier before downstream adoption. README consumers should
change only their generated region, so rollback does not replace authored
prose.

## Fixtures and verification

[`tests/fixtures/repository-presentation`](../../tests/fixtures/repository-presentation)
contains organization-default, product-override, private-repository, and
missing-evidence inputs plus the exact pinned proposed Hygiene profile.
`tests/test_render_repository_presentation.py` proves all ten states, exact
messages, full commit/evidence links, accessible variants, deterministic
checksums, bounded overrides, source/README immutability, and fail-closed
unknown behavior.
