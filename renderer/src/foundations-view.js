// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import React from "react";

import { colorValueToCss, tokenValueToText } from "./model.js";
import { declaredColorPairs, fontLicenseUrl, typographyPreviewStyle } from "./foundations.js";

const h = React.createElement;

export function ColorFoundations({ tokens, CopyControl, DefinitionList }) {
  const colors = tokens.filter((token) => token.type === "color");
  const pairs = declaredColorPairs(tokens);
  return h("div", { className: "section-stack", "data-color-foundations": true },
    h("div", { className: "color-grid" }, ...colors.map((token) => {
      const contrast = token.constraints?.contrast;
      const value = colorValueToCss(token.value);
      return h("article", { className: "panel color-card", key: token.path },
        h("div", {
          className: "color-swatch", role: "img",
          style: value ? { backgroundColor: value } : undefined,
          "aria-label": `${token.path}: ${value || "Preview unavailable"}`,
        }),
        h("h3", null, token.path),
        h("p", { className: "token-value" }, tokenValueToText(token)),
        h(CopyControl, { label: token.path, value: tokenValueToText(token) }),
        h(DefinitionList, { entries: [
          ["Role", contrast?.intent || "Not declared"],
          ["Supported pairings", contrast?.pairedWith.length ? contrast.pairedWith.join(", ") : "Not declared"],
          ["Source layer", token.sourceLayer],
        ] }),
      );
    })),
    colors.length ? null : h("p", { className: "empty-state" }, "No color tokens are declared."),
    h("article", { className: "panel" },
      h("h3", null, "Declared color pairings"),
      h("p", null, "Use the listed foreground on its listed background. Unlisted combinations and theme variants are not approved by these results."),
      h("p", { className: "support-note" },
        "Contrast is measured for the displayed opaque sRGB values. Normal text needs 4.5:1 for AA; large text needs 3:1 at 18pt regular or 14pt bold. Source minimums may be stricter. Decisions use the unrounded ratio; displayed ratios are rounded.",
      ),
      h("a", { href: "https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html" }, "WCAG contrast guidance"),
    ),
    pairs.length ? pairs.map((pair) => h(ColorPair, {
      key: JSON.stringify([pair.foregroundPath, pair.backgroundPath]), pair, DefinitionList,
    })) : h("div", { className: "empty-state", role: "note" },
      h("h3", null, "Approved pairings not declared"),
      h("p", null, "Color values alone do not establish supported foreground/background or light/dark combinations."),
    ),
  );
}

function ColorPair({ pair, DefinitionList }) {
  const measured = pair.ratio !== null;
  return h("article", { className: "panel", "data-color-pair": JSON.stringify([pair.foregroundPath, pair.backgroundPath]) },
    h("h4", null, `${pair.foregroundPath} on ${pair.backgroundPath}`),
    h(DefinitionList, { entries: [
      ["Contrast ratio", measured ? `${pair.ratio.toFixed(2)}:1` : "Not measured"],
      ["Declared minimum", `${pair.minimumRatio}:1`],
      ["Source requirement", measured ? pair.ratio >= pair.minimumRatio ? "Meets declared minimum" : "Below declared minimum" : "Not measured"],
      ["Normal text (AA)", measured ? pair.ratio >= 4.5 ? "Meets 4.5:1" : "Below 4.5:1" : "Not measured"],
      ["Large text (AA)", measured ? pair.ratio >= 3 ? "Meets 3:1" : "Below 3:1" : "Not measured"],
    ] }),
    pair.reason ? h("p", { className: "support-note" }, pair.reason)
      : pair.ratio >= 3 ? h(React.Fragment, null,
        h("p", {
          className: "foundation-pair-sample",
          style: {
            color: colorValueToCss(pair.foreground.value),
            backgroundColor: colorValueToCss(pair.background.value),
            fontSize: pair.ratio >= 4.5 ? "16px" : "24px", fontWeight: 400,
          },
        }, "Readable text in this declared pairing."),
        h("p", { className: "support-note" }, "Contrast example only; its sample size does not define a brand type scale. Review actual text, states and placement in the consuming product."),
      ) : h("p", { className: "support-note" }, "Text preview omitted: this pairing does not meet AA large-text contrast."),
  );
}

export function TypographyFoundations({ tokens, CopyControl, DefinitionList, projectLinksAvailable }) {
  const typography = tokens.filter((token) =>
    ["fontFamily", "fontWeight", "typography"].includes(token.type) || token.path.startsWith("typography."),
  );
  const composites = typography.filter((token) => token.type === "typography");
  const hasConcreteHierarchy = composites.some((token) => {
    const style = typographyPreviewStyle(token);
    return ["fontFamily", "fontWeight", "fontSize", "lineHeight"].every((field) => style[field] !== undefined);
  });
  return h("div", { className: "section-stack", "data-typography-foundations": true },
    h("article", { className: "panel" },
      h("h3", null, "Font availability and fallbacks"),
      h("p", null, "These previews use fonts available on your device and do not fetch font files. Preserve the declared family order; if a family is unavailable, the browser uses the next available fallback."),
      h("p", { className: "support-note" }, "Font download locations are not declared by this token contract. Obtain approved font files and review their terms before bundling; a declared license identifier does not establish redistribution approval."),
      projectLinksAvailable ? h("a", { href: "#press-kit" }, "Project-provided links and contact") : null,
    ),
    h("div", { className: "typography-stack" }, ...typography.map((token) => {
      const constraints = token.constraints?.typography;
      const style = typographyPreviewStyle(token);
      const copyValue = token.type === "fontFamily" && style.fontFamily ? style.fontFamily : tokenValueToText(token);
      const licenseUrl = fontLicenseUrl(constraints?.license);
      const composite = token.type === "typography" && token.value && typeof token.value === "object" ? token.value : null;
      const complete = composite && ["fontFamily", "fontWeight", "fontSize", "lineHeight"].every((field) => style[field] !== undefined);
      return h("article", { className: "panel typography-sample", key: token.path, "data-type-token": token.path },
        h("h3", null, token.path),
        Object.keys(style).length ? h("p", { className: "foundation-type-sample", style }, "Clarity makes a system easier to trust.") : null,
        token.type === "typography" && !complete
          ? h("p", { className: "support-note" }, "Partial or unavailable preview: unsupported values remain visible below and no missing family, weight, size or line height is inferred.") : null,
        h("p", { className: "token-value" }, copyValue),
        h(CopyControl, { label: token.path, value: copyValue }),
        h(DefinitionList, { entries: [
          ["Token type", token.type],
          ["Family / fallback order", token.type === "fontFamily" ? displayValue(token.value) : displayValue(composite?.fontFamily)],
          ["Weight", token.type === "fontWeight" ? displayValue(token.value) : displayValue(composite?.fontWeight)],
          ["Size", displayValue(composite?.fontSize)],
          ["Line height", displayValue(composite?.lineHeight)],
          ["Font license", constraints?.license || "Not declared"],
          ["Language coverage", constraints?.languages.join(", ") || "Not declared"],
          ["Legibility guidance", constraints?.legibility || "Not declared"],
          ["Source layer", token.sourceLayer],
        ] }),
        licenseUrl ? h("a", { href: licenseUrl }, "Declared font license reference") : null,
      );
    })),
    hasConcreteHierarchy ? null
      : h("div", { className: "empty-state", role: "note" },
        h("h3", null, composites.length ? "Type hierarchy preview unavailable" : "Type hierarchy not declared"),
        h("p", null, composites.length
          ? "The supplied composite values do not provide a complete supported preview. Unresolved aliases or unsupported values remain visible as supplied."
          : "The supplied tokens do not declare a composite type hierarchy. Sizes, weights and line heights are not assigned to families by guessing from token names."),
      ),
    typography.length ? null : h("p", { className: "empty-state" }, "Typography not declared."),
  );
}

function displayValue(value) {
  if (value === undefined || value === null) return "Not declared";
  if (Array.isArray(value)) return value.join(" → ");
  if (typeof value === "object") {
    return Object.hasOwn(value, "value") && Object.hasOwn(value, "unit")
      ? `${value.value}${value.unit}` : JSON.stringify(value);
  }
  return String(value);
}
