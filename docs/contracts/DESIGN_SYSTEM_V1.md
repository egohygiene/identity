# Identity v1 design-system handbook and context contract

## Status and boundary

This document defines the contract slice for [issue #35](https://github.com/egohygiene/identity/issues/35).
It establishes approved local input and stable output shapes. It does **not**
yet implement the handbook/context projection command or a component library.

Identity remains the source-and-projection boundary for reviewed brand intent.
It does not take ownership of product UI implementation:

| Concern | Owner | Identity's role |
| --- | --- | --- |
| Tokens, voice, usage, asset provenance, and handbook principles | Identity | Validate, resolve, and project reviewed source |
| Reusable UI components | Holon | Consume constraints; own implementations and APIs |
| Product layouts and interaction decisions | Consumer | Own implementation and bounded overrides |
| Agent instructions and task execution | Aether or consumer | Consume the compact context; do not originate canonical brand decisions |

## Canonical source

`identity.project/v1` may add the optional `documents.handbook` object:

```json
{
  "designSystem": ".identity/guidance/design-system.json",
  "references": ".identity/guidance/design-references.json"
}
```

The extension is deliberately optional and additive: existing v1 consumers do
not become invalid merely because they have not adopted handbook source. Once
present, both paths are local, normalized, and required.

`identity.design-system-source/v1` contains reviewed sections, principles, and
declared capability boundaries. Every principle and capability carries the
existing governance envelope: subject, lifecycle state, visibility,
provenance, and approval. Public projection therefore includes only reviewed
public records. A capability must explicitly state one of:

- `declared` — a real Identity contract is available;
- `not-declared` — the named concern is intentionally outside the current
  Identity contract;
- `unsupported` — Identity will not support it in this version.

The record also names `identity`, `holon`, or `consumer` as the accountable
owner. A Holon-owned component capability cannot be made to look like an
Identity component API through prose alone.

`identity.design-reference-catalog/v1` is a separate reviewed observation
ledger. A record captures its HTTPS URL, capture time, patterns worth studying,
decision (`adopt`, `adapt`, `reject`, or `observe`), rights note, canonical
effect, and governance. It stores no third-party assets or copied prose. A
reference can influence canonical source only after a distinct approved source
change; `affectsCanonical: false` is the safe default for observation.

## Generated projections

`scripts/render_design_system.py` validates this source and derives two
framework-neutral artifacts outside `.identity/`.

| Projection | Schema | Audience | Contents |
| --- | --- | --- | --- |
| Design-system handbook | `identity.design-system-handbook/v1` plus Markdown | Human reviewers and product teams | Resolved inheritance, enabled profile versions, approved principles, token/voice/usage/asset entries, capability boundaries, and reviewed references |
| Compact design context | `identity.design-context/v1` plus Markdown | Aether and other automation/consumer tools | Project identity, source digest, enabled profile versions, applicability, concise tokens/voice/usage facts, and explicit capability states |

Neither projection is an authority to invent design decisions. They copy or
normalize reviewed source; a renderer may choose presentation, but cannot
reinterpret a `not-declared` capability as implemented or promote a candidate
record to public guidance.

## Determinism and provenance

The generated handbook and context must be reproducible from the same
validated source. The future renderer will:

1. validate the complete Identity v1 source before resolving anything;
2. include a stable SHA-256 source digest covering the resolved inputs;
3. sort derived arrays by stable source IDs/paths and use canonical JSON;
4. record a fixed renderer/projection version rather than a wall-clock
   generation timestamp; and
5. refuse to write to `.identity/` or retrieve reference URLs at render time.

This makes a context record useful to an agent without making it an opaque,
stale prompt blob. Consumers can verify the digest against the local source and
rebuild it when a reviewed decision changes.

## Validation and diagnostics

The standard-library-only validator validates configured handbook sources as
part of `identity.project/v1`:

```bash
python3 scripts/validate_identity.py \
  --repository-root "path/to/consumer" \
  --format "human"
```

The `IDN1701` family identifies closed-structure, lifecycle, approval, and
capability errors in `design-system.json`. `IDN1702` identifies equivalent
catalog, URL, decision, and rights-record errors in `design-references.json`.
Existing `IDN1601`–`IDN1604` guidance diagnostics continue to enforce the
shared governance envelope.

## Commands

Print one projection to standard output without writing files:

```bash
python3 scripts/render_design_system.py \
  --repository-root "path/to/consumer" \
  --format "handbook-markdown"
```

Write the complete generated set outside canonical source:

```bash
python3 scripts/render_design_system.py \
  --repository-root "path/to/consumer" \
  --output-directory "assets/identity/design-system"
```

The explicit output directory receives `design-system-handbook.json`,
`design-system-handbook.md`, `design-context.json`, and `design-context.md`.
It may not point into `.identity/`, traverse symbolic links, or cause an
external reference URL to be retrieved.

## Deliberately deferred

This contract does not create:

- a Holon component library or a component registry;
- a consumer layout/template contract;
- live crawling or import of reference sites;
- automated approval of references or creative choices; or
- a public website redesign.

Those are separate implementation or consumer-owned decisions. The next
follow-up is a real consumer handoff that uses these projections without
claiming that a component implementation belongs to Identity.
