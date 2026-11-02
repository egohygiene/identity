// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { describe, expect, test } from "vitest";

import { assertPressKitView, createPressKitView } from "../src/press-kit.js";

describe("Press Kit renderer view", () => {
  for (const field of ["asset", "artifact"]) {
    test.each([
      "../outside.svg", "assets/./mark.svg", "//elsewhere.test/mark.svg",
      "https://elsewhere.test/mark.svg", "assets/%2e%2e/outside.svg",
      "assets/%2fmark.svg", "assets/%5cmark.svg", "assets/%252fmark.svg", "assets\\mark.svg",
    ])(`rejects an unsafe ${field} path in both projections and imported views: %s`, (input) => {
      const pressKit = projection();
      const setPath = (value) => {
        if (field === "asset") value.assets[0].downloadPath = input;
        else value.artifacts[4].path = input;
      };
      setPath(pressKit);
      expect(() => createPressKitView({ pressKit, artifactDirectory: "press-kit" })).toThrow(/bundle-relative path/u);

      const view = createPressKitView({ pressKit: projection(), artifactDirectory: "press-kit" });
      if (field === "asset") view.pressKit.assets[0].downloadPath = `press-kit/${input}`;
      else view.artifacts[4].path = `press-kit/${input}`;
      expect(() => assertPressKitView(view)).toThrow(/bundle-relative path/u);
    });
  }

  test.each(["../kit", "//elsewhere.test/kit", "kit\\nested", "kit/%2f", "kit/%252f"])(
    "rejects an unsafe Press Kit directory %s", (artifactDirectory) => {
      expect(() => createPressKitView({ pressKit: projection(), artifactDirectory })).toThrow(/bundle-relative path/u);
    },
  );

  test("canonicalizes safe prefixes and URL encoding consistently", () => {
    const pressKit = projection();
    pressKit.assets[0].downloadPath = "./assets/mark%20draft..svg";
    const view = createPressKitView({ pressKit, artifactDirectory: "./press kit/" });
    expect(view.pressKit.assets[0].downloadPath).toBe("press%20kit/assets/mark%20draft..svg");
    expect(assertPressKitView(view)).toBe(view);
  });

  test("validates projection artifact paths retained inside an imported view", () => {
    const view = createPressKitView({ pressKit: projection(), artifactDirectory: "press-kit" });
    view.pressKit.artifacts[4].path = "https://elsewhere.test/kit.zip";
    expect(() => assertPressKitView(view)).toThrow(/Press Kit projection artifact path.*bundle-relative path/u);
  });

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
    ).toThrow("must be a non-empty bundle-relative path");
  });

  test("retains an optional supplied paragraph without changing existing boilerplates", () => {
    const pressKit = projection();
    const paragraph = {
      id: "paragraph",
      kind: "paragraph",
      text: "A supplied approved paragraph, copied exactly.",
    };
    pressKit.boilerplates.push(paragraph);
    const view = createPressKitView({ pressKit, artifactDirectory: "press-kit" });

    expect(view.pressKit.boilerplates).toEqual(pressKit.boilerplates);
    expect(view.pressKit.boilerplates.find((value) => value.kind === "paragraph")).toEqual(paragraph);
    expect(assertPressKitView(view)).toBe(view);
  });

  test.each(["duplicate-short", "duplicate-paragraph", "unknown", "missing-short", "missing-long"])(
    "rejects %s boilerplate kinds before rendering or importing a view", (invalid) => {
      const mutate = (pressKit) => {
        if (invalid.startsWith("missing-")) {
          pressKit.boilerplates = pressKit.boilerplates.filter(
            (value) => value.kind !== invalid.slice("missing-".length),
          );
        } else {
          const kind = invalid === "unknown" ? "unknown" : invalid.slice("duplicate-".length);
          const value = { id: "extra", kind, text: "Extra supplied copy." };
          pressKit.boilerplates.push(value);
          if (kind === "paragraph") pressKit.boilerplates.push({ ...value, id: "another-paragraph" });
        }
      };
      const pressKit = projection();
      mutate(pressKit);
      expect(() => createPressKitView({ pressKit, artifactDirectory: "press-kit" })).toThrow(/boilerplate/u);

      const view = createPressKitView({ pressKit: projection(), artifactDirectory: "press-kit" });
      mutate(view.pressKit);
      expect(() => assertPressKitView(view)).toThrow(/boilerplate/u);
    },
  );
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
