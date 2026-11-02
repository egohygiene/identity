// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { execFileSync, spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { JSDOM } from "jsdom";
import { describe, expect, test } from "vitest";

const testDirectory = path.dirname(fileURLToPath(import.meta.url));
const rendererRoot = path.resolve(testDirectory, "..");
const repositoryRoot = path.resolve(rendererRoot, "..");
const projectionSource = path.join(repositoryRoot, "tests/fixtures/v1/valid/minimal");
const rendererFixture = path.join(rendererRoot, "fixtures/example.brand-kit.view-model.json");
const renderStatic = path.join(rendererRoot, "scripts/render-static.mjs");
const renderDesignSystem = path.join(repositoryRoot, "scripts/render_design_system.py");
const artifactNames = [
  "design-system-handbook.json", "design-system-handbook.md",
  "design-context.json", "design-context.md",
];

function withConsumer(legacy, check) {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "identity-design-system-renderer-"));
  try {
    const consumerRoot = path.join(temporary, "consumer");
    fs.cpSync(projectionSource, consumerRoot, { recursive: true });
    if (legacy) {
      fs.writeFileSync(path.join(consumerRoot, ".identity/identity.toml"), "[identity]\nname = \"legacy\"\n");
    }
    execFileSync("python3", [
      renderDesignSystem, "--repository-root", consumerRoot,
      "--output-directory", "assets/identity/design-system",
    ], { cwd: repositoryRoot, stdio: "pipe" });
    const projectionDirectory = path.join(consumerRoot, "assets/identity/design-system");
    const read = (name) => JSON.parse(fs.readFileSync(path.join(projectionDirectory, name), "utf8"));
    const handbook = read("design-system-handbook.json");
    const context = read("design-context.json");
    // Construct a test model for this snapshot; retain the committed v0 fixture
    // and all real release bindings unchanged.
    const model = JSON.parse(fs.readFileSync(rendererFixture, "utf8"));
    model.tokens = structuredClone(context.tokens);
    model.release.sourceDigest = handbook.source.digest;
    model.release.immutableId = `sha256:${handbook.source.digest}`;
    const modelPath = path.join(temporary, "model.json");
    const siteRoot = path.join(temporary, "site");
    const outputPath = path.join(siteRoot, "index.html");
    const render = () => {
      fs.writeFileSync(modelPath, JSON.stringify(model));
      return spawnSync(process.execPath, [
        renderStatic, "--model", modelPath, "--output", outputPath,
        "--design-system-directory", projectionDirectory,
        "--design-system-artifact-directory", "design-system",
      ], { cwd: rendererRoot, encoding: "utf8" });
    };
    check({ model, handbook, context, projectionDirectory, siteRoot, outputPath, render });
  } finally {
    fs.rmSync(temporary, { recursive: true, force: true });
  }
}

describe("generated design-system renderer handoff", () => {
  test.each([false, true])("renders matching guidance and all four downloads (legacy TOML: %s)", (legacy) => {
    withConsumer(legacy, ({ model, handbook, context, projectionDirectory, siteRoot, outputPath, render }) => {
      expect(handbook.source.digest).toBe("1002ff75ea51f6e016929894ea30cc96565bdbbca749a0e7fff1ebd0d2f21353");
      expect(context.source.digest).toBe(model.release.sourceDigest);
      fs.mkdirSync(siteRoot);
      fs.cpSync(projectionDirectory, path.join(siteRoot, "design-system"), { recursive: true });
      const result = render();
      expect(result.status, result.stderr).toBe(0);
      const document = new JSDOM(fs.readFileSync(outputPath, "utf8")).window.document;
      const section = document.querySelector("#design-system");
      expect(section?.textContent).toContain("Example Product");
      expect(section?.textContent).toContain("Start with semantic intent");
      expect(section?.textContent).toContain("Make meaning survive styling changes");
      expect(section?.textContent).toContain("Semantic token guidance");
      expect(section?.textContent).not.toContain("Ego Hygiene");
      const links = [...section.querySelectorAll("a[download]")];
      expect(links.map((link) => link.getAttribute("href"))).toEqual(
        artifactNames.map((name) => `./design-system/${name}`),
      );
      for (const [index, link] of links.entries()) {
        const downloaded = fs.readFileSync(path.resolve(siteRoot, link.getAttribute("href")));
        expect(downloaded).toEqual(fs.readFileSync(path.join(projectionDirectory, artifactNames[index])));
      }
    });
  });

  test.each([
    ["stale context", ({ context }) => { context.source.digest = "0".repeat(64); }, "source digests must match"],
    ["stale handbook", ({ handbook }) => { handbook.source.digest = "0".repeat(64); }, "source digests must match"],
    ["mixed release", ({ model }) => { model.release.sourceDigest = "0".repeat(64); }, "must match the Brand Kit immutable release"],
    ["missing handbook binding", ({ handbook }) => { delete handbook.source; }, "handbook source must be an object"],
    ["malformed context binding", ({ context }) => { context.source.digest = ["a".repeat(64)]; }, "SHA-256 source digest"],
    ["different project", ({ handbook, context }) => { handbook.project.id = "other"; context.project.id = "other"; }, "project must match"],
    ["historical v0 release plus new v1 guidance", ({ model }) => {
      model.release = JSON.parse(fs.readFileSync(rendererFixture, "utf8")).release;
    }, "must match the Brand Kit immutable release"],
    ["displayed value with a matching digest", ({ model }) => {
      model.tokens[0].value = { colorSpace: "srgb", components: [0, 0, 0], alpha: 1 };
    }, "token values must match"],
    ["context value with a matching digest", ({ context }) => {
      context.tokens[0].value = { colorSpace: "srgb", components: [0, 0, 0], alpha: 1 };
    }, "token values must match"],
    ["handbook value with a matching digest", ({ handbook }) => {
      const token = handbook.sections.flatMap((section) => section.entries).find((entry) => entry.kind === "token");
      token.content.value = { colorSpace: "srgb", components: [0, 0, 0], alpha: 1 };
    }, "token values must match"],
  ])("rejects %s before replacing an existing page", (_name, mutate, message) => {
    withConsumer(false, (inputs) => {
      mutate(inputs);
      for (const [name, projection] of [
        ["design-system-handbook.json", inputs.handbook], ["design-context.json", inputs.context],
      ]) {
        fs.writeFileSync(path.join(inputs.projectionDirectory, name), JSON.stringify(projection));
      }
      fs.mkdirSync(inputs.siteRoot);
      fs.writeFileSync(inputs.outputPath, "existing reviewed page");
      const result = inputs.render();
      expect(result.status).not.toBe(0);
      expect(result.stderr).toContain(message);
      expect(fs.readFileSync(inputs.outputPath, "utf8")).toBe("existing reviewed page");
    });
  });
});
