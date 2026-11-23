# Declared source timestamp consistency — 2026-11-23

Issue: [#70](https://github.com/egohygiene/identity/issues/70), existing roadmap
step `IDN-Q28`. Base: `ad8fca58946ca03f6f07d13be6c64046216569d0`.
Code selection: `d159c680e6161e85854fd45c255d4196aec5c34f`.

The earlier approval repair required complete, offset-bearing date-time strings,
but other declared source timestamps still used Python's broader ISO parser.
Asset origin capture time was only checked for a nonempty string. Thus a source
could satisfy authoritative preflight with date-only, naive or coerced values
despite the curated schemas' `format: date-time` and existing RFC3339 diagnostics.

## Existing contract enforcement

The unchanged approval grammar/calendar check now lives in the canonical common
module as `valid_rfc3339_timestamp`. Approval validation retains its existing
`valid_review_timestamp` import facade. These source fields share that check:

| Source field | Existing diagnostic family |
| --- | --- |
| Approval `reviewedAt` | `IDN1404` |
| Asset origin `capturedAt` in `provenance.schema.json` | `IDN1405` |
| Governed guidance provenance `capturedAt` | `IDN1602` |
| Design-reference `capturedAt` | `IDN1702` |
| Channel registry metadata `reviewedAt` | `IDN2101` |

The shared guidance check reaches voice, usage, design-system principles and
capabilities, references, channel governance, Press Kits and social surfaces
through their existing callers. Existing code/path/recovery messages remain;
the newly enforced origin-string check uses the existing provenance family.
Missing, empty and non-string origins retain their earlier incomplete-origin
diagnostic rather than gain duplicate format findings.

The parser accepts `T/t`, `Z/z`, fractional seconds and explicit bounded offsets,
including `-00:00`; it checks calendar values without rewriting source strings.
It retains the existing Python calendar parser's leap-second limitation. This
is declared field validation, not an exhaustive RFC3339 engine or proof that
an asserted human/capture event occurred.

The generated standalone script is regenerated from canonical modules. It
remains standard-library-only and is the same script embedded by native
preflight. No schema identifier, network resolution, dependency or approval
policy changes.

## Actual validation

- Full Python suite: **238 discovered, 236 passed, two existing skips**, with
  actual Make and pinned Task3.45.3 available. The skips retain optional
  local-experience/native-Windows scopes.
- Focused validator/channel suites: **28 methods pass**. New controls exercise
  six capture bindings with five invalid and three valid forms, registry review
  and channel capture through the real projection CLI, no output on refusal,
  valid lowercase/fraction/offset forms and byte-preserved source. Existing
  approval grammar controls remain active.
- Full locked offline Rust suite: **119 passed, four explicit helper-only
  ignores**; all-target/all-feature strict Clippy and formatting pass. Native
  CLI generation, verification and library preflight now reject date-only and
  naive asset/guidance/reference captures before output/cache mutation. The
  changed source bytes and existing output sentinel remain preserved.
- [Twelve actual before/after controls](before-after.json) execute the immutable
  base and repaired standalone scripts with Python `-I -S` against disposable
  fictional consumers. Eight newly checked field bindings previously accepted
  a bare date and now reject it. Valid lowercase reference time now passes;
  date-only lifecycle, the approval facade and prior incomplete-origin
  diagnostics remain unchanged. Every consumer and the original fixture retain
  their source bytes.
- Standalone bundle drift, extraction/provenance, documentation and whitespace
  checks pass. Independent read-only source/tests review and separate actual
  before/after controls find no blocker. [Check identities and local binary
  hash](checks.json) retain exact inputs and raw-log hashes.

Tests and the local native build ran against candidate code bytes, subsequently
audited equal to the selected code commit. Later evidence/continuity changes
are not relabeled as a clean-source run or new native execution. The local
test binary is not a downloaded, signed or released installation.

## Boundaries and remaining work

Date-only channel lifecycle `since` and launch release `date` retain their own
contracts and implementations. Publisher/view-model origin strings whose
contract is only nonempty text also remain unchanged, including the existing
date-only Kern records. No historical time, timezone offset, human review,
source value or output is fabricated to satisfy the new checks.

The separate actual Identity proposal still has exactly its two missing-review
`IDN1404` findings; no owner selection or root adoption follows. Final merged
source/platform/install, local artifact-server, release and publisher acceptance
remain with #70/#98/#116 and their existing domain checkpoints. No hosted job,
publication, tag, deployment or issue closure is performed here.

Decision impact: reference accepted ADR-0005/ADR-0012 and existing human-owned
approval boundary ADR-0001. This completes declared offline semantic validity
rather than choosing a new data model or policy; no duplicate ADR or lifecycle
promotion. The pinned Aether decision2.1.0/continuity1.1.0 guidance at
`dc8a16851f452763ef4f7fbe4bf057d4500b1921` and Hygiene policy1.2.0 at
`a05b14f8b9e2772124f879f818e09a911e996ad8` were read through immutable source.
