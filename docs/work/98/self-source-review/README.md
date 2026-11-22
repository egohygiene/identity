# Identity self-source review packet — 2026-11-22

This packet turns the confirmed owner choices into exact, reviewable assembly
inputs. It is **not adopted source, an approved token layer, a valid complete
Identity consumer, generated output or release evidence**. The existing
[candidate](../candidate/README.md) remains deliberately incomplete; its active
`layers` list and native approval/provenance arrays are unchanged.

The [owner answers](../OWNER_ANSWERS_2026-11-22.md) already settle the two master
selections, reviewer `szmyty`, logo-use terms/credit, lowercase name,
specification-first copy, voice/principles, palette/Inter direction and optional
Kern. Do not repeat those selection questions. Exact local token bytes, lookup
mapping, inheritance and record assembly were left for review.

## The concrete layer choice

Current v1 requires at least one `organization-defaults` layer followed by
exactly one final `product-override` layer. It has no standalone `local` layer
kind. That does not require pretending Identity's palette is an organization
standard.

| Option | Exact meaning and remaining review |
| --- | --- |
| **A: explicit empty inheritance, then Identity-local values** | Review a first snapshot containing **zero organization token values**, then a final local product layer containing the nine selected publication values. This is an explicit choice to inherit none for this consumer, not approval of an organization-wide palette. It is structurally supported by the inspected v1 schema/loader, but is not selected or adopted here. |
| **B: an actual reviewed organization snapshot, then Identity differences** | Identify and review the actual snapshot and byte pin. Compare every local path against it; each real replacement requires its own reason and same-subject `token:<path>` approval. No such snapshot or replacement approvals are invented in this packet. |

An unresolved organization source does not automatically select option A. Do
not give the existing nine Identity values an `organization-defaults` label
merely to make validation succeed.

Option A's exact files and proposed manifest fragment are:

| Staged review file | Proposed final path after review | Layer |
| --- | --- | --- |
| [organization-empty.tokens.json](layers/organization-empty.tokens.json) | `.identity/defaults/organization-empty.tokens.json` | `identity-empty-organization-defaults`, `organization-defaults`, priority `0` |
| [identity-local-product.tokens.json](layers/identity-local-product.tokens.json) | `.identity/overrides/identity-local-product.tokens.json` | `identity-local`, `product-override`, priority `10` |

The [proposed layer fragment](layers.proposed.json) pins both files by exact
SHA256. None of its declarations is installed in the active manifest. The first
layer adds no values; the final layer adds nine paths, so no inherited token is
replaced and no token-replacement approval is manufactured.

The [verification record](validation.json) lists all nine preserved type/value
records. The seven color values keep the exact publication decimal components
and alpha; the two font-family values remain
`["Inter", "system-ui", "sans-serif"]`. No font file, weight, metric, contrast
claim, gold role or motion token is introduced.

There is **one explicit lookup change**: publication `color.text` is represented
as DTCG **`color.text.default`**, retaining `color.text.muted`. DTCG cannot make
`text` both a token and the parent of `muted`. Review this mapping and update
actual consumers deliberately before adoption; it is not asserted compatible
with existing `color.text` lookups.

## Confirmed subjects and native record preparation

[governance.proposed.json](governance.proposed.json) binds the exact `mark` and
`horizontal-lockup` SHA256 values, reviewer, known review date, policy identifier
and credit. These are the already-confirmed visual selections, not new artwork.

The embedded native approval-document **drafts** deliberately have
`reviewedAt: null`: the actual chat review date is known, but its exact review
instant was not supplied. They therefore fail the existing date-time schema
at that field and are not copied into the active decisions array. A later
explicit review of the assembled packet can record its own actual timestamp;
do not fabricate midnight or substitute an artwork creation time.

Native provenance drafts preserve the selected policy and owner-reported
generated origin, but leave unreviewed `altText`, `safeZone` and `minimumSize`
null. They are visibly incomplete under the native schema. A visual master
approval does not approve newly written accessibility or usage wording. The
`capturedAt` value records preparation of this draft provenance, not the unknown
artwork creation date. Exact reference-kit/generation links and model/version
remain unidentified.

No approved-source copy or public download is introduced. The existing master
copies remain in `candidate/.identity/candidates/masters/`; the native
`sources/` area retains its current state.

[public-copy.proposed.json](public-copy.proposed.json) preserves the exact
confirmed copy, voice and principles without expanding them into invented
audience, localization or usage policies. Candidate voice/usage remain null.
The proposed product classification and core/tokens/metadata output selection
retain their existing review status.

The unchanged horizontal master still contains the old **“brand kit
generator”** tagline. The new **“project identity specification”** wording is
confirmed for project copy, but no altered visual master is approved by that
answer. Preserve the selected bytes; prepare any new-tagline derivative as a
separate review candidate before presenting it as the existing approved asset.

Kern keeps its independent source, CC-BY-4.0 attribution and existing approval
subjects. The generic native producer still rejects non-SVG provenance assets,
including PNG. This packet neither inserts Kern PNGs into native provenance nor
removes their governance to force a producer pass.

## What was actually checked

- The two proposed token documents and layer declarations pass their existing
  JSON Schemas.
- Isolated `load_layers` resolves exactly nine original type/value records,
  with zero replacements/override approvals. A deliberately wrong digest is
  rejected with `IDN1302`.
- Native approval/provenance drafts fail at their explicitly missing fields;
  the [record](validation.json) identifies those expected schema errors.
- The authoritative full check of the **active candidate** returns exit `1`,
  `valid: false`, and `IDN1301` at `/layers`. The validator made no input writes.

These are separate results. A component check of a proposed topology does not
prove authoritative project validity, organizational authority, producer
support, public-kit completeness, accessibility/contrast or release readiness.

## Next review and assembly

1. Review option A's explicit zero-value inheritance, or identify option B's real
   organization snapshot.
2. Review the exact nine-value document, `color.text.default` mapping and
   declarations/digests together. Already-confirmed colors and Inter direction
   need not be selected again.
3. Complete the timestamped packet review and actual accessibility/usage
   descriptor fields; retain distinct same-subject evidence. Keep any unknown
   source history explicit.
4. Confirm the final project classification/output selection and optional
   projections, then assemble the candidate without mutating existing root
   source or approved masters. Run the complete matching source validator,
   selected producer/output checks and real publisher handoff separately.

The [machine-readable review inventory](REVIEW.json) identifies exact inputs,
choices and readiness boundaries. This is review-only assembly under existing
ADR-0001/0004/0012 and the separately proposed ADR-0035 policy record; no schema,
runtime, ownership, release or ADR lifecycle changes occur here. The parent
[#98 packet](../OWNER_PACKET.md) retains actual source, qualification,
release/live/rollback and contrasting-consumer acceptance.
