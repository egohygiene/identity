// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import fs from "node:fs";
import http from "node:http";
import { createRequire } from "node:module";
import os from "node:os";
import path from "node:path";

import { expect, test } from "@playwright/test";

import { buildKit, unpackKitFixtures } from "../kit-fixtures.js";

const require = createRequire(import.meta.url);
let temporary;
let output;
let server;
let url;

test.beforeAll(async () => {
  temporary = fs.mkdtempSync(path.join(os.tmpdir(), "identity-complete-kit-browser-"));
  const input = path.join(temporary, "inputs");
  unpackKitFixtures(input);
  output = path.join(temporary, "site");
  buildKit(path.join(input, "expanded"), output);
  server = http.createServer((request, response) => {
    const relative = decodeURIComponent(new URL(request.url, "http://127.0.0.1").pathname);
    const file = path.resolve(output, `.${relative === "/" ? "/index.html" : relative}`);
    if (!file.startsWith(`${output}${path.sep}`) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {
      response.writeHead(404); return response.end();
    }
    const types = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".png": "image/png", ".svg": "image/svg+xml" };
    response.writeHead(200, { "Content-Type": types[path.extname(file)] || "application/octet-stream" });
    response.end(fs.readFileSync(file));
  });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  url = `http://127.0.0.1:${server.address().port}/`;
});

test.afterAll(async () => {
  server?.closeAllConnections();
  if (server) await new Promise((resolve) => server.close(resolve));
  if (temporary) fs.rmSync(temporary, { recursive: true, force: true });
});

test("the complete public kit works with and without JavaScript", async ({ page, browser }) => {
  const errors = [];
  const missing = [];
  page.on("pageerror", (error) => errors.push(error.message));
  page.on("response", (response) => { if (response.status() >= 400) missing.push(response.url()); });
  await page.goto(url);
  await expect(page.locator("[data-studio]")).toHaveCount(0);
  await page.getByRole("link", { name: "Presentation profiles", exact: true }).focus();
  await page.keyboard.press("Enter");
  await expect(page).toHaveURL(/#presentation$/u);
  const preview = page.locator("[data-presentation-profile='github'] img");
  await preview.scrollIntoViewIfNeeded();
  await expect(preview).toHaveJSProperty("naturalWidth", 1280);
  const copy = page.locator("#presentation [data-copy-label='short description']");
  await copy.focus();
  await copy.press("Enter");
  await expect(page.getByRole("status")).toContainText("short description copied.");
  for (const [name, relative] of [["Download GitHub repository Social preview", "github/social-preview.png"], ["Download asset package", "packages/brand-kit/brand-kit.zip"]]) {
    const completed = page.waitForEvent("download");
    await page.getByRole("link", { name, exact: true }).click();
    const download = await completed;
    expect(fs.readFileSync(await download.path()).equals(fs.readFileSync(path.join(output, relative)))).toBe(true);
  }
  await page.addScriptTag({ path: require.resolve("axe-core/axe.min.js") });
  expect((await page.evaluate(async () => window.axe.run(document))).violations).toEqual([]);
  await page.setViewportSize({ width: 390, height: 844 });
  expect(await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth)).toBeLessThanOrEqual(1);
  expect(errors).toEqual([]);
  expect(missing).toEqual([]);
  const context = await browser.newContext({ javaScriptEnabled: false });
  try {
    const staticPage = await context.newPage();
    await staticPage.goto(url);
    for (const id of ["logos", "colors", "typography", "press-kit", "presentation"]) {
      await expect(staticPage.locator(`#${id}`)).toBeAttached();
    }
    await expect(staticPage.locator("#press-kit")).toContainText("turns reviewed identity intent");
    await expect(staticPage.locator("[data-asset-rights='mark']").first()).toContainText("MIT");
    expect(await staticPage.locator("a[download]").count()).toBeGreaterThan(10);
  } finally { await context.close(); }
});
