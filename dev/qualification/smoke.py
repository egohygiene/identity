#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Run bounded functional checks inside a built development add-on image."""

from __future__ import annotations

import argparse
import hashlib
import http.server
import json
import os
from pathlib import Path
import platform
import shutil
import ssl
import subprocess
import tempfile
import threading
import tomllib


MARKER = "IDENTITY_DEV_CONTAINER_RECEIPT="
REPOSITORY = Path(__file__).resolve().parents[2]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def inventory(root: Path) -> dict[str, str]:
    return {
        item.relative_to(root).as_posix(): sha256(item.read_bytes())
        for item in sorted(root.rglob("*"))
        if item.is_file()
    }


def run(
    arguments: list[str], *, cwd: Path = REPOSITORY,
    environment: dict[str, str] | None = None,
    expected_exit_codes: tuple[int, ...] = (0,), timeout: int = 1200,
) -> str:
    print("Running: " + " ".join(arguments), flush=True)
    result = subprocess.run(
        arguments, cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, check=False, env=environment, timeout=timeout,
    )
    print(result.stdout, end="", flush=True)
    COMMANDS.append({
        "command": arguments,
        "exit_code": result.returncode,
        "expected_exit_codes": list(expected_exit_codes),
        "output_sha256": sha256(result.stdout.encode()),
    })
    if result.returncode not in expected_exit_codes:
        raise RuntimeError(f"Command failed with exit code {result.returncode}: {arguments[0]}")
    return result.stdout.strip()


COMMANDS: list[dict[str, object]] = []


def synthetic_ca_probe() -> dict[str, object]:
    """Prove explicit CA bindings locally without touching system trust stores."""
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            body = b"identity-local-ca-probe\n"
            self.send_response(200)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, _format, *args):
            pass

    environment = {key: value for key, value in os.environ.items() if key.upper() not in (
        "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY", "NODE_EXTRA_CA_CERTS",
        "CURL_CA_BUNDLE", "SSL_CERT_FILE", "SSL_CERT_DIR",
    )}
    environment["NO_PROXY"] = "127.0.0.1,localhost"
    with tempfile.TemporaryDirectory(prefix="identity-local-ca-") as temporary:
        root = Path(temporary)
        ca = root / "ca.pem"
        ca_key = root / "ca.key"
        key = root / "server.key"
        csr = root / "server.csr"
        certificate = root / "server.pem"
        extensions = root / "server.ext"
        extensions.write_text("subjectAltName=IP:127.0.0.1\nextendedKeyUsage=serverAuth\nbasicConstraints=CA:FALSE\n")
        run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "1", "-subj", "/CN=Identity disposable qualification CA", "-addext", "basicConstraints=critical,CA:TRUE", "-addext", "keyUsage=critical,keyCertSign,cRLSign", "-keyout", str(ca_key), "-out", str(ca)], timeout=30)
        run(["openssl", "req", "-new", "-newkey", "rsa:2048", "-nodes", "-subj", "/CN=localhost", "-keyout", str(key), "-out", str(csr)], timeout=30)
        run(["openssl", "x509", "-req", "-in", str(csr), "-CA", str(ca), "-CAkey", str(ca_key), "-CAcreateserial", "-days", "1", "-extfile", str(extensions), "-out", str(certificate)], timeout=30)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certificate, key)
        class Server(http.server.ThreadingHTTPServer):
            def get_request(self):
                connection, address = super().get_request()
                connection.settimeout(5)
                try:
                    return context.wrap_socket(connection, server_side=True), address
                except BaseException:
                    connection.close()
                    raise

        server = Server(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        url = f"https://127.0.0.1:{server.server_port}/"
        curl = ["curl", "--silent", "--show-error", "--fail", "--connect-timeout", "5", "--max-time", "10", "--noproxy", "*"]
        node_script = (
            'const https = require("node:https"); '
            'const request = https.get(process.argv[1], { timeout: 5000 }, (response) => { '
            'let body = ""; response.setEncoding("utf8"); response.on("data", (chunk) => body += chunk); '
            'response.on("end", () => { if (response.statusCode !== 200 || body !== "identity-local-ca-probe\\n") { process.exitCode = 5; } else { console.log("trusted"); } }); }); '
            'request.on("timeout", () => request.destroy(new Error("timeout"))); '
            'request.on("error", (error) => { console.error(error.code || "NON_CERTIFICATE_ERROR"); '
            'process.exitCode = ["UNABLE_TO_VERIFY_LEAF_SIGNATURE", "SELF_SIGNED_CERT_IN_CHAIN", "DEPTH_ZERO_SELF_SIGNED_CERT", "CERT_UNTRUSTED"].includes(error.code) ? 3 : 4; });'
        )
        try:
            run(curl + [url], environment=environment, expected_exit_codes=(60,), timeout=15)
            if run(curl + ["--cacert", str(ca), url], environment=environment, timeout=15) != "identity-local-ca-probe":
                raise RuntimeError("Curl did not receive the synthetic trusted TLS response")
            run(["node", "--eval", node_script, url], environment=environment, expected_exit_codes=(3,), timeout=15)
            trusted_environment = dict(environment, NODE_EXTRA_CA_CERTS=str(ca))
            if run(["node", "--eval", node_script, url], environment=trusted_environment, timeout=15) != "trusted":
                raise RuntimeError("Node did not receive the synthetic trusted TLS response")
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)
            if thread.is_alive():
                raise RuntimeError("The synthetic TLS server did not stop")
    return {
        "classification": "synthetic localhost CA-binding check; not a private proxy qualification",
        "unknown_ca_rejected": {"curl": True, "node": True},
        "explicit_ca_accepted": {"curl_cacert": True, "node_extra_ca_certs": True},
        "system_trust_modified": False,
        "certificate_or_key_bytes_recorded": False,
        "disposable_server_stopped": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-uid", type=int, required=True)
    parser.add_argument("--expected-gid", type=int, required=True)
    args = parser.parse_args()
    if (os.getuid(), os.getgid()) != (args.expected_uid, args.expected_gid):
        raise RuntimeError("The add-on changed the qualified development user's UID/GID")
    if platform.system() != "Linux" or platform.machine() not in ("x86_64", "amd64"):
        raise RuntimeError("This qualification covers only linux/amd64")
    if os.environ.get("NODE_TLS_REJECT_UNAUTHORIZED") == "0":
        raise RuntimeError("Qualification requires Node certificate verification")

    writable: dict[str, dict[str, object]] = {}
    for name in (
        "IDENTITY_DEV_PREFIX", "CARGO_HOME", "RUSTUP_HOME", "COREPACK_HOME",
        "PLAYWRIGHT_BROWSERS_PATH", "npm_config_cache", "XDG_CACHE_HOME",
    ):
        value = os.environ.get(name)
        if not value:
            raise RuntimeError(f"The activated environment does not declare {name}")
        directory = Path(value)
        directory.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryFile(dir=directory) as probe:
            probe.write(b"identity development-user permission probe\n")
            probe.flush()
        writable[name] = {"path": value, "writable": True, "owner_uid": directory.stat().st_uid}
    for relative in (".", "renderer", "renderer/node_modules", "target"):
        directory = REPOSITORY / relative
        with tempfile.TemporaryFile(dir=directory) as probe:
            probe.write(b"identity checkout permission probe\n")
            probe.flush()
        writable[relative] = {"writable": True, "owner_uid": directory.stat().st_uid}
    pnpm_store = Path(os.environ["IDENTITY_DEV_PREFIX"]) / "pnpm-store"
    with tempfile.TemporaryFile(dir=pnpm_store) as probe:
        probe.write(b"identity pnpm-store permission probe\n")
        probe.flush()
    writable["pnpm-store"] = {"writable": True, "owner_uid": pnpm_store.stat().st_uid}

    versions = {}
    for name, command in (
        ("python", ["python3", "--version"]),
        ("node", ["node", "--version"]),
        ("npm", ["npm", "--version"]),
        ("corepack", ["corepack", "--version"]),
        ("pnpm", ["corepack", "pnpm", "--version"]),
        ("rustc", ["rustc", "--version", "--verbose"]),
        ("cargo", ["cargo", "--version"]),
        ("rustup", ["rustup", "--version"]),
        ("cc", ["cc", "--version"]),
        ("curl", ["curl", "--version"]),
        ("libc", ["getconf", "GNU_LIBC_VERSION"]),
    ):
        # Corepack selects packageManager from the owning renderer workspace.
        versions[name] = run(command, cwd=REPOSITORY / "renderer" if name == "pnpm" else REPOSITORY)
    expected_rust = tomllib.loads((REPOSITORY / "rust-toolchain.toml").read_text())["toolchain"]["channel"]
    expected_pnpm = json.loads((REPOSITORY / "renderer/package.json").read_text())["packageManager"].split("@", 1)[1]
    if not versions["rustc"].startswith(f"rustc {expected_rust} "):
        raise RuntimeError("The installed Rust toolchain differs from the repository pin")
    if versions["pnpm"] != expected_pnpm:
        raise RuntimeError("The activated pnpm differs from the repository pin")
    if int(versions["node"].lstrip("v").split(".", 1)[0]) < 24:
        raise RuntimeError("The qualified Node runtime must be 24 or newer")
    ca_probe = synthetic_ca_probe()

    fixture = REPOSITORY / "tests/fixtures/v1/valid/minimal/.identity"
    fixture_before = inventory(fixture)
    binary = REPOSITORY / "target/debug/identity"
    with tempfile.TemporaryDirectory(prefix="identity-dev-qualification-") as temporary:
        temporary_root = Path(temporary)
        consumer = temporary_root / "consumer"
        consumer.mkdir()
        shutil.copytree(fixture, consumer / ".identity")
        copied_binary = temporary_root / "identity"
        shutil.copy2(binary, copied_binary)
        unrelated = consumer / "unrelated.txt"
        unrelated.write_bytes(b"Unrelated consumer source must remain unchanged.\n")
        source_before = inventory(consumer / ".identity")
        unrelated_before = unrelated.read_bytes()
        run([str(copied_binary), "--help"], cwd=temporary_root)
        for command in ("v1-inspect", "v1-recover"):
            run([str(copied_binary), command, "--help"], cwd=temporary_root)
        snapshots = []
        for _ in range(2):
            run([str(copied_binary), "v1-generate", "--repository-root", str(consumer)], cwd=temporary_root)
            run([str(copied_binary), "v1-verify", "--repository-root", str(consumer)], cwd=temporary_root)
            snapshots.append(inventory(consumer / "assets/identity"))
        if not snapshots[0] or ".identity-manifest.json" not in snapshots[0]:
            raise RuntimeError("Generation did not produce its complete manifest-bound output")
        if snapshots[0] != snapshots[1]:
            raise RuntimeError("Repeated generation changed the complete output inventory")
        if inventory(consumer / ".identity") != source_before or unrelated.read_bytes() != unrelated_before:
            raise RuntimeError("Generation or verification changed canonical/unrelated source")
    if inventory(fixture) != fixture_before:
        raise RuntimeError("Qualification changed the repository's canonical fixture")

    renderer = REPOSITORY / "renderer"
    for command in ("check", "test", "build", "validate:public"):
        run(["corepack", "pnpm", "run", command], cwd=renderer)
    receipt = {
        "status": "passed",
        "platform": "linux/amd64",
        "uid": os.getuid(), "gid": os.getgid(),
        "os_release": (Path("/etc/os-release").read_text()),
        "runtime_versions": versions,
        "writable_paths": writable,
        "strict_node_tls": True,
        "synthetic_ca_probe": ca_probe,
        "proxy_values_recorded": False,
        "shipping_cli_sha256": sha256(binary.read_bytes()),
        "canonical_fixture_files": len(fixture_before),
        "canonical_fixture_preserved": True,
        "unrelated_source_preserved": True,
        "repeated_output_equal": True,
        "complete_output_inventory": snapshots[0],
        "commands": COMMANDS,
        "limits": [
            "No browser installation, screenshot baseline or font-environment qualification.",
            "No claim about arbitrary custom bases, architectures or native host platforms.",
            "No release, registry push or deployment.",
        ],
    }
    print(MARKER + json.dumps(receipt, sort_keys=True, separators=(",", ":")), flush=True)


if __name__ == "__main__":
    main()
