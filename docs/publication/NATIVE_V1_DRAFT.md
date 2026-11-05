# Native v1 release-publication draft

This is unqualified source under [draft PR139](https://github.com/egohygiene/identity/pull/139),
not a selected release configuration or deployment. The existing
[publication path](IDENTITY_PAGES.md) and exact `v1.0.0` compatibility mapping
remain selected and unchanged. [ADR-0034](../decisions/ADR-0034-native-release-publication-input.md)
is proposed; tests/CI and actual source-to-publication qualification are deferred.

## Input and release boundary

The explicit configuration discriminator is `sourceMode: "native-v1"` under
the existing `identity.public-brand-kit-config/v1` identity. Native
configuration contains publication choices only: `canonicalUrl`, `release`,
optional `assetBaseUrl`, `browserAssets`, `openGraphImage`, and `nativeInputs`.
Project, tokens, assets, guidance and support are rejected as competing facts.

`release` contains `defaultTag` and `binding: "selected-annotated-tag"`.
It contains no guessed self-commit. The publisher still requires an actual
published stable release and annotated tag, resolves the exact commit and
creates the detached release source. Native config must be that release's
`publication/identity-brand-kit.config.json`. The verifier compares the checkout
HEAD with the selected commit and compares actual generated/config bytes to
that commit's Git blobs. A matching HEAD alone cannot bless dirty or untracked
release inputs. Legacy configs retain exact defaultTag/
defaultCommit matching; native compatibility fallbacks are rejected.

The builder requires explicit `--source-root`, `--release-tag` and
`--release-commit` for the native handoff. Its normal frozen-package invocation
remains `build:public`. `--output-directory` must select a new or empty directory
disjoint from all generated inputs. The existing publisher's clean `dist/`
destination follows that rule.

`assets/identity/` in the selected release must contain the unchanged native
compiler manifest and renderer output. Their project must be Identity and
their version must match the stable tag. `nativeInputs` can explicitly select
release-relative generated `designSystem` and/or `pressKit` directories. Both
retain existing same-project/source, public-selection and package verification.
CLI optional-directory arguments may not override those release-owned choices.
Canonical `.identity/` input, links escaping the release, and competing brand
facts cannot substitute for generated artifacts.

The existing `prepareKit` boundary selects the exact native and optional files.
No neighboring legacy export is copied because it happens to share the asset
directory. Publisher-owned CNAME, alias, manifest/archive/checksum and site paths
cannot collide with selected native output. The native model, compiler manifest
and original renderer output keep their bytes and lifecycle; a stable site
wrapper does not rewrite `generated` into `published` in native data.

## Digest and download meanings

| Field | Meaning |
| --- | --- |
| Native model/compiler `sourceDigest` | Existing canonical source digest from the v1 source contract |
| Public manifest/site `sourceDigest` | Existing NUL-framed inventory of declared paths and per-file SHA-256 values |
| Native public manifest/site `canonicalSourceDigest` | Explicit additional binding to the unchanged native model/compiler source digest |

Native publication inventory paths use the renderer's normalized bundle URL
spelling; ZIP members retain their actual filesystem names. Framing is over
the declared sorted inventory records. Legacy path spelling and archive bytes
are unchanged. Neither hash is a rights grant or a signature.

The download verifier checks the original compiler/model/byte binding and the
separate framed publication inventory. The site verifier reconstructs the
expected native/optional selection, checks exact file/hash equality, and
compares embedded and downloaded views. Public manifest/archive downloads are
verified independently of the unchanged native asset-package download.
Browser/OG selections must name actual verified native files; omitted entries
do not advertise invented browser or social artifacts.

## Release preparation still required

The [owner packet](../work/98/OWNER_PACKET.md) and its candidate configuration
are proposals. The real root source, rights, generated native/optional files,
compatible package version, release target and qualification do not yet exist
as one proven candidate. Select them before placing native configuration in a
release tree. Never use the incomplete source candidate or an arbitrary commit
as a published-release substitute.

Keep main's current legacy configuration and default release until an approved
rollout changes them. Existing Decisions collection/composition, CNAME and
compatibility routes retain their owners. Refresh the rollback record from the
preceding retained verified artifact before changing stable release bytes;
exercise rollback later rather than weakening the historical hash checks.

No production workflow was dispatched. A renderer/publication/ADR merge can
automatically deploy the existing site, so this PR stays draft until that
side effect is explicitly approved. Organization `/identity/` installation and
consumer repository writes require their independent owner approvals.

## Deferred acceptance

Prove unchanged legacy archive/model/site behavior; a real native self-consumer
round trip; optional omission and governed inclusion; wrong project/version/
commit/config denial; no competing brand facts; missing/extra/tampered files;
canonical versus inventory digest vectors; encoded paths and download bases;
no-clobber/confinement; immutable native bytes; static/keyboard/AX/visual
behavior; Decisions composition and actual approved deployment/rollback.
All runtime scenarios remain unrun in this source campaign.
