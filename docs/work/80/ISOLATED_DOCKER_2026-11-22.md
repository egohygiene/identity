# Isolated Docker qualification runtime — 2026-11-22

This execution note records an actual Docker 28.4.0 `overlay2` backend prepared
for [Identity #80](https://github.com/egohygiene/identity/issues/80) and
[#82](https://github.com/egohygiene/identity/issues/82), from Identity base
`75ca39f3fc7e5e9e0b5578af58c966cd2590a652`. It is a task-local environment
procedure, not a new supported product installation or completed qualification.
The original qualifiers retain their profiles, immutable images and storage
guards. Their source-bound receipts determine acceptance.

ADR-Ref: egohygiene/identity#ADR-0011 (reference). This applies the existing
[layered evidence decision](../../decisions/ADR-0011-accessibility-and-visual-evidence.md);
runtime capability probes do not replace pinned browser, workflow, native or
human evidence. The pinned Aether decision-authoring skill v2.1.0 was read from
Git object `dc8a16851f452763ef4f7fbe4bf057d4500b1921`, at
`library/organization/skills/architecture/create-decisions-document/SKILL.md`.
No contract, approval, default daemon configuration or ADR disposition changed.

## Why another daemon was needed

The shared engine uses `vfs` on a nearly full 32 GB overlay filesystem. Previous
attempts at the official Playwright image incurred VFS layer copies before the
browser build. Repeating that attempt would exhaust the workspace and would
not satisfy the original conservative VFS capacity gate.

An existing separate `/tmp` tmpfs has 9,441,329,152 bytes total capacity. A
capability probe proved that the kernel supports native OverlayFS there, then
a disposable helper hosted a real, isolated `overlay2` engine. The data root,
source and evidence share that **one** filesystem. Its initial actual free
space was 9,410,756,608 bytes; these are not independent capacity reserves.
The client and daemon independently observed the same data-root device and
inode. The [observation receipt](evidence-2026-11-22/isolated-docker-runtime.json)
records a later live observation and the narrower cgroup budget.

Heavy profiles run sequentially. Browser goes first; remove only task-owned
images/cache after preserving its receipts, then verify the development
qualifier's unchanged 8 GiB non-VFS guard. Before every attempt, measure actual
free bytes and parent/helper memory use. Tmpfs consumes memory; `docker info`
physical memory is not proof that those bytes are available under a cgroup.

## Scope of the helper

The existing cached helper image is pinned to
`ghcr.io/catthehacker/ubuntu@sha256:19619a010b204f44c5340bff7d39b68551109fe6a56a53f75201ea91e05d4270`.
The task helper has two CPUs, a 12 GiB memory limit and private PID, network,
mount and cgroup namespaces. It adds `SYS_ADMIN`, `NET_ADMIN` and `SYS_PTRACE`,
and disables the helper's seccomp/AppArmor filters. Those substantial powers
are confined to an explicitly trusted disposable helper; this is not a
recommendation for running untrusted workloads or a security-hardening claim.
It is not launched with `--privileged`, host PID/network namespaces, host raw
devices or a host Docker socket.

Only these mounts are needed:

- The exact task runtime directory, read/write at the same absolute path.
- The exact task evidence directory, read/write; selected public source
  worktrees and their public Git common directory, read-only when used.
- The six trusted runtime executables (`dockerd`, `containerd`,
  `containerd-shim-runc-v2`, `runc`, `docker-init`, `docker-proxy`), read-only.
- The public system CA bundle, read-only. No private keys, home directory,
  Docker credentials or unrelated workspace trees are imported.
- For the local workflow replay only, its two exact temporary output paths
  mapped to task-owned directories on the measured tmpfs.

The shared daemon configuration and cached image remain unchanged. The helper
container itself is created/removed through that daemon. Nested images, build
cache, socket and data-root state belong to this task's isolated engine.

## Runnable daemon procedure

Choose a fresh task directory on an actual adequate filesystem; this procedure
does not create fictitious disk capacity. In the observed environment, `/tmp`
already supplies the separate tmpfs. Preserve source/evidence outside the
ephemeral directory before cleanup.

```bash
runtime_root="$(mktemp -d /tmp/identity-runtime.XXXXXXXX)"
chmod 700 "$runtime_root"
mkdir -p "$runtime_root/data" "$runtime_root/exec" "$runtime_root/work"
```

Place the following trusted `start.sh` inside that directory. Docker's client
proxy configuration may inject namespace-correct lowercase proxy variables;
Go prioritizes uppercase variables. Normalize only the already-present proxy
environment inside this helper and never print values.

```bash
#!/bin/bash
set -euo pipefail
runtime_root="$1"
if test -n "${http_proxy:-}"; then export HTTP_PROXY="$http_proxy"; fi
if test -n "${https_proxy:-}"; then export HTTPS_PROXY="$https_proxy"; fi
if test -n "${no_proxy:-}"; then export NO_PROXY="$no_proxy"; fi

# This is the helper's private network namespace, not host sysctl state.
mount --bind /proc/sys/net /proc/sys/net
mount -o remount,rw,bind /proc/sys/net

# A regular file is needed by runc's protected self-reexec on this kernel.
mkdir -p /opt/identity-runtime-bin
cp /usr/local/bin/runc /opt/identity-runtime-bin/runc
chmod 755 /opt/identity-runtime-bin/runc
export PATH="/opt/identity-runtime-bin:$PATH"

# This is the helper's private cgroup namespace and delegated subtree.
mount -o remount,rw /sys/fs/cgroup
mkdir -p /sys/fs/cgroup/identity-init
while read -r pid; do
  printf '%s\n' "$pid" > /sys/fs/cgroup/identity-init/cgroup.procs || true
done < /sys/fs/cgroup/cgroup.procs
controls="$(sed 's/ / +/g; s/^/+/' /sys/fs/cgroup/cgroup.controllers)"
if test -n "$controls"; then
  printf '%s\n' "$controls" > /sys/fs/cgroup/cgroup.subtree_control
fi

exec /usr/local/bin/dockerd \
  --host="unix://$runtime_root/docker.sock" \
  --data-root="$runtime_root/data" --exec-root="$runtime_root/exec" \
  --pidfile="$runtime_root/dockerd.pid" --storage-driver=overlay2 \
  --exec-opt=native.cgroupdriver=cgroupfs \
  --iptables=true --ip6tables=false --bip=172.28.0.1/24
```

Create the helper through the existing daemon. The fixed subnet is suitable
only if it does not conflict with the helper's own observed routes. Add source
and output mounts individually; never add a broad host-root or Docker-socket
mount. These commands assume the six runtime executables exist at the shown
paths; record their versions and hashes before using them.

```bash
helper_name="identity-runtime-task"
args=(run --detach --name "$helper_name" --user 0:0 --cpus 2 --memory 12g
  --cgroupns private --cap-add SYS_ADMIN --cap-add NET_ADMIN
  --cap-add SYS_PTRACE --security-opt seccomp=unconfined
  --security-opt apparmor=unconfined
  --env HTTP_PROXY --env HTTPS_PROXY --env NO_PROXY
  --mount "type=bind,src=$runtime_root,dst=$runtime_root"
  --mount type=bind,src=/etc/ssl/certs/ca-certificates.crt,dst=/etc/ssl/certs/ca-certificates.crt,readonly)
for tool in dockerd containerd containerd-shim-runc-v2 runc docker-init docker-proxy; do
  args+=(--mount "type=bind,src=/usr/local/bin/$tool,dst=/usr/local/bin/$tool,readonly")
done
args+=(--entrypoint /bin/bash
  ghcr.io/catthehacker/ubuntu@sha256:19619a010b204f44c5340bff7d39b68551109fe6a56a53f75201ea91e05d4270
  "$runtime_root/start.sh" "$runtime_root")
docker "${args[@]}"
```

Wait for that daemon to be healthy; do not start a second heavy operation
while another qualifier owns the budget. Grant only the calling user's group
access to its socket (for this session the group was 1000), or execute the
client inside the helper. Never make the socket world-writable.

```bash
docker exec "$helper_name" bash -c \
  'chown 0:"$2" "$1/docker.sock"; chmod 660 "$1/docker.sock"' \
  identity-socket "$runtime_root" "$(id -g)"
env -u DOCKER_CONTEXT DOCKER_HOST="unix://$runtime_root/docker.sock" \
  docker info --format '{{.Driver}} {{.DockerRootDir}}'
stat -f "$runtime_root/data"
stat -c '%d %i' "$runtime_root/data"
docker exec "$helper_name" stat -f "$runtime_root/data"
docker exec "$helper_name" stat -c '%d %i' "$runtime_root/data"
```

Compare filesystem/device/inode/available-byte measurements from both
namespaces. Keep the data root visible at the exact absolute path to clients
that enforce the original storage guards. If a job runs inside another
container, explicitly bind that exact data-root path read-only; a merely
matching string is insufficient. A remote or namespace-invisible root must
remain unknown and be refused unless the existing qualifier has an explicit
supported independent-measurement interface.

Client processes inside the helper also need namespace-correct proxy values;
`docker exec` does not inherit exports made by the helper's PID 1. Execute a
qualification command with scoped endpoint and proxy normalization:

```bash
docker exec --env DOCKER_HOST="unix://$runtime_root/docker.sock" \
  --env NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt \
  "$helper_name" bash -c '
    export HTTP_PROXY="${http_proxy:-${HTTP_PROXY:-}}"
    export HTTPS_PROXY="${https_proxy:-${HTTPS_PROXY:-}}"
    export NO_PROXY="${no_proxy:-${NO_PROXY:-}}"
    exec "$@"
  ' identity-client COMMAND ARGUMENTS
```

Here `COMMAND ARGUMENTS` means the unchanged selected qualifier or workflow
runner, with task-owned source/output paths. Browser BuildKit's existing
optional `identity_proxy_ca` secret can use the public CA bundle when needed;
daemon trust alone does not install that CA inside a build image. Keep TLS
enabled and preserve immutable pins. Do not copy proxy values into public
receipts, image layers, Dockerfiles or committed configuration.

When local `act` uses this helper's host executor, its context's two fixed
temporary paths must also refer to the measured filesystem. Bind only those
task-owned directories inside the helper, after its initial mounts exist:

```bash
for name in identity-browser-ci identity-browser-local; do
  mkdir -p "$runtime_root/work/browser/runner-temp/$name"
  docker exec "$helper_name" mount --bind \
    "$runtime_root/work/browser/runner-temp/$name" "/tmp/$name"
done
```

The two destination directories must already exist inside the helper. This
mount mutation is confined to its own namespace and must be reapplied after
a helper restart. Independently measure those aliases before replay; their
free bytes come from the same pool as source, evidence and the daemon.

## Concrete failures and repairs

1. Native user/mount-namespace OverlayFS capability succeeded on tmpfs.
2. The first nested runc container failed self-reexec with
   `fork/exec /proc/self/fd/6: permission denied`. Tracing identified the
   file-bind-mounted runc binary's protected lower-directory reexec behavior.
   Copying the byte-identical binary to a normal helper file fixed execution;
   no runtime source, permissions policy or security code was patched. Both
   runc copies hash to
   `37f99361bd5e6ea4c44865697580009f215effb335e02d1966c52c534963c581`
   (runc 1.3.0, commit `4ca628d`, libseccomp 2.5.4).
3. Nonroot child namespace access required `SYS_PTRACE` in the helper's private
   PID namespace. Default bridge setup required its own `/proc/sys/net` view
   writable. A nonexistent named bridge was replaced with default bridge
   creation using the explicit helper-local subnet.
4. The original browser qualifier first refused source/evidence on the full
   workspace filesystem. Moving those task-owned paths onto the actual tmpfs
   passed its unchanged guards. No threshold was reduced.
5. The next actual immutable MCR pull timed out at the initial registry `/v2/`
   GET, before payload transfer. HTTPS curl success was not Docker transport
   proof. Host-forwarded uppercase proxy values differed from Docker-injected
   lowercase values inside the helper. Normalizing uppercase from lowercase
   repaired actual Go/Docker metadata acquisition with TLS enabled. Neither
   proxy values nor credential material are retained here.
6. Exact digest-only Docker metadata inspection then passed for both immutable
   Playwright and Node indexes. Node `manifest inspect` using a combined
   tag-and-digest reference failed CLI manifest verification; the digest-only
   metadata form passed. This is not evidence to alter the qualifier's pinned
   tag-and-digest `docker pull`; its actual run is the relevant test.

## Capability proof and remaining acceptance

An explicitly generated static C probe and tiny task-owned image proved real
image import, preservation of UID 1234 file ownership, UID 0/1000 execution,
none/default-bridge/host child networking, cgroup CPU/memory limits, BuildKit
`RUN`, and image export. These prove the owned engine can execute real Docker
workloads; they do not qualify Identity's full images.

The repaired original browser qualifier passed exit 0 on clean source
`9d11d9993555bbe1736cda5c43e4c2a8239e657c`, including its positive, negative and
restored checks. Its independent `ACTION_REPLAY_2026-11-22.md` checkpoint and
`action-replay-2026-11-22/original-docker/host-qualification.json` receipt own
that result; this engine observation is not a duplicate
acceptance record. The full development image, setup-twice default and
nonroot variants, exact workflow replay and eventual hosted/native/human gates
must retain their own truthful outcomes. No derived rootfs probe substitutes
for those results, and local `act` evidence is not GitHub-hosted CI evidence.

Before teardown, copy the small source-bound evidence to the task's durable
worktree. Stop/remove only this named helper and its own directory; never use
global `docker system prune`, delete shared image IDs or change global Docker
configuration. The tmpfs daemon and data are disposable execution state.
