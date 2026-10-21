// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { JSDOM } from "jsdom";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, test } from "vitest";

import { BrandKitPage } from "../src/app.js";
import { assertBrandKitViewModel } from "../src/model.js";

const rendererRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const fixture = JSON.parse(fs.readFileSync(
  path.join(rendererRoot, "fixtures/example.brand-kit.view-model.json"), "utf8",
));

describe("selected, source-bound Brand Kit downloads", () => {
  test.each(["brand-kit-archive", "complete-brand-kit"])(
    "uses the declared %s archive path in the hero", (id) => {
      const model = structuredClone(fixture);
      model.packages = [{ ...model.packages[0], id, path: "packages/reviewed-kit-v2.zip" }];
      const document = renderDocument(model, "https://cdn.example.invalid/identity/v2/");
      expect(document.querySelector(".hero a[download]").getAttribute("href"))
        .toBe("https://cdn.example.invalid/identity/v2/packages/reviewed-kit-v2.zip");
    },
  );

  test("omits a missing complete archive without guessing from another ZIP", () => {
    const model = structuredClone(fixture);
    model.packages = [{ ...model.packages[0], id: "selected-asset-archive", path: "packages/selected.zip" }];
    const document = renderDocument(model);
    expect(document.querySelector(".hero a[download]")).toBeNull();
    expect(document.querySelector(".hero__meta").textContent).toContain("Release");
    expect(document.querySelector("#downloads").textContent).toContain("Complete Brand Kit");
    expect([...document.querySelectorAll("a[download]")].map((link) => link.getAttribute("href")))
      .not.toContain("./packages/brand-kit/brand-kit.zip");
  });

  test("groups only supplied renditions with their public source and preserves usage", () => {
    const model = structuredClone(fixture);
    const source = model.assets[0];
    source.label = "Reviewed compact mark";
    source.kind = "mark";
    source.notes = "Use the supplied neutral background.";
    source.usage = {
      safeZone: "Keep one cap height clear.",
      minimumSize: "At least 24 pixels.",
      restrictions: ["Do not recolor this artwork."],
    };
    model.downloads = [
      rendition(source, { id: "reviewed-master", path: source.downloadPath, mediaType: source.mediaType }),
      rendition(source),
    ];
    const document = renderDocument(model, "/products/example/v1/");
    const card = document.querySelector("#logos .asset-card");
    const derived = card.querySelector("[data-asset-downloads]");
    expect(derived.dataset.assetDownloads).toBe(source.id);
    expect([...card.querySelectorAll("a[download]")].map((link) => link.getAttribute("href")))
      .toEqual([
        `/products/example/v1/${source.downloadPath}`,
        "/products/example/v1/web/reviewed-icon.png",
      ]);
    for (const value of [source.label, source.notes, ...Object.values(source.usage).flat()]) {
      expect(card.textContent).toContain(value);
    }
    for (const value of ["Supplied 32-pixel icon", "32 × 32 pixels", "image/png", "web", source.id, source.sha256]) {
      expect(derived.textContent).toContain(value);
    }
    expect(card.textContent).not.toMatch(/Monochrome|Dark variant|Light variant/u);
  });

  test("retains legacy models and omits absent optional renditions", () => {
    const model = structuredClone(fixture);
    expect(model).not.toHaveProperty("downloads");
    const document = renderDocument(model);
    expect(document.querySelector("[data-asset-downloads]")).toBeNull();
    expect(document.querySelector("#logos").textContent).not.toContain("undefined");
  });

  test.each([
    ["missing source", (model) => { model.downloads[0].sourceAssetId = "unselected-source"; }],
    ["different source hash", (model) => { model.downloads[0].sourceSha256 = "f".repeat(64); }],
    ["malformed source hash", (model) => { model.downloads[0].sourceSha256 = "not-a-digest"; }],
    ["unsafe path", (model) => { model.downloads[0].path = "%2e%2e/private.png"; }],
    ["missing dimensions", (model) => { delete model.downloads[0].dimensions; }],
    ["duplicate identifier", (model) => { model.downloads.push({ ...model.downloads[0], path: "web/other.png" }); }],
    ["duplicate canonical path", (model) => { model.downloads.push({ ...model.downloads[0], id: "another", path: "./web/reviewed-icon.png" }); }],
    ["non-array declaration", (model) => { model.downloads = null; }],
  ])("rejects %s before rendering public download links", (_label, mutate) => {
    const model = structuredClone(fixture);
    model.downloads = [rendition(model.assets[0])];
    mutate(model);
    expect(() => assertBrandKitViewModel(model)).toThrow();
  });
});

describe("explicit browser assets and local artifact verification", () => {
  test("omits undeclared browser links from a standalone preview", () => {
    withStaticInputs(({ run, output }) => {
      expect(run().status).toBe(0);
      const document = new JSDOM(fs.readFileSync(output, "utf8")).window.document;
      expect(document.querySelector("link[rel=icon]")).toBeNull();
      expect(document.querySelector("link[rel=apple-touch-icon]")).toBeNull();
      expect(document.querySelector("link[rel=manifest]")).toBeNull();
    });
  });

  test.each(["./", "../identity/", "/products/example/v1/", "https://cdn.example.invalid/identity/v1/"])(
    "preserves explicit browser assets under base %s", (base) => {
      withStaticInputs(({ run, output }) => {
        expect(run([
          "--asset-base-url", base,
          "--icon-path", "web/reviewed-icon.svg",
          "--apple-touch-icon-path", "web/reviewed-touch.png",
          "--web-manifest-path", "web/reviewed.webmanifest",
        ]).status).toBe(0);
        const document = new JSDOM(fs.readFileSync(output, "utf8")).window.document;
        expect(document.querySelector("link[rel=icon]").getAttribute("href"))
          .toBe(`${base}web/reviewed-icon.svg`);
        expect(document.querySelector("link[rel=apple-touch-icon]").getAttribute("href"))
          .toBe(`${base}web/reviewed-touch.png`);
        expect(document.querySelector("link[rel=manifest]").getAttribute("href"))
          .toBe(`${base}web/reviewed.webmanifest`);
      });
    },
  );

  test.each([
    ["encoded traversal", ["--icon-path", "%2e%2e/hidden.svg"]],
    ["external browser path", ["--web-manifest-path", "https://elsewhere.invalid/site.webmanifest"]],
    ["manifest without root", ["--artifact-manifest", "missing-manifest.json"]],
  ])("rejects %s without replacing an existing page", (_label, argumentsList) => {
    withStaticInputs(({ run, output }) => {
      expect(run(argumentsList).status).not.toBe(0);
      expect(fs.readFileSync(output, "utf8")).toBe("existing reviewed page");
    });
  });

  test("checks supplied local artifacts before replacing an existing page", () => {
    withStaticInputs(({ model, modelPath, temporary, run, output }) => {
      const root = path.join(temporary, "artifacts");
      model.packages = [];
      model.assets = [model.assets[0]];
      const asset = model.assets[0];
      const contents = Buffer.from(asset.text, "utf8");
      asset.sha256 = createHash("sha256").update(contents).digest("hex");
      const target = path.join(root, asset.downloadPath);
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.writeFileSync(target, contents);
      fs.writeFileSync(modelPath, JSON.stringify(model));
      expect(run(["--artifact-root", root]).status).toBe(0);
      fs.writeFileSync(output, "existing reviewed page");
      fs.rmSync(target);
      const missing = run(["--artifact-root", root]);
      expect(missing.status).not.toBe(0);
      expect(fs.readFileSync(output, "utf8")).toBe("existing reviewed page");
    });
  });
});

function rendition(source, values = {}) {
  return {
    id: "reviewed-icon-32",
    label: "Supplied 32-pixel icon",
    path: "web/reviewed-icon.png",
    mediaType: "image/png",
    profile: "web",
    sourceAssetId: source.id,
    sourceSha256: source.sha256,
    dimensions: "32 × 32 pixels",
    ...values,
  };
}

function renderDocument(model, assetBaseUrl = "./") {
  return new JSDOM(renderToStaticMarkup(React.createElement(BrandKitPage, {
    model, assetBaseUrl,
  }))).window.document;
}

function withStaticInputs(check) {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "identity-selected-downloads-"));
  try {
    const model = structuredClone(fixture);
    const modelPath = path.join(temporary, "model.json");
    const output = path.join(temporary, "index.html");
    fs.writeFileSync(modelPath, JSON.stringify(model));
    fs.writeFileSync(output, "existing reviewed page");
    const run = (argumentsList = []) => spawnSync(process.execPath, [
      path.join(rendererRoot, "scripts/render-static.mjs"),
      "--model", modelPath,
      "--output", output,
      ...argumentsList,
    ], { cwd: rendererRoot, encoding: "utf8" });
    check({ model, modelPath, temporary, output, run });
  } finally {
    fs.rmSync(temporary, { recursive: true, force: true });
  }
}
