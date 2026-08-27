// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

import React from "react";
import { renderToStaticMarkup } from "react-dom/server";

import { BrandKitPage } from "../src/app.js";
import {
  assertBrandKitViewModel,
  deriveThemeVariables,
} from "../src/model.js";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const rendererRoot = path.resolve(scriptDirectory, "..");
const argumentsMap = parseArguments(process.argv.slice(2));
const modelPath = path.resolve(
  rendererRoot,
  argumentsMap.model || "fixtures/example.brand-kit.view-model.json",
);
const outputPath = path.resolve(
  rendererRoot,
  argumentsMap.output || "index.html",
);
const templatePath = path.resolve(rendererRoot, "index.template.html");
const assetBaseUrl = argumentsMap["asset-base-url"] || "./";

const model = assertBrandKitViewModel(
  JSON.parse(await fs.readFile(modelPath, "utf8")),
);
const markup = renderToStaticMarkup(
  React.createElement(BrandKitPage, { model, assetBaseUrl }),
);
const template = await fs.readFile(templatePath, "utf8");
const rendered = template
  .replaceAll("{{LANGUAGE}}", "en")
  .replaceAll("{{PAGE_TITLE}}", escapeHtml(`${model.project.displayName} Brand Kit`))
  .replaceAll("{{PAGE_DESCRIPTION}}", escapeHtml(model.project.tagline))
  .replaceAll("{{THEME_VARIABLES}}", deriveThemeVariables(model))
  .replaceAll("{{ASSET_BASE_URL}}", escapeHtmlAttribute(assetBaseUrl))
  .replaceAll("{{STATIC_MARKUP}}", markup)
  .replaceAll("{{MODEL_JSON}}", escapeScriptJson(model));

await fs.mkdir(path.dirname(outputPath), { recursive: true });
await fs.writeFile(outputPath, rendered, "utf8");
process.stdout.write(`Rendered static Brand Kit: ${outputPath}\n`);

function parseArguments(values) {
  const result = {};
  for (let index = 0; index < values.length; index += 1) {
    const value = values[index];
    if (!value.startsWith("--")) {
      throw new Error(`Unexpected positional argument: ${value}`);
    }
    const key = value.slice(2);
    const next = values[index + 1];
    if (!next || next.startsWith("--")) {
      throw new Error(`Argument --${key} requires a value.`);
    }
    result[key] = next;
    index += 1;
  }
  return result;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function escapeHtmlAttribute(value) {
  return escapeHtml(value).replaceAll('"', "&quot;");
}

function escapeScriptJson(value) {
  return JSON.stringify(value)
    .replaceAll("<", "\\u003c")
    .replaceAll(">", "\\u003e")
    .replaceAll("&", "\\u0026")
    .replaceAll("\u2028", "\\u2028")
    .replaceAll("\u2029", "\\u2029");
}
