# Qualification sprint handoff — November 22, 2026

Identity main is `75ca39f3fc7e5e9e0b5578af58c966cd2590a652`; Aether main is
`e5a67e581857122a8131fe8a24d1c7e6c1fa1170`. This sprint leaves implementation
in draft branches for review. It performs no merge, release, tag, deployment,
hosted workflow dispatch or creative/ADR lifecycle promotion.

## Draft review order

- Aether [#141](https://github.com/egohygiene/aether/pull/141) →
  [#142](https://github.com/egohygiene/aether/pull/142): consume build-only export
  metadata, then verify pristine portability and exact installed materialization.
- Identity [#163](https://github.com/egohygiene/identity/pull/163) →
  [#164](https://github.com/egohygiene/identity/pull/164) →
  [#165](https://github.com/egohygiene/identity/pull/165) → source-assembly proposal child.
  Review parents before children and reconcile continuity semantically on merge.

Every receipt retains its exact represented source. Integrating a branch does
not relabel earlier observations as execution of later code. Qualification
contexts, local frontend checks, Docker/browser results, workflow outcome and
hosted/native availability remain separate.

## Completed scope and actual results

Aether's direct Identity companion has zero pristine portable diagnostics and
passes all five actual gh2.96 local scenarios. Raw installed006/017 tracking
findings remain recorded. Overall readiness is still not-ready because remote
scenarios are skipped; the three historical pilots retain pristine015/016
governing-resource/provenance findings. Final suite428:417passes/11existing
skips;32focused controls and independent core/receipt review pass.

The Identity approval parser now enforces its declared complete, timezone-bearing
string requirement instead of coercing broad ISO values. Date-only and naive
values fail before source/cache/output mutation; valid lowercase UTC works.
At `edca416d58d15b06ccc05029b0803bc27e65fe18`, full Python212 completes
210passes/two existing skips; native119passes/four helper-only ignores,
formatting, strict Clippy and generated-bundle/provenance checks pass.
Only approval `reviewedAt` is repaired; other date-time fields retain their
separate checks. No actual review instant is invented.

Browser qualification at `a56399b33548cab075e4442e64605035bccd973f`
passes the original Docker path directly and both original workflow browser
steps through local act (CI label and documented local entrypoint). Each runs
nine positives, requires the deliberate screenshot failure and passes restoration;
there are zero skips. All three bind the same 423-file source inventory
`07bb513dd71ad84f2980fed5479cf683a7689b749c7700d35f92a322ffbd3726`,
profile, exact fonts and unchanged approved PNG. The workflow also passes all
424 renderer tests, 51 source parses, public build and public-output validation.
The whole local act job exits 1: its artifact server rejects the unchanged
upload action's `mime_type` protocol field. This is not a passing hosted workflow.
The retained complete raw packets and sanitized workflow log preserve both facts.

The acquisition helper verifies four immutable action pins, archive sizes/hashes
and reconstructed Git trees. Optional `IDENTITY_BROWSER_PROXY_CA` reuses the
existing explicit build-only secret; explicit CLI wins, invalid paths fail
without disclosure, and unsafe CSV path syntax is rejected. Twenty-two focused
controls and independent source review pass. The owned overlay2 runtime recipe
retains actual shared filesystem/cgroup accounting and proxy/runc repairs;
default daemon configuration, browser profile, screenshot and storage guards
remain unchanged.

Development-image qualification at
`8255c5b9ab0e669c2cde6002353515b5a8fc0511` passes the original complete
default-root and inherited-UID1000 path. Each image executes 32 smoke commands,
including a second actual setup; all 58 selected source inputs and the exact
Rust1.97.1/pnpm11.21.0 pins remain preserved. Both repeated 14-file output
inventories agree within and across images; all 17 canonical fixture files are
preserved. Metadata inheritance, cache ownership, unknown-CA rejection,
explicit trust and native/renderer checks pass. The fresh run observes
8,957,652,992 free bytes before acquisition, above the unchanged 8GiB reserve;
no storage override is used.

The demonstrated transport failure was repaired through names-only proxy
forwarding and opt-in `--proxy-ca`/`IDENTITY_DEVELOPMENT_PROXY_CA`. Trust uses
an ephemeral public-CA BuildKit secret readable by the selected non-root user
and a read-only smoke bind. It does not modify the system trust store or
persist proxy/CA configuration into the image. Independent review catches and
closes preflight privacy and non-root secret-permission findings before the
fresh run; negative controls retain actual absence/isolation observations.

The separate self-source assembly keeps the earlier active candidate, root
source and approved masters unchanged. Fourteen proposed consumer files narrow
mechanical validation to two null review-time findings. Actual native generate
and verify refuse before output. Layer/token and descriptor/output choices
remain unselected pending the two exact review questions; component validity,
a merge or this engineering authorization does not supply those choices.

At integrated pre-handoff source `33948ad48e14d9468f136e2b7f768e321082092d`,
full Python234 completes232passes/two existing skips with actual Make and pinned
Task available. Documentation, standalone-bundle drift, extraction/provenance,
whitespace, exact reviewed packet comparisons and protected-input checks pass.
The selected Rust product/test/contract/fixture inputs remain byte-identical to
`edca416`, retaining its119native passes without inventing a new native execution.
The stricter standalone and actual native CLI also refuse the unchanged proposed
consumer with exactly two missing-review diagnostics, preserving all14inputs
and producing no output. See [integrated checks](qualification-20261122/integrated-checks.json)
and [strict refusal](qualification-20261122/self-source-strict-preflight.json).

## Next mini-roadmap within existing issues

1. **#98 — selected actual self-source.** Resolve the exact layer/token and
   descriptor/output packet, bind the actual new review event, then validate,
   generate twice, compare complete inventories and verify deliberate drift.
   Existing confirmed master/reviewer/copy/voice/permission choices stay retained.
2. **#70 / #80 / #82 / #88 — final engineering acceptance.** Reconcile these
   draft results against the merged source, retain any workflow-upload limitation,
   close demonstrated remaining date-time gaps and obtain required current native
   macOS/Windows/install coverage. Local Linux proof does not supply those facts.
3. **Aether #38 — older pilots and remote consumption.** Author portable draft
   governing resources with complete dependency closure and honest retained
   migration history; keep approved auditor/staging bytes and strict validation.
   Then rerun actual local pilots and separately qualify remote update/rollback
   and observed agent use. Do not silently strip source paths or rewrite bundled
   specification bytes to evade diagnostics.
4. **#98 — release and publication.** Qualify the selected broad target/channel
   matrix and downloaded install/upgrade/rollback; assemble checksums, license/SBOM
   and provenance. Preserve immutable v1.0.0; the next version/commit/tag remains
   a concrete later selection. Follow with release-backed public-kit/live-hash/
   restore proof and one contrasting reviewed consumer upgrade/rollback.
5. **#116 — reconcile last.** Close the finish tracker only after actual producer,
   engineering, release and consumer acceptance. Hygiene #128 and Flow adoption
   retain their own later repository-contract scope.

No duplicate issue or speculative new closure dependency is added. Decision
impact references existing ADR-0001/0005/0011/0012 and preserves all dispositions.

Review packets: [layers/tokens](../98/self-source-review/README.md),
[descriptors/output and candidate](../98/source-assembly/README.md),
[browser evidence](../80/ACTION_REPLAY_2026-11-22.md),
[image evidence](../82/FULL_IMAGE_2026-11-22.md),
[owned runtime](../80/ISOLATED_DOCKER_2026-11-22.md).
