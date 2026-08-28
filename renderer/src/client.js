// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import React from "react";
import { hydrateRoot } from "react-dom/client";

import { BrandKitPage } from "./app.js";
import { assertBrandKitViewModel, sourceDataUrl } from "./model.js";
import { createApprovedHandoff, inspectCandidateBundle } from "./studio.js";
import "./section-states.css";
import "./styles.css";

const modelElement = document.querySelector("#identity-brand-kit-model");
const rootElement = document.querySelector("#identity-brand-kit-root");

if (!(modelElement instanceof HTMLScriptElement) || !rootElement) {
  throw new Error("Reference renderer is missing its immutable model or root.");
}

const model = assertBrandKitViewModel(JSON.parse(modelElement.textContent || "{}"));
const assetBaseUrl = rootElement.dataset.assetBaseUrl || "./";
const publication = readPublication(rootElement.dataset.publication);

hydrateRoot(
  rootElement,
  React.createElement(BrandKitPage, { model, assetBaseUrl, publication }),
);

let studioPlan = null;
let studioBundle = null;
const studio = document.querySelector("[data-studio]");
if (studio) {
  const input = studio.querySelector("#candidate-bundle");
  const importInput = studio.querySelector("[data-studio-import]");
  const result = studio.querySelector("[data-studio-result]");
  const comparison = studio.querySelector("[data-studio-comparison]");
  const approval = studio.querySelector("[data-studio-approval]");
  const reviewer = studio.querySelector("[data-studio-reviewer]");
  const exportButton = studio.querySelector("[data-studio-export]");
  const exportBundleButton = studio.querySelector("[data-studio-export-bundle]");
  studio.querySelector("[data-studio-preview]").addEventListener("click", () => {
    try {
      const inspected = inspectCandidateBundle(JSON.parse(input.value), model);
      studioPlan = inspected.plan;
      studioBundle = inspected.bundle;
      result.textContent = inspected.errors.length ? inspected.errors.join("\n") : JSON.stringify(studioPlan, null, 2);
      renderCandidateComparisons(comparison, studioBundle, model);
      updateStudioControls();
    } catch (error) {
      studioPlan = null;
      studioBundle = null;
      result.textContent = `Invalid JSON: ${error.message}`;
      comparison.textContent = "No candidate comparison is available.";
      updateStudioControls();
    }
  });
  importInput.addEventListener("change", async () => {
    const [file] = importInput.files;
    if (!file) return;
    input.value = await file.text();
    result.textContent = `Loaded ${file.name}. Validate and preview the imported bundle.`;
  });
  approval.addEventListener("change", updateStudioControls);
  reviewer.addEventListener("input", updateStudioControls);
  exportButton.addEventListener("click", () => {
    downloadJson("identity-approved-handoff.json", createApprovedHandoff(studioPlan, reviewer.value));
  });
  exportBundleButton.addEventListener("click", () => downloadJson("identity-candidate-review.json", studioBundle));

  function updateStudioControls() {
    exportBundleButton.disabled = !studioBundle;
    exportButton.disabled = !studioPlan
      || studioPlan.writes.length === 0
      || !approval.checked
      || !reviewer.value.trim();
  }
}

function renderCandidateComparisons(container, bundle, currentModel) {
  container.replaceChildren();
  if (!bundle) {
    container.textContent = "No candidate comparison is available.";
    return;
  }
  const heading = document.createElement("h3");
  heading.textContent = `Candidate review · ${bundle.profiles.join(", ")}`;
  container.append(heading);
  for (const candidate of bundle.candidates) {
    const card = document.createElement("article");
    card.className = "studio__candidate";
    const title = document.createElement("h4");
    title.textContent = `${candidate.id} · ${candidate.state}`;
    card.append(title);
    const state = document.createElement("p");
    state.textContent = `State: ${candidate.state}. Kind: ${candidate.kind}.`;
    card.append(state);
    const surfaces = document.createElement("div");
    surfaces.className = "studio__surfaces";
    appendStudioSurface(surfaces, "Candidate", candidate.preview?.dataUrl);
    const approved = currentModel.assets.find((asset) => asset.id === candidate.approvedAssetId);
    appendStudioSurface(surfaces, "Approved", approved ? sourceDataUrl(approved) : "");
    card.append(surfaces);
    container.append(card);
  }
}

function appendStudioSurface(container, label, source) {
  const surface = document.createElement("section");
  const heading = document.createElement("h5");
  heading.textContent = label;
  surface.append(heading);
  if (source) {
    const image = document.createElement("img");
    image.alt = `${label} asset comparison`;
    image.src = source;
    surface.append(image);
  } else {
    const absent = document.createElement("p");
    absent.textContent = "No local preview supplied.";
    surface.append(absent);
  }
  container.append(surface);
}

function downloadJson(fileName, value) {
  const link = document.createElement("a");
  const objectUrl = URL.createObjectURL(new Blob([JSON.stringify(value, null, 2)], { type: "application/json" }));
  link.href = objectUrl;
  link.download = fileName;
  link.click();
  window.setTimeout(() => URL.revokeObjectURL(objectUrl), 0);
}

document.addEventListener("click", async (event) => {
  const copyButton = event.target.closest("[data-copy-value]");
  if (copyButton instanceof HTMLButtonElement) {
    const value = copyButton.dataset.copyValue || "";
    const label = copyButton.dataset.copyLabel || "value";
    await copyText(value);
    updateCopyStatus(`${label} copied.`);
    copyButton.textContent = "Copied";
    window.setTimeout(() => {
      copyButton.textContent = "Copy value";
    }, 1800);
    return;
  }

  const themeButton = event.target.closest("[data-theme-toggle]");
  if (themeButton instanceof HTMLButtonElement) {
    const theme = nextTheme(document.documentElement.dataset.theme || "system");
    document.documentElement.dataset.theme = theme;
    themeButton.textContent = `Theme: ${theme}`;
    themeButton.setAttribute("aria-label", `Change color theme. Current theme: ${theme}`);
  }
});

async function copyText(value) {
  if (navigator.clipboard?.writeText) {
    try {
      await navigator.clipboard.writeText(value);
      return;
    } catch {
      // Continue to the deterministic local fallback.
    }
  }

  const textarea = document.createElement("textarea");
  textarea.value = value;
  textarea.setAttribute("readonly", "");
  textarea.style.position = "fixed";
  textarea.style.opacity = "0";
  document.body.append(textarea);
  textarea.select();
  document.execCommand?.("copy");
  textarea.remove();
}

function updateCopyStatus(message) {
  const status = document.querySelector("#copy-status");
  if (status) {
    status.textContent = message;
  }
}

function nextTheme(current) {
  if (current === "system") {
    return "light";
  }
  if (current === "light") {
    return "dark";
  }
  return "system";
}

function readPublication(value) {
  if (!value) {
    return null;
  }
  const publication = JSON.parse(value);
  if (!publication || Object.keys(publication).length === 0) {
    return null;
  }
  return publication;
}
