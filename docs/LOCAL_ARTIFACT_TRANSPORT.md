# Strict local artifact transport

The original pinned `actions/upload-artifact` sends a typed `mime_type` field
that upstream act 0.2.98 does not yet describe. Its strict parser rejects the
request. After adding the exact sender field, the real Azure SDK exposes a
second incompatibility: an unescaped padded signature loses its final `=` in
the sender's query parser. These are local transport failures, separate from
the product, browser, security and hosted-runner results.

The optional [reviewed lock](../dev/local-actions/act-artifact-compat/lock.json)
and [public patch](../dev/local-actions/act-artifact-compat/zip-mime.patch) name
`identity-act-zipmime 0.2.98+identity.zipmime.2` explicitly as a local derivative.
They do not replace the official/global act executable. The bounded patch adds
only `google.protobuf.StringValue mime_type = 6`, permits `application/zip` or
legacy empty values, and URL-escapes the emitted signature. Unknown fields,
malformed values, unsupported MIME types, invalid tokens and altered signed
targets continue to fail. The verifier, HMAC and target bindings are unchanged.

## Reproduce the reviewed build

On Linux amd64, select a new private directory outside the checkout:

```bash
python3 scripts/prepare_local_act.py \
  --download --build \
  --output-directory /tmp/identity-act-review
```

Alternatively, use `--archive-directory /prepared/archives` instead of
`--download`, with the exact names in the lock. Without `--build`, the helper
only prepares verified sources. Building explicitly permits normal verified Go
module acquisition through the public module proxy and checksum database.
Go, protoc, the generator module, sender archive, upstream source archive/Git
tree and patch are pinned and checked. Compiler/module caches and binaries stay
inside the selected output; no global installation, HOME change or persistent
PATH modification occurs. Builds use two Go workers and preserve private logs.

Upstream tracks generated Go without the original `.proto`. The patch restores
that source from its descriptor. The builder first regenerates a legacy
descriptor and requires byte equality with upstream, then removes only the new
typed field from the patched descriptor and again requires byte equality. It
also requires the generated Go bytes and every patched file to match the lock.
The generated header's `protoc v7.36.2` is the pinned 36.2 compiler's own output.

The successful reviewed build produced SHA-256
`e103cd431339dd0be997d5b0a9599a7327da8d1d327ed3fe809636b8fdd2ce90`.
This is an observed binary identity, not a publisher signature or promise of
cross-host byte equality. The receipt records the actual build identities.
Twenty-eight top-level Go artifact tests pass, including 15 MIME subcases and
six signed-target negatives. One pre-existing Docker integration test is
explicitly skipped by `-short`; it is not included as a pass.

## Fast actual sender preflight

Prepare the unchanged full-commit action mirrors as described in
[local workflow replay](LOCAL_WORKFLOW_REPLAY.md), then run:

```bash
python3 scripts/qualify_local_artifacts.py \
  --act-executable /tmp/identity-act-review/bin/identity-act-zipmime \
  --act-sha256 e103cd431339dd0be997d5b0a9599a7327da8d1d327ed3fe809636b8fdd2ce90 \
  --expected-version 'act version 0.2.98+identity.zipmime.2' \
  --uploader-source /prepared/actions/upload-artifact-exact-source \
  --output-directory /tmp/identity-artifact-preflight
```

This disposable two-file ZIP fixture uses the actual pinned uploader, real
loopback artifact API and authenticated signed download. The independent
worker requires the uploader digest, downloaded archive SHA-256 and complete
expected file inventory to agree. It refuses different origins/redirects,
missing or changed files, duplicate/unsafe/link entries and excessive sizes.
Ambient act configuration is refused. Private tokens, signed URLs and raw
logs are not included in public receipts. The earlier v1 derivative's actual
401/padding failure remains historical evidence; it is not relabeled a pass.

## Original workflow replay and evidence

`replay_local_artifact_workflow.py` requires a clean standalone checkout at an
explicit full commit, exact binary hash/version, four independently rehashed
action trees, private caller environment, owned source/evidence/cache roots
and the real measured Docker endpoint. Use its `--help` for the caller inputs.
It executes the original reference workflow and all its original steps.
It neither changes action pins nor disables security or browser checks.

The caller sets act's supported `ACTIONS_RUNTIME_URL` to a bounded loopback
forwarder. The forwarder preserves actual authorization, request and backend
response bytes. During successful finalization, while the actual owned pinned
Node uploader and workspace still exist, it hashes exactly the original
literal input directories using hidden-file and common-root rules. It then
downloads the actual backend ZIP and checks its complete inventory and hash
against the real finalization digest. Tokens and signed URLs remain in memory.
The controller additionally matches the digest printed by the actual uploader.
An observer failure fails the proof while preserving the backend's response.

Full-workflow acceptance requires whole-job exit zero, preserved source/action
trees and the complete actual archive proof. A fast fixture pass alone supplies
none of the full browser, hosted CI, release or publishing acceptance. Original
profile/font/image/PNG bindings and ADR-0011 evidence requirements remain in
force. Local security-action results retain their self-hosted limitations.

Decision impact: reference ADR-0011. This is an optional, explicitly identified
local evidence transport adapter for the existing contract; no new creative,
architecture lifecycle or release decision is accepted by this checkpoint.
