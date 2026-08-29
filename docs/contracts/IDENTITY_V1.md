# Identity v1 source contract

## Contract boundary

`identity.project/v1` is the consumer-owned, editor-friendly source contract
for one organization, product, or repository identity. Canonical input stays
under `.identity/`; Identity-owned projections stay under `assets/identity/`.
No generated file becomes source merely because it is committed.

The v1 topology is:

```text
.identity/
├── identity.json                    # project, layer order, paths, compatibility
├── brief.md                         # human-reviewed creative intent
├── defaults/
│   └── organization.tokens.json     # immutable organization-default snapshot
├── overrides/
│   └── product.tokens.json          # intentional product differences
├── targets/
│   └── profiles.json                # versioned output-profile selection
├── governance/
│   ├── provenance.json              # license, lineage, accessibility, usage
│   └── approvals.json               # human decisions and evidence
├── guidance/
│   ├── voice.json                   # optional until IDN-11 lands
│   ├── usage.json                   # optional until IDN-11 lands
│   ├── design-system.json            # optional reviewed handbook source
│   ├── design-references.json        # optional reviewed reference catalog
│   ├── press-kit.json                # optional reviewed Press/Media Kit source
│   ├── social-surfaces.json          # optional pinned surface selections
│   └── mascot.json                   # optional reviewed character system
├── sources/                         # approved canonical source assets
├── candidates/                      # unapproved work state
└── references/                      # reviewed inspiration, never implicit license
```

The manifest may choose different normalized repository-relative paths, but it
must name every boundary above. Voice and usage paths are nullable in the first
v1 slice so #13 can stabilize their contents without pretending that v0 prose
was already structured. Directories are never optional.

`documents.handbook` is an optional additive v1 object. When a consumer adopts
it, it names both local handbook source files. `design-system.json` records
approved principles and explicit capability ownership; `design-references.json`
records reviewed external observations and rights constraints. They validate
under the same human approval model as voice and usage. See the
[design-system handbook contract](DESIGN_SYSTEM_V1.md).

`documents.pressKit` is an optional additive v1 path. It names one local,
reviewed Press and Media Kit source document. The source can contain approved
short and long boilerplate, facts, links, contacts, optional team bios, and
explicit selections from already-approved public assets. It never makes a
candidate record, unapproved fact, or unspecified asset public. See the
[Press Kit contract](PRESS_KIT_V1.md).

`documents.socialSurfaces` is an optional additive v1 path. It selects exact
records from a repository-local, digest-pinned Aether catalog, then maps them
to existing approved public Identity assets and closed project metadata
selectors. Projects explicitly adopt every organization default and can record
reviewed product exclusions or bounded overrides. See the
[social-surface projection contract](SOCIAL_SURFACES_V1.md).

`documents.mascot` is an optional additive v1 path. It binds one reviewed
character system to a governed canonical asset, semantic visual invariants,
responsive variants, accessibility guidance, motion limits, a license, and a
human approval. See the [mascot and character-system contract](MASCOT_SYSTEM_V1.md).

## Layer and merge model

Layers are listed in ascending, unique integer priority. All
`organization-defaults` layers precede exactly one final `product-override`
layer. Every token document is locally available and pinned by SHA-256; the
validator performs no network access.

Resolution follows these rules:

1. Flatten each DTCG token document to stable dot-separated token paths.
2. Apply layers in ascending priority.
3. A new token path is added directly.
4. Replacing an inherited token requires
   `$extensions.org.egohygiene.identity.override` with a non-empty reason and
   approval ID.
5. A replacement without that declaration is `IDN1304` and fails closed.
6. Resolve aliases only after all layers merge.
7. Missing aliases (`IDN1305`) and alias cycles (`IDN1306`) fail closed.

The resolved value retains its source layer. Compiler projections must expose
that lineage and the override declaration rather than presenting the final
value as context-free.

## DTCG alignment

Token documents use the Design Tokens Community Group 2025.10 shape:

- groups contain nested groups/tokens plus `$type`, `$description`,
  `$extensions`, or `$deprecated` metadata;
- tokens contain `$value` and optional `$type`, `$description`, `$extensions`,
  or `$deprecated` fields;
- aliases use `{dot.separated.token.path}`;
- group `$type` is inherited when the token omits `$type`;
- the supported stable type vocabulary is encoded in
  [`tokens.schema.json`](../../contracts/v1/tokens.schema.json).

Identity adds only the namespaced `org.egohygiene.identity` extension. It
records layer identity, intentional overrides, contrast intent, typography
license/language/legibility constraints, reduced-motion alternatives, and
approval/provenance references. Other namespaced DTCG extensions are preserved
but are not interpreted by the v1 validator. Unnamespaced extensions and
unknown Identity extension fields are rejected rather than accepted silently.

The v1 schema intentionally does not make Style Dictionary, CSS, Tailwind, or
any renderer canonical. Semantic tokens are source. Concrete platform values
remain versioned projections selected through target profiles.

## Accessibility and asset governance

The contract can express:

- color background/foreground/decorative intent, supported pairings, and a
  required minimum contrast ratio;
- typography license, language coverage, fallbacks through DTCG values, and
  legibility constraints;
- motion timing with a named reduced-motion alternative;
- mark/imagery alt text, safe zone, minimum size, and usage restrictions;
- immutable file digests, license status, creator/method/source lineage, and a
  linked human approval decision.

Every non-documentation file under the approved `sources/` directory requires
one provenance record. The record's digest must match the bytes. Its license
status must be `approved`, its provenance must be complete, and its approval
must resolve to an approved human decision for the same subject. Candidates
and references remain distinct trust zones.

## Diagnostics

Validation emits `identity.diagnostics/v1`. Diagnostics are sorted by JSON
pointer or repository-relative path and stable code. Each includes severity,
message, and a concrete recovery action. The initial code families are:

| Range | Boundary |
| --- | --- |
| `IDN1000`–`IDN1099` | project/topology/loading |
| `IDN1100`–`IDN1199` | closed structure and primitive values |
| `IDN1200`–`IDN1299` | token/DTCG structure |
| `IDN1300`–`IDN1399` | layers, overrides, aliases, and conflicts |
| `IDN1400`–`IDN1499` | license, provenance, source bytes, and approvals |
| `IDN1500`–`IDN1599` | target profiles and compatibility |
| `IDN1600`–`IDN1699` | voice, usage, and guidance lifecycle |
| `IDN1700`–`IDN1799` | handbook source and reviewed references |
| `IDN1800`–`IDN1899` | Press Kit source and public-selection boundary |
| `IDN1900`–`IDN1999` | pinned social catalog, selection, and projection boundary |
| `IDN2000`–`IDN2099` | mascot source, approval, provenance, and variant boundary |

JSON output is the automation contract. Human output renders the same records;
it does not invent a second validation result.

## Compatibility, deprecation, and migration

The schema major is part of every contract identity. Additive optional fields,
new diagnostics, and clarified validation may remain within v1. Removing or
renaming fields, changing merge precedence, or changing an accepted field's
meaning requires v2 plus migration guidance.

Deprecated fields/tokens remain readable for at least one minor release and
must identify a replacement or removal plan. Unknown fields always fail; an
extension must use an explicit namespace and versioned schema.

`identity.project/v0` is not silently reinterpreted as v1. The migration plan
preserves project metadata, profile selection, required-source roles, brief,
and context inputs while identifying human decisions that v0 could not encode:
organization-default snapshots, DTCG tokens, license/provenance records,
approvals, voice, and usage. Migration writes to a separate destination,
validates it, compares plans, and promotes it only after review. Rollback keeps
the v0 source and last generated outputs until v1 is accepted.

## Validation

```bash
python3 scripts/validate_identity.py \
  --repository-root "path/to/consumer" \
  --format "human"

python3 scripts/validate_identity.py \
  --repository-root "path/to/consumer" \
  --format "json"
```

The validator uses only the Python standard library, reads local files, makes
no network calls, and never mutates canonical or generated state.
