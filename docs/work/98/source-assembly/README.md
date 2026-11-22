# Concrete Identity source assembly proposal

This packet fills the remaining descriptor choices with concrete wording. It
does not adopt source, change the selected artwork or record a human approval.
The [earlier layer packet](../self-source-review/README.md) and its exact
option A token files remain unchanged. The owner question selecting option A
or an actual organization snapshot is still pending.

## Proposed descriptors

Exact strings and source hashes live in
[DESCRIPTORS.proposed.json](DESCRIPTORS.proposed.json).

| Master | Proposed accessible description | Proposed digital guidance |
| --- | --- | --- |
| Emblem, 512 × 512 viewBox | Identity emblem: a vertical crystal prism surrounded by gold orbital rings. | Preserve the artboard; leave clear space equal to 1/8 of its displayed height (64 original SVG units). Recommended full-detail width: 64 CSS px. Review smaller contexts. |
| Horizontal lockup, 1200 × 400 viewBox | identity wordmark with crystal-prism emblem and the tagline “brand kit generator”. | Preserve the artboard; leave clear space equal to 1/8 of its displayed height (50 original SVG units). Recommended complete-lockup width: 600 CSS px; use the emblem in narrower layouts. |

The artboard sizes and existing tagline come directly from unchanged SVGs.
At 600 CSS px wide, the horizontal master's 28-unit tagline has a nominal
14 CSS px font size before font-specific metrics. The ratio and recommended
minimums are **new authored proposals**, not recovered approved policy or
measured WCAG/contrast/legibility results. They add no new legal condition to
the selected logo-use permission. Print minima remain unspecified.

The horizontal artwork still says **brand kit generator**. The already-selected
project-copy tagline is **project identity specification**; these records do
not silently replace the approved visual master's bytes or text.

## Proposed first output selection

[OUTPUTS.proposed.json](OUTPUTS.proposed.json) recommends `kind: product` and
the existing `core`, `tokens` and `metadata` profiles at `1.0.0`. Voice and
usage can initially remain `null` for the small executable core. This selection
is still for review; unselected presentation profiles are deferred rather than
declared permanently inapplicable.

For advertised downloads, the optional [usage.proposed.json](usage.proposed.json)
selects only the two unchanged governed SVGs as `identity-emblem.svg` and
`identity-horizontal-lockup.svg`. Every newly authored usage record remains
`candidate` with null approval. The generic public renderer withholds candidate
usage records. Nullable-core validity alone does not advertise asset downloads
or establish a complete public Brand Kit.

Kern remains a separately governed optional package; its PNG source is not
inserted into the generic native SVG-only producer. Unknown creation dates,
generation links/model and external reference-kit lineage remain unknown.

## Review and next assembly

The remaining response can cover this exact descriptor/output bundle together;
existing master/reviewer/copy/voice/principles/terms selections need not be asked
again. Review the independent inheritance/token question as well. Only an
explicit new packet review can supply its actual review timestamp and approve
these new descriptors or usage selection. A merge or the command to continue
engineering work does not select them.

The separate [assembled candidate](candidate/README.md) now places these files
in the existing v1 topology without altering root `.identity/`, the earlier
active incomplete candidate, original masters, runtime/schema contracts or ADR
dispositions. Its exact structural option is still **unselected**, and native
governance retains null timestamps. The matching authoritative validator
returns exactly two `IDN1404` findings at those `reviewedAt` fields. That narrows
the mechanical gaps; it does not select the pending layers, descriptors or
outputs on the owner's behalf.

The pinned local native test executable rejects both generation and read-only
verification before producing output, with the same missing-review diagnostics.
All 14 candidate files and the original active candidate remain unchanged.
[assembly-validation.json](assembly-validation.json) binds the actual commands,
local build/input identity, refusal results and candidate hashes. It is not a
successful source, release, downloaded-install or publisher receipt. No new
synthetic approval was inserted to force a successful producer run.

The proposal schema checks cover closed structure and known values. The local
Python JSON Schema installation has no registered `date-time` checker, so those
checks do not independently validate timestamp formats. A separate controlled
fixture probe exposed the existing approval parser accepting a bare date;
[the bounded finding](REVIEW_TIME_FINDING.md) records that issue for #70 rather
than using it to bypass the pending source review. Source validity, generation,
selected-output verification and real publisher acceptance remain separate.

Decision impact: reference ADR-0001/0004/0012 and proposed ADR-0035. These are
concrete review inputs under existing contracts, with no new runtime or policy
semantics selected.
