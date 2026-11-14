# Local implementation acceptance — 2026-11-14

Reviewed combined main: `80729d12acb52a3d578b0561c42222a558bfde9c`.
PRs #138, #139, #140 and #146 are merged. This is scoped implementation
evidence for #84–#86 and a reproduced test-harness repair; the later repository
audit, `act`, full platform/browser qualification and release remain separate.

| Issue | Actual acceptance evidence |
| --- | --- |
| #84 | The historical #13/#37 owner/merge record is retained in [workflow retirement](workflow-retirement.md). A fresh exact `git ls-remote --heads origin feat/13-brand-guidance-v1` returned no ref. Both writers remain absent; the seven-purpose trigger/permission inventory remains current. The retirement guard and its three regressions pass; read-only documentation validation passes. |
| #85 | The generated standalone validator matches canonical modules. Exact diagnostic fields/order match the pre-extraction `d247487379569c3701a8cefe6d6136502657fa64` validator for three complete source roots and all twelve invalid mutation fixtures. The 169-case Python suite passes with two existing skips. All fourteen native v1 consumer tests pass, including copied-binary/embedded-validator, source-authority and cross-language digest vectors. No new runtime dependency is introduced. |
| #86 | Exact pre-extraction/current output bytes agree for twelve guidance public/review JSON/Markdown/HTML, handbook/context and Press Kit projections. Selected Press Kit asset bytes also agree. Python public/review, path, failure and digest regressions pass; the native shared lifecycle/digest cases pass. Distinct v0/v1 profiles and stdlib/offline entry points remain intact. |

The schema-inventory regression initially failed because #138 added two genuine
initializer schemas. Its expected inventory now includes those schemas;
schema contents and validation rules are unchanged. The full Python rerun
completed: 167 passed, two existing skips.

## Copied executable investigation

The first Rust baseline reproduced the retained Linux error 26 at
`consumer_recovery.rs` process spawn. Its library cases and v0 parity cases
passed; the recovery suite failed when immediately executing a copied binary.

A bounded synthetic Linux fork experiment retained an inherited writable
descriptor after its parent closed it. Execution returned `ETXTBSY` (26);
after the child closed that descriptor, the unchanged executable ran. This
demonstrates the copy/spawn race mechanism; it is not a production recovery
failure or a claim that a retry diagnosed the historical hosted process.

The recovery harness now serializes executable copying against both child
spawn sites. The mutex is released immediately after spawn, so child execution,
native writer exclusion and recovery concurrency remain exercised. No retry,
assertion relaxation, production lock or durability change is added. The
recovery suite passes once with its normal configuration and twice with
sixteen test threads: nine passes and one explicit helper-only ignore per run.

`python3 scripts/build_identity_validator.py --check` and
`python3 scripts/verify_extraction.py` pass. Full Rust completion after the
remaining module moves, Clippy, native platforms, qualified screenshots and
`act` remain named later gates. ADR not required: qualify existing refactors
and fix test-fixture synchronization without changing public contracts.
