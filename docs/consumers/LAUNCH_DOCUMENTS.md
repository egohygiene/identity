# Optional release-announcement drafts

Selected first use case for [#106](https://github.com/egohygiene/identity/issues/106):
prepare a small Markdown release-announcement draft from existing governed
Press Kit material and explicit project-supplied changing facts. The
[complete reference example](../../examples/launch/README.md) includes the
request, actually generated draft, receipt and one selected unchanged asset.
It uses the existing fictional expanded consumer; no real project's release,
rights or claim approval is inferred from the example.

The opt-in, standard-library Python tool reuses the project's existing approved
public Press Kit source. It selects exact boilerplate and optional existing
asset records; it does not rewrite brand copy, generate promotional claims,
choose a release version/date, or change ordinary Brand Kit generation.

## Inputs

The consumer must already adopt a valid `documents.pressKit` and its existing
governed usage/rights source. Missing, internal, candidate or unselected copy
and assets are unavailable to this tool. Author them through the existing
[worksheet](AUTHORING.md), with real owner review, rather than manufacturing
approval to make this command run.

Supply a separate request, outside canonical brand source. The
[request schema](../../contracts/v1/launch-document-request.schema.json) is
closed; one template is supported:

```json
{
  "schema": "identity.launch-document-request/v1",
  "template": "release-announcement",
  "projectId": "example-expanded",
  "boilerplateId": "long",
  "assetIds": ["mark"],
  "release": {
    "version": "0.1.0-example",
    "date": "2026-11-02",
    "url": "https://example.invalid/example-expanded/releases/0.1.0-example",
    "highlights": ["A synthetic, project-supplied release claim for review."]
  }
}
```

This is deliberately synthetic. Replace the project/boilerplate selection and
all release facts with the actual owner's inputs; the sample supplies no
approval or real publication claim. `assetIds` is optional and refers only to
selected public Press Kit asset IDs, not arbitrary files or a new asset type.
The tool never infers facts from Git history, moving tags, a registry or a date
on the local machine. It performs no network requests.

## Generate and inspect

From the same reviewed Identity checkout used for the consumer's projections:

```bash
python3 scripts/render_launch_document.py \
  --repository-root path/to/consumer \
  --request path/to/project-supplied-release.json \
  --output-directory build/release-announcement-draft
python3 scripts/render_launch_document.py \
  --verify-directory path/to/consumer/build/release-announcement-draft
```

The output directory is relative to the consumer and must be new. Canonical
`.identity/`, symlink-traversing destinations and existing outputs are refused.
There is no implicit cleanup or replacement. An interrupted output has no
complete receipt and requires inspection before removing only owned files.

The result contains `release-announcement.md`, explicitly selected asset bytes
and a [draft receipt](../../contracts/v1/launch-document.schema.json). The
receipt binds the source digest, selected public boilerplate/approval, asset
rights and exact request to every output file. Verification checks inventory,
hashes and deterministic prose reconstruction; extra files, tampering and
non-draft receipts reject. It proves local integrity, not authentication,
creative acceptance, truth of changing claims or release publication.

The Markdown carries a visible draft notice. Selected assets retain exact
bytes, alternative text, attribution/license and usage restrictions. A text-only
request omits the asset section and creates no placeholder. Supplied prose is
escaped rather than evaluated as Markdown/HTML instructions.

## Review boundary

Review version, date, link, every changing feature claim, voice/tone, copy and
asset suitability for the actual destination. The owner must approve the final
announcement and perform any posting through its existing channel. Brand-copy
approval is not approval of new release claims. This tool supplies no scheduler,
publishing API, social catalog admission, presentation framework or CMS.

The 2026-11-02 [delivery record](../work/106/CLOSEOUT.md) records actual sample
generation and read-only package verification using the existing tool. These
are the selected use-case demonstration, not a regression-suite or general
production-adoption result. The five authored regressions and broader
source/projection/native/browser checks remain deferred under #70/#80.

The selected scope is this optional Markdown template and reference package.
Real adoption requires real owner-supplied facts and reviewed source; other
document/presentation formats remain future choices when requested. The
proposed [ADR-0032](../decisions/ADR-0032-optional-launch-document-drafts.md)
retains null approval with a dated demonstration outcome. No posting or
formal ADR acceptance is supplied by issue completion.
