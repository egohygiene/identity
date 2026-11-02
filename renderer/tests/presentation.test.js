// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import fs from "node:fs";

import { JSDOM } from "jsdom";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, test } from "vitest";

import { BrandKitPage } from "../src/app.js";
import { createPressKitView } from "../src/press-kit.js";
import { presentationCopy, selectedPresentationProfiles } from "../src/presentation.js";

function modelFor(profiles = ["github"]) {
  const model = JSON.parse(fs.readFileSync(new URL("../fixtures/example.brand-kit.view-model.json", import.meta.url), "utf8"));
  const source = model.assets[0];
  model.downloads = profiles.map((profile) => ({
    id: profile === "github" ? "github-social-preview" : "social-card-1200x630",
    profile, label: "Selected preview", path: `${profile}/selected.png`, mediaType: "image/png",
    sourceAssetId: source.id, sourceSha256: source.sha256,
    dimensions: profile === "github" ? "1280 × 640 pixels" : "1200 × 630 pixels",
  }));
  return model;
}

function documentFor(model, assetBaseUrl = "/project/v1/") {
  return new JSDOM(renderToStaticMarkup(React.createElement(BrandKitPage, { model, assetBaseUrl }))).window.document;
}

describe("selected presentation profiles", () => {
  test.each([
    { profiles: [] }, { profiles: ["github"] }, { profiles: ["social"] },
    { profiles: ["github", "social"] },
  ])("shows only the selected profiles $profiles", ({ profiles }) => {
    const model = modelFor(profiles);
    const before = structuredClone(model);
    const document = documentFor(model);
    expect([...document.querySelectorAll("[data-presentation-profile]")].map((entry) => entry.dataset.presentationProfile))
      .toEqual(profiles);
    expect(Boolean(document.querySelector("nav a[href='#presentation']"))).toBe(profiles.length > 0);
    expect(model).toEqual(before);
  });

  test("uses the supplied download path, dimensions, alt text and source rights under a deployment base", () => {
    const model = modelFor();
    model.assets[0].usage = { safeZone: "Keep the supplied clear space.", minimumSize: "24 pixels.", restrictions: ["Do not recolor."] };
    const section = documentFor(model).querySelector("#presentation");
    expect(section.querySelector("img").getAttribute("src")).toBe("/project/v1/github/selected.png");
    expect(section.querySelector("img").getAttribute("alt")).toBe(model.assets[0].altText);
    expect(section.querySelector("a[download]").getAttribute("href")).toBe("/project/v1/github/selected.png");
    expect(section.textContent).toContain(model.downloads[0].dimensions);
    expect(section.textContent).toContain("Do not recolor.");
    expect(section.textContent).toContain(model.assets[0].sha256);
    expect(section.querySelector("a[href^='https://docs.github.com/']")).not.toBeNull();
  });

  test("renders the exact real-consumer handoff whose PNG and model match the retained receipt", () => {
    const root = new URL("../fixtures/mantle-presentation/", import.meta.url);
    const receipt = JSON.parse(fs.readFileSync(new URL("../../docs/evidence/identity-presentation-mantle-2026-10-21.json", import.meta.url), "utf8"));
    for (const entry of receipt.generatedFixtures) {
      const bytes = fs.readFileSync(new URL(`../../${entry.path}`, import.meta.url));
      expect(createHash("sha256").update(bytes).digest("hex")).toBe(entry.sha256);
      expect(bytes.length).toBe(entry.bytes);
    }
    const model = JSON.parse(fs.readFileSync(new URL("brand-kit.view-model.json", root), "utf8"));
    const section = documentFor(model).querySelector("#presentation");
    expect(section.querySelectorAll("[data-presentation-profile]")).toHaveLength(1);
    expect(section.querySelector("a[download]").getAttribute("href")).toBe("/project/v1/github/social-preview.png");
    expect(section.querySelector("[data-copy-label='Project tagline']").dataset.copyValue).toBe(model.project.tagline);
    expect(section.textContent).toContain("Copyright 2026 Ego Hygiene");
    expect(section.textContent).toContain("Do not stretch, rotate, remove layers, or recolor outside approved tokens.");
    expect(section.textContent).toContain("not declared for this kit");
    expect(section.textContent).not.toContain("crates.io");
  });

  test("does not turn an unknown target or unrelated profile into a platform promise", () => {
    const model = modelFor();
    model.downloads[0].id = "unreviewed-instagram-target";
    expect(selectedPresentationProfiles(model)).toEqual([]);
    model.downloads[0].id = "github-social-preview";
    model.downloads[0].profile = "other";
    expect(documentFor(model).querySelector("#presentation")).toBeNull();
    expect(documentFor(modelFor(["social"])).querySelector("#presentation").textContent)
      .toContain("does not declare support for a particular social platform");
  });

  test("reuses generated approved descriptions without inferring package identifiers, keywords or accounts", () => {
    const model = modelFor();
    expect(presentationCopy(model).map((entry) => entry.value))
      .toEqual([model.project.displayName, model.project.tagline, model.project.repository]);
    const projection = JSON.parse(execFileSync("python3", [
      new URL("../../scripts/render_press_kit.py", import.meta.url).pathname,
      "--repository-root", new URL("../../examples/v1/expanded", import.meta.url).pathname,
      "--format", "json",
    ], { encoding: "utf8" }));
    model.projectId = projection.project.id;
    for (const field of ["displayName", "repository", "tagline", "kind"]) {
      model.project[field] = projection.project[field];
    }
    model.release.sourceDigest = projection.source.digest;
    model.release.immutableId = `sha256:${projection.source.digest}`;
    // Synthetic imported projection facts exercise exact reuse, not authority
    // to publish a real registry package or create an account.
    projection.facts = [
      { id: "package-id", label: "npm package", value: "@example/declared-package" },
      { id: "keywords", label: "Discovery keywords", value: "supplied, exact keywords" },
    ];
    projection.links.push({ id: "registry", label: "Package registry", kind: "other", url: "https://example.invalid/registry/declared-package" });
    model.pressKit = createPressKitView({ pressKit: projection, artifactDirectory: "press-kit" });
    const values = [...documentFor(model).querySelectorAll("#presentation [data-copy-value]")]
      .map((entry) => entry.dataset.copyValue);
    for (const value of [...projection.boilerplates.map((entry) => entry.text),
      ...projection.facts.map((entry) => entry.value), ...projection.links.map((entry) => entry.url)]) {
      expect(values).toContain(value);
    }
    expect(values).not.toContain("@example/example-expanded");
  });

  test.each(["../private.png", "https://elsewhere.invalid/preview.png"])("rejects an unsafe selected path %s", (path) => {
    const model = modelFor();
    model.downloads[0].path = path;
    expect(() => documentFor(model)).toThrow(/bundle-relative path/u);
  });

  test("keeps the legacy model free of presentation navigation and placeholders", () => {
    const model = modelFor();
    delete model.downloads;
    const document = documentFor(model);
    expect(document.querySelector("#presentation")).toBeNull();
    expect(document.querySelector("a[href='#presentation']")).toBeNull();
  });
});
