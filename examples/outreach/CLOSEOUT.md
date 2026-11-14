# Outreach examples acceptance — 2026-11-14

[#145](https://github.com/egohygiene/identity/issues/145) is implemented as
editable Markdown examples and an existing-workflow handoff. The
[guide](../../docs/consumers/OUTREACH_KITS.md) documents canonical governed source,
consumer-owned `campaigns/` drafts and separate generated review packages.

- The email provides recipient, subject, body, sender and campaign placeholders.
- The social kit provides maintainer/community, contributor/short-social and
  adopter/professional-network variants, reviewable links/hashtags, an existing
  approved visual reference, exact alt text, attribution and usage restrictions.
- The exact public `short` boilerplate is reused from the fictional expanded
  consumer. Other example wording is original draft copy. No upstream artwork
  or text is imported; the README attributes the Open Source Pledge references.
- The documented workflow was actually replayed in a new disposable consumer:
  Press Kit generation/read-only package verification and release-announcement
  generation/read-only inventory verification both pass. The two editable
  drafts were copied into its campaign directory. Documentation links pass.

The replay used the unchanged projection implementation from
`0ce87e35790dc224b04fae5176a676cf86b9b90f`; subsequent integration adds tests
and browser tooling without modifying those projection scripts. These synthetic
examples supply no real campaign facts, recipient list, asset rights, message
approval or publication. The consumer previews the exported Markdown and
chooses what to send or post.

ADR not required: documentation/examples reuse the existing Press Kit,
launch-document and source/approval boundaries without a new public contract.
