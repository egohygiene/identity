# ADR-015: Keep Press Kits as governed public projections

- **Status:** Accepted
- **Date:** 2026-08-28
- **Tracking:** [issue #34](https://github.com/egohygiene/identity/issues/34)
- **Decision owners:** Identity maintainers and consumer identity owners

## Context

Press and Media Kits need consistent, ready-to-download material, but they
often accumulate unreviewed launch claims, stale bios, private contacts, and
asset folders whose rights or intended use are unclear. Identity already has
local source, approval, provenance, and public-asset boundaries. A separate
hand-maintained press folder or renderer configuration would create another
authority and make public exposure hard to review.

## Decision

Add an optional local `documents.pressKit` source boundary to Identity v1.
Require reviewed short and long boilerplate and govern every optional fact,
link, contact, team biography, and selected asset. Generate the Press Kit
outside `.identity/` as a deterministic JSON, Markdown, integrity-manifest,
checksums, and ZIP package.

Selected assets may only reference assets that have already passed the active,
public, approval, provenance, and byte-integrity checks. The reference renderer
may render a supplied package only after it matches the immutable Brand Kit
project and source digest. Identity does not own website routing or publication.

## Consequences

- Existing v1 consumers remain valid until they explicitly adopt Press Kit
  source.
- Approved information can be rebuilt, checked, archived, and reused across
  release pages without another hand-maintained bundle.
- Candidate claims, private contacts, and unselected assets cannot become
  public by renderer configuration or directory copying.
- Consumers retain control of domains, routes, deployment, and social systems.
- Maintainers must create explicit reviewed records before new material appears
  in a public package.

## Alternatives rejected

- **Maintain a free-form press folder:** no schema, approval, selection, or
  integrity boundary.
- **Let the renderer read `.identity/`:** makes publication depend on private
  source and allows renderer code to become a second content author.
- **Copy every approved asset automatically:** exposes more material than a
  given Press Kit actually needs and weakens intent.
- **Generate contacts, biographies, or claims from prompts:** cannot establish
  factual ownership, approval, or a durable correction path.

## Reconsider when

Revisit if Identity needs a separately versioned multi-language content
localization contract, or if a consumer-owned publication service establishes a
reviewable deployment and release manifest that can consume the same immutable
package without changing this authority boundary.
