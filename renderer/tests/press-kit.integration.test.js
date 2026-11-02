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
  test.each([null, 'An approved paragraph keeps “supplied” project copy exact & reusable.'])(
    "renders generated approved material with optional paragraph %s", (paragraph) => {
    const temporaryDirectory = fs.mkdtempSync(
      path.join(os.tmpdir(), "identity-press-kit-renderer-"),
    );
    try {
      const consumerRoot = path.join(temporaryDirectory, "consumer");
      fs.cpSync(projectionSource, consumerRoot, { recursive: true });
      addPressSource(consumerRoot, { paragraph });
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
      const rights = section.querySelector('[data-asset-rights="mark"]');
      const asset = pressKit.assets[0];
      for (const value of [asset.license.spdx, asset.license.attribution,
        asset.origin.creator, asset.origin.source, asset.sha256, asset.approval.id,
        asset.usage.safeZone, asset.usage.minimumSize, ...asset.usage.restrictions]) {
        expect(rights.textContent).toContain(value);
      }
      expect(rights.textContent).toContain("Selection approval");
      for (const license of pressKit.guidance.legal.value.thirdPartyLicenses) {
        for (const value of Object.values(license)) expect(section.textContent).toContain(value);
      }
      if (paragraph !== null) {
        expect(section?.textContent).toContain(paragraph);
        expect(
          [...section.querySelectorAll("[data-copy-value]")].map((button) => button.dataset.copyValue),
        ).toContain(paragraph);
        expect(pressKit.boilerplates.find((value) => value.kind === "paragraph")?.text).toBe(paragraph);
        expect(fs.readFileSync(path.join(projectionDirectory, "press-kit.md"), "utf8")).toContain(paragraph);
      } else {
        expect(pressKit.boilerplates.some((value) => value.kind === "paragraph")).toBe(false);
        expect(section?.textContent).not.toContain("Paragraph description");
      }
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

  test.each([
    ["approved", "internal"],
    ["candidate", "internal"],
    ["rejected", "internal"],
    ["superseded", "internal"],
  ])("withholds %s/%s paragraph and profile facts from public HTML and exports", (state, visibility) => {
    const temporaryDirectory = fs.mkdtempSync(path.join(os.tmpdir(), "identity-press-kit-withheld-"));
    try {
      const consumerRoot = path.join(temporaryDirectory, "consumer");
      fs.cpSync(projectionSource, consumerRoot, { recursive: true });
      const paragraph = `Withheld ${state} paragraph must stay in canonical source.`;
      const fact = `Withheld ${state} short name must stay in canonical source.`;
      addPressSource(consumerRoot, { paragraph });
      const pressPath = path.join(consumerRoot, ".identity/guidance/press-kit.json");
      const press = JSON.parse(fs.readFileSync(pressPath, "utf8"));
      press.facts.push({
        id: "short-name",
        label: "Short name",
        value: fact,
        governance: governance("press-kit:fact:short-name", "approve-press-short-name"),
      });
      const approvalsPath = path.join(consumerRoot, ".identity/governance/approvals.json");
      const decisions = JSON.parse(fs.readFileSync(approvalsPath, "utf8"));
      decisions.decisions.push(approval("approve-press-short-name", "press-kit:fact:short-name"));
      for (const record of [press.boilerplates.at(-1), press.facts.at(-1)]) {
        const authority = record.governance;
        const decision = decisions.decisions.find((value) => value.id === authority.approval);
        authority.state = state;
        authority.visibility = visibility;
        if (state === "candidate") {
          authority.approval = null;
          authority.provenance.method = "handoff-candidate";
        } else {
          decision.status = state;
          if (state === "superseded") {
            const earlier = approval(`${decision.id}-earlier`, decision.subject);
            decisions.decisions.push(earlier);
            decision.supersedes = earlier.id;
          }
        }
      }
      writeJson(pressPath, press);
      writeJson(approvalsPath, decisions);
      const projectionDirectory = path.join(consumerRoot, "assets/identity/press-kit");
      execFileSync("python3", [renderPressKit, "--repository-root", consumerRoot,
        "--output-directory", "assets/identity/press-kit"], { cwd: repositoryRoot, stdio: "pipe" });
      const generated = JSON.parse(fs.readFileSync(path.join(projectionDirectory, "press-kit.json"), "utf8"));
      const model = JSON.parse(fs.readFileSync(rendererFixture, "utf8"));
      model.release.sourceDigest = generated.source.digest;
      model.release.immutableId = `sha256:${generated.source.digest}`;
      const modelPath = path.join(temporaryDirectory, "brand-kit.view-model.json");
      const outputPath = path.join(temporaryDirectory, "index.html");
      writeJson(modelPath, model);
      execFileSync(process.execPath, [renderStatic, "--model", modelPath, "--output", outputPath,
        "--press-kit-directory", projectionDirectory], { cwd: rendererRoot, stdio: "pipe" });

      for (const output of [outputPath, path.join(projectionDirectory, "press-kit.json"),
        path.join(projectionDirectory, "press-kit.md")]) {
        const text = fs.readFileSync(output, "utf8");
        expect(text).not.toContain(paragraph);
        expect(text).not.toContain(fact);
      }
      expect(generated.boilerplates.map((value) => value.kind)).toEqual(["long", "short"]);
      expect(generated.facts.some((value) => value.id === "short-name")).toBe(false);
      expect(fs.readFileSync(pressPath, "utf8")).toContain(paragraph);
      expect(fs.readFileSync(pressPath, "utf8")).toContain(fact);
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

  test.each([
    ["approved", "public", true],
    ["approved", "internal", false],
    ["candidate", "internal", false],
    ["rejected", "internal", false],
    ["superseded", "internal", false],
  ])("shows only approved public legal and official references: %s/%s", (state, visibility, publicRecord) => {
    const temporaryDirectory = fs.mkdtempSync(path.join(os.tmpdir(), "identity-press-kit-rights-"));
    try {
      const consumerRoot = path.join(temporaryDirectory, "consumer");
      fs.cpSync(projectionSource, consumerRoot, { recursive: true });
      addPressSource(consumerRoot);
      const { links, contact, legal } = addRightsReferences(consumerRoot, state, visibility);
      const projectionDirectory = path.join(consumerRoot, "assets/identity/press-kit");
      execFileSync("python3", [renderPressKit, "--repository-root", consumerRoot,
        "--output-directory", "assets/identity/press-kit"], { cwd: repositoryRoot, stdio: "pipe" });
      const generated = JSON.parse(fs.readFileSync(path.join(projectionDirectory, "press-kit.json"), "utf8"));
      const model = JSON.parse(fs.readFileSync(rendererFixture, "utf8"));
      model.release.sourceDigest = generated.source.digest;
      model.release.immutableId = `sha256:${generated.source.digest}`;
      const modelPath = path.join(temporaryDirectory, "brand-kit.view-model.json");
      const outputPath = path.join(temporaryDirectory, "index.html");
      writeJson(modelPath, model);
      execFileSync(process.execPath, [renderStatic, "--model", modelPath, "--output", outputPath,
        "--press-kit-directory", projectionDirectory], { cwd: rendererRoot, stdio: "pipe" });
      const html = fs.readFileSync(outputPath, "utf8");
      const section = new JSDOM(html).window.document.querySelector("#press-kit");
      const exported = [html,
        fs.readFileSync(path.join(projectionDirectory, "press-kit.json"), "utf8"),
        fs.readFileSync(path.join(projectionDirectory, "press-kit.md"), "utf8"),
      ];

      for (const link of links) {
        const anchor = [...section.querySelectorAll("a")].find((entry) => entry.textContent === link.label);
        if (publicRecord) {
          expect(anchor?.getAttribute("href")).toBe(link.url);
          expect(anchor?.hasAttribute("download")).toBe(false);
        } else {
          expect(anchor).toBeUndefined();
          for (const output of exported) {
            expect(output).not.toContain(link.label);
            expect(output).not.toContain(link.url);
          }
        }
      }
      if (publicRecord) {
        expect(section.textContent).toContain(contact.label);
        expect(section.querySelector(`a[href="${contact.value}"]`)).not.toBeNull();
        expect(section.textContent).toContain(legal.trademark);
        expect(section.textContent).toContain(legal.thirdPartyLicenses[0].attribution);
        expect(section.querySelector("[data-third-party-licenses]")).not.toBeNull();
      } else {
        for (const output of exported) {
          expect(output).not.toContain(contact.value);
          expect(output).not.toContain(legal.trademark);
          expect(output).not.toContain(legal.thirdPartyLicenses[0].attribution);
        }
        expect(section.textContent).toContain("Public legal guidance is not declared.");
      }
      expect([...section.querySelectorAll("a[download]")].map((link) => link.getAttribute("href")))
        .not.toContain("https://example.invalid/fonts/acquire-separately");
    } finally {
      fs.rmSync(temporaryDirectory, { recursive: true, force: true });
    }
  });
});

function addRightsReferences(repositoryRoot, state, visibility) {
  const pressPath = path.join(repositoryRoot, ".identity/guidance/press-kit.json");
  const usagePath = path.join(repositoryRoot, ".identity/guidance/usage.json");
  const approvalsPath = path.join(repositoryRoot, ".identity/governance/approvals.json");
  const press = JSON.parse(fs.readFileSync(pressPath, "utf8"));
  const usage = JSON.parse(fs.readFileSync(usagePath, "utf8"));
  const decisions = JSON.parse(fs.readFileSync(approvalsPath, "utf8"));
  const links = [
    ["software-license", "Software license", "documentation", "software/LICENSE"],
    ["governance", "Project governance", "documentation", "policies/governance"],
    ["conduct", "Code of Conduct", "documentation", "policies/conduct"],
    ["security", "Security reporting", "documentation", "policies/security"],
    ["contribution", "Contribution guide", "documentation", "policies/contributing"],
    ["support", "Official support", "support", "support"],
    ["community", "Official community", "other", "community"],
    ["font-acquisition", "Acquire separate Example font", "other", "fonts/acquire-separately"],
  ].map(([id, label, kind, route]) => ({
    id, label, kind, url: `https://example.invalid/${route}`,
    governance: governance(`press-kit:link:${id}`, `approve-rights-${id}`),
  }));
  const contact = {
    id: "official-support", label: "Official support contact", kind: "url",
    value: "https://example.invalid/contact/support", notes: "Contact the supplied support owner.",
    governance: governance("press-kit:contact:official-support", "approve-rights-contact"),
  };
  const legal = {
    trademark: "Supplied trademark rule: identify the project without implying endorsement.",
    copyright: "Copyright 2026 Synthetic rights example.",
    attribution: "Retain the attribution recorded for the selected asset.",
    thirdPartyLicenses: [{ name: "Separate Example font", spdx: "OFL-1.1", attribution: "Synthetic font attribution for rights filtering." }],
    governance: governance("usage:rights-example", "approve-rights-legal"),
  };
  for (const record of [...links, contact, legal]) {
    const authority = record.governance;
    const decision = approval(authority.approval, authority.subject);
    authority.state = state;
    authority.visibility = visibility;
    if (state === "candidate") {
      authority.approval = null;
      authority.provenance.method = "handoff-candidate";
    } else {
      decision.status = state;
      if (state === "superseded") {
        const earlier = approval(`${decision.id}-earlier`, decision.subject);
        decisions.decisions.push(earlier);
        decision.supersedes = earlier.id;
      }
    }
    decisions.decisions.push(decision);
  }
  press.links.push(...links);
  press.contacts.push(contact);
  usage.legal = legal;
  writeJson(pressPath, press);
  writeJson(usagePath, usage);
  writeJson(approvalsPath, decisions);
  return { links, contact, legal };
}

function addPressSource(repositoryRoot, { paragraph = null } = {}) {
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
  if (paragraph !== null) {
    records.push(["approve-press-paragraph", "press-kit:boilerplate:paragraph"]);
  }
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
  if (paragraph !== null) {
    press.boilerplates.push({
      id: "paragraph",
      kind: "paragraph",
      text: paragraph,
      governance: governance("press-kit:boilerplate:paragraph", "approve-press-paragraph"),
    });
  }
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
