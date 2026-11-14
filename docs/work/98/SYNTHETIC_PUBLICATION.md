# Synthetic native publication proof — 2026-11-14

The [bounded receipt](../../evidence/identity-native-publication-synthetic-2026-11-14.json)
records an actual compiler → release-owned native inputs → publisher → public
verifier execution. Source is a disposable copy of the existing fictional
expanded fixture, explicitly named **Synthetic native-publication fixture**.
Its ID is `identity` solely to exercise this Identity-owned adapter; its
repository is `https://example.invalid/native-publication`. This supplies no
real self-source, artwork rights, release or public upload.

## Construction and actual checks

1. Copy the expanded `.identity/` into a new disposable consumer. Select the
   synthetic ID/name/repository above while preserving its existing synthetic
   asset/approval subjects and exact asset bytes.
2. Run the built CLI's `v1-generate` and read-only `v1-verify`, retaining the
   native compiler manifest/model under `assets/identity/`.
3. Select the existing `identity.public-brand-kit-config/v1` config with
   `sourceMode: native-v1`, the normal canonical URL, `assetBaseUrl: ./`, empty
   optional browser assets and release selection
   `{defaultTag: v1.0.0, binding: selected-annotated-tag}`. This matches the
   compiled fixture's version; it is not a new real Identity release.
4. Initialize a local-only Git repository, ignore the compiler's `.cache/`,
   commit source/config/artifacts and create an annotated synthetic tag at that
   exact commit. No remote is configured or pushed. The tag resolves to fixture
   commit `222bdf690ab55f758cda2e487713f84f59a68083`.
5. Run `renderer/scripts/build-public-site.mjs` twice with explicit
   `--source-root`, `--config`, `--release-tag`, `--release-commit` and two new
   `--output-directory` selections. Run `verify-public-site.mjs` on each.
6. Compare all emitted files: both 24-file sites match byte for byte. The
   archive contains fifteen native artifacts. All selected source/config/native
   bytes remain unchanged and Git stays clean.
7. Change archive bytes and require public verification to reject them, then
   restore them. Change the source brief and require the selected Git-blob gate
   to reject it. Independently require the canonical-source-to-native-output
   gate to reject the stale binding. Restore the brief and rerun public verify.

All checks pass, including three required negative results and restored
verification. Canonical source digest
`ea3644770636c18e45cc317f15c812bf5d1b9edc717e20043cb57caa04ee9c0e`
and public-inventory digest
`961729d4d34f27883ae74387a33cb4d552fbbda7b1a0e4e5cfb0e4120c101f39`
retain their separate meanings. The deterministic archive SHA-256 is
`ece6e7fe7885cb5d974a7e62dc3f9d4ceb7025db00639d680cd6edf6bcc3f13c`.

The publisher is the merged PR139 implementation, using the renderer component
candidate with exact function/HTML comparisons. This local proof does not
replace permanent release/platform/CI regressions, actual Identity root source,
or real release-backed publication/rollback. Legacy v1.0.0 selection is unchanged.

ADR-Ref: egohygiene/identity#ADR-0034, proposed with null approval.
