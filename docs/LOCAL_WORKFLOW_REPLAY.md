# Exact action sources for local workflow replay

The local `act` Git transport can fail acquiring a public full-commit action
even while that exact GitHub object is readable through HTTPS. This is separate
from action execution, Docker capacity and browser qualification. Do not replace
an action pin, copy a moving branch or call the missing step passed.

[`prepare_local_actions.py`](../scripts/prepare_local_actions.py) prepares
explicit local source substitutions for the existing reference-renderer
workflow. It does not run actions, edit the workflow, select an engine, provide
credentials or qualify hosted security behavior.

## Locked acquisition

The [local mirror lock](../dev/local-actions/reference-renderer.lock.json)
binds the complete workflow SHA-256 and every literal remote action selection:
repository, full commit, public codeload URL, archive size/SHA-256 and Git tree
SHA-1. The four tree identities were inspected through the exact GitHub Git
commit API endpoints. During preparation, each file's bytes/executable mode is
hashed into its Git blob and complete Git tree, independently of the archive
checksum. Both identities must match the reviewed lock.

The lock is reviewed source, not independently authenticated publisher evidence.
The preparer checks its declared identities; it does not verify a signature,
fetch a fresh commit object or approve the upstream action. A workflow change
requires an explicit corresponding lock review rather than an implicit refresh.

For an explicit online acquisition into a new directory outside the checkout:

```bash
python3 scripts/prepare_local_actions.py \
  --download \
  --output-directory /tmp/identity-actions-review
```

For offline preparation from already acquired archives, name files as
`owner--repository--<full-commit>.tar.gz`:

```bash
python3 scripts/prepare_local_actions.py \
  --archive-directory /prepared/action-archives \
  --output-directory /tmp/identity-actions-offline
```

The output must be new. The helper never overwrites an earlier preparation or
writes into the consumer checkout. Archives have compressed/decompressed,
member-count and extracted-byte limits. Traversal, links, special files,
duplicates, mode/content mismatches and unexpected source selections fail.
This bounded profile supports literal root GitHub actions; it rejects mutable,
expression, Docker and nested remote-action selectors rather than approximating
a general workflow parser.

## Feed exact mirrors to act

`action-mirrors.json` contains paths relative to the preparation directory,
without private local paths. Resolve these paths only for the actual local
invocation. Pass one argument pair for every recorded repository/commit:

```python
import json
from pathlib import Path

prepared = Path("/tmp/identity-actions-review")
receipt = json.loads((prepared / "action-mirrors.json").read_text())
mirror_arguments = []
for action in receipt["mirrors"]:
    selection = action["repository"] + "@" + action["revision"]
    mirror_arguments += [
        "--local-repository",
        selection + "=" + str(prepared / action["directory"]),
    ]
```

Use these arguments with the original selected workflow and explicitly reviewed
runner image, resource, network, socket and TLS options. Use a disposable
standalone Git checkout when the selected act version cannot read a Git
worktree's `worktreeconfig`; preserve the full source commit and actual copied
bytes. Do not copy Git credentials or unrelated host configuration.

An actual `act --strict --dryrun` with these mirrors proves only local source
resolution and workflow planning. It does not execute the action steps. In an
actual run, upstream hardening may report self-hosted or unsupported behavior;
retain that exact result rather than label it GitHub-hosted protection. Do not
disable or rewrite a security step merely to produce a green result.

## Docker and evidence remain separate

The original browser command still requires its pinned image, registry/font
bindings, actual capacity observations, all nine positive tests, deliberate
screenshot failure and restored pass. The approved PNG/tolerance are unchanged.
Read [browser qualification](BROWSER_ENVIRONMENT.md) for that contract.

When act runs a Docker-using workflow, the actual daemon must see the evidence
bind paths and the client must observe its real storage filesystem. A forwarded
Unix socket alone does not establish either fact. Use task-owned explicit
mounts and record the daemon/storage/native-or-emulated context; do not present
an unrelated client path's free space as daemon capacity.

Retain source/lock/tool hashes, local substitutions, actual command/exit and
sanitized logs. The preparation receipt intentionally claims neither browser,
workflow, hosted CI, release nor publication acceptance. #80 and dependent #88
close only after their actual remaining evidence is established.
