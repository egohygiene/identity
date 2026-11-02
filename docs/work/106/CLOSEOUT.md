# Issue #106 selected template delivery — 2026-11-02

Reviewed Identity base: `f5fd0b03ebf5e0033725768b2e52088b3ddf88ea`.
Scope: [#106](https://github.com/egohygiene/identity/issues/106), with tests/CI
and broader quality work deferred by the maintainer.

## Selected use case

Prepare one optional Markdown release-announcement draft from existing public
Press Kit source and a separate explicit request. Under the maintainer's
instruction to execute this issue, the first concrete demonstration uses the
existing fictional expanded reference consumer. Its existing public `long`
boilerplate explains the fictional project, and its selected `mark` retains
its source bytes, alternative text, attribution, license and usage restrictions.
The request supplies explicitly fictional version/date/link/highlights.

The [complete example](../../../examples/launch/README.md) contains the actual
request, generated Markdown, selected SVG and draft-only receipt. No real
project's release, approval, rights or destination acceptance is invented.
Actual adopters must supply real facts and reviewed material. Additional
slide/document formats remain unselected possibilities, not promised outputs.

## Acceptance coverage

| Issue criterion | Delivered result |
| --- | --- |
| Select concrete requested templates | One release-announcement Markdown template and complete reference request/package are selected for this issue; other formats are not selected. |
| Reuse approved copy, voice, assets and presentation material | The tool reuses the existing governed example's literal public boilerplate and selected public mark/usage records. Fictional source approvals retain their example-only meaning; no new artwork or profile is introduced. |
| Keep changing facts project-supplied | Version, date, HTTPS URL and every highlight are explicit request fields outside canonical identity source. Nothing is inferred from Git, tags, the clock or a hosted release. |
| Demonstrate one selected use case with required/optional inputs | The sample command actually generated the checked-in package and its read-only verifier passed. The example documents every required field and the optional `assetIds` list/text-only form. |
| Preserve rights, approvals and audience | Existing public Press Kit selection supplies copy/assets; the artifact retains source digest, approval identities, bytes, alternative text and rights/usage. This does not turn synthetic evidence into real approval or authorize new claims. |
| Keep ordinary kit generation unaffected | The command remains opt-in; all runtime code, canonical examples, native/renderer workflows and normal kit interfaces are unchanged by this delivery. |

## Commands and represented evidence

The actual invocation used a disposable copy of the unchanged expanded source
and a new output directory, then copied the complete generated package into the
example. Machine-local paths are omitted. Equivalent public commands are:

```bash
python3 scripts/render_launch_document.py \
  --repository-root path/to/expanded-consumer \
  --request examples/launch/release-announcement.request.json \
  --output-directory build/release-announcement
python3 scripts/render_launch_document.py \
  --verify-directory path/to/expanded-consumer/build/release-announcement
```

Both commands exited 0. All 13 original input files remained byte-identical in
the disposable consumer and original example. The package contains three files:
`release-announcement.md`, `launch-document.json` and the selected SVG at
`assets/mark/example-expanded-mark.svg`. The source digest is
`aec3ea886ad78897341863ba9f567cb2582e21d99abf9ae795d3d4dc7a8afa98`.
The [bounded evidence](sample-generation.json) records exact input/request/output
hashes, the unchanged generator's Git blob/source revision and Python version.

This is actual example generation and local package integrity, not a full
regression result, authenticated publication record or real project adoption.
The fixture's synthetic approvals, dates, rights and contact information were
already present and were not amended for this demonstration.

## Deferred work and decision impact

The five existing `tests/test_render_launch_document.py` regressions and the
broader source/projection/consumer/native/browser suites remain unexecuted under
#70/#80. #70 explicitly retains the launch-tool selection, omission, path,
literal-text, deterministic, no-overwrite and tamper/failure checks. Existing
#98 retains its independent real self-source/rights/release/dogfood acceptance;
this example does not complete that work or add a new publication obligation.

Decision impact: append the dated demonstration outcome to proposed ADR-0032,
preserving its original rationale/metadata and null approval. The original
proposal suggested a real-consumer adoption follow-up; this selected delivery
is explicitly a fictional reference-use-case demonstration. Real adopters still
need their own facts and review. Issue completion does not accept the ADR,
publish a release or validate broader production behavior.
