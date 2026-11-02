// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { createHash } from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import { isDeepStrictEqual } from "node:util";

import { normalizeArtifactPath, normalizeAssetBaseUrl } from "./artifact-paths.js";

const RENDERER_OUTPUT = "packages/renderer/brand-kit.view-model.json";

/** Check supplied artifact bytes without changing the model-only preview port. */
export async function verifyArtifactDownloads(model, {
  artifactRoot,
  manifestPath,
  browserAssets = {},
  includeFiles = false,
}) {
  const read = await artifactReader(artifactRoot);
  const inventory = manifestPath
    ? await manifestInventory(model, manifestPath, read)
    : null;
  const advertised = [
    ...(model.assets || []).filter((asset) => asset.downloadPath).map((asset) => ({
      path: asset.downloadPath, sha256: asset.sha256, bound: true,
    })),
    ...(model.packages || []).map((entry) => ({ path: entry.path, bound: true })),
    ...(model.downloads || []).map((entry) => ({ path: entry.path, bound: true })),
    ...Object.values(browserAssets).filter((value) => value !== undefined)
      .map((value) => ({ path: value, bound: true })),
    ...(model.designSystem?.artifacts || []).map((entry) => ({ path: entry.path })),
    ...(model.pressKit?.artifacts || []).map((entry) => ({ path: entry.path })),
    ...(model.pressKit?.pressKit?.assets || []).map((asset) => ({
      path: asset.downloadPath, sha256: asset.sha256,
    })),
  ];
  for (const entry of advertised) {
    const file = await read(entry.path);
    if (entry.sha256 !== undefined && file.sha256 !== entry.sha256) {
      throw new Error(`Advertised asset checksum does not match: ${entry.path}`);
    }
    if (inventory && entry.bound && !inventory.has(file.path)) {
      throw new Error(`Advertised artifact is absent from the selected manifest: ${entry.path}`);
    }
  }
  if (browserAssets.manifest !== undefined) {
    const manifestFile = await read(browserAssets.manifest);
    const webManifest = JSON.parse(manifestFile.bytes.toString("utf8"));
    if (webManifest.icons !== undefined && !Array.isArray(webManifest.icons)) {
      throw new Error("The browser manifest icons must be an array.");
    }
    const directory = path.posix.dirname(manifestFile.path);
    for (const icon of webManifest.icons || []) {
      const iconPath = normalizeArtifactPath(icon.src, "Browser manifest icon path");
      const relativePath = directory === "." ? iconPath : `${directory}/${iconPath}`;
      const file = await read(relativePath);
      if (inventory && !inventory.has(file.path)) {
        throw new Error(`Browser manifest icon is absent from the selected manifest: ${relativePath}`);
      }
      advertised.push({ path: relativePath });
    }
  }
  const verifiedPaths = [...new Set(advertised.map((entry) => normalizeArtifactPath(entry.path)))];
  return {
    verifiedPaths,
    ...(includeFiles ? {
      files: await Promise.all([...new Set([...(inventory?.keys() || []), ...verifiedPaths])].map(read)),
    } : {}),
  };
}

/** Verify extra emitted links with the same path and filesystem confinement. */
export async function verifyArtifactPaths(paths, { artifactRoot }) {
  const read = await artifactReader(artifactRoot);
  for (const relativePath of paths) await read(relativePath);
}

/** Map a configured local/CDN URL back to its local artifact; never fetch it. */
export function artifactPathFromUrl(value, assetBaseUrl = "./") {
  const base = normalizeAssetBaseUrl(assetBaseUrl);
  if (typeof value !== "string" || !value.startsWith(base)) {
    throw new Error(`Artifact URL does not use the configured asset base: ${value}`);
  }
  return normalizeArtifactPath(value.slice(base.length), "Published artifact URL");
}

async function artifactReader(artifactRoot) {
  if (typeof artifactRoot !== "string" || !artifactRoot.length) {
    throw new Error("Artifact verification requires an artifact root.");
  }
  const root = await fs.realpath(path.resolve(artifactRoot));
  if (!(await fs.stat(root)).isDirectory()) {
    throw new Error("Artifact root must be a directory.");
  }
  const cache = new Map();
  return async (value) => {
    const relativePath = normalizeArtifactPath(value, "Verified artifact path");
    if (cache.has(relativePath)) return cache.get(relativePath);
    const candidate = path.join(root, ...relativePath.split("/").map(decodeURIComponent));
    let resolved;
    try {
      resolved = await fs.realpath(candidate);
    } catch (error) {
      throw new Error(`Advertised artifact is missing: ${relativePath}`, { cause: error });
    }
    const within = path.relative(root, resolved);
    if (within === ".." || within.startsWith(`..${path.sep}`) || path.isAbsolute(within)) {
      throw new Error(`Artifact resolves outside its root: ${relativePath}`);
    }
    const status = await fs.stat(resolved);
    if (!status.isFile() || status.size === 0) {
      throw new Error(`Expected a non-empty artifact file: ${relativePath}`);
    }
    const bytes = await fs.readFile(resolved);
    const result = { path: relativePath, bytes, sha256: sha256(bytes), size: bytes.length };
    cache.set(relativePath, result);
    return result;
  };
}

async function manifestInventory(model, manifestPath, read) {
  const manifestBytes = await fs.readFile(path.resolve(manifestPath));
  const manifest = JSON.parse(manifestBytes.toString("utf8"));
  if (!/^[0-9a-f]{64}$/u.test(manifest.sourceDigest || "") || manifest.sourceDigest !== model.release?.sourceDigest) {
    throw new Error("Artifact manifest source digest does not match the renderer release.");
  }
  const inventory = new Map();
  const add = async (value, expected) => {
    const relativePath = normalizeArtifactPath(value, "Manifest artifact path");
    if (inventory.has(relativePath)) {
      throw new Error(`Manifest contains a duplicate artifact path: ${relativePath}`);
    }
    const size = expected.bytes ?? expected.sizeBytes;
    if (!/^[0-9a-f]{64}$/u.test(expected.sha256 || "") || !Number.isSafeInteger(size) || size <= 0) {
      throw new Error(`Manifest has invalid integrity evidence: ${relativePath}`);
    }
    const file = await read(relativePath);
    if (file.sha256 !== expected.sha256 || file.size !== size) {
      throw new Error(`Artifact does not match manifest checksum/size: ${relativePath}`);
    }
    inventory.set(relativePath, expected);
  };
  if (manifest.schema === "identity.compiler-manifest/v1") {
    if (manifest.projectId !== model.projectId || !Array.isArray(manifest.outputs)) {
      throw new Error("Compiler manifest does not match the renderer project/output contract.");
    }
    const renderer = manifest.outputs.find((output) => output.targetId === "reference-renderer-view-model");
    const rendererPath = normalizeArtifactPath(renderer?.path, "Compiler renderer output path");
    if (!rendererPath.endsWith(`/${RENDERER_OUTPUT}`) && rendererPath !== RENDERER_OUTPUT) {
      throw new Error("Compiler manifest is missing its reference-renderer output binding.");
    }
    const prefix = rendererPath.slice(0, -RENDERER_OUTPUT.length);
    for (const output of manifest.outputs) {
      const outputPath = normalizeArtifactPath(output.path, "Compiler output path");
      if (!outputPath.startsWith(prefix)) {
        throw new Error("Compiler outputs disagree about their artifact root.");
      }
      await add(outputPath.slice(prefix.length), output);
    }
    const rendererFile = await read(RENDERER_OUTPUT);
    const selectedModel = JSON.parse(rendererFile.bytes.toString("utf8"));
    const coreModel = ({ designSystem, pressKit, ...core }) => core;
    if (!isDeepStrictEqual(coreModel(model), coreModel(selectedModel))) {
      throw new Error("Renderer model does not match the compiler manifest's selected output.");
    }
  } else if (manifest.schema === "identity.public-brand-kit-manifest/v1") {
    if (manifest.release?.tag !== `v${model.release?.version}`) {
      throw new Error("Public manifest release does not match the renderer release.");
    }
    if (!Array.isArray(manifest.files)) throw new Error("Public manifest must declare its file inventory.");
    for (const entry of manifest.files) await add(entry.path, entry);
    const manifestName = path.basename(manifestPath);
    await add(`packages/${manifestName}`, { sha256: sha256(manifestBytes), bytes: manifestBytes.length });
    const archiveName = normalizeArtifactPath(manifest.archive?.path, "Public archive path");
    await add(`packages/${archiveName}`, manifest.archive);
    const checksumsPath = `packages/${archiveName.replace(/\.zip$/u, ".SHA256SUMS")}`;
    const checksums = await read(checksumsPath);
    const expectedChecksums = new Map([
      [archiveName, manifest.archive.sha256],
      [manifestName, sha256(manifestBytes)],
    ]);
    for (const line of checksums.bytes.toString("utf8").trim().split("\n")) {
      const match = /^([0-9a-f]{64})  (.+)$/u.exec(line);
      if (!match || expectedChecksums.get(match[2]) !== match[1]) {
        throw new Error("Public checksum file does not match its manifest/archive.");
      }
      expectedChecksums.delete(match[2]);
    }
    if (expectedChecksums.size) throw new Error("Public checksum file omits required entries.");
    inventory.set(checksumsPath, { sha256: checksums.sha256, bytes: checksums.size });
  } else {
    throw new Error(`Unsupported artifact manifest schema: ${manifest.schema}`);
  }
  return inventory;
}

function sha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}
