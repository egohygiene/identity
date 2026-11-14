# Optional typed review feeds in the existing Identity publisher

Refs [Relay #74](https://github.com/egohygiene/relay/issues/74),
[Relay #76](https://github.com/egohygiene/relay/issues/76) and
[Pace #13](https://github.com/egohygiene/pace/issues/13).

Identity's existing `Publish Identity Brand Kit` workflow can normalize supplied
public typed audit and architecture-review reports through Relay's shared
`repository-intelligence-review-feed` action. The exact immutable selection is
recorded in the workflow and the [current candidate guide](INTELLIGENCE_CANDIDATE.md).
Identity supplies its source and plan; Aether owns report semantics, Hygiene
owns public admission and human governance, Observatory owns normalization and
Relay owns the bounded action. Identity adds no parallel semantic code.

The release-backed Brand Kit, canonical host, existing deployment/recovery jobs
and source holds retain their own authority. This optional input cannot approve
assets, change an ADR lifecycle or authenticate a human decision. A normalized
review or successful upload is not publication or acceptance evidence.

## Select real checked-in source evidence

On a manual dispatch, `intelligence_review_plan` may select a canonical
repository-relative plan path. The default is empty, which skips normalization
and passes no review-model input to the builder. Existing native sources and
the default-off Compare mode keep their independent selections.

The selected path is admitted only when publisher, represented Intelligence
revision and workflow event SHA are the same current default-branch revision.
A release event, branch/head race or historical ancestor replay cannot select
this current review-feed path. Those existing paths keep their source behavior
when the new input is empty. Review selection is independent of enabling Compare.

The checked-in plan has exactly these fields:

- `schema`: `egohygiene.relay.typed-review-plan/v1`.
- `contract_version`: `1.0.0-alpha.1`.
- `visibility`: `public`.
- `repository`: `egohygiene/identity`.
- `audits` and `sanity`: arrays of report descriptors, each containing exactly
  `path` and the original file's lowercase SHA-256 in `sha256`.

Report paths end in `.json`, are unique across both arrays and are sorted by
path within each array. These are selected typed report files, not Markdown
documents for a new prose parser.

Plan and report paths refer to immutable Git blobs at the represented source
revision. Working-tree replacements, symlinks, path traversal and a matching
filename alone supply no source authority. The shared action performs source,
hash, size, schema, repository and public-scope checks; this workflow validates
only the path/context admission before invoking it. No request or report is
fabricated automatically, and no raw report is copied into the public site.

Original report clocks, scope and represented revisions remain unchanged.
Checking a report into a later source commit does not rewrite its subject: an
older-revision assessment remains historical context in the current projection.
No self-referential checked-in commit SHA, substituted current timestamp or
caller assertion upgrades it to a current assessment.

An empty array is a valid declaration that no selected report was supplied for
that owner model. It produces explicit unavailable evidence, never a clean
audit, zero-defect conclusion or human ratification. Missing/incompatible owner
evidence retains its actual unavailable/unsupported boundary. This wiring does
not run an audit, perform an architecture review or execute the organization
sweep.

## One source and evaluation boundary

Current Work/Health/Releases capture runs first, as before. Its actual returned
`as-of` is passed unchanged to the review-feed action, native builder and optional
Compare composition. The feed action receives the explicit source root,
repository and represented commit. It retains original source/report times;
normalization does not mint observations or human approval.

Normalized outputs live under `.cache/repository-review-feed`, separate from
the native builder's `.cache/repository-intelligence` work directory. The
builder's `observatory-audits` and `observatory-sanity` inputs receive only the
shared action's repository-model paths. Fleet models are retained as ordinary
review evidence; they are never passed into the repository builder. The source
plan, raw reports, runtime and operational receipts are outside the Pages tree.

The existing native ADR, Journey, Search and admitted dependency/provider
sources remain selected. Consumer alias composition and byte-preserved Brand
Kit verification run after the native build and optional Compare step. Final
composition, handoff and deployment verification consume the final tree and
manifest rather than an earlier builder digest.

## Retain ordinary evidence separately

The shared action's actual `artifact-directory` is uploaded as a separate
ordinary artifact. The upload may retain a bounded failure receipt when the
action had sufficient admitted context to emit one; a denied request never
supplies successful model paths. No output is invented when admission fails
before that context exists. A failure still prevents the publishing candidate
from advancing through its existing success gates.

On success, the feed receipt is also copied into the private deployment
handoff. `source-binding.json` records its actual receipt digest, upload ID/ZIP
digest, represented source, evaluation time and run/attempt separately from the
provider capture and Compare retention. These operational facts stay outside
`renderer/dist`; only the validated rendered owner views and their bounded
public provenance enter the existing site.

The ordinary artifact is review evidence, not an automatically selected fleet
source or cloud pointer. A later organization intake must select its exact
producer, revision, run/attempt, artifact and digests through its own reviewed
boundary. No latest/name lookup, report mutation, Pages uploader or deployment
authority is introduced here.

## Qualification and decision boundary

Source adoption is distinct from an executed feed, native build, artifact
upload, deployment or live verification. The user deferred tests, builds,
application/native/owner-helper execution, CI, provider calls and live checks.
Static source, YAML/Bash/Python syntax, exact selector preservation and peer
review are the available checks for this change. Real supplied-report admission,
freshness/failure behavior, retained evidence, rendered routes and recovery
remain later qualification work.

Decision-impact disposition: reference proposed
[ADR-0022](../decisions/ADR-0022-decisions-publication-composition.md) and the
accepted [ADR-0017](../decisions/ADR-0017-zensical-launchkit-publication-architecture.md)
composition boundary. This is routine adoption of an owner-defined bounded
input in the existing publisher; no new ownership or lifecycle decision is
introduced. Historical source receipts, ADR dispositions, release inputs and
the recorded recovery point remain unchanged.
