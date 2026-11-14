# Optional outreach email and social kits

Use the [editable email and social examples](../../examples/outreach/README.md)
for a launch or campaign. This implements the bounded template scope of
[#145](https://github.com/egohygiene/identity/issues/145) through the existing
Press Kit and launch-document workflow.

## Source and draft ownership

Keep reusable voice, approved copy, links, visual assets and rights in the
consumer’s existing `.identity/` documents. In particular, `documents.pressKit`
selects the governed public source for boilerplates, links and assets;
`documents.guidance.voice` and `usage` retain their existing ownership.
Do not add invented email/social fields to those closed contracts.

Keep editable campaign files outside canonical source, for example:

```text
campaigns/launch-name/
  email.md
  social-kit.md
```

These are consumer-owned working drafts. Recipient details, subjects, campaign
facts, benefits, calls to action, links and hashtags require actual supplied
values and editorial review. A public boilerplate’s existing approval does not
approve newly written campaign claims. Keep recipient lists/contact details in
the consumer’s chosen private workspace when they are not intended for Git.

Generated approved source packages remain separate under `build/outreach/`.
No email is sent, account accessed or post published by copying these files.

## Export and preview a complete fictional example

From an immutable Identity checkout, choose a new disposable consumer path:

```bash
consumer=/tmp/identity-outreach-example
cp -R examples/v1/expanded "$consumer"
python3 scripts/render_press_kit.py --repository-root "$consumer" \
  --output-directory build/outreach/press-kit
python3 scripts/render_press_kit.py \
  --verify-directory "$consumer/build/outreach/press-kit"
mkdir -p "$consumer/campaigns/example-launch"
cp examples/outreach/email.md examples/outreach/social-kit.md \
  "$consumer/campaigns/example-launch/"
```

Inspect the exported Press Kit Markdown/JSON, its selected asset bytes, source
rights and approval subjects. Fill the placeholders in the two campaign files,
copy the exact selected public boilerplate, and point the draft’s visual
reference at the selected asset. Open the Markdown drafts in the consumer’s
ordinary Markdown preview to review email subject/body and each social variant.
The files themselves are the editable export; no new renderer, template
language, source schema or publishing integration is required.

To include a source-bound release-announcement draft in the same review:

```bash
python3 scripts/render_launch_document.py --repository-root "$consumer" \
  --request examples/launch/release-announcement.request.json \
  --output-directory build/outreach/release-announcement
python3 scripts/render_launch_document.py \
  --verify-directory "$consumer/build/outreach/release-announcement"
```

The release request explicitly contains fictional facts. Supply actual release
facts in a separate request for real use; the [launch-document guide](LAUNCH_DOCUMENTS.md)
explains its source/receipt/no-overwrite boundary. These existing commands
validate and export local material, and never send an email or publish a post.

## Use with a real consumer

Use its actual governed source and select only public approved boilerplate,
links and assets. Omit a missing optional visual rather than borrowing the
example’s rights or making one up. Review actual destination length, crop,
contrast, alt text and rights before export/use. Suggested channel labels and
hashtags are editable campaign choices, not a new external platform registry.

The [example README](../../examples/outreach/README.md) attributes the upstream
Open Source Pledge resources that inspired the structure. The example copy is
original and the visual reuses Identity’s existing synthetic sample asset.
