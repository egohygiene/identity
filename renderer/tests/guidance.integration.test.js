// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { describe, expect, test } from "vitest";

const rendererRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const repositoryRoot = path.resolve(rendererRoot, "..");
const cases = JSON.parse(
  fs.readFileSync(
    path.join(repositoryRoot, "tests/fixtures/guidance-public-cases.json"),
    "utf8",
  ),
).cases;
const fixtureRoot = path.join(repositoryRoot, "tests/fixtures/v1/valid/minimal");
const fixtureModel = path.join(rendererRoot, "fixtures/example.brand-kit.view-model.json");

describe("public guidance in static renderer output", () => {
  for (const guidanceCase of cases) {
    test(`filters ${guidanceCase.id} from HTML and embedded model data`, () => {
      const temporary = fs.mkdtempSync(
        path.join(os.tmpdir(), "identity-public-guidance-"),
      );
      try {
        const consumer = path.join(temporary, "consumer");
        fs.cpSync(fixtureRoot, consumer, { recursive: true });
        for (const update of guidanceCase.updates) {
          const sourcePath = path.join(
            consumer,
            `.identity/guidance/${update.document}.json`,
          );
          const source = JSON.parse(fs.readFileSync(sourcePath, "utf8"));
          const tokens = update.pointer.slice(1).split("/");
          let parent = source;
          for (const token of tokens.slice(0, -1)) parent = parent[token];
          parent[tokens.at(-1)] = update.value;
          fs.writeFileSync(sourcePath, JSON.stringify(source));
        }
        const pythonModel = JSON.parse(
          execFileSync(
            "python3",
            [
              path.join(repositoryRoot, "scripts/render_guidance.py"),
              "--repository-root", consumer,
              "--audience", "public",
              "--format", "json",
            ],
            { encoding: "utf8" },
          ),
        );
        const model = JSON.parse(fs.readFileSync(fixtureModel, "utf8"));
        const declared = (value) => ({ status: "declared", canonical: true, value });
        model.guidance = {
          voice: declared(
            Object.fromEntries(
              ["foundation", "characteristics", "contexts", "localization"]
                .filter((key) => pythonModel[key] !== null)
                .map((key) => [key, pythonModel[key]]),
            ),
          ),
          usage: declared({
            sections: pythonModel.sections,
            assets: [...pythonModel.downloads, ...pythonModel.legacyAssets],
            ...(pythonModel.accessibility
              ? { accessibility: pythonModel.accessibility }
              : {}),
            ...(pythonModel.legal ? { legal: pythonModel.legal } : {}),
          }),
        };
        const modelPath = path.join(temporary, "model.json");
        const outputPath = path.join(temporary, "index.html");
        fs.writeFileSync(modelPath, JSON.stringify(model));
        execFileSync(process.execPath, [
          path.join(rendererRoot, "scripts/render-static.mjs"),
          "--model", modelPath,
          "--output", outputPath,
        ]);
        const html = fs.readFileSync(outputPath, "utf8");
        for (const phrase of guidanceCase.withheld) expect(html).not.toContain(phrase);
        for (const phrase of guidanceCase.retained) expect(html).toContain(phrase);
        expect(html).toContain("Voice and personality");
        expect(html).toContain("Usage rules");
      } finally {
        fs.rmSync(temporary, { recursive: true, force: true });
      }
    });
  }
});
