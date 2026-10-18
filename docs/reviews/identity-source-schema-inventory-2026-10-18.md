# Identity source-schema inventory — checkpoint 1

Reviewed source: `063a4c70fcaccc6c15393f28ac2aabe62b34e1e7` on 2026-10-18 UTC. Companion to the [field review](identity-fields-2026-10-18.md). This is a dated audit snapshot, not another schema or a promise that every declared field reaches every consumer.

## Reading the inventory

All checked-in schema files are classified below. Property tables cover the sixteen v0/v1 canonical source/profile schemas and the separate motion-policy schema. Creative exchange, generated/exchange models and publication composition are inventoried separately so their fields do not become brand-authoring requirements.

`R` means required within its containing object, not globally required for every project. Optional documents can require many fields once adopted. `O` means not listed in that object's `required` array; other conditional/semantic constraints still apply. Refs point to definitions in the named source schema. Pattern-based token names and foreign namespaced token extensions are dynamic; the finite named-property inventory does not enumerate their possible instances. JSON Schema acceptance, authoritative validator acceptance, generation, public selection and renderer use are distinct checks.

## Contract classification

| Contract | Role | SHA-256 at reviewed source |
| --- | --- | --- |
| [contracts/candidate-manifest.schema.json](../../contracts/candidate-manifest.schema.json) | Creative exchange port; not approved source by itself | `1f98f393940344b6a2a13b62a58eebb720ef8223a02c30dbda43998a29185338` |
| [contracts/handoff-manifest.schema.json](../../contracts/handoff-manifest.schema.json) | Creative exchange port; not approved source by itself | `908a7441acd59acea8fb5641f9e37a153e937d0a798b3ce208b4bcddb71725e4` |
| [contracts/profile.schema.json](../../contracts/profile.schema.json) | Canonical source/profile description | `e1067e03fb2d6d933e23d9c75665c9d0b2a2396e236e842ef1cef917413dc49e` |
| [contracts/project.schema.json](../../contracts/project.schema.json) | Canonical source/profile description | `2f30f5d88e436718e11223be24460588ba0a9d894dc721d47150d719902ceef4` |
| [contracts/v1/approvals.schema.json](../../contracts/v1/approvals.schema.json) | Canonical source/profile description | `bc958303fb359380d9042fc0e99949250d962e34c901307106f1f258bb67e301` |
| [contracts/v1/brand-guidance.schema.json](../../contracts/v1/brand-guidance.schema.json) | Generated package, projection, plan, or evidence exchange | `021fd3b4744091c33972f90199b09d8ee5b16bc4d345714466494592419cea46` |
| [contracts/v1/brand-kit-checksums.schema.json](../../contracts/v1/brand-kit-checksums.schema.json) | Generated package, projection, plan, or evidence exchange | `aed4679e4a6df91b42fd755e3237c060367e21067be9f2a616fef839fa76289a` |
| [contracts/v1/brand-kit-package.schema.json](../../contracts/v1/brand-kit-package.schema.json) | Generated package, projection, plan, or evidence exchange | `1eb70e3ac1c0e21e39a389b24c2c2e4e6116443db27b55b2e7b4ae443843f46c` |
| [contracts/v1/brand-kit-view-model.schema.json](../../contracts/v1/brand-kit-view-model.schema.json) | Generated package, projection, plan, or evidence exchange | `cdac2107d5b7fc4351dfcd03ca7183ec2aecb59542e5a7758be48882067075a4` |
| [contracts/v1/channel-registry-package-manifest.schema.json](../../contracts/v1/channel-registry-package-manifest.schema.json) | Generated package, projection, plan, or evidence exchange | `762e44ab74985898b247dae201bd9982aaa3913ec61732d342e3a23790c65b8f` |
| [contracts/v1/channel-registry-package.schema.json](../../contracts/v1/channel-registry-package.schema.json) | Generated package, projection, plan, or evidence exchange | `3be324d741e912ee6887034ac8dcb508d2d0dddc48fae4ea8baf838c648a652f` |
| [contracts/v1/channel-registry.schema.json](../../contracts/v1/channel-registry.schema.json) | Canonical source/profile description | `30cf2356110f6682184920dcaf9a840e06df061a6cb7fd8822acc0df22c425ba` |
| [contracts/v1/compiler-manifest.schema.json](../../contracts/v1/compiler-manifest.schema.json) | Generated package, projection, plan, or evidence exchange | `068f032c68d88083be80524cbd194430cf6fed6f8ede1538d8500de4fae76271` |
| [contracts/v1/compiler-plan.schema.json](../../contracts/v1/compiler-plan.schema.json) | Generated package, projection, plan, or evidence exchange | `933cfbd14e3d144721be5a40e9a940f8b72cf095c95c17ba786fc4cf0e561d2d` |
| [contracts/v1/design-context.schema.json](../../contracts/v1/design-context.schema.json) | Generated package, projection, plan, or evidence exchange | `49f9f6472ed52344c337601d4af03492552bd8e5ec440a6868d9be8ce4bbb7db` |
| [contracts/v1/design-references.schema.json](../../contracts/v1/design-references.schema.json) | Canonical source/profile description | `17274584539fc72fa4c1e9a3c8ab0f8617142958bdad7110e3dca04f2092f68d` |
| [contracts/v1/design-system-handbook.schema.json](../../contracts/v1/design-system-handbook.schema.json) | Generated package, projection, plan, or evidence exchange | `e3c7874c51725602caa3e6bb4c7baf7738a79448f501d1b77657d765921b3928` |
| [contracts/v1/design-system.schema.json](../../contracts/v1/design-system.schema.json) | Canonical source/profile description | `00c03c27b70e935b7fbd82820b08413c87e7cbfa35f167819ac5205519d64b1f` |
| [contracts/v1/diagnostics.schema.json](../../contracts/v1/diagnostics.schema.json) | Generated package, projection, plan, or evidence exchange | `0aa2b83f3e968ab0ce501f4d8a7255a4b3442f10def931db4ea468535519f1d5` |
| [contracts/v1/identity-experience-content.schema.json](../../contracts/v1/identity-experience-content.schema.json) | Publication composition; separately owned | `3ee5e05253990bfdcc66077cd49a6d0bae6cb6334b30f78a50962b4026e8565d` |
| [contracts/v1/identity-experience-publication.schema.json](../../contracts/v1/identity-experience-publication.schema.json) | Publication composition; separately owned | `daefd6e88a89da3ca21b57bfd34ac829ca8f3f69db1697a6dd3600c48343ac88` |
| [contracts/v1/mascot-package.schema.json](../../contracts/v1/mascot-package.schema.json) | Generated package, projection, plan, or evidence exchange | `d1410b94e92ac6754c559555a7c0618e76806ca5eeab492321b294b0e273fdec` |
| [contracts/v1/mascot.schema.json](../../contracts/v1/mascot.schema.json) | Canonical source/profile description | `7cee3a5ee8f9dcf483a639c6048fa431ca5af3d4ca7e5dacdb4f64f8e04d3604` |
| [contracts/v1/motion-policy.schema.json](../../contracts/v1/motion-policy.schema.json) | Engine policy; not a project-manifest field | `76f196287494d8da21cdd33c7b240c89d89e65154ee52af42f4ec7259905de95` |
| [contracts/v1/press-kit-package.schema.json](../../contracts/v1/press-kit-package.schema.json) | Generated package, projection, plan, or evidence exchange | `c1bf164882a18b9a632b4c44b8a20ce13f71950fc0be2b68b30f62e7e7698a7a` |
| [contracts/v1/press-kit-projection.schema.json](../../contracts/v1/press-kit-projection.schema.json) | Generated package, projection, plan, or evidence exchange | `6e9694957f43833f3be7cb8b2a3452f7a10c0c40feb32587c19ba38928bd4cfe` |
| [contracts/v1/press-kit.schema.json](../../contracts/v1/press-kit.schema.json) | Canonical source/profile description | `7cdeaaf93ad9fabfd7654c0c4b1ba0ef28931881b445255cdd469378355e89eb` |
| [contracts/v1/project.schema.json](../../contracts/v1/project.schema.json) | Canonical source/profile description | `2594d307fb644fe59b6dd06ef937872f0bc17a38536dcc4e1e0d452ad060015a` |
| [contracts/v1/provenance.schema.json](../../contracts/v1/provenance.schema.json) | Canonical source/profile description | `a876fe775cf16382ae85c74f79a8849c69a71a61faefd84380ebaefd412ea03b` |
| [contracts/v1/publication-architecture.schema.json](../../contracts/v1/publication-architecture.schema.json) | Publication composition; separately owned | `a8f35a07bd5664c610c3025b1412e389ab05758c1a1c3de6ee1605b560922f78` |
| [contracts/v1/quality-report.schema.json](../../contracts/v1/quality-report.schema.json) | Generated package, projection, plan, or evidence exchange | `f56782e280893fb54d6feb076612b75b402d00abe1ca31dfd7dca7d785d8c501` |
| [contracts/v1/repository-presentation-package-manifest.schema.json](../../contracts/v1/repository-presentation-package-manifest.schema.json) | Generated package, projection, plan, or evidence exchange | `b8b4961d2e03235219ea979b382ba4d022fb44512f7fc9279ea1eec08d5a2809` |
| [contracts/v1/repository-presentation-package.schema.json](../../contracts/v1/repository-presentation-package.schema.json) | Generated package, projection, plan, or evidence exchange | `54634bcd0040fd0f052df44590b53978d6ad420d98e31edb4dcf9487eefb116f` |
| [contracts/v1/repository-presentation.schema.json](../../contracts/v1/repository-presentation.schema.json) | Canonical source/profile description | `d505acfe4ca8b0cf53561539b961ec1d2f5a36839bcfe1131d6b710e5e7b506d` |
| [contracts/v1/social-surface-package-manifest.schema.json](../../contracts/v1/social-surface-package-manifest.schema.json) | Generated package, projection, plan, or evidence exchange | `111c9fbaea436acfdedc3776f1ebc2041e28f9b9efa0cfb081a419a7d3e32a03` |
| [contracts/v1/social-surface-package.schema.json](../../contracts/v1/social-surface-package.schema.json) | Generated package, projection, plan, or evidence exchange | `4302ed50221e7afd42b9442e933bc782a06d3d55aceb150d29e4721384541468` |
| [contracts/v1/social-surface-press-kit-handoff.schema.json](../../contracts/v1/social-surface-press-kit-handoff.schema.json) | Generated package, projection, plan, or evidence exchange | `b5d93df3a8009eb9567dae7529a0257d919d197fbfc67eaa23c92183e374d82d` |
| [contracts/v1/social-surfaces.schema.json](../../contracts/v1/social-surfaces.schema.json) | Canonical source/profile description | `4c50da3768c2df56534687adae431229d5fd8927b00bf2e4c7e85fd42b2d518f` |
| [contracts/v1/targets.schema.json](../../contracts/v1/targets.schema.json) | Canonical source/profile description | `b2a89d761933b437fabd2ee4e099a223221f6cc835ae0979c00d7021faa8557a` |
| [contracts/v1/tokens.schema.json](../../contracts/v1/tokens.schema.json) | Canonical source/profile description | `07046647158b32cd77d003aa0e57d2874185b5484ad6c2db4a75c573ca429430` |
| [contracts/v1/usage.schema.json](../../contracts/v1/usage.schema.json) | Canonical source/profile description | `3b16a5e38e9636d7e4855f8f0febe62f81a4eb9bbf580d3cbeac2e3b7796575f` |
| [contracts/v1/visual-motion-manifest.schema.json](../../contracts/v1/visual-motion-manifest.schema.json) | Generated package, projection, plan, or evidence exchange | `f12f46dea9cf68fecb82afbbf36057ce3a5b9cfbeba7d3dede071842981f194e` |
| [contracts/v1/voice.schema.json](../../contracts/v1/voice.schema.json) | Canonical source/profile description | `3d1022e0e5c7a4dfb5d561582172be196b27f1a71811d33c21ced0bc5b5b95b4` |

## contracts/project.schema.json

Source: [identity project specification](../../contracts/project.schema.json).

Object `#`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `schema` | R | constant `"identity.project/v0"` |
| `project` | R | object |
| `paths` | R | object |
| `profiles` | R | object |
| `sources` | R | object |
| `context` | O | object |

Object `#/properties/project`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | string |
| `display_name` | R | string; minLength=1 |
| `repository` | R | string |
| `tagline` | R | string; minLength=1 |

Object `#/properties/paths`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `output_root` | R | ref `#/$defs/relativePath` |
| `source_root` | R | ref `#/$defs/relativePath` |
| `brief` | R | ref `#/$defs/relativePath` |

Object `#/properties/profiles`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `enabled` | R | array; minItems=1 |
| `inapplicable` | O | array |

Object `#/properties/sources`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `approval` | R | constant `"human"` |
| `required` | R | array; minItems=1 |

Object `#/properties/context`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `files` | O | array |

Object `#/$defs/sourceRequirement`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `role` | R | ref `#/$defs/identifier` |
| `path` | R | ref `#/$defs/relativePath` |
| `format` | R | string; minLength=1 |
| `description` | R | string; minLength=1 |


## contracts/profile.schema.json

Source: [identity output profile](../../contracts/profile.schema.json).

Object `#`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `schema` | R | constant `"identity.profile/v0"` |
| `id` | R | string |
| `version` | R | string |
| `verified_at` | R | string (date) |
| `references` | R | array |
| `targets` | R | array; minItems=1 |

Object `#/$defs/target`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | string |
| `path` | R | string; minLength=1 |
| `format` | R | string; minLength=1 |
| `source_role` | R | string; minLength=1 |
| `description` | R | string; minLength=1 |
| `width` | O | integer; minimum=1 |
| `height` | O | integer; minimum=1 |
| `purpose` | O | string; minLength=1 |
| `maximum_bytes` | O | integer; minimum=1 |
| `required` | O | boolean |


## contracts/v1/project.schema.json

Source: [Identity v1 consumer project](../../contracts/v1/project.schema.json).

Object `#`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `$schema` | R | string |
| `schema` | R | constant `"identity.project/v1"` |
| `project` | R | object |
| `layers` | R | array; minItems=1 |
| `documents` | R | object |
| `directories` | R | object |
| `compatibility` | R | object |

Object `#/properties/project`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `displayName` | R | string; minLength=1 |
| `repository` | R | string |
| `tagline` | R | string; minLength=1 |
| `kind` | R | `"organization"`, `"product"`, `"repository"` |

Object `#/properties/documents`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `brief` | R | ref `#/$defs/relativePath` |
| `targets` | R | ref `#/$defs/relativePath` |
| `provenance` | R | ref `#/$defs/relativePath` |
| `approvals` | R | ref `#/$defs/relativePath` |
| `guidance` | R | object |
| `handbook` | O | object |
| `pressKit` | O | ref `#/$defs/relativePath` |
| `socialSurfaces` | O | ref `#/$defs/relativePath` |
| `channelRegistry` | O | ref `#/$defs/relativePath` |
| `repositoryPresentation` | O | ref `#/$defs/relativePath` |
| `mascot` | O | ref `#/$defs/relativePath` |

Object `#/properties/documents/properties/guidance`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `voice` | R | ref `#/$defs/optionalRelativePath` |
| `usage` | R | ref `#/$defs/optionalRelativePath` |

Object `#/properties/documents/properties/handbook`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `designSystem` | R | ref `#/$defs/relativePath` |
| `references` | R | ref `#/$defs/relativePath` |

Object `#/properties/directories`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `sources` | R | ref `#/$defs/relativePath` |
| `candidates` | R | ref `#/$defs/relativePath` |
| `references` | R | ref `#/$defs/relativePath` |

Object `#/properties/compatibility`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `acceptedSchemaMajor` | R | constant `1` |
| `migrationFrom` | R | array |

Object `#/$defs/layer`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `kind` | R | `"organization-defaults"`, `"product-override"` |
| `priority` | R | integer; minimum=0 |
| `tokens` | R | ref `#/$defs/relativePath` |
| `sha256` | R | ref `#/$defs/sha256` |


## contracts/v1/tokens.schema.json

Source: [Identity v1 DTCG token layer](../../contracts/v1/tokens.schema.json).

Object `#`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `$schema` | R | string |
| `$description` | O | string |
| `$extensions` | R | ref `#/$defs/extensions` |

Object `#/$defs/group`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `$type` | O | ref `#/$defs/tokenType` |
| `$description` | O | string |
| `$extensions` | O | ref `#/$defs/extensions` |
| `$deprecated` | O | union |

Object `#/$defs/token`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `$value` | R | schema-defined value |
| `$type` | O | ref `#/$defs/tokenType` |
| `$description` | O | string |
| `$extensions` | O | ref `#/$defs/extensions` |
| `$deprecated` | O | union |

Object `#/$defs/extensions`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `org.egohygiene.identity` | O | ref `#/$defs/identityExtension` |

Object `#/$defs/identityExtension`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `schema` | O | `"identity.tokens/v1"`, `"identity.token-extension/v1"` |
| `layer` | O | object |
| `override` | O | object |
| `contrast` | O | object |
| `typography` | O | object |
| `motion` | O | object |
| `provenance` | O | object |

Object `#/$defs/identityExtension/properties/layer`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | string; minLength=1 |
| `kind` | R | `"organization-defaults"`, `"product-override"` |
| `priority` | R | integer; minimum=0 |

Object `#/$defs/identityExtension/properties/override`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `reason` | R | string; minLength=1 |
| `approval` | R | string; minLength=1 |

Object `#/$defs/identityExtension/properties/contrast`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `intent` | R | `"background"`, `"foreground"`, `"decorative"` |
| `pairedWith` | R | array |
| `minimumRatio` | R | number; minimum=1; maximum=21 |

Object `#/$defs/identityExtension/properties/typography`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `license` | R | string; minLength=1 |
| `languages` | R | array; minItems=1 |
| `legibility` | R | string; minLength=1 |

Object `#/$defs/identityExtension/properties/motion`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `reducedMotion` | R | string; minLength=1 |

Object `#/$defs/identityExtension/properties/provenance`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `record` | R | string; minLength=1 |
| `approval` | R | string; minLength=1 |


## contracts/v1/targets.schema.json

Source: [Identity v1 target profile selection](../../contracts/v1/targets.schema.json).

Object `#`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `$schema` | R | string |
| `schema` | R | constant `"identity.targets/v1"` |
| `enabled` | R | array; minItems=1 |
| `inapplicable` | R | array |

Object `#/$defs/profile`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | string |
| `version` | R | string |


## contracts/v1/provenance.schema.json

Source: [Identity v1 asset provenance](../../contracts/v1/provenance.schema.json).

Object `#`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `$schema` | R | string |
| `schema` | R | constant `"identity.provenance/v1"` |
| `assets` | R | array |

Object `#/$defs/asset`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `path` | R | string; minLength=1 |
| `kind` | R | `"mark"`, `"imagery"`, `"illustration"`, `"font"`, `"reference"` |
| `sha256` | R | string |
| `license` | R | object |
| `origin` | R | object |
| `accessibility` | R | object |
| `usage` | R | object |
| `approval` | R | ref `#/$defs/identifier` |

Object `#/$defs/asset/properties/license`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `spdx` | R | string; minLength=1 |
| `status` | R | constant `"approved"` |
| `attribution` | R | string |

Object `#/$defs/asset/properties/origin`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `creator` | R | string; minLength=1 |
| `method` | R | `"first-party"`, `"commissioned"`, `"licensed"`, `"generated"` |
| `source` | R | string; minLength=1 |
| `capturedAt` | R | string (date-time) |

Object `#/$defs/asset/properties/accessibility`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `altText` | R | string; minLength=1 |

Object `#/$defs/asset/properties/usage`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `safeZone` | R | string; minLength=1 |
| `minimumSize` | R | string; minLength=1 |
| `restrictions` | R | array |


## contracts/v1/approvals.schema.json

Source: [Identity v1 human approval decisions](../../contracts/v1/approvals.schema.json).

Object `#`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `$schema` | R | string |
| `schema` | R | constant `"identity.approvals/v1"` |
| `decisions` | R | array |

Object `#/$defs/decision`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | string |
| `subject` | R | string; minLength=1 |
| `candidate` | R | string; minLength=1 |
| `status` | R | `"approved"`, `"rejected"`, `"superseded"` |
| `reviewedBy` | R | string; minLength=1 |
| `reviewedAt` | R | string (date-time) |
| `evidence` | R | string; minLength=1 |
| `supersedes` | R | union |
| `notes` | R | string |


## contracts/v1/voice.schema.json

Source: [Identity v1 brand voice guidance](../../contracts/v1/voice.schema.json).

Object `#`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `$schema` | R | string |
| `schema` | R | constant `"identity.voice/v1"` |
| `foundation` | R | ref `#/$defs/foundation` |
| `characteristics` | R | array; minItems=1 |
| `contexts` | R | array; minItems=1 |
| `localization` | R | ref `#/$defs/localization` |

Object `#/$defs/provenance`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `method` | R | `"human-authored"`, `"handoff-candidate"`, `"imported"` |
| `source` | R | string; minLength=1 |
| `capturedAt` | R | string (date-time) |

Object `#/$defs/governance`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `subject` | R | string; minLength=1 |
| `state` | R | `"candidate"`, `"approved"`, `"rejected"`, `"superseded"` |
| `visibility` | R | `"public"`, `"internal"` |
| `provenance` | R | ref `#/$defs/provenance` |
| `approval` | R | union |

Object `#/$defs/foundation`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `purpose` | R | string; minLength=1 |
| `positioning` | R | string; minLength=1 |
| `audience` | R | ref `#/$defs/nonEmptyStrings` |
| `personality` | R | ref `#/$defs/nonEmptyStrings` |
| `governance` | R | ref `#/$defs/governance` |

Object `#/$defs/characteristic`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `label` | R | string; minLength=1 |
| `description` | R | string; minLength=1 |
| `governance` | R | ref `#/$defs/governance` |

Object `#/$defs/message`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `text` | R | string; minLength=1 |
| `rationale` | R | string; minLength=1 |
| `governance` | R | ref `#/$defs/governance` |

Object `#/$defs/context`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `label` | R | string; minLength=1 |
| `audience` | R | string; minLength=1 |
| `intent` | R | string; minLength=1 |
| `tone` | R | string; minLength=1 |
| `characteristics` | R | ref `#/$defs/nonEmptyStrings` |
| `preferredVocabulary` | R | ref `#/$defs/nonEmptyStrings` |
| `avoidedLanguage` | R | ref `#/$defs/nonEmptyStrings` |
| `naming` | R | string; minLength=1 |
| `capitalization` | R | string; minLength=1 |
| `punctuation` | R | string; minLength=1 |
| `examples` | R | array; minItems=1 |
| `antiExamples` | R | array; minItems=1 |
| `governance` | R | ref `#/$defs/governance` |

Object `#/$defs/localization`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `sourceLanguage` | R | string |
| `supportedLanguages` | R | array; minItems=1 |
| `fallback` | R | string; minLength=1 |
| `governance` | R | ref `#/$defs/governance` |

Object `#/$defs/localization/properties/supportedLanguages/items`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `tag` | R | string |
| `coverage` | R | `"reviewed"`, `"partial"`, `"unsupported"` |
| `notes` | R | string |


## contracts/v1/usage.schema.json

Source: [Identity v1 brand usage guidance](../../contracts/v1/usage.schema.json).

Object `#`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `$schema` | R | string |
| `schema` | R | constant `"identity.usage/v1"` |
| `sections` | R | array; minItems=1 |
| `assets` | R | array; minItems=1 |
| `accessibility` | R | ref `#/$defs/accessibility` |
| `legal` | R | ref `#/$defs/legal` |

Object `#/$defs/provenance`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `method` | R | `"human-authored"`, `"handoff-candidate"`, `"imported"` |
| `source` | R | string; minLength=1 |
| `capturedAt` | R | string (date-time) |

Object `#/$defs/governance`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `subject` | R | string; minLength=1 |
| `state` | R | `"candidate"`, `"approved"`, `"rejected"`, `"superseded"` |
| `visibility` | R | `"public"`, `"internal"` |
| `provenance` | R | ref `#/$defs/provenance` |
| `approval` | R | union |

Object `#/$defs/rule`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `kind` | R | `"do"`, `"dont"` |
| `category` | R | `"mark"`, `"color"`, `"typography"`, `"imagery"`, `"illustration"`, `"mascot"`, `"motion"`, `"accessibility"`, `"legal"`, `"localization"` |
| `instruction` | R | string; minLength=1 |
| `rationale` | R | string; minLength=1 |
| `details` | R | ref `#/$defs/nonEmptyStrings` |
| `contexts` | R | ref `#/$defs/nonEmptyStrings` |
| `governance` | R | ref `#/$defs/governance` |

Object `#/$defs/section`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `title` | R | string; minLength=1 |
| `description` | R | string; minLength=1 |
| `rules` | R | array; minItems=1 |

Object `#/$defs/asset`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `label` | R | string; minLength=1 |
| `kind` | R | `"mark"`, `"wordmark"`, `"imagery"`, `"illustration"`, `"mascot"` |
| `path` | R | ref `#/$defs/relativePath` |
| `status` | R | `"active"`, `"legacy"` |
| `availability` | R | `"public"`, `"internal"`, `"blocked"` |
| `replacement` | R | union |
| `downloadName` | R | union |
| `notes` | R | string; minLength=1 |
| `governance` | R | ref `#/$defs/governance` |

Object `#/$defs/accessibility`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `summary` | R | string; minLength=1 |
| `rules` | R | ref `#/$defs/nonEmptyStrings` |
| `governance` | R | ref `#/$defs/governance` |

Object `#/$defs/thirdPartyLicense`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `name` | R | string; minLength=1 |
| `spdx` | R | string; minLength=1 |
| `attribution` | R | string; minLength=1 |

Object `#/$defs/legal`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `trademark` | R | string; minLength=1 |
| `copyright` | R | string; minLength=1 |
| `attribution` | R | string; minLength=1 |
| `thirdPartyLicenses` | R | array |
| `governance` | R | ref `#/$defs/governance` |


## contracts/v1/design-system.schema.json

Source: [Identity v1 reviewed design-system handbook source](../../contracts/v1/design-system.schema.json).

Object `#`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `$schema` | R | string |
| `schema` | R | constant `"identity.design-system-source/v1"` |
| `sections` | R | array; minItems=1 |
| `capabilities` | R | array; minItems=1 |

Object `#/$defs/provenance`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `method` | R | `"human-authored"`, `"handoff-candidate"`, `"imported"` |
| `source` | R | string; minLength=1 |
| `capturedAt` | R | string (date-time) |

Object `#/$defs/governance`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `subject` | R | string; minLength=1 |
| `state` | R | `"candidate"`, `"approved"`, `"rejected"`, `"superseded"` |
| `visibility` | R | `"public"`, `"internal"` |
| `provenance` | R | ref `#/$defs/provenance` |
| `approval` | R | union |

Object `#/$defs/principle`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `title` | R | string; minLength=1 |
| `guidance` | R | string; minLength=1 |
| `rationale` | R | string; minLength=1 |
| `appliesTo` | R | ref `#/$defs/nonEmptyStrings` |
| `governance` | R | ref `#/$defs/governance` |

Object `#/$defs/section`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `title` | R | string; minLength=1 |
| `summary` | R | string; minLength=1 |
| `principles` | R | array; minItems=1 |

Object `#/$defs/capability`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `label` | R | string; minLength=1 |
| `status` | R | `"declared"`, `"not-declared"`, `"unsupported"` |
| `owner` | R | `"identity"`, `"holon"`, `"consumer"` |
| `notes` | R | string; minLength=1 |
| `governance` | R | ref `#/$defs/governance` |


## contracts/v1/design-references.schema.json

Source: [Identity v1 reviewed design-system reference catalog](../../contracts/v1/design-references.schema.json).

Object `#`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `$schema` | R | string |
| `schema` | R | constant `"identity.design-reference-catalog/v1"` |
| `references` | R | array; minItems=1 |

Object `#/$defs/provenance`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `method` | R | `"human-authored"`, `"handoff-candidate"`, `"imported"` |
| `source` | R | string; minLength=1 |
| `capturedAt` | R | string (date-time) |

Object `#/$defs/governance`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `subject` | R | string; minLength=1 |
| `state` | R | `"candidate"`, `"approved"`, `"rejected"`, `"superseded"` |
| `visibility` | R | `"public"`, `"internal"` |
| `provenance` | R | ref `#/$defs/provenance` |
| `approval` | R | union |

Object `#/$defs/reference`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `url` | R | string |
| `capturedAt` | R | string (date-time) |
| `patterns` | R | array; minItems=1 |
| `decision` | R | `"adopt"`, `"adapt"`, `"reject"`, `"observe"` |
| `notes` | R | string; minLength=1 |
| `rights` | R | string; minLength=1 |
| `affectsCanonical` | R | boolean |
| `governance` | R | ref `#/$defs/governance` |


## contracts/v1/press-kit.schema.json

Source: [Identity v1 reviewed Press Kit and Media Kit source](../../contracts/v1/press-kit.schema.json).

Object `#`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `$schema` | R | string |
| `schema` | R | constant `"identity.press-kit-source/v1"` |
| `boilerplates` | R | array; minItems=2 |
| `facts` | R | array |
| `links` | R | array |
| `contacts` | R | array |
| `team` | R | array |
| `assets` | R | array |

Object `#/$defs/provenance`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `method` | R | `"human-authored"`, `"handoff-candidate"`, `"imported"` |
| `source` | R | string; minLength=1 |
| `capturedAt` | R | string (date-time) |

Object `#/$defs/governance`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `subject` | R | string; minLength=1 |
| `state` | R | `"candidate"`, `"approved"`, `"rejected"`, `"superseded"` |
| `visibility` | R | `"public"`, `"internal"` |
| `provenance` | R | ref `#/$defs/provenance` |
| `approval` | R | union |

Object `#/$defs/boilerplate`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `kind` | R | `"short"`, `"long"` |
| `text` | R | string; minLength=1 |
| `governance` | R | ref `#/$defs/governance` |

Object `#/$defs/fact`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `label` | R | string; minLength=1 |
| `value` | R | string; minLength=1 |
| `governance` | R | ref `#/$defs/governance` |

Object `#/$defs/link`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `label` | R | string; minLength=1 |
| `url` | R | string |
| `kind` | R | `"website"`, `"product"`, `"repository"`, `"documentation"`, `"support"`, `"social"`, `"other"` |
| `governance` | R | ref `#/$defs/governance` |

Object `#/$defs/contact`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `label` | R | string; minLength=1 |
| `kind` | R | `"email"`, `"url"`, `"other"` |
| `value` | R | string; minLength=1 |
| `notes` | R | string |
| `governance` | R | ref `#/$defs/governance` |

Object `#/$defs/teamMember`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `name` | R | string; minLength=1 |
| `role` | R | string; minLength=1 |
| `bio` | O | string; minLength=1 |
| `governance` | R | ref `#/$defs/governance` |

Object `#/$defs/asset`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `assetId` | R | ref `#/$defs/identifier` |
| `label` | R | string; minLength=1 |
| `notes` | R | string; minLength=1 |
| `governance` | R | ref `#/$defs/governance` |


## contracts/v1/social-surfaces.schema.json

Source: [Identity v1 social-surface projection source](../../contracts/v1/social-surfaces.schema.json).

Object `#`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `$schema` | R | string |
| `schema` | R | constant `"identity.social-surface-source/v1"` |
| `catalog` | R | ref `#/$defs/catalogLock` |
| `organizationDefaults` | R | array |
| `project` | R | object |

Object `#/properties/project`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `adopt` | R | array |
| `exclude` | R | array |
| `overrides` | R | array |

Object `#/$defs/catalogLock`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `path` | R | ref `#/$defs/relativePath` |
| `id` | R | string |
| `version` | R | string |
| `digest` | R | object |

Object `#/$defs/catalogLock/properties/digest`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `algorithm` | R | constant `"sha256-utf8-lf"` |
| `value` | R | ref `#/$defs/sha256` |

Object `#/$defs/governance`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `subject` | R | string; minLength=1 |
| `state` | R | constant `"approved"` |
| `visibility` | R | constant `"public"` |
| `provenance` | R | object |
| `approval` | R | ref `#/$defs/identifier` |

Object `#/$defs/governance/properties/provenance`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `method` | R | `"human-authored"`, `"imported"` |
| `source` | R | string; minLength=1 |
| `capturedAt` | R | string (date-time) |

Object `#/$defs/defaultSelection`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `surfaceId` | R | string |
| `sourceAssetId` | R | ref `#/$defs/identifier` |
| `copySource` | R | ref `#/$defs/copySource` |
| `linkSource` | R | ref `#/$defs/linkSource` |
| `governance` | R | ref `#/$defs/governance` |

Object `#/$defs/adoption`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `approval` | R | ref `#/$defs/identifier` |

Object `#/$defs/exclusion`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `reason` | R | string; minLength=1 |
| `approval` | R | ref `#/$defs/identifier` |

Object `#/$defs/override`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `sourceAssetId` | O | ref `#/$defs/identifier` |
| `copySource` | O | ref `#/$defs/copySource` |
| `linkSource` | O | ref `#/$defs/linkSource` |
| `reason` | R | string; minLength=1 |
| `approval` | R | ref `#/$defs/identifier` |


## contracts/v1/channel-registry.schema.json

Source: [Identity v1 organization channel registry source](../../contracts/v1/channel-registry.schema.json).

Object `#`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `$schema` | R | string |
| `schema` | R | constant `"identity.channel-registry-source/v1"` |
| `registry` | R | ref `#/$defs/registry` |
| `security` | R | ref `#/$defs/security` |
| `channels` | R | array |

Object `#/$defs/registry`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `version` | R | string |
| `owner` | R | string; minLength=1 |
| `reviewedAt` | R | string (date-time) |

Object `#/$defs/security`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `secretsStored` | R | constant `false` |
| `ownerReferenceKind` | R | constant `"role"` |
| `procedureLocation` | R | string; minLength=1 |

Object `#/$defs/channel`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `platform` | R | ref `#/$defs/platform` |
| `canonicalUrl` | R | union |
| `handle` | R | string/null; minLength=1 |
| `ownershipEntity` | R | string; minLength=1 |
| `verification` | R | ref `#/$defs/verification` |
| `lifecycle` | R | ref `#/$defs/lifecycle` |
| `audiencePurpose` | R | string; minLength=1 |
| `contentScope` | R | array; minItems=1 |
| `locale` | R | array; minItems=1 |
| `accessibility` | R | ref `#/$defs/accessibility` |
| `recoveryOwner` | R | string; minLength=1 |
| `badge` | R | ref `#/$defs/badge` |
| `governance` | R | ref `#/$defs/governance` |

Object `#/$defs/platform`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `label` | R | string; minLength=1 |

Object `#/$defs/verification`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `state` | R | `"unverified"`, `"pending"`, `"verified"`, `"not-applicable"` |
| `evidence` | R | union |

Object `#/$defs/lifecycle`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `state` | R | `"planned"`, `"reserved"`, `"active"`, `"unavailable"`, `"deprecated"`, `"impersonation-risk"` |
| `since` | R | string (date) |
| `notes` | R | string |

Object `#/$defs/accessibility`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `label` | R | string; minLength=1 |
| `contactNotes` | R | string |

Object `#/$defs/badge`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `approved` | R | boolean |
| `label` | R | string; minLength=1 |
| `icon` | R | ref `#/$defs/icon` |

Object `#/$defs/icon`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `source` | R | ref `#/$defs/httpsUrl` |
| `license` | R | string; minLength=1 |

Object `#/$defs/governance`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `subject` | R | string; minLength=1 |
| `state` | R | `"candidate"`, `"approved"`, `"rejected"`, `"superseded"` |
| `visibility` | R | `"public"`, `"internal"` |
| `provenance` | R | ref `#/$defs/provenance` |
| `approval` | R | union |

Object `#/$defs/provenance`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `method` | R | `"human-authored"`, `"imported"` |
| `source` | R | string; minLength=1 |
| `capturedAt` | R | string (date-time) |


## contracts/v1/repository-presentation.schema.json

Source: [Identity v1 repository-presentation source](../../contracts/v1/repository-presentation.schema.json).

Object `#`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `$schema` | R | string |
| `schema` | R | constant `"identity.repository-presentation-source/v1"` |
| `profile` | R | ref `#/$defs/profileLock` |
| `organizationDefault` | R | ref `#/$defs/selection` |
| `project` | R | object |

Object `#/properties/project`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `visibility` | R | `"public"`, `"internal"`, `"private"` |
| `override` | R | union |

Object `#/properties/project/properties/override/oneOf/1`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `bannerAssetId` | O | ref `#/$defs/identifier` |
| `altText` | O | ref `#/$defs/text` |
| `reason` | R | ref `#/$defs/text` |
| `approval` | R | ref `#/$defs/identifier` |

Object `#/$defs/profileLock`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `path` | R | ref `#/$defs/relativePath` |
| `id` | R | constant `"egohygiene.repository-presentation-profile/v1"` |
| `version` | R | string |
| `status` | R | `"proposed"`, `"active"`, `"deprecated"`, `"superseded"` |
| `owner` | R | constant `"egohygiene/hygiene"` |
| `repository` | R | constant `"https://github.com/egohygiene/hygiene"` |
| `commit` | R | ref `#/$defs/commit` |
| `digest` | R | object |

Object `#/$defs/profileLock/properties/digest`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `algorithm` | R | constant `"sha256-utf8-lf"` |
| `value` | R | ref `#/$defs/sha256` |

Object `#/$defs/selection`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `bannerAssetId` | R | ref `#/$defs/identifier` |
| `altText` | R | ref `#/$defs/text` |
| `fallbackText` | R | ref `#/$defs/text` |
| `license` | R | object |
| `bannerApproval` | R | ref `#/$defs/identifier` |
| `badgeApproval` | R | ref `#/$defs/identifier` |

Object `#/$defs/selection/properties/license`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `spdx` | R | string |
| `attribution` | R | ref `#/$defs/text` |


## contracts/v1/mascot.schema.json

Source: [Identity v1 mascot source](../../contracts/v1/mascot.schema.json).

Object `#`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `$schema` | R | string |
| `schema` | R | constant `"identity.mascot-source/v1"` |
| `id` | R | ref `#/$defs/identifier` |
| `name` | R | string; minLength=1 |
| `pronouns` | R | string; minLength=1 |
| `role` | R | string; minLength=1 |
| `status` | R | `"candidate"`, `"approved"`, `"rejected"`, `"retired"` |
| `character` | R | object |
| `meanings` | R | array; minItems=1 |
| `canonicalAsset` | R | object |
| `variants` | R | array; minItems=1 |
| `accessibility` | R | object |
| `usage` | R | object |
| `motion` | R | object |
| `license` | R | object |
| `approval` | R | ref `#/$defs/identifier` |

Object `#/properties/character`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `archetype` | R | string; minLength=1 |
| `traits` | R | array; minItems=3 |
| `silhouette` | R | string; minLength=1 |
| `face` | R | string; minLength=1 |
| `eyes` | R | object |
| `outfit` | R | string; minLength=1 |
| `emblem` | R | object |
| `prohibitedElements` | R | array |

Object `#/properties/character/properties/eyes`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `count` | R | integer; minimum=1; maximum=8 |
| `treatment` | R | string; minLength=1 |

Object `#/properties/character/properties/emblem`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `placement` | R | string; minLength=1 |
| `integrated` | R | constant `true` |

Object `#/properties/meanings/items`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `element` | R | string; minLength=1 |
| `meaning` | R | string; minLength=1 |

Object `#/properties/canonicalAsset`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `assetId` | R | ref `#/$defs/identifier` |
| `path` | R | ref `#/$defs/relativePath` |
| `sha256` | R | ref `#/$defs/sha256` |
| `mediaType` | R | `"image/png"`, `"image/svg+xml"` |

Object `#/properties/variants/items`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `id` | R | ref `#/$defs/identifier` |
| `role` | R | string; minLength=1 |
| `aspectRatio` | R | string |
| `crop` | R | string; minLength=1 |
| `minimumWidth` | R | integer; minimum=1 |
| `altText` | R | string; minLength=1 |

Object `#/properties/accessibility`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `altText` | R | string; minLength=1 |
| `decorativeAlt` | R | constant `""` |
| `neverSoleCarrier` | R | constant `true` |

Object `#/properties/usage`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `safeZone` | R | string; minLength=1 |
| `backgrounds` | R | string; minLength=1 |
| `do` | R | ref `#/$defs/nonEmptyStrings` |
| `dont` | R | ref `#/$defs/nonEmptyStrings` |

Object `#/properties/motion`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `status` | R | `"not-declared"`, `"optional"`, `"declared"` |
| `default` | R | string; minLength=1 |
| `reducedMotion` | R | string; minLength=1 |
| `restrictions` | R | ref `#/$defs/nonEmptyStrings` |

Object `#/properties/license`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `spdx` | R | string; minLength=1 |
| `attribution` | R | string; minLength=1 |
| `trademark` | R | string; minLength=1 |


## contracts/v1/motion-policy.schema.json

Source: [Identity v1 motion policy](../../contracts/v1/motion-policy.schema.json).

Object `#`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `$schema` | R | string |
| `schema` | R | constant `"identity.motion-policy/v1"` |
| `durationsMs` | R | object |
| `assetBytes` | R | object |
| `maximumFrameRate` | R | number |
| `maximumDimensionPixels` | R | integer; minimum=1 |
| `allowedAnimatedProperties` | R | array; minItems=1 |
| `allowedEasing` | R | array; minItems=1 |
| `allowedNetworkModes` | R | array; minItems=1 |

Object `#/properties/durationsMs`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `microInteraction` | R | integer; minimum=0 |
| `transition` | R | integer; minimum=0 |
| `landingSequence` | R | integer; minimum=0 |
| `continuousStatus` | R | integer; minimum=0 |
| `demoCapture` | R | integer; minimum=0 |

Object `#/properties/assetBytes`:

| Named property | Presence | Declared shape |
| --- | --- | --- |
| `microInteraction` | R | integer; minimum=1 |
| `transition` | R | integer; minimum=1 |
| `landingSequence` | R | integer; minimum=1 |
| `continuousStatus` | R | integer; minimum=1 |
| `demoCapture` | R | integer; minimum=1 |
| `staticImagery` | R | integer; minimum=1 |

## Snapshot totals

43 contract schemas classified; 17 property inventories; 530 named property declarations (including reused governance/type definitions). This count measures schema declarations, not independent questions for an identity author.
