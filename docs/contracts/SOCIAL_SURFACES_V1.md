# Identity v1 social-surface projection contract

## Status and ownership boundary

This document defines the contract slice for
[issue #52](https://github.com/egohygiene/identity/issues/52). Identity maps
reviewed brand inputs onto explicitly selected social surfaces. It does not
own third-party platform facts, fetch the web, render final platform media, or
publish to an account.

[Aether](https://github.com/egohygiene/aether) owns the reusable
`aether.social-surface-catalog/v1` fact contract and collection skill. Identity
accepts a catalog only as an external, repository-local build input with an
exact ID, semantic version, and `sha256-utf8-lf` digest lock. A human or
consumer-owned design/publishing tool owns final rendering, current-fact
verification, upload, and publication.

## Optional canonical source

`identity.project/v1` may add `documents.socialSurfaces`, a normalized local
path to `identity.social-surface-source/v1`. Existing consumers remain valid
without it. The source contains four distinct decisions:

1. `catalog` locks the exact Aether artifact supplied outside `.identity/`.
2. `organizationDefaults` maps stable Aether record IDs to existing approved
   public Identity assets and closed project metadata selectors.
3. `project.adopt` explicitly opts into each default; there is no implicit
   platform matrix.
4. `project.exclude` and `project.overrides` record bounded, separately
   approved product decisions.

Defaults, adoptions, exclusions, and overrides require matching approved
decision subjects. An override can change only `sourceAssetId`, `copySource`,
or `linkSource`; it cannot edit platform dimensions or other Aether facts.
Copy selectors are limited to `project.displayName` and `project.tagline`, and
the only link selector is `project.repository`. Identity therefore reuses
canonical facts instead of accepting parallel social-only prose.

## Catalog admission and validation

The compiler performs no network requests. The pinned catalog must:

- use `aether.social-surface-catalog/v1`;
- match the selected ID, version, and normalized text digest;
- be `stable`, rights-review `approved`, and release-included;
- contain each selected record exactly once; and
- provide stable dimensions for every adopted active surface.

Identity validates the mapped asset through its existing usage, approval,
provenance, license, accessibility, and byte-digest boundary. Missing artwork,
dimensions, metadata selectors, or approvals fail closed. Nullable Aether
constraints remain null. An unknown safe zone is emitted as `unknown` with a
renderer note; Identity never draws a plausible fictional boundary.

The repository fixtures use synthetic, first-party records for a profile
image, profile header, and organic post. They prove contract behavior without
vendoring or implying redistribution rights for live third-party source packs.
The rights-rejected metadata-only Aether release is intentionally unsuitable
for production projection until independently gathered official records pass
review.

## Generated package

When `documents.channelRegistry` is present, every generated target consumes
the approved active channel with the same reviewed platform label. The target
contains that canonical channel record, or explicit null when no account is
active; planned or withheld channels never become publication links.

Run:

```bash
python3 "scripts/render_social_surfaces.py" \
  --repository-root "path/to/consumer" \
  --output-directory "assets/identity/social-surfaces"
```

The output is deterministic and contains:

| Path | Purpose |
| --- | --- |
| `social-surfaces.json` | Complete renderer-neutral package view model |
| `social-surfaces.md` | Human review of selections, dimensions, and unknowns |
| `targets/<selection>.json` | Exact per-surface constraints and brand mapping |
| `inputs/<asset>` | Approved canonical Identity input copied by digest |
| `press-kit-handoff.json` | Closed, publication-denying Press Kit handoff |
| `social-surfaces-manifest.json` | Source, catalog, and file integrity evidence |
| `SHA256SUMS` | Checksums for immutable contents |
| `social-surfaces.zip` | Reproducible offline handoff archive |

Every target preserves the Aether source URL and capture metadata,
verification state, lifecycle, dimensions, media constraints, safe-zone state,
Identity asset provenance/license/accessibility data, and the exact approvals
that authorized the mapping. The package records a freshness warning and
`publicationAuthorized: false`.

## Press Kit consumption

The Press Kit compiler can verify and include the generated archive without
reading parallel brand facts:

```bash
python3 "scripts/render_press_kit.py" \
  --repository-root "path/to/consumer" \
  --social-surfaces-directory "assets/identity/social-surfaces" \
  --output-directory "assets/identity/press-kit"
```

It checks the handoff and manifest schemas, project ID, current canonical
Identity digest, catalog identity, fixed package paths, archive path safety,
and each manifested file digest and byte count. A stale, mismatched, damaged,
or publication-authorizing handoff fails closed. The verified archive is then
listed and checksummed as `social/social-surfaces.zip` in the Press Kit.

## Catalog updates, rollback, and versioning

Treat a catalog update as an explicit review event:

1. Obtain a new Aether release artifact through the governed collection
   process and place it at the consumer-owned input path.
2. Review changed records, rights status, lifecycle, source capture, and every
   selected surface.
3. Update the catalog ID/version/digest lock together; never update only a
   digest to silence validation.
4. Run Identity validation and regenerate the social package.
5. Review the target diff, then regenerate any consuming Press Kit.
6. Publish only through a separate human-approved consumer workflow.

Generated artifacts are immutable snapshots, so rollback restores the prior
catalog artifact, source lock, approvals, and last accepted package together.
Additive optional fields may remain in v1. Renaming fields, changing selector
meaning, weakening catalog admission, or granting publication authority
requires a new contract major and migration guidance.

## Non-goals

- platform credentials, account provisioning, scheduling, or posting;
- ad buying, targeting, analytics, or campaign optimization;
- live specification scraping during Identity validation or generation;
- raw third-party source-pack or SVG-template redistribution; and
- automatic copy, artwork, constraints, safe zones, or approvals.
