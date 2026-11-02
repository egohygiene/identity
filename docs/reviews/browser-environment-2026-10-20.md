# Browser environment qualification — 2026-10-20

Issue [#80](https://github.com/egohygiene/identity/issues/80), from merged #122
at 2d18ed114d3799da3867260d69d8c70bf05d428d.

## Scope and authority

This candidate implements the accepted ADR-0011 browser-environment requirement.
One digest-pinned Playwright 1.62.1 Noble profile fixes browser/system-font bytes
and rendering settings for the documented local command and both browser CI
gates. The approved PNG is preserved exactly; tolerance and manual baseline
approval remain unchanged. All 26 ADRs and their dispositions remain unchanged.
Decision operation: reference egohygiene/identity#ADR-0011.

## Registry and baseline identity

The [registry observation](../evidence/identity-browser-registry-2026-10-20.json)
binds official OCI index
sha256:dcc5531e97840b9b5e794f2814476b21571c5124a3fca2267d73041f56e7580e
to selected Linux/amd64 manifest
sha256:c091b21d9fae78c76e85cd4356431e9b018402f172a214fc7d7a5e9a7e29d8ac
and config
sha256:fee853fafa59550d162cef52bca02d907694b44ebf6ef9fb075bcc0c65d8dedb.
Raw bytes matched their SHA-256 identities. Immutable upstream source is
microsoft/playwright@26a9e470a7b3c7822084b09fb7f13902c5f37b51; its browser
metadata declares Chromium/headless-shell revision 1234/version 151.0.7922.34.

The baseline remains 149285 bytes, 1440×1000, SHA-256
53d7d144734ac63ceb730e95c7a39acc47d3fa64c5429f752233978289088543,
last changed by human commit 85f650f936950094a608f5c477b9a59d4be29a87.
No baseline bytes or comparison tolerances change.

## Executed validation

Local checks pass: 300 renderer unit cases (including 21 browser-proof boundary
cases), 24-file source check, build/public validation; 148 Python cases with 146
passes/two existing skips; six standalone verifiers, compilation and whitespace
checks. Independent review verifies the package/file identities and the
positive/negative report guards. Host checks do not establish an image pass.

The initial official image executes five functional checks but fails the
unchanged approved screenshot by 78,987 pixels in
[run 39429093327](https://github.com/egohygiene/identity/actions/runs/39429093327)
at source head b0eb3c414aec4c22c8b376f54b04eafe5081d200. Its retained actual/diff
images show different text weight and wrapping. A subsequent diagnostic run
records generic sans and Inter fallback to WenQuanYi Zen Hei, with no DejaVu
font files installed. Historical human font metadata was not recorded; baseline
pixel/metrics comparison suggested DejaVu Sans, to be verified by the unchanged
assertion rather than treated as historical fact.

The qualified image now adds intact fonts-dejavu-mono and fonts-dejavu-core
2.37-8 packages from the official Noble archive. Both downloads match official
package metadata, exact byte counts and SHA-256 before installation; all eight
extracted font hashes match the profile. The
[source receipt](../evidence/identity-browser-fonts-2026-10-20.json) retains the
metadata, license and signature-verification limit. Runtime font guards record
and check actual installed packages, font bytes and Fontconfig configuration.
This repairs the environment while preserving product CSS and the approved PNG.

Earlier harness failures (strict pnpm metadata resolution, public evidence
directory permissions, preview log parsing and a CDP command requiring an unset
automation flag) are not counted as qualification. Corrected probes resolve the
declared dependency chain, use readable synthetic output, probe actual HTTP and
inspect only this qualifier's newly launched browser child without changing
browser flags.

Actual pinned-image qualification passes at source head
c2107af9244d16a8f1511f28a5f71ce8d5a19729, represented merge candidate
2a15468bc4b0da8272316fb1bd7fad5ecd0b5056:

| Execution | Actual proof |
| --- | --- |
| [Reference CI and default local-entrypoint replay](https://github.com/egohygiene/identity/actions/runs/39431712372), job 118658145375 | Both pass six positive checks, one required screenshot-comparison failure and one restored-baseline check. |
| [Release browser smoke](https://github.com/egohygiene/identity/actions/runs/39431711965), job 118658139539 | The same positive/negative/restored proof passes in CI mode. |

Every phase has zero skipped/flaky/retried cases; snapshot updates remain none.
All three executions preserve the approved PNG and produce the same deliberate
diff SHA-256 5940286f9ecaeb144bd86b00b638950e7e748118d8bd6400f8f4994d2820b4f5.
Actual runtime is native Linux/amd64 Ubuntu 24.04.4, Node 24.18.1, pnpm 11.21.0,
Playwright 1.62.1, Fontconfig 2.15.0 and Chromium 151.0.7922.34. The headless-shell
executable hash, launch arguments, fixed settings, package versions, 55 font
files and 63 Fontconfig files agree across all three. Chromium identifies the
heading as DejaVuSans-Bold, token text as Liberation Mono and studio textarea
as DejaVuSansMono.

The [durable runtime receipt](../evidence/identity-browser-environment-2026-10-20.json)
retains all three host/container receipts and the failed/unavailable attempts.
All 22 critical source hashes and the 339-input inventory reproduce after this
documentation-only update. The release artifact ZIP digest and all 13 delivered
file hashes verify. Three hidden .last-run.json state files are omitted by the
artifact action's default policy; the receipt states that limit. Required
[positive](../evidence/browser-environment-2026-10-20/positive-report.json),
[negative](../evidence/browser-environment-2026-10-20/negative-report.json) and
[restored](../evidence/browser-environment-2026-10-20/restored-report.json) reports,
the [deliberate actual](../evidence/browser-environment-2026-10-20/deliberate-change-actual.png)
and [diff](../evidence/browser-environment-2026-10-20/deliberate-change-diff.png),
and initial font-mismatch actual/diff images are retained with verified hashes.
They remain reviewable after temporary CI artifacts expire.

This workspace has no usable Docker runtime; its local command exits with an
explicit missing-Docker receipt while preserving the PNG. The default local
entrypoint is verified by hosted-local-entrypoint-replay, not by a Docker run
in this authoring workspace. Exact results for the containing final head belong
externally in PR #123; the containing commit cannot name its own CI runs.

## Boundaries

The selected native Linux/amd64 image is the bounded candidate. An index's arm64
entry, arbitrary host font environment or emulated platform is not automatically
qualified. Browser tests cover the existing fixture and assertions; no full
WCAG/manual visual acceptance or publication/release claim follows.

Pinned Aether decision-impact 2.1.0/continuity 1.1.0 and Hygiene 1.2.0 source were
loaded from verified exact checkouts. ROADMAP preserves 40 IDs/88 edges and all
26 ADR bytes. Q20 is complete, Q19 active; Q21/Q27 await reviewed #80 completion.

Roadmap-Step: IDN-Q19
ADR-Ref: egohygiene/identity#ADR-0011
