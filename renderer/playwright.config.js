// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { readFileSync } from "node:fs";

import { defineConfig, devices } from "@playwright/test";

const profile = JSON.parse(
  readFileSync(new URL("../dev/browser/profile.json", import.meta.url), "utf8"),
);

export default defineConfig({
  testDir: "./tests/e2e",
  outputDir: "./test-results",
  snapshotPathTemplate: "{testDir}/__snapshots__/{arg}{ext}",
  fullyParallel: false,
  forbidOnly: Boolean(process.env.CI),
  retries: 0,
  updateSnapshots: "none",
  workers: 1,
  reporter: process.env.CI ? [["line"], ["html", { open: "never" }]] : "list",
  use: {
    baseURL: "http://127.0.0.1:4173",
    trace: "retain-on-failure",
  },
  webServer: {
    command: "corepack pnpm run preview -- --host 127.0.0.1 --port 4173",
    url: "http://127.0.0.1:4173",
    reuseExistingServer: false,
    timeout: 120_000,
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"], ...profile.settings },
    },
  ],
});
