# Identity documentation

Choose a guide for the work you are doing. Commands in the usage and development
guides run from the checkout root; consumer paths remain explicit.

| Work | Guides |
| --- | --- |
| Understand the product | [Overview, preview and capabilities](OVERVIEW.md), [architecture](../ARCHITECTURE.md), [system responsibilities](../SYSTEM.md) |
| Author a project's identity | [Authoring worksheet](consumers/AUTHORING.md), [v1 examples](../examples/v1/README.md), [explicit v1 initializer](consumers/V1_INITIALIZATION.md), [field review](reviews/identity-fields-2026-10-18.md) |
| Adopt and generate | [Adoption](consumers/ADOPTION.md), [CLI and optional projections](USAGE.md), [complete Brand Kit](consumers/COMPLETE_BRAND_KIT.md) |
| Select optional outputs | [Presentation profiles](consumers/PRESENTATION_PROFILES.md), [launch documents](consumers/LAUNCH_DOCUMENTS.md), [outreach email and social kits](consumers/OUTREACH_KITS.md), [visuals](consumers/OPTIONAL_VISUALS.md) |
| Integrate other tools | [Initialization and validation handoffs](consumers/INITIALIZATION_AND_VALIDATION_HANDOFFS.md), [product component scope](consumers/PRODUCT_DESIGN_SYSTEM_SCOPE.md) |
| Develop and inspect | [Development setup and Task commands](DEVELOPMENT.md), [compiler/packages/evidence](IMPLEMENTATION.md), [renderer](../renderer/README.md), [validator modules](../scripts/identity_validation/README.md) |
| Qualify and recover | [Browser environment](BROWSER_ENVIRONMENT.md), [quality contract](contracts/QUALITY_GATES_V1.md), [consumer recovery](consumers/RECOVERY.md) |
| Release and publish | [Release process](releases/RELEASE_PROCESS.md), [next-release distribution matrix](releases/NEXT_RELEASE_MATRIX.md), [v1 release guide](releases/V1.md), [Brand Kit publication](publication/IDENTITY_PAGES.md), [native publisher source handoff](publication/NATIVE_V1_DRAFT.md), [product experience](../experience/README.md) |
| Follow decisions and work | [Decision index](decisions/README.md), [roadmap](../ROADMAP.md), [current source closeout](work/116/SOURCE_CLOSEOUT_2026-11-14.md), [owner questionnaire](work/98/QUESTIONNAIRE.md), [owner packet](work/98/OWNER_PACKET.md), [qualification handoff](work/83/QUALIFICATION_HANDOFF.md), [continuity checkpoint](../CONTINUITY.md) |

## Versioned contracts

| Area | Specification |
| --- | --- |
| Source and guidance | [Identity v1](contracts/IDENTITY_V1.md), [guidance](contracts/GUIDANCE_V1.md), [design-system handbook](contracts/DESIGN_SYSTEM_V1.md) |
| Source identity | [Canonical source digest](contracts/SOURCE_DIGEST_V1.md) |
| Compilation and output | [Compiler](contracts/COMPILER_V1.md), [Brand Kit packages](contracts/BRAND_KIT_PACKAGES_V1.md), [Brand Kit renderer](contracts/BRAND_KIT_RENDERER_V1.md) |
| Optional presentation | [Press and Media Kits](contracts/PRESS_KIT_V1.md), [social surfaces](contracts/SOCIAL_SURFACES_V1.md), [repository presentation](contracts/REPOSITORY_PRESENTATION_V1.md) |
| Channel governance | [Channel registry](contracts/CHANNEL_REGISTRY_V1.md) |
| Visual assets and evidence | [Mascot system](contracts/MASCOT_SYSTEM_V1.md), [visual motion](contracts/VISUAL_MOTION_V1.md), [quality gates](contracts/QUALITY_GATES_V1.md) |

The source contract owns normative fields and compatibility. Guides explain how
to use them; generated examples and current source do not imply that a selected
release contains every later feature. See the [capability snapshot](OVERVIEW.md#current-capability-state)
and the exact source/release evidence before choosing a tool revision.
