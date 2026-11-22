# Approval review-time enforcement — 2026-11-22

Issue: [#70](https://github.com/egohygiene/identity/issues/70). Base:
`75ca39f3fc7e5e9e0b5578af58c966cd2590a652`.

The real self-source assembly exposed a source-validation defect:
`reviewedAt` is a string with JSON Schema `date-time` format, and the existing
diagnostic/recovery contract requires an RFC 3339 timestamp with an explicit
offset. The implementation coerced arbitrary values through `str()` and used
Python's broader ISO parser. Date-only, numeric basic dates, naive times,
week dates and nonstandard separators could pass; valid lowercase UTC notation
failed. An absent optional JSON Schema format checker cannot supply this
required authoritative semantic check.

The canonical governance module now checks the actual string and complete
ASCII date/time grammar before calendar parsing. It accepts `T/t`, `Z/z`,
fractional seconds and explicit bounded `HH:MM` offsets, including `-00:00`.
It does not invent a narrower maximum real-world timezone policy. Offset
minutes cannot normalize from invalid `60` or `99` values into another offset.
Source strings are validated without rewriting them. Existing `IDN1404`
diagnostics, public entrypoints and schema remain unchanged.

The generated standalone validator is rebuilt from its canonical modules, so
the offline copied script and Rust's embedded preflight use the same repair.
No optional package or network access is needed for timestamp validation.

## Actual verification

- Full standalone-validator fixture suite: 16 test methods pass, including
  eighteen invalid and seven valid timestamp subcases through the complete
  validator. Approval bytes remain unchanged.
- The [before/after probe](before-after.json) executes both immutable original
  and repaired standalone scripts with Python `-I -S` against disposable
  fictional fixture copies. It records the old acceptance of date-only/numeric/
  naive values, corrected lowercase UTC handling, and calendar/offset controls.
- Full Python suite: **212 discovered, 210 passed and two existing skips**.
  Actual Make and pinned Task were available. The skips retain their optional
  local-experience and native-Windows scopes.
- Locked offline native Rust suite: **119 passed, four helper-only ignores**;
  formatting and all-target/all-feature strict Clippy pass. The existing actual
  CLI/library no-mutation regression now includes date-only and naive approval
  values, rejecting generation and verification before source/cache/output
  mutation. The ignores are not counted as independently passing product cases.
- Standalone bundle drift, extraction provenance, documentation and whitespace
  checks pass. Independent read-only review found no blocker in grammar,
  calendar constraints, source preservation or the offline boundary.

## Limits and decision impact

This repair checks **approval `reviewedAt` only**. Other explicitly formatted
date-time fields retain their existing implementations and need their own
bounded checks; date-only lifecycle fields must not be swept into this policy.
Python's existing calendar parser rejects leap seconds, and this checkpoint
does not claim exhaustive leap-second support or verify that an asserted human
event actually occurred.

Unknown actual review times stay unknown. This is not permission to fill the
real Identity source's pending timestamps, select layers, approve new usage
descriptors or adopt root source. No historical receipt, source artwork, native
platform claim, release or deployment changes.

Decision impact: reference existing ADR-0001/ADR-0005 and the declared approval
schema. This implements existing validity requirements rather than a new
approval policy; no duplicate ADR or lifecycle promotion is needed. The pinned
Aether decision/continuity workflow remains unchanged.
