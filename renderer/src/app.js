// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import React from "react";

import { PresentationProfiles, selectedPresentationProfiles } from "./presentation.js";
import { joinAssetUrl, statusLabel } from "./model.js";
import { Section, DefinitionList, CopyControl } from "./components/shared.js";
import { GuidanceSection, AssetRights } from "./components/guidance.js";
import { DesignSystemSection } from "./components/design-system.js";
import { PressKitSection } from "./components/press-kit.js";
import { AssetsSection } from "./components/assets.js";
import { ColorSection, TypographySection } from "./components/foundations.js";
import { DownloadsSection, ProvenanceSection } from "./components/downloads.js";
import { resolvePageInputs } from "./page-input.js";

const h = React.createElement;

export function BrandKitPage({ model, assetBaseUrl = "./", publication = null, publicOnly = false }) {
  const inputs = resolvePageInputs({ model, assetBaseUrl, publication, publicOnly });
  assetBaseUrl = inputs.assetBaseUrl;
  const { colorTokens, foundations, typographyTokens, completeKit, sections } = inputs;
  const visible = (id) => sections.some(([section]) => section === id);

  return h(
    "div",
    {
      className: "brand-kit-shell",
      "data-project-id": model.projectId,
      "data-source-digest": model.release.sourceDigest,
    },
    h(SkipLink),
    h(
      "header",
      { className: "hero", id: "top" },
      h(
        "div",
        { className: "hero__content" },
        h("p", { className: "eyebrow" }, "Public Brand Kit"),
        h("h1", null, model.project.displayName),
        h("p", { className: "hero__tagline" }, model.project.tagline),
        h(
          "div",
          { className: "hero__meta" },
          h(
            "span",
            { className: "status-pill" },
            `Release ${model.release.version}`,
          ),
          h(
            "span",
            { className: "status-pill status-pill--quiet" },
            model.release.status,
          ),
        ),
      ),
      h(
        "div",
        { className: "hero__actions" },
        h(
          "button",
          {
            className: "button button--secondary",
            type: "button",
            "data-theme-toggle": true,
            "aria-label": "Change color theme",
          },
          "Theme: system",
        ),
        completeKit ? h(
          "a",
          {
            className: "button",
            href: joinAssetUrl(
              assetBaseUrl,
              completeKit.path,
            ),
            download: true,
          },
          publicOnly ? "Download asset package" : "Download complete kit",
        ) : null,
      ),
    ),
    h(
      "div",
      { className: "layout" },
      h(SectionNavigation, { sections }),
      h(
        "main",
        { id: "main-content", tabIndex: -1 },
        h(OverviewSection, { model }),
        visible("logos") ? h(AssetsSection, {
          assets: model.assets,
          downloads: model.downloads || [],
          assetBaseUrl,
        }) : null,
        visible("colors") ? h(ColorSection, { tokens: colorTokens, foundations }) : null,
        visible("typography") ? h(TypographySection, {
          tokens: typographyTokens, foundations,
          projectLinksAvailable: Boolean(model.pressKit?.pressKit.links.length),
        }) : null,
        visible("voice") ? h(GuidanceSection, {
          id: "voice",
          title: "Voice and personality",
          guidance: model.guidance.voice,
        }) : null,
        visible("usage") ? h(GuidanceSection, {
          id: "usage",
          title: "Usage rules",
          guidance: model.guidance.usage,
        }) : null,
        visible("creative-direction") ? h(CreativeDirectionSection, { support: model.support, publicOnly }) : null,
        model.designSystem
          ? h(DesignSystemSection, {
              designSystem: model.designSystem,
              assetBaseUrl,
            })
          : null,
        model.pressKit
          ? h(PressKitSection, {
              pressKit: model.pressKit,
              assetBaseUrl,
            })
          : null,
        selectedPresentationProfiles(model).length
          ? h(Section, { id: "presentation", title: "Selected presentation profiles" },
              h(PresentationProfiles, { model, assetBaseUrl, CopyControl, DefinitionList, AssetRights }),
            )
          : null,
        visible("studio") ? h(StudioSection, { model }) : null,
        visible("downloads") ? h(DownloadsSection, {
          packages: model.packages,
          assetBaseUrl,
        }) : null,
        h(ProvenanceSection, { model, assetBaseUrl, publication }),
      ),
    ),
    h(
      "footer",
      { className: "footer" },
      h(
        "p",
        null,
        "Generated from an immutable Identity view model. Canonical source remains consumer-owned.",
      ),
      h(
        "a",
        { href: model.project.repository },
        "Project repository",
      ),
    ),
    h(
      "p",
      {
        id: "copy-status",
        className: "visually-hidden",
        role: "status",
        "aria-live": "polite",
        "aria-atomic": "true",
      },
      "Copy controls are ready.",
    ),
  );
}

function StudioSection({ model }) {
  return h(Section, { id: "studio", title: "Review candidate assets" },
    h("div", { className: "panel studio", "data-studio": true, "data-project-id": model.projectId, "data-source-digest": model.release.sourceDigest },
      h("p", null, "Import a portable candidate bundle to compare local candidates against the immutable approved release. Previewing never writes canonical or generated files."),
      h("label", { htmlFor: "candidate-bundle-file" }, "Import candidate bundle"),
      h("input", { id: "candidate-bundle-file", type: "file", accept: "application/json", "data-studio-import": true }),
      h("label", { htmlFor: "candidate-bundle" }, "Candidate bundle JSON"),
      h("textarea", { id: "candidate-bundle", rows: 12, spellCheck: false, placeholder: '{ "schema": "identity.brand-kit-candidate/v1", "profiles": ["social"], ... }' }),
      h("div", { className: "studio__actions" },
        h("button", { className: "button button--secondary", type: "button", "data-studio-preview": true }, "Validate and preview plan"),
        h("button", { className: "button button--secondary", type: "button", disabled: true, "data-studio-export-bundle": true }, "Export review bundle")),
      h("pre", { className: "studio__result", "data-studio-result": true, "aria-live": "polite" }, "No candidate bundle has been loaded."),
      h("div", { className: "studio__comparison", "data-studio-comparison": true, "aria-live": "polite" }, "No candidate comparison is available."),
      h("label", { htmlFor: "studio-reviewer" }, "Reviewer identity"),
      h("input", { id: "studio-reviewer", type: "text", autoComplete: "name", "data-studio-reviewer": true }),
      h("label", { className: "studio__approval" }, h("input", { type: "checkbox", "data-studio-approval": true }), "I reviewed this plan and authorize a compiler handoff. This does not write files or publish assets."),
      h("button", { className: "button", type: "button", disabled: true, "data-studio-export": true }, "Export approved handoff"),
    ));
}

function SkipLink() {
  return h(
    "a",
    { className: "skip-link", href: "#main-content" },
    "Skip to Brand Kit content",
  );
}

function SectionNavigation({ sections }) {
  return h(
    "aside",
    { className: "section-navigation" },
    h(
      "nav",
      { "aria-label": "Brand Kit sections" },
      h(
        "ol",
        null,
        ...sections.map(([id, label]) =>
          h(
            "li",
            { key: id },
            h("a", { href: `#${id}` }, label),
          ),
        ),
      ),
    ),
  );
}

function OverviewSection({ model }) {
  return h(
    Section,
    { id: "overview", title: "Overview and version" },
    h(
      "div",
      { className: "overview-grid" },
      h(
        "article",
        { className: "panel panel--feature" },
        h("p", { className: "eyebrow" }, "Immutable release"),
        h("h3", null, model.project.displayName),
        h("p", null, model.project.tagline),
        h(DefinitionList, {
          entries: [
            ["Version", model.release.version],
            ["Profile", model.release.profileVersion],
            ["Status", model.release.status],
            ["Immutable ID", model.release.immutableId],
          ],
        }),
      ),
      h(
        "article",
        { className: "panel" },
        h("p", { className: "eyebrow" }, "Authority boundary"),
        h("h3", null, "What this page represents"),
        h(
          "p",
          null,
          "Assets and previews are generated projections. Voice and usage sections are labeled separately because they project canonical, human-reviewed guidance.",
        ),
      ),
    ),
  );
}

function CreativeDirectionSection({ support, publicOnly }) {
  const entries = [
    ["Motion", support.motion],
    ["Imagery", support.imagery],
    ["Mascot", support.mascot],
  ].filter(([, entry]) => !publicOnly || entry.status === "declared");
  return h(
    Section,
    {
      id: "creative-direction",
      title: "Motion, imagery, and mascot guidance",
    },
    h(
      "div",
      { className: "support-grid" },
      ...entries.map(([label, section]) =>
        h(
          "article",
          { className: "panel", key: label },
          h("h3", null, label),
          h(
            "p",
            { className: `declaration-status declaration-status--${section.status}` },
            statusLabel(section.status),
          ),
          h(
            "p",
            { className: "support-note" },
            section.status === "declared"
              ? "The release contains structured source data for this area."
              : "No canonical guidance is declared; the renderer leaves this area explicit rather than fabricating examples.",
          ),
        ),
      ),
    ),
  );
}
