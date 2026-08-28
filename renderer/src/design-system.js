// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

export const DESIGN_SYSTEM_HANDBOOK_SCHEMA =
  "identity.design-system-handbook/v1";
export const DESIGN_CONTEXT_SCHEMA = "identity.design-context/v1";

const ARTIFACTS = Object.freeze([
  [
    "handbook-json",
    "Design-system handbook (JSON)",
    "design-system-handbook.json",
    "application/json",
  ],
  [
    "handbook-markdown",
    "Design-system handbook (Markdown)",
    "design-system-handbook.md",
    "text/markdown",
  ],
  ["context-json", "AI design context (JSON)", "design-context.json", "application/json"],
  ["context-markdown", "AI design context (Markdown)", "design-context.md", "text/markdown"],
]);

/**
 * Validate generated Identity projections and adapt them for the public renderer.
 *
 * The renderer receives the reviewed projections as immutable inputs. It neither
 * recreates source facts nor infers missing design guidance.
 */
export function createDesignSystemView({ handbook, context, artifactDirectory }) {
  assertObject(handbook, "Design-system handbook");
  assertObject(context, "AI design context");
  if (handbook.schema !== DESIGN_SYSTEM_HANDBOOK_SCHEMA) {
    throw new TypeError(
      `Design-system handbook schema must be ${DESIGN_SYSTEM_HANDBOOK_SCHEMA}.`,
    );
  }
  if (context.schema !== DESIGN_CONTEXT_SCHEMA) {
    throw new TypeError(
      `AI design context schema must be ${DESIGN_CONTEXT_SCHEMA}.`,
    );
  }
  assertObject(handbook.project, "Design-system handbook project");
  assertObject(context.project, "AI design context project");
  assertObject(context.source, "AI design context source");
  if (handbook.project.id !== context.project.id) {
    throw new TypeError(
      "Design-system handbook and AI context must declare the same project.",
    );
  }
  if (handbook.project.displayName !== context.project.displayName) {
    throw new TypeError(
      "Design-system handbook and AI context must declare the same display name.",
    );
  }
  if (context.source.handbookSchema !== handbook.schema) {
    throw new TypeError(
      "AI design context must declare the handbook schema it was projected from.",
    );
  }
  if (!/^[0-9a-f]{64}$/u.test(context.source.digest || "")) {
    throw new TypeError("AI design context must declare a SHA-256 source digest.");
  }
  for (const [value, label] of [
    [handbook.sections, "Design-system handbook sections"],
    [handbook.capabilities, "Design-system handbook capabilities"],
    [context.tokens, "AI design context tokens"],
  ]) {
    if (!Array.isArray(value)) {
      throw new TypeError(`${label} must be an array.`);
    }
  }

  const directory = normalizeArtifactDirectory(artifactDirectory);
  return {
    handbook,
    context,
    artifacts: ARTIFACTS.map(([id, label, fileName, mediaType]) => ({
      id,
      label,
      path: `${directory}${fileName}`,
      mediaType,
    })),
  };
}

export function assertDesignSystemView(value) {
  assertObject(value, "Design-system renderer view");
  return createDesignSystemView({
    handbook: value.handbook,
    context: value.context,
    artifactDirectory: artifactDirectoryFromView(value),
  });
}

function artifactDirectoryFromView(value) {
  if (!Array.isArray(value.artifacts) || value.artifacts.length !== ARTIFACTS.length) {
    throw new TypeError("Design-system renderer view must declare all four artifacts.");
  }
  const first = value.artifacts[0];
  if (!first || typeof first.path !== "string") {
    throw new TypeError("Design-system renderer view artifact paths must be strings.");
  }
  const suffix = "design-system-handbook.json";
  if (!first.path.endsWith(suffix)) {
    throw new TypeError("Design-system renderer view has an unexpected handbook artifact path.");
  }
  return first.path.slice(0, -suffix.length);
}

function normalizeArtifactDirectory(value) {
  if (typeof value !== "string" || value.length === 0) {
    throw new TypeError("Design-system artifact directory must be a non-empty relative path.");
  }
  if (/^(?:\/|https?:\/\/)/u.test(value) || value.includes("..")) {
    throw new TypeError("Design-system artifact directory must stay within the published site.");
  }
  return value.endsWith("/") ? value : `${value}/`;
}

function assertObject(value, label) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new TypeError(`${label} must be an object.`);
  }
}
