# Canonical validator source

This internal package separates source I/O/inventory/digest, project contracts,
tokens, approvals/provenance, targets, guidance, voice, usage, handbooks,
channels, Press Kits, social surfaces, repository presentation and mascots.
`entrypoint.py` keeps the existing orchestration and CLI order.

Edit these modules, then regenerate the checked-in public entry point:

```sh
python3 scripts/build_identity_validator.py
python3 scripts/build_identity_validator.py --check
```

`scripts/validate_identity.py` remains a self-contained, standard-library-only
script and the existing import facade. Rust's existing `include_str!` and the
consumer-authoring copy path continue to read that single file. The generator
concatenates source definitions without executing modules and omits internal
package imports; the shared module retains the original stdlib prelude.
There is no new installed package or organization runtime dependency.

Internal module paths are not an additional public API. Existing consumers
continue importing or executing `validate_identity.py`; do not mix its types
with direct internal-module imports. Generated code is derived output and must
be committed with a source change. Do not hand-edit it to hide source drift.

The extraction records structural source/AST preservation in
`docs/work/116/validator-extraction.json`. That record is a dated refactor
receipt, not fixture outcome or cross-language runtime evidence. Existing
source/digest/confinement/approval suites and all CLI/import/embedded-consumer
checks remain deferred to the agreed sweep before acceptance.
