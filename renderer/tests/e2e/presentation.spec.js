// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import fs from "node:fs";
import { createRequire } from "node:module";

import { expect, test } from "@playwright/test";
import { JSDOM } from "jsdom";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";

import { BrandKitPage } from "../../src/app.js";
import { deriveThemeVariables } from "../../src/model.js";

const require = createRequire(import.meta.url);

test("selected presentation preview hydrates, downloads and copies with keyboard access", async ({ page }) => {
  // Exact native output from unchanged Mantle source, bound by the #104 receipt.
  const model = JSON.parse(fs.readFileSync(new URL("../../fixtures/mantle-presentation/brand-kit.view-model.json", import.meta.url), "utf8"));
  const png = fs.readFileSync(new URL("../../fixtures/mantle-presentation/github/social-preview.png", import.meta.url));
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.route("**/*", async (route) => {
    if (new URL(route.request().url()).pathname === "/github/social-preview.png") {
      return route.fulfill({ contentType: "image/png", body: png });
    }
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
  const section = page.locator("#presentation");
  const navigation = page.getByRole("link", { name: "Presentation profiles", exact: true });
  await navigation.focus();
  await navigation.press("Enter");
  await expect(page).toHaveURL(/#presentation$/u);
  await expect(section.locator("img")).toHaveJSProperty("naturalWidth", 1280);
  await expect(section.locator("img")).toHaveJSProperty("naturalHeight", 640);
  const copy = section.locator("[data-copy-label='Project tagline']");
  await expect(copy).toHaveAttribute("data-copy-value", model.project.tagline);
  await copy.focus();
  await copy.press("Enter");
  await expect(page.getByRole("status")).toContainText("Project tagline copied.");
  const completed = page.waitForEvent("download");
  await section.getByRole("link", { name: "Download GitHub repository preview", exact: true }).click();
  const download = await completed;
  expect(download.suggestedFilename()).toBe("social-preview.png");
  expect(fs.readFileSync(await download.path())).toEqual(png);
  await page.addScriptTag({ path: require.resolve("axe-core/axe.min.js") });
  const accessibility = await page.evaluate(async () => window.axe.run(document));
  expect(accessibility.violations).toEqual([]);
  await page.setViewportSize({ width: 390, height: 844 });
  expect(await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth))
    .toBeLessThanOrEqual(1);
  expect(errors).toEqual([]);
});
