// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { JSDOM } from "jsdom";
import { describe, expect, test } from "vitest";

const rendererRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const repositoryRoot = path.resolve(rendererRoot, "..");
const cases = JSON.parse(
  fs.readFileSync(
    path.join(repositoryRoot, "tests/fixtures/guidance-public-cases.json"),
    "utf8",
  ),
).cases;
cases.push({
  id: "supplied-extension-naming",
  updates: [
    { document: "usage", pointer: "/sections/0/title", value: "Supplied extension naming" },
    { document: "usage", pointer: "/sections/0/description", value: "Supplied guidance for extension naming." },
    { document: "usage", pointer: "/sections/0/rules/0/instruction", value: "APPROVED-EXTENSION-NAMING-INSTRUCTION." },
    { document: "usage", pointer: "/sections/0/rules/0/rationale", value: "APPROVED-EXTENSION-NAMING-RATIONALE." },
    { document: "usage", pointer: "/sections/0/rules/0/details", value: ["APPROVED-EXTENSION-NAMING-DETAIL."] },
    { document: "usage", pointer: "/sections/0/rules/1/instruction", value: "WITHHELD-EXTENSION-NAMING-INSTRUCTION." },
    { document: "usage", pointer: "/sections/0/rules/1/governance/visibility", value: "internal" },
  ],
  retained: ["APPROVED-EXTENSION-NAMING-INSTRUCTION."],
  withheld: ["WITHHELD-EXTENSION-NAMING-INSTRUCTION."],
});
const fixtureRoot = path.join(repositoryRoot, "tests/fixtures/v1/valid/minimal");
const fixtureModel = path.join(rendererRoot, "fixtures/example.brand-kit.view-model.json");

describe("public guidance in static renderer output", () => {
  for (const guidanceCase of cases) {
    test(`filters ${guidanceCase.id} from HTML and embedded model data`, () => {
      const temporary = fs.mkdtempSync(
        path.join(os.tmpdir(), "identity-public-guidance-"),
      );
      try {
        const consumer = path.join(temporary, "consumer");
        fs.cpSync(fixtureRoot, consumer, { recursive: true });
        for (const update of guidanceCase.updates) {
          const sourcePath = path.join(
            consumer,
            `.identity/guidance/${update.document}.json`,
          );
          const source = JSON.parse(fs.readFileSync(sourcePath, "utf8"));
          const tokens = update.pointer.slice(1).split("/");
          let parent = source;
          for (const token of tokens.slice(0, -1)) parent = parent[token];
          parent[tokens.at(-1)] = update.value;
          fs.writeFileSync(sourcePath, JSON.stringify(source));
        }
        const pythonModel = JSON.parse(
          execFileSync(
            "python3",
            [
              path.join(repositoryRoot, "scripts/render_guidance.py"),
              "--repository-root", consumer,
              "--audience", "public",
              "--format", "json",
            ],
            { encoding: "utf8" },
          ),
        );
        const model = JSON.parse(fs.readFileSync(fixtureModel, "utf8"));
        const declared = (value) => ({ status: "declared", canonical: true, value });
        model.guidance = {
          voice: declared(
            Object.fromEntries(
              ["foundation", "characteristics", "contexts", "localization"]
                .filter((key) => pythonModel[key] !== null)
                .map((key) => [key, pythonModel[key]]),
            ),
          ),
          usage: declared({
            sections: pythonModel.sections,
            assets: [...pythonModel.downloads, ...pythonModel.legacyAssets],
            ...(pythonModel.accessibility
              ? { accessibility: pythonModel.accessibility }
              : {}),
            ...(pythonModel.legal ? { legal: pythonModel.legal } : {}),
          }),
        };
        const modelPath = path.join(temporary, "model.json");
        const outputPath = path.join(temporary, "index.html");
        fs.writeFileSync(modelPath, JSON.stringify(model));
        execFileSync(process.execPath, [
          path.join(rendererRoot, "scripts/render-static.mjs"),
          "--model", modelPath,
          "--output", outputPath,
        ]);
        const html = fs.readFileSync(outputPath, "utf8");
        const document = new JSDOM(html).window.document;
        const visibleText = document.querySelector("main").textContent;
        const voice = document.querySelector("#voice");
        for (const phrase of guidanceCase.withheld) expect(html).not.toContain(phrase);
        for (const phrase of guidanceCase.retained) expect(html).toContain(phrase);
        for (const phrase of guidanceCase.withheld) expect(visibleText).not.toContain(phrase);
        expect(visibleText).toContain("Voice and personality");
        expect(visibleText).toContain("Usage rules");
        expect(voice.textContent).not.toContain("[object Object]");
        expect(voice.querySelector("pre")).toBeNull();
        assertVisibleVoice(voice, pythonModel);
        assertVisibleUsage(document.querySelector("#usage"), pythonModel);
      } finally {
        fs.rmSync(temporary, { recursive: true, force: true });
      }
    });
  }
});

function assertVisibleVoice(voice, model) {
  const expectedCopy = [];
  const foundation = voice.querySelector("[data-voice-foundation]");
  if (model.foundation) {
    expect(foundation).not.toBeNull();
    for (const key of ["purpose", "positioning"]) {
      expect(foundation.textContent).toContain(model.foundation[key]);
      expectedCopy.push(model.foundation[key]);
    }
    for (const value of [...model.foundation.audience, ...model.foundation.personality]) {
      expect(foundation.textContent).toContain(value);
    }
  } else {
    expect(foundation).toBeNull();
    expect(voice.textContent).not.toContain("Project profile");
  }

  for (const characteristic of model.characteristics) {
    expect(voice.textContent).toContain(characteristic.label);
    expect(voice.textContent).toContain(characteristic.description);
  }
  const contexts = [...voice.querySelectorAll("[data-voice-context]")];
  expect(contexts.map((context) => context.dataset.voiceContext)).toEqual(
    model.contexts.map((context) => context.id),
  );
  for (const context of model.contexts) {
    const element = contexts.find((entry) => entry.dataset.voiceContext === context.id);
    for (const key of ["label", "audience", "intent", "tone", "naming", "capitalization", "punctuation"]) {
      expect(element.textContent).toContain(context[key]);
    }
    for (const value of [...context.preferredVocabulary, ...context.avoidedLanguage]) {
      expect(element.textContent).toContain(value);
    }
    for (const example of [...context.examples, ...context.antiExamples]) {
      expect(element.textContent).toContain(example.text);
      expect(element.textContent).toContain(example.rationale);
    }
    expectedCopy.push(...context.examples.map((example) => example.text));
    const contextCopy = [...element.querySelectorAll("[data-copy-value]")]
      .map((control) => control.dataset.copyValue);
    for (const example of context.antiExamples) expect(contextCopy).not.toContain(example.text);
  }

  const localization = voice.querySelector("[data-voice-localization]");
  if (model.localization) {
    expect(localization).not.toBeNull();
    expect(localization.textContent).toContain(model.localization.sourceLanguage);
    expect(localization.textContent).toContain(model.localization.fallback);
    for (const language of model.localization.supportedLanguages) {
      expect(localization.textContent).toContain(language.tag);
      expect(localization.textContent).toContain(language.coverage);
      expect(localization.textContent).toContain(language.notes);
    }
  } else {
    expect(localization).toBeNull();
  }
  const controls = [...voice.querySelectorAll("[data-copy-value]")];
  expect(controls.map((control) => control.dataset.copyValue)).toEqual(expectedCopy);
  expect(controls.every((control) => control.getAttribute("aria-describedby") === "copy-status"))
    .toBe(true);
}

function assertVisibleUsage(usage, model) {
  const sections = [...usage.querySelectorAll("[data-usage-section]")];
  expect(sections.map((section) => section.dataset.usageSection)).toEqual(
    model.sections.map((section) => section.id),
  );
  for (const section of model.sections) {
    const element = sections.find((entry) => entry.dataset.usageSection === section.id);
    expect(element.querySelector("h3").textContent).toBe(section.title);
    expect(element.querySelector("p").textContent).toBe(section.description);
    expect(element.textContent).not.toContain("[object Object]");
    expect(element.querySelector("pre")).toBeNull();
    const rules = [...element.querySelectorAll("[data-usage-rule]")];
    expect(rules.map((rule) => rule.dataset.usageRule)).toEqual(
      section.rules.map((rule) => rule.id),
    );
    for (const rule of section.rules) {
      const ruleElement = rules.find((entry) => entry.dataset.usageRule === rule.id);
      expect(ruleElement.dataset.usageKind).toBe(rule.kind);
      expect(ruleElement.dataset.usageCategory).toBe(rule.category);
      expect(ruleElement.querySelector("h4").textContent)
        .toBe(`${rule.kind === "do" ? "Do" : "Don't"} · ${rule.category}`);
      const paragraphs = [...ruleElement.querySelectorAll("p")];
      expect(paragraphs.map((paragraph) => paragraph.textContent)).toEqual([
        rule.instruction,
        rule.rationale,
        `Contexts: ${rule.contexts.join(", ")}`,
      ]);
      expect([...ruleElement.querySelectorAll("li")].map((detail) => detail.textContent))
        .toEqual(rule.details);
      expect(ruleElement.querySelector("[data-copy-value]")).toBeNull();
    }
  }
}
