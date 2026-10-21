// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { spawnSync } from "node:child_process";
import { once } from "node:events";
import fs from "node:fs";
import { createServer } from "node:http";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { JSDOM } from "jsdom";
import { describe, expect, test } from "vitest";

import { createDesignSystemView } from "../src/design-system.js";

const rendererRoot = fileURLToPath(new URL("../", import.meta.url));
const fixturePath = path.join(rendererRoot, "fixtures/example.brand-kit.view-model.json");
const expectedRoot = path.resolve(rendererRoot, "../tests/fixtures/v1/valid/minimal/expected");
const artifactNames = [
  "design-system-handbook.json", "design-system-handbook.md", "design-context.json", "design-context.md",
];

async function withInputs(check) {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "identity-artifact-paths-"));
  try {
    const model = JSON.parse(fs.readFileSync(fixturePath, "utf8"));
    const read = (name) => JSON.parse(fs.readFileSync(path.join(expectedRoot, name), "utf8"));
    model.designSystem = createDesignSystemView({
      handbook: read(artifactNames[0]), context: read(artifactNames[2]), artifactDirectory: "design-system",
    });
    model.release.sourceDigest = model.designSystem.handbook.source.digest;
    model.tokens = structuredClone(model.designSystem.context.tokens);
    model.release.immutableId = `sha256:${model.release.sourceDigest}`;
    const publication = {
      releaseTag: "v1.0.0", releaseUrl: "https://github.com/egohygiene/identity/releases/tag/v1.0.0",
      manifestPath: "packages/publication.manifest.json", manifestSha256: "a".repeat(64),
    };
    const outputPath = path.join(temporary, "index.html");
    fs.writeFileSync(outputPath, "existing reviewed page");
    const render = (base = "./", extraArguments = []) => {
      const modelPath = path.join(temporary, "model.json");
      const publicationPath = path.join(temporary, "publication.json");
      fs.writeFileSync(modelPath, JSON.stringify(model));
      fs.writeFileSync(publicationPath, JSON.stringify(publication));
      return spawnSync(process.execPath, [
        path.join(rendererRoot, "scripts/render-static.mjs"), "--model", modelPath,
        "--publication", publicationPath, "--output", outputPath, "--asset-base-url", base,
        ...extraArguments,
      ], { cwd: rendererRoot, encoding: "utf8" });
    };
    await check({ model, publication, outputPath, render });
  } finally {
    fs.rmSync(temporary, { recursive: true, force: true });
  }
}

describe("static artifact URL handoff", () => {
  test.each(["./", "../identity/", "/products/example/v1/", "https://cdn.example.test/identity/v1/"])(
    "retains every generated download under configured base %s", (base) => {
      return withInputs(({ model, publication, outputPath, render }) => {
        expect(render(base).status).toBe(0);
        const document = new JSDOM(fs.readFileSync(outputPath, "utf8")).window.document;
        const actual = [...document.querySelectorAll("a[download]")].map((link) => link.getAttribute("href"));
        expect(actual).toEqual([
          `${base}${model.packages[0].path}`,
          ...model.assets.map((asset) => `${base}${asset.downloadPath}`),
          ...artifactNames.map((name) => `${base}design-system/${name}`),
          ...model.packages.map((entry) => `${base}${entry.path}`),
          `${base}${publication.manifestPath}`,
        ]);
        expect(document.querySelector("#provenance a:not([download])").getAttribute("href")).toBe(publication.releaseUrl);
      });
    },
  );

  test.each([
    ["generic asset traversal", ({ model }) => { model.assets[0].downloadPath = "../outside.svg"; }],
    ["generic external package", ({ model }) => { model.packages[0].path = "https://elsewhere.test/kit.zip"; }],
    ["secondary Design System artifact", ({ model }) => { model.designSystem.artifacts[3].path = "design-system/%2e%2e/outside.md"; }],
    ["publication manifest", ({ publication }) => { publication.manifestPath = "//elsewhere.test/manifest.json"; }],
  ])("rejects %s before replacing an existing page", (_name, mutate) => {
    return withInputs((inputs) => {
      mutate(inputs);
      const result = inputs.render("https://cdn.example.test/identity/v1/");
      expect(result.status).not.toBe(0);
      expect(result.stderr).toMatch(/bundle-relative path/u);
      expect(fs.readFileSync(inputs.outputPath, "utf8")).toBe("existing reviewed page");
    });
  });

  test("rejects an invalid configured base before replacing an existing page", () => {
    return withInputs(({ outputPath, render }) => {
      expect(render("javascript:alert(1)").status).not.toBe(0);
      expect(fs.readFileSync(outputPath, "utf8")).toBe("existing reviewed page");
    });
  });

  test("validates an explicitly supplied optional artifact directory", () => {
    return withInputs(({ outputPath, render }) => {
      const result = render("./", [
        "--design-system-directory", expectedRoot, "--design-system-artifact-directory", "kit/%2foutside",
      ]);
      expect(result.status).not.toBe(0);
      expect(result.stderr).toMatch(/Design-system artifact directory.*bundle-relative path/u);
      expect(fs.readFileSync(outputPath, "utf8")).toBe("existing reviewed page");
    });
  });

  test("downloads the unchanged generated files through a configured HTTP directory", () => {
    return withInputs(async ({ outputPath, render }) => {
      const prefix = "/cdn/identity/v1/";
      const server = createServer((request, response) => {
        const name = request.url.slice(`${prefix}design-system/`.length);
        if (!request.url.startsWith(`${prefix}design-system/`) || !artifactNames.includes(name)) {
          response.writeHead(404).end();
          return;
        }
        response.end(fs.readFileSync(path.join(expectedRoot, name)));
      });
      server.listen(0, "127.0.0.1");
      await once(server, "listening");
      try {
        const base = `http://127.0.0.1:${server.address().port}${prefix}`;
        expect(render(base).status).toBe(0);
        const document = new JSDOM(fs.readFileSync(outputPath, "utf8")).window.document;
        const links = [...document.querySelectorAll("#design-system a[download]")];
        expect(links).toHaveLength(4);
        for (const [index, link] of links.entries()) {
          const response = await fetch(link.getAttribute("href"));
          expect(response.ok).toBe(true);
          expect(Buffer.from(await response.arrayBuffer())).toEqual(fs.readFileSync(path.join(expectedRoot, artifactNames[index])));
        }
      } finally {
        await new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
      }
    });
  });
});
