# Assemble a complete public Brand Kit

The consumer kit builder presents generated public material in one static
experience. It reads the selected native compiler manifest and renderer model,
plus explicitly supplied generated handbook and Press Kit directories. It does
not read canonical `.identity/` source or supply missing facts, rights or
approvals. Create and approve artwork in your preferred design workflow, then
record it through the existing [authoring contract](AUTHORING.md).

## Generate and assemble

Use one reviewed immutable Identity tool/source selection for every projection.
From that Identity checkout, generate and verify the consumer's native outputs:

```bash
consumer_root="/absolute/path/to/consumer"
identity_bin="/absolute/path/to/reviewed/identity"
"$identity_bin" v1-generate --repository-root "$consumer_root"
"$identity_bin" v1-verify --repository-root "$consumer_root"
```

When the consumer adopts `documents.handbook` or `documents.pressKit`, generate
those existing optional projections from the **same unchanged source**:

```bash
python3 scripts/render_design_system.py \
  --repository-root "$consumer_root" \
  --output-directory "build/identity-handbook"
python3 scripts/render_press_kit.py \
  --repository-root "$consumer_root" \
  --output-directory "build/identity-press"
```

From `renderer/`, with its locked dependencies installed, assemble the kit:

```bash
corepack pnpm run build:kit -- \
  --artifact-root "$consumer_root/assets/identity" \
  --output-directory "$consumer_root/build/identity-kit" \
  --design-system-directory "$consumer_root/build/identity-handbook" \
  --press-kit-directory "$consumer_root/build/identity-press"
corepack pnpm run verify:kit -- \
  --output-directory "$consumer_root/build/identity-kit"
```

Omit each optional generation command and matching builder flag when its source
is not adopted. The minimal command needs only `--artifact-root` and
`--output-directory`. Output must be new or empty and disjoint from all supplied
input directories; the builder rejects canonical `.identity/` destinations.
Rebuild into a new directory instead of overwriting unrelated files.

`--asset-base-url` defaults to `./`. An explicit local deployment prefix or
HTTP(S) artifact directory uses the existing safe-path contract. Verification
checks the retained local files; it never fetches a CDN or proves remote
availability. Browser metadata is opt-in through `--icon-path`,
`--apple-touch-icon-path` and `--web-manifest-path`, naming actual selected native
files. The page's own JavaScript/CSS remain portable relative resources.

## What a visitor gets

The public page brings together approved marks and source rights, exact supplied
copy, color/font guidance, handbook material and selected presentation images.
Navigation and copy controls use the existing renderer. Essential content and
downloads remain in static HTML when JavaScript is disabled. Review controls
and absent optional sections are omitted. The independent model-only preview
retains its existing review tools and explicit absence states.

Downloads remain the existing generated files and packages. The native asset
archive is labeled **Download asset package** in the public hero; an optional
Press Kit has its own complete archive, and handbook/context files retain their
own downloads. A new all-in-one archive is not needed to obtain the complete
set from this page. Existing native archive contents are unchanged.

## Binding and verification

The builder validates the native model against its actual compiler inventory,
checks all selected files, and copies only verified native outputs and explicit
optional projection files. Neighboring unselected files are excluded.
Handbook/Press Kit project identity and source digests must agree with the
native immutable model. The displayed optional JSON must equal its downloadable
projection. Press Kit verification reconstructs the deterministic package and
compares every file, including archive bytes, rejecting extra files and ZIP
member injection. This native-only mode does not admit an external social
catalog/package; its separate existing admission boundary still applies.

The output retains `.identity-manifest.json` and the native renderer model
unchanged. `brand-kit.view-model.json` is the existing model with the supplied
optional renderer views composed. `kit.json`, described by the
[consumer receipt schema](../../contracts/v1/consumer-brand-kit.schema.json),
binds its project/source/release metadata, artifact base, browser selections and
every output file's bytes and SHA-256, excluding the receipt itself. The offline
verifier checks exact inventory equality, native manifest binding, displayed
projection agreement, selected download links and navigation targets.

The receipt is integrity evidence, not a signature, rights grant or publication
decision. Preserve the native release status/version/source digest; a local
build does not turn generated material into a published release. Regenerate all
projections together after source changes. Never edit immutable historical
artifacts or substitute another project's optional projection.

## Publication owners and remaining self-dogfood

| Surface | Owner and gate |
| --- | --- |
| This consumer kit | Consumer-owned canonical source, matching generated projections and the existing renderer. Build and offline verification produce a reviewable artifact directory. |
| `identity.egohygiene.io` | Existing stable-release Brand Kit publisher and `site.json` binding. This command changes no release selection, canonical route, deployment or rollback policy. |
| `egohygiene.io/identity/` | Existing Holon-based product experience and organization route owner; retain their independent release/artifact handoff. |
| Intelligence/Decisions | Existing Relay composition and independently pinned source; preserve its routes and separate ADR disposition. A Brand Kit receipt supplies no Intelligence publication authority. |

See the [publication guide](../publication/IDENTITY_PAGES.md) and accepted
[ADR-0017](../decisions/ADR-0017-zensical-launchkit-publication-architecture.md).
The separate [ADR-0022](../decisions/ADR-0022-decisions-publication-composition.md)
proposal remains proposed. [ADR-0030](../decisions/ADR-0030-consumer-kit-assembly.md)
records this assembly/receipt proposal without supplying human acceptance.

Identity's older exported logo files still have no structured asset-rights
record in the legacy publication configuration. This work preserves that
unknown state and does not manufacture a v1 approval/license or replace those
immutable exports. The real root self-consumer source and final release/dogfood
acceptance remain recorded under [#98](https://github.com/egohygiene/identity/issues/98)
and tracker [G09](https://github.com/egohygiene/identity/issues/116).
The bounded [fixture receipt](../../renderer/fixtures/complete-kit/receipt.json)
records unchanged real Mantle inputs and independent native generations,
alongside explicitly synthetic minimal/expanded cases. Hosted renderer/browser
results belong to the exact reviewed PR head. Broad Docker/CI/refactoring and
final documentation reconciliation remain with #70/#80/#83.
