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
  **13 tests pass**. Four smoke controls cover success, lockfile/source mutation,
  setup failure and runtime pin drift. Two additional host-reader controls reject
  missing/forged inventories, wrong pins and absent/duplicate/failed command
  records; seven original storage/configuration/receipt boundaries remain.
- Python compilation and `git diff --check` pass.

These controls use disposable fixtures and command doubles. They do not claim
that real setup or the full default/custom image qualifier has executed.

## Actual execution status

The managed Docker engine uses VFS and the workspace had approximately 6.7 GiB
free when this checkpoint began. The original guard remains 24 GiB for that
copying driver and 8 GiB for others, subject to an explicitly measured runner
budget. No known-failing VFS image pull/build is repeated merely to obtain a
fresh failure receipt. Parent runtime work is investigating a separate bounded
engine/backend while preserving the managed daemon and shared caches.

The original pinned default and non-root custom image qualification remains
**not run in this checkpoint yet**. Its actual dependency acquisition, inherited
user/command metadata, complete cache/TLS/native/renderer proof and repeated real
setup must pass before #82 can close. #80 remains the separate browser/workflow
gate. No hosted CI, image publication, tag, release or deployment is performed.

Decision impact: **ADR not required** for completing the existing image/setup
coverage and refusing incomplete evidence. Existing ADR-0011 supplies the layered
evidence boundary; no new ownership, source semantics or human disposition is
selected. Pinned Aether decision authoring 2.1.0 and continuity 1.1.0 were loaded
with `git show` at `dc8a16851f452763ef4f7fbe4bf057d4500b1921`; Hygiene policy
1.2.0 retains its selected immutable reference.
