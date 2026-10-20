// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { execFileSync, spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { JSDOM } from "jsdom";
import { describe, expect, test } from "vitest";

const rendererRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const repositoryRoot = path.resolve(rendererRoot, "..");

describe("release-backed public asset rights", () => {
  test("preserves supplied rights and leaves absent metadata unresolved without changing the release archive", () => {
    const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "identity-public-rights-"));
    try {
      const repository = path.join(temporary, "consumer");
      const renderer = path.join(repository, "renderer");
      fs.mkdirSync(renderer, { recursive: true });
      for (const name of ["src", "scripts", "index.template.html", "vite.config.js", "package.json"]) {
        fs.cpSync(path.join(rendererRoot, name), path.join(renderer, name), { recursive: true });
      }
      fs.symlinkSync(path.join(rendererRoot, "node_modules"), path.join(renderer, "node_modules"), "junction");
      fs.mkdirSync(path.join(repository, "scripts"));
      fs.copyFileSync(
        path.join(repositoryRoot, "scripts/package_public_brand_kit.py"),
        path.join(repository, "scripts/package_public_brand_kit.py"),
      );
      fs.cpSync(path.join(repositoryRoot, "publication"), path.join(repository, "publication"), { recursive: true });

      const config = JSON.parse(fs.readFileSync(
        path.join(repositoryRoot, "publication/identity-brand-kit.config.json"), "utf8",
      ));
      const known = {
        ...config.assets[0], id: "known", label: "Supplied asset rights", sourcePath: "brand/known.svg",
        license: { spdx: "CC-BY-4.0", status: "approved", attribution: "Synthetic rights-holder attribution." },
        origin: { creator: "Synthetic creator", method: "licensed", source: "https://example.invalid/artwork", capturedAt: "2026-10-20" },
        approval: "synthetic-rights-review",
        usage: { safeZone: "One cap height", minimumSize: "24 pixels", restrictions: ["Keep the supplied attribution."] },
      };
      const unknown = {
        ...config.assets[0], id: "unknown", label: "Rights not declared", sourcePath: "brand/unknown.svg",
      };
      delete unknown.license;
      delete unknown.origin;
      delete unknown.approval;
      delete unknown.usage;
      config.assets = [known, unknown];
      fs.writeFileSync(path.join(repository, "publication/identity-brand-kit.config.json"), JSON.stringify(config));
      fs.mkdirSync(path.join(repository, "assets/identity/brand"), { recursive: true });
      const contents = {
        "known.svg": "<svg xmlns=\"http://www.w3.org/2000/svg\"><title>Supplied synthetic asset</title></svg>\n",
        "unknown.svg": "<svg xmlns=\"http://www.w3.org/2000/svg\"><title>Existing release asset with unresolved metadata</title></svg>\n",
      };
      for (const [name, value] of Object.entries(contents)) {
        fs.writeFileSync(path.join(repository, "assets/identity/brand", name), value);
      }

      const result = spawnSync(process.execPath, [
        path.join(renderer, "scripts/build-public-site.mjs"),
        "--source-root", repository,
        "--output-directory", "dist",
        "--release-tag", "v1.0.0",
        "--release-commit", "a".repeat(40),
      ], { cwd: renderer, encoding: "utf8" });
      expect(result.status, `${result.stdout}\n${result.stderr}`).toBe(0);
      const model = JSON.parse(fs.readFileSync(path.join(renderer, ".identity-public-build/brand-kit.view-model.json"), "utf8"));
      expect(model.assets[0].license).toEqual(known.license);
      expect(model.assets[0].origin).toEqual(known.origin);
      expect(model.assets[0].approval).toBe(known.approval);
      expect(model.assets[0].usage).toEqual(known.usage);
      expect(model.assets[1].license).toBeNull();
      expect(model.assets[1].origin).toBeNull();
      expect(model.assets[1].approval).toBeNull();
      expect(model.assets[1]).not.toHaveProperty("usage");
      expect(JSON.stringify(model.assets[1])).not.toMatch(/MIT|Ego Hygiene contributors|human-approved-visual-direction|2026-08-22/u);

      const document = new JSDOM(fs.readFileSync(path.join(renderer, "dist/index.html"), "utf8")).window.document;
      expect(document.querySelector("#provenance").textContent).toContain("Rights not declared");
      expect(document.querySelector("#provenance").textContent).toContain("Not declared");
      const embedded = JSON.parse(document.querySelector("#identity-brand-kit-model").textContent);
      expect(embedded.assets[1]).toEqual(model.assets[1]);
      const downloads = [...document.querySelectorAll("a[download]")].map((link) => link.getAttribute("href"));
      expect(downloads).toContain("./brand/unknown.svg");

      const archive = path.join(renderer, "dist/packages/identity-brand-kit-v1.0.0.zip");
      const archived = JSON.parse(execFileSync("python3", [
        "-c", "import json,sys,zipfile; archive=zipfile.ZipFile(sys.argv[1]); print(json.dumps({name:archive.read(name).decode(\"utf-8\") for name in archive.namelist()}))",
        archive,
      ], { encoding: "utf8" }));
      for (const [name, value] of Object.entries(contents)) {
        expect(fs.readFileSync(path.join(renderer, "dist/brand", name), "utf8")).toBe(value);
        expect(archived[`identity-brand-kit/brand/${name}`]).toBe(value);
      }
      const manifest = JSON.parse(fs.readFileSync(path.join(renderer, "dist/packages/identity-brand-kit-v1.0.0.manifest.json"), "utf8"));
      expect(manifest.files.map((entry) => entry.path)).toEqual(["brand/known.svg", "brand/unknown.svg"]);
    } finally {
      fs.rmSync(temporary, { recursive: true, force: true });
    }
  }, 20000);
});
