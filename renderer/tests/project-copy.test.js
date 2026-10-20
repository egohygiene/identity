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

describe("approved project copy", () => {
  test.each([false, true])("copies exact supplied descriptions and facts with paragraph present: %s", (paragraph) => {
    const model = structuredClone(fixture);
    const pressKit = projection(model, paragraph);
    model.pressKit = createPressKitView({ pressKit, artifactDirectory: "press-kit" });
    const document = renderDocument(model);
    const section = document.querySelector("#press-kit");
    const controls = [...section.querySelectorAll("[data-copy-value]")];

    expect(controls.map((control) => control.dataset.copyValue)).toEqual([
      ...pressKit.boilerplates.map((entry) => entry.text),
      ...pressKit.facts.map((entry) => entry.value),
    ]);
    expect(controls.map((control) => control.dataset.copyLabel)).toEqual([
      "Short description",
      ...(paragraph ? ["Paragraph description"] : []),
      "Long description",
      "Short name",
    ]);
    for (const control of controls) {
      expect(control.getAttribute("aria-describedby")).toBe("copy-status");
      expect(control.parentElement.querySelector("p").textContent).toBe(control.dataset.copyValue);
    }
    expect([...section.querySelectorAll("h4")].map((heading) => heading.textContent))
      .toContain("Short");
    if (!paragraph) expect(section.textContent).not.toContain("Paragraph");
    expect(section.textContent).not.toContain("undefined");
    expect(document.querySelector("#copy-status")).not.toBeNull();
  });

  test("omits absent optional profile material without supplying claims", () => {
    const model = structuredClone(fixture);
    model.guidance.voice.value = { characteristics: [], contexts: [] };
    const pressKit = projection(model, false);
    pressKit.facts = [];
    model.pressKit = createPressKitView({ pressKit, artifactDirectory: "press-kit" });
    const document = renderDocument(model);
    const voice = document.querySelector("#voice");
    const press = document.querySelector("#press-kit");

    expect(voice.querySelectorAll(".panel")).toHaveLength(0);
    expect(voice.querySelectorAll("[data-copy-value]")).toHaveLength(0);
    expect(voice.querySelector("pre")).toBeNull();
    expect(voice.textContent).not.toMatch(/Purpose|Positioning|Audience|Naming|Localization/u);
    expect(press.textContent).toContain("Key facts not declared");
    expect(press.textContent).not.toMatch(/Short name|Pronunciation|Mission|Values/u);
    expect(press.querySelectorAll("[data-copy-value]")).toHaveLength(2);
  });
});

function renderDocument(model) {
  return new JSDOM(renderToStaticMarkup(React.createElement(BrandKitPage, { model })))
    .window.document;
}

function projection(model, paragraph) {
  const kinds = ["short", ...(paragraph ? ["paragraph"] : []), "long"];
  return {
    schema: "identity.press-kit/v1",
    project: { id: model.projectId, ...model.project, kind: "product" },
    source: {
      digest: model.release.sourceDigest,
      sourceSchema: "identity.press-kit-source/v1",
      projectionVersion: "1.0.0",
    },
    boilerplates: kinds.map((kind) => ({
      id: kind,
      kind,
      text: `Approved ${kind} copy: “Example Product”.\nPreserve the reviewed wording.`,
      approval: { id: `approve-${kind}` },
    })),
    facts: [{
      id: "short-name",
      label: "Short name",
      value: "Example",
      approval: { id: "approve-short-name" },
    }],
    links: [],
    contacts: [],
    team: [],
    assets: [],
    guidance: { usageRules: [], legal: { status: "not-declared" } },
    artifacts: [
      ["press-kit-json", "press-kit.json"],
      ["press-kit-markdown", "press-kit.md"],
      ["press-kit-manifest", "press-kit-manifest.json"],
      ["press-kit-checksums", "SHA256SUMS"],
      ["press-kit-archive", "press-kit.zip"],
    ].map(([id, path]) => ({ id, path, label: id })),
  };
}
