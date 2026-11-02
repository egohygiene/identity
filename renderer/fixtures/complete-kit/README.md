# Complete kit renderer inputs

`inputs.zip` contains exact generated native files for three renderer cases:

- `minimal`: unchanged `examples/v1/minimal`, with optional public content absent.
- `expanded`: a disposable synthetic variant of the existing complete source
  fixture, using its governed handbook plus the existing Press Kit test helper.
  It selects the documented native web, GitHub, social and archive profiles.
  Its fictional approvals do not approve real project artwork or copy.
- `mantle`: unchanged `egohygiene/mantle` source at
  `b08045acc1e982dd9424c1d8c91b0badd64744e8`, retaining its actual selected
  outputs and supplied rights. No Press Kit or handbook facts are invented.

`receipt.json` binds every input/output hash, the actual native binary, exact
base source, raw-Git Mantle comparison and two independent native generations.
Native read-only verification passes and original sources stay unchanged.
The archive is test transport, not a new distributable product bundle or a
released/deployed kit. Renderer/browser runtime evidence is recorded separately.

Regenerate from the matching reviewed Identity native source with:

```bash
python3 renderer/fixtures/complete-kit/generate.py \
  --identity-binary "target/debug/identity" \
  --mantle-root "/absolute/path/to/pinned/mantle"
```

Only generated files enter the transport archive. The builder/verification tests
exercise all three complete native sets; the expanded browser case exercises
real static bundling, download bytes, keyboard use, accessibility, narrow layout
and essential content with JavaScript disabled. The receipt itself does not
claim those tests ran.
