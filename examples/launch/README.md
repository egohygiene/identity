# Release-announcement draft example

Selected first template for [#106](https://github.com/egohygiene/identity/issues/106):
prepare a Markdown release announcement from existing public Press Kit copy,
explicit release facts and one optionally selected asset. This is a complete,
fictional reference-consumer example; it is not a real project release or
approval to publish an announcement.

The source is the unchanged [expanded example](../v1/expanded/.identity/identity.json).
Its existing public `long` boilerplate explicitly describes the fictional
project, and its existing selected `mark` carries the example's rights and
usage records. All source reviewer, approval and rights information remains
synthetic. No new source fact, artwork or approval was added for this example.

## Inspect the input and output

- [Request](release-announcement.request.json): explicit project/copy/asset
  selection, synthetic version, date, release-note URL and changing claims.
- [Generated draft](release-announcement/release-announcement.md): the actual
  output of the optional command, including the draft notice and selected
  asset link, alternative text, rights and usage guidance.
- [Generated receipt](release-announcement/launch-document.json): exact request,
  source digest, selected public records and output hashes. It records `draft`
  status and contains no publication or claim-approval decision.

## Reproduce in a disposable consumer

From a reviewed immutable Identity checkout, copy the entire
`examples/v1/expanded` directory to a disposable consumer. Preserve its source
and select a new output directory. Run from the same Identity checkout:

```bash
python3 scripts/render_launch_document.py \
  --repository-root path/to/expanded-consumer \
  --request examples/launch/release-announcement.request.json \
  --output-directory build/release-announcement
python3 scripts/render_launch_document.py \
  --verify-directory path/to/expanded-consumer/build/release-announcement
```

The command needs Python 3.11+ and the matching Identity scripts. It performs
the existing source validation and Press Kit selection internally; no separate
native build, generated kit, model, network access or package installation is
needed to create this draft. The example's editor `$schema` references remain
checkout-relative hints; use matching immutable schemas for an independent
consumer as described in the [v1 guide](../v1/README.md).

## Required facts and optional selection

| Input | Responsibility |
| --- | --- |
| `schema`, `template` | Select the current `release-announcement` request contract. |
| `projectId`, `boilerplateId` | Match the consumer and an existing approved public Press Kit record. |
| `release.version`, `date`, `url`, `highlights` | Explicit project-owned facts; replace every fictional value before real use. |
| `assetIds` | Optional; omit or use an empty list for a text-only draft. Selected IDs must already be public Press Kit assets. |

For real use, author the request outside canonical `.identity/`, using actual
owner-supplied facts and existing reviewed copy/assets. A source approval for
brand material does not approve new release claims. Review voice, destination,
facts and rights before publishing through the project's chosen channel.

The [consumer guide](../../docs/consumers/LAUNCH_DOCUMENTS.md) describes output
ownership and the optional tool's full boundary. The
[delivery record](../../docs/work/106/CLOSEOUT.md) separates this generated
example from deferred regression/CI work and any future real-project adoption.
