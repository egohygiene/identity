# Identity v1 consumer adoption

This is the golden path for adding a repository, product, or publication to the
Identity system after `v1.0.0`. It turns a one-off branding exercise into a
reviewable source-and-projection lifecycle.

## Outcome and authority

```text
consumer-owned .identity/ intent
          ↓ validate
human approval boundary
          ↓ generate
assets/identity/ projections
          ↓ verify
README, docs, release, site, and social consumers
```

The consumer owns canonical intent beneath `.identity/`. Identity owns the
compiler and projection contracts. Generated assets remain generated even when
committed or published. A renderer, website, agent, or downstream framework may
consume the package but may not silently redefine brand facts or approvals.

## 1. Define the bounded identity

Before selecting colors or drawing a mark, record:

- project ID, display name, repository, tagline, and product kind;
- purpose, audience, positioning, personality, and prohibited implications;
- the relationship to Ego Hygiene family defaults;
- required output profiles and explicitly inapplicable surfaces; and
- who has authority to approve source assets, token overrides, voice, and use.

Keep the result in `.identity/brief.md`. Branding should clarify the product's
actual boundary, not compensate for an unclear one.

## 2. Create canonical source

Adopt the v1 topology documented by
[`IDENTITY_V1.md`](../contracts/IDENTITY_V1.md):

```text
.identity/
├── identity.json
├── brief.md
├── defaults/organization.tokens.json
├── overrides/product.tokens.json
├── targets/profiles.json
├── governance/{approvals,provenance}.json
├── guidance/{voice,usage}.json
├── sources/
├── candidates/
└── references/
```

Snapshot organization defaults locally and pin their SHA-256 digest. Product
differences belong in the final override layer and require a reason plus an
approval identifier. Candidates and references are separate trust zones; do
not promote either by copying it into generated output.

## 3. Preserve human creative authority

Every public source asset requires first-party or licensed provenance, an exact
digest, meaningful alternative text, usage constraints, and a human approval
for the same subject. Token overrides, public voice, and usage guidance require
their own decisions.

Automation can validate evidence and render a candidate. It cannot invent an
approval, infer consent from a passing test, or turn an unreviewed candidate
into canonical intent.

## 4. Pin and validate the toolchain

Use an immutable Identity release. For `v1.0.0`, install from the locked source
tag or verify the attached Linux archive as described in the
[release guide](../releases/V1.md).

Run the standard-library validator from the same immutable release source:

```bash
python3 scripts/validate_identity.py \
  --repository-root "path/to/consumer" \
  --format "human"
```

If a consumer adopts an additive projection merged after the latest stable
release, pin the exact Identity commit and the SHA-256 digest of every consumed
script until that capability ships in a new release. Never curl a mutable
default branch in CI.

## 5. Generate and verify the Brand Kit

```bash
identity v1-generate --repository-root "path/to/consumer"
identity v1-verify --repository-root "path/to/consumer"
```

Generation writes transactionally beneath `assets/identity/` and never mutates
`.identity/`. Verification is read-only and fails when selected output is
missing, stale, or drifted.

Select only profiles the consumer needs. A repository-only tool commonly uses
`core`, `github`, `docs`, `tokens`, `metadata`, and `archive`, while declaring
`web`, `pwa`, and `social` inapplicable until those surfaces exist.

## 6. Add optional projections deliberately

Handbooks, Press Kits, social-surface packages, repository presentation, and
mascots are opt-in v1 extensions. Each has an independent source contract,
approval boundary, deterministic output, and consumer owner. Do not enable a
surface merely because Identity can render it.

Repository presentation additionally pins the exact proposed or active Hygiene
profile and consumes explicit evidence supplied by the repository. Identity
renders that state; it never evaluates conformance or claims certification.

## 7. Integrate downstream consumers

README files, documentation, release packaging, sites, and applications should
read generated descriptors or assets only. Keep authored prose outside
generated regions. Link machine claims to evidence, provide textual fallbacks,
and never make color, imagery, or animation the only carrier of meaning.

## 8. Block drift in CI

A consumer CI job should:

1. download or install the immutable Identity release;
2. verify release and any pinned-script digests before execution;
3. validate `.identity/`;
4. run `identity v1-verify` against committed generated output;
5. regenerate optional projections into a temporary directory;
6. compare their complete file trees or checksums with the committed package;
7. fail on any mismatch without rewriting the branch.

This keeps local generation, code review, and CI on the same contracts.

## 9. Upgrade and rollback atomically

For an upgrade, review upstream release notes and contract diffs, update the
immutable tool/profile pins and digests together, regenerate into a separate
directory, inspect visual and machine-readable differences, and publish only
after human approval.

For rollback, restore the prior `.identity/` source, external profile snapshots,
explicit evidence, and `assets/identity/` projections as one set. Re-run
validation and verification. Never repair generated output by hand.

## Consumer proof

Empathy and OptiFlow are the stable-release pilots. Mantle issue
[#27](https://github.com/egohygiene/mantle/issues/27) is the first post-v1
repository-fleet adoption: it uses governed source, the released compiler,
digest-pinned additive presentation scripts, explicit Hygiene evidence, and CI
drift detection without importing Identity internals.
