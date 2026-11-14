// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import React from "react";


const h = React.createElement;

export function Section({ id, title, preview = false, canonical = false, children }) {
  return h(
    "section",
    { className: "content-section", id, "aria-labelledby": `${id}-title` },
    h(
      "div",
      { className: "section-heading" },
      h("h2", { id: `${id}-title` }, title),
      preview
        ? h("span", { className: "authority-badge" }, "Generated preview")
        : null,
      canonical
        ? h(
            "span",
            { className: "authority-badge authority-badge--canonical" },
            "Canonical guidance",
          )
        : null,
    ),
    children,
  );
}

export function DefinitionList({ entries }) {
  return h(
    "dl",
    { className: "definition-list" },
    ...entries.flatMap(([term, description]) => [
      h("dt", { key: `${term}-term` }, term),
      h(
        "dd",
        { key: `${term}-description` },
        shouldUseCode(term)
          ? h("code", null, String(description))
          : String(description),
      ),
    ]),
  );
}

export function CopyControl({ label, value }) {
  return h(
    "button",
    {
      className: "copy-control",
      type: "button",
      "data-copy-value": value,
      "data-copy-label": label,
      "aria-describedby": "copy-status",
    },
    "Copy value",
  );
}

export function EmptyState({ title, message }) {
  return h(
    "div",
    { className: "empty-state", role: "note" },
    h("h3", null, title),
    h("p", null, message),
  );
}

export function humanize(value) {
  return value
    .split(/[-_]/u)
    .filter(Boolean)
    .map((segment) => `${segment[0].toUpperCase()}${segment.slice(1)}`)
    .join(" ");
}

export function shouldUseCode(term) {
  return [
    "Immutable ID",
    "Source digest",
    "Contract",
    "SHA-256",
  ].includes(term);
}
