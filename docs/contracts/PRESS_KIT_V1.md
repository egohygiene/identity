# Identity v1 Press Kit and Media Kit contract

## Status and boundary

This document defines the contract slice for
[issue #34](https://github.com/egohygiene/identity/issues/34). It creates a
deterministic, offline Press Kit and Media Kit from reviewed local Identity
source. It is a projection boundary, not a publication system, a content
authoring system, or permission to expose unfinished material.

Identity owns validation and the generated package. Consumer identity owners
remain responsible for every supplied claim, contact, biography, asset, and
approval. Website routing and deployment remain outside this repository.

## Canonical source

`identity.project/v1` may add one optional path:

```json
{
  "pressKit": ".identity/guidance/press-kit.json"
}
```

The extension is additive: a v1 consumer without `documents.pressKit` remains
valid, and the generator reports that a Press Kit has not been adopted. Once
the path is configured, the source must validate as
`identity.press-kit-source/v1` under the same local human approval model as
voice, usage, and handbook material.

The source requires exactly one `short` and one `long` boilerplate. It may
also contain facts, HTTPS links, contacts, optional team biographies, and
explicit asset selections. Every record has a lifecycle, visibility,
provenance, and approval envelope. Only `approved` + `public` records with a
matching approved decision can appear in generated output.

An asset selection references an existing `assetId`; it does not embed a new
file. The selected asset must already be active, public, approved, and
provenance-verified by the normal Identity asset boundary. This keeps a Press
Kit from accidentally turning candidate artwork, private material, or an
unverified download into a public asset.

## Generated package

`scripts/render_press_kit.py` first validates the complete consumer source,
then creates a framework-neutral `identity.press-kit/v1` projection. Its
source block records the canonical SHA-256 source digest, source schema, and a
fixed projection version. It also preserves resolved layer inheritance so an
organization-wide Press Kit and a product Press Kit are equally auditable.

The complete package contains:

| File | Purpose |
| --- | --- |
| `press-kit.json` | Machine-readable approved projection |
| `press-kit.md` | Human-readable Press and Media Kit |
| `press-kit-manifest.json` | `identity.press-kit-package/v1` integrity index |
| `SHA256SUMS` | Checksums for the immutable package contents |
| `press-kit.zip` | Deterministic offline archive |
| `assets/…` | Only the explicitly selected approved public assets |

Arrays are sorted by stable source identifiers, JSON is canonical, archive
timestamps and modes are fixed, and no generation timestamp is recorded. The
same valid source therefore produces byte-identical output. The command never
fetches links or contacts, changes canonical source, or writes inside
`.identity/`.

## Commands

Review a single projection without writing files:

```bash
python3 "scripts/render_press_kit.py" \
  --repository-root "path/to/consumer" \
  --format "markdown"
```

Write the complete release-ready package outside canonical source:

```bash
python3 "scripts/render_press_kit.py" \
  --repository-root "path/to/consumer" \
  --output-directory "assets/identity/press-kit"
```

The package directory is explicit so a downstream site or release process can
copy it as a single immutable unit. A caller that needs a different static
route owns that routing and deployment configuration.

## Renderer handoff

The reference renderer accepts an explicit generated Press Kit directory. It
checks the Press Kit projection schema, project ID, display name, and exact
source digest against the immutable Brand Kit view model. A mismatch fails
closed rather than rendering a plausible but unrelated package.

When the handoff is valid, the optional Press and media kit section shows only
generated source: boilerplate, facts, links, contacts, supplied public team
bios, selected assets, usage/legal status, and bundle downloads. Relative
asset paths are normalized and constrained to the generated Press Kit
directory. The renderer never reads `.identity/` or fills in a missing press
contact, biography, asset, legal claim, or social account.

## Missing data and lifecycle behavior

Facts, links, contacts, team bios, and selected assets can be absent. Their
generated JSON and Markdown explain the absence instead of inventing content.
The two public boilerplates are the minimum affirmative content required to
generate a Press Kit.

Candidate, internal, rejected, and superseded records stay in canonical source
for review history but are not promoted into the public package. Rebuilding
after an approval or source decision changes is the only way to change an
existing package; publishing or routing the rebuilt package is a separate
consumer deployment decision.

## Deliberately deferred

This contract does not create:

- a social-account registry or social publishing workflow;
- automatic bios, press contacts, launch claims, or screenshots;
- live web scraping, remote asset retrieval, or third-party redistribution;
- website deployment, custom-domain routing, analytics, or a newsroom CMS; or
- automatic creative, legal, or factual approval.

Those boundaries keep the package reliable today while allowing future
consumer-owned social or publication systems to consume the immutable output.
