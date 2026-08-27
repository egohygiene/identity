# Support policy

## Supported environments

Identity v1 is a local CLI. The release gate executes the full test suite and
clean-room Brand Kit generation on each supported source-install environment.

| Environment | Install path | Evidence | Status |
| --- | --- | --- | --- |
| Ubuntu 24.04, x86_64 | Prebuilt archive or locked source install | Release and CI | Supported |
| macOS current GitHub-hosted runner | Locked source install | CI | Supported |
| Windows current GitHub-hosted runner | Locked source install | CI | Supported |

The prebuilt archive is deliberately limited to Linux x86_64 GNU for this
initial release. A platform is not a promise of a native binary: macOS and
Windows are supported from the audited source-install procedure below until
their archive packaging is separately validated.

## Getting help

Open a GitHub issue for reproducible defects, documentation gaps, or support
questions. Include the Identity version or immutable commit, operating system,
Rust version, command, non-sensitive diagnostics, and a minimal `.identity/`
fixture if one can be safely shared.

Do not include private brand source, unapproved creative candidates,
credentials, or personally identifying material in public issues.

## Compatibility and upgrade policy

- CLI, schema, package profiles, renderer model, and adapter boundaries follow
  semantic-versioning rules described in the v1 contracts.
- Consumers pin an immutable release tag or commit. They do not consume the
  mutable default branch.
- Upgrade by generating a plan, reviewing the resulting package/manifest, and
  committing or deploying the new generated state only after review.
- Roll back by restoring the prior immutable Identity release and its recorded
  generated package/manifest. Never manually edit generated output to emulate
  a rollback.

See [the v1 guide](docs/releases/V1.md) for exact commands and known
limitations.
