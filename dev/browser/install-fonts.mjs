// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

// Image-build-only installation; browser qualification itself has no egress.
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";

const profile = JSON.parse(readFileSync(new URL("./profile.json", import.meta.url), "utf8"));
const directory = mkdtempSync(path.join(tmpdir(), "identity-browser-fonts-"));
try {
  const archives = [];
  if (profile.fontPackages?.length !== 2) throw new Error("The reviewed font pair must be explicit");
  for (const font of profile.fontPackages) {
    const expectedUrl = `https://archive.ubuntu.com/ubuntu/pool/main/f/fonts-dejavu/${font.name}_${font.version}_all.deb`;
    if (!["fonts-dejavu-core", "fonts-dejavu-mono"].includes(font.name) ||
        !/^[0-9A-Za-z.+~-]+$/u.test(font.version) || font.url !== expectedUrl ||
        !/^[0-9a-f]{64}$/u.test(font.sha256) || !Number.isSafeInteger(font.bytes) || font.bytes <= 0) {
      throw new Error("The browser font archive must have a reviewed immutable identity");
    }
    const response = await fetch(font.url, { signal: AbortSignal.timeout(60_000) });
    if (!response.ok) throw new Error(`Font archive download failed: HTTP ${response.status}`);
    const bytes = Buffer.from(await response.arrayBuffer());
    if (bytes.length !== font.bytes || createHash("sha256").update(bytes).digest("hex") !== font.sha256) {
      throw new Error(`Font archive identity differs: ${font.name}`);
    }
    const archive = path.join(directory, `${font.name}.deb`);
    writeFileSync(archive, bytes);
    archives.push(archive);
  }
  // Install intact packages together, retaining their dependency and copyright files.
  execFileSync("dpkg", ["--install", ...archives], { stdio: "inherit" });
  execFileSync("fc-cache", ["--force"], { stdio: "inherit" });
} finally {
  rmSync(directory, { recursive: true, force: true });
}
