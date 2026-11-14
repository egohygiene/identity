# Portable entry point coverage — 2026-11-14

Base: `376232249209f3304843795f6113baf7dd504019`.
The actual shared helper is exercised through standalone Bash, Make and
checksum-pinned Task 3.45.3; no frontend reimplements setup policy.

## Actual checks

- Five protocol tests pass with both real frontends required. Each runs the
  actual helper in a disposable consumer using synthetic external tools.
  They assert repeated setup, frozen Cargo/pnpm arguments, activation and
  owned cache bindings, browser argument forwarding, unchanged consumer files,
  and rejection of a deliberately wrong pnpm version and unknown operation.
- Real `bash scripts/dev-env.sh setup` and `make setup` both pass with the
  pinned Rust 1.97.1/pnpm 11.21.0 tools, frozen dependencies and shared caches.
  Real `task browsers -- --dry-run` then passes without a TTY, reinstall or
  browser download. Source/lockfiles and unrelated files remain unchanged.
- The Task installer downloads only its exact official v3.45.3 Linux/amd64
  archive, verifies SHA-256
  `2c39d989ba8ab6ed37c025e9094e37240360fa2d69158504fc7a7486c88dc26f`,
  extracts the executable into the explicitly selected check-tools directory,
  and reports version 3.45.3. Its download is bounded to sixty seconds.
- Bash syntax, documentation and extraction/provenance checks pass.

## Demonstrated repairs

The helper now checks the activated pnpm version before dependencies/builds.
The injected `999.0.0` activation is rejected through all three frontends.

An actual Task invocation exposed pnpm 11's configuration-prefix and CI/global
virtual-store default differences: prepared dependencies attempted an implicit
reinstall and failed without a TTY. The helper now exports its owned store
using `pnpm_config_store_dir`, defaults global virtual store to false in both
contexts, and defaults dependency drift to an explicit error. Existing explicit
environment overrides remain supported. After these repairs, repeated real
setup and the ordinary non-CI Task dry run pass.

## Remaining acceptance

The normal validation workflow now installs the exact check-only Task binary
and requires actual Make/Task coverage in the existing Python test step.
No hosted workflow was dispatched. Current-source clean-base Docker and CI
execution remain for the requested later `act` campaign, alongside #80's CI
gate. #82 stays open; the implementation and local evidence do not claim that
remaining acceptance.

ADR not required: cover and repair the existing portable helper's version,
cache and dispatch behavior without changing product/source authority.
