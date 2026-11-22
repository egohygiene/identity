# Identity release process

This procedure applies to release candidates and stable releases. It creates
an immutable artifact boundary; it does not mutate a consumer repository.
Publishing a stable release also triggers the separate, release-backed Identity
Brand Kit Pages projection described in
[the public publication guide](../publication/IDENTITY_PAGES.md).

For the next release, use the proposed
[distribution and compatibility plan](NEXT_RELEASE_MATRIX.md) alongside this
procedure. Published `v1.0.0` remains immutable. The next version is proposed as
`v1.1.0`, subject to actual compatibility review; new target/package rows remain
planned until their own artifact and native-install evidence passes.

## Preconditions

- The target revision is merged to `main`, has no unresolved release-blocking
  diagnostics, and has passing required checks.
- `Cargo.toml` and `renderer/package.json` declare the same valid semantic
  version.
- The release notes, support policy, security policy, source-install guide,
  migration/rollback guidance, and known limitations are current.
- The source contracts, profile versions, CLI surface, adapter boundary, and
  generated package compatibility are semver-compatible with the intended
  version.
- Empathy and OptiFlow evidence still pins an immutable compatible Identity
  revision. The public renderer/browser smoke test passes.

## Candidate and stable tags

1. Select the next compatible version, then use `<version>-rc.N` for a
   candidate. Do not reuse published `v1.0.0` or call a candidate stable in
   documentation or consumer defaults.
2. Run `python3 scripts/verify_release.py --repository-root "."` and the full
   validation suite before tagging.
3. Create an annotated, immutable tag named exactly `v<package-version>`.
   The tag must match the selected package version; preserve every prior tag.
4. Push the tag. The release workflow validates the exact tag/version pairing,
   currently builds the Linux archive, creates an SPDX SBOM, a locked-dependency
   license inventory and checksums, attests the archive, and creates the GitHub
   release. Broader packaging needs the separately implemented and qualified
   target/channel path in the next-release plan; this guide does not add it.
5. Verify the GitHub release has every selected qualified artifact,
   `SHA256SUMS`, SPDX SBOM, license inventory and available build-provenance
   attestation. Independently verify downloaded integrity/authenticity and
   clean-install the actual published bytes for each supported cohort before
   advertising its matrix cell as supported.
6. Confirm `Publish Identity Brand Kit` deploys the static page from that same
   annotated stable tag. The public site is a projection of the release, not a
   second release artifact source.

## Stable release gate

The next stable tag is permitted only when all of the following evidence is
current for its exact selected source and supported cohorts:

- schema and migration contracts validate, including compatibility diagnostics;
- deterministic compiler/package and clean-room double-generation checks pass;
- the `.gitattributes` line-ending policy preserves identical source and visual
  baseline digests on every supported platform;
- Linux, macOS, and Windows source-install CLI checks pass;
- the reference renderer's accessibility and visual/browser checks pass;
- license/provenance checks, SPDX SBOM, archive checksums, and provenance
  attestation are present;
- documentation links, quickstart, support/security policy, upgrade/rollback,
  and known limitations have been checked;
- the generated Brand Kit and public renderer smoke surface pass;
- Empathy and OptiFlow consumer evidence is compatible with the exact release
  commit or has a documented, reviewable upgrade rationale.

Select and prepare source/artifact changes before the final engineering sweep.
Then complete release/live/rollback and contrasting-consumer evidence under
#98, and reconcile #116 last. Those two issues remain open through their actual
release acceptance; zero open issues is not a prerequisite for performing the
release work that closes them. The historical [v1.0.0 guide](V1.md) and receipts
retain their original scope.

## Rollback and incident handling

Git tags and release assets are immutable evidence. Do not replace a bad asset
under the same tag. Mark the affected release as a pre-release or add a clear
release warning, withdraw its support status, publish a corrected higher
version, and update the changelog/security advisory as appropriate. Consumers
roll back to their previous immutable release and regenerate/verify their
package boundary.

Relay may later execute this workflow through a reusable release contract.
Until then, this repository keeps the workflow thin and pinned while preserving
the same artifacts and evidence boundary.
