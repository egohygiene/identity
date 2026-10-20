# Identity v1 authoring worksheet

Use this worksheet to gather reviewed facts and put each fact in its canonical
home. It complements the [adoption workflow](ADOPTION.md), the
[source contract](../contracts/IDENTITY_V1.md), and the
[field review](../reviews/identity-fields-2026-10-18.md); it does not introduce
another profile or fact catalog. Paths below use the examples' topology. The
manifest may select other normalized repository-relative paths.

## Select the implementation before authoring

The nullable-guidance behavior and examples in this worksheet are the #99
checkpoint 2 implementation, **after the published `v1.0.0` release**. Pin the
exact reviewed Identity implementation commit, build its locked compiler, and
use scripts and schemas from that same commit. Record the commit and consumed
script digests in the consuming repository's toolchain configuration. Installing
the published `v1.0.0` binary does not provide this behavior, even when a source
document says `identity.project/v1`.

| Identifier | What to record | Who supplies it |
| --- | --- | --- |
| Source schema family | `schema: "identity.project/v1"` and `compatibility.acceptedSchemaMajor: 1` | Contract constant; not a tool release |
| Implementation | Immutable reviewed Identity commit; same-commit scripts and schemas | Integration owner |
| Selected profiles | `enabled[].id` and exact `enabled[].version`, such as `core` / `1.0.0` | Consumer selects supported versions |
| Layer and asset pins | SHA-256 of the actual reviewed local file bytes | Tooling computes them |
| Source identity | Canonical source digest in generated evidence | Producer computes it; not a human brand version |
| Consumer software version | Existing release metadata in the consumer repository | Consumer release process; no new manifest field |

Confirm the implementation commit against the consuming PR's reviewed pin
before executing the commands below. A successful build or a still-unchanged
Cargo package version is not evidence that the checkout is the published tag.

## 1. Gather intent and choose outputs

Have the identity owner supply the public name, stable ID, repository, tagline,
kind, intended users, product boundary, approved defaults, and actual surfaces.
Have the rights/review owners supply approved masters, source records, license
terms, accessibility and usage constraints, and decision evidence. Compute
digests from those bytes; do not ask the owner to invent checksums, review dates,
licenses, accounts, or approval-shaped placeholders.

Keep creative rationale and unresolved questions in `.identity/brief.md`.
Point from that brief to structured approved records as they are adopted; use
the structured home below for reusable facts. Unresolved creative work belongs
in the declared candidates directory, and inspiration belongs in references.
Neither becomes approved source through a copy, build, test, or merge.

Choose the smallest useful set of target profiles before preparing exports.
The examples select `core`, `tokens`, and `metadata`, each at `1.0.0`.
They explicitly mark `web`, `pwa`, `github`, `docs`, `social`, and `archive`
inapplicable. This is an example selection, not a universal repository policy.
Additional enabled profiles determine additional supported source/output needs;
an archive exists only when its profile is selected and generation succeeds.

## 2. Fill the executable core

`H` below means human-supplied or human-reviewed facts, `I` means a reviewed
local inherited snapshot, and `D` means a mechanically derived value. Required
means required within the named document. Optional documents can have strict
requirements once adopted. Schemas define the full closed shape; the worksheet
identifies the authoring choices rather than duplicating every declaration.

| Exact source location | Type and presence | Origin | Validation, governance, and consumer |
| --- | --- | --- | --- |
| `.identity/identity.json` → `project.id` | Required kebab-case identifier string | H | Stable joins across package/project evidence; choose before adoption |
| `project.displayName`, `project.tagline` | Required nonempty strings | H | Public project metadata and renderer copy; review their public meaning |
| `project.repository` | Required HTTPS URL string | H | Public repository metadata; use the actual canonical repository |
| `project.kind` | Required `organization`, `product`, or `repository` | H | Project classification in source/package consumers |
| `documents.brief`, `documents.targets`, `documents.provenance`, `documents.approvals` | Required local path strings | H | Each referenced document must exist and validate; named files below |
| `documents.guidance.voice`, `documents.guidance.usage` | Both keys required; each a local path string or `null` | H | `null` explicitly adopts no document of that kind; a configured path invokes its full strict contract |
| `directories.sources`, `directories.candidates`, `directories.references` | Required local directory path strings | H | Distinct trust zones; local portable paths and regular files, without links/reparse points |
| `compatibility.migrationFrom` | Required unique string array; `[]` for no migration | H | Record actual prior schema provenance, not guessed history |
| `layers[].{id,kind,priority,tokens,sha256}` | Required identifier, `organization-defaults`/`product-override` kind, nonnegative integer, local path, 64-character lowercase digest | I/H/D | Organization snapshots precede exactly one final product override; priorities are unique and ascending; validate all pins offline |
| `.identity/targets/profiles.json` → `enabled[].{id,version}`, `inapplicable` | Required nonempty profile array and unique string array | H | Exact supported versions; no profile may be both enabled and inapplicable; selected profiles drive generated output |
| `.identity/governance/provenance.json` → `assets[].{id,path,kind,sha256}` | Required per adopted asset: identifier, path, `mark`/`imagery`/`illustration`/`font`/`reference` kind, digest | H/D | Byte identity and source role; the current built-in core uses asset ID `mark` for its mark input |
| `assets[].license.{spdx,status,attribution}` | Required strings; status is `approved`; attribution may be empty only when appropriate | H | Supply actual artwork/font rights; the repository's software license alone supplies no blanket trademark permission |
| `assets[].origin.{creator,method,source,capturedAt}` | Required strings; method enum and actual date-time | H | Preserve real first-party, commissioned, licensed, or generated lineage in provenance evidence |
| `assets[].accessibility.altText`, `usage.{safeZone,minimumSize,restrictions}` | Required nonempty alt/safe-zone/minimum-size strings and restriction array | H | Asset guidance and accessibility intent; prose constraints are not inferred numeric output guarantees |
| `assets[].approval` | Required decision identifier | H | Resolves to an approved decision for the same asset subject |
| `.identity/governance/approvals.json` → `decisions[]` | Required array; entries require identifier `id`, strings `subject`, `candidate`, `reviewedBy`, `evidence`, `notes`, actual date-time `reviewedAt`, `approved`/`rejected`/`superseded` status, ID-or-null `supersedes` | H | Actual human decisions; subject/status must match the governed material. Notes may be empty; required identity/evidence strings may not |

Every non-documentation file under the approved sources directory needs
provenance. Keep a pinned organization-default token file and a final product
token file even when the latter has no value overrides. These are DTCG token
documents with local layer metadata. A replacement token requires
`$extensions.org.egohygiene.identity.override.{reason,approval}`; the decision
must cover that token subject. Compute and update the layer pin only after
reviewing the actual changed snapshot. Local token layers do not inherit copy,
artwork, accounts, or an arbitrary remote parent identity.

Both guidance values can be `null`, or one can be configured independently.
Absence is not an approved empty voice or a substitute for usage permission.
The normalized guidance projection represents missing voice singletons as
`null` and collections as empty; missing usage similarly has empty collections
and withheld singletons. A requested context must exist in adopted voice
source. Consumers must handle absence instead of supplying invented guidance.

## 3. Adopt rich copy and usage when needed

Do not add `shortName`, audience, positioning, or description fields to the
closed project manifest. Its current fields remain the public identity source.
Use the existing governed homes when a consumer needs richer material:

| Exact source location | Type and presence | Origin and approval | Public/review consumer |
| --- | --- | --- | --- |
| `.identity/guidance/voice.json` → `foundation.{purpose,positioning}` | Required nonempty strings when voice is adopted | H; foundation governance covers the bundle | Approved/public foundation in guidance packages and renderer |
| `foundation.{audience,personality}` | Required nonempty unique string arrays when adopted | H; same foundation governance | Same foundation, with no competing audience/positioning catalog |
| `characteristics[]` | Required nonempty array of IDs, labels, descriptions, governance | H; governed characteristic records | Context references and guidance projection |
| `contexts[]` → `naming`, `capitalization`, `punctuation` | Required nonempty strings per adopted context | H; context governance | Exact contextual writing/naming rules; no global short-name field is implied |
| `contexts[]` → `audience`, `intent`, `tone`, `characteristics`, `preferredVocabulary`, `avoidedLanguage`, `examples`, `antiExamples` | Required context-specific text and nonempty arrays; examples have their own governance | H; context and message approvals | Context-selected guidance; copied exactly rather than paraphrased by the renderer |
| `localization` → `sourceLanguage`, `supportedLanguages`, `fallback`, `governance` | Required when voice is adopted; language-tag strings and coverage records | H; record actual reviewed/partial/unsupported coverage | Public localization/fallback guidance; no implied translation approval |
| `.identity/guidance/usage.json` → `sections[].rules[]` | Required nonempty sections/rules when usage is adopted; rule IDs, do/don't kind, category, instruction, rationale, details, contexts, governance | H; per-rule governance | Rules filtered by context ID or explicit `all` |
| `assets[]` | Required nonempty array when usage is adopted; ID, label, kind, path, status, availability, replacement, downloadName, notes, governance | H; match existing source provenance/approval | Public guidance downloads require active/public/approved records; legacy assets require a replacement and separate labeling |
| `accessibility.{summary,rules,governance}` | Required summary string and nonempty rules array when adopted | H; governed bundle | Approved/public accessibility guidance |
| `legal.{trademark,copyright,attribution,thirdPartyLicenses,governance}` | Required strings, third-party-license array, governance when adopted | H; governed bundle; actual rights owners | Approved/public legal guidance; authoritative policy documents retain their owners |
| `.identity/guidance/press-kit.json` → `boilerplates[]` | Optional document; exactly one `short` and one `long` nonempty text record required for a public kit; at most one optional `paragraph` record | H; each has ID, kind, text, governance | Canonical supplied descriptions in the Press Kit projection, page, Markdown and ZIP |
| `facts`, `links`, `contacts`, `team`, `assets` in that Press Kit source | Required arrays in the adopted document; may be empty | H; each supplied record governed; assets reference existing `assetId` | Only affirmative reviewed facts/contacts/bios and explicitly selected public assets; absence stays explicit |
| `.identity/guidance/channel-registry.json`, selected by `documents.channelRegistry` | Optional document; follow its closed schema and contract | H; actual account lifecycle, verification and record governance | Authoritative social URLs/handles for registry, Press Kit and social consumers; do not duplicate registry social links in Press Kit source |

For the project profile, use these homes consistently:

| Supplied material | Authoritative home |
| --- | --- |
| Official name, tagline, repository | Project `displayName`, `tagline`, `repository` |
| Website and contact | Press Kit `links[]` with `kind: "website"` and `contacts[]` |
| Audience, positioning, personality | Voice `foundation` fields above |
| Short name, distinct mission statement, values, pronunciation | Optional Press Kit `facts[]`; choose an explicit human-readable label and exact approved value for each supplied fact |
| Purpose or mission already expressed by the approved purpose | Voice `foundation.purpose`; reuse it rather than maintaining a second version |
| Terminology and capitalization | The relevant voice context's `preferredVocabulary`, `avoidedLanguage` and `capitalization` |
| Official naming and unofficial-extension naming rules | The relevant context's `naming`; use governed usage rules for additional constraints |
| Practical voice examples | The relevant context's separately governed `examples[]` and `antiExamples[]` |

Fact IDs and labels do not select special renderer behavior: a supplied
"Short name" or "Pronunciation" fact appears under that exact label. The
renderer does not derive a mission, shorten a name, infer values, pronounce a
name, or grant unofficial extensions permission to use it. Owners must supply
the actual rule and its approval before that guidance appears publicly.

Use `short` for the supplied one-sentence description, optional `paragraph` for
a separately approved paragraph, and `long` for the longer description. These
are editorial labels, not sentence-count or length validators. Copy controls
reuse the projected text exactly; no description is generated from another.
An absent or withheld paragraph adds no placeholder. The optional paragraph
extension requires matching updated schemas, producer and renderer; older
pinned tools can reject it or omit it. See the
[Press Kit compatibility notes](../contracts/PRESS_KIT_V1.md#compatibility).

Every governed record includes
`governance.{subject,state,visibility,provenance,approval}`. Provenance supplies
`method`, `source`, and the actual `capturedAt` time. Candidates are internal
with `approval: null`; approved/rejected/superseded records need a matching
human decision for the same subject and state. Public projections recursively
select approved/public records and referenced decisions. Review projections
preserve the complete adopted lifecycle ledger. See the
[guidance contract](../contracts/GUIDANCE_V1.md) for exact envelope semantics.

The expanded example adopts one public voice context, public usage guidance,
and a Press Kit with short/long descriptions, a website, a media contact, and
the approved mark. Empty facts/team arrays demonstrate genuine optionality.
Its synthetic review and rights evidence is for exercising this example only;
it cannot approve real consumer copy, artwork, licenses, or people.

### Rights, policy references and font acquisition

Keep software licensing, trademark rules and third-party asset rights distinct.
The repository's software license is not blanket permission to reuse its name,
marks or fonts. Use the existing governed homes rather than copying policies
into a second catalog:

| Supplied material | Authoritative home and consumer behavior |
| --- | --- |
| Distributed asset rights, attribution, creator/source and restrictions | The asset's provenance `license`, `origin`, `usage` and `approval`; Press Kit reuses the rights and digest with its own asset-selection approval, while the core renderer carries the source approval |
| Trademark, copyright and third-party notices | Approved/public usage `legal.{trademark,copyright,attribution,thirdPartyLicenses}`; preserve supplied wording and the rights owner's authority |
| Software license, governance, Code of Conduct, security-reporting and contribution documents | Approved/public Press Kit `links[]` with `kind: "documentation"` or `"other"`, an explicit label and the authoritative HTTPS URL |
| Support/community destinations and official contacts | Approved/public Press Kit `links[]` and `contacts[]`; use `kind: "support"` where applicable and the channel registry for adopted social-account links |
| A font that consumers must acquire separately | An approved/public external Press Kit link, with a clear supplied label and explanatory usage/legal guidance where needed; the link is not a redistribution approval |
| Permissions that have not been established | An approved explanatory fact or guidance statement describing that uncertainty; do not invent an approved license or place unresolved bytes among selected public assets |

Link IDs and labels do not select policy semantics. The renderer preserves the
configured label and destination; it does not fetch, copy, verify or rewrite
the linked policy. Omit absent optional references. Changes to a policy or its
owner remain with that policy's existing repository or organization owner.

Canonical provenance requires `license.status: "approved"` and an actual
subject-matched asset decision. There is no invented `unresolved` license
status that makes unknown rights distributable. Keep acquisition-only fonts
outside local selected assets until the owner has approved the actual bytes,
license evidence and checksums. A font family name or provider URL supplies no
such approval; builds do not download fonts. The optional inspection/subsetting
adapters in [ADR-0007](../decisions/ADR-0007-font-tooling-boundaries.md) are not
implemented by this presentation work.

The separate legacy release publisher can have missing rights metadata. Its
page now exposes that absence rather than manufacturing a license or approval;
its existing archive selection is unchanged. This does not establish those
permissions or withhold the already-selected bytes. See the
[publication rights boundary](../publication/IDENTITY_PAGES.md#rights-metadata-and-release-selection).

## 4. Rehearse on a disposable copy

Start in the exact reviewed Identity source checkout identified by your pin.
The [authoring examples](../../examples/v1/README.md) include the executable
[minimal manifest](../../examples/v1/minimal/.identity/identity.json) and an
[expanded manifest](../../examples/v1/expanded/.identity/identity.json) adopting
the governed documents above. Neither is a substitute for the consumer's own
facts and decisions. Existing `tests/fixtures/v1/valid/minimal` remains a
historical regression fixture with additional optional material. Example
`$schema` editor paths resolve in this checkout; independent consumers should
point them to equivalent schema files from the same immutable source pin.

```bash
identity_source="$PWD"
consumer_root="$(mktemp -d)"
cp -R "$identity_source/examples/v1/minimal/." "$consumer_root/"

cargo build --locked --bin identity
python3 "$identity_source/scripts/validate_identity.py" \
  --repository-root "$consumer_root" \
  --format "human"
"$identity_source/target/debug/identity" v1-generate \
  --repository-root "$consumer_root"
"$identity_source/target/debug/identity" v1-verify \
  --repository-root "$consumer_root"
```

Use a fresh disposable directory to exercise the expanded source, then inspect
public guidance and generate the separately owned optional Press Kit:

```bash
consumer_root="$(mktemp -d)"
cp -R "$identity_source/examples/v1/expanded/." "$consumer_root/"
python3 "$identity_source/scripts/validate_identity.py" \
  --repository-root "$consumer_root" \
  --format "human"
"$identity_source/target/debug/identity" v1-generate \
  --repository-root "$consumer_root"
"$identity_source/target/debug/identity" v1-verify \
  --repository-root "$consumer_root"
python3 "$identity_source/scripts/render_guidance.py" \
  --repository-root "$consumer_root" \
  --format "json"
python3 "$identity_source/scripts/render_press_kit.py" \
  --repository-root "$consumer_root" \
  --output-directory "assets/identity/press-kit"
```

These commands write generated state only under the disposable consumer's
`assets/identity/`. The current `init` and `validate` CLI commands are v0
entry points; they do not initialize or validate this v1 authoring topology.
Use the standard-library source validator and the explicit `v1-*` commands.
Optional packages have their own projection and integrity checks; core
`v1-verify` does not establish that a separately generated Press Kit is current.

## 5. Record what the result proves

| Check | Evidence and limit |
| --- | --- |
| Valid source | Same-commit validator checks closed structure, local bytes/pins, references, rights and decision consistency. It cannot grant creative/legal approval or promise support by every producer. |
| Supported producer | The chosen adapter must accept every relevant source format/role and satisfy selected profiles. The [capability table](../contracts/IDENTITY_V1.md#source-authority-and-producer-capabilities) records the current SVG-only Rust core, which ingests all provenance assets; a valid PNG/font declaration is not proof it can produce that format. |
| Verified selected outputs | `v1-generate` plus `v1-verify` checks the core selected package state. Inspect its manifest and actual files; verify optional packages through their separate paths. |
| Public-kit readiness | Requires the real public selection, downloads, rights presentation, visual/accessibility review, and publication integration proof for that consumer. Passing the prior checks does not establish this. |

The audit's internal-asset exposure finding G03 and advertised-but-unselected
archive finding G04 remain implementation/regression work in #101/#105. Do not
infer safe generic public selection or a complete kit from these examples.
The [Mantle walkthrough](MANTLE_AUTHORING_PROOF.md) exercises this worksheet
against pinned real source. Its evidence and the [initialization/validation
handoffs](INITIALIZATION_AND_VALIDATION_HANDOFFS.md) supply checkpoint 3
evidence for review within its stated boundary; they establish no release or publication.

Adopt handbooks, channels, social surfaces, repository presentation, mascots,
supporting visuals, and templates only for a concrete consumer need under
their existing contracts and roadmap owners. Repository engineering files
such as `.gitattributes`, `.gitignore`, policy documents, and required-file
validation stay with repository policy/EgoLint; scaffolding and components
stay with Holon, shared agent instructions with Aether, reusable CI with Relay,
and installation/deployment with the consuming surface. They do not move into
`.identity/` merely because the repository adopts Identity.

Decision impact: **reference** ADR-0001, ADR-0012, ADR-0013 and ADR-0019 for human
creative authority, local pinned layers, lifecycle and immutable releases.
The worksheet explains those existing boundaries; it creates no new source
field, approval, release state, or architecture decision.
