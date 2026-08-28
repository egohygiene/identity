# ADR-014: Keep design-system handbooks as governed projections

- **Status:** Accepted
- **Date:** 2026-08-28
- **Tracking:** [issue #35](https://github.com/egohygiene/identity/issues/35)
- **Decision owners:** Identity maintainers and consumer identity owners

## Context

Identity needs a useful design-system handbook for humans and concise context
for automation, while remaining a brand-source compiler rather than a UI
framework. Existing token, voice, usage, provenance, and approval contracts
already establish human-reviewed local source. Free-form handbook prose,
untracked inspiration, or agent-maintained instructions would create another
authority and make review, ownership, and reproducibility unclear.

## Decision

Add an optional local `documents.handbook` source boundary to Identity v1.
Validate a reviewed design-system source and a reviewed external-reference
catalog under the existing lifecycle and approval model. Define two derived
contracts: a human handbook and a compact AI-readable design context.

Both projections are generated outside `.identity/`, carry a stable resolved
source digest, and identify a fixed projection version rather than a runtime
timestamp. They expose explicit capability status and ownership. Identity owns
brand contracts and projections; Holon owns reusable components; consumers own
layouts; Aether and other tools consume the compact context without becoming
canonical authors.

Reference catalogs describe observations and rights constraints only. They do
not fetch, copy, redistribute, or grant permission to use third-party assets,
marks, or copy.

## Consequences

- Existing v1 consumers remain valid until they explicitly adopt handbook
  source.
- A handbook can show what is absent or owned elsewhere instead of implying a
  fictitious component library.
- Automation receives concise, verifiable source facts rather than a mutable
  prompt document.
- The renderer implementation has an exact output contract and an auditable
  deterministic boundary.
- Authors must create approval records for handbook principles and reference
  decisions before they can appear publicly.

## Alternatives rejected

- **Make a Markdown handbook canonical:** lacks closed structure, lifecycle,
  and machine-readable ownership information.
- **Put components in Identity:** duplicates Holon's responsibility and couples
  the brand compiler to one UI implementation.
- **Allow agents to maintain their own brand context:** makes review and
  provenance impossible to establish.
- **Scrape reference sites during rendering:** creates network, licensing,
  reproducibility, and availability dependencies.

## Reconsider when

Revisit if a future component contract proves that Identity must own a
framework-neutral interface, or if the organization accepts a versioned,
reviewable external-reference ingestion process with stronger rights evidence.
