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
import { createDesignSystemView } from "../src/design-system.js";
import { createPressKitView } from "../src/press-kit.js";

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
const canonicalUrl = argumentsMap["canonical-url"] || null;
const openGraphImage = argumentsMap["open-graph-image"] || null;
const publicationPath = argumentsMap.publication
  ? path.resolve(argumentsMap.publication)
  : null;
const designSystemDirectory = argumentsMap["design-system-directory"]
  ? path.resolve(argumentsMap["design-system-directory"])
  : null;
const designSystemArtifactDirectory =
  argumentsMap["design-system-artifact-directory"] || "design-system";
const pressKitDirectory = argumentsMap["press-kit-directory"]
  ? path.resolve(argumentsMap["press-kit-directory"])
  : null;
const pressKitArtifactDirectory =
  argumentsMap["press-kit-artifact-directory"] || "press-kit";

const baseModel = assertBrandKitViewModel(
  JSON.parse(await fs.readFile(modelPath, "utf8")),
);
let model = baseModel;
if (designSystemDirectory) {
  model = assertBrandKitViewModel({
    ...model,
    designSystem: await loadDesignSystem(
      designSystemDirectory,
      designSystemArtifactDirectory,
    ),
  });
}
if (pressKitDirectory) {
  model = assertBrandKitViewModel({
    ...model,
    pressKit: await loadPressKit(pressKitDirectory, pressKitArtifactDirectory),
  });
}
const publication = publicationPath
  ? JSON.parse(await fs.readFile(publicationPath, "utf8"))
  : null;
const markup = renderToStaticMarkup(
  React.createElement(BrandKitPage, { model, assetBaseUrl, publication }),
);
const template = await fs.readFile(templatePath, "utf8");
const rendered = template
  .replaceAll("{{LANGUAGE}}", "en")
  .replaceAll("{{PAGE_TITLE}}", escapeHtml(`${model.project.displayName} Brand Kit`))
  .replaceAll("{{PAGE_DESCRIPTION}}", escapeHtml(model.project.tagline))
  .replaceAll("{{THEME_VARIABLES}}", deriveThemeVariables(model))
  .replaceAll("{{ASSET_BASE_URL}}", escapeHtmlAttribute(assetBaseUrl))
  .replaceAll("{{PUBLICATION_JSON}}", escapeHtmlAttribute(JSON.stringify(publication || {})))
  .replaceAll(
    "{{CANONICAL_METADATA}}",
    canonicalMetadata({ model, canonicalUrl, openGraphImage }),
  )
  .replaceAll("{{STATIC_MARKUP}}", markup)
  .replaceAll("{{MODEL_JSON}}", escapeScriptJson(model));

await fs.mkdir(path.dirname(outputPath), { recursive: true });
await fs.writeFile(outputPath, rendered, "utf8");
process.stdout.write(`Rendered static Brand Kit: ${outputPath}\n`);

async function loadDesignSystem(directory, artifactDirectory) {
  const [handbook, context] = await Promise.all([
    readJson(path.join(directory, "design-system-handbook.json")),
    readJson(path.join(directory, "design-context.json")),
  ]);
  return createDesignSystemView({ handbook, context, artifactDirectory });
}

async function loadPressKit(directory, artifactDirectory) {
  return createPressKitView({
    pressKit: await readJson(path.join(directory, "press-kit.json")),
    artifactDirectory,
  });
}

async function readJson(filePath) {
  try {
    return JSON.parse(await fs.readFile(filePath, "utf8"));
  } catch (error) {
    throw new Error(`Cannot read generated Identity artifact: ${filePath}: ${error.message}`);
  }
}

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

function canonicalMetadata({ model, canonicalUrl: url, openGraphImage: image }) {
  if (!url) {
    return "";
  }
  const canonical = new URL(url);
  if (canonical.protocol !== "https:" || canonical.pathname !== "/") {
    throw new Error("The canonical Brand Kit URL must be an HTTPS origin URL ending in /.");
  }
  if (image) {
    const openGraphUrl = new URL(image);
    if (openGraphUrl.protocol !== "https:") {
      throw new Error("The Open Graph image URL must use HTTPS.");
    }
  }

  const title = `${model.project.displayName} Brand Kit`;
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    name: title,
    description: model.project.tagline,
    url: canonical.toString(),
    isBasedOn: model.project.repository,
  };
  const lines = [
    `<link rel="canonical" href="${escapeHtmlAttribute(canonical.toString())}" />`,
    `<meta property="og:type" content="website" />`,
    `<meta property="og:title" content="${escapeHtmlAttribute(title)}" />`,
    `<meta property="og:description" content="${escapeHtmlAttribute(model.project.tagline)}" />`,
    `<meta property="og:url" content="${escapeHtmlAttribute(canonical.toString())}" />`,
    `<meta name="twitter:card" content="summary_large_image" />`,
    `<meta name="twitter:title" content="${escapeHtmlAttribute(title)}" />`,
    `<meta name="twitter:description" content="${escapeHtmlAttribute(model.project.tagline)}" />`,
  ];
  if (image) {
    const openGraphUrl = new URL(image).toString();
    lines.push(
      `<meta property="og:image" content="${escapeHtmlAttribute(openGraphUrl)}" />`,
      `<meta name="twitter:image" content="${escapeHtmlAttribute(openGraphUrl)}" />`,
    );
  }
  lines.push(
    `<script type="application/ld+json">${escapeScriptJson(structuredData)}</script>`,
  );
  return lines.join("\n    ");
}
