# Issue #108 ecosystem handoff closeout — 2026-11-02

Scope: [Identity #108](https://github.com/egohygiene/identity/issues/108).
Reviewed Identity base: `d6864918c7303e9c277130528a3ecdf19cf70ea7`.
The maintainer authorized completing and closing this reference/ownership
handoff, with actual tests/CI and larger integration work deferred.

## Acceptance coverage

| Issue criterion | Completed bounded result |
| --- | --- |
| Sources, owners and consumers | The [integration guide](../../consumers/ECOSYSTEM_INTEGRATION.md#owners-and-consumers) records pinned Aether/Realm/Relay/Holon/trust sources and their Identity consumption boundaries. Their GitHub main revisions still match those pins. |
| Shared defaults and later repository configuration | Existing digest-bound organization defaults and explicit product overrides are illustrated by real Mantle source. Broader environment/default consolidation stays after stabilization in Identity #70 and existing Realm/Aether/Holon owner work. |
| Authoritative contribution, folder and template references | Existing governed Press Kit links can expose supplied policies; original documents and scaffolding stay with their owners. The real Mantle example links its actual contribution guide/license and invents no adopted templates or policy links. |
| Existing DCO queue linked or explicitly unresolved | The exact reported Relay issue/action remains explicitly unresolved after the bounded refresh below. This is an allowed criterion outcome. Sanctuary #8 is a related open catalog/owner-handoff queue, not the missing Relay implementation. |
| Reuse enforcement work | No new DCO action, sign-off, protection setting or duplicated policy is introduced. Reuse existing governance catalog work and the authoritative trust policy. |
| Policy references distinguished from enforcement | The guide uses existing governed link fields and explicitly separates a displayed link/configured policy from actual installation, adoption and required-check evidence. |
| CLA kept optional | No concrete consumer or signing/data owner is selected; CLA remains a future owner decision. No service or speculative issue is created. |
| Bounded example and actual override behavior | The [Mantle handoff](../../consumers/ECOSYSTEM_INTEGRATION.md#concrete-mantle-consumer-handoff) names the real source, priorities, output commands, omitted optional inputs and future Realm/Relay seams. Historical receipt scope and current source-only inspection remain separate. |

## Source and duplicate review

The live main revisions were checked through GitHub before editing:

- Aether: `dc8a16851f452763ef4f7fbe4bf057d4500b1921`.
- Realm: `0a3bbdc379b54db07dc5103887af0dfe05f97a0a`.
- Relay: `b4a88db20bc26f9ddefbee174baa8162cbe94ff2`.
- Holon: `a7734dba83305276b12932fcd4ce348044d9a2e9`.
- Organization trust policy: `ac2e4035173ed252d71d6655e723964ef93684df`.
- Mantle: `0f54fa6e100c5b86af64aa383e41eed8c64e363a`.

Relay issue pages 1 and 2 contain all 157 issue/PR entries, including 95
issues through #1. Neither their titles/bodies nor 222 tracked Relay
implementation/documentation files matched DCO/developer-certificate/sign-off
terms. The organization-wide DCO issue search returned eight related issues,
including existing Sanctuary #8 and the closed policy-definition issue
egohygiene/.github#9. Relay #3 is closed label/contributor automation and does
not establish DCO implementation. This is bounded absence evidence, not proof
that the reported work never existed or approval to replace it.

Initializer duplicate searches for `initializer` and `v1-init` in Identity
found only the historical #99 and coordinating #116. The requirements in the
[existing handoff](../../consumers/INITIALIZATION_AND_VALIDATION_HANDOFFS.md)
still routed future work through #108, so new
[#133](https://github.com/egohygiene/identity/issues/133) preserves that concrete
later implementation. Its scope keeps v0 behavior and human-supplied facts.

The following queues were read back as open and are reused: Realm #19/#26/#60,
Aether #67, Holon #41, EgoLint #35/#36, Relay #49 and Sanctuary #8. Their
continued existence establishes tracking coverage, not completed adapters.
The [deferred-work table](../../consumers/ECOSYSTEM_INTEGRATION.md#deferred-work-and-existing-queues)
keeps each actual owner and queue visible without adding new hard prerequisites
to #106/#107 or declaring a shared-default consolidation implemented.

## Mantle evidence boundary

The unchanged complete-kit receipt names Mantle
`b08045acc1e982dd9424c1d8c91b0badd64744e8` and records its original independent
native generations. Read-only raw Git inspection verified all 14 consumed
files against that receipt's SHA-256 values and found them byte-identical at
the current Mantle main revision above. The manifest has organization/default
and product/override layers; no Press Kit or handbook is declared.

No consumer source, rights, assets, approvals, historic receipt, screenshot,
runtime code or workflow definition changes in this closeout. No new
generation, renderer/browser/native/Docker test, installation or CI execution
is performed; historical results retain their original represented source.

## Decision impact

ADR not required: apply existing source/projection, installation, scaffolding
and policy-owner boundaries; update operational references and retain deferred
requirements. No contract, dependency, authority or ADR lifecycle is changed.
The actual later initializer/API choices require their own decision-impact
review under the pinned policy when selected for implementation.
