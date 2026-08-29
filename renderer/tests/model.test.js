// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { describe, expect, test } from "vitest";

import { joinAssetUrl, sourceDataUrl } from "../src/model.js";

describe("joinAssetUrl", () => {
  test("preserves route-relative generated downloads", () => {
    expect(joinAssetUrl("./", "packages/brand-kit/brand-kit.zip")).toBe(
      "./packages/brand-kit/brand-kit.zip",
    );
    expect(joinAssetUrl("../identity", "/brand/mark.svg")).toBe(
      "../identity/brand/mark.svg",
    );
  });

  test("preserves rooted and absolute deployment prefixes", () => {
    expect(joinAssetUrl("/products/example/v1", "packages/tokens/tokens.json")).toBe(
      "/products/example/v1/packages/tokens/tokens.json",
    );
    expect(
      joinAssetUrl(
        "https://cdn.example.invalid/identity/v1",
        "packages/metadata/metadata.json",
      ),
    ).toBe(
      "https://cdn.example.invalid/identity/v1/packages/metadata/metadata.json",
    );
  });
});

describe("sourceDataUrl", () => {
  test("uses immutable download paths for approved raster previews", () => {
    expect(
      sourceDataUrl(
        {
          mediaType: "image/png",
          downloadPath: "mascot/kern-icon.png",
          text: "",
        },
        "./",
      ),
    ).toBe("./mascot/kern-icon.png");
  });
});
