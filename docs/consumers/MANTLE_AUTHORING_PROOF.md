# Mantle authoring proof

This is #99 checkpoint 3's representative-consumer walkthrough. It applies the
[authoring worksheet](AUTHORING.md) to existing public source and records bounded
execution evidence. It creates no new brand facts, artwork, human approvals,
consumer pin changes, release or deployment.

## Immutable inputs and authority

| Input | Selected source and meaning |
| --- | --- |
| Real consumer | `egohygiene/mantle@b08045acc1e982dd9424c1d8c91b0badd64744e8` |
| Identity implementation | `egohygiene/identity@03eaeac72e2cf69c7bf205dd80f53ca25d1629e4`, including merged checkpoint 2 PR #117 |
| Canonical source identity | `fb5b86b632cb47eb160b13da92742687f5e76148b6d5300239a601b7d29147e8` |
| Declared profiles | `core`, `github`, `docs`, `tokens`, `metadata`, `archive`, each `1.0.0` |
| Inapplicable profiles | `web`, `pwa`, `social` |
| Existing consumer tool selection | Published compiler `v1.0.0` and additive scripts at `3c2fd3141371b355628e81f66f63159f19d63338`; this experiment does not update them |

The consumer's [manifest](https://github.com/egohygiene/mantle/blob/b08045acc1e982dd9424c1d8c91b0badd64744e8/.identity/identity.json)
supplies its actual name, repository, tagline and kind. Its local organization
snapshot and product layer own tokens and reviewed overrides. The provenance
and approvals documents bind the SVG mark's bytes, declared rights and six
existing decisions. Voice foundation/context source owns purpose, audience,
positioning and naming; usage owns the public mark selection and legal guidance.
Repository presentation is explicitly adopted. Press Kit, handbook, mascot,
social-surface and channel documents are absent.

These are preexisting **declared** approval records. Their references to closed
[Mantle #27](https://github.com/egohygiene/mantle/issues/27) are preserved; this
exercise checks their consistency and does not independently ratify creative
material or create a new approval.

The physical `.identity/` inventory contains 13 files. The canonical source
digest includes 11, excluding the candidate/reference README files under its
existing contract. A complete file-inventory comparison therefore supplements
the canonical digest when proving preservation; the two hashes are different
evidence, not interchangeable algorithms. The validator also consults the
declared vendored repository-presentation profile outside `.identity/`; the
proof inventory and raw Git comparisons bind all 14 input files.

## What was exercised

The [receipt](../evidence/identity-authoring-mantle-2026-10-19.json) records actual
binary/script hashes, source and generated inventories, outcomes and limits.
The new proof harness is identified by its own candidate-source hash; it is not
claimed to exist in the earlier implementation commit or to attest a released
binary build.

1. Validate the unchanged real consumer with the matching stdlib validator.
2. Generate the selected core outputs in two independent fresh disposable
   copies. Compare complete output inventories, including the hidden compiler
   manifest; an in-place incremental rerun alone would not prove fresh render
   determinism. Each fresh core tree contains 18 selected output files and
   the hidden manifest (19 files); the existing 42-file consumer tree also
   contains 23 separately generated repository-presentation files.
3. Independently cross-check each manifest output's path, byte length and SHA-256
   against actual files. The source selects six profiles; the generated renderer
   adapter is an additional compiler-owned projection, not a new authored fact.
4. Verify current outputs and prove verification changes no files. In separate
   disposable cases, remove one output, alter output bytes and append JSON
   whitespace to the canonical manifest while keeping old outputs. The last
   case changes source byte identity without inventing a fact. Each verify must fail and preserve the
   deliberately changed state rather than repairing it.
5. Compare the real consumer's existing generated tree and optional repository
   presentation with disposable regeneration. Core verification and optional
   package verification remain distinct operations.
6. Inspect public and review guidance. The baseline has 17 governed public
   records, two public contexts and one public mark download. Its public ledger
   includes only the two referenced voice/usage decisions; review retains all
   six existing decisions.

No consumer code or scripts are executed by the proof harness. Generation and
deliberate drift occur only in disposable copies. The supplied checkout's complete
worktree inventory outside Git metadata remains unchanged.

## Explicitly noncanonical probes

Three disposable omission variants set voice null, usage null, or both null.
They retain both physical guidance files and all existing approval records;
only the manifest declaration changes. Each validates, generates, verifies and
renders both audiences. Public governed-record counts are respectively seven,
ten and zero. Review retains the six historical decisions. These variants are
test inputs, not proposed edits to Mantle or new approved identities.
The adopted repository-presentation projection still runs when only voice is
null; it reports its existing usage prerequisite when usage is null. Its
declaration stays present throughout these tests.

A separate counterfactual changes the existing `command-plan` context's
visibility to internal. Validation still passes, public guidance omits that
context, and review retains it. No new content or approval is introduced.
This demonstrates the existing guidance boundary; generic renderer asset
selection still has the separately tracked G03 limitation.

Invoking the absent optional Press Kit or handbook projection fails with a
clear missing-adoption error. Their absence does not prevent the selected core
build. Their commands are not silently invoked by `v1-generate`.

## Reproduce the bounded proof

Use a checkout of the reviewed checkpoint 3 candidate for the proof harness,
and build its locked compiler. Record the actual checkout revision and binary
hash when rerunning; a later checkout is a new observation. Prepare a separate
clean Mantle checkout at the immutable consumer commit above. Do not run this
against an unreviewed identity or substitute a mutable default branch.

```bash
identity_source="$PWD"
consumer_checkout="path/to/clean-mantle-checkout"
identity_revision="$(git rev-parse HEAD)"
receipt_file="$identity_source/../new-authoring-receipt.json"

cargo build --locked --bin identity
python3 "$identity_source/scripts/verify_consumer_authoring.py" \
  --repository-root "$consumer_checkout" \
  --identity-binary "$identity_source/target/debug/identity" \
  --consumer-repository "egohygiene/mantle" \
  --consumer-revision "b08045acc1e982dd9424c1d8c91b0badd64744e8" \
  --identity-revision "$identity_revision" \
  --receipt "$receipt_file"
```

The harness is offline and requires local reviewed inputs. It emits bounded
development evidence, not a new EgoLint report contract or publication artifact.
Its receipt destination must be outside the supplied consumer and source trees.
Its file-tree digest follows the existing release-smoke framing; it is not the
canonical Identity source digest.

For the separately adopted repository-presentation package, use the real
consumer's evidence file with an absolute path. That argument resolves from the
shell's working directory, while the source manifest's paths are consumer-relative:

```bash
consumer_copy="path/to/disposable-mantle-copy"
evidence_file="$(cd "$consumer_copy" && pwd)/evidence/repository-presentation.json"
presentation_output="path/to/disposable-presentation-output"

python3 scripts/render_repository_presentation.py \
  --repository-root "$consumer_copy" \
  --evidence "$evidence_file" \
  --output "$presentation_output"
```

Compare the complete regenerated package against the selected committed package,
including file inventory and bytes. Core `v1-verify` does not verify this optional
package merely because it shares the generated root.

## Completion and remaining owners

The archive's additional PWA/social entries reproduce its documented
[portable representative bundle](../contracts/BRAND_KIT_PACKAGES_V1.md#deterministic-archive).
The compiler manifest, rather than the archive index, owns the exact selected
build. This is documented existing behavior, not a new subset-generation defect.

This proof establishes the authoring and selected-output path for the pinned
consumer. G03 generic internal asset selection and G04 advertised-but-unselected
archive remain #101/#105. Actual rights presentation, visual acceptance, complete
public-kit assembly, self-adoption, new release, publication and contrasting
consumer upgrade remain #100–#105/#98 as scoped by the roadmap.

The [initialization and validation handoffs](INITIALIZATION_AND_VALIDATION_HANDOFFS.md)
record the supported manual v1 route, v0 CLI limits, future initializer acceptance
and proposed EgoLint owner coordination. They establish no installed adapter,
universal policy gate or automated v1 initializer. With these evidence and
handoff boundaries, #99 can complete after review; the operational next issue
is transaction-path confinement #78.

Decision impact: reference ADR-0012, ADR-0013, ADR-0019 and proposed ADR-0025.
Execution and evidence do not promote any decision lifecycle.
