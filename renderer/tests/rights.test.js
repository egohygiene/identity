// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import fs from "node:fs";

import { JSDOM } from "jsdom";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, test } from "vitest";

import { BrandKitPage } from "../src/app.js";
import { createPressKitView } from "../src/press-kit.js";

const fixture = JSON.parse(fs.readFileSync(
  new URL("../fixtures/example.brand-kit.view-model.json", import.meta.url),
  "utf8",
));

describe("asset rights and authoritative references", () => {
  test("presents supplied asset rights and restrictions in both download surfaces", () => {
    const model = structuredClone(fixture);
    const asset = model.assets[0];
    asset.license = { spdx: "CC-BY-4.0", status: "approved", attribution: "Artwork © Example artist" };
    asset.origin = {
      creator: "Example artist",
      method: "commissioned",
      source: "https://example.invalid/artwork/source",
      capturedAt: "2026-10-20T12:00:00Z",
    };
    asset.usage = {
      safeZone: "Keep one mark width clear.",
      minimumSize: "Use at 24 CSS pixels or larger.",
      restrictions: ["Preserve the original proportions.", "Do not imply endorsement."],
    };
    asset.approval = "approve-artwork";
    const pressKit = projection(model);
    pressKit.assets = [{
      ...asset,
      assetId: asset.id,
      notes: "Supplied media selection.",
      approval: { id: asset.approval, subject: "asset:mark" },
    }];
    model.pressKit = createPressKitView({ pressKit, artifactDirectory: "press-kit" });
    const document = renderDocument(model);

    for (const section of ["#provenance", "#press-kit"]) {
      const rights = document.querySelector(`${section} [data-asset-rights="mark"]`);
      expect(rights).not.toBeNull();
      for (const value of [
        asset.license.spdx, asset.license.attribution, asset.origin.creator,
        asset.origin.method, asset.origin.source, asset.origin.capturedAt,
        asset.sha256, asset.approval, asset.usage.safeZone, asset.usage.minimumSize,
        ...asset.usage.restrictions,
      ]) expect(rights.textContent).toContain(value);
      expect(rights.textContent).toContain("Asset license");
      expect(rights.textContent).not.toContain("MIT");
      expect(rights.querySelector("pre")).toBeNull();
      expect(rights.textContent).not.toContain("[object Object]");
    }
    expect(document.querySelector("#press-kit [data-asset-rights]").textContent)
      .toContain("asset:mark");
  });

  test("keeps absent rights unresolved without software-license or approval defaults", () => {
    const model = structuredClone(fixture);
    for (const field of ["license", "origin", "approval", "usage"]) delete model.assets[0][field];
    const document = renderDocument(model);
    const rights = document.querySelector("#provenance [data-asset-rights]");
    const terms = [...rights.querySelectorAll("dt")];
    const valueFor = (term) => terms.find((entry) => entry.textContent === term)?.nextElementSibling.textContent;

    for (const term of ["Asset license", "License review", "Attribution", "Approval", "Creator", "Source", "Safe zone", "Minimum size"]) {
      expect(valueFor(term)).toBe("Not declared");
    }
    expect(valueFor("SHA-256")).toBe(model.assets[0].sha256);
    expect(rights.textContent).toContain("No restrictions declared.");
    expect(rights.textContent).not.toMatch(/MIT|approved|human-approved|Ego Hygiene/u);
  });

  test("renders structured legal and third-party rights readably without copying software policy", () => {
    const model = structuredClone(fixture);
    const legal = {
      trademark: "Use the reviewed project name without implying endorsement.",
      copyright: "Copyright 2026 Example rights owner.",
      attribution: "Retain the supplied attribution.",
      thirdPartyLicenses: [{
        name: "Separate Example font",
        spdx: "OFL-1.1",
        attribution: "Copyright Example type designer.",
      }],
    };
    model.guidance.usage.value = { sections: [], legal };
    const document = renderDocument(model);
    const guidance = document.querySelector("#usage [data-legal-guidance]");

    expect(guidance.querySelector("pre")).toBeNull();
    expect(guidance.textContent).not.toContain("[object Object]");
    expect(guidance.textContent).toContain("Trademark rules");
    expect(guidance.textContent).toContain("Third-party asset licenses");
    for (const value of [legal.trademark, legal.copyright, legal.attribution,
      ...Object.values(legal.thirdPartyLicenses[0])]) {
      expect(guidance.textContent).toContain(value);
    }
  });

  test("omits missing optional legal records and official references cleanly", () => {
    const model = structuredClone(fixture);
    model.guidance.usage.value = { sections: [] };
    const pressKit = projection(model);
    model.pressKit = createPressKitView({ pressKit, artifactDirectory: "press-kit" });
    const document = renderDocument(model);

    expect(document.querySelector("#usage [data-legal-guidance]")).toBeNull();
    expect(document.querySelector("[data-third-party-licenses]")).toBeNull();
    expect(document.querySelector("#press-kit").textContent).toContain("Links and contact not declared");
    expect(document.querySelector("#press-kit").textContent).toContain("Public legal guidance is not declared.");
    expect(document.querySelectorAll("#press-kit a:not([download])")).toHaveLength(0);
  });
});

function renderDocument(model) {
  return new JSDOM(renderToStaticMarkup(React.createElement(BrandKitPage, { model })))
    .window.document;
}

function projection(model) {
  return {
    schema: "identity.press-kit/v1",
    project: { id: model.projectId, ...model.project, kind: "product" },
    source: {
      digest: model.release.sourceDigest,
      sourceSchema: "identity.press-kit-source/v1",
      projectionVersion: "1.0.0",
    },
    boilerplates: ["short", "long"].map((kind) => ({
      id: kind,
      kind,
      text: `Supplied ${kind} project description.`,
      approval: { id: `approve-${kind}` },
    })),
    facts: [],
    links: [],
    contacts: [],
    team: [],
    assets: [],
    guidance: { usageRules: [], legal: { status: "not-declared", value: null } },
    artifacts: [
      ["press-kit-json", "press-kit.json"],
      ["press-kit-markdown", "press-kit.md"],
      ["press-kit-manifest", "press-kit-manifest.json"],
      ["press-kit-checksums", "SHA256SUMS"],
      ["press-kit-archive", "press-kit.zip"],
    ].map(([id, path]) => ({ id, path, label: id })),
  };
}
