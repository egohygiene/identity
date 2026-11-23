# Local source-candidate installation qualification — 2026-11-23

This [#70](https://github.com/egohygiene/identity/issues/70) checkpoint executes
the local installation mechanism needed by #98. It is **source-candidate
qualification**, not downloaded official-release acceptance or a new supported
matrix row. Published v1.0.0 and its assets remain untouched.

## Exact inputs

| Input | Observed identity |
| --- | --- |
| New product source | `d159c680e6161e85854fd45c255d4196aec5c34f` |
| New local binary | SHA256 `37ff6ca4afee895e60d1ee98ceb76175513c9a971c8feebd67a0742669214907` |
| Previous local product source | `edca416d58d15b06ccc05029b0803bc27e65fe18` |
| Previous local binary | SHA256 `f6a840212fab05bb40dee203d2010c5be9d185aaef7bc6030b422e7b1831a1d7` |
| Executed proof source | `d0ff470147bf45d007fa83c4087d62309583ce7f` |
| Proof script | SHA256 `f58748908f6af51d700696da214bc8efbb3ba53aa0ba05fb77c07dda6758663c` |
| Unchanged real consumer | `egohygiene/mantle@b08045acc1e982dd9424c1d8c91b0badd64744e8` |
| Native cohort | Linux amd64 on this host, separately recorded Python runtime |

The new binary's existing [timestamp build/test evidence](timestamp-consistency-20261123/VALIDATION.md)
and the retained previous strict-preflight binary establish separate local
source/build observations. The proof takes explicit binary digests; it does
not independently attest compilation, signatures or release authenticity.
Both actual `--version` output digests match `identity 1.0.0\n`. Distinct byte
hashes identify the replacement; this is not a published semantic-version upgrade.

## Actual result

The [receipt](local-install-20261123/qualification.json) retains seventeen
installed CLI commands, each bound to the actual selected executable hash,
their exit codes/output digests, archive digests and nested consumer proof.

- Two deterministic single-file USTAR/gzip archives, about 15.69 MB each,
  transfer over a real loopback HTTP server with proxy handling disabled.
  Their expected archive and executable SHA256 values match before installation.
  No redirect, generic archive extraction, arbitrary archive paths, links or
  additional payload members are admitted.
- Fresh private prefixes include spaces and Unicode. PATH selects their actual
  `identity` executables. Both installations retain mode 0755; system PATH,
  user/global installations and supplied binaries remain unchanged.
- The previous binary generates/verifies the pinned Mantle source. The new
  binary generates/verifies in the same disposable consumer. Both complete
  nineteen-file output inventories happen to match. `outputBytesEqual` is an
  observed metric, not a general required upgrade-compatibility promise.
- Selecting the previous binary again and restoring its retained generated
  tree passes verification and reproduces its exact prior output inventory.
- Missing Python refuses generation and v1 initialization without mutation.
  Installed inspect and completed/empty recovery still work without Python;
  inspection changes no files or directories. This is not a new interrupted-
  process recovery proof; the existing native integration cases own that scope.
- The installed v0 initializer/validator work. Explicit v1 preparation preserves
  v0 and unrelated files, remains honestly `incomplete`, refuses an existing
  destination and never imports the disposable consumer's hostile `json.py`.
- The existing [consumer authoring harness](../../../scripts/verify_consumer_authoring.py)
  runs against the installed candidate: two fresh generations, exact manifest
  inventory checks and three read-only drift failures. All fourteen consumed
  Mantle input files match their raw pinned Git blobs; the original consumer,
  its declared source and both supplied executables remain unchanged.

The real run also requires checksum, traversal-archive, existing-prefix and
symlink-prefix negative controls to fail while preserving existing files.
Eleven focused test methods add archive corruption/invalid DEFLATE, expanded
size bounds, extra members, special files, redirect refusal, native input/hash
checks, selected-executable mutation and unrelated-source deletion controls.
The latter command controls model deliberate mutation; actual CLI behavior is
established separately by the receipt. A review found the DEFLATE decoder's
`zlib.error` outside the original compression catch; it is now a bounded public
failure with an exact regression case. The final fixed-source run passes. Full Python discovery also passes249methods
(247passed/two existing skips) with actual Make and pinned Task available;
documentation, syntax, receipt hashes, privacy and whitespace checks pass.

## Reproduce

Use explicitly reviewed local binaries and a clean checkout of the pinned
consumer. The receipt's parent directory must exist outside source, consumer
and binary inputs; the destination must be new.

```bash
python3 scripts/qualify_local_install.py \
  --candidate-binary PATH_TO_NEW_BINARY --candidate-sha256 NEW_SHA256 \
  --candidate-revision NEW_SOURCE_SHA \
  --baseline-binary PATH_TO_PRIOR_BINARY --baseline-sha256 PRIOR_SHA256 \
  --baseline-revision PRIOR_SOURCE_SHA \
  --consumer-root PATH_TO_CLEAN_MANTLE \
  --consumer-repository egohygiene/mantle \
  --consumer-revision b08045acc1e982dd9424c1d8c91b0badd64744e8 \
  --receipt PATH_OUTSIDE_INPUTS/new-local-install-receipt.json
```

The harness is a standard-library developer proof, not a generic system
installer. Inputs are trusted caller-selected native ELF binaries; filesystem
and consumer mutation occurs only inside private disposable directories. It
does not install Python, fetch dependencies, run consumer scripts, change a
real consumer pin or assume a hostile concurrent filesystem writer is safe.

## Remaining acceptance and decision impact

No minimum GNU libc/kernel, distribution coverage, macOS/Windows, official
download, SBOM/license inventory, signature/attestation, released upgrade,
publication or creative acceptance follows from this local test. These retain
their [planned release gates](../../releases/NEXT_RELEASE_MATRIX.md).
Self-source choices stay with their actual owner. The proof's tool revision,
product source revisions and later documentation/integration revisions are
distinct and are not relabeled as one executed source.

Decision impact: reference accepted ADR-0011/ADR-0019 and the existing consumer
preservation boundaries. ADR not required: this adds bounded development proof
of existing install/consumer contracts without a new public runtime, release
policy or approval authority.

## Test portability followup

At test-only source `ec3350969b47e21f55b8d76edcad11aee89023c6`, generic archive, checksum, ELF, clobber and receipt checks remain portable. POSIX permission/shebang controls have explicit platform requirements; three separate symlink negatives skip only when the filesystem or permissions actually deny link creation. Unexpected link errors still fail. This does not qualify the Linux-only developer harness on another platform.

Actual local Linux verification: **253 Python checks, 251 passed and two existing skips**, with Make and Task 3.45.3, in 20.852 seconds. All 15 focused checks pass. A separate simulated symlink-permission denial yields 12 passes and three precise skips. Full-suite raw log SHA256: `c395a97690e3493db95d3a35a3c472e4280bb692bf6eab76d7460a56e92f2b02`; retained task-locally. The earlier executed candidate transport and binary provenance remain unchanged.
