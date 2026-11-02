# Optional release-announcement drafts

Candidate use case for [#106](https://github.com/egohygiene/identity/issues/106):
prepare a small release announcement for review when a project ships the next
version of its Brand Kit or software. The selection is proposed for maintainer
review; it is not an agreed campaign, scheduled post or new artwork request.

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
  "projectId": "example-product",
  "boilerplateId": "short",
  "assetIds": [],
  "release": {
    "version": "1.2.3",
    "date": "2026-11-02",
    "url": "https://example.invalid/releases/1.2.3",
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

The implementation is an unvalidated draft in this sprint. Focused regressions
are authored but unexecuted; run them and the source/projection suites during
the agreed quality sweep before adoption. The proposed
[ADR-0032](../decisions/ADR-0032-optional-launch-document-drafts.md) retains null
approval, and #106 remains open for consumer selection and acceptance.
