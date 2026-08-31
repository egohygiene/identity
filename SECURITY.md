# Security policy

## Supported releases

Only the most recent stable `1.x` release receives security fixes. Release
candidates are evaluation builds and should be upgraded to the next stable
release or withdrawn rather than patched in place.

| Version line | Support |
| --- | --- |
| Latest stable `1.x` | Security fixes when a maintainable fix exists |
| `1.0.0-rc.*` | Evaluation only; no patch line |
| Earlier or untagged revisions | Unsupported |

## Reporting a vulnerability

Please do not open a public issue for a suspected vulnerability. Report it to
the Ego Hygiene maintainers through GitHub's private vulnerability-reporting
flow for [`egohygiene/identity`](https://github.com/egohygiene/identity/security/advisories/new).

Include the affected Identity version or immutable commit, operating system,
reproduction steps, impact, and any proof-of-concept needed to assess it.
Maintainers will acknowledge a report within seven calendar days, coordinate a
fix or mitigation, and publish an advisory when disclosure is appropriate.

## Supply-chain expectations

Release artifacts include SHA-256 checksums, an SPDX SBOM, and a GitHub build
provenance attestation. Verify those before installing a prebuilt archive.
The compiler is local-first and does not require credentials or a network
connection after its locked dependencies have been obtained.

## Social and community accounts

The public channel registry stores lifecycle, ownership role, public URLs,
verification evidence, and approved badge metadata only. Passwords, tokens,
session cookies, recovery codes, MFA seeds, backup keys, private contact data,
and provider recovery answers must remain in the private organization
account-recovery runbook. Registry `recoveryOwner` values name roles, never
credentials or private individuals' contact details.
