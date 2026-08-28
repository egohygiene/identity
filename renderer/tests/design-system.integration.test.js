// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { JSDOM } from "jsdom";
import { describe, expect, test } from "vitest";

import { assertBrandKitViewModel } from "../src/model.js";

const testDirectory = path.dirname(fileURLToPath(import.meta.url));
const rendererRoot = path.resolve(testDirectory, "..");
const repositoryRoot = path.resolve(rendererRoot, "..");
const projectionSource = path.join(
  repositoryRoot,
  "tests/fixtures/v1/valid/minimal",
);
const rendererFixture = path.join(
  rendererRoot,
  "fixtures/example.brand-kit.view-model.json",
);
const renderStatic = path.join(rendererRoot, "scripts/render-static.mjs");
const renderDesignSystem = path.join(
  repositoryRoot,
  "scripts/render_design_system.py",
);

describe("generated design-system renderer handoff", () => {
  test("renders generated handbook and AI context without hard-coded project facts", () => {
    const temporaryDirectory = fs.mkdtempSync(
      path.join(os.tmpdir(), "identity-design-system-renderer-"),
    );
    try {
      const consumerRoot = path.join(temporaryDirectory, "consumer");
      fs.cpSync(projectionSource, consumerRoot, { recursive: true });
      const projectionDirectory = path.join(
        consumerRoot,
        "assets/identity/design-system",
      );
      const outputPath = path.join(temporaryDirectory, "index.html");

      execFileSync(
        "python3",
        [
          renderDesignSystem,
          "--repository-root",
          consumerRoot,
          "--output-directory",
          "assets/identity/design-system",
        ],
        { cwd: repositoryRoot, stdio: "pipe" },
      );
      execFileSync(
        process.execPath,
        [
          renderStatic,
          "--model",
          rendererFixture,
          "--output",
          outputPath,
          "--design-system-directory",
          projectionDirectory,
          "--design-system-artifact-directory",
          "design-system",
        ],
        { cwd: rendererRoot, stdio: "pipe" },
      );

      const document = new JSDOM(fs.readFileSync(outputPath, "utf8")).window
        .document;
      const section = document.querySelector("#design-system");
      const downloadPaths = [
        ...document.querySelectorAll("#design-system a[download]"),
      ].map((link) => link.getAttribute("href"));

      expect(section?.textContent).toContain("Example Product");
      expect(section?.textContent).toContain("Start with semantic intent");
      expect(section?.textContent).toContain("Make meaning survive styling changes");
      expect(section?.textContent).toContain("Semantic token guidance");
      expect(downloadPaths).toEqual([
        "./design-system/design-system-handbook.json",
        "./design-system/design-system-handbook.md",
        "./design-system/design-context.json",
        "./design-system/design-context.md",
      ]);
      expect(section?.textContent).not.toContain("Ego Hygiene");
    } finally {
      fs.rmSync(temporaryDirectory, { recursive: true, force: true });
    }
  });

  test("refuses a handbook for a different Brand Kit project", () => {
    const model = JSON.parse(fs.readFileSync(rendererFixture, "utf8"));
    model.designSystem = {
      handbook: {
        schema: "identity.design-system-handbook/v1",
        project: { id: "other-product", displayName: "Other Product" },
        sections: [],
        capabilities: [],
      },
      context: {
        schema: "identity.design-context/v1",
        project: { id: "other-product", displayName: "Other Product" },
        source: {
          digest: "0000000000000000000000000000000000000000000000000000000000000000",
          handbookSchema: "identity.design-system-handbook/v1",
        },
        tokens: [],
      },
      artifacts: [
        {
          id: "handbook-json",
          label: "Handbook JSON",
          path: "design-system/design-system-handbook.json",
          mediaType: "application/json",
        },
        {
          id: "handbook-markdown",
          label: "Handbook Markdown",
          path: "design-system/design-system-handbook.md",
          mediaType: "text/markdown",
        },
        {
          id: "context-json",
          label: "Context JSON",
          path: "design-system/design-context.json",
          mediaType: "application/json",
        },
        {
          id: "context-markdown",
          label: "Context Markdown",
          path: "design-system/design-context.md",
          mediaType: "text/markdown",
        },
      ],
    };

    expect(() => assertBrandKitViewModel(model)).toThrow(
      "Design-system handbook project must match",
    );
  });
});
