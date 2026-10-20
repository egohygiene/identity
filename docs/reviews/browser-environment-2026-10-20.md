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

Runtime qualification is pending. Registry identity alone does not prove a
screenshot pass. This workspace has no usable Docker/namespace/chroot runtime;
local host checks cannot be reported as a pinned-image run. The shared local
entrypoint will also be replayed on a hosted Docker engine and labelled as
such. Exact outcomes, font/runtime evidence and deliberate-drift artifacts
will be recorded before handoff.

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
