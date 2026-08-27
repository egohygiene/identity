// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const rendererRoot = path.resolve(scriptDirectory, "..");
const sourceRoots = ["src", "scripts", "tests"];
const files = sourceRoots
  .flatMap((directory) => collectJavaScript(path.join(rendererRoot, directory)))
  .sort();

for (const file of files) {
  execFileSync(process.execPath, ["--check", file], {
    cwd: rendererRoot,
    stdio: "inherit",
  });
}

process.stdout.write(`Checked ${files.length} JavaScript source files.\n`);

function collectJavaScript(directory) {
  if (!fs.existsSync(directory)) {
    return [];
  }
  const results = [];
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const absolutePath = path.join(directory, entry.name);
    if (entry.isDirectory() && entry.name !== "__snapshots__") {
      results.push(...collectJavaScript(absolutePath));
      continue;
    }
    if (
      entry.isFile() &&
      [".js", ".mjs"].includes(path.extname(entry.name))
    ) {
      results.push(absolutePath);
    }
  }
  return results;
}
