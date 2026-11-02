# Identity roadmap sprint and merged-source handoff

Current merged status: see [MERGES.md](MERGES.md). The source PRs are merged; the detailed candidate and deferred-check notes below remain relevant.

Latest product closeout, 2026-11-02: #108 completes its bounded integration
handoff; see the [eight-criterion review](../108/CLOSEOUT.md). The exact Relay
DCO action remains explicitly unresolved under the allowed criterion. Existing
owner queues retain future work; #133 now owns the deferred v1 initializer.
Next product selection is #106, then #107; tests/CI remain deferred.

Latest scope disposition, 2026-11-02: the maintainer resolved #109 around
comprehensive identity specification and validation. Components remain a future
possibility; existing foundations suffice now. See the
[scope record](../../consumers/PRODUCT_DESIGN_SYSTEM_SCOPE.md). Next product
choices are #106/#107 after the subsequent #108 closeout. Tests/CI stay deferred.

Coordinator: [#116](https://github.com/egohygiene/identity/issues/116).
Merged sprint: [PR #130](https://github.com/egohygiene/identity/pull/130), originally stacked on #129.
Original sprint branch: `codex/identity-product-sprint-20261102`.
Original sprint base: then-unmerged [PR #129](https://github.com/egohygiene/identity/pull/129) at
`d247487379569c3701a8cefe6d6136502657fa64`, exact tree
`5d49bc6c1dcdb0d758e182ab3ffd14cb37489fe5`.
Main at sprint start: `47995976ae41415226bd6fb9400fbbd02777fca6`. Current source merge: `037fcc042f8e94743d3756a121f0df1d0a5f74d7`.
Mode: bounded implementation/proposal sprint with tests and CI explicitly deferred.

## Merged sprint source and remaining acceptance

| Issue / roadmap step | Source result | Remaining acceptance |
| --- | --- | --- |
| #109 / IDN-Q39 | Maintainer-selected specification/validation scope; foundations suffice now and components remain possible later. The [scope record](../../consumers/PRODUCT_DESIGN_SYSTEM_SCOPE.md) and dated ADR-0031 clarification retain the disposition. | Scope decision complete; no component implementation or follow-up selected. Formal ADR-0031 lifecycle remains proposed. |
| #108 / IDN-Q38 | Verified owner references, concrete existing Mantle source/override/kit handoff, eight-criterion closeout and deferred-work mapping. | Bounded scope complete with the allowed unresolved Relay DCO reference. V1 initializer is #133; existing owner issues retain installation, guidance, validation and governance work. Runtime/CI proof is deferred. |
| #106 / IDN-Q36 | Optional standard-library announcement-draft tool, request/receipt schemas, [consumer guide](../../consumers/LAUNCH_DOCUMENTS.md), proposed ADR-0032 and five unexecuted regression cases. | Agree on the proposed real consumer/template, run focused/source suites, review voice/claims/rights and record real adoption. No posting or approval is performed. |
| #107 / IDN-Q37 | [Existing imagery/motion inventory](../../consumers/OPTIONAL_VISUALS.md) and a bounded approved-illustration source-to-kit route. | Select an actual consumer/category or approve a scope disposition. No new artwork, asset category or animation engine is invented. |
| #84 / IDN-Q23 | Remove the two retired hardcoded guidance rewrite definitions after verifying merged PR37, closed issue13 and absence of its old branch ref. | Review [ownership/retained-workflow inventory](workflow-retirement.md) and execute deferred source/workflow checks. The definitions are now retired through merged PR130; runtime checks remain deferred. |
| #85 / IDN-Q24 | Canonical validator source split into common plus fourteen focused modules, with a deterministic self-contained public bundle and read-only drift guards. | Execute existing CLI/import/source/digest/embedded-consumer suites. [Structural receipt](validator-extraction.json) proves AST preservation, not runtime outcomes. |
| #86 / IDN-Q25 | Explicit shared projection source/audience/path/serialization mechanics behind unchanged wrappers and formats. | Run public/review isolation, digest, failure-path and generated-byte comparisons. [Extraction record](projection-extraction.json) identifies the wrappers and preserved function bodies. |

The merged sprint did not complete seven acceptance gates. #109 has its separate maintainer scope disposition and #108 its bounded handoff closeout; the five other sprint issues retain their remaining acceptance. PR129/PR130/PR123 are merged and #105 is closed. Historical exact-head evidence does not qualify later combined code. Prior ADR rationale, approvals, existing asset bytes and immutable releases are preserved.

## Structural evidence actually collected

- All 32 parent-PR source blobs, including its binary fixture, matched their
  Git object IDs and the complete parent source tree before implementation.
- The generated standalone validator has exactly the same Python AST as the
  pre-extraction script. Original CLI/import names, definition order and Rust
  single-file embedding are preserved structurally; no validator runtime was
  executed as part of that comparison.
- Projection functions outside the thirteen named delegating wrappers retain
  their original ASTs. Audience predicates intentionally retain the distinction
  between prevalidated guidance and Press Kit approval-identity admission.
- Changed Python syntax, JSON, local documentation links, pinned Hygiene ADR
  metadata, continuity structure/budgets, prior ADR bytes, roadmap step blocks
  and whitespace are checked before delivery. The final PR records the actual
  result and remote file/head verification.
- Standalone artifact generation is separate from behavioral validation.
  No fixture outcome, browser result, Rust compile/test, CI success, deployment,
  creative acceptance or release readiness is claimed for this sprint.

## Deferred quality pass

Prepare the repository's existing pinned toolchain/dependencies before running
the existing native checks. No test jobs, dependency installation or tool
acquisition were initiated for this sprint. Useful focused commands are:

```sh
python3 scripts/build_identity_validator.py --check
python3 -m unittest discover --start-directory tests --pattern test_render_launch_document.py --verbose
python3 -m unittest discover --start-directory tests --pattern test_validate_identity_v1.py --verbose
python3 -m unittest discover --start-directory tests --pattern test_source_digest.py --verbose
python3 -m unittest discover --start-directory tests --pattern test_render_guidance.py --verbose
python3 -m unittest discover --start-directory tests --pattern test_render_design_system.py --verbose
python3 -m unittest discover --start-directory tests --pattern test_render_press_kit.py --verbose
python3 scripts/verify_docs.py --repository-root .
```

Then use the existing `make check` or `task check`/`scripts/dev-env.sh check`
surface for the full Rust, Python, renderer and public-kit pass, plus the
existing pinned decision-owner checks described in
[decision validation](../../decision-validation.md). Complete actual native
platform/browser/Docker qualification separately under #70/#80/#82. Existing
cross-language source-digest vectors and v0/v1 distinctions remain unchanged.
Do not report an unavailable or unrun check as a pass.

Before adopting the new announcement tool, prove matching/unknown/internal
record selection, omitted assets, exact rights/bytes, supplied-fact validation,
literal prose, source preservation, deterministic output, no overwrite,
canonical-path rejection, receipt integrity, extra/tampered files and clear
failure/partial-output handling. The five authored cases are starting coverage,
not proof that those behaviors passed. Verify actual voice/destination fit with
the selected owner and retain review of changing claims.

## Scope and next action

The three source PRs are merged; review the current merged source and keep new
ADRs 0031/0032 proposed with null approval. The source merges, #105 closure and subsequent maintainer scope disposition for #109 are recorded separately. Issue #80 is reopened for missing proof. No release, publication, deployment, social posting, DCO attestation or creative approval was performed. Commits contain `[skip ci]`; provider runs are checked
separately after merging; zero runs were observed for all three source merge commits.

#80 remains open after PR123 source merged and still needs its actual local Docker acceptance and fresh nine-case proof. #82/#88 retain
their existing prerequisites. Rust tooling is unavailable in this environment,
so #87 is unstarted. Final #83 reconciliation, #70 comprehensive qualification
and #98/G09 self-source/rights, release, dogfood and contrasting-consumer
acceptance remain in tracker #116. No new real consumer/approval is fabricated
to bypass those gates.

The forty stable roadmap IDs, issue mappings and dependencies remain. Q35 records its exact qualified source and merge; Q39 records the maintainer scope disposition; Q38 records its bounded handoff. Other acceptance states and exit boxes are retained. Any newer main/parent/candidate edits
need a fresh source comparison before combining branches.
