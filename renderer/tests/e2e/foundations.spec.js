// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import fs from "node:fs";
import { createRequire } from "node:module";

import { expect, test } from "@playwright/test";
import { JSDOM } from "jsdom";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";

import { BrandKitPage } from "../../src/app.js";
import { createDesignSystemView } from "../../src/design-system.js";
import { deriveThemeVariables } from "../../src/model.js";

const require = createRequire(import.meta.url);

test("source-bound foundations hydrate, remain accessible, and copy actual values", async ({ page }) => {
  const read = (file) => JSON.parse(fs.readFileSync(new URL(file, import.meta.url), "utf8"));
  const model = read("../../fixtures/example.brand-kit.view-model.json");
  const handbook = read("../../../tests/fixtures/v1/valid/minimal/expected/design-system-handbook.json");
  const context = read("../../../tests/fixtures/v1/valid/minimal/expected/design-context.json");
  model.tokens = structuredClone(context.tokens);
  model.release.sourceDigest = handbook.source.digest;
  model.release.immutableId = `sha256:${handbook.source.digest}`;
  model.designSystem = createDesignSystemView({ handbook, context, artifactDirectory: "design-system" });
  const errors = [];
  const fontRequests = [];
  page.on("pageerror", (error) => errors.push(error.message));
  page.on("request", (request) => {
    if (request.resourceType() === "font") fontRequests.push(request.url());
  });
  // Exercise the optional immutable port with a real generated fixture pair.
  // The reviewed legacy model and its screenshot remain byte-preserved.
  await page.route("**/*", async (route) => {
    if (route.request().resourceType() !== "document") return route.continue();
    const response = await route.fetch();
    const document = new JSDOM(await response.text()).window.document;
    document.querySelector("#identity-brand-kit-root").innerHTML = renderToStaticMarkup(
      React.createElement(BrandKitPage, { model }),
    );
    document.querySelector("#identity-brand-kit-model").textContent = JSON.stringify(model).replaceAll("<", "\\u003c");
    document.querySelector("#identity-brand-vars").textContent = deriveThemeVariables(model);
    await route.fulfill({ response, body: `<!doctype html>\n${document.documentElement.outerHTML}` });
  });
  await page.goto("/");
  await page.evaluate(() => document.fonts.ready);
  await expect(page.locator("[data-color-pair]")).toHaveCount(1);
  await expect(page.locator("[data-color-pair]")).toContainText("18.34:1");
  await expect(page.locator("#typography")).toContainText("OFL-1.1");
  const copy = page.locator("#typography [data-copy-value]").first();
  await expect(copy).toHaveAttribute("data-copy-value", "\"Inter\", system-ui, sans-serif");
  await copy.focus();
  await copy.press("Enter");
  await expect(page.getByRole("status")).toContainText("typography.body.family copied.");
  await page.addScriptTag({ path: require.resolve("axe-core/axe.min.js") });
  const accessibility = await page.evaluate(async () => window.axe.run(document));
  expect(accessibility.violations).toEqual([]);
  await page.setViewportSize({ width: 390, height: 844 });
  expect(await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth))
    .toBeLessThanOrEqual(1);
  expect(errors).toEqual([]);
  expect(fontRequests).toEqual([]);
});
