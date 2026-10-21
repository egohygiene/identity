// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { isDeepStrictEqual } from "node:util";

import { JSDOM } from "jsdom";

import { normalizeArtifactPath, normalizeAssetBaseUrl } from "../src/artifact-paths.js";
import { artifactPathFromUrl, verifyArtifactDownloads, verifyArtifactPaths } from "../src/download-integrity.js";
import { assertBrandKitViewModel } from "../src/model.js";
import { createDesignSystemView } from "../src/design-system.js";
import { createPressKitView } from "../src/press-kit.js";

export const rendererRoot = fileURLToPath(new URL("../", import.meta.url));
export const MODEL_PATH = "brand-kit.view-model.json";
export const COMPILER_MANIFEST = ".identity-manifest.json";
export const KIT_MANIFEST = "kit.json";
const NATIVE_MODEL = "packages/renderer/brand-kit.view-model.json";

export const digest = (bytes) => createHash("sha256").update(bytes).digest("hex");
export const jsonBytes = (value) => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);

export function run(command, args, options = {}) {
  const result = spawnSync(command, args, { encoding: "utf8", ...options });
  if (result.status !== 0) throw new Error(`${command} failed: ${result.stderr || result.stdout || result.error}`);
  return result;
}

export function parseArguments(values, allowed) {
  const result = {};
  if (values[0] === "--") values = values.slice(1);
  for (let index = 0; index < values.length; index += 2) {
    const key = values[index]?.slice(2);
    if (!values[index]?.startsWith("--") || !allowed.includes(key) || Object.hasOwn(result, key)
      || !values[index + 1] || values[index + 1].startsWith("--")) {
      throw new Error(`Unknown, repeated or missing argument: ${values[index]}`);
    }
    result[key] = values[index + 1];
  }
  return result;
}

async function read(root, relative) {
  relative = normalizeArtifactPath(relative);
  await verifyArtifactPaths([relative], { artifactRoot: root });
  return fs.readFile(path.join(root, ...relative.split("/").map(decodeURIComponent)));
}

async function readJson(root, relative) {
  return JSON.parse((await read(root, relative)).toString("utf8"));
}

export function verifyPressKit(directory) {
  run(process.env.IDENTITY_PYTHON || (process.platform === "win32" ? "python" : "python3"), [
    fileURLToPath(new URL("../../scripts/render_press_kit.py", import.meta.url)),
    "--verify-directory", directory,
  ]);
}

function verifyHandbook(directory) {
  run(process.env.IDENTITY_PYTHON || (process.platform === "win32" ? "python" : "python3"), [
    fileURLToPath(new URL("../../scripts/render_design_system.py", import.meta.url)),
    "--verify-directory", directory,
  ]);
}

/** Read only selected native files and explicitly supplied governed projections. */
export async function prepareKit({ artifactRoot, designSystemDirectory, pressKitDirectory, browserAssets = {} }) {
  const root = await fs.realpath(artifactRoot);
  const manifest = await readJson(root, COMPILER_MANIFEST);
  if (manifest.schema !== "identity.compiler-manifest/v1") throw new Error("A native compiler manifest is required.");
  let model = assertBrandKitViewModel(await readJson(root, NATIVE_MODEL));
  if (model.designSystem || model.pressKit) throw new Error("The native model must precede optional projection composition.");
  const selected = await verifyArtifactDownloads(model, {
    artifactRoot: root, manifestPath: path.join(root, COMPILER_MANIFEST), browserAssets, includeFiles: true,
  });
  const files = new Map();
  const add = (relative, bytes) => {
    relative = normalizeArtifactPath(relative);
    if (files.has(relative) || relative === KIT_MANIFEST) throw new Error(`Kit artifact path collides: ${relative}`);
    files.set(relative, bytes);
  };
  for (const file of selected.files) add(file.path, file.bytes);
  add(COMPILER_MANIFEST, await read(root, COMPILER_MANIFEST));
  if (designSystemDirectory) {
    const directory = await fs.realpath(designSystemDirectory);
    const view = createDesignSystemView({
      handbook: await readJson(directory, "design-system-handbook.json"),
      context: await readJson(directory, "design-context.json"), artifactDirectory: "design-system",
    });
    model = assertBrandKitViewModel({ ...model, designSystem: view });
    verifyHandbook(directory);
    for (const artifact of view.artifacts) add(artifact.path, await read(directory, artifact.path.slice("design-system/".length)));
  }
  if (pressKitDirectory) {
    const directory = await fs.realpath(pressKitDirectory);
    verifyPressKit(directory);
    const view = createPressKitView({ pressKit: await readJson(directory, "press-kit.json"), artifactDirectory: "press-kit" });
    model = assertBrandKitViewModel({ ...model, pressKit: view });
    for (const relative of new Set([
      ...view.artifacts.map((artifact) => artifact.path),
      ...view.pressKit.assets.map((asset) => asset.downloadPath),
    ])) add(relative, await read(directory, relative.slice("press-kit/".length)));
  }
  add(MODEL_PATH, jsonBytes(model));
  return { model, files };
}

export async function inventory(root) {
  const files = {};
  async function walk(directory, prefix = "") {
    for (const entry of (await fs.readdir(directory, { withFileTypes: true })).sort((a, b) => a.name.localeCompare(b.name, "en"))) {
      const relative = `${prefix}${entry.name}`;
      if (entry.isSymbolicLink()) throw new Error(`Kit files cannot be symbolic links: ${relative}`);
      if (entry.isDirectory()) await walk(path.join(directory, entry.name), `${relative}/`);
      else if (entry.isFile() && relative !== KIT_MANIFEST) {
        const bytes = await read(root, relative);
        files[normalizeArtifactPath(relative)] = { sha256: digest(bytes), bytes: bytes.length };
      } else if (!entry.isFile()) throw new Error(`Unsupported kit entry: ${relative}`);
    }
  }
  await walk(root);
  return Object.fromEntries(Object.entries(files).sort(([left], [right]) => left < right ? -1 : left > right ? 1 : 0));
}

/** Offline verification checks the complete site, not just the page's links. */
export async function verifyKit(directory) {
  const root = await fs.realpath(directory);
  const receipt = await readJson(root, KIT_MANIFEST);
  if (receipt.schema !== "identity.consumer-brand-kit/v1") throw new Error("Unknown consumer Brand Kit receipt.");
  if (!isDeepStrictEqual(Object.keys(receipt).sort(), ["assetBaseUrl", "browserAssets", "files", "projectId", "release", "schema", "sourceDigest"])) {
    throw new Error("Consumer Brand Kit receipt has missing or unknown fields.");
  }
  if (!isDeepStrictEqual(await inventory(root), receipt.files)) throw new Error("Kit inventory/checksum mismatch.");
  const model = assertBrandKitViewModel(await readJson(root, MODEL_PATH));
  if (receipt.projectId !== model.projectId || receipt.sourceDigest !== model.release.sourceDigest
    || !isDeepStrictEqual(receipt.release, model.release)) throw new Error("Kit receipt does not match its source/release.");
  const base = normalizeAssetBaseUrl(receipt.assetBaseUrl);
  const browserAssets = receipt.browserAssets || {};
  if (Object.keys(browserAssets).some((key) => !["icon", "appleTouchIcon", "manifest"].includes(key))) {
    throw new Error("Kit receipt declares an unknown browser asset role.");
  }
  const verified = await verifyArtifactDownloads(model, {
    artifactRoot: root, manifestPath: path.join(root, COMPILER_MANIFEST), browserAssets,
  });
  if (model.designSystem) {
    verifyHandbook(path.join(root, "design-system"));
    const expected = createDesignSystemView({
      handbook: await readJson(root, "design-system/design-system-handbook.json"),
      context: await readJson(root, "design-system/design-context.json"), artifactDirectory: "design-system",
    });
    if (!isDeepStrictEqual(model.designSystem, expected)) throw new Error("Displayed handbook differs from its download.");
  }
  if (model.pressKit) {
    verifyPressKit(path.join(root, "press-kit"));
    const expected = createPressKitView({ pressKit: await readJson(root, "press-kit/press-kit.json"), artifactDirectory: "press-kit" });
    if (!isDeepStrictEqual(model.pressKit, expected)) throw new Error("Displayed Press Kit differs from its download.");
  }
  const document = new JSDOM((await read(root, "index.html")).toString("utf8")).window.document;
  const pageModel = document.querySelector("#identity-brand-kit-model");
  if (!pageModel || !isDeepStrictEqual(JSON.parse(pageModel.textContent), model)) throw new Error("Page and downloadable view model disagree.");
  const pageRoot = document.querySelector("#identity-brand-kit-root");
  if (pageRoot?.dataset.publicOnly !== "true" || pageRoot.dataset.assetBaseUrl !== base || document.querySelector("[data-studio]")) {
    throw new Error("Consumer kit must use the public audience and configured artifact base.");
  }
  for (const [key, relation] of [["icon", "icon"], ["appleTouchIcon", "apple-touch-icon"], ["manifest", "manifest"]]) {
    const links = [...document.querySelectorAll(`link[rel="${relation}"]`)];
    if (links.length > 1 || (links.length ? artifactPathFromUrl(links[0].getAttribute("href"), base) : undefined) !== browserAssets[key]) {
      throw new Error("Browser metadata differs from its selected kit artifacts.");
    }
  }
  for (const link of document.querySelectorAll("a[download]")) {
    if (!verified.verifiedPaths.includes(artifactPathFromUrl(link.getAttribute("href"), base))) {
      throw new Error("Page advertises a download absent from its selected model.");
    }
  }
  for (const link of document.querySelectorAll("nav a[href^='#']")) {
    if (!document.getElementById(link.getAttribute("href").slice(1))) throw new Error("Page navigation targets a missing section.");
  }
  return receipt;
}

/** Resolve existing parent links before guarding source/output overlap. */
export async function outputPath(value, inputs) {
  let existing = path.resolve(value);
  const tail = [];
  while (true) {
    try { await fs.lstat(existing); break; }
    catch (error) {
      if (error.code !== "ENOENT") throw error;
      tail.unshift(path.basename(existing));
      existing = path.dirname(existing);
    }
  }
  const output = path.join(await fs.realpath(existing), ...tail);
  if (output.split(path.sep).includes(".identity")) throw new Error("Kit output cannot enter canonical .identity source.");
  for (const input of inputs.filter(Boolean)) {
    const root = await fs.realpath(input);
    const within = (parent, child) => { const relative = path.relative(parent, child); return !relative || (!relative.startsWith(`..${path.sep}`) && relative !== ".." && !path.isAbsolute(relative)); };
    if (within(root, output) || within(output, root)) throw new Error("Kit output and input directories must be disjoint.");
  }
  try {
    if (!(await fs.lstat(output)).isDirectory() || (await fs.readdir(output)).length) throw new Error("Kit output must be new or empty.");
  } catch (error) { if (error.code !== "ENOENT") throw error; }
  return output;
}
