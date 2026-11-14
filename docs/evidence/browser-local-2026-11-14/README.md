# Actual local Docker qualification — 2026-11-14

Immutable source: `695f14c0c4f3b272b83b96619246eb981adaf6e5` (clean).
The managed authoring workspace ran native Linux/amd64 Docker 28.4.0 with the
unchanged digest-pinned Playwright image, font files, rendering settings and
approved PNG. This is a local-host run, not a GitHub-hosted replay.

Command: `python3 scripts/qualify_browser.py --mode local --proxy-ca
/etc/ssl/certs/ca-certificates.crt --output-directory <new-external-directory>`.

The complete [host receipt](host-qualification.json) and
[container receipt](qualification.json) pass. All sixteen hashed report,
log, trace and screenshot artifacts are retained under `browser-ba1WDi/`.
Their bytes were verified against the host receipt after copying.

- Positive: nine passed, zero skipped/retried/failed.
- Deliberate built-CSS inversion: the original screenshot assertion fails
  with the expected actual/diff PNG evidence; this is the required negative
  result, not an unrelated runner failure.
- Restored built CSS: the original screenshot passes.
- Actual browser executable/argv, direct-child ownership, fonts, locale,
  timezone, scale, viewport and sRGB settings are verified.
- Approved screenshot remains
  `53d7d144734ac63ceb730e95c7a39acc47d3fa64c5429f752233978289088543`.

Earlier attempts retain their actual failures in the work record: direct
Node font-fetch networking, optional Linux `/proc/.../children`, and exhausted
vfs build storage. The first runtime already passed all three visual phases
before process-metadata collection failed. Build-only proxy/CA forwarding and
PPid fallback repaired those observed compatibility issues. Only task-created
build caches were removed to recover capacity. No retry relaxation, baseline
update or tolerance change was introduced.

This completes #80's missing actual authoring-host Docker proof. Matching
current-source CI execution remains part of the requested later `act` campaign;
it is not supplied by changing the invocation label. #80 stays open for that
remaining CI acceptance. No release, deployment or human visual approval occurs.

ADR-Ref: egohygiene/identity#ADR-0011 (reference).

## Post-extraction qualification

The [renderer-source receipt](renderer-65807c6/host-qualification.json) and all
of its hashed artifacts are retained separately under `renderer-65807c6/`.
At clean source `65807c6d65238f280fd748cede6f4a6e48275bb5`, all nine positive
cases, deliberate screenshot failure and restored pass succeed with no retries
or skips. The same approved PNG, immutable browser/fonts/settings and strict
process ownership checks remain intact. Local vfs build layers were reduced;
this does not substitute for current-source CI execution.
