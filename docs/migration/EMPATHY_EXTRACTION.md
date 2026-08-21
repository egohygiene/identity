# Empathy Identity CLI extraction

## Source baseline

The independently buildable Identity CLI was extracted from
`egohygiene/empathy` at immutable revision
`cbd6e0dfb08befa1d8bf795f5328bac9fddb27fc`. Its reusable source was isolated
beneath `identity/`; Empathy's consumer-owned intent remains beneath
`.identity/` and is not promoted into this repository as canonical brand truth.

The machine-readable [extraction manifest](../../migration/empathy-extraction-v1.json)
records the source-to-destination disposition and SHA-256 digest for each
reusable implementation file.

## Preserved behavior

| Surface | Incubated evidence | Extracted evidence |
| --- | --- | --- |
| CLI | `init`, `validate`, `plan`, `handoff` | Four command-level parity tests |
| Contracts | Four closed JSON Schemas using `identity.*/*v0` | Byte-identical files under `contracts/` |
| Profiles | `core`, `docs`, `github`, `metadata`, `pwa`, `social`, `tokens`, `web` | Byte-identical files under `profiles/` |
| Target catalog | 45 unique repository-relative targets | Validation and deterministic-plan parity tests |
| Human authority | Candidate manifest starts unapproved | Candidate and handoff contracts preserved |
| Provenance | Handoff hashes inputs and profile models | Deterministic handoff parity test |

The package manifest changes only its repository ownership and description.
The mature root architecture documents supersede the incubation-local README
and architecture notes; their history and digests remain recorded in the
extraction manifest.

## Consumer transition

Empathy remains the golden consumer, not the implementation owner. After this
change is accepted and an immutable Identity commit or release is available:

1. pin that revision in Empathy's dependency/desired-state record;
2. run the extracted CLI against Empathy's unchanged `.identity/` input;
3. compare the profile inventory, JSON plan, and handoff manifest with the
   pre-extraction evidence;
4. update Empathy's local task and CI adapters to invoke the pinned CLI;
5. remove the transitional `identity/` source copy only after parity passes.

The consumer transition is a separate Empathy-owned review. It must not copy
the extracted implementation back into Empathy.

## Rollback

Before the Empathy transition merges, rollback is simply removal of the
consumer-integration change; the incubated source remains available at the
pinned source revision above. After transition, rollback restores Empathy's
previous Identity pin and its corresponding generated outputs. Canonical
`.identity/` intent is never deleted or rewritten by rollback.

If extracted behavior diverges, stop the consumer migration, reproduce the
failing command against the pinned Empathy revision, and fix the canonical
implementation here. Do not patch a second implementation in the consumer.
