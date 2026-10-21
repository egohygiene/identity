// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import fs from "node:fs";
import http from "node:http";
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { expect, test } from "@playwright/test";
import { JSDOM } from "jsdom";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";

import { BrandKitPage } from "../../src/app.js";
import { deriveThemeVariables } from "../../src/model.js";

const require = createRequire(import.meta.url);
const distRoot = path.resolve(fileURLToPath(new URL("../../dist/", import.meta.url)));
const model = JSON.parse(fs.readFileSync(new URL("../../fixtures/mantle-presentation/brand-kit.view-model.json", import.meta.url), "utf8"));
const png = fs.readFileSync(new URL("../../fixtures/mantle-presentation/github/social-preview.png", import.meta.url));
let server;
let fixtureUrl;

test.beforeAll(async () => {
  // Serve the exact native fixture and the real built renderer over HTTP.
  // Browser downloads can bypass page routing; no virtual route or mutation of
  // a running Vite server's generated tree is used for the download assertion.
  const document = new JSDOM(fs.readFileSync(path.join(distRoot, "index.html"), "utf8")).window.document;
  document.querySelector("#identity-brand-kit-root").innerHTML = renderToStaticMarkup(
    React.createElement(BrandKitPage, { model }),
  );
  document.querySelector("#identity-brand-kit-model").textContent = JSON.stringify(model).replaceAll("<", "\\u003c");
  document.querySelector("#identity-brand-vars").textContent = deriveThemeVariables(model);
  const html = `<!doctype html>\n${document.documentElement.outerHTML}`;
  const types = { ".js": "text/javascript", ".css": "text/css", ".png": "image/png", ".svg": "image/svg+xml" };
  server = http.createServer((request, response) => {
    const pathname = decodeURIComponent(new URL(request.url, "http://127.0.0.1").pathname);
    if (pathname === "/") {
      response.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
      return response.end(html);
    }
    if (pathname === "/github/social-preview.png") {
      response.writeHead(200, { "Content-Type": "image/png", "Content-Length": png.length });
      return response.end(png);
    }
    const file = path.resolve(distRoot, `.${pathname}`);
    if (!file.startsWith(`${distRoot}${path.sep}`) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {
      response.writeHead(404);
      return response.end();
    }
    response.writeHead(200, { "Content-Type": types[path.extname(file)] || "application/octet-stream" });
    response.end(fs.readFileSync(file));
  });
  await new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", resolve);
  });
  fixtureUrl = `http://127.0.0.1:${server.address().port}/`;
});

test.afterAll(async () => {
  if (!server) return;
  server.closeAllConnections();
  await new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
});

test("selected presentation preview hydrates, downloads and copies with keyboard access", async ({ page }) => {
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto(fixtureUrl);
  const section = page.locator("#presentation");
  const navigation = page.getByRole("link", { name: "Presentation profiles", exact: true });
  await navigation.focus();
  await navigation.press("Enter");
  await expect(page).toHaveURL(/#presentation$/u);
  await section.locator("img").scrollIntoViewIfNeeded();
  await expect(section.locator("img")).toHaveJSProperty("naturalWidth", 1280);
  await expect(section.locator("img")).toHaveJSProperty("naturalHeight", 640);
  const copy = section.locator("[data-copy-label='Project tagline']");
  await expect(copy).toHaveAttribute("data-copy-value", model.project.tagline);
  await copy.focus();
  await copy.press("Enter");
  await expect(page.getByRole("status")).toContainText("Project tagline copied.");
  const completed = page.waitForEvent("download");
  await section.getByRole("link", { name: "Download GitHub repository Social preview", exact: true }).click();
  const download = await completed;
  expect(download.suggestedFilename()).toBe("social-preview.png");
  expect(fs.readFileSync(await download.path()).equals(png), "Download must equal the exact native PNG bytes").toBe(true);
  const guidanceValues = page.locator(".structured-value");
  const scrollable = await guidanceValues.evaluateAll((values) => values.findIndex(
    (value) => value.scrollWidth > value.clientWidth,
  ));
  expect(scrollable).toBeGreaterThanOrEqual(0);
  const guidance = guidanceValues.nth(scrollable);
  await guidance.focus();
  await expect(guidance).toBeFocused();
  await guidance.press("ArrowRight");
  await expect.poll(() => guidance.evaluate((value) => value.scrollLeft)).toBeGreaterThan(0);
  await page.addScriptTag({ path: require.resolve("axe-core/axe.min.js") });
  const accessibility = await page.evaluate(async () => window.axe.run(document));
  expect(accessibility.violations).toEqual([]);
  await page.setViewportSize({ width: 390, height: 844 });
  expect(await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth))
    .toBeLessThanOrEqual(1);
  expect(errors).toEqual([]);
});
