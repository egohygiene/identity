// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import fs from "node:fs";
import os from "node:os";
import path from "node:path";

import { JSDOM } from "jsdom";
import { afterAll, beforeAll, describe, expect, test } from "vitest";

import { artifactPathFromUrl } from "../src/download-integrity.js";
import { inventory, jsonBytes, verifyKit } from "../lib/kit-bundle.mjs";
import { buildKit, receipt, unpackKitFixtures } from "./kit-fixtures.js";

let temporary;
beforeAll(() => {
  temporary = fs.mkdtempSync(path.join(os.tmpdir(), "identity-complete-kit-test-"));
  unpackKitFixtures(path.join(temporary, "inputs"));
});
afterAll(() => fs.rmSync(temporary, { recursive: true, force: true }));

describe("complete native consumer Brand Kit", () => {
  test.each(["minimal", "expanded", "mantle"])("builds every actual download for %s from retained generated inputs", async (name) => {
    const input = path.join(temporary, "inputs", name);
    const output = path.join(temporary, `site-${name}`);
    // Unselected and private neighbor files must never be copied into the kit.
    fs.writeFileSync(path.join(input, "native/unselected-private.txt"), "Do not distribute this neighboring file.");
    const before = await inventory(input);
    buildKit(input, output);
    expect(await inventory(input)).toEqual(before);
    const evidence = await verifyKit(output);
    expect(evidence.sourceDigest).toBe(receipt.cases[name].sourceDigest);
    const document = new JSDOM(fs.readFileSync(path.join(output, "index.html"), "utf8")).window.document;
    expect(document.querySelector("[data-studio]")).toBeNull();
    expect(document.querySelector("a[href='#studio']")).toBeNull();
    expect(fs.existsSync(path.join(output, "unselected-private.txt"))).toBe(false);
    for (const link of document.querySelectorAll("a[download]")) {
      const relative = artifactPathFromUrl(link.getAttribute("href"));
      expect(evidence.files[relative]?.bytes).toBeGreaterThan(0);
    }
    for (const id of ["press-kit", "design-system", "presentation"]) {
      expect(Boolean(document.querySelector(`#${id}`))).toBe(name === "expanded" || (id === "presentation" && name === "mantle"));
    }
    if (name === "minimal") {
      for (const id of ["logos", "voice", "usage", "creative-direction"]) expect(document.querySelector(`#${id}`)).toBeNull();
    }
    if (name === "expanded") {
      expect(document.querySelector("#press-kit").textContent).toContain("turns reviewed identity intent");
      expect(document.querySelector("#colors").textContent).toContain("contrast");
      expect(document.querySelector("#typography").textContent).toContain("Inter");
      expect(document.querySelector("[data-asset-rights='mark']").textContent).toContain("MIT");
      expect(document.querySelector(".hero__actions a[download]").textContent).toBe("Download asset package");
    }
    if (name === "mantle") {
      expect(document.querySelector("h1").textContent).toBe("Mantle");
      expect(document.querySelector("#logos").textContent).toContain("MIT");
    }
  }, 30000);

  test("repeated complete builds have identical inventories and honor an explicit deployment base", async () => {
    const input = path.join(temporary, "inputs/expanded");
    const outputs = [path.join(temporary, "repeat-a"), path.join(temporary, "repeat-b")];
    for (const output of outputs) buildKit(input, output, ["--asset-base-url", "/consumer/v1/"]);
    expect(await inventory(outputs[0])).toEqual(await inventory(outputs[1]));
    const document = new JSDOM(fs.readFileSync(path.join(outputs[0], "index.html"), "utf8")).window.document;
    for (const link of document.querySelectorAll("a[download]")) expect(link.getAttribute("href")).toMatch(/^\/consumer\/v1\//u);
    await verifyKit(outputs[0]);
  }, 30000);

  test("rejects a stale handbook and damaged native/Press Kit artifacts before creating output", () => {
    for (const kind of ["handbook", "native", "press"]) {
      const input = path.join(temporary, `bad-${kind}`);
      fs.cpSync(path.join(temporary, "inputs/expanded"), input, { recursive: true });
      if (kind === "handbook") {
        for (const file of ["design-system-handbook.json", "design-context.json"]) {
          const target = path.join(input, "handbook", file);
          const model = JSON.parse(fs.readFileSync(target, "utf8"));
          model.source.digest = "f".repeat(64);
          fs.writeFileSync(target, JSON.stringify(model));
        }
      } else fs.appendFileSync(path.join(input, kind === "native" ? "native/github/social-preview.png" : "press/press-kit.zip"), "damaged");
      const output = path.join(temporary, `bad-${kind}-output`);
      expect(() => buildKit(input, output)).toThrow();
      expect(fs.existsSync(output)).toBe(false);
    }
  }, 30000);

  test("rejects source/output overlap and preserves existing nonempty destinations", async () => {
    const input = path.join(temporary, "inputs/expanded");
    const before = await inventory(input);
    expect(() => buildKit(input, path.join(input, "native/site"))).toThrow();
    const output = path.join(temporary, "existing");
    fs.mkdirSync(output);
    fs.writeFileSync(path.join(output, "keep.txt"), "Unrelated file");
    expect(() => buildKit(input, output)).toThrow();
    expect(fs.readFileSync(path.join(output, "keep.txt"), "utf8")).toBe("Unrelated file");
    expect(await inventory(input)).toEqual(before);
  });

  test("offline verification rejects changed bytes and a self-consistent page with an unselected download", async () => {
    const output = path.join(temporary, "tampered");
    fs.cpSync(path.join(temporary, "site-expanded"), output, { recursive: true });
    const page = path.join(output, "index.html");
    fs.appendFileSync(page, '<a download href="./unselected.txt">Unselected download</a>');
    await expect(verifyKit(output)).rejects.toThrow(/inventory/u);
    const manifestPath = path.join(output, "kit.json");
    const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
    manifest.files = await inventory(output);
    fs.writeFileSync(manifestPath, jsonBytes(manifest));
    await expect(verifyKit(output)).rejects.toThrow(/absent from its selected model/u);
  });
});
