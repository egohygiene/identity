// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

export const BRAND_KIT_VIEW_MODEL_SCHEMA = "identity.brand-kit-view-model/v1";

export const SECTION_DEFINITIONS = Object.freeze([
  ["overview", "Overview"],
  ["logos", "Logos and marks"],
  ["colors", "Color palette"],
  ["typography", "Typography"],
  ["voice", "Voice and personality"],
  ["usage", "Usage rules"],
  ["creative-direction", "Motion, imagery, and mascot"],
  ["studio", "Review candidate assets"],
  ["downloads", "Downloads"],
  ["provenance", "Provenance and support"],
]);

export function assertBrandKitViewModel(model) {
  if (!model || typeof model !== "object") {
    throw new TypeError("Brand Kit view model must be an object.");
  }
  if (model.schema !== BRAND_KIT_VIEW_MODEL_SCHEMA) {
    throw new TypeError(
      `Brand Kit view model schema must be ${BRAND_KIT_VIEW_MODEL_SCHEMA}.`,
    );
  }
  if (!model.project || typeof model.project.displayName !== "string") {
    throw new TypeError("Brand Kit view model must declare project metadata.");
  }
  for (const collectionName of ["tokens", "assets", "packages"]) {
    if (!Array.isArray(model[collectionName])) {
      throw new TypeError(
        `Brand Kit view model ${collectionName} must be an array.`,
      );
    }
  }
  if (!model.release || typeof model.release.immutableId !== "string") {
    throw new TypeError("Brand Kit view model must declare an immutable release.");
  }
  if (!model.guidance || !model.support) {
    throw new TypeError(
      "Brand Kit view model must declare guidance and support statuses.",
    );
  }
  return model;
}

export function tokenValueToText(token) {
  if (token.type === "color") {
    return colorValueToCss(token.value) ?? JSON.stringify(token.value);
  }
  if (token.type === "fontFamily" && Array.isArray(token.value)) {
    return token.value.join(", ");
  }
  if (
    token.value &&
    typeof token.value === "object" &&
    "value" in token.value &&
    "unit" in token.value
  ) {
    return `${token.value.value}${token.value.unit}`;
  }
  if (typeof token.value === "string") {
    return token.value;
  }
  return JSON.stringify(token.value);
}

export function colorValueToCss(value) {
  if (
    !value ||
    value.colorSpace !== "srgb" ||
    !Array.isArray(value.components) ||
    value.components.length !== 3
  ) {
    return null;
  }
  const channels = value.components.map((component) =>
    Math.max(0, Math.min(255, Math.round(Number(component) * 255))),
  );
  const alpha = value.alpha === undefined ? 1 : Number(value.alpha);
  if (alpha === 1) {
    return `#${channels
      .map((channel) => channel.toString(16).padStart(2, "0"))
      .join("")}`;
  }
  return `rgba(${channels.join(", ")}, ${alpha})`;
}

export function sourceDataUrl(asset) {
  if (asset.mediaType === "image/svg+xml") {
    return `data:image/svg+xml;charset=utf-8,${encodeURIComponent(asset.text)}`;
  }
  return "";
}

export function joinAssetUrl(assetBaseUrl, relativePath) {
  const normalizedPath = relativePath.replace(/^\/+/, "");
  const normalizedBase = ensureTrailingSlash(assetBaseUrl || "./");

  if (/^https?:\/\//u.test(normalizedBase)) {
    return new URL(normalizedPath, normalizedBase).toString();
  }

  return `${normalizedBase}${normalizedPath}`;
}

export function deriveThemeVariables(model) {
  const values = new Map(
    model.tokens.map((token) => [token.path, tokenValueToText(token)]),
  );
  const variablePairs = [
    ["--brand-primary", values.get("color.brand.primary")],
    ["--brand-secondary", values.get("color.brand.secondary")],
    ["--brand-canvas", values.get("color.canvas")],
    ["--brand-surface", values.get("color.surface")],
    ["--brand-text", values.get("color.text")],
    ["--brand-text-muted", values.get("color.text.muted")],
    ["--brand-border", values.get("color.border")],
    ["--brand-body-font", fontFamilyValue(values.get("typography.body.family"))],
    [
      "--brand-heading-font",
      fontFamilyValue(values.get("typography.heading.family")),
    ],
  ].filter(([, value]) => value);

  return `:root {\n${variablePairs
    .map(([name, value]) => `  ${name}: ${value};`)
    .join("\n")}\n}`;
}

export function statusLabel(status) {
  switch (status) {
    case "declared":
      return "Declared";
    case "unsupported":
      return "Unsupported";
    default:
      return "Not declared";
  }
}

function ensureTrailingSlash(value) {
  return value.endsWith("/") ? value : `${value}/`;
}

function fontFamilyValue(value) {
  if (!value) {
    return null;
  }
  return value
    .split(",")
    .map((family) => {
      const normalized = family.trim();
      return normalized.includes(" ") ? `"${normalized}"` : normalized;
    })
    .join(", ");
}
