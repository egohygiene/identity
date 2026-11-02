# Maintain shared projection boundaries

The public guidance, handbook and Press Kit entry points retain their existing
names, error classes and formats. `scripts/projection_boundary.py` holds only
the shared standard-library mechanics selected for #86:

- Object-shaped JSON loading, with the caller's existing exception class.
- Approved/public audience predicates, preserving the explicit distinction
  that Press Kit admission also requires its existing approval identifier.
- Delegation to the existing validator's canonical source-inventory/digest
  contract; no second digest algorithm or Rust implementation is introduced.
- Existing repository-relative generated-output guards, with each caller's
  existing canonical-source error message.
- Identical JSON serialization and text/byte temporary-write mechanics.

`render_guidance.py` continues using the design-system audience boundary;
format-specific selection, inheritance, approval resolution, source/release
binding, Markdown/HTML rendering and packaging remain with their current
owners. Channel active/badge rules, external-social admission and v0/v1 profiles
are not collapsed into a generic boolean. No source state is promoted.

Keep exceptions and wrapper signatures stable when changing shared code.
Preserve the shared source-digest conformance vectors and compare generated
bytes through the existing guidance/design-system/Press Kit suites. The
[extraction receipt](../work/116/projection-extraction.json) records which
wrappers changed and confirms every other function's AST was preserved; that
is structural evidence only. Runtime, audience-isolation, cross-language
digest, failure-path and output-equality checks are deferred to the agreed
quality sweep. This candidate makes no passing behavioral claim.

The common module ships with these existing source-checkout entry points.
The validator's [generated standalone bundle](../../scripts/identity_validation/README.md)
remains independent and is still embedded/copied through its original single
file. Do not add a dependency on the internal validator package to a consumer
solely for projection organization.

ADR not required: internal mechanics are delegated behind unchanged existing
interfaces and policy decisions; no new authority or public format is adopted.
