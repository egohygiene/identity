# Identity-only baseline for review

The owner confirmed the existing purple/blue/dark palette and Inter family and
requested an **Identity-only token baseline for review** until an approved
organization-default source is identified. [identity-local.tokens.json](identity-local.tokens.json)
is that draft; preparing it does not approve its exact token document, adopt a
layer or establish an organization standard.

## Source and preserved values

The sole value source is
[`publication/identity-brand-kit.config.json` at `afc368003bfc6a2101051229efd237c8d6fadf71`](https://github.com/egohygiene/identity/blob/afc368003bfc6a2101051229efd237c8d6fadf71/publication/identity-brand-kit.config.json).
Its raw SHA-256 is
`408e3c5bed913e76ea11ef881a8be36cb996c60c1394ab3be08d8808dfcad983`.

The draft preserves all nine supplied type/value records: primary, secondary,
canvas, surface, default text, muted text, border, body family and heading
family. Color components retain their original decimal values; border alpha
remains exactly `0.42`. Both font-family values remain
`["Inter", "system-ui", "sans-serif"]`. These are family references, not bundled
font files or redistribution permissions. No gold role, font metrics, weights,
contrast pairings/thresholds, motion values or new rights facts are invented.

## Draft representation and compatibility

The publication's flat role list contains both `color.text` and
`color.text.muted`. A DTCG tree cannot make `text` both a token and the parent
of another token. This review candidate therefore maps the existing
`color.text` value to **`color.text.default`**, retaining `color.text.muted` and
all other paths unchanged. This is an explicit draft representation choice,
not a new text role or a claim of compatibility with existing lookups.
Consumers expecting `color.text` need a reviewed mapping before adoption;
no existing projection or consumer has been changed.

The document uses the existing Identity v1 token schema and its supported
`color` and `fontFamily` shapes. Its root names the token contract but omits
layer identity/kind/priority: no organization-default authority is asserted,
and the candidate project's layer list remains unadopted. Review the exact
document and eventual layer declarations/digests before connecting it to the
candidate manifest. An actual reviewed organization snapshot remains pending.

JSON/schema and exact source-value checks are narrower than full project
validation, contrast or renderer qualification. They do not make the incomplete
self-source candidate valid or approved. Do not promote this draft into the
repository's canonical `.identity/` merely because those checks pass.

ADR not required: this prepares a review-only candidate under the existing
DTCG and local-layer contracts (ADR-0004 and ADR-0012), without changing a
schema, projection, policy or approved source.
