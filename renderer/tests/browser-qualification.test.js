// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { afterEach, beforeEach, describe, expect, test } from "vitest";

import { installedBrowserMetadata, validateReport } from "../scripts/qualify-browser.mjs";

const screenshotTitle = "matches the reviewed desktop viewport baseline";
const approvedBaseline = fileURLToPath(new URL(
  "./e2e/__snapshots__/brand-kit-page.png", import.meta.url,
));
const png = fs.readFileSync(approvedBaseline);
const pngSha256 = crypto.createHash("sha256").update(png).digest("hex");
let temporary;
let artifactRoot;

beforeEach(() => {
  temporary = fs.mkdtempSync(path.join(os.tmpdir(), "identity-browser-report-"));
  artifactRoot = path.join(temporary, "artifacts");
  fs.mkdirSync(artifactRoot);
});

afterEach(() => {
  fs.rmSync(temporary, { recursive: true, force: true });
});

function report({ count = 1, failed = false } = {}) {
  const specs = Array.from({ length: count }, (_, index) => ({
    title: failed ? screenshotTitle : `qualified browser case ${index + 1}`,
    file: "renderer.spec.js",
    ok: !failed,
    tests: [{
      projectName: "chromium",
      expectedStatus: "passed",
      status: failed ? "unexpected" : "expected",
      results: [{
        status: failed ? "failed" : "passed",
        retry: 0,
        errors: [],
        attachments: [],
      }],
    }],
  }));
  const value = {
    config: {
      updateSnapshots: "none",
      projects: [{ name: "chromium", retries: 0, repeatEach: 1 }],
    },
    suites: [{
      title: "renderer.spec.js",
      specs: [],
      suites: [{ title: "nested suite", specs }],
    }],
    errors: [],
    stats: {
      expected: failed ? 0 : count,
      unexpected: failed ? count : 0,
      skipped: 0,
      flaky: 0,
    },
  };
  if (failed) {
    const actual = path.join(artifactRoot, "brand-kit-page-actual.png");
    const diff = path.join(artifactRoot, "brand-kit-page-diff.png");
    fs.writeFileSync(actual, png);
    fs.writeFileSync(diff, png);
    const result = specs[0].tests[0].results[0];
    const message = "Error: expect(page).toHaveScreenshot(expected) failed\n"
      + "12345 pixels (ratio 0.5 of all image pixels) are different.";
    result.error = { message };
    result.errors = [{ message }];
    result.attachments = [
      { name: "brand-kit-page-expected.png", contentType: "image/png", path: approvedBaseline },
      { name: "brand-kit-page-actual.png", contentType: "image/png", path: actual },
      { name: "brand-kit-page-diff.png", contentType: "image/png", path: diff },
    ];
  }
  return value;
}

function onlySpec(value) {
  return value.suites[0].suites[0].specs[0];
}

function negativeOptions() {
  return {
    expectedPassed: 0,
    expectedFailed: 1,
    expectedTitle: screenshotTitle,
    artifactRoot,
  };
}

describe("qualified browser report evidence", () => {
  test("resolves real frozen-install browser metadata through declared pnpm dependencies", () => {
    const profile = JSON.parse(fs.readFileSync(new URL("../../dev/browser/profile.json", import.meta.url), "utf8"));
    const { playwrightVersion, browsers } = installedBrowserMetadata();
    expect(playwrightVersion).toBe(profile.playwright);
    expect(browsers.browsers.find((browser) => browser.name === "chromium-headless-shell")).toMatchObject({
      revision: String(profile.chromium.revision), browserVersion: profile.chromium.version,
    });
  });

  test("accepts the exact nested positive suite without retries or skips", () => {
    const result = validateReport(report({ count: 6 }), {
      expectedPassed: 6,
      expectedFailed: 0,
      artifactRoot,
    });
    expect(result).toMatchObject({ passed: 6, failed: 0, skipped: 0 });
    expect(result.diffArtifacts).toEqual([]);
  });

  test("accepts a comparison failure with confined PNG evidence and canonical expected attachment", () => {
    // These copied PNGs exercise report validation; the actual visual mutation
    // and comparison are separately proven by the real browser qualification.
    const result = validateReport(report({ failed: true }), negativeOptions());
    expect(result).toMatchObject({ passed: 0, failed: 1, skipped: 0 });
    expect(result.diffArtifacts).toHaveLength(1);
    expect(result.diffArtifacts[0].sha256).toBe(pngSha256);
  });

  test("refuses a generic failed run even when image attachments exist", () => {
    const value = report({ failed: true });
    const result = onlySpec(value).tests[0].results[0];
    result.error = { message: "Navigation failed: net::ERR_CONNECTION_REFUSED" };
    result.errors = [result.error];
    expect(() => validateReport(value, negativeOptions())).toThrow();
  });

  test("refuses a runner timeout even if the error mentions a screenshot", () => {
    const value = report({ failed: true });
    onlySpec(value).tests[0].results[0].status = "timedOut";
    expect(() => validateReport(value, negativeOptions())).toThrow();
  });

  test.each([
    ["snapshot updates", (value) => { value.config.updateSnapshots = "all"; }],
    ["configured retries", (value) => { value.config.projects[0].retries = 1; }],
    ["repeated runs", (value) => { value.config.projects[0].repeatEach = 2; }],
    ["a different configured project", (value) => { value.config.projects[0].name = "firefox"; }],
    ["an extra configured project", (value) => {
      value.config.projects.push({ name: "firefox", retries: 0, repeatEach: 1 });
    }],
  ])("rejects %s even when case outcomes look successful", (_name, mutate) => {
    const value = report();
    mutate(value);
    expect(() => validateReport(value, { expectedPassed: 1, artifactRoot })).toThrow();
  });

  test.each([
    ["a different test", (value) => { onlySpec(value).title = "unrelated browser case"; }],
    ["a different project", (value) => { onlySpec(value).tests[0].projectName = "firefox"; }],
    ["an expected-failure declaration", (value) => { onlySpec(value).tests[0].expectedStatus = "failed"; }],
  ])("does not count %s as the deliberate screenshot failure", (_name, mutate) => {
    const value = report({ failed: true });
    mutate(value);
    expect(() => validateReport(value, negativeOptions())).toThrow();
  });

  test.each([
    ["a retry", (value) => { onlySpec(value).tests[0].results[0].retry = 1; }],
    ["multiple results", (value) => {
      const results = onlySpec(value).tests[0].results;
      results.push(structuredClone(results[0]));
    }],
    ["a global runner error", (value) => { value.errors.push({ message: "Worker terminated" }); }],
    ["flaky results", (value) => { value.stats.flaky = 1; }],
    ["skipped coverage", (value) => { value.stats.skipped = 1; }],
  ])("rejects %s instead of reporting a clean positive run", (_name, mutate) => {
    const value = report();
    mutate(value);
    expect(() => validateReport(value, { expectedPassed: 1, artifactRoot })).toThrow();
  });

  test("refuses missing diff evidence rather than reusing a report alone", () => {
    const value = report({ failed: true });
    fs.unlinkSync(path.join(artifactRoot, "brand-kit-page-diff.png"));
    expect(() => validateReport(value, negativeOptions())).toThrow();
  });

  test("rejects an actual/diff attachment outside the phase output directory", () => {
    const value = report({ failed: true });
    const outside = path.join(temporary, "outside.png");
    fs.writeFileSync(outside, png);
    onlySpec(value).tests[0].results[0].attachments.find(
      (attachment) => attachment.name.endsWith("-diff.png"),
    ).path = outside;
    expect(() => validateReport(value, negativeOptions())).toThrow();
  });

  test("rejects a symlink that redirects diff evidence outside the phase", () => {
    const value = report({ failed: true });
    const outside = path.join(temporary, "outside.png");
    fs.writeFileSync(outside, png);
    const diff = path.join(artifactRoot, "brand-kit-page-diff.png");
    fs.unlinkSync(diff);
    fs.symlinkSync(outside, diff, "file");
    expect(() => validateReport(value, negativeOptions())).toThrow();
  });
});
