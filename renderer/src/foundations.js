// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

/** Read existing handbook token entries, never a second token catalog. */
export function foundationTokens(designSystem) {
  return designSystem.handbook.sections.flatMap((section) => section.entries || [])
    .filter((entry) => entry.kind === "token" && entry.status === "declared")
    .map((entry) => entry.content);
}

/** A matching digest alone cannot establish that the displayed values agree. */
export function assertFoundationAgreement(tokens, designSystem) {
  const displayed = tokenMap(tokens, "Displayed");
  const context = tokenMap(designSystem.context.tokens, "Design context");
  const handbook = tokenMap(foundationTokens(designSystem), "Handbook");
  if (displayed.size !== context.size || context.size !== handbook.size) {
    throw new TypeError("Displayed, context and handbook token inventories must match.");
  }
  for (const [path, token] of displayed) {
    for (const projected of [context.get(path), handbook.get(path)]) {
      if (!projected || !equalValue(tokenIdentity(token), tokenIdentity(projected))) {
        throw new TypeError(`Displayed, context and handbook token values must match: ${path}`);
      }
    }
    assertConstraints(handbook.get(path).constraints);
  }
}

function tokenMap(tokens, label) {
  const result = new Map();
  for (const token of tokens) {
    if (!token || typeof token.path !== "string" || !token.path.length
      || typeof token.type !== "string" || !Object.hasOwn(token, "value")
      || typeof token.sourceLayer !== "string" || result.has(token.path)) {
      throw new TypeError(`${label} tokens must have complete, unique identities.`);
    }
    result.set(token.path, token);
  }
  return result;
}

function tokenIdentity(token) {
  return {
    path: token.path, type: token.type, value: token.value,
    sourceLayer: token.sourceLayer,
    overrideReason: token.overrideReason ?? null, approval: token.approval ?? null,
  };
}

function equalValue(left, right) {
  if (left === right) return true;
  if (!left || !right || typeof left !== "object" || typeof right !== "object") return false;
  if (Array.isArray(left) !== Array.isArray(right)) return false;
  const keys = Object.keys(left).sort();
  return keys.length === Object.keys(right).length
    && keys.every((key) => Object.hasOwn(right, key) && equalValue(left[key], right[key]));
}

function assertConstraints(value) {
  if (value === undefined) return;
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new TypeError("Handbook token constraints must be an object.");
  }
  const contrast = value.contrast;
  if (contrast !== undefined && (
    !contrast || !["foreground", "background", "decorative"].includes(contrast.intent)
    || !Array.isArray(contrast.pairedWith)
    || contrast.pairedWith.some((path) => typeof path !== "string" || !path.length)
    || !Number.isFinite(contrast.minimumRatio) || contrast.minimumRatio < 1
    || contrast.minimumRatio > 21
  )) throw new TypeError("Handbook contrast constraints must preserve the declared intent, pairs and minimum.");
  const typography = value.typography;
  if (typography !== undefined && (
    !typography || typeof typography.license !== "string" || !typography.license.length
    || !Array.isArray(typography.languages) || !typography.languages.length
    || typography.languages.some((language) => typeof language !== "string" || !language.length)
    || typeof typography.legibility !== "string" || !typography.legibility.length
  )) throw new TypeError("Handbook typography constraints must preserve license, languages and legibility.");
}

/** Only explicit foreground/background declarations introduce a pair. */
export function declaredColorPairs(tokens) {
  const byPath = new Map(tokens.map((token) => [token.path, token]));
  const pairs = new Map();
  for (const token of tokens.filter((entry) => entry.type === "color")) {
    const constraint = token.constraints?.contrast;
    if (!constraint || constraint.intent === "decorative") continue;
    for (const partner of constraint.pairedWith) {
      const foregroundPath = constraint.intent === "foreground" ? token.path : partner;
      const backgroundPath = constraint.intent === "background" ? token.path : partner;
      const key = JSON.stringify([foregroundPath, backgroundPath]);
      const pair = pairs.get(key) || { foregroundPath, backgroundPath, minimumRatio: 1 };
      pair.minimumRatio = Math.max(pair.minimumRatio, constraint.minimumRatio);
      pairs.set(key, pair);
    }
  }
  return [...pairs.values()].sort((a, b) =>
    a.foregroundPath.localeCompare(b.foregroundPath) || a.backgroundPath.localeCompare(b.backgroundPath),
  ).map((pair) => {
    const foreground = byPath.get(pair.foregroundPath);
    const background = byPath.get(pair.backgroundPath);
    let reason = null;
    if (foreground?.type !== "color" || background?.type !== "color") {
      reason = "A declared pairing refers to a missing color token.";
    } else if (
      ["background", "decorative"].includes(foreground.constraints?.contrast?.intent)
      || ["foreground", "decorative"].includes(background.constraints?.contrast?.intent)
    ) {
      reason = "The declared foreground/background roles conflict.";
    }
    const ratio = reason ? null : contrastRatio(foreground.value, background.value);
    if (!reason && ratio === null) {
      reason = "Contrast requires opaque sRGB colors; no backing color or conversion is assumed.";
    }
    return { ...pair, foreground, background, ratio, reason };
  });
}

/** WCAG 2.2 luminance of the actual rounded 8-bit CSS/export color. */
export function contrastRatio(foreground, background) {
  const left = luminance(foreground);
  const right = luminance(background);
  if (left === null || right === null) return null;
  return (Math.max(left, right) + 0.05) / (Math.min(left, right) + 0.05);
}

function luminance(value) {
  if (!value || value.colorSpace !== "srgb" || (value.alpha ?? 1) !== 1
    || !Array.isArray(value.components) || value.components.length !== 3
    || value.components.some((part) => !Number.isFinite(part) || part < 0 || part > 1)) return null;
  const linear = value.components.map((part) => Math.round(part * 255) / 255)
    .map((part) => part <= 0.04045 ? part / 12.92 : ((part + 0.055) / 1.055) ** 2.4);
  return linear[0] * 0.2126 + linear[1] * 0.7152 + linear[2] * 0.0722;
}

const GENERIC_FAMILIES = new Set([
  "serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui",
  "ui-serif", "ui-sans-serif", "ui-monospace", "ui-rounded", "emoji", "math", "fangsong",
]);

export function fontStackToCss(value) {
  const families = typeof value === "string" ? [value] : value;
  if (!Array.isArray(families) || !families.length || families.some((family) =>
    typeof family !== "string" || !family.trim().length
      || /^[{][^{}]+[}]$/u.test(family) || /[\u0000-\u001f\u007f]/u.test(family),
  )) return null;
  return families.map((family) => GENERIC_FAMILIES.has(family.toLowerCase())
    ? family : `"${family.replaceAll("\\", "\\\\").replaceAll("\"", "\\\"")}"`,
  ).join(", ");
}

export function typographyPreviewStyle(token) {
  if (token.type === "fontFamily") {
    const fontFamily = fontStackToCss(token.value);
    return fontFamily ? { fontFamily } : {};
  }
  const source = token.type === "typography" && token.value && typeof token.value === "object"
    ? token.value : token.type === "fontWeight" ? { fontWeight: token.value } : {};
  const style = {};
  const family = fontStackToCss(source.fontFamily);
  if (family) style.fontFamily = family;
  if ((Number.isFinite(source.fontWeight) && source.fontWeight >= 1 && source.fontWeight <= 1000)
    || ["normal", "bold"].includes(source.fontWeight)) style.fontWeight = source.fontWeight;
  if (source.fontSize && ["px", "rem"].includes(source.fontSize.unit)
    && Number.isFinite(source.fontSize.value) && source.fontSize.value > 0) {
    style.fontSize = `${source.fontSize.value}${source.fontSize.unit}`;
  }
  if (Number.isFinite(source.lineHeight) && source.lineHeight > 0) style.lineHeight = source.lineHeight;
  return style;
}

/** A supplied license identifier/URL is information, not redistribution approval. */
export function fontLicenseUrl(license) {
  if (license === "OFL-1.1") return "https://spdx.org/licenses/OFL-1.1.html";
  try {
    const url = new URL(license);
    return url.protocol === "https:" && !url.username && !url.password ? url.href : null;
  } catch {
    return null;
  }
}
