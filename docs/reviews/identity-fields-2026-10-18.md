# Identity fields — checkpoint 1 review

Issue: [#99](https://github.com/egohygiene/identity/issues/99). Reviewed source:
[`063a4c70fcaccc6c15393f28ac2aabe62b34e1e7`](https://github.com/egohygiene/identity/commit/063a4c70fcaccc6c15393f28ac2aabe62b34e1e7),
2026-10-18 UTC. Status: **audit complete; recommendations await review**.

This packet answers what belongs in an identity, where it is represented today,
and what must be resolved before repeatable authoring across repositories.
It changes no schema, validator, generated asset, approval or publication.
Recommendations below are review proposals, not newly enforced requirements.

The creative workflow can remain a conversation with a person or creative tool.
The consumer owns approved facts and artwork; Identity validates, resolves and
projects them. Mechanical identifiers, digests and output sizes should be
derived or selected by tooling wherever possible rather than becoming interview
questions. A single authoring worksheet can map to several existing documents.

## Review first

Five findings need explicit treatment before claiming a complete usable core:

1. The project JSON Schema allows null voice/usage paths, while the authoritative
   validator rejects them and the Rust loader requires files. Decide actual
   optionality and keep schema, diagnostics and generation aligned.
2. A synthetic PNG provenance entry passes source validation but the current
   Rust bridge fails while decoding its bytes as UTF-8. Source-format validity
   and compiler support need an explicit shared boundary.
3. A generated view model advertises the Brand Kit ZIP even when the selected
   profiles omit `archive`; that target is absent from the generated tree.
4. The fixture's internal, superseded `legacy-wordmark` is excluded from public
   usage guidance but still enters the generic renderer's top-level asset list,
   including embedded SVG source. Public asset selection needs end-to-end proof.
5. `init` authors v0 TOML. Rich project copy, v1 authoring and delegated repository
   validation still need an explicit usable path.

These are source observations and temporary-consumer results, not claims about
the contents or behavior of a deployed site. The
[probe receipt](../evidence/identity-fields-checkpoint-1-2026-10-18.json)
retains synthetic cases and outcomes without local workspace paths. The
[schema inventory](identity-source-schema-inventory-2026-10-18.md) classifies all
43 checked-in schemas and lists every named property in 17 source/profile/policy
inventories. A schema declaration alone does not establish consumer support.

## Existing sources and interfaces

| Boundary | Actual role at the reviewed source | Authority and limit |
| --- | --- | --- |
| `.identity/identity.toml`; [v0 project schema](../../contracts/project.schema.json), [v0 profile schema](../../contracts/profile.schema.json) | Legacy project metadata, configured source roles, paths, context and target descriptions. `init`, `validate`, `plan` and `handoff` use this path. | Preserve supported v0 behavior; these commands do not initialize or validate the complete v1 JSON topology. |
| `.identity/identity.json`; [v1 project schema](../../contracts/v1/project.schema.json) | Project identity, local layer declarations, document/directory references and schema compatibility. | Consumer-owned source. Default topology is `.identity/`; declared paths obey the contract's repository-relative rules. |
| Referenced token, target, provenance, approval and guidance documents | Canonical structured brand data under their own closed contracts. | Local source and immutable organization snapshots; no mutable remote lookup is needed during validation. |
| [Authoritative validator](../../scripts/validate_identity.py) | Offline source validation with stable `identity.diagnostics/v1` records. | The stdlib implementation checks structure and semantic relationships; JSON Schema acceptance and this implementation can differ, as the probes show. |
| [V1 consumer bridge](../../src/v1_consumer.rs), [embedded preflight](../../src/v1_consumer/preflight.rs) | `V1ConsumerPipeline::load` runs source preflight; `v1-generate` produces selected packages and a renderer model; `v1-verify` checks selected output drift read-only. | Python 3.11+ is required by embedded preflight. The current bridge has narrower asset support than the source contract. |
| [Package profiles](../../src/brandkit/profiles.rs) | `core`, `web`, `pwa`, `github`, `docs`, `social`, `tokens`, `metadata`, `archive`, selected by ID/version. | These are implemented output profiles, not a new repository-class taxonomy. Named authoring presets could compose them later. |
| [Optional projection commands](../consumers/ADOPTION.md#6-add-optional-projections-deliberately) | Guidance, handbook/context, Press Kit, channel, social-surface, repository-presentation and mascot projections. | Separate explicit entry points; `v1-generate` does not automatically generate every configured optional package. CI must verify adopted packages too. |
| [Brand Kit renderer model](../../contracts/v1/brand-kit-view-model.schema.json), handbook/context, package indexes and checksums | Generated/exchange data consumed by renderers, packages and downstream sites. | Output fields are not additional facts for an author to fill in. Public visibility and release agreement must hold across these ports. |
| [Creative handoff](../../contracts/handoff-manifest.schema.json), [candidate manifest](../../contracts/candidate-manifest.schema.json), `studio-review` | Candidate exchange and review of a handoff against a release and supported plan. | A candidate or provider output is not approval. Preserve the existing v0/v1 and human-review distinctions. |
| Publication configuration and experience composition | Canonical URLs, release selection, routes, site content and installation/deployment inputs. | Publication owners retain their authority. Identity's root currently has generated assets and publication configuration but no tracked `.identity/` self-consumer source. |

The [adoption guide](../consumers/ADOPTION.md), [source contract](../contracts/IDENTITY_V1.md),
[package contract](../contracts/BRAND_KIT_PACKAGES_V1.md) and
[renderer contract](../contracts/BRAND_KIT_RENDERER_V1.md) remain normative for
their current supported boundaries. This review does not silently repair their
historical wording or replace them with a second source contract.

## Field catalog

Presence below describes current behavior, not desired future requiredness:
**R** = required at that boundary; **C** = required when that section/profile is
adopted; **O** = optional section/fact; **D** = derived or mechanically selected.
Coverage labels mean **covered**, **incomplete**, **optional**, or **owned
elsewhere**. Covered means a concrete source and consumer exist; it does not
claim that every renderer presents all details or that a fresh deployment was
verified. The appendix lists named properties, declared requiredness and type
references; the linked schemas own the complete constraints.

### Project, strategy and copy

| ID and fact | Current source and presence | Concrete consumer and coverage |
| --- | --- | --- |
| F01 Stable identifier and project kind | `project.id`, `project.kind` in `identity.json`; R, human-selected. | V1 bridge, profile/handbook metadata; **covered**. `kind` is organization/product/repository, not an asset-output preset. |
| F02 Official display name, repository and tagline | `project.displayName`, `project.repository`, `project.tagline`; R. | Compiler project, metadata and renderer; **covered** for these five metadata fields. Project metadata has no per-field approval/visibility envelope, so it must be public-safe. |
| F03 Short name, aliases and pronunciation | Contextual `voice.contexts[].naming` exists; no dedicated top-level `shortName`, alias or pronunciation field. | Contextual guidance projections exist; reusable profile/naming semantics are **incomplete**, #100. A `shortName` probe is rejected as an unknown field. |
| F04 One-sentence, paragraph and longer descriptions | Optional Press Kit `boilerplates[]` supplies exactly short/long kinds once adopted; voice `foundation.positioning` is a separate fact. | Press Kit renderer/Markdown; **incomplete** as a uniform reusable project-copy interface, #100. Do not duplicate positioning as a description without a deliberate meaning. |
| F05 Purpose, positioning, audience and personality | `voice.foundation.{purpose,positioning,audience,personality,governance}`; C. | Public/review guidance and handbook/context; **covered**. Reuse this authority rather than adding competing copies to the project manifest. |
| F06 Mission, values and principles | Purpose exists in voice; approved handbook principles and usage rules can express values in context. No separate generic mission/values catalog. | Handbook/context and guidance; **incomplete only for demonstrated distinct needs**, #100/#109. Decide whether an additional field has a separate consumer. |
| F07 Voice, contextual tone and terminology | `voice.characteristics[]`, `contexts[]` with audience, intent, tone, preferred/avoided language, naming, capitalization, punctuation, examples/anti-examples; C. | Guidance JSON/Markdown/HTML and handbook/context; **covered**. Existing governance accompanies authored records. |
| F08 Language and localization | `voice.localization` declares source language, supported languages/coverage/notes, fallback and governance; C. | Guidance and context; **covered** as guidance. This is not automatic translation or proof that every output is localized. |
| F09 Website, official contacts and reusable links | Governed Press Kit `links[]`/`contacts[]`; channel registry for actual social accounts. No manifest `website` or `contact` field. | Press Kit and channel projections; **incomplete** as a consistent project-profile reference, #100/#103. Choose one source per fact. |

### Foundations and approved artwork

| ID and fact | Current source and presence | Concrete consumer and coverage |
| --- | --- | --- |
| F10 Semantic tokens and aliases | DTCG groups/tokens, `$value`, inherited `$type`, descriptions/deprecation and namespaced extensions in pinned layer files; R for the compiler's nonempty resolved token model. | JSON/CSS/JS/TypeScript/Tailwind-compatible exports and renderer; **covered**. Structural token support does not mean every token kind has identical visual presentation. |
| F11 Colors, themes and contrast intent | Color/dimension/etc. token values; identity extension `contrast.{intent,pairedWith,minimumRatio}`; usage rules. | Token exports, renderer palette, quality harness, guidance; **covered foundations**, practical intended combinations and theme presentation remain #102. No new independent color catalog. |
| F12 Typography and font availability | Font family/weight/dimension/composite typography tokens; extension `typography.{license,languages,legibility}`; asset provenance and usage rules. | Token/docs exports and renderer samples; **incomplete** for a complete font-acquisition/hierarchy experience, #102. A provenance `kind: font` declaration is not proof the Rust bridge can package binary fonts. |
| F13 Organization defaults and product overrides | `layers[].{id,kind,priority,tokens,sha256}` plus root token-layer metadata; R. At least one organization-defaults layer and exactly one final product-override layer are enforced. | V1 merge/alias resolver and inheritance projections; **covered** for token inheritance. Full copy/artwork inheritance or arbitrary parent-identity loading is not implemented by this mechanism. |
| F14 Intentional override rationale | Token extension `override.{reason,approval}`; C when replacing inherited values. | Resolver, diagnostics, exported lineage and handbook inheritance; **covered**. Approval must match the token subject. |
| F15 Approved master assets and their identity | Provenance `assets[].{id,path,kind,sha256}`; C for referenced source assets. Current kinds include mark/imagery/illustration/font/reference. | Validator and optional asset selectors; Rust bridge currently reads all provenance sources as UTF-8 SVG; **incomplete**, #99/#101/#107. Asset ID is also used as the core compiler source role. |
| F16 Primary/compact/wordmark/monochrome/light/dark variants | Distinct provenance assets and usage `assets[]` kind/status/availability/path/replacement/downloadName/notes can describe variants. No general role/theme/relationship binding selects them across all profiles. | Current built-in core and icon profiles consume the `mark` role; generic renderer only assigns a generated source download to `mark`; **incomplete**, #101. New distinct compositions require approval rather than automatic invention. |
| F17 Export formats, dimensions and intended targets | V0 profile target dimensions; v1 enabled profile ID/version selects fixed compiler dimensions. Intrinsic SVG dimensions are read for display. | Core SVG; 32/64 PNG favicons; 192/512 PWA icons and 512 maskable icon; 1280×640 GitHub and 1200×630 social cards; **covered fixed profiles**, missing requested formats/variants belong to #101/#104. Every possible size is not a canonical source file. |
| F18 Clear space, minimum size and restrictions | Provenance `usage.{safeZone,minimumSize,restrictions}` plus governed usage rules; C. | Source validator and guidance. The Rust bridge reads but does not propagate this provenance usage object and sets numeric `safe_zone` to None; **incomplete** for consistent display/machine interpretation, #101. Do not reinterpret prose as a number. |
| F19 Accessibility and alternatives | Provenance `accessibility.altText`; governed usage accessibility rules; mascot-specific decorative/reduced-motion fields; C/O. | Renderer image alternatives, guidance and quality checks; **covered foundations**, verify each selected output/profile, #101/#102/#105. Automated checks do not establish creative suitability. |

### Governance, rights and distribution

| ID and fact | Current source and presence | Concrete consumer and coverage |
| --- | --- | --- |
| F20 Asset rights and attribution | Provenance `license.{spdx,status,attribution}`; usage legal trademark/copyright/attribution/third-party licenses; R/C. | Validation, renderer provenance, Press Kit and packages; **covered inputs**, complete presentation/authoritative references remain #103. A software LICENSE is not blanket artwork/trademark permission. |
| F21 Source lineage | Provenance `origin.{creator,method,source,capturedAt}` and asset `sha256`; R for assets. | Byte-integrity validation and provenance outputs; **covered**. Creators/rights are supplied facts; checksums are D; dates reflect actual events. |
| F22 Human decisions | `approvals.decisions[]` IDs, subject, candidate, status, reviewer, review time, evidence, supersedes and notes; R at this boundary. | Validator, token/asset/guidance selection and review history; **covered**. Candidates, generated content, a successful test and a merged PR cannot invent an approval. |
| F23 Lifecycle and public/internal selection | Governance subject/state/visibility/provenance/approval on guidance records; usage asset status/availability; C. | Public/review guidance and optional packages; **incomplete across generic assets**, see G03. The provenance record itself does not carry the same lifecycle envelope. |
| F24 Enabled and inapplicable output profiles | Targets document `enabled[].{id,version}`, `inapplicable[]`; R. At least one core compiler profile is enabled; profiles cannot be both enabled and inapplicable. | Planning/generation/verification; **covered**. Optional presentation profiles may be absent; that differs from an entirely empty core profile selection. |
| F25 Actual channels and account lifecycle | Channel registry owner/version/review date/security boundary; channel URLs/handles, verification, lifecycle, purpose, locale, accessibility, recovery-owner role, badges and governance; O/C. | Channel badges/footer, Press Kit and social handoffs; **optional, covered**. Identity records verified facts; owning account processes perform verification and recovery. No credentials belong in source. |
| F26 Platform artwork, package identifiers and discoverability | Social surfaces pin catalog facts, organization selections and project adoptions/exclusions/overrides; current project metadata is narrow. | Social-surface outputs and handoff; **optional existing mechanism**, registry IDs, keywords and richer copy selectors need bounded coverage review in #104. |
| F27 Policy and support references | Governed Press Kit links/contacts and usage legal guidance provide partial homes. | Press Kit/public kit; **incomplete**, #103/#108. Reference authoritative software, security, contribution and conduct policy; their content and enforcement remain with repository policy owners. |
| F28 Press Kit and team material | Boilerplates, facts, links, contacts, biographies and selected existing public assets; O, then C within the adopted source. | Press Kit JSON/Markdown/ZIP/manifest/checksums and renderer; **optional, covered**. Reuse canonical copy/channels rather than authoring competing facts. |

### Optional material and technical facts

| ID and fact | Current source and presence | Concrete consumer and coverage |
| --- | --- | --- |
| F29 Design guidance and external references | Handbook source sections/principles/capabilities; reference URLs, captures, observed patterns, decisions, rights and governance; O/C. | Handbook/context projections and optional renderer section; **optional, covered**. Component implementation and third-party usage rights retain their owners. |
| F30 Repository banner and badge presentation | Pinned repository-presentation profile, approved banner/alt/fallback/license selection, organization defaults and product override; O/C. | Presentation package; Holon/consumer installs README regions; **optional, covered**. Caller-supplied evidence is not conformance evaluated by Identity. |
| F31 Mascot identity | Name/pronouns/role, character/meanings, canonical asset, variants, accessibility, usage, motion, license and approval; O/C. | Mascot projection/package and selected public assets; **optional, covered with its own producer path**. Audit actual consumer format support before passing binary mascot sources through core generation. |
| F32 Imagery, illustrations, patterns and motion | Provenance/usage guidance, token motion extensions, mascot motion and separate `identity.motion-policy/v1` engine policy; O/C. | Existing quality/motion APIs and optional projections; **incomplete for unspecified new visual categories**, #107. Engine budgets are not automatically project-manifest fields. |
| F33 Launch, document and presentation templates | Approved kit data can feed a selected consumer template; there is no universal template-authoring object to require. | **Optional scope**, #106; consumer/tool ownership applies. Dates, feature claims and event facts come from the project. |
| F34 Schema, source identity and software versions | `$schema`/`schema`, `compatibility.acceptedSchemaMajor` and migration provenance; selected profile versions; D source digest and generated release/package metadata. | Validators, compiler and release-bound renderers; **covered distinct concepts**, clarify labels in #99. There is no independent human brand-version field in the manifest. Do not substitute the project's software version for source identity. |
| F35 Repository engineering and deployment | Git attributes/ignores, required repository docs, lint policy, component code, routes, credentials and release publishers. | **Owned elsewhere**. Repository policy/EgoLint can require and delegate valid identity evidence; Holon owns scaffolding. Publication/installation remains explicit. These files are not moved into `.identity/`. |

## Observed gaps and proposed handling

The IDs below identify review findings, not new contract identifiers. Checkpoint
2 selects a bounded subset after review; later kit work retains its existing
issues. Confirmed consumer-boundary failures need regression proof before
calling the complete kit ready, even if source-schema validation passes.

| Finding | Evidence and consequence | Proposed handling |
| --- | --- | --- |
| G01 Nullable guidance mismatch | `null-guidance`: project JSON Schema accepts both nulls; authoritative validation emits two IDN1003 errors. Rust `V1ConsumerPipeline::load` also expects paths. Existing source prose describes nullable guidance. | #99 checkpoint 2: choose and test compatible schema/validator/compiler semantics. Preserve already-supported documents; record any versioned migration needed. |
| G02 Raster/font source versus core bridge | `raster-source`: an additional governed PNG validates, then generation returns IDN3301 at UTF-8 decoding. `media_type` supports SVG only. This does not prove every binary format was tested. | Agree a source/producer capability table in #99; #101/#107 implement supported selected formats or useful preflight diagnostics. Do not force SVG-only source globally just to hide the compiler mismatch. |
| G03 Generic public-asset selection | Baseline usage marks `legacy-wordmark` internal/superseded; generic renderer `assets[]` includes it with embedded source. The adjacent public guidance filter does remove it. | Carry an explicit blocking regression into #101/#105, coordinated with the public-boundary contract established by #71. Review whether a dedicated repair checkpoint is needed before new asset fields. No deployed exposure is inferred. |
| G04 Advertised optional package absent | Baseline selects core/metadata/tokens and generates 13 projections. Renderer package catalog includes `packages/brand-kit/brand-kit.zip`; the file does not exist because archive was not selected. | #101/#105: derive advertised downloads from actual selected outputs and verify bytes/status, including optional absence. A URL returning a generic fallback page is insufficient. |
| G05 Rich project profile and copy authority | Manifest allows only id/displayName/repository/tagline/kind. `shortName` gets IDN1101. Voice foundation, Press Kit boilerplates and channel facts already cover overlapping meanings. | #99/#100: propose a small governed profile/copy addition or explicit references after reviewing existing homes. Avoid ungoverned duplicate audience/positioning/links. |
| G06 Asset role/theme and usage transport | Core profiles use `mark`, only that source gets a generated download path, and provenance usage strings are discarded by the Rust bridge's output adaptation. | #101: agree variant relationships/roles, supported sizes/formats and which existing constraints reach renderers. Add only fields needed by the first consumer. |
| G07 V1 authoring path | Source inspection: `init` writes `identity.toml`; `validate` checks v0. The existing `minimal` v1 fixture already adopts handbook/mascot and contains three assets. | #99 checkpoints 2/3: true minimal/expanded examples and an authoring worksheet. Scope a v1 initializer/CLI follow-up explicitly if examples do not make adoption sufficiently usable. |
| G08 Delegated repository validation | Identity exposes source diagnostics and core `v1-verify`; optional package verification has separate paths. This Identity backlog does not explicitly define the proposed EgoLint handoff. | #108/adoption follow-up: identify an immutable producer and report/execution contract with EgoLint; define absent, invalid, unsupported, stale and valid outcomes. Do not implement an EgoLint fork in this repository. |
| G09 Real self-adoption | No tracked root `.identity/` exists; root generated assets/publication configuration are not canonical v1 source. | #99 inventories existing approved source; #105/#98 establish actual self-consumer source and canary/release evidence without inventing copy, rights or approval. |

## Proposed required core and review decisions

Preserve today's supported documents while defining a small usable authoring
core. The existing baseline requires project metadata, topology, pinned token
layers, targets, provenance and approvals. The schema/runtime guidance mismatch
must be resolved before promising a smaller executable core. Unknown fields
currently fail; adding required fields or changing meaning can require a major
contract/migration rather than an optional v1 addition.

| Review decision | Recommendation for checkpoint 2 | Remains unresolved |
| --- | --- | --- |
| D01 What is universal? | Stable public project identity, explicit source/tool/profile selection, rights/approval for adopted public material, and enough supported source to satisfy selected outputs. | Whether voice/usage are executable optional sections or part of the required compiler core; G01. |
| D02 Where does rich copy live? | Reuse governed voice foundation and existing Press Kit/channel authorities; introduce only the missing reusable profile/naming/copy facts. | Exact document/field layout and approval granularity; G05. No new paths are reserved here. |
| D03 Which visual variants are required? | A selected output profile determines required roles/formats/dimensions. Keep approved masters/distinct compositions canonical and derive mechanical sizes. | First agreed repository/web/PWA needs and the role/theme mapping; G02/G06. Existing profile IDs remain intact. |
| D04 How do defaults work? | Retain local, digest-pinned token snapshots and explicit reviewed overrides. | Whether the first consumer needs non-token family defaults. Any addition must have a concrete source/consumer and preserve offline operation. |
| D05 How is completeness reported? | Separate valid source, supported producer capabilities, verified selected outputs, and public-kit readiness. Keep absent optional sections explicit. | Whether a dedicated machine completeness report is needed or existing diagnostics/manifests suffice; G07/G08. |
| D06 What is optional or external? | Opt in to Press Kit, channels, social surfaces, mascots, supporting visuals and templates. Keep engineering policy, reusable components and deployment with their owners. | Actual #106–#109 use cases and owner dispositions. Capturing a possibility does not make it required. |

Every field selected for checkpoint 2 needs a type/example, one canonical owner,
required/optional/profile-conditional status, human/inherited/derived origin,
public/review treatment, semantic validation and a named output consumer. Use
real omissions and diagnostics rather than approval-shaped placeholder facts.

## Checkpoints and completion boundary

| Checkpoint | Deliverable | Exit and current state |
| --- | --- | --- |
| 1 — Inventory and review | This field catalog, exact schema inventory, interface/consumer map, probe receipt and proposed decisions. | **Ready for review.** Catalog conclusions do not accept schema changes or authorize checkpoint 2 automatically. |
| 2 — Compatible contract and examples | Selected demonstrated gaps, aligned validation, true minimal/expanded fixtures, useful errors and guided authoring worksheet. | **Not started.** Preserve supported formats, entry points, approvals and source/public boundaries; use an ADR proposal where the chosen compatibility change requires one. |
| 3 — Authoring proof | Representative consumer walkthrough; supported output and optional-omission/public-selection proof; bounded initializer/EgoLint follow-ups and updated handoff. | **Not started.** This is authoring proof, not #105 complete-kit delivery, a creative approval, fleet rollout or publication. |

#78/#79/#77 still own transaction confinement, writers and recovery. #81/#80/#82
qualify setup/browser environments; #84 and final #83 reconcile maintenance and
documentation. #100/#103/#101/#102/#104/#105 assemble the usable kit, followed by
the bounded #85–#88 extractions and #106–#109 scope decisions. #98 retains final
self-dogfood, release and contrasting-consumer proof. #99 is the selected
current priority; this packet does not make unrelated ecosystem work a gate.

## Evidence and decision impact

The probe receipt was produced from a locked local Rust build of the reviewed
source and its stdlib validator. Five temporary consumers were copied from the
existing fixture; all retained identical canonical `.identity/` bytes before
and after validation/generation. Only synthetic test data was added. The
baseline and optional-document omission generate successfully; the individual
failures and missing targets are recorded separately, not hidden by that exit.

Reproduction recipe: build `identity` with `cargo build --locked --bin identity`;
copy `tests/fixtures/v1/valid/minimal` to a disposable consumer; run
`python3 scripts/validate_identity.py --repository-root "$consumer" --format "json"`
and, only on source success, `identity v1-generate --repository-root "$consumer"`.
For null guidance replace both declared guidance paths with null. For short name
add `project.shortName`. For optional omission remove `documents.handbook` and
`documents.mascot`. For the raster case add one local 1×1 PNG, matching digest,
imagery provenance and a synthetic approved decision for that asset ID. Inspect
the generated renderer model and compare advertised package paths with actual
files; compare top-level asset selection with usage availability/governance.
Use synthetic approval evidence, never a copied real person's approval.

Decision-impact operation: **reference**. Existing
[ADR-001](../decisions/ADR-001-creative-approval-human-owned.md),
[ADR-012](../decisions/ADR-012-local-layered-identity-v1.md),
[ADR-013](../decisions/ADR-013-preserve-guidance-lifecycle.md) and
[ADR-019](../decisions/ADR-019-immutable-release-contract.md) govern authority,
local source, lifecycle and release distinctions. This checkpoint inventories
evidence and presents choices without adopting a new source shape. Aether's
pinned decision-impact v2.0.0 and continuity v1.1.0 at
`8ef3bd34d5fec835da54eb8acd0d074b79ee8fe2` were applied under the repository's
existing Hygiene policy selection. Existing ADRs and their dispositions remain
unchanged; consequential checkpoint 2 choices receive their own review.
