// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import axe from "axe-core";
import { JSDOM } from "jsdom";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, test } from "vitest";

import { BrandKitPage } from "../src/app.js";
import {
  SECTION_DEFINITIONS,
  assertBrandKitViewModel,
} from "../src/model.js";

const testDirectory = path.dirname(fileURLToPath(import.meta.url));
const rendererRoot = path.resolve(testDirectory, "..");
const fixture = assertBrandKitViewModel(
  JSON.parse(
    fs.readFileSync(
      path.join(rendererRoot, "fixtures/example.brand-kit.view-model.json"),
      "utf8",
    ),
  ),
);

describe("BrandKitPage", () => {
  test("renders every required section from the immutable fixture", () => {
    const document = renderDocument(fixture);
    const sections = [...document.querySelectorAll("main > section")].map(
      (section) => ({
        id: section.id,
        heading: section.querySelector("h2")?.textContent,
      }),
    );

    expect(sections.map(({ id }) => id)).toEqual(
      SECTION_DEFINITIONS.filter(([id]) => id !== "design-system").map(
        ([id]) => id,
      ),
    );
    expect(sections.map(({ heading }) => heading)).toEqual([
      "Overview and version",
      "Logo and marks",
      "Color palette and approved pairings",
      "Typography and type scale",
      "Voice and personality",
      "Usage rules",
      "Motion, imagery, and mascot guidance",
      "Review candidate assets",
      "Downloads and package installation",
      "Provenance, licenses, changelog, and support",
    ]);
    expect(document.querySelector("h1")?.textContent).toBe("Example Product");
    expect(document.body.textContent).not.toContain("Ego Hygiene");
  });

  test("distinguishes canonical guidance from generated previews", () => {
    const document = renderDocument(fixture);
    const badges = [...document.querySelectorAll(".authority-badge")].map(
      (badge) => badge.textContent,
    );

    expect(badges.filter((label) => label === "Canonical guidance")).toHaveLength(
      2,
    );
    expect(badges.filter((label) => label === "Generated preview")).toHaveLength(
      3,
    );
  });

  test("keeps missing data explicit instead of inventing guidance", () => {
    const incomplete = structuredClone(fixture);
    incomplete.assets = [];
    incomplete.tokens = incomplete.tokens.filter(
      (token) => !token.path.startsWith("typography."),
    );
    incomplete.guidance.voice = {
      status: "not-declared",
      canonical: true,
    };
    incomplete.guidance.usage = {
      status: "not-declared",
      canonical: true,
    };

    const document = renderDocument(incomplete);
    const text = document.body.textContent;

    expect(text).toContain("No approved marks");
    expect(text).toContain("Approved pairings not declared");
    expect(text).toContain("Typography not declared");
    expect(text).toContain("Voice and personality not declared");
    expect(text).toContain("Usage rules not declared");
    expect(text).toContain("The renderer does not infer or invent it.");
  });

  test("exposes governed asset metadata, copy controls, and immutable downloads", () => {
    const document = renderDocument(fixture);
    const copyControls = [...document.querySelectorAll("[data-copy-value]")];
    const downloads = [...document.querySelectorAll("a[download]")];
    const logoSectionText = document.querySelector("#logos")?.textContent || "";

    expect(logoSectionText).toContain("64 × 64 SVG viewBox units");
    expect(logoSectionText).toContain(
      "Primary scalable brand mark for approved product surfaces.",
    );
    expect(copyControls.length).toBeGreaterThan(0);
    expect(
      copyControls.every(
        (control) => control.getAttribute("aria-describedby") === "copy-status",
      ),
    ).toBe(true);
    expect(downloads.length).toBeGreaterThanOrEqual(5);
    expect(
      downloads.every((link) => {
        const href = link.getAttribute("href");
        return Boolean(href && href !== "#" && !href.includes("undefined"));
      }),
    ).toBe(true);
  });

  test("passes automated accessibility checks for the static document", async () => {
    const markup = renderToStaticMarkup(
      React.createElement(BrandKitPage, {
        model: fixture,
        assetBaseUrl: "./",
      }),
    );
    const dom = new JSDOM(
      `<!doctype html><html lang="en"><head><title>Example Product Brand Kit</title></head><body>${markup}</body></html>`,
      {
        runScripts: "outside-only",
        url: "https://identity.invalid/",
      },
    );
    dom.window.eval(axe.source);
    const results = await dom.window.axe.run(dom.window.document, {
      rules: {
        "color-contrast": { enabled: false },
      },
    });

    expect(results.violations).toEqual([]);
  });

  test("preserves the visual section hierarchy as a regression contract", () => {
    const document = renderDocument(fixture);
    const visualContract = {
      hero: {
        eyebrow: document.querySelector(".hero .eyebrow")?.textContent,
        title: document.querySelector(".hero h1")?.textContent,
        actions: document.querySelectorAll(".hero__actions .button").length,
      },
      sections: [...document.querySelectorAll("main > section")].map(
        (section) => ({
          id: section.id,
          panels: section.querySelectorAll(".panel").length,
          emptyStates: section.querySelectorAll(".empty-state").length,
        }),
      ),
      downloads: document.querySelectorAll("a[download]").length,
    };

    expect(visualContract).toEqual({
      hero: {
        eyebrow: "Public Brand Kit",
        title: "Example Product",
        actions: 2,
      },
      sections: [
        { id: "overview", panels: 2, emptyStates: 0 },
        { id: "logos", panels: 1, emptyStates: 0 },
        { id: "colors", panels: 7, emptyStates: 1 },
        { id: "typography", panels: 2, emptyStates: 1 },
        { id: "voice", panels: 3, emptyStates: 0 },
        { id: "usage", panels: 2, emptyStates: 0 },
        { id: "creative-direction", panels: 3, emptyStates: 0 },
        { id: "studio", panels: 1, emptyStates: 0 },
        { id: "downloads", panels: 0, emptyStates: 0 },
        { id: "provenance", panels: 3, emptyStates: 0 },
      ],
      downloads: 6,
    });
  });
});

describe("renderer stylesheet contract", () => {
  test("contains responsive, theme, focus, print, and reduced-motion policies", () => {
    const stylesheet = fs.readFileSync(
      path.join(rendererRoot, "src/styles.css"),
      "utf8",
    );
    const sectionStates = fs.readFileSync(
      path.join(rendererRoot, "src/section-states.css"),
      "utf8",
    );

    for (const requiredPolicy of [
      "@media (prefers-color-scheme: dark)",
      "@media (prefers-reduced-motion: reduce)",
      "@media (max-width: 56rem)",
      "@media (max-width: 40rem)",
      "@media print",
      ":focus-visible",
      "[data-theme=\"dark\"]",
    ]) {
      expect(stylesheet).toContain(requiredPolicy);
    }
    expect(sectionStates).toContain(".section-stack");
  });
});

function renderDocument(model) {
  const markup = renderToStaticMarkup(
    React.createElement(BrandKitPage, {
      model,
      assetBaseUrl: "./",
    }),
  );
  return new JSDOM(
    `<!doctype html><html lang="en"><head><title>Example Product Brand Kit</title></head><body>${markup}</body></html>`,
    {
      url: "https://identity.invalid/",
    },
  ).window.document;
}
