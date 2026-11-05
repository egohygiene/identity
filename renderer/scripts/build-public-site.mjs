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
import { normalizeArtifactPath, normalizeAssetBaseUrl } from "../src/artifact-paths.js";
import { verifyArtifactPaths } from "../src/download-integrity.js";
import { joinAssetUrl } from "../src/model.js";
import { prepareKit, outputPath } from "../lib/kit-bundle.mjs";

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
const configPath = argumentsMap.config
  ? path.resolve(repositoryRoot, argumentsMap.config)
  : path.resolve(sourceRoot, "publication/identity-brand-kit.config.json");
const config = await readJson(configPath);
if (![undefined, "legacy-assets", "native-v1"].includes(config.sourceMode)) {
  throw new Error("Unknown publication source mode.");
}
const nativeMode = config.sourceMode === "native-v1";
if (nativeMode && (!argumentsMap["source-root"] || !argumentsMap["release-tag"] || !argumentsMap["release-commit"])) {
  throw new Error("Native publication requires an explicitly selected release source, stable tag and commit.");
}
const releaseTag = argumentsMap["release-tag"] || config.release.defaultTag;
const releaseCommit = argumentsMap["release-commit"] || config.release.defaultCommit;
const releaseVersion = assertStableRelease(releaseTag, releaseCommit);
const assetBaseUrl = normalizeAssetBaseUrl(argumentsMap["asset-base-url"] || config.assetBaseUrl || "./");
const browserAssets = Object.fromEntries(Object.entries(config.browserAssets || {}).map(
  ([key, value]) => [key, normalizeArtifactPath(value, `Browser asset ${key}`)],
));
for (const key of Object.keys(browserAssets)) {
  if (!["icon", "appleTouchIcon", "manifest"].includes(key)) {
    throw new Error(`Unknown browser asset role: ${key}`);
  }
}
const designSystemDirectory = nativeMode
  ? await nativeInput("designSystem", "design-system-directory")
  : argumentsMap["design-system-directory"] ? path.resolve(argumentsMap["design-system-directory"]) : null;
const pressKitDirectory = nativeMode
  ? await nativeInput("pressKit", "press-kit-directory")
  : argumentsMap["press-kit-directory"] ? path.resolve(argumentsMap["press-kit-directory"]) : null;
const sourceAssetRoot = path.resolve(sourceRoot, "assets/identity");
const buildRoot = path.resolve(rendererRoot, ".identity-public-build");
const publicDirectory = path.join(buildRoot, "public");
const modelPath = path.join(buildRoot, "brand-kit.view-model.json");
const publicationPath = path.join(buildRoot, "publication.json");
const nativeAssetRoot = path.join(buildRoot, "native-assets");

await assertDirectory(sourceAssetRoot, "immutable Identity asset root");
let nativeKit = null;
if (nativeMode) {
  runSelectedConfigVerifier();
  nativeKit = await prepareKit({ artifactRoot: sourceAssetRoot,
    designSystemDirectory, pressKitDirectory, browserAssets });
  if (nativeKit.model.projectId !== "identity" || nativeKit.model.release.version !== releaseVersion) {
    throw new Error("Native Identity model does not match the selected release project/version.");
  }
  const reserved = new Set(["CNAME", "site.json", ...["zip", "manifest.json", "SHA256SUMS"]
    .map((suffix) => `packages/identity-brand-kit-v${releaseVersion}.${suffix}`)]);
  for (const relative of nativeKit.files.keys()) {
    if (reserved.has(relative) || relative === "brand-kit" || relative.startsWith("brand-kit/")) {
      throw new Error(`Native artifact collides with a publisher-owned path: ${relative}`);
    }
  }
  if (config.openGraphImage && !nativeKit.files.has(normalizeArtifactPath(config.openGraphImage))) {
    throw new Error("Native Open Graph image is absent from the verified selected artifacts.");
  }
  await outputPath(outputDirectory, [sourceAssetRoot, designSystemDirectory, pressKitDirectory]);
} else {
  await verifyArtifactPaths([
    ...config.assets.map((asset) => asset.sourcePath), ...Object.values(browserAssets),
  ], { artifactRoot: sourceAssetRoot });
}
for (const input of [sourceAssetRoot, designSystemDirectory, pressKitDirectory].filter(Boolean)) {
  const relative = path.relative(buildRoot, await fs.realpath(input));
  if (!relative || (!relative.startsWith(`..${path.sep}`) && relative !== ".." && !path.isAbsolute(relative))) {
    throw new Error("Publication staging cannot contain a selected input.");
  }
}
await fs.rm(buildRoot, { recursive: true, force: true });
await fs.mkdir(buildRoot, { recursive: true });
if (nativeMode) {
  for (const [relative, bytes] of nativeKit.files) {
    const destination = path.join(nativeAssetRoot, ...relative.split("/").map(decodeURIComponent));
    await fs.mkdir(path.dirname(destination), { recursive: true });
    await fs.writeFile(destination, bytes);
  }
  await fs.cp(nativeAssetRoot, publicDirectory, { recursive: true });
} else {
  await fs.cp(sourceAssetRoot, publicDirectory, { recursive: true });
}
await copyPublicationFiles();
const designSystem = !nativeMode && designSystemDirectory
  ? await copyDesignSystemArtifacts(designSystemDirectory)
  : null;
const pressKit = !nativeMode && pressKitDirectory
  ? await copyPressKitArtifacts(pressKitDirectory)
  : null;

runPythonPackager(nativeKit?.model.release.sourceDigest);
const packageManifestPath = path.join(
  publicDirectory,
  "packages",
  `identity-brand-kit-v${releaseVersion}.manifest.json`,
);
const packageManifest = await readJson(packageManifestPath);
const packageManifestSha256 = sha256(await fs.readFile(packageManifestPath));
const model = nativeMode ? nativeKit.model : await buildViewModel(packageManifest, designSystem, pressKit);
const publication = {
  canonicalUrl: config.canonicalUrl,
  releaseTag,
  releaseUrl: packageManifest.release.url,
  manifestPath: `packages/${path.basename(packageManifestPath)}`,
  manifestSha256: packageManifestSha256,
  ...(nativeMode ? { inventoryDigest: packageManifest.sourceDigest,
    archivePath: `packages/${packageManifest.archive.path}` } : {}),
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
      ...(nativeMode ? { sourceMode: "native-v1", canonicalSourceDigest: model.release.sourceDigest } : {}),
      publicationManifest: publication.manifestPath,
      publicationManifestSha256: publication.manifestSha256,
      assetBaseUrl,
      browserAssets,
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
    assetBaseUrl,
    "--artifact-root",
    publicDirectory,
    "--artifact-manifest",
    packageManifestPath,
    ...Object.entries({
      "icon-path": browserAssets.icon,
      "apple-touch-icon-path": browserAssets.appleTouchIcon,
      "web-manifest-path": browserAssets.manifest,
    }).flatMap(([flag, value]) => value === undefined ? [] : [`--${flag}`, value]),
    "--canonical-url",
    config.canonicalUrl,
    ...(nativeMode ? ["--audience", "public"] : []),
    ...(!nativeMode ? ["--open-graph-image", `${config.canonicalUrl}brand/open-graph.svg`]
      : config.openGraphImage ? ["--open-graph-image",
        new URL(joinAssetUrl(assetBaseUrl, normalizeArtifactPath(config.openGraphImage)), config.canonicalUrl).href] : []),
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

function runPythonPackager(canonicalSourceDigest) {
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
      ...(nativeMode ? ["--asset-root", nativeAssetRoot,
        "--canonical-source-digest", canonicalSourceDigest] : []),
    ],
    { cwd: repositoryRoot, encoding: "utf8", stdio: "inherit" },
  );
  if (result.status !== 0) {
    throw new Error("The public Brand Kit packager failed.");
  }
}

function runSelectedConfigVerifier() {
  const result = spawnSync(process.env.IDENTITY_PYTHON || (process.platform === "win32" ? "python" : "python3"), [
    path.join(repositoryRoot, "scripts/verify_publication_release_configs.py"),
    "--repository-root", repositoryRoot, "--source-root", sourceRoot,
    "--config", configPath, "--release-tag", releaseTag, "--release-commit", releaseCommit,
  ], { cwd: repositoryRoot, stdio: "inherit" });
  if (result.status !== 0) throw new Error("Native publication release/input binding failed.");
}

async function nativeInput(role, flag) {
  const value = config.nativeInputs?.[role];
  if (value === undefined) {
    if (argumentsMap[flag]) throw new Error(`Native optional input ${role} must be selected by release-owned config.`);
    return null;
  }
  const relative = normalizeArtifactPath(value, `Native ${role} directory`);
  const directory = await fs.realpath(path.join(sourceRoot, ...relative.split("/").map(decodeURIComponent)));
  const within = path.relative(await fs.realpath(sourceRoot), directory);
  if (!within || within === ".." || within.startsWith(`..${path.sep}`) || path.isAbsolute(within)) {
    throw new Error(`Native ${role} input escapes its release tree.`);
  }
  if (argumentsMap[flag] && await fs.realpath(path.resolve(argumentsMap[flag])) !== directory) {
    throw new Error(`Native ${role} CLI input disagrees with release-owned selection.`);
  }
  return directory;
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
      const sourcePath = normalizeArtifactPath(asset.sourcePath, "Public asset path");
      const contents = await fs.readFile(path.join(sourceAssetRoot, ...sourcePath.split("/").map(decodeURIComponent)));
      const embeddedText = asset.mediaType === "image/svg+xml"
        || asset.mediaType.startsWith("text/")
        || asset.mediaType === "application/json";
      return {
        id: asset.id,
        label: asset.label,
        mediaType: asset.mediaType,
        sha256: sha256(contents),
        altText: asset.altText,
        dimensions: asset.dimensions,
        intendedUse: asset.intendedUse,
        safeZone: asset.safeZone,
        text: embeddedText ? contents.toString("utf8") : "",
        availability: "generated-download",
        downloadPath: sourcePath,
        // Release-owned byte selection does not supply missing rights metadata.
        license: asset.license ?? null,
        origin: asset.origin ?? null,
        approval: asset.approval ?? null,
        ...(asset.usage === undefined ? {} : { usage: asset.usage }),
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
