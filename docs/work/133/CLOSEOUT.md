# Explicit v1 initialization acceptance — 2026-11-14

Source base: `0ce87e35790dc224b04fae5176a676cf86b9b90f`, containing merged
PR138's initializer. This closeout adds scenario coverage and reconciles the
guide; it does not replace v0 behavior or introduce a new initializer contract.

| #133 acceptance | Actual result |
| --- | --- |
| Explicit invocation and v0 preservation | `v1-init` is documented independently. A copied binary runs the existing v0 `init`/`validate` and prepares a separate v1 candidate without changing v0 source. |
| Supplied facts/profiles/defaults/source | Seed tests retain actual supplied project fields, exact token bytes, mechanically computed digests and explicit profiles. Unsupported profiles/material reject. Validated v1 import preserves all source and approval bytes, including a declared input outside `.identity/`. |
| Reviewable candidate and missing facts | Absent/partial source produces an incomplete separate candidate, missing-fact diagnostics and empty human-evidence arrays. Only a complete validated fixture import reaches ready-for-review; that status never means approval or canonical adoption. |
| Path and failure preservation | Reserved, nonportable, overlapping, missing-parent, existing and symlink paths reject. Repeat invocation cannot overwrite. Original inputs are compared after success/failure. Injected final I/O failure retains only the explicitly selected partial destination, without a completion receipt or leaked staging tree. |
| Compatibility and setup separation | Deterministic reports bind package, script hashes, source schema and available profile versions. The copied binary works outside the checkout with embedded code and isolated Python, ignoring consumer `json.py`/`sitecustomize.py`; a missing runtime fails without writes. No installation or network acquisition is added. |
| Required scenario matrix | All fourteen Python cases pass, plus the copied-binary Rust case. Complete source is an explicit existing fixture import; absent evidence is never manufactured. |
| Manual fallback and owner handoff | The standalone script is exercised with `-I -S`. The guide retains manual authoring/adoption, separate generation/recovery and Holon/Realm/Aether/EgoLint/Relay ownership. |

`cargo fmt --all --check` and Clippy for the new integration target with
denied warnings pass. A real incomplete output report validates against the
closed report schema. Documentation links and extraction/provenance checks
pass. No production initializer source or schema needed a behavior change.

This is local Linux implementation acceptance. Full native-platform/CI checks
remain #70, and actual Identity self-source/rights/release/adoption remain #98.
No tool installs, source promotion, release or publication occurred.

ADR-Ref: egohygiene/identity#ADR-0033 (reference; proposed, approval null).
Local acceptance supplies no ADR lifecycle disposition.
