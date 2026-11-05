---
schema: egohygiene.architecture-decision/v1
id: ADR-0033
title: Prepare explicit v1 initialization candidates from local requests
status: proposed
date: "2026-11-05"
decision_scope: repository
visibility: public
owners: [egohygiene/identity]
issue: https://github.com/egohygiene/identity/issues/133
pull_request: https://github.com/egohygiene/identity/pull/138
related: [ADR-0001, ADR-0002, ADR-0003, ADR-0005, ADR-0012, ADR-0025]
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/identity]
affected_contracts: []
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/identity/issues/133
    description: Existing seven-criterion initializer scope, preserving manual authoring and v0 behavior.
approval: null
exceptions: []
---

# ADR-0033: Prepare explicit v1 initialization candidates from local requests

## Context

The current `init` command writes v0 source. Manual v1 authoring is supported,
but copying a fictional example can accidentally carry invented approvals or
rights into real source. Issue #133 asks for an explicit, separately reviewable
v1 candidate without implicit migration, installation or publication.

## Decision

Propose `identity v1-init --repository-root ROOT --request FILE
--output-directory DIR`. A closed, versioned local JSON request supplies
project facts, token-layer files and profile selection, or imports an existing
validated v1 source root. The initializer computes digests and writes a new
standalone candidate root plus an initialization report. Missing facts produce
an explicitly incomplete starter, never an approval or a valid-identity claim.

Use the existing authoritative stdlib validator for candidate diagnostics.
The Rust CLI embeds the initializer and validator and uses the existing v1
Python runtime boundary. It does not execute consumer code or acquire tools.
Canonical promotion remains a separate reviewed manual operation.

## Alternatives considered and rejected

- `init --schema-version v1`: considered during interface selection; the
  separate `v1-init` name matches the existing explicit v1 command family.
- Numerous fact/profile/source flags: a local request is easier to retain and
  review, while existing v1 documents remain the authority for rich material.
- Direct canonical initialization or an overwrite flag: this would conflate a
  starter with adoption and introduce implicit source-replacement authority.

## Consequences and tradeoffs

The candidate can be incomplete and fail ordinary v1 validation. Its report
distinguishes this from malformed requests, unsafe paths and execution errors.
An existing v1 import preserves exact source and approval subjects. It cannot
be combined with replacements that silently alter their meaning. The command
requires the already documented Python 3.11+ v1 runtime and remains offline.

## Implementation and evidence links

The [interface guide](../consumers/V1_INITIALIZATION.md), closed request/report
schemas, trusted standalone initializer and embedded CLI bridge implement the
candidate boundary in draft PR138. Syntax parsing and Rust compilation are
limited structural/build evidence. This source-preparation campaign defers
runtime tests, qualification and hosted CI; implementation is unqualified and
this ADR remains proposed with null approval. Package versions alone do not
identify a reviewed implementation revision.

## Replacement or exit strategy

Omit this optional command to continue manual v1 authoring. Removing it does
not change v0 initialization or the v1 source/generate/verify/recovery APIs.
Discard only an explicitly selected candidate; never clean canonical source
or another process's files as an initializer recovery action.

## Follow-up work

Finish the bounded #133 draft, then run its complete acceptance matrix in the
separate qualification campaign. Obtain human decision disposition separately
from implementation, merge, source validation and creative review.
