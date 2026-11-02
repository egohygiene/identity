// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import fs from "node:fs";

import { JSDOM } from "jsdom";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, test } from "vitest";

import { BrandKitPage } from "../src/app.js";
import { createDesignSystemView } from "../src/design-system.js";
import { assertBrandKitViewModel } from "../src/model.js";
import {
  contrastRatio, declaredColorPairs, fontLicenseUrl, fontStackToCss,
  foundationTokens, typographyPreviewStyle,
} from "../src/foundations.js";

function boundModel() {
  const read = (file) => JSON.parse(fs.readFileSync(new URL(file, import.meta.url), "utf8"));
  const handbook = read("../../tests/fixtures/v1/valid/minimal/expected/design-system-handbook.json");
  const context = read("../../tests/fixtures/v1/valid/minimal/expected/design-context.json");
  const model = read("../fixtures/example.brand-kit.view-model.json");
  model.tokens = structuredClone(context.tokens);
  model.release.sourceDigest = handbook.source.digest;
  model.release.immutableId = `sha256:${handbook.source.digest}`;
  model.designSystem = createDesignSystemView({ handbook, context, artifactDirectory: "design-system" });
  return model;
}

function documentFor(model) {
  return new JSDOM(renderToStaticMarkup(React.createElement(BrandKitPage, { model }))).window.document;
}

function color(red, green = red, blue = red, alpha = 1) {
  return { colorSpace: "srgb", components: [red, green, blue], alpha };
}

function appendToken(model, token, constraints = {}) {
  model.tokens.push(structuredClone(token));
  model.designSystem.context.tokens.push(structuredClone(token));
  model.designSystem.handbook.sections.at(-1).entries.push({
    id: `token:${token.path}`, kind: "token", status: "declared",
    content: { ...structuredClone(token), constraints },
    rationale: "Synthetic reviewed token fixture.", sourceLayer: token.sourceLayer,
  });
}

describe("source-bound color and typography foundations", () => {
  test("renders the real projected pair, roles, license, language and fallback order without changing inputs", () => {
    const model = boundModel();
    const before = structuredClone(model);
    const document = documentFor(model);
    const colors = document.querySelector("#colors");
    expect(colors.textContent).toContain("foreground");
    expect(colors.textContent).toContain("decorative");
    expect(colors.querySelectorAll("[data-color-pair]")).toHaveLength(1);
    expect(colors.textContent).toContain("18.34:1");
    expect(colors.textContent).toContain("Meets declared minimum");
    expect(colors.querySelector(".foundation-pair-sample").style.backgroundColor).toBe("rgb(250, 250, 255)");
    expect(colors.querySelector(".foundation-pair-sample").style.color).toBe("rgb(13, 15, 26)");
    const type = document.querySelector("#typography");
    expect(type.textContent).toContain("Inter → system-ui → sans-serif");
    expect(type.textContent).toContain("OFL-1.1");
    expect(type.textContent).toContain("Prefer open counters and a minimum 16px body size.");
    expect(type.textContent).toContain("Type hierarchy not declared");
    expect(type.textContent).toContain("do not fetch font files");
    expect(type.querySelector("a[href='https://spdx.org/licenses/OFL-1.1.html']")).not.toBeNull();
    expect([...type.querySelectorAll("[data-copy-value]")].map((entry) => entry.dataset.copyValue))
      .toContain("\"Inter\", system-ui, sans-serif");
    expect(type.querySelector("link[rel='stylesheet'], style")).toBeNull();
    expect(model).toEqual(before);
  });

  test.each([
    ["displayed color", (model) => { model.tokens[0].value = color(0); }],
    ["context value", (model) => { model.designSystem.context.tokens[0].value = color(0); }],
    ["handbook value", (model) => { foundationTokens(model.designSystem)[0].value = color(0); }],
    ["source layer", (model) => { model.tokens[0].sourceLayer = "other-layer"; }],
    ["type", (model) => { model.tokens[0].type = "number"; }],
    ["override approval", (model) => { model.tokens[0].approval = "other-approval"; }],
    ["missing token", (model) => { model.tokens.pop(); }],
    ["duplicate token", (model) => { model.tokens.push(structuredClone(model.tokens[0])); }],
  ])("rejects mismatched %s even with unchanged digest fields", (_label, mutate) => {
    const model = boundModel();
    mutate(model);
    expect(() => assertBrandKitViewModel(model)).toThrow(/token.*(match|identit)|inventor/iu);
  });

  test("ignores JSON object-key order while preserving semantic token equality", () => {
    const model = boundModel();
    model.tokens[0].value = Object.fromEntries(Object.entries(model.tokens[0].value).reverse());
    expect(assertBrandKitViewModel(model)).toBe(model);
  });

  test("does not infer pairings, hierarchy or a font license when optional constraints are missing", () => {
    const model = boundModel();
    for (const token of foundationTokens(model.designSystem)) delete token.constraints;
    const document = documentFor(model);
    expect(document.querySelectorAll("[data-color-pair]")).toHaveLength(0);
    expect(document.querySelector("#colors").textContent).toContain("Approved pairings not declared");
    expect(document.querySelector("#typography").textContent).toContain("Not declared");
    expect(document.querySelector("#typography").textContent).not.toContain("OFL-1.1");
  });

  test("uses explicit composite type values without assigning neighboring size or weight tokens", () => {
    const model = boundModel();
    const token = {
      path: "typography.heading", type: "typography", sourceLayer: "example-organization",
      value: { fontFamily: ["Example Heading", "serif"], fontWeight: 700,
        fontSize: { value: 2, unit: "rem" }, lineHeight: 1.2 },
    };
    appendToken(model, token, { typography: {
      license: "https://example.test/approved-font-terms", languages: ["en", "ja"],
      legibility: "Use the supplied heading size.",
    } });
    const document = documentFor(model);
    const heading = document.querySelector("[data-type-token='typography.heading']");
    const sample = heading.querySelector(".foundation-type-sample");
    expect(sample.style.fontSize).toBe("2rem");
    expect(sample.style.fontWeight).toBe("700");
    expect(sample.style.lineHeight).toBe("1.2");
    expect(heading.textContent).toContain("en, ja");
    expect(heading.querySelector("a").href).toBe("https://example.test/approved-font-terms");
    expect(document.querySelector("[data-type-token='typography.body.family'] .foundation-type-sample").style.fontWeight).toBe("");
  });

  test("retains the standalone legacy preview without inventing handbook constraints", () => {
    const model = boundModel();
    delete model.designSystem;
    const document = documentFor(model);
    expect(document.querySelector("[data-color-foundations]")).toBeNull();
    expect(document.querySelector("#colors").textContent).toContain("Approved pairings not declared");
  });
});

describe("declared contrast measurement", () => {
  test("matches known black/white and 8-bit grey vectors and measures the CSS/export rounding", () => {
    expect(contrastRatio(color(0), color(1))).toBe(21);
    expect(contrastRatio(color(1), color(0))).toBe(21);
    expect(contrastRatio(color(0.5), color(0.5))).toBe(1);
    expect(contrastRatio(color(118 / 255), color(1))).toBeCloseTo(4.542224959605253, 10);
    expect(contrastRatio(color(119 / 255), color(1))).toBeCloseTo(4.478089453577214, 10);
    expect(contrastRatio(color(0.465), color(1))).toBe(contrastRatio(color(119 / 255), color(1)));
  });

  test.each([
    color(0, 0, 0, 0.5), { ...color(0), colorSpace: "display-p3" }, color(-1), color(2),
    { ...color(0), components: [0, 0] }, { ...color(0), components: [NaN, 0, 0] },
  ])("does not fabricate opaque sRGB proof for %j", (value) => {
    expect(contrastRatio(value, color(1))).toBeNull();
  });

  test("deduplicates reciprocal declarations and preserves the stricter declared threshold", () => {
    const tokens = foundationTokens(boundModel().designSystem);
    tokens.find((token) => token.path === "color.canvas").constraints.contrast.minimumRatio = 4.5;
    const pairs = declaredColorPairs(tokens);
    expect(pairs).toHaveLength(1);
    expect(pairs[0].minimumRatio).toBe(7);
    expect(pairs[0].foregroundPath).toBe("color.text");
    expect(pairs[0].backgroundPath).toBe("color.canvas");
  });

  test("keeps missing, conflicting and translucent pairs explicitly unmeasured", () => {
    for (const mutate of [
      (tokens) => { tokens.find((token) => token.path === "color.text").value.alpha = 0.5; },
      (tokens) => { tokens.splice(tokens.findIndex((token) => token.path === "color.text"), 1); },
      (tokens) => { tokens.find((token) => token.path === "color.text").constraints.contrast.intent = "decorative"; },
    ]) {
      const tokens = foundationTokens(boundModel().designSystem);
      mutate(tokens);
      const [pair] = declaredColorPairs(tokens);
      expect(pair.ratio).toBeNull();
      expect(pair.reason).toBeTruthy();
    }
  });

  test("shows failure in text and omits an inaccessible text example", () => {
    const model = boundModel();
    for (const tokens of [model.tokens, model.designSystem.context.tokens, foundationTokens(model.designSystem)]) {
      tokens.find((token) => token.path === "color.text").value = color(0.9);
      tokens.find((token) => token.path === "color.canvas").value = color(1);
    }
    const document = documentFor(model);
    expect(document.querySelector("#colors").textContent).toContain("Below declared minimum");
    expect(document.querySelector("#colors").textContent).toContain("Below 3:1");
    expect(document.querySelector(".foundation-pair-sample")).toBeNull();
  });

  test("does not promote a displayed 4.50 ratio that is below the unrounded AA threshold", () => {
    const model = boundModel();
    for (const tokens of [model.tokens, model.designSystem.context.tokens, foundationTokens(model.designSystem)]) {
      tokens.find((token) => token.path === "color.text").value = color(100 / 255, 125 / 255, 102 / 255);
      tokens.find((token) => token.path === "color.canvas").value = color(1);
    }
    const document = documentFor(model);
    const pair = document.querySelector("[data-color-pair]");
    expect(pair.textContent).toContain("4.50:1");
    expect(pair.textContent).toContain("Below 4.5:1");
    expect(pair.querySelector(".foundation-pair-sample").style.fontSize).toBe("24px");
  });
});

describe("font preview and reference boundaries", () => {
  test("preserves fallback order and quotes family names containing punctuation", () => {
    expect(fontStackToCss(["Example, Body", "Example \"Display\"", "system-ui", "sans-serif"]))
      .toBe("\"Example, Body\", \"Example \\\"Display\\\"\", system-ui, sans-serif");
    expect(fontStackToCss(["bad\nname"])).toBeNull();
    expect(fontStackToCss([])).toBeNull();
  });

  test("does not apply unresolved composite aliases or infer style from a token name", () => {
    expect(typographyPreviewStyle({ type: "dimension", path: "typography.heading.size", value: { value: 3, unit: "rem" } })).toEqual({});
    expect(typographyPreviewStyle({ type: "typography", value: { fontFamily: "{font.body}", fontSize: "{size.body}" } })).toEqual({});
  });

  test.each(["javascript:alert(1)", "data:text/plain,license", "http://example.test/terms", "https://user:password@example.test/terms", "Proprietary"])(
    "does not turn %s into a license link", (license) => {
      expect(fontLicenseUrl(license)).toBeNull();
    },
  );
});
