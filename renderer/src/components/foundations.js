// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import React from "react";

import { ColorFoundations, TypographyFoundations } from "../foundations-view.js";
import { colorValueToCss, tokenValueToText } from "../model.js";
import { Section, DefinitionList, CopyControl, EmptyState } from "./shared.js";

const h = React.createElement;

export function ColorSection({ tokens, foundations }) {
  if (foundations) return h(Section,
    { id: "colors", title: "Color palette and approved pairings", preview: true },
    h(ColorFoundations, { tokens: foundations, CopyControl, DefinitionList }),
  );
  return h(
    Section,
    { id: "colors", title: "Color palette and approved pairings", preview: true },
    tokens.length === 0
      ? h(EmptyState, {
          title: "No color tokens",
          message:
            "The current release does not declare color tokens that the renderer can preview.",
        })
      : h(
          "div",
          { className: "section-stack" },
          h(
            "div",
            { className: "color-grid" },
            ...tokens.map((token) => {
              const cssValue = colorValueToCss(token.value);
              return h(
                "article",
                { className: "panel color-card", key: token.path },
                h("div", {
                  className: "color-swatch",
                  role: "img",
                  style: cssValue ? { backgroundColor: cssValue } : undefined,
                  "aria-label": cssValue
                    ? `${token.path} previewed as ${cssValue}`
                    : `${token.path} cannot be previewed`,
                }),
                h("h3", null, token.path),
                h("p", { className: "token-value" }, tokenValueToText(token)),
                h(CopyControl, {
                  label: token.path,
                  value: tokenValueToText(token),
                }),
                h(
                  "p",
                  { className: "support-note" },
                  `Source layer: ${token.sourceLayer}`,
                ),
              );
            }),
          ),
          h(EmptyState, {
            title: "Approved pairings not declared",
            message:
              "Semantic colors are previewed individually, but the current release does not declare canonical color pairings. The renderer does not infer combinations.",
          }),
        ),
  );
}

export function TypographySection({ tokens, foundations, projectLinksAvailable }) {
  if (foundations) return h(Section,
    { id: "typography", title: "Typography and type scale", preview: true },
    h(TypographyFoundations, { tokens: foundations, CopyControl, DefinitionList, projectLinksAvailable }),
  );
  const hasTypeScale = tokens.some((token) =>
    [".size", ".lineHeight", ".line-height", ".weight", ".scale"].some(
      (fragment) => token.path.includes(fragment),
    ),
  );

  return h(
    Section,
    { id: "typography", title: "Typography and type scale", preview: true },
    tokens.length === 0
      ? h(EmptyState, {
          title: "Typography not declared",
          message:
            "The current release does not contain typography tokens. System defaults remain in effect.",
        })
      : h(
          "div",
          { className: "section-stack" },
          h(
            "div",
            { className: "typography-stack" },
            ...tokens.map((token) =>
              h(
                "article",
                { className: "panel typography-sample", key: token.path },
                h("p", { className: "eyebrow" }, token.path),
                h(
                  "p",
                  {
                    className: "type-preview",
                    style:
                      token.type === "fontFamily" && Array.isArray(token.value)
                        ? { fontFamily: token.value.join(", ") }
                        : undefined,
                  },
                  "Clarity makes a system easier to trust.",
                ),
                h("p", { className: "token-value" }, tokenValueToText(token)),
                h(CopyControl, {
                  label: token.path,
                  value: tokenValueToText(token),
                }),
              ),
            ),
          ),
          hasTypeScale
            ? null
            : h(EmptyState, {
                title: "Type scale not declared",
                message:
                  "Font family tokens are available, but the current release does not declare canonical sizes, weights, or line-height relationships.",
              }),
        ),
  );
}
