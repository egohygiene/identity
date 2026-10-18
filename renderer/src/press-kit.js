// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { normalizeArtifactDirectory, normalizeArtifactPath } from "./artifact-paths.js";

export const PRESS_KIT_PROJECTION_SCHEMA = "identity.press-kit/v1";

/**
 * Validate a generated Press Kit projection and adapt its links for the static
 * public renderer. The renderer receives immutable approved facts only.
 */
export function createPressKitView({ pressKit, artifactDirectory }) {
  assertProjection(pressKit);
  const directory = normalizeArtifactDirectory(artifactDirectory, "Press Kit artifact directory");
  return {
    pressKit: {
      ...pressKit,
      assets: pressKit.assets.map((asset) => ({
        ...asset,
        downloadPath: `${directory}${normalizeArtifactPath(
          asset?.downloadPath,
          "Press Kit asset download path",
        )}`,
      })),
    },
    artifacts: pressKit.artifacts.map((artifact) => ({
      ...artifact,
      path: `${directory}${normalizeArtifactPath(
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
  const jsonArtifactPath = normalizeArtifactPath(jsonArtifact.path, "Press Kit artifact path");
  const suffix = "press-kit.json";
  if (!jsonArtifactPath.endsWith(suffix)) {
    throw new TypeError("Press Kit renderer view has an unexpected JSON artifact path.");
  }
  const directory = normalizeArtifactDirectory(
    jsonArtifactPath.slice(0, -suffix.length),
    "Press Kit artifact directory",
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
  for (const artifact of pressKit.artifacts) {
    normalizeArtifactPath(artifact?.path, "Press Kit projection artifact path");
  }
  const kinds = new Set(pressKit.boilerplates.map((value) => value?.kind));
  if (!kinds.has("short") || !kinds.has("long")) {
    throw new TypeError("Press Kit projection must include short and long boilerplates.");
  }
}

function assertPublishedPath(value, directory, label) {
  const normalized = normalizeArtifactPath(value, label);
  if (!normalized.startsWith(directory)) {
    throw new TypeError(`${label} must stay within the published Press Kit directory.`);
  }
}

function assertObject(value, label) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new TypeError(`${label} must be an object.`);
  }
}
