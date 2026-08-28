// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

export const PRESS_KIT_PROJECTION_SCHEMA = "identity.press-kit/v1";

/**
 * Validate a generated Press Kit projection and adapt its links for the static
 * public renderer. The renderer receives immutable approved facts only.
 */
export function createPressKitView({ pressKit, artifactDirectory }) {
  assertProjection(pressKit);
  const directory = normalizeArtifactDirectory(artifactDirectory);
  return {
    pressKit: {
      ...pressKit,
      assets: pressKit.assets.map((asset) => ({
        ...asset,
        downloadPath: `${directory}${normalizeRelativePath(
          asset?.downloadPath,
          "Press Kit asset download path",
        )}`,
      })),
    },
    artifacts: pressKit.artifacts.map((artifact) => ({
      ...artifact,
      path: `${directory}${normalizeRelativePath(
        artifact?.path,
        "Press Kit artifact path",
      )}`,
    })),
  };
}

export function assertPressKitView(value) {
  assertObject(value, "Press Kit renderer view");
  assertProjection(value.pressKit);
  if (!Array.isArray(value.artifacts) || value.artifacts.length < 5) {
    throw new TypeError("Press Kit renderer view must declare complete artifacts.");
  }
  const jsonArtifact = value.artifacts.find(
    (artifact) => artifact?.id === "press-kit-json",
  );
  if (!jsonArtifact || typeof jsonArtifact.path !== "string") {
    throw new TypeError("Press Kit renderer view must declare the JSON artifact path.");
  }
  const suffix = "press-kit.json";
  if (!jsonArtifact.path.endsWith(suffix)) {
    throw new TypeError("Press Kit renderer view has an unexpected JSON artifact path.");
  }
  const directory = normalizeArtifactDirectory(
    jsonArtifact.path.slice(0, -suffix.length),
  );
  for (const artifact of value.artifacts) {
    assertPublishedPath(artifact?.path, directory, "Press Kit artifact path");
  }
  for (const asset of value.pressKit.assets) {
    assertPublishedPath(asset?.downloadPath, directory, "Press Kit asset download path");
  }
  return value;
}

function assertProjection(pressKit) {
  assertObject(pressKit, "Press Kit projection");
  if (pressKit.schema !== PRESS_KIT_PROJECTION_SCHEMA) {
    throw new TypeError(
      `Press Kit projection schema must be ${PRESS_KIT_PROJECTION_SCHEMA}.`,
    );
  }
  assertObject(pressKit.project, "Press Kit project");
  assertObject(pressKit.source, "Press Kit source");
  if (!/^[0-9a-f]{64}$/u.test(pressKit.source.digest || "")) {
    throw new TypeError("Press Kit projection must declare a SHA-256 source digest.");
  }
  if (pressKit.source.sourceSchema !== "identity.press-kit-source/v1") {
    throw new TypeError(
      "Press Kit projection must identify the reviewed Press Kit source schema.",
    );
  }
  for (const [value, label] of [
    [pressKit.boilerplates, "Press Kit boilerplates"],
    [pressKit.facts, "Press Kit facts"],
    [pressKit.links, "Press Kit links"],
    [pressKit.contacts, "Press Kit contacts"],
    [pressKit.team, "Press Kit team"],
    [pressKit.assets, "Press Kit assets"],
    [pressKit.artifacts, "Press Kit artifacts"],
  ]) {
    if (!Array.isArray(value)) {
      throw new TypeError(`${label} must be an array.`);
    }
  }
  const kinds = new Set(pressKit.boilerplates.map((value) => value?.kind));
  if (!kinds.has("short") || !kinds.has("long")) {
    throw new TypeError("Press Kit projection must include short and long boilerplates.");
  }
}

function normalizeArtifactDirectory(value) {
  if (typeof value !== "string" || value.length === 0) {
    throw new TypeError("Press Kit artifact directory must be a non-empty relative path.");
  }
  if (/^(?:\/|https?:\/\/)/u.test(value) || value.includes("..")) {
    throw new TypeError("Press Kit artifact directory must stay within the published site.");
  }
  return value.endsWith("/") ? value : `${value}/`;
}

function normalizeRelativePath(value, label) {
  if (
    typeof value !== "string" ||
    value.length === 0 ||
    /^(?:\/|https?:\/\/)/u.test(value) ||
    value.includes("..") ||
    value.includes("\\")
  ) {
    throw new TypeError(`${label} must stay within the published Press Kit directory.`);
  }
  return value.replace(/^\.\/+/u, "");
}

function assertPublishedPath(value, directory, label) {
  if (typeof value !== "string" || !value.startsWith(directory)) {
    throw new TypeError(`${label} must stay within the published Press Kit directory.`);
  }
  normalizeRelativePath(value.slice(directory.length), label);
}

function assertObject(value, label) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new TypeError(`${label} must be an object.`);
  }
}
