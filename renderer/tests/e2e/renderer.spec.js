// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { createRequire } from "node:module";

import { expect, test } from "@playwright/test";

const require = createRequire(import.meta.url);
const axePath = require.resolve("axe-core/axe.min.js");

test.beforeEach(async ({ page }) => {
  await page.goto("/");
  await page.evaluate(() => document.fonts.ready);
});

test("renders an accessible, linkable, downloadable static Brand Kit", async ({
  page,
  request,
}) => {
  await expect(page).toHaveTitle("Example Product Brand Kit");
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(
    "Example Product",
  );

  await page.addScriptTag({ path: axePath });
  const accessibility = await page.evaluate(async () => window.axe.run(document));
  expect(accessibility.violations).toEqual([]);

  const downloads = await page.locator("a[download]").evaluateAll((links) =>
    links.map((link) => link.href),
  );
  expect(downloads.length).toBeGreaterThanOrEqual(5);

  for (const downloadUrl of downloads) {
    const response = await request.get(downloadUrl);
    expect(response.ok(), `download failed: ${downloadUrl}`).toBe(true);
  }

  await page.getByRole("link", { name: "Color palette" }).click();
  await expect(page).toHaveURL(/#colors$/u);
  await expect(
    page.getByRole("heading", {
      level: 2,
      name: "Color palette and approved pairings",
    }),
  ).toBeInViewport();
});

test("copy feedback and theme controls remain keyboard operable", async ({
  page,
}) => {
  const copyButton = page.getByRole("button", { name: "Copy value" }).first();
  await copyButton.focus();
  await expect(copyButton).toBeFocused();
  await copyButton.press("Enter");
  await expect(page.getByRole("status")).toContainText("copied");

  const themeButton = page.getByRole("button", { name: /Change color theme/u });
  await themeButton.focus();
  await themeButton.press("Enter");
  await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  await themeButton.press("Enter");
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
});

test("studio imports a local review bundle without mutating the release", async ({ page }) => {
  const candidateBundle = {
    schema: "identity.brand-kit-candidate/v1",
    projectId: "example-product",
    sourceDigest: "545e54ad462fa84807ef594110a6742bf861bdf90a7e71fd60e1729b05d58516",
    profiles: ["social", "pwa"],
    candidates: [{
      id: "candidate-mark",
      kind: "mark",
      state: "candidate",
      provenance: { source: "local-review" },
      approvedAssetId: "mark",
    }],
  };
  await page.getByLabel("Candidate bundle JSON").fill(JSON.stringify(candidateBundle));
  await page.getByRole("button", { name: "Validate and preview plan" }).click();
  await expect(page.getByText("Candidate review · pwa, social")).toBeVisible();
  await expect(page.getByText("State: candidate. Kind: mark.")).toBeVisible();
  await expect(page.getByRole("button", { name: "Export review bundle" })).toBeEnabled();
  await page.getByLabel("Reviewer identity").fill("local reviewer");
  await page.getByLabel(/I reviewed this plan/u).check();
  await expect(page.getByRole("button", { name: "Export approved handoff" })).toBeEnabled();
});

test("honors reduced motion and remains responsive on a narrow viewport", async ({
  page,
}) => {
  await page.emulateMedia({ reducedMotion: "reduce", colorScheme: "dark" });
  await page.setViewportSize({ width: 390, height: 844 });
  await page.reload();

  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  );
  expect(overflow).toBeLessThanOrEqual(1);

  const transitionDuration = await page
    .getByRole("button", { name: "Copy value" })
    .first()
    .evaluate((element) => getComputedStyle(element).transitionDuration);
  const longestTransitionSeconds = Math.max(
    ...transitionDuration
      .split(",")
      .map((duration) => Number.parseFloat(duration.trim())),
  );
  expect(longestTransitionSeconds).toBeLessThanOrEqual(0.001);
});

test("matches the reviewed desktop viewport baseline", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.reload();
  await page.evaluate(() => document.fonts.ready);
  await expect(page).toHaveScreenshot("brand-kit-page.png", {
    animations: "disabled",
    fullPage: false,
  });
});
