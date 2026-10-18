// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import fs from "node:fs";

import { describe, expect, test } from "vitest";

import { normalizeArtifactDirectory, normalizeArtifactPath, normalizeAssetBaseUrl } from "../src/artifact-paths.js";
import { assertBrandKitViewModel, joinAssetUrl } from "../src/model.js";

const invalidPaths = [
  undefined, null, 0, {}, ["brand/mark.svg"], "", ".", "..", "./", "././mark.svg",
  "../outside.svg", "brand/../outside.svg", "brand/./mark.svg", "/brand/mark.svg",
  "//elsewhere.test/mark.svg", "https://elsewhere.test/mark.svg", "https:mark.svg",
  "javascript:alert(1)", "data:image/png;base64,AA", "file:///mark.svg", "C:/mark.svg",
  "brand\\mark.svg", "brand//mark.svg", "brand/", "%2e%2e/outside.svg",
  "brand/.%2E/outside.svg", "brand/%2foutside.svg", "brand/%5Coutside.svg",
  "brand/%252e%252e/outside.svg", "brand/%252foutside.svg", "brand/%25.svg",
  "brand/%.svg", "brand/%GG.svg", "brand/%ff.svg", "brand/mark.svg?raw=1",
  "brand/mark.svg#preview", "brand/mark%3fraw.svg", "brand/mark%23preview.svg",
  "brand/mark\n.svg", "brand/mark\u0000.svg", "brand/mark%0a.svg", "brand/\ud800.svg",
];

function fixture() {
  return JSON.parse(fs.readFileSync(new URL(
    "../fixtures/example.brand-kit.view-model.json", import.meta.url,
  ), "utf8"));
}

describe("bundle-relative artifact paths", () => {
  test.each([
    ["brand/mark.svg", "brand/mark.svg"],
    ["./brand/mark.svg", "brand/mark.svg"],
    ["brand/logo..draft.svg", "brand/logo..draft.svg"],
    ["brand/mark with space.svg", "brand/mark%20with%20space.svg"],
    ["brand/%6dark.svg", "brand/mark.svg"],
    ["brand/日本語.svg", "brand/%E6%97%A5%E6%9C%AC%E8%AA%9E.svg"],
    ["brand/mark%20with%20space.svg", "brand/mark%20with%20space.svg"],
  ])("canonicalizes %s without changing its bundle location", (input, expected) => {
    expect(normalizeArtifactPath(input)).toBe(expected);
    expect(normalizeArtifactPath(expected)).toBe(expected);
    expect(joinAssetUrl("https://cdn.example.test/brand/", input)).toBe(
      `https://cdn.example.test/brand/${expected}`,
    );
  });

  test.each(invalidPaths)("rejects an unsafe path at the URL boundary: %j", (input) => {
    expect(() => joinAssetUrl("https://cdn.example.test/brand/", input)).toThrow(/bundle-relative path/u);
    expect(() => joinAssetUrl("../identity", input)).toThrow(/bundle-relative path/u);
  });

  test("normalizes directory prefixes with the same rules", () => {
    expect(normalizeArtifactDirectory("./kit..draft/")).toBe("kit..draft/");
    expect(normalizeArtifactDirectory("kit with space")).toBe("kit%20with%20space/");
    expect(() => normalizeArtifactDirectory("kit//")).toThrow(/bundle-relative path/u);
    expect(() => normalizeArtifactDirectory("../kit/")).toThrow(/bundle-relative path/u);
  });
});

describe("imported Brand Kit paths", () => {
  for (const collection of ["assets", "packages"]) {
    test.each(invalidPaths)(`checks every ${collection} download before rendering: %j`, (input) => {
      const model = fixture();
      const entry = structuredClone(model[collection][0]);
      entry[collection === "assets" ? "downloadPath" : "path"] = input;
      model[collection].push(entry);
      expect(() => assertBrandKitViewModel(model)).toThrow(/bundle-relative path/u);
    });
  }

  test("keeps embedded sources and generated package paths compatible without mutating the model", () => {
    const model = fixture();
    model.assets.push({ ...model.assets[0], availability: "embedded-source", downloadPath: null });
    const before = structuredClone(model);
    expect(assertBrandKitViewModel(model)).toBe(model);
    expect(model).toEqual(before);
  });
});

describe("explicit deployment bases", () => {
  test.each([
    [undefined, "./"], ["", "./"], ["./", "./"], ["../identity", "../identity/"],
    ["/", "/"], ["/products/example/v1", "/products/example/v1/"],
    ["https://cdn.example.test/identity/v1", "https://cdn.example.test/identity/v1/"],
    ["HTTP://localhost:4173/identity/", "http://localhost:4173/identity/"],
  ])("preserves the configured directory %j", (input, expected) => {
    expect(normalizeAssetBaseUrl(input)).toBe(expected);
    expect(joinAssetUrl(input, "packages/brand-kit/brand-kit.zip")).toBe(
      `${expected}packages/brand-kit/brand-kit.zip`,
    );
  });

  test.each([
    null, false, 123, {}, ["./"], "//cdn.example.test/identity", "javascript:alert(1)",
    "data:text/plain,hello", "file:///identity", "https:cdn.example.test/identity",
    "https://", "https://user:password@cdn.example.test/identity", "./identity?raw=1",
    "https://cdn.example.test/identity#section", "identity\\assets", "identity\nassets",
    " https://cdn.example.test/identity",
  ])("rejects an ambiguous or unsupported base %j", (input) => {
    expect(() => normalizeAssetBaseUrl(input)).toThrow(/Asset base URL/u);
  });
});
