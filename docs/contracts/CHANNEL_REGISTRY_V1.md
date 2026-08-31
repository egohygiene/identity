# Identity v1 organization channel registry

## Status and ownership

This contract closes [issue #65](https://github.com/egohygiene/identity/issues/65).
Identity owns the versioned public facts for official Ego Hygiene social accounts
and community channels. Consumers own where generated links appear. Account
providers own their platforms, and private operators own credentials, recovery
codes, multi-factor authentication, and account-recovery procedures.

The first canonical registry is
[`publication/channel-registry.v1.json`](../../publication/channel-registry.v1.json).
It records X, Bluesky, Threads, Instagram, Pinterest, Mastodon, Discord, and
Open Collective as reviewed `planned` candidates. No handle or account URL is
invented, and no account is represented as active before a human review.

## Source contract

`identity.project/v1` may add `documents.channelRegistry`, a normalized local
path to `identity.channel-registry-source/v1`. Every channel records:

- stable channel and platform IDs plus the public platform label;
- canonical HTTPS URL and handle, or explicit null values before activation;
- ownership entity and a recovery-owner role;
- separate lifecycle and verification state;
- audience, purpose, content scope, locale, and accessibility/contact notes;
- badge label, reviewed icon source, and license metadata; and
- provenance and a matching `channel:<id>` approval.

Lifecycle is one of `planned`, `reserved`, `active`, `unavailable`,
`deprecated`, or `impersonation-risk`. Verification is independently one of
`unverified`, `pending`, `verified`, or `not-applicable`. This prevents an
active but unverified account from being mislabeled and keeps impersonation
risk distinct from deprecation or account unavailability.

An active channel requires a canonical HTTPS URL. A verified channel requires
public verification evidence. Only an active channel may approve a public
badge. The validator fails closed on duplicates, unknown fields, unsupported
states, missing approvals, unsafe URLs, or a public source that claims to store
secrets.

## Deterministic public projection

Run:

```bash
python3 "scripts/render_channel_registry.py" \
  --repository-root "path/to/consumer" \
  --output-directory "assets/identity/channels"
```

The generated package contains:

| Path | Purpose |
| --- | --- |
| `channel-registry.json` | Complete reviewed lifecycle view and active public projection |
| `channel-registry.md` | Maintainer review of lifecycle, verification, URLs, and badge state |
| `badges.md` | Accessible links for badge-approved active channels only |
| `footer-links.json` | Framework-neutral footer links for badge-approved active channels only |
| `channel-registry-manifest.json` | Source and file integrity evidence |
| `SHA256SUMS` | Checksums for immutable package contents |
| `channel-registry.zip` | Reproducible offline handoff archive |

Planned, reserved, unavailable, deprecated, and impersonation-risk records
remain visible in the maintainer projection, but never enter `badges.md` or
`footer-links.json`. Empty public adapters are an honest valid output.

## Press Kit and social-surface consumption

When `documents.channelRegistry` is present, the Press Kit derives all `social`
links from its approved active channels. Parallel authored social links are a
validation error. The social-surface projection attaches the active channel
whose reviewed platform label matches each catalog target, or explicit null when the registry has
no active account for that platform. Both projections therefore use the same
canonical URL, handle, accessibility label, verification state, and badge/icon
metadata.

The registry grants neither platform publication authority nor permission to
create accounts. Social-surface packages continue to set
`publicationAuthorized: false`.

## Account activation and migration

Migrate an existing account without changing its identity:

1. Preserve its current handle and canonical URL; do not rename the account as
   part of registry adoption.
2. Confirm the ownership entity and private recovery-owner role out of band.
3. Capture public verification evidence when available.
4. Change the lifecycle to `active`, update `since`, and approve the badge only
   after the URL, accessible label, icon source, and license are reviewed.
5. Add or supersede the matching `channel:<id>` approval, bump the registry
   version, validate, and regenerate all channel, Press Kit, and social outputs.
6. Review generated links and checksums before merging.

Rollback restores the previous registry bytes, approval set, version, and
generated outputs together. Deprecation and impersonation response are state
transitions, not deletion: historical IDs remain stable so consumers can
remove links without losing the governance record.

## Security boundary

The public registry records only a role such as
`organization-account-administrator` and a non-secret description of where the
private recovery procedure is maintained. Never store passwords, API tokens,
session cookies, private email addresses, recovery codes, MFA seeds, backup
keys, phone numbers, or security-question answers in Identity source or
generated artifacts.
