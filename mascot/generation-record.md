# Kern generation record

Kern is a human-selected, AI-assisted first-party character. The reviewed
direction was developed in the Identity issue #50 conversation and approved by
the project owner on 2026-08-29.

## Reviewed direction

- Regenerate the character from scratch as a compact hooded Identity guide.
- Use exactly three featureless, warm-white glowing eyes.
- Integrate the layered diamond identity kernel into the chest garment.
- Keep the open-hand pose, charcoal/obsidian robe, violet and luminous-blue
  accents, and restrained soft-gold trim.
- Remove every floating object, orbit line, particle trail, and detached
  emblem.

The approval evidence is recorded in [`approval.json`](approval.json). The raw
review candidate is content-addressed by SHA-256
`37df5721f80c0a818e4a6bac20efc3fa8eee7bde377384e42c9c15c317f6c14c`.
The raw candidate is not published because its checkerboard was baked into RGB
pixels rather than represented as transparency.

## Canonical transparency pass

The selected pixels were converted into the canonical RGBA master using
ImageMagick 6.9.12-98. This was a technical background-removal pass, not a new
creative candidate:

```bash
convert "reviewed-raw.png" \
  -alpha on \
  -bordercolor "white" \
  -border "1" \
  -fuzz "12%" \
  -fill "none" \
  -draw "matte 0,0 floodfill" \
  -shave "1x1" \
  "reviewed-rgba-1024.png"
```

The reviewed RGBA intermediate digest is
`b13bada66a7383a1840598a2b1f2da7e8430b3fce05822fc5fb6ae96bbcda65c`.
The distributable master preserves the approved 2:3 composition at a compact,
high-quality 768 × 1152 resolution:

```bash
convert "reviewed-rgba-1024.png" \
  -strip \
  -resize "768x1152" \
  -define "png:compression-level=9" \
  "mascot/source/kern-master.png"
```

The canonical master digest is
`56d68e14d92aab9f61b821ee97c1b63a1759b0d0fc2d49141aad962f9d094e3c`.
The verifier requires real RGBA transparency and refuses an opaque RGB image,
which prevents the baked-checkerboard failure from returning unnoticed.

## Reviewed projections

The Brand Kit variants are byte-bound in
[`assets/identity/mascot/manifest.json`](../assets/identity/mascot/manifest.json):

```bash
cp "mascot/source/kern-master.png" \
  "assets/identity/mascot/kern-full.png"

convert "mascot/source/kern-master.png" \
  -crop "768x768+0+60" \
  +repage \
  -resize "512x512" \
  -strip \
  "assets/identity/mascot/kern-portrait.png"

convert "mascot/source/kern-master.png" \
  -crop "615x615+76+22" \
  +repage \
  -resize "256x256" \
  -strip \
  "assets/identity/mascot/kern-icon.png"
```

ImageMagick is not a runtime dependency. Identity distributes the reviewed
bytes and validates their digests, dimensions, media type, and alpha channel
offline with the Python standard library.
