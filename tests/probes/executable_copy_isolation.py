#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT
"""Bounded Linux probe for inherited writable executable descriptors.

This uses the system's true executable, never Identity source or user media.
It demonstrates a kernel/process mechanism, not the cause of an old CI run.
"""

from __future__ import annotations

import errno
import hashlib
import json
import os
from pathlib import Path
import select
import shutil
import signal
import subprocess
import sys
import tempfile
import time


TIMEOUT = 5


def receive(descriptor: int) -> None:
    ready, _, _ = select.select([descriptor], [], [], TIMEOUT)
    if not ready or os.read(descriptor, 1) != b"1":
        raise RuntimeError("child readiness/release timed out")


class HeldChild:
    """Retain a child at a pipe barrier without an unbounded wait."""

    def __init__(self, writer: Path | None = None):
        ready_read, ready_write = os.pipe()
        release_read, release_write = os.pipe()
        self.pid = os.fork()
        self.reaped = False
        if self.pid == 0:
            try:
                os.close(ready_read)
                os.close(release_write)
                descriptor = os.open(writer, os.O_WRONLY) if writer else None
                os.write(ready_write, b"1")
                receive(release_read)
                if descriptor is not None:
                    os.close(descriptor)
                os._exit(0)
            except BaseException:
                os._exit(1)
        os.close(ready_write)
        os.close(release_read)
        self.release_write: int | None = release_write
        try:
            receive(ready_read)
        except BaseException:
            self.close()
            raise
        finally:
            os.close(ready_read)

    def release(self) -> None:
        assert self.release_write is not None
        os.write(self.release_write, b"1")
        os.close(self.release_write)
        self.release_write = None
        deadline = time.monotonic() + TIMEOUT
        while time.monotonic() < deadline:
            child, status = os.waitpid(self.pid, os.WNOHANG)
            if child:
                self.reaped = True
                if not os.WIFEXITED(status) or os.WEXITSTATUS(status) != 0:
                    raise RuntimeError("barrier child failed")
                return
            time.sleep(0.01)
        raise RuntimeError("child exit timed out")

    def close(self) -> None:
        if not self.reaped:
            os.kill(self.pid, signal.SIGKILL)
            os.waitpid(self.pid, 0)
            self.reaped = True
        if self.release_write is not None:
            os.close(self.release_write)
            self.release_write = None


def execute(path: Path) -> dict[str, int | None]:
    try:
        result = subprocess.run([path], check=False, timeout=TIMEOUT)
        return {"exit_code": result.returncode, "errno": None}
    except OSError as failure:
        return {"exit_code": None, "errno": failure.errno}


def probe() -> dict[str, object]:
    if not sys.platform.startswith("linux") or not hasattr(os, "fork"):
        raise RuntimeError("this mechanism probe requires Linux fork semantics")
    source = shutil.which("true")
    if source is None:
        raise RuntimeError("a system true executable is required")
    expected = hashlib.sha256(Path(source).read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory(prefix="identity-executable-copy-") as directory:
        binary = Path(directory) / "true-copy"
        shutil.copyfile(source, binary)
        binary.chmod(0o700)

        # Model a fork while a parent thread has the destination open for
        # writing. After the parent's close, the child still holds that inode.
        writer = os.open(binary, os.O_WRONLY)
        inherited = HeldChild()
        try:
            os.close(writer)
            inherited_result = execute(binary)
            assert inherited_result["errno"] == errno.ETXTBSY, inherited_result
            inherited.release()
            after_inherited_exit = execute(binary)
            assert after_inherited_exit["exit_code"] == 0, after_inherited_exit
        finally:
            inherited.close()

        # An unrelated child forked by the parent cannot inherit a descriptor
        # opened only in the isolated writer. Keep that unrelated child alive
        # after the writer exits, and prove execution succeeds.
        isolated = HeldChild(binary)
        unrelated = None
        try:
            while_writer_held = execute(binary)
            assert while_writer_held["errno"] == errno.ETXTBSY, while_writer_held
            unrelated = HeldChild()
            isolated.release()
            os.kill(unrelated.pid, 0)
            after_isolated_exit = execute(binary)
            assert after_isolated_exit["exit_code"] == 0, after_isolated_exit
            unrelated.release()
        finally:
            isolated.close()
            if unrelated is not None:
                unrelated.close()
        actual = hashlib.sha256(binary.read_bytes()).hexdigest()
        assert actual == expected
    return {
        "schema": "identity.executable-copy-mechanism-probe/v1",
        "platform": sys.platform,
        "system_executable_sha256": expected,
        "parent_writer_inherited_by_live_child": inherited_result,
        "after_inheriting_child_exits": after_inherited_exit,
        "while_isolated_writer_is_live": while_writer_held,
        "after_isolated_writer_exits_with_unrelated_child_still_live": after_isolated_exit,
        "copied_bytes_unchanged": True,
        "scope": "Controlled mechanism evidence; not historical CI causality or Identity product qualification.",
    }


if __name__ == "__main__":
    print(json.dumps(probe(), indent=2, sort_keys=True))
