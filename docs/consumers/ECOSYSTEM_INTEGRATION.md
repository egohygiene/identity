# Repository setup and contribution references

This handoff addresses [#108](https://github.com/egohygiene/identity/issues/108)
using the existing Identity source, policy links and offline commands. It adds
no repository scaffolder, policy-inheritance engine, DCO action or CLA service.

The 2026-11-02 [closeout review](../work/108/CLOSEOUT.md) verifies the pinned
owners, maps all eight acceptance criteria and records the concrete Mantle
handoff below. Actual installation, adapter implementation and current-source
runtime qualification retain their linked follow-ups.

## Owners and consumers

The inspected source revisions below bind ownership statements. A source
reference does not prove publication, installation, enforcement or adoption.

| Surface | Authoritative owner/source | Identity's boundary |
| --- | --- | --- |
| Approved project facts, defaults, overrides and public assets | Consumer-owned `.identity/`; [Identity v1](../contracts/IDENTITY_V1.md) | Validate and project selected source; keep project changes and approvals with its owner. |
| Portable skills, specifications and agent instructions | [Aether at dc8a168](https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/ARCHITECTURE.md) | Consume an explicitly selected compatible artifact. Do not copy instructions into brand facts or claim host discovery. |
| Tool admission, pinned installation and machine-local environments | [Realm at 0a3bbdc](https://github.com/egohygiene/realm/blob/0a3bbdc379b54db07dc5103887af0dfe05f97a0a/ARCHITECTURE.md) | Run Identity's existing commands. Realm owns acquisition, local paths and diagnostics; Identity does not install sibling source. |
| Reusable workflow execution, release adapters and evidence | [Relay at b4a88db](https://github.com/egohygiene/relay/blob/b4a88db20bc26f9ddefbee174baa8162cbe94ff2/ARCHITECTURE.md) | A consumer pins a compatible workflow/action and records actual results. Identity supplies artifacts and verification, not enforcement policy. |
| Repository structure, file materialization and initial templates | [Holon at a7734db](https://github.com/egohygiene/holon/blob/a7734dba83305276b12932fcd4ce348044d9a2e9/ARCHITECTURE.md) | Reuse an explicit reviewed profile. Contribution/security policy, root folders and issue/PR templates keep their owners. |
| Contribution attestation and trust policy | [Organization trust policy at ac2e403](https://github.com/egohygiene/.github/blob/ac2e4035173ed252d71d6655e723964ef93684df/TRUST_POLICY.md) | Link supplied authoritative policy. A reference or configured sign-off is not proof of a required check. |

The [initialization/validation handoff](INITIALIZATION_AND_VALIDATION_HANDOFFS.md)
already separates source validity, verified outputs and public-kit completeness.
Preserve those separate outcomes when composing these owners.

## Contribution-policy references

Reuse approved public Press Kit `links[]`, with an explicit label and
`kind: "documentation"` or `"other"`, for the repository's contribution guide,
security policy, Code of Conduct, license and issue/PR templates. Follow the
[existing authoring worksheet](AUTHORING.md#rights-policy-references-and-font-acquisition)
and the consumer's selected `documents.pressKit` path. A minimal source needs
neither a Press Kit nor a new folder convention.

Each link retains its actual source's reviewed governance/approval record,
exact supplied label and authoritative HTTPS URL. Prefer immutable file URLs
where reproducibility is required. An intentionally moving documentation URL
remains an owner choice recorded through existing governance. Do not generate
policy prose, manufacture approval or imply an unadopted organization policy
applies to a consumer. Policy changes stay with the linked owner.

The generated kit does not fetch a URL or check DCO/CLA enforcement. IDs and
labels activate no hidden policy behavior. Omit unknown references instead of
adding a compliance badge, invented policy or inferred permissions.

## DCO queue: unresolved, not duplicated

The pinned trust policy names Relay as the reusable DCO-check owner and
distinguishes piloting from required enforcement. Source inspection and GitHub
issue searches in `egohygiene/relay` for `DCO`, `sign-off`, `certificate` and
`contribution` did **not locate the specific queued DCO action** reported by the
project owner. Related contributor automation [Relay #3](https://github.com/egohygiene/relay/issues/3)
does not establish that implementation; no DCO action definition was located
in the inspected Relay source above.

The exact Relay issue/action link remains unresolved after the 2026-11-02
refresh: all 95 Relay issues (open and closed), the organization DCO search and
222 tracked Relay implementation/documentation files were inspected. This
bounded result is not proof the reported work never existed. #108 explicitly
permits an unresolved reference as its completion outcome.

[Sanctuary #8](https://github.com/egohygiene/sanctuary/issues/8) already tracks
the future governance catalog, including DCO checks and whether they should
graduate to Relay. It is a related existing follow-up, not the missing Relay
action or proof of enforcement. The policy definition in
[organization #9](https://github.com/egohygiene/.github/issues/9) is closed;
policy completion does not establish action availability. Reuse the existing
catalog work and retain the unresolved Relay reference instead of creating a
duplicate action. Do not substitute an unrelated check, add a contributor's
sign-off or change repository protections.
Later qualification must distinguish adoption mode, immutable action version,
actual check outcome and provider required-check settings.

CLA support remains optional future work requiring a concrete use case,
policy/legal owner, signing/data boundary and accountable delivery owner.
This checkpoint collects no signatures and proposes no signing service.

## Concrete Mantle consumer handoff

Use the existing real Mantle source at
[`b08045acc1e982dd9424c1d8c91b0badd64744e8`](https://github.com/egohygiene/mantle/tree/b08045acc1e982dd9424c1d8c91b0badd64744e8/.identity).
Its [manifest](https://github.com/egohygiene/mantle/blob/b08045acc1e982dd9424c1d8c91b0badd64744e8/.identity/identity.json)
already selects digest-bound organization defaults at priority 0 and Mantle's
product override at priority 10. This is the existing explicit override model.
Its [contribution guide](https://github.com/egohygiene/mantle/blob/b08045acc1e982dd9424c1d8c91b0badd64744e8/CONTRIBUTING.md)
and [license](https://github.com/egohygiene/mantle/blob/b08045acc1e982dd9424c1d8c91b0badd64744e8/LICENSE)
remain consumer-owned. This source declares no Press Kit or handbook; it
does not adopt new policy links, folders or templates through this example.

The retained [complete-kit receipt](../../renderer/fixtures/complete-kit/receipt.json)
records this source's two independent native generations and unchanged inputs
at its original checkpoint. The 2026-11-02 source inspection found all 14
consumed raw Git files still identical at Mantle main
`0f54fa6e100c5b86af64aa383e41eed8c64e363a`. This comparison is not a fresh
runtime pass or evidence that Realm/Relay installation has been exercised.

In a disposable checkout of that consumer, with one reviewed immutable
Identity implementation and its matching renderer dependencies already
provisioned, the handoff is:

1. Aether supplies selected compatible authoring/validation guidance. The
   existing [worksheet](AUTHORING.md) supplies the manual v1 source route;
   the current `identity init` still creates v0 source.
2. Realm supplies the executable and prerequisites through its selected
   environment. Missing versions or executables remain setup failures; an
   Identity validation command does not install tools.
3. Run the selected executable, using the consumer's existing output root:

   ```bash
   "$identity_bin" v1-generate --repository-root "$mantle_root"
   "$identity_bin" v1-verify --repository-root "$mantle_root"
   ```

4. From the matching Identity `renderer/`, assemble the native-only kit:

   ```bash
   corepack pnpm run build:kit -- \
     --artifact-root "$mantle_root/assets/identity" \
     --output-directory "$mantle_root/build/identity-kit"
   corepack pnpm run verify:kit -- \
     --output-directory "$mantle_root/build/identity-kit"
   ```

   `identity_bin` and `mantle_root` are caller-supplied paths. The output
   directory must be new or empty. No optional projection flags are supplied
   because this real source does not adopt those documents. A later reviewed
   Press Kit adoption can expose supplied policy references through existing
   governed links; it is not performed by this example.
5. A later consumer-owned Relay adapter may invoke the selected check-only
   interfaces and retain actual outcomes. Neither that adapter nor a new
   combined Realm/Relay execution was implemented or run in this closeout.

The commands above document existing interfaces for a later run. Original
receipt evidence retains its represented-source scope; all new runtime and
CI execution remains deferred under #70/#80.

Shared brand defaults retain existing content-addressed source and explicit
consumer overrides. This guide grants no implicit configuration inheritance.
Later Realm/Aether consolidation remains a bounded post-stabilization handoff,
not a mandatory fleet migration.

## Deferred work and existing queues

| Remaining outcome | Existing owner/queue |
| --- | --- |
| Explicit v1 initialization; preserve v0 and human-supplied facts | [Identity #133](https://github.com/egohygiene/identity/issues/133), newly separated from this completed coordination issue. |
| Released-tool installation and verified fallback selection | [Realm #19](https://github.com/egohygiene/realm/issues/19); existing projection/release/host acceptance remains [Realm #60](https://github.com/egohygiene/realm/issues/60). |
| Repository-default agent guidance and organization workspaces | [Aether #67](https://github.com/egohygiene/aether/issues/67), [Realm #26](https://github.com/egohygiene/realm/issues/26) and [Holon #41](https://github.com/egohygiene/holon/issues/41). |
| Delegated validation applicability, report/enforcement semantics and execution | [EgoLint #35](https://github.com/egohygiene/egolint/issues/35), [#36](https://github.com/egohygiene/egolint/issues/36) and [Relay #49](https://github.com/egohygiene/relay/issues/49); retain the [detailed interface handoff](INITIALIZATION_AND_VALIDATION_HANDOFFS.md). |
| DCO workflow curation and owner handoff | [Sanctuary #8](https://github.com/egohygiene/sanctuary/issues/8); the exact reported Relay action remains explicitly unresolved. |
| Current native/browser/Docker/setup/CI proof and final docs | Identity #70/#80/#82/#83; no new duplicate quality tracker. Shared development-environment consolidation stays in #70's deferred Realm/Aether design. |

CLA support has no selected consumer or implementation requirement. Preserve
it as an optional future owner decision rather than creating a signing service
or speculative issue. This closeout does not add the deferred queues as new
hard prerequisites for the current usable kit or remaining #106/#107 choices.

ADR not required: this applies existing projection and cross-owner boundaries
without adopting policy or changing an interface.
