// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const rendererRoot = fileURLToPath(new URL("../", import.meta.url));
export const receipt = JSON.parse(fs.readFileSync(new URL("../fixtures/complete-kit/receipt.json", import.meta.url), "utf8"));
const archivePath = fileURLToPath(new URL("../fixtures/complete-kit/inputs.zip", import.meta.url));

export function unpackKitFixtures(directory) {
  const hash = createHash("sha256").update(fs.readFileSync(archivePath)).digest("hex");
  if (hash !== receipt.archiveSha256) throw new Error("Generated fixture archive differs from its retained receipt.");
  execFileSync("python3", ["-c", "import sys,zipfile; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])", archivePath, directory]);
  for (const [name, selected] of Object.entries(receipt.cases)) {
    for (const [relative, expected] of Object.entries(selected.generatedFiles)) {
      const bytes = fs.readFileSync(path.join(directory, name, relative));
      if (bytes.length !== expected.bytes || createHash("sha256").update(bytes).digest("hex") !== expected.sha256) {
        throw new Error(`Generated fixture file differs: ${name}/${relative}`);
      }
    }
  }
}

export function buildKit(input, output, extra = []) {
  const args = [path.join(rendererRoot, "scripts/build-kit.mjs"), "--artifact-root", path.join(input, "native"), "--output-directory", output];
  for (const [name, flag] of [["handbook", "design-system-directory"], ["press", "press-kit-directory"]]) {
    if (fs.existsSync(path.join(input, name))) args.push(`--${flag}`, path.join(input, name));
  }
  return execFileSync(process.execPath, [...args, ...extra], { cwd: rendererRoot, encoding: "utf8", stdio: "pipe" });
}
