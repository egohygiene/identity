# Repository setup and contribution references

This handoff addresses [#108](https://github.com/egohygiene/identity/issues/108)
using the existing Identity source, policy links and offline commands. It adds
no repository scaffolder, policy-inheritance engine, DCO action or CLA service.

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

The exact issue/action link remains unresolved. This bounded search result is
not proof the work never existed. During review, obtain the owner's reference
and link that existing work. Do not create another action, substitute an
unrelated check, add a contributor's sign-off or change repository protections.
Later qualification must distinguish adoption mode, immutable action version,
actual check outcome and provider required-check settings.

CLA support remains optional future work requiring a concrete use case,
policy/legal owner, signing/data boundary and accountable delivery owner.
This checkpoint collects no signatures and proposes no signing service.

## Bounded consumer example

1. Keep canonical policy documents and existing issue/PR templates in their
   authoritative locations. Holon may materialize an explicitly selected
   baseline; Identity does not rewrite those files.
2. Record approved brand facts in `.identity/`. If a Press Kit is adopted,
   supply reviewed policy links and exact approved copy through its existing
   source; no new policy/override schema is needed.
3. In an already provisioned Realm environment, use the selected executable:

   ```bash
   identity v1-generate --repository-root path/to/consumer
   identity v1-verify --repository-root path/to/consumer
   ```

   Missing executables, incompatible versions and failed validation remain
   explicit setup/check results; they do not authorize fetching sibling code.
4. Optionally generate the Press Kit and assemble the
   [complete public kit](COMPLETE_BRAND_KIT.md). Native and optional source
   digests must agree. Missing optional policy links remain absent.
5. A consumer-owned workflow can later call these same commands through a
   reviewed Relay adapter. Record the actual environment/result. Local checks
   do not establish hosted CI, policy enforcement, release or deployment.

Shared brand defaults retain existing content-addressed source and explicit
consumer overrides. This guide grants no implicit configuration inheritance.
Later Realm/Aether consolidation remains a bounded post-stabilization handoff,
not a mandatory fleet migration.

ADR not required: this applies existing projection and cross-owner boundaries
without adopting policy or changing an interface.
