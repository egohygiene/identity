# Full development-image qualification checkpoint — 2026-11-22

Base source: `75ca39f3fc7e5e9e0b5578af58c966cd2590a652`.
Owner: [Identity #82](https://github.com/egohygiene/identity/issues/82),
roadmap `IDN-Q21`. The earlier portable-entrypoint and resource-guard results
remain in [LOCAL_ACCEPTANCE.md](LOCAL_ACCEPTANCE.md); they do not supply full
default/non-root image acceptance.

## Demonstrated coverage gap and bounded repair

The add-on Dockerfile ran real `setup` once during construction. Its smoke then
checked tools, cache ownership, TLS, generation and rendering, but never ran a
second real setup inside either built image. The existing five frontend
protocol tests exercise repetition against synthetic external tools; their
success does not establish repeated real dependency/tool acquisition in an image.

The smoke now invokes the same `bash scripts/dev-env.sh setup` again after the
initial built-image runtime/cache checks. A shared pure input selector binds
the Rust source, minimal canonical v1 fixture and five toolchain/dependency
manifest/lock inputs. The second setup must preserve every selected byte and
the Rust/pnpm pins before ordinary CA/native/renderer smoke continues.

Host admission independently compares the emitted inventory against the exact
selected host source and requires the expected runtime pins, a true preservation
flag and one successful actual repeat-command record. Missing, stale, empty or
changed subreceipts fail. Historical receipts remain dated evidence; they are
not rewritten to satisfy the current smoke contract.

No dependency, base-image, Rust/pnpm pin, profile, screenshot, source fixture or
public identity contract is changed. This is qualification behavior, not a new
product runtime feature or a claim of all-frontend image coverage.

## Checks executed during preparation

- `python3 -m unittest discover --start-directory tests --pattern 'test_*dev_image*.py' --verbose`:
  **16 tests pass**. Four smoke controls cover success, lockfile/source mutation,
  setup failure and runtime pin drift. Two additional host-reader controls reject
  missing/forged inventories, wrong pins and absent/duplicate/failed command
  records; three scoped proxy/trust controls enforce CLI precedence, invalid-file/symlink-loop refusal without private path disclosure, names-only transport and read-only trust selection; seven original storage/configuration/receipt boundaries remain.
- Python compilation and `git diff --check` pass.

The focused controls use disposable fixtures and command doubles; the separate
actual image run below supplies real setup/image evidence.

## Demonstrated network gap and bounded repair

The first original full run used a separate native Linux amd64 overlay2 engine
with **9,031,909,376 bytes** free, exceeding the unchanged 8 GiB reserve. From
clean preparation commit `82249b2ab12cc9caab32f1c1e0236e73107f5951`, the exact
pinned Node index pull, platform and image-config binding passed. The first
setup build then failed: curl could not connect to sh.rustup.rs (exit 7). The
qualifier had not forwarded the host's required proxy argument names.

Two actual probes in that exact pinned base separated connectivity from trust:
with populated proxy names forwarded, curl rejected the untrusted TLS issuer
(exit 60); with the same names and an explicitly selected read-only public CA
bundle, the same endpoint succeeded (exit 0). Neither probe installed trust.

The qualifier now forwards the populated predefined proxy names for builds and
container smoke without logging their values. Optional `--proxy-ca`, with scoped
`IDENTITY_DEVELOPMENT_PROXY_CA` default and CLI precedence, selects a BuildKit
public-readable ephemeral secret for setup under either inherited user and a read-only container bind for real repeated setup. The
source path is redacted from public command records. No image-global trust or
base/tool pin changes are made, and synthetic unknown-CA rejection remains
required. Fresh repaired-source full qualification passed as recorded below.

## Actual full image acceptance — passed

Fresh full qualification ran from clean reviewed source
`8255c5b9ab0e669c2cde6002353515b5a8fc0511`, starting at
`2026-11-22T19:02:36.009863+00:00`. The separate native Linux amd64 overlay2
engine had **8,957,652,992 bytes** free at admission, above the original
**8,589,934,592-byte (8 GiB)** reserve. No reserve override was supplied. The
managed VFS daemon and its shared images/caches were unchanged.

The exact original Node index/config digest was pulled again after task-owned
nested-image/cache cleanup. Both the default root image and the derived
`1000:1000` image built and passed their actual complete smoke:

- 32 recorded smoke commands in each image, including real second `setup`.
- Exact Rust **1.97.1**, pnpm **11.21.0**, Node **24.22.0**, Python **3.11.2**;
  the inherited Corepack was **0.36.0** and reused rather than replaced.
- All **58 selected Rust/canonical-source/manifest/lock inputs** remained exact
  across repeated setup. All **17 canonical fixture files** and unrelated source
  remained unchanged during native generation/verification.
- Inherited user/entrypoint/command metadata and actual writable tool/cache,
  renderer, dependency and target paths passed under each selected user.
- Curl and Node rejected the synthetic unknown CA, then accepted explicit trust;
  strict Node TLS remained enabled. The disposable TLS server stopped.
- Native generation/verification repeated successfully, all **14 complete
  generated output files** matched between repetitions and between both images,
  and renderer checks, tests, build and public validation passed.

Additional actual, network-disabled probes of both built images found no
persisted proxy values in image configuration/history, no transport proxy/CA
variables in image configuration and no ephemeral CA files without the runtime
bind. Their system CA bundle bytes remained equal to the exact pinned base.
Those probes are bounded checks, not a universal secret scan or security audit.

The [evidence directory](full-image-2026-11-22/SHA256-MANIFEST.json) retains exact
structured JSON from the original failure, the distinguishing network probes,
the successful repaired run and image trust-persistence controls. Command/output
hashes remain intact; raw task-local build/network logs are hashed in the index
and excluded from the repository. No private proxy values, CA bytes or selected
host bundle path are retained. Historical receipts were not rewritten.

This clears the current-source **full default/non-root development-image gate**.
It does not turn that local native proof into hosted runner hardening, a full
all-entrypoint CI matrix, arbitrary-base/platform support, browser acceptance or
a release. The earlier five frontend protocols and narrow actual `act` job keep
their original scope; #80 and final #70/#116 reconciliation retain their owners.
No hosted CI, image publication, tag, release or deployment occurred.

Decision impact: **ADR not required** for completing the existing image/setup
coverage and refusing incomplete evidence. Existing ADR-0011 supplies the layered
evidence boundary; no new ownership, source semantics or human disposition is
selected. Pinned Aether decision authoring 2.1.0 and continuity 1.1.0 were loaded
with `git show` at `dc8a16851f452763ef4f7fbe4bf057d4500b1921`; Hygiene policy
1.2.0 retains its selected immutable reference.
