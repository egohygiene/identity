// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { describe, expect, test } from "vitest";

import { assertPressKitView, createPressKitView } from "../src/press-kit.js";

describe("Press Kit renderer view", () => {
  test("keeps every generated path inside its supplied publication directory", () => {
    const view = createPressKitView({
      pressKit: projection(),
      artifactDirectory: "press-kit",
    });

    expect(view.artifacts.map((artifact) => artifact.path)).toEqual([
      "press-kit/press-kit.json",
      "press-kit/press-kit.md",
      "press-kit/press-kit-manifest.json",
      "press-kit/SHA256SUMS",
      "press-kit/press-kit.zip",
    ]);
    expect(view.pressKit.assets[0].downloadPath).toBe(
      "press-kit/assets/example-mark.svg",
    );
    expect(assertPressKitView(view)).toBe(view);
  });

  test("rejects a view whose generated artifact escapes its publication directory", () => {
    const view = createPressKitView({
      pressKit: projection(),
      artifactDirectory: "press-kit",
    });
    view.artifacts[0].path = "elsewhere/press-kit.json";

    expect(() => assertPressKitView(view)).toThrow(
      "must stay within the published Press Kit directory",
    );
  });

  test("rejects a projection attempting a traversal path before rendering", () => {
    const value = projection();
    value.assets[0].downloadPath = "../private-mark.svg";

    expect(() =>
      createPressKitView({ pressKit: value, artifactDirectory: "press-kit" }),
    ).toThrow("must stay within the published Press Kit directory");
  });
});

function projection() {
  return {
    schema: "identity.press-kit/v1",
    project: { id: "example-product", displayName: "Example Product" },
    source: {
      digest: "a".repeat(64),
      sourceSchema: "identity.press-kit-source/v1",
    },
    boilerplates: [
      { id: "short", kind: "short", text: "Short approved boilerplate." },
      { id: "long", kind: "long", text: "Long approved boilerplate." },
    ],
    facts: [],
    links: [],
    contacts: [],
    team: [],
    assets: [{ id: "mark", downloadPath: "assets/example-mark.svg" }],
    guidance: {},
    artifacts: [
      ["press-kit-json", "Press Kit data", "press-kit.json", "application/json"],
      ["press-kit-markdown", "Press Kit", "press-kit.md", "text/markdown"],
      ["press-kit-manifest", "Manifest", "press-kit-manifest.json", "application/json"],
      ["press-kit-checksums", "Checksums", "SHA256SUMS", "text/plain"],
      ["press-kit-archive", "Archive", "press-kit.zip", "application/zip"],
    ].map(([id, label, path, mediaType]) => ({ id, label, path, mediaType })),
  };
}
