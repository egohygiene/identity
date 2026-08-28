// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { JSDOM } from "jsdom";
import { describe, expect, test } from "vitest";

import { assertBrandKitViewModel } from "../src/model.js";
import { createPressKitView } from "../src/press-kit.js";

const testDirectory = path.dirname(fileURLToPath(import.meta.url));
const rendererRoot = path.resolve(testDirectory, "..");
const repositoryRoot = path.resolve(rendererRoot, "..");
const projectionSource = path.join(
  repositoryRoot,
  "tests/fixtures/v1/valid/minimal",
);
const rendererFixture = path.join(
  rendererRoot,
  "fixtures/example.brand-kit.view-model.json",
);
const renderStatic = path.join(rendererRoot, "scripts/render-static.mjs");
const renderPressKit = path.join(repositoryRoot, "scripts/render_press_kit.py");

describe("generated Press Kit renderer handoff", () => {
  test("renders generated approved material without hard-coded project facts", () => {
    const temporaryDirectory = fs.mkdtempSync(
      path.join(os.tmpdir(), "identity-press-kit-renderer-"),
    );
    try {
      const consumerRoot = path.join(temporaryDirectory, "consumer");
      fs.cpSync(projectionSource, consumerRoot, { recursive: true });
      addPressSource(consumerRoot);
      const projectionDirectory = path.join(
        consumerRoot,
        "assets/identity/press-kit",
      );
      const outputPath = path.join(temporaryDirectory, "index.html");
      const modelPath = path.join(temporaryDirectory, "brand-kit.view-model.json");

      execFileSync(
        "python3",
        [
          renderPressKit,
          "--repository-root",
          consumerRoot,
          "--output-directory",
          "assets/identity/press-kit",
        ],
        { cwd: repositoryRoot, stdio: "pipe" },
      );
      const pressKit = JSON.parse(
        fs.readFileSync(path.join(projectionDirectory, "press-kit.json"), "utf8"),
      );
      const model = JSON.parse(fs.readFileSync(rendererFixture, "utf8"));
      model.release.sourceDigest = pressKit.source.digest;
      model.release.immutableId = `sha256:${pressKit.source.digest}`;
      fs.writeFileSync(modelPath, `${JSON.stringify(model, null, 2)}\n`, "utf8");
      execFileSync(
        process.execPath,
        [
          renderStatic,
          "--model",
          modelPath,
          "--output",
          outputPath,
          "--press-kit-directory",
          projectionDirectory,
          "--press-kit-artifact-directory",
          "press-kit",
        ],
        { cwd: rendererRoot, stdio: "pipe" },
      );

      const document = new JSDOM(fs.readFileSync(outputPath, "utf8")).window
        .document;
      const section = document.querySelector("#press-kit");
      const downloadPaths = [
        ...document.querySelectorAll("#press-kit a[download]"),
      ].map((link) => link.getAttribute("href"));

      expect(section?.textContent).toContain("Example Product");
      expect(section?.textContent).toContain("turns reviewed identity intent");
      expect(section?.textContent).toContain("Example Maintainer");
      expect(downloadPaths).toEqual([
        "./press-kit/assets/example-product-mark.svg",
        "./press-kit/press-kit.json",
        "./press-kit/press-kit.md",
        "./press-kit/press-kit-manifest.json",
        "./press-kit/SHA256SUMS",
        "./press-kit/press-kit.zip",
      ]);
      expect(section?.textContent).not.toContain("Ego Hygiene");
    } finally {
      fs.rmSync(temporaryDirectory, { recursive: true, force: true });
    }
  });

  test("refuses a Press Kit for a different immutable Brand Kit project", () => {
    const temporaryDirectory = fs.mkdtempSync(
      path.join(os.tmpdir(), "identity-press-kit-project-mismatch-"),
    );
    try {
      const consumerRoot = path.join(temporaryDirectory, "consumer");
      fs.cpSync(projectionSource, consumerRoot, { recursive: true });
      addPressSource(consumerRoot);
      execFileSync(
        "python3",
        [
          renderPressKit,
          "--repository-root",
          consumerRoot,
          "--output-directory",
          "assets/identity/press-kit",
        ],
        { cwd: repositoryRoot, stdio: "pipe" },
      );
      const pressKit = JSON.parse(
        fs.readFileSync(
          path.join(consumerRoot, "assets/identity/press-kit/press-kit.json"),
          "utf8",
        ),
      );
      pressKit.project.id = "other-product";
      const model = JSON.parse(fs.readFileSync(rendererFixture, "utf8"));
      model.release.sourceDigest = pressKit.source.digest;
      model.release.immutableId = `sha256:${pressKit.source.digest}`;
      model.pressKit = createPressKitView({
        pressKit,
        artifactDirectory: "press-kit",
      });

      expect(() => assertBrandKitViewModel(model)).toThrow(
        "Press Kit project must match",
      );
    } finally {
      fs.rmSync(temporaryDirectory, { recursive: true, force: true });
    }
  });
});

function addPressSource(repositoryRoot) {
  const identityPath = path.join(repositoryRoot, ".identity/identity.json");
  const identity = JSON.parse(fs.readFileSync(identityPath, "utf8"));
  identity.documents.pressKit = ".identity/guidance/press-kit.json";
  writeJson(identityPath, identity);

  const approvalsPath = path.join(
    repositoryRoot,
    ".identity/governance/approvals.json",
  );
  const approvals = JSON.parse(fs.readFileSync(approvalsPath, "utf8"));
  const records = [
    ["approve-press-short", "press-kit:boilerplate:short"],
    ["approve-press-long", "press-kit:boilerplate:long"],
    ["approve-press-fact", "press-kit:fact:availability"],
    ["approve-press-link", "press-kit:link:repository"],
    ["approve-press-contact", "press-kit:contact:media"],
    ["approve-press-team", "press-kit:team:maintainer"],
    ["approve-press-asset", "press-kit:asset:mark"],
  ];
  approvals.decisions.push(
    ...records.map(([id, subject]) => approval(id, subject)),
  );
  writeJson(approvalsPath, approvals);

  const press = {
    $schema: "../../../../../contracts/v1/press-kit.schema.json",
    schema: "identity.press-kit-source/v1",
    boilerplates: [
      {
        id: "short",
        kind: "short",
        text: "Example Product turns reviewed identity intent into reusable, deterministic artifacts.",
        governance: governance(
          "press-kit:boilerplate:short",
          "approve-press-short",
        ),
      },
      {
        id: "long",
        kind: "long",
        text: "Example Product is a local-first Identity workflow for maintainers who need approved tokens, assets, and guidance without splitting brand truth across hand-maintained folders.",
        governance: governance(
          "press-kit:boilerplate:long",
          "approve-press-long",
        ),
      },
    ],
    facts: [
      {
        id: "availability",
        label: "Availability",
        value: "Open source and available to repository maintainers.",
        governance: governance("press-kit:fact:availability", "approve-press-fact"),
      },
    ],
    links: [
      {
        id: "repository",
        label: "Project repository",
        url: "https://example.invalid/example-product",
        kind: "repository",
        governance: governance("press-kit:link:repository", "approve-press-link"),
      },
    ],
    contacts: [
      {
        id: "media",
        label: "Media contact",
        kind: "email",
        value: "press@example.invalid",
        notes: "Please include the requested publication date and deadline.",
        governance: governance("press-kit:contact:media", "approve-press-contact"),
      },
    ],
    team: [
      {
        id: "maintainer",
        name: "Example Maintainer",
        role: "Project maintainer",
        bio: "Maintains the reviewed source and release boundaries for Example Product.",
        governance: governance("press-kit:team:maintainer", "approve-press-team"),
      },
    ],
    assets: [
      {
        id: "mark",
        assetId: "mark",
        label: "Primary mark",
        notes: "Use with the accompanying approved usage guidance.",
        governance: governance("press-kit:asset:mark", "approve-press-asset"),
      },
    ],
  };
  writeJson(path.join(repositoryRoot, ".identity/guidance/press-kit.json"), press);
}

function approval(id, subject) {
  return {
    id,
    subject,
    candidate: `press-kit:${id}/v1`,
    status: "approved",
    reviewedBy: "example-maintainer",
    reviewedAt: "2026-08-28T18:00:00Z",
    evidence: `https://example.invalid/reviews/${id}`,
    supersedes: null,
    notes: "Approved for the public Press Kit fixture.",
  };
}

function governance(subject, approvalId) {
  return {
    subject,
    state: "approved",
    visibility: "public",
    provenance: {
      method: "human-authored",
      source: ".identity/brief.md",
      capturedAt: "2026-08-28T18:00:00Z",
    },
    approval: approvalId,
  };
}

function writeJson(filePath, value) {
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}
