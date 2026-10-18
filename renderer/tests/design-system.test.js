// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import fs from "node:fs";

import { describe, expect, test } from "vitest";

import { createDesignSystemView } from "../src/design-system.js";
import { assertBrandKitViewModel } from "../src/model.js";

function projections() {
  const read = (name) => JSON.parse(fs.readFileSync(new URL(
    `../../tests/fixtures/v1/valid/minimal/expected/${name}.json`,
    import.meta.url,
  ), "utf8"));
  return {
    handbook: read("design-system-handbook"),
    context: read("design-context"),
    artifactDirectory: "design-system",
  };
}

function boundModel() {
  const pair = projections();
  const model = JSON.parse(fs.readFileSync(new URL(
    "../fixtures/example.brand-kit.view-model.json", import.meta.url,
  ), "utf8"));
  model.release.sourceDigest = pair.handbook.source.digest;
  model.release.immutableId = `sha256:${pair.handbook.source.digest}`;
  model.designSystem = createDesignSystemView(pair);
  return model;
}

describe("design-system source binding", () => {
  test("accepts the generated pair bound to its release without changing inputs", () => {
    const model = boundModel();
    const before = structuredClone(model);
    expect(assertBrandKitViewModel(model)).toBe(model);
    expect(model).toEqual(before);
    expect(model.designSystem.artifacts).toHaveLength(4);
  });

  for (const document of ["handbook", "context"]) {
    test.each([undefined, null, []])(`rejects absent/non-object ${document} source: %j`, (source) => {
      const pair = projections();
      pair[document].source = source;
      expect(() => createDesignSystemView(pair)).toThrow(/source must be an object/u);
    });

    test.each([
      undefined, null, 123, {}, ["a".repeat(64)], "a".repeat(63),
      "", "A".repeat(64), `${"a".repeat(64)} `,
      `${"a".repeat(64)}\n`, `${"a".repeat(64)}\r\n`,
    ])(`rejects malformed ${document} digest: %j`, (digest) => {
      const pair = projections();
      pair[document].source.digest = digest;
      expect(() => createDesignSystemView(pair)).toThrow(/SHA-256 source digest/u);
    });

    test(`rejects a ${document} from another source snapshot`, () => {
      const pair = projections();
      pair[document].source.digest = "0".repeat(64);
      expect(() => createDesignSystemView(pair)).toThrow(/source digests must match/u);
    });
  }

  test("rejects an internally matching pair from a different release", () => {
    const model = boundModel();
    model.designSystem.handbook.source.digest = "0".repeat(64);
    model.designSystem.context.source.digest = "0".repeat(64);
    expect(() => assertBrandKitViewModel(model)).toThrow(/must match the Brand Kit immutable release/u);
  });

  test.each([undefined, null, 123, ["a".repeat(64)], "invalid", "0".repeat(64)])(
    "rejects missing, malformed or mismatched release binding: %j", (digest) => {
      const model = boundModel();
      model.release.sourceDigest = digest;
      expect(() => assertBrandKitViewModel(model)).toThrow(/must match the Brand Kit immutable release/u);
    },
  );

  test.each(["id", "displayName"])("rejects a pair for another project %s", (field) => {
    const model = boundModel();
    model.designSystem.handbook.project[field] = "Other Product";
    model.designSystem.context.project[field] = "Other Product";
    expect(() => assertBrandKitViewModel(model)).toThrow(/must match the Brand Kit view model project/u);
  });

  test("keeps the projection pair optional for existing Brand Kits", () => {
    const model = boundModel();
    delete model.designSystem;
    expect(assertBrandKitViewModel(model)).toBe(model);
  });
});
