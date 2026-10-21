// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { build } from "vite";

import { normalizeAssetBaseUrl, normalizeArtifactPath } from "../src/artifact-paths.js";
import { rendererRoot, MODEL_PATH, COMPILER_MANIFEST, KIT_MANIFEST, jsonBytes,
  prepareKit, verifyKit, inventory, outputPath, parseArguments, run } from "../lib/kit-bundle.mjs";

const args = parseArguments(process.argv.slice(2), [
  "artifact-root", "output-directory", "design-system-directory", "press-kit-directory",
  "asset-base-url", "icon-path", "apple-touch-icon-path", "web-manifest-path",
]);
if (!args["artifact-root"] || !args["output-directory"]) throw new Error("--artifact-root and --output-directory are required.");
const inputs = [args["artifact-root"], args["design-system-directory"], args["press-kit-directory"]];
const output = await outputPath(args["output-directory"], inputs);
const assetBaseUrl = normalizeAssetBaseUrl(args["asset-base-url"] || "./");
const browserAssets = Object.fromEntries([
  ["icon", args["icon-path"]], ["appleTouchIcon", args["apple-touch-icon-path"]], ["manifest", args["web-manifest-path"]],
].filter(([, value]) => value !== undefined).map(([key, value]) => [key, normalizeArtifactPath(value)]));
const { model, files } = await prepareKit({
  artifactRoot: args["artifact-root"], designSystemDirectory: args["design-system-directory"],
  pressKitDirectory: args["press-kit-directory"], browserAssets,
});
const work = await fs.mkdtemp(path.join(os.tmpdir(), "identity-consumer-kit-"));
try {
  const artifacts = path.join(work, "public");
  for (const [relative, bytes] of files) {
    const file = path.join(artifacts, ...relative.split("/").map(decodeURIComponent));
    await fs.mkdir(path.dirname(file), { recursive: true });
    await fs.writeFile(file, bytes);
  }
  const entry = path.join(work, "index.html");
  run(process.execPath, [path.join(rendererRoot, "scripts/render-static.mjs"),
    "--model", path.join(artifacts, MODEL_PATH), "--output", entry,
    "--audience", "public", "--asset-base-url", assetBaseUrl,
    "--artifact-root", artifacts, "--artifact-manifest", path.join(artifacts, COMPILER_MANIFEST),
    ...["icon-path", "apple-touch-icon-path", "web-manifest-path"].flatMap((flag) => args[flag] ? [`--${flag}`, args[flag]] : []),
  ]);
  // Only the bundler's trusted code entry is rebased; artifact paths stay unchanged.
  const client = path.relative(work, path.join(rendererRoot, "src/client.js")).split(path.sep).join("/");
  await fs.writeFile(entry, (await fs.readFile(entry, "utf8")).replace('src="./src/client.js"', `src="${client}"`));
  const staged = path.join(work, "site");
  await build({ configFile: false, root: work, base: "./", publicDir: artifacts,
    build: { outDir: staged, emptyOutDir: true, assetsInlineLimit: 0, sourcemap: false }, logLevel: "warn" });
  await fs.writeFile(path.join(staged, KIT_MANIFEST), jsonBytes({
    schema: "identity.consumer-brand-kit/v1", projectId: model.projectId, sourceDigest: model.release.sourceDigest,
    release: model.release, assetBaseUrl, browserAssets, files: await inventory(staged),
  }));
  await verifyKit(staged);
  // No existing nonempty directory is replaced, and source artifacts remain read-only.
  await outputPath(output, inputs);
  await fs.mkdir(path.dirname(output), { recursive: true });
  try { await fs.rmdir(output); } catch (error) { if (error.code !== "ENOENT") throw error; }
  await fs.cp(staged, output, { recursive: true, errorOnExist: true, force: false });
  await verifyKit(output);
  process.stdout.write(`Built public consumer Brand Kit: ${output} (${model.release.immutableId})\n`);
} finally {
  await fs.rm(work, { recursive: true, force: true });
}
