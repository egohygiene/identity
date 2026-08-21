# Identity v1 voice, usage, and guidance projections

## Source boundary

Every `identity.project/v1` source names two required, local guidance documents:

- `identity.voice/v1` records purpose, positioning, audience, personality,
  characteristics, contextual tone and mechanics, examples, anti-examples, and
  language coverage;
- `identity.usage/v1` records renderer-ready do/don't rules, current downloads,
  legacy assets, accessibility requirements, and legal/license notes.

Both documents are canonical consumer-owned source under `.identity/guidance/`.
The renderer reads them only after the complete project validates. It never
generates, paraphrases, or overwrites reviewed prose.

## Governance envelope

Every consequential guidance record carries the same envelope:

| Field | Meaning |
| --- | --- |
| `subject` | Exact content or reviewed bundle named by a decision |
| `state` | `candidate`, `approved`, `rejected`, or `superseded` |
| `visibility` | `public` or `internal` |
| `provenance` | Authorship/import/handoff method, source, and capture time |
| `approval` | Human decision ID, or `null` while still a candidate |

Candidates are internal and cannot claim an approval. Approved, rejected, and
superseded records must link to an `identity.approvals/v1` decision for the same
subject and state. A decision records the exact candidate, reviewer, review
time, evidence, notes, and any earlier decision it supersedes.

AI or another external creative provider can therefore contribute only a
`handoff-candidate` with visible provenance. A human decision must change its
lifecycle state before public guidance can include it.

## Context retrieval

Voice contexts use stable IDs such as `repository-readme` or
`incident-update`. Each context contains its audience, intent, tone,
characteristics, vocabulary, naming, capitalization, punctuation, examples,
and anti-examples. Usage rules independently name the contexts where they
apply; `all` is the explicit global selector.

The renderer's `--context` option selects one voice context and only the usage
rules that name that context or `all`. Consumer applications receive the same
selection through `identity.brand-guidance/v1` JSON.

## Renderer model

`identity.brand-guidance/v1` is a framework-neutral projection containing:

- project metadata and the optional selected context;
- foundation, characteristics, contexts, and localization;
- grouped usage sections plus a flattened `doDont` list;
- public, active, approved downloads;
- separately labeled legacy assets;
- accessibility and legal guidance;
- the complete human decision ledger.

Markdown and HTML render the same model. The HTML is static, semantic,
responsive, keyboard-visible, and reduced-motion safe. The later public
renderer can consume this model directly without parsing prose or changing the
authority model. CLI output defaults to the `public` audience, which removes
every internal or unapproved record and retains only decisions referenced by
the remaining model. The explicit `review` audience preserves the complete
lifecycle ledger for maintainers.

## Legacy policy

A legacy asset remains visible only as a labeled migration/history record. It
must name an active replacement and retain provenance. Internal or blocked
records disable their public download name. Public availability requires an
explicit approved/public governance record and stable download name. Promoting
it again therefore requires a new reviewed decision rather than editing the
generated view.

## Commands

Render the complete guidance model:

```bash
python3 scripts/render_guidance.py \
  --repository-root "path/to/consumer" \
  --format "json"
```

Retrieve one context as Markdown:

```bash
python3 scripts/render_guidance.py \
  --repository-root "path/to/consumer" \
  --context "repository-readme" \
  --format "markdown"
```

Inspect the complete internal lifecycle ledger:

```bash
python3 scripts/render_guidance.py \
  --repository-root "path/to/consumer" \
  --audience "review" \
  --format "html"
```

Write generated HTML outside canonical source:

```bash
python3 scripts/render_guidance.py \
  --repository-root "path/to/consumer" \
  --format "html" \
  --output "assets/identity/brand-guidance.html"
```

`--output` must be a normalized repository-relative path and cannot point
beneath `.identity/`.
