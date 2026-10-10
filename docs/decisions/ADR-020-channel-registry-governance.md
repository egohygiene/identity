---
schema: egohygiene.architecture-decision/v1
id: ADR-020
title: Separate channel governance, account lifecycle, and verification
status: proposed
date: "2026-10-10"
decision_scope: repository
visibility: public
owners:
  - egohygiene/identity
issue: https://github.com/egohygiene/identity/issues/65
pull_request: https://github.com/egohygiene/identity/pull/68
related: [ADR-013, ADR-015, ADR-016]
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/identity]
affected_contracts: []
implementation_status: implemented
evidence:
  - type: pull_request
    url: https://github.com/egohygiene/identity/pull/68
    description: Implements the canonical registry, independent lifecycle and verification, deterministic public adapters, and shared Press Kit/social consumption.
  - type: documentation
    url: https://github.com/egohygiene/identity/blob/8aae2c6767d07714ea16bf0ea493e1f1ac399b6e/docs/contracts/CHANNEL_REGISTRY_V1.md
    description: Inspected channel-registry source, projection, activation, rollback, and no-secrets contract.
  - type: implementation
    url: https://github.com/egohygiene/identity/blob/8aae2c6767d07714ea16bf0ea493e1f1ac399b6e/publication/channel-registry.v1.json
    description: Canonical source at the audit boundary records planned channels; source presence does not prove active accounts or architectural approval.
approval: null
exceptions: []
---

# ADR-020: Separate channel governance, account lifecycle, and verification

## Context

Press Kits, social packages, footers, and badges need consistent reviewed
account facts without confusing a planned channel with an existing account
or a verified account with an active one. The inspected
`identity.channel-registry-source/v1` contract implements this distinction.
ADR-016 assigns third-party platform facts to Aether; this additional choice
concerns consumer-owned account identity and its governed projections.

## Decision

Keep canonical public channel facts in the optional local registry selected
by `documents.channelRegistry`. Maintain separate governance, account
lifecycle, and verification states. Active accounts require canonical HTTPS
URLs; a verified claim requires public evidence. Only reviewed active accounts
with badge approval enter public badge and footer-link adapters.

Derive Press Kit social links and social-surface account bindings from that
same registry when adopted. Reject parallel authored social links rather
than permitting two competing URL sources. Keep credentials and recovery
secrets outside all Identity source and output. Registry adoption grants no
account-creation or platform-publication authority.

## Alternatives considered and rejected

The existing contract rejects parallel authored social links when a registry
is present, promoting inactive records into public adapters, and storing
recovery secrets in public metadata. No separate contemporaneous comparison
of competing registry designs was located. Their additional rationale remains
unknown rather than reconstructed from current code.

## Consequences and tradeoffs

Consumers share one URL and account-state source. Planned or unavailable
records remain inspectable while empty public adapters can truthfully indicate
that no channel is ready. Operators must separately review activation,
verification, icon rights, accessible labels, and governance. A declared
planned registry entry proves neither ownership of an external account nor
successful public verification.

## Implementation and evidence links

[PR #68](https://github.com/egohygiene/identity/pull/68) and the immutable
contract/source links above establish the bounded implementation. The
[contract guide](../contracts/CHANNEL_REGISTRY_V1.md) records the renderer,
activation steps, integrity package, and consumer rules. This reconstruction
does not create, access, activate, verify, or publish any external account;
historical test summaries are not a new validation run.

## Replacement or exit strategy

Upgrade the versioned source and projection contracts through a reviewed
migration that preserves channel IDs and explicitly translates lifecycle and
verification. Rollback restores source, approvals, version, and generated
outputs together. Retain deprecated and impersonation-risk history instead
of deleting it or silently recycling identifiers.

## Follow-up work

Obtain human disposition of this proposed architecture record. Any account
activation remains a separately authorized operation with current public
evidence and owner-reviewed registry changes.

## Reconstruction note

Reconstructed on 2026-10-10 from main revision
`8aae2c6767d07714ea16bf0ea493e1f1ac399b6e`. The source implementation commit
`60bcd9a8202ec054650bc6c0bea6fbe0349a75f0` is dated 2026-08-31. This is an
implementation date, not a proven human architectural disposition. No global
contract ID is invented for the existing `identity.*` source identifiers.
