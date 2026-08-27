// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import React from "react";
import { hydrateRoot } from "react-dom/client";

import { BrandKitPage } from "./app.js";
import { assertBrandKitViewModel } from "./model.js";
import "./section-states.css";
import "./styles.css";

const modelElement = document.querySelector("#identity-brand-kit-model");
const rootElement = document.querySelector("#identity-brand-kit-root");

if (!(modelElement instanceof HTMLScriptElement) || !rootElement) {
  throw new Error("Reference renderer is missing its immutable model or root.");
}

const model = assertBrandKitViewModel(JSON.parse(modelElement.textContent || "{}"));
const assetBaseUrl = rootElement.dataset.assetBaseUrl || "./";

hydrateRoot(
  rootElement,
  React.createElement(BrandKitPage, { model, assetBaseUrl }),
);

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
