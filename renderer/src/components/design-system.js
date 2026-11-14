// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import React from "react";

import { joinAssetUrl, statusLabel } from "../model.js";
import { Section, DefinitionList } from "./shared.js";

const h = React.createElement;

export function DesignSystemSection({ designSystem, assetBaseUrl }) {
  const { handbook, context, artifacts } = designSystem;
  return h(
    Section,
    {
      id: "design-system",
      title: "Design-system handbook",
      canonical: true,
    },
    h(
      "div",
      { className: "section-stack" },
      h(
        "article",
        { className: "panel" },
        h("p", { className: "eyebrow" }, "Generated projection"),
        h("h3", null, handbook.project.displayName),
        h(
          "p",
          null,
          "This public view consumes the reviewed handbook and AI context artifacts directly. It does not recreate source guidance.",
        ),
        h(DefinitionList, {
          entries: [
            ["Project kind", handbook.project.kind],
            ["Projection schema", handbook.schema],
            ["Source digest", context.source.digest],
            ["Projection version", context.source.projectionVersion],
          ],
        }),
      ),
      handbook.inheritance
        ? h(
            "article",
            { className: "panel" },
            h("h3", null, "Inheritance and bounded overrides"),
            h(
              "p",
              null,
              `Organization layers: ${(handbook.inheritance.organizationLayers || []).join(", ") || "None declared"}.`,
            ),
            h(
              "p",
              null,
              `Product layer: ${handbook.inheritance.productLayer || "Not declared"}.`,
            ),
            handbook.inheritance.overrides?.length
              ? h(
                  "ul",
                  { className: "guidance-list" },
                  ...handbook.inheritance.overrides.map((override) =>
                    h(
                      "li",
                      { key: override.token },
                      h("code", null, override.token),
                      ` — ${override.reason} (approval: ${override.approval})`,
                    ),
                  ),
                )
              : h("p", { className: "support-note" }, "No reviewed overrides are declared."),
          )
        : null,
      h(
        "div",
        { className: "handbook-grid" },
        ...handbook.sections.map((section) =>
          h(
            "article",
            { className: "panel handbook-card", key: section.id },
            h("h3", null, section.title),
            h("p", null, section.summary),
            section.principles?.length
              ? h(
                  "div",
                  { className: "handbook-principles" },
                  ...section.principles.map((principle) =>
                    h(
                      "section",
                      { key: principle.id },
                      h("h4", null, principle.title),
                      h("p", null, principle.guidance),
                      h("p", { className: "support-note" }, `Why: ${principle.rationale}`),
                      h(
                        "p",
                        { className: "support-note" },
                        `Applies to: ${(principle.appliesTo || []).join(", ")}`,
                      ),
                    ),
                  ),
                )
              : h("p", { className: "support-note" }, "No public principles are declared for this section."),
          ),
        ),
      ),
      h(
        "article",
        { className: "panel" },
        h("h3", null, "Capability ownership"),
        h(
          "div",
          { className: "capability-list" },
          ...handbook.capabilities.map((capability) =>
            h(
              "div",
              { className: "capability-row", key: capability.id },
              h(
                "div",
                null,
                h("h4", null, capability.label),
                h("p", null, capability.notes),
              ),
              h(
                "p",
                { className: "declaration-status" },
                `${statusLabel(capability.status)} · ${capability.owner}`,
              ),
            ),
          ),
        ),
      ),
      h(
        "article",
        { className: "panel" },
        h("h3", null, "Handbook and AI context downloads"),
        h(
          "div",
          { className: "download-list" },
          ...artifacts.map((artifact) =>
            h(
              "div",
              { className: "download-row", key: artifact.id },
              h(
                "div",
                null,
                h("h4", null, artifact.label),
                h("p", { className: "support-note" }, artifact.mediaType),
              ),
              h(
                "a",
                {
                  className: "button button--secondary",
                  href: joinAssetUrl(assetBaseUrl, artifact.path),
                  download: true,
                },
                "Download",
              ),
            ),
          ),
        ),
      ),
    ),
  );
}
