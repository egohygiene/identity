# ADR-007: Separate font inspection, rendering, subsetting, and approval

- **Status:** Accepted
- **Date:** 2026-08-20
- **Issue:** [#7](https://github.com/egohygiene/identity/issues/7)

## Context

Fonts are both untrusted binary inputs and licensed creative works. Inspection,
text shaping, subsetting, and legal approval have different failure and
authority boundaries.

## Decision

Adapt Fontations `read-fonts`/`skrifa` for metadata inspection and use the font
stack selected transitively with `resvg` for rendering. Adapt an exactly pinned
fontTools `pyftsubset` subprocess only for profiles that request subsetting and
whose license evidence explicitly permits modification/subsetting.

Do not download fonts during a build. Canonical source identifies approved font
bytes and license evidence by checksum. Reject license inference from a family
name, provider URL, or embedded metadata alone. Defer a Rust-native subsetter
until corpus parity establishes equivalent OpenType behavior.

## Consequences

- Rendering and inspection remain native while mature subsetting remains
  available behind an isolated optional adapter.
- Python is not required for profiles that do not subset fonts.
- Subsetting failures cannot silently fall back to shipping an unapproved full
  font.
- Font fixtures need malicious-input, language-coverage, variations, shaping,
  and reproducibility tests.

## Exit strategy

Replace either inspection or subsetting independently through their ports. A
Rust subsetter can replace fontTools after matching the approved corpus,
metadata preservation, checksum stability, and license evidence behavior.

## Evidence

- [Google Fonts Fontations](https://github.com/googlefonts/fontations)
- [fontTools documentation](https://fonttools.readthedocs.io/en/latest/)

