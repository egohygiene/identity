# Explicit v1 initialization candidates

This is the draft interface for [#133](https://github.com/egohygiene/identity/issues/133).
It is not in the published `v1.0.0` release. Runtime acceptance and CI are
deferred; pin the exact reviewed draft implementation before later execution.
[ADR-0033](../decisions/ADR-0033-explicit-v1-initialization-candidates.md)
remains proposed.

```text
identity v1-init --repository-root ROOT --request FILE --output-directory DIR
```

`ROOT` must exist. `FILE` and `DIR` are normalized repository-relative paths.
`DIR` must not exist and must be disjoint from canonical source, generated
assets and all selected inputs. There is no force or automatic apply option.

## Request and output

The `identity.initialization-request/v1` request accepts supplied partial
`project` facts using the existing v1 project fields, `layers` containing
existing layer metadata and local token paths (digests are computed), and a
`targets` path to an existing v1 targets document. No profile is enabled by
default. Missing facts remain absent.

Alternatively, `sourceRoot` selects an existing local consumer root containing
validated v1 source. This import is exclusive with the seed fields above;
it preserves source bytes and approval subjects instead of merging conflicting
facts. The explicit root `.` is allowed for this read-only import.

Output is `DIR/.identity/` plus `DIR/initialization-report.json`. The report
contains source diagnostics, missing-input notes, byte inventories and actual
implementation/validator fingerprints. `incomplete` and `ready-for-review`
describe candidate preparation only. Neither is human approval, producer
capability proof, a released kit or permission to publish.

Malformed/unsupported material and unsafe/conflicting paths fail without
altering supplied files. Missing human facts are a successful incomplete
candidate result. Repeating the command at an existing destination fails;
choose another explicit destination. Initialization installs no tools, fetches
no network material and generates no Brand Kit outputs.

## Manual review and adoption

Review the request, candidate diff, report and all human evidence. Supply
missing actual facts, masters, rights and same-subject approvals in the
candidate. Validate it with the matching immutable standalone validator.
Only then review a separate manual copy into the consumer's canonical source,
preserving existing v0/v1, generated and unrelated files. A conflict requires
an explicit reviewed source change; the initializer never resolves it.

Manual authoring through the [worksheet](AUTHORING.md) remains supported.
Generation, verification and [recovery](RECOVERY.md) remain separate commands.
Holon owns scaffold materialization, Realm immutable installation, Aether agent
guidance, and EgoLint/Relay delegated checking and enforcement; see the existing
[handoffs](INITIALIZATION_AND_VALIDATION_HANDOFFS.md).

## Deferred acceptance

The later campaign must cover absent, v0-only and existing-v1 consumers;
partial facts; unsupported/invalid inputs; path conflicts, links and failure
preservation; repeated invocation; exact import bytes; and successful source
validation only after actual required facts/evidence are supplied. Include
copied-binary/offline execution, cross-platform path handling and the existing
v0 parity/source-authority regressions. No case is claimed executed here.
