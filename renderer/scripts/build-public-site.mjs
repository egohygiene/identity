// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

import { createDesignSystemView } from "../src/design-system.js";
import { createPressKitView } from "../src/press-kit.js";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const rendererRoot = path.resolve(scriptDirectory, "..");
const repositoryRoot = path.resolve(rendererRoot, "..");
const argumentsMap = parseArguments(process.argv.slice(2));
const sourceRoot = path.resolve(
  argumentsMap["source-root"] || repositoryRoot,
);
const outputDirectory = path.resolve(
  rendererRoot,
  argumentsMap["output-directory"] || "dist",
);
const configPath = path.resolve(
  repositoryRoot,
  argumentsMap.config || "publication/identity-brand-kit.config.json",
);
const config = await readJson(configPath);
const releaseTag = argumentsMap["release-tag"] || config.release.defaultTag;
const releaseCommit = argumentsMap["release-commit"] || config.release.defaultCommit;
const releaseVersion = assertStableRelease(releaseTag, releaseCommit);
const designSystemDirectory = argumentsMap["design-system-directory"]
  ? path.resolve(argumentsMap["design-system-directory"])
  : null;
const pressKitDirectory = argumentsMap["press-kit-directory"]
  ? path.resolve(argumentsMap["press-kit-directory"])
  : null;
const sourceAssetRoot = path.resolve(sourceRoot, "assets/identity");
const buildRoot = path.resolve(rendererRoot, ".identity-public-build");
const publicDirectory = path.join(buildRoot, "public");
const modelPath = path.join(buildRoot, "brand-kit.view-model.json");
const publicationPath = path.join(buildRoot, "publication.json");

await assertDirectory(sourceAssetRoot, "immutable Identity asset root");
await fs.rm(buildRoot, { recursive: true, force: true });
await fs.mkdir(buildRoot, { recursive: true });
await fs.cp(sourceAssetRoot, publicDirectory, { recursive: true });
await copyPublicationFiles();
const designSystem = designSystemDirectory
  ? await copyDesignSystemArtifacts(designSystemDirectory)
  : null;
const pressKit = pressKitDirectory
  ? await copyPressKitArtifacts(pressKitDirectory)
  : null;

runPythonPackager();
const packageManifestPath = path.join(
  publicDirectory,
  "packages",
  `identity-brand-kit-v${releaseVersion}.manifest.json`,
);
const packageManifest = await readJson(packageManifestPath);
const packageManifestSha256 = sha256(await fs.readFile(packageManifestPath));
const model = await buildViewModel(packageManifest, designSystem, pressKit);
const publication = {
  canonicalUrl: config.canonicalUrl,
  releaseTag,
  releaseUrl: packageManifest.release.url,
  manifestPath: `packages/${path.basename(packageManifestPath)}`,
  manifestSha256: packageManifestSha256,
};

await fs.writeFile(modelPath, `${JSON.stringify(model, null, 2)}\n`, "utf8");
await fs.writeFile(
  publicationPath,
  `${JSON.stringify(publication, null, 2)}\n`,
  "utf8",
);
await fs.writeFile(
  path.join(publicDirectory, "site.json"),
  `${JSON.stringify(
    {
      schema: "identity.public-brand-kit-site/v1",
      canonicalUrl: config.canonicalUrl,
      aliases: ["/brand-kit/"],
      release: packageManifest.release,
      sourceDigest: packageManifest.sourceDigest,
      publicationManifest: publication.manifestPath,
      publicationManifestSha256: publication.manifestSha256,
    },
    null,
    2,
  )}\n`,
  "utf8",
);

runNode(
  [
    path.join(scriptDirectory, "render-static.mjs"),
    "--model",
    modelPath,
    "--output",
    path.join(rendererRoot, "index.html"),
    "--asset-base-url",
    "./",
    "--canonical-url",
    config.canonicalUrl,
    "--open-graph-image",
    `${config.canonicalUrl}brand/open-graph.svg`,
    "--publication",
    publicationPath,
  ],
  { IDENTITY_RENDERER_PUBLIC_DIR: publicDirectory },
);
runNode(
  [
    path.join(rendererRoot, "node_modules/vite/bin/vite.js"),
    "build",
    "--outDir",
    outputDirectory,
  ],
  { IDENTITY_RENDERER_PUBLIC_DIR: publicDirectory },
);

process.stdout.write(
  `Built public Brand Kit: ${outputDirectory} from ${releaseTag} (${packageManifest.sourceDigest})\n`,
);

async function copyPublicationFiles() {
  await fs.copyFile(
    path.join(repositoryRoot, "publication", "CNAME"),
    path.join(publicDirectory, "CNAME"),
  );
  await fs.cp(
    path.join(repositoryRoot, "publication", "routes", "brand-kit"),
    path.join(publicDirectory, "brand-kit"),
    { recursive: true },
  );
}

async function copyDesignSystemArtifacts(directory) {
  const destination = path.join(publicDirectory, "design-system");
  await assertDirectory(directory, "generated design-system artifact directory");
  await fs.cp(directory, destination, { recursive: true });
  const [handbook, context] = await Promise.all([
    readJson(path.join(directory, "design-system-handbook.json")),
    readJson(path.join(directory, "design-context.json")),
  ]);
  return createDesignSystemView({
    handbook,
    context,
    artifactDirectory: "design-system",
  });
}

async function copyPressKitArtifacts(directory) {
  const destination = path.join(publicDirectory, "press-kit");
  await assertDirectory(directory, "generated Press Kit artifact directory");
  await fs.cp(directory, destination, { recursive: true });
  return createPressKitView({
    pressKit: await readJson(path.join(directory, "press-kit.json")),
    artifactDirectory: "press-kit",
  });
}

function runPythonPackager() {
  const result = spawnSync(
    "python3",
    [
      path.join(repositoryRoot, "scripts", "package_public_brand_kit.py"),
      "--source-root",
      sourceRoot,
      "--stage-directory",
      publicDirectory,
      "--release-tag",
      releaseTag,
      "--release-commit",
      releaseCommit,
    ],
    { cwd: repositoryRoot, encoding: "utf8", stdio: "inherit" },
  );
  if (result.status !== 0) {
    throw new Error("The public Brand Kit packager failed.");
  }
}

function runNode(argumentsList, environment) {
  const result = spawnSync(process.execPath, argumentsList, {
    cwd: rendererRoot,
    env: { ...process.env, ...environment },
    encoding: "utf8",
    stdio: "inherit",
  });
  if (result.status !== 0) {
    throw new Error(`Node command failed: ${argumentsList.join(" ")}`);
  }
}

async function buildViewModel(packageManifest, designSystem, pressKit) {
  const assets = await Promise.all(
    config.assets.map(async (asset) => {
      const sourcePath = safeRelativePath(asset.sourcePath);
      const contents = await fs.readFile(path.join(sourceAssetRoot, sourcePath));
      return {
        id: asset.id,
        label: asset.label,
        mediaType: asset.mediaType,
        sha256: sha256(contents),
        altText: asset.altText,
        dimensions: asset.dimensions,
        intendedUse: asset.intendedUse,
        safeZone: asset.safeZone,
        text: contents.toString("utf8"),
        availability: "generated-download",
        downloadPath: sourcePath,
        license: {
          spdx: "MIT",
          status: "approved",
          attribution: "Ego Hygiene contributors",
        },
        origin: {
          creator: "Ego Hygiene",
          method: "deterministic vector projection",
          source: `assets/identity/${sourcePath}`,
          capturedAt: "2026-08-22",
        },
        approval: "human-approved-visual-direction",
      };
    }),
  );

  return {
    schema: "identity.brand-kit-view-model/v1",
    projectId: config.project.id,
    project: {
      displayName: config.project.displayName,
      repository: config.project.repository,
      tagline: config.project.tagline,
    },
    release: {
      version: releaseVersion,
      profileVersion: releaseVersion,
      sourceDigest: packageManifest.sourceDigest,
      immutableId: `sha256:${packageManifest.sourceDigest}`,
      status: "published",
    },
    tokens: config.tokens,
    assets,
    guidance: config.guidance,
    support: config.support,
    ...(designSystem ? { designSystem } : {}),
    ...(pressKit ? { pressKit } : {}),
    packages: [
      {
        id: "complete-brand-kit",
        label: "Complete Brand Kit",
        path: `packages/${packageManifest.archive.path}`,
        mediaType: "application/zip",
        intendedUse: "Versioned offline archive of approved public Brand Kit assets.",
      },
      {
        id: "publication-manifest",
        label: "Publication manifest",
        path: `packages/${path.basename(packageManifestPath)}`,
        mediaType: "application/json",
        intendedUse: "Release, source-digest, file-inventory, and archive-integrity record.",
      },
      {
        id: "publication-checksums",
        label: "Publication checksums",
        path: `packages/identity-brand-kit-v${releaseVersion}.SHA256SUMS`,
        mediaType: "text/plain",
        intendedUse: "SHA-256 checksums for the downloadable archive and manifest.",
      },
    ],
  };
}

function assertStableRelease(tag, commit) {
  const tagMatch = /^v(\d+\.\d+\.\d+)$/u.exec(tag);
  if (!tagMatch) {
    throw new Error("The public Brand Kit requires a stable semantic-version release tag.");
  }
  if (!/^[0-9a-f]{40}$/u.test(commit)) {
    throw new Error("The public Brand Kit requires a lowercase 40-character release commit.");
  }
  return tagMatch[1];
}

function assertDirectory(directory, description) {
  return fs.stat(directory).then((status) => {
    if (!status.isDirectory()) {
      throw new Error(`${description} is not a directory: ${directory}`);
    }
  });
}

async function readJson(filePath) {
  try {
    return JSON.parse(await fs.readFile(filePath, "utf8"));
  } catch (error) {
    throw new Error(`Cannot read ${filePath}: ${error.message}`);
  }
}

function safeRelativePath(value) {
  if (typeof value !== "string" || value.length === 0 || path.isAbsolute(value)) {
    throw new Error("A public Brand Kit asset path must be a non-empty relative path.");
  }
  const normalized = path.posix.normalize(value);
  if (normalized === ".." || normalized.startsWith("../")) {
    throw new Error(`A public Brand Kit asset path escapes its source root: ${value}`);
  }
  return normalized;
}

function sha256(contents) {
  return createHash("sha256").update(contents).digest("hex");
}

function parseArguments(values) {
  const result = {};
  const argumentValues = values[0] === "--" ? values.slice(1) : values;
  for (let index = 0; index < argumentValues.length; index += 1) {
    const value = argumentValues[index];
    if (!value.startsWith("--")) {
      throw new Error(`Unexpected positional argument: ${value}`);
    }
    const key = value.slice(2);
    const next = argumentValues[index + 1];
    if (!next || next.startsWith("--")) {
      throw new Error(`Argument --${key} requires a value.`);
    }
    result[key] = next;
    index += 1;
  }
  return result;
}
