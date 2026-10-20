// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { createHash } from "node:crypto";
import {
  chmodSync, existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync,
  realpathSync, statSync, writeFileSync,
} from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";
import { spawn, spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";

const rendererRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const repositoryRoot = path.resolve(rendererRoot, "..");
const profilePath = path.join(repositoryRoot, "dev/browser/profile.json");
const screenshotTitle = "matches the reviewed desktop viewport baseline";
const marker = "IDENTITY_BROWSER_RECEIPT=";
const commands = [];

const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const require = createRequire(import.meta.url);

export function installedBrowserMetadata() {
  // pnpm exposes each package's declared dependencies only from that package.
  const testPackage = require.resolve("@playwright/test/package.json");
  const testRequire = createRequire(testPackage);
  const playwrightRequire = createRequire(testRequire.resolve("playwright/package.json"));
  const corePackage = playwrightRequire.resolve("playwright-core/package.json");
  return {
    playwrightVersion: JSON.parse(readFileSync(testPackage, "utf8")).version,
    browsers: JSON.parse(readFileSync(path.join(path.dirname(corePackage), "browsers.json"), "utf8")),
  };
}

function inside(root, candidate) {
  const relative = path.relative(root, candidate);
  return relative === "" || (!relative.startsWith(`..${path.sep}`) && relative !== ".." && !path.isAbsolute(relative));
}

function artifact(file, root) {
  const resolved = realpathSync(file);
  if (!inside(realpathSync(root), resolved) || !statSync(resolved).isFile()) {
    throw new Error("A browser artifact escapes its fresh phase directory");
  }
  const bytes = readFileSync(resolved);
  if (bytes.length < 24 || !bytes.subarray(0, 8).equals(Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]))) {
    throw new Error("Screenshot evidence must contain a nonempty PNG artifact");
  }
  return { path: path.relative(root, resolved).split(path.sep).join("/"), sha256: sha256(bytes) };
}

function flatten(suites) {
  return suites.flatMap((suite) => [
    ...(suite.specs ?? []).flatMap((spec) => (spec.tests ?? []).map((test) => ({ spec, test }))),
    ...flatten(suite.suites ?? []),
  ]);
}

export function validateReport(report, { expectedPassed, expectedFailed = 0, expectedTitle = null, artifactRoot }) {
  const projects = report.config?.projects;
  if (report.config?.updateSnapshots !== "none" || projects?.length !== 1 ||
      projects[0].name !== "chromium" || projects[0].retries !== 0 || projects[0].repeatEach !== 1) {
    throw new Error("Browser evidence must disable snapshot updates, retries and repetition in one Chromium project");
  }
  if (!Array.isArray(report.suites) || (report.errors ?? []).length !== 0) {
    throw new Error("Browser qualification has missing suites or global runner errors");
  }
  const tests = flatten(report.suites);
  if (tests.length !== expectedPassed + expectedFailed || tests.length === 0) {
    throw new Error("Browser qualification did not execute the exact intended case count");
  }
  const expectedStats = { expected: expectedPassed, unexpected: expectedFailed, skipped: 0, flaky: 0 };
  for (const [name, value] of Object.entries(expectedStats)) {
    if (report.stats?.[name] !== value) throw new Error(`Unexpected browser report ${name} count`);
  }
  let passed = 0;
  let failed = 0;
  const diffArtifacts = [];
  for (const { spec, test } of tests) {
    if (test.projectName !== "chromium" || test.expectedStatus !== "passed" || test.results?.length !== 1) {
      throw new Error("Browser evidence must use the unmodified Chromium cases without expected failures or retries");
    }
    const result = test.results[0];
    if (result.retry !== 0) throw new Error("A retried browser case is not qualification evidence");
    if (expectedTitle !== null && spec.title !== expectedTitle) throw new Error("The visual probe selected another test");
    if (result.status === "passed" && test.status === "expected") {
      passed += 1;
    } else if (result.status === "failed" && test.status === "unexpected" && expectedFailed === 1) {
      if (spec.title !== screenshotTitle) throw new Error("An unrelated failure is not visual drift proof");
      const messages = [result.error, ...(result.errors ?? [])].filter(Boolean).map((error) => error.message ?? "").join("\n");
      if (!messages.includes("toHaveScreenshot") || !/pixel|screenshot comparison/iu.test(messages)) {
        throw new Error("The negative probe did not fail a screenshot pixel comparison");
      }
      const attachments = result.attachments ?? [];
      const actual = attachments.filter((item) => item.name.endsWith("-actual.png") && item.path);
      const diffs = attachments.filter((item) => item.name.endsWith("-diff.png") && item.path);
      if (actual.length !== 1 || diffs.length !== 1) throw new Error("The visual failure lacks its actual/diff PNG evidence");
      artifact(actual[0].path, artifactRoot);
      diffArtifacts.push(artifact(diffs[0].path, artifactRoot));
      failed += 1;
    } else {
      throw new Error("Skipped, flaky, timed-out or unrelated failed cases are not browser qualification");
    }
  }
  if (passed !== expectedPassed || failed !== expectedFailed) throw new Error("Browser result statuses differ from the intended proof");
  return { passed, failed, skipped: 0, diffArtifacts };
}

function outputDirectory(argument) {
  if (!path.isAbsolute(argument)) throw new Error("--output-directory must be absolute and outside the checkout");
  let ancestor = argument;
  const suffix = [];
  while (!existsSync(ancestor)) {
    suffix.unshift(path.basename(ancestor));
    ancestor = path.dirname(ancestor);
  }
  const resolved = path.join(realpathSync(ancestor), ...suffix);
  if (inside(realpathSync(repositoryRoot), resolved)) throw new Error("Browser evidence cannot overwrite repository source");
  if (existsSync(resolved) && !statSync(resolved).isDirectory()) throw new Error("Browser output must be a directory");
  if (existsSync(path.join(resolved, "qualification.json"))) throw new Error("Use a fresh output directory; prior qualification evidence is preserved");
  mkdirSync(resolved, { recursive: true });
  return realpathSync(resolved);
}

function checked(command, arguments_, options = {}) {
  const result = spawnSync(command, arguments_, {
    cwd: rendererRoot, encoding: "utf8", timeout: 240_000,
    env: { ...process.env, CI: "1", TZ: "UTC" }, ...options,
  });
  commands.push({ command: [command, ...arguments_], exitCode: result.status, signal: result.signal, outputSha256: sha256((result.stdout ?? "") + (result.stderr ?? "")) });
  if (result.error || result.signal || result.status !== 0) {
    throw new Error(`Required browser command failed: ${command} (exit ${result.status})\n${result.stderr ?? ""}`);
  }
  return ((result.stdout ?? "") + (result.stderr ?? "")).trim();
}

function baselineGuard(profile) {
  const baseline = path.resolve(repositoryRoot, profile.baseline.path);
  if (!inside(repositoryRoot, baseline) || !inside(realpathSync(repositoryRoot), realpathSync(baseline))) {
    throw new Error("The reviewed baseline must remain inside the repository");
  }
  if (sha256(readFileSync(baseline)) !== profile.baseline.sha256) throw new Error("The approved screenshot baseline is missing or changed");
  return baseline;
}

function phase(name, runRoot, profile, { passed, failed = 0, title = null }) {
  baselineGuard(profile);
  const directory = path.join(runRoot, name);
  mkdirSync(directory);
  const report = path.join(directory, "report.json");
  const artifacts = path.join(directory, "artifacts");
  const args = ["pnpm", "exec", "playwright", "test", "--project=chromium", "--retries=0", "--reporter=json", "--update-snapshots=none", `--output=${artifacts}`];
  // Playwright grep matches the full project/file/title string.
  if (title !== null) args.push("--grep", `${title}$`);
  const result = spawnSync("corepack", args, {
    cwd: rendererRoot, encoding: "utf8", timeout: 240_000,
    env: { ...process.env, CI: "1", TZ: "UTC", PLAYWRIGHT_JSON_OUTPUT_FILE: report },
  });
  const output = (result.stdout ?? "") + (result.stderr ?? "");
  writeFileSync(path.join(directory, "command.log"), output);
  commands.push({ command: ["corepack", ...args], exitCode: result.status, signal: result.signal, outputSha256: sha256(output) });
  baselineGuard(profile);
  if (result.error || result.signal || result.status !== (failed ? 1 : 0)) {
    throw new Error(`The ${name} browser phase had an unexpected process outcome (exit ${result.status})\n${output.slice(-6000)}`);
  }
  const parsed = JSON.parse(readFileSync(report, "utf8"));
  const summary = validateReport(parsed, { expectedPassed: passed, expectedFailed: failed, expectedTitle: title, artifactRoot: artifacts });
  return {
    exitCode: result.status, ...summary,
    report: path.relative(path.dirname(runRoot), report).split(path.sep).join("/"),
    diffArtifacts: summary.diffArtifacts.map((item) => ({ ...item, path: path.relative(path.dirname(runRoot), path.join(artifacts, item.path)).split(path.sep).join("/") })),
  };
}

function inventory(paths) {
  const files = new Set();
  const visited = new Set();
  function walk(file) {
    const resolved = realpathSync(file);
    if (visited.has(resolved)) return;
    visited.add(resolved);
    if (statSync(resolved).isDirectory()) {
      for (const entry of readdirSync(resolved).sort()) walk(path.join(resolved, entry));
    } else if (statSync(resolved).isFile()) files.add(resolved);
  }
  for (const item of paths) walk(item);
  return [...files].sort().map((file) => ({ path: file, sha256: sha256(readFileSync(file)) }));
}

async function browserEvidence(profile, runRoot) {
  const { chromium, devices } = await import("@playwright/test");
  const server = spawn(process.execPath, [path.join(rendererRoot, "node_modules/vite/bin/vite.js"), "preview", "--host", "127.0.0.1", "--port", "4173", "--strictPort"], {
    cwd: rendererRoot, env: { ...process.env, CI: "1", TZ: "UTC" }, stdio: ["ignore", "pipe", "pipe"],
  });
  let serverLog = "";
  server.stdout.on("data", (data) => { serverLog = (serverLog + data).slice(-100_000); });
  server.stderr.on("data", (data) => { serverLog = (serverLog + data).slice(-100_000); });
  let browser;
  try {
    let ready = false;
    for (let attempt = 0; attempt < 100; attempt += 1) {
      if (server.exitCode !== null || server.signalCode !== null) throw new Error(`Qualification preview failed: ${serverLog}`);
      if (serverLog.includes("http://127.0.0.1:4173/")) {
        try { const response = await fetch("http://127.0.0.1:4173", { signal: AbortSignal.timeout(1000) }); ready = response.ok; } catch { /* Await only this owned preview. */ }
      }
      if (ready) break;
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
    if (!ready) throw new Error("Qualification preview did not become ready");
    browser = await chromium.launch({ headless: true });
    if (browser.version() !== profile.chromium.version) throw new Error("The launched Chromium version differs from the qualified profile");
    const browserSession = await browser.newBrowserCDPSession();
    const commandLine = (await browserSession.send("Browser.getBrowserCommandLine")).arguments;
    if (!commandLine.includes("--force-color-profile=srgb")) throw new Error("The actual browser lacks the qualified sRGB rendering flag");
    const executable = realpathSync(commandLine[0]);
    if (!executable.startsWith(`/ms-playwright/chromium_headless_shell-${profile.chromium.revision}/`)) {
      throw new Error("The actual executable is not the profile's image-owned Chromium headless shell");
    }
    const context = await browser.newContext({ ...devices["Desktop Chrome"], ...profile.settings });
    const page = await context.newPage();
    await page.goto("http://127.0.0.1:4173");
    await page.evaluate(() => document.fonts.ready);
    const settings = await page.evaluate(() => ({
      locale: navigator.language, timezoneId: Intl.DateTimeFormat().resolvedOptions().timeZone,
      deviceScaleFactor: devicePixelRatio, colorScheme: matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light",
      reducedMotion: matchMedia("(prefers-reduced-motion: reduce)").matches ? "reduce" : "no-preference",
      viewport: { width: innerWidth, height: innerHeight }, colorDepth: screen.colorDepth,
    }));
    for (const [name, value] of Object.entries(profile.settings)) {
      if (JSON.stringify(settings[name]) !== JSON.stringify(value)) throw new Error(`Actual browser ${name} differs from the qualified profile`);
    }
    const session = await context.newCDPSession(page);
    await session.send("DOM.enable");
    await session.send("CSS.enable");
    const rootNode = (await session.send("DOM.getDocument")).root.nodeId;
    const renderedFonts = [];
    for (const selector of ["body", "h1", ".token-value", ".studio textarea"]) {
      const { nodeId } = await session.send("DOM.querySelector", { nodeId: rootNode, selector });
      if (!nodeId) throw new Error(`The qualification fixture lacks ${selector}`);
      renderedFonts.push({
        selector, declaredFamily: await page.locator(selector).first().evaluate((element) => getComputedStyle(element).fontFamily),
        fonts: (await session.send("CSS.getPlatformFontsForNode", { nodeId })).fonts,
      });
    }
    if (!renderedFonts.some((entry) => entry.fonts.some((font) => font.glyphCount > 0))) {
      throw new Error("The browser did not resolve any rendered platform fonts for the fixture");
    }
    return {
      version: browser.version(), executable, executableSha256: sha256(readFileSync(executable)),
      commandLine: commandLine.map((value) => value.startsWith("--user-data-dir=") ? "--user-data-dir=<disposable-browser-profile>" : value),
      settings, renderedFonts,
    };
  } finally {
    if (browser) await browser.close();
    if (server.exitCode === null) {
      const stopped = new Promise((resolve) => server.once("exit", resolve));
      server.kill("SIGTERM");
      await Promise.race([stopped, new Promise((resolve) => setTimeout(resolve, 5000))]);
      if (server.exitCode === null) { server.kill("SIGKILL"); await stopped; }
    }
    writeFileSync(path.join(runRoot, "preview.log"), serverLog);
  }
}

async function main(arguments_) {
  if (arguments_.length !== 2 || arguments_[0] !== "--output-directory") throw new Error("Usage: node scripts/qualify-browser.mjs --output-directory /evidence");
  const output = outputDirectory(arguments_[1]);
  const runRoot = mkdtempSync(path.join(output, "browser-"));
  // This directory contains only public synthetic evidence and must be readable
  // by the host artifact collector when the container runs as root.
  chmodSync(runRoot, 0o755);
  const receipt = { kind: "dated browser environment qualification receipt", status: "failed", platform: "linux/amd64", observedAt: new Date().toISOString(), commands };
  let profile;
  try {
    profile = JSON.parse(readFileSync(profilePath, "utf8"));
    if (process.platform !== "linux" || process.arch !== "x64" || profile.platform !== "linux/amd64") throw new Error("This browser qualification is limited to Linux/amd64");
    if (process.env.FONTCONFIG_FILE || process.env.FONTCONFIG_PATH) throw new Error("The default qualified image does not permit a host Fontconfig override");
    baselineGuard(profile);
    receipt.baseline = { ...profile.baseline, unchanged: false };
    receipt.profileSha256 = sha256(readFileSync(profilePath));
    const package_ = JSON.parse(readFileSync(path.join(rendererRoot, "package.json"), "utf8"));
    const { playwrightVersion, browsers } = installedBrowserMetadata();
    const shell = browsers.browsers.find((browser) => browser.name === "chromium-headless-shell");
    if (playwrightVersion !== profile.playwright || package_.packageManager !== profile.packageManager || shell.revision !== String(profile.chromium.revision) || shell.browserVersion !== profile.chromium.version) {
      throw new Error("Installed browser/package pins differ from the qualification profile");
    }
    const pnpm = checked("corepack", ["pnpm", "--version"]);
    if (`pnpm@${pnpm}` !== profile.packageManager) throw new Error("Activated pnpm differs from the renderer pin");
    receipt.runtimes = { node: process.version, pnpm, playwright: playwrightVersion, osRelease: readFileSync("/etc/os-release", "utf8"), fontconfig: checked("fc-cache", ["--version"]) };
    receipt.settings = profile.settings;
    receipt.source = Object.fromEntries([
      "dev/browser/profile.json", "renderer/package.json", "renderer/pnpm-lock.yaml", "renderer/playwright.config.js",
      "renderer/scripts/qualify-browser.mjs", "renderer/scripts/render-static.mjs", "renderer/src/styles.css",
      "renderer/tests/e2e/renderer.spec.js", profile.baseline.path,
    ].map((file) => [file, sha256(readFileSync(path.join(repositoryRoot, file)))]));
    receipt.positive = phase("positive", runRoot, profile, { passed: 6 });
    const cssFiles = readdirSync(path.join(rendererRoot, "dist/assets")).filter((file) => file.endsWith(".css"));
    if (cssFiles.length !== 1) throw new Error("The visual mutation requires one unambiguous built CSS file");
    const cssPath = path.join(rendererRoot, "dist/assets", cssFiles[0]);
    const originalCss = readFileSync(cssPath);
    try {
      writeFileSync(cssPath, Buffer.concat([originalCss, Buffer.from("\nhtml { filter: invert(1) !important; }\n")]));
      receipt.negative = {
        ...phase("negative", runRoot, profile, { passed: 0, failed: 1, title: screenshotTitle }),
        expectedFailure: "screenshot-comparison", baselineUnchanged: true,
      };
    } finally {
      writeFileSync(cssPath, originalCss);
      if (sha256(readFileSync(cssPath)) !== sha256(originalCss)) throw new Error("The disposable visual mutation could not be restored");
      baselineGuard(profile);
    }
    receipt.restored = phase("restored", runRoot, profile, { passed: 1, title: screenshotTitle });
    receipt.browser = await browserEvidence(profile, runRoot);
    const fontFiles = [...new Set(checked("fc-list", ["--format", "%{file}\n"]).split("\n").filter(Boolean))];
    if (fontFiles.length === 0) throw new Error("The qualified image has no Fontconfig font inventory");
    receipt.fonts = {
      files: inventory(fontFiles), configuration: inventory(["/etc/fonts", "/usr/share/fontconfig"]),
      activeConfiguration: checked("fc-conflist", []),
      resolutions: Object.fromEntries(["Inter", "system-ui", "sans-serif", "monospace", "Liberation Mono"].map((family) => [family, checked("fc-match", ["--format", "%{family}\t%{file}\n", family])])),
    };
    baselineGuard(profile);
    receipt.baseline.unchanged = true;
    receipt.status = "passed";
    receipt.limits = ["Only the recorded Linux/amd64 image and immutable source inputs are qualified.", "The deliberately changed built CSS is disposable and restored; no baseline regeneration or tolerance relaxation occurs.", "Automated browser evidence does not supply human creative approval or complete accessibility conformance."];
  } catch (error) {
    receipt.failure = error.message;
    if (profile) {
      try { baselineGuard(profile); receipt.baseline = { ...profile.baseline, unchanged: true }; } catch { receipt.baseline = { ...profile.baseline, unchanged: false }; }
    }
  }
  writeFileSync(path.join(output, "qualification.json"), `${JSON.stringify(receipt, null, 2)}\n`);
  console.log(marker + JSON.stringify(receipt));
  return receipt.status === "passed" ? 0 : 1;
}

if (process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url) {
  try { process.exitCode = await main(process.argv.slice(2)); } catch (error) { console.error(error.message); process.exitCode = 2; }
}
