# Identity release process

This procedure applies to release candidates and stable releases. It creates
an immutable artifact boundary; it does not publish a website or mutate a
consumer repository.

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

1. Use `1.0.0-rc.N` for a candidate. Do not call it stable in documentation or
   consumer defaults.
2. Run `python3 scripts/verify_release.py --repository-root "."` and the full
   validation suite before tagging.
3. Create an annotated, immutable tag named exactly `v<package-version>`.
   Example: `v1.0.0-rc.1` for package version `1.0.0-rc.1`.
4. Push the tag. The release workflow validates the exact tag/version pairing,
   builds the Linux archive, creates an SPDX SBOM, a locked-dependency license
   inventory, and checksums, attests the archive, and creates the GitHub
   release.
5. Verify the GitHub release has the archive, `SHA256SUMS`, SPDX SBOM, license
   inventory, and an available build-provenance attestation. Re-run the
   documented quickstart from the released source or archive before marking a
   stable release.

## Final v1.0.0 gate

A `v1.0.0` tag is permitted only when all of the following evidence is current:

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
