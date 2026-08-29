# Kern, the Identity guide

Kern is Identity's approved mascot: a calm, hooded guide with three glowing
eyes and a layered diamond identity kernel integrated into his outfit. The
three eyes stand for observing context, reflecting intent, and verifying a
consistent projection. His open hands express guidance without replacing human
creative authority.

## Authority and files

- [`kern.character.json`](kern.character.json) is the canonical character,
  semantics, accessibility, motion, and usage source.
- [`source/kern-master.png`](source/kern-master.png) is the approved transparent
  RGBA master.
- [`approval.json`](approval.json) and [`provenance.json`](provenance.json) bind
  the asset to its human review, origin, digest, and license.
- [`generation-record.md`](generation-record.md) records the reviewed prompt
  direction and deterministic derivative operations.
- [`../assets/identity/mascot/manifest.json`](../assets/identity/mascot/manifest.json)
  binds the distributable full, portrait, and icon bytes.

Run the offline verifier before publishing or packaging the character:

```bash
python3 scripts/verify_mascot.py --repository-root "."
```

## Non-negotiable visual constraints

Kern has exactly three featureless warm-white glowing eyes. The identity kernel
is attached to the chest garment. Do not add floating props, rings, particles,
detached emblems, pupils, irises, a mouth, a nose, or extra eyes. Use the
approved crops rather than creating ad hoc small-format variants.

Kern is supportive imagery. He never replaces a visible heading, text label,
status, instruction, or accessible name.
