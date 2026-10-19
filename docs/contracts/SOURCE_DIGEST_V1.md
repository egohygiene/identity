# Canonical source digest v1

`egohygiene.identity.source-digest/v1` names the SHA-256 inventory contract shared by the
Rust v1 consumer and Python projections. It preserves the existing Rust/Unix
digest for supported trees, including the established fixture hash
`1002ff75ea51f6e016929894ea30cc96565bdbbca749a0e7fff1ebd0d2f21353`.
The proposed compatibility decision is [ADR-0023](../decisions/ADR-0023-canonical-source-digest.md).

## Inventory

Start at the selected repository's `.identity/` directory. It must be a real
directory. Recursively include every regular file, including hidden files and
files not referenced by the project manifest, subject to these exact,
case-sensitive lexical exclusions:

| Entry | Exclusion |
| --- | --- |
| `.identity/identity.toml` | The root legacy v0 entry, including any subtree |
| `.identity/candidates` | The root candidate entry and entire subtree |
| `.identity/references` | The root reference entry and entire subtree |
| Any entry named `README.md` | That entry and any subtree, at every depth |

Apply exclusions before inspecting or descending into an entry. An excluded
symlink is never followed. Nested lookalikes such as
`.identity/notes/identity.toml` and `.identity/notes/references/ref.txt` are
included. `Readme.md` is included. Empty directories contribute no bytes.
Generated assets and other files outside `.identity/` are outside this inventory.

An exclusion from this digest does not exempt an explicitly declared input
from normal source validation. In particular, a declared candidate/reference
directory must still satisfy the project contract.

## Paths and filesystem entries

Inventory paths are repository-relative UTF-8 strings, beginning with
`.identity/`, separated with `/` on every operating system. Their spelling and
case are preserved. Do not case-fold, Unicode-normalize, lossily decode, or
substitute native Windows separators.

Use the compiler's portable path rules: no absolute roots, empty/dot/parent
segments, trailing separators, backslashes, control characters (U+0000–001F
or U+007F–009F), `:*?"<>|`, or segments ending with a dot or space. A segment's
stem before its first dot must not be an ASCII-case-insensitive Windows device
name: `CON`, `PRN`, `AUX`, `NUL`, or `COM`/`LPT` followed by 1–9 or ¹/²/³.
Non-UTF-8 names are invalid.

Reject included symbolic links, including broken links, directory links and
cycles. Reject Windows reparse points, including junctions. Reject other
non-regular entries such as FIFOs, sockets and devices before reading their
contents. Never silently skip them or traverse their targets. The standalone
validator reports inventory failures as `IDN1003`; the Rust pipeline runs that
same embedded preflight before loading source. The digest implementations also
check independently when collecting their inventories.

Cross-platform source trees must preserve exact names and file bytes. A tree
requiring distinct case-only or Unicode-normalization variants cannot be
reproduced on a filesystem that aliases those names. A filesystem that rewrites
names or checkout configuration that changes line endings is not a compatible
reproduction of that source. No automatic rename or newline conversion is part
of hashing. The repository's `.gitattributes` preserves its tracked fixture bytes.

## Ordering and byte framing

1. Split each repository-relative path into components at `/`.
2. Compare the component sequences lexicographically; compare each component
   by its unsigned UTF-8 bytes. If one sequence is a prefix, it sorts first.
   This is component ordering, not whole-path string ordering or native
   case-insensitive path ordering. For example, `a/child.json` precedes
   `a-b.json`, which precedes `a.json`.
3. In that order, append each complete UTF-8 repository-relative path, one
   zero byte, the file's exact raw bytes, and one zero byte.
4. SHA-256 the concatenation and return 64 lowercase hexadecimal characters.

There is no BOM, contract prefix, JSON transformation, newline conversion,
file length, timestamp, permission, owner, directory record or trailing extra
record. An empty inventory hashes the empty byte string; it does not constitute
a valid v1 project. Binary content, including embedded zero bytes, is hashed
unchanged. This historical delimiter framing is not self-describing; digest
equality alone does not attest an inventory or its approvals. Release evidence
must retain the exact source revision and artifact checksums as well.

The v1 inventory is also distinct from the complete validation read-set.
Declared inputs outside `.identity/` are checked and freshness-bound by
preflight, but their raw bytes are not added to this historical digest. Extending
the inventory or replacing its framing requires a separately versioned contract.

## Compatibility and release migration

This correction is **unreleased**. Existing tags, published artifacts, fixture
goldens and release/publication bindings are retained byte-for-byte. The new
contract identifier names these clarified rules; it is not prepended to the
hash or added to existing closed v1 model schemas.

| Historical producer/input | Effect in the corrected implementation |
| --- | --- |
| Rust on Unix, supported inventory | Same digest, including root legacy TOML coexistence |
| Python on Unix, ordinary supported inventory without root legacy TOML | Same digest |
| Python with root legacy TOML or an excluded entry used as a directory | Corrected exclusions can change the digest to the compiler value |
| Rust on Windows | Replacing native `\` separators with `/` changes historical hashes |
| Python on Windows with case-sensitive ordering differences | Exact component ordering can change historical hashes |
| Included links, reparse points, special files, non-UTF-8 or nonportable names | Fail validation; no silent omission or lossy-path compatibility mode |

For the next reviewed release and consumer upgrade:

1. Pin the corrected tool's exact immutable release/source. Version selection
   is required because existing models carry only a bare digest, not its
   algorithm identifier. A bare old hash does not establish its producer dialect.
2. Validate the consumer source and compute the shared v1 digest. If a former
   digest differs, retain that historical producer/output binding as evidence;
   do not overwrite it or recognize the old hash as an alias for the new one.
3. Regenerate the compiler package and every selected Python projection together
   from the same source and corrected tool selection. Review the resulting
   source digests, manifests, artifact checksums and compatibility metadata as
   one new release candidate. Never edit generated digest fields to force a match.
4. Publish a higher immutable release when approved, and upgrade the consumer's
   entire bound artifact set together. Roll back to the previous whole set and
   its original tool pin when needed. Never retag or replace a published asset.

[#75](https://github.com/egohygiene/identity/issues/75) owns enforcing optional
guidance/release agreement and reporting stale or mixed sets. This change does
not alter existing publication configs, version numbers, tags or deployments.
A future length-framed digest, expanded read-set or normalization rule needs a
new major digest contract and an explicit model/binding migration; never change
this algorithm under the existing identifier.

## Conformance evidence

[`source-digest-v1.json`](../../tests/fixtures/source-digest-v1.json) contains
shared, fixed inventories, exact file bytes encoded as hexadecimal, expected
ordering/hashes, link cases and portable path cases. Both language suites consume
these vectors rather than generating expected hashes from either implementation.
They include normal and reversed creation order, legacy coexistence, exclusions,
nested lookalikes, component/case ordering, Unicode paths, binary/NUL/CRLF bytes,
missing roots, links and cycles. Unix tests cover non-UTF-8 conversion and
special files; Python also exercises non-UTF-8 inventory entries on filesystems
that permit their creation. macOS rejects creating those names with `EILSEQ`.
The full consumer regression compares actual Rust and
Python projection digests and preserves the existing fixture hash and goldens.

```bash
cargo test --locked --lib source_digest
cargo test --locked --test v1_consumer
python3 -m unittest discover --start-directory tests --pattern "test_source_digest.py" --verbose
```

The existing [release gate](../../.github/workflows/release.yml) runs the Rust
and Python suites on Linux, macOS and Windows for source/test changes. On Windows,
use `python` as in that workflow. Link creation requires runner privilege: the
Rust vectors require it, and a missing Python capability is explicitly reported
as skipped. A skipped capability is not conformance evidence. Hosted matrix
results establish platform coverage separately from any local Linux result.
