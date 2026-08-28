# Changelog

All notable user-facing changes to Identity are recorded here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and versions
follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

No unreleased changes.

## 1.0.0 — 2026-08-28

### Released

- Publish the first stable, independently installable Identity Brand Kit generator after the full cross-platform, renderer, reproducibility, SBOM, checksum, license-inventory, and provenance release gates passed.
- Retain `1.0.0-rc.2` as the final prerelease record that verified the end-to-end GitHub publication path.

## 1.0.0-rc.2 — 2026-08-28

### Fixed

- Check out the annotated release tag before `gh release create --verify-tag`, so the automated prerelease can publish its verified assets.

## 1.0.0-rc.1 — 2026-08-27

### Added

- A standalone, local-first Identity CLI with v1 source validation,
  deterministic Brand Kit generation, drift verification, and recovery-aware
  generated-state transactions.
- Nine versioned output profiles for core marks, web, PWA, GitHub, documents,
  social, tokens, metadata/guidance, and deterministic archives.
- DTCG-compatible token projections, source/approval provenance, package
  manifests, checksums, quality evidence, and a static Brand Kit renderer.
- Immutable consumer proof in Empathy and OptiFlow, plus cross-platform
  clean-room generation and release automation.

### Security

- A locked Rust toolchain and dependency graph, SPDX SBOM generation, artifact
  checksums, and GitHub build provenance attestations for tagged releases.

### Known limitations

- The first release publishes a Linux x86_64 GNU binary. macOS and Windows are
  supported through the locked source install path and verified in CI, but do
  not yet receive native archive assets.
- `egohygiene.io/identity` remains a separately deployed website integration;
  the static reference renderer is the release smoke surface.
