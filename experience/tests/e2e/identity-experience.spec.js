import { expect, test } from "@playwright/test";
import axe from "axe-core";
import { readFile } from "node:fs/promises";
import path from "node:path";

async function expectNoSeriousAccessibilityViolations(page) {
  await page.addScriptTag({ content: axe.source });
  const result = await page.evaluate(async () => globalThis.axe.run(document));
  const blocking = result.violations.filter((violation) =>
    ["serious", "critical"].includes(violation.impact),
  );
  expect(blocking).toEqual([]);
}

test("landing remains readable, keyboard navigable, and accessible", async ({ page }) => {
  await page.goto("/identity/");
  const publication = await page.request.get("/identity/publication.json");
  const evidence = await publication.json();

  await expect(page.locator("h1")).toHaveText("Carry intent all the way to the artifact.");
  await expect(page.getByText(`Release ${evidence.release.tag}`, { exact: true })).toBeVisible();
  await expect(
    page.getByText(`Commit ${evidence.release.commit.slice(0, 12)}`, { exact: true }),
  ).toBeVisible();
  await expect(page.locator('img[src*="kern-full.png"]')).toHaveAttribute(
    "alt",
    "Kern, Identity's hooded guide, floats with open hands, three warm-white glowing eyes, and a luminous diamond kernel set into his charcoal and violet robes.",
  );

  await page.keyboard.press("Tab");
  const skipLink = page.getByRole("link", { name: "Skip to content" });
  await expect(skipLink).toBeFocused();
  await expect(skipLink).toBeVisible();
  await expectNoSeriousAccessibilityViolations(page);
});

test("static landing remains complete without JavaScript", async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false, colorScheme: "dark" });
  const page = await context.newPage();
  await page.goto("/identity/");

  await expect(page.locator("main")).toContainText("Brand truth that survives the framework.");
  await expect(page.locator("main")).toContainText("Every transformation leaves evidence.");
  await expect(page.getByRole("link", { name: "Read the documentation" })).toHaveAttribute(
    "href",
    "/identity/docs/",
  );
  await context.close();
});

test("reduced motion and high contrast preserve the approved static mascot", async ({ page }) => {
  await page.emulateMedia({ reducedMotion: "reduce", contrast: "more", colorScheme: "dark" });
  await page.goto("/identity/");

  const mascot = page.locator('img[src*="kern-full.png"]');
  await expect(mascot).toBeVisible();
  const motion = await mascot.evaluate((element) => {
    const style = getComputedStyle(element);
    return { animation: style.animationName, duration: style.animationDuration };
  });
  expect(motion.animation).toBe("none");
  const durationSeconds = motion.duration.endsWith("ms")
    ? Number.parseFloat(motion.duration) / 1000
    : Number.parseFloat(motion.duration);
  expect(durationSeconds).toBeLessThanOrEqual(0.000001);
  await expectNoSeriousAccessibilityViolations(page);
});

test("Zensical documentation is linked, local, and accessible", async ({ page }) => {
  await page.goto("/identity/docs/");

  await expect(page.locator("h1")).toContainText("Identity documentation");
  await expect(page.getByRole("link", { name: "Kern", exact: true }).first()).toHaveAttribute(
    "href",
    "kern/",
  );
  await expect(page.locator('meta[content="zensical-0.0.57"]')).toHaveCount(1);
  await expect(page.locator('meta[content="Holon docs-zensical@1.0.0"]')).toHaveCount(1);
  await expectNoSeriousAccessibilityViolations(page);
});

test("architecture and legal surfaces remain direct and accessible", async ({ page }) => {
  await page.goto("/identity/architecture/");
  await expect(page.locator("h1")).toContainText("Identity publication architecture");
  await expect(page.getByText("ADR-017", { exact: false }).first()).toBeVisible();
  await expectNoSeriousAccessibilityViolations(page);

  await page.goto("/identity/legal/");
  await expect(page.locator("h1")).toContainText("Identity legal and trust");
  await expect(page.getByRole("link", { name: "Accessibility", exact: true }).first()).toHaveAttribute(
    "href",
    "accessibility/",
  );
  await expectNoSeriousAccessibilityViolations(page);
});

test("reviewed visual baselines remain stable", async ({ browserName, page }) => {
  test.skip(browserName !== "chromium", "Visual baselines use the pinned Chromium renderer.");
  const baseline = JSON.parse(
    await readFile(new URL("../../visual-baselines.json", import.meta.url), "utf8"),
  );
  for (const evidence of baseline.browserEvidence) {
    await page.setViewportSize({ width: evidence.width, height: evidence.height });
    await page.goto(evidence.route);
    await page.screenshot({
      path: path.join("test-results", "visual", `${evidence.id}.png`),
      fullPage: true,
      animations: "disabled",
    });
  }
});
