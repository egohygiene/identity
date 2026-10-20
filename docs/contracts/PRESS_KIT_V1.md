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

The source requires exactly one `short` and one `long` boilerplate. It permits
at most one additional `paragraph` boilerplate for a separately supplied
paragraph description. Kinds are unique; the optional paragraph does not
replace either required record. These labels describe intended reuse, without
enforcing sentence counts or generating one length from another. It may
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

When `documents.channelRegistry` is present, all generated `social` links come
from its badge-approved active records. The Press Kit source must not duplicate
those links. This keeps its URLs, handles, verification state, accessible
labels, and icon metadata aligned with badges, footers, and social-surface
targets.

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

When a social package has already been generated from the same canonical
Identity source, the Press Kit can verify and include it:

```bash
python3 "scripts/render_press_kit.py" \
  --repository-root "path/to/consumer" \
  --social-surfaces-directory "assets/identity/social-surfaces" \
  --output-directory "assets/identity/press-kit"
```

The consumer checks the social handoff, manifest, source digest, catalog lock,
archive paths, and manifested contents before adding
`social/social-surfaces.zip`. It does not reconstruct social facts or read a
second manual brand source. See the
[social-surface projection contract](SOCIAL_SURFACES_V1.md).

## Renderer handoff

The reference renderer accepts an explicit generated Press Kit directory. It
checks the Press Kit projection schema, project ID, display name, and exact
source digest against the immutable Brand Kit view model. A mismatch fails
closed rather than rendering a plausible but unrelated package.

When the handoff is valid, the optional Press and media kit section shows only
generated source: boilerplate, facts, links, contacts, supplied public team
bios, selected assets, usage/legal status, and bundle downloads. Relative
asset paths are normalized and constrained to the generated Press Kit
directory using the shared
[artifact-path contract](BRAND_KIT_RENDERER_V1.md#artifact-paths-and-configured-deployment-bases).
Every imported artifact and selected-asset download is checked; configured
local/CDN bases remain separate from these paths.
The renderer never reads `.identity/` or fills in a missing press
contact, biography, asset, legal claim, or social account.

The page provides copy controls for supplied boilerplates and facts using
their exact projected text. Short, optional paragraph and long descriptions
reuse the same approved records as JSON, Markdown and the offline ZIP. Profile
facts such as a short name, distinct mission statement, values or pronunciation
remain ordinary labeled facts; labels and IDs do not activate inferred fields
or generated copy. Contextual naming and voice guidance retain their existing
[voice/usage authority](GUIDANCE_V1.md#context-retrieval).

## Missing data and lifecycle behavior

Facts, links, contacts, team bios, and selected assets can be absent. Their
generated JSON and Markdown explain the absence instead of inventing content.
The two public boilerplates are the minimum affirmative content required to
generate a Press Kit. An absent or nonpublic paragraph is omitted from the
public JSON, Markdown and page without a replacement or placeholder. An
approved public paragraph uses the same governance and exact-text projection
as the required descriptions.

Candidate, internal, rejected, and superseded records stay in canonical source
for review history but are not promoted into the public package. Rebuilding
after an approval or source decision changes is the only way to change an
existing package; publishing or routing the rebuilt package is a separate
consumer deployment decision.

## Compatibility

The optional `paragraph` kind extends the existing source and projection
schemas without adding a second copy document or changing project metadata.
Sources containing only the original short/long pair remain valid. Existing
public-kit prerequisites and filtering still apply.

Older pinned schemas and producers can reject the new enum value, and older
renderers may reject or omit it. Pin a compatible schema, validator, producer
and renderer together when adopting paragraph copy; a v1 schema identifier
alone does not establish support in a previously released tool. Regenerate
digest-bound handoffs from that reviewed source and tool selection, and retain
the previous immutable package for rollback. See proposed
[ADR-0027](../decisions/ADR-0027-optional-paragraph-boilerplate.md) for the bounded
extension and its tradeoffs. This implementation does not accept that proposal
or grant publication authority.

## Deliberately deferred

This contract does not create:

- a social-account registry or social publishing workflow;
- automatic bios, press contacts, launch claims, or screenshots;
- live web scraping, remote asset retrieval, or third-party redistribution;
- website deployment, custom-domain routing, analytics, or a newsroom CMS; or
- automatic creative, legal, or factual approval.

Those boundaries keep the package reliable today while allowing future
consumer-owned social or publication systems to consume the immutable output.
