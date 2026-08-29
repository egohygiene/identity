// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import React from "react";

import {
  SECTION_DEFINITIONS,
  assertBrandKitViewModel,
  colorValueToCss,
  joinAssetUrl,
  sourceDataUrl,
  statusLabel,
  tokenValueToText,
} from "./model.js";

const h = React.createElement;

export function BrandKitPage({ model, assetBaseUrl = "./", publication = null }) {
  assertBrandKitViewModel(model);
  const colorTokens = model.tokens.filter((token) => token.type === "color");
  const typographyTokens = model.tokens.filter(
    (token) =>
      token.type === "fontFamily" || token.path.startsWith("typography."),
  );

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
        h(
          "a",
          {
            className: "button",
            href: joinAssetUrl(
              assetBaseUrl,
              "packages/brand-kit/brand-kit.zip",
            ),
            download: true,
          },
          "Download complete kit",
        ),
      ),
    ),
    h(
      "div",
      { className: "layout" },
      h(SectionNavigation, { model }),
      h(
        "main",
        { id: "main-content", tabIndex: -1 },
        h(OverviewSection, { model }),
        h(AssetsSection, { assets: model.assets, assetBaseUrl }),
        h(ColorSection, { tokens: colorTokens }),
        h(TypographySection, { tokens: typographyTokens }),
        h(GuidanceSection, {
          id: "voice",
          title: "Voice and personality",
          guidance: model.guidance.voice,
        }),
        h(GuidanceSection, {
          id: "usage",
          title: "Usage rules",
          guidance: model.guidance.usage,
        }),
        h(CreativeDirectionSection, { support: model.support }),
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
        h(StudioSection, { model }),
        h(DownloadsSection, {
          packages: model.packages,
          assetBaseUrl,
        }),
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

function SectionNavigation({ model }) {
  const sections = SECTION_DEFINITIONS.filter(([id]) => {
    if (id === "design-system") {
      return Boolean(model.designSystem);
    }
    if (id === "press-kit") {
      return Boolean(model.pressKit);
    }
    return true;
  });
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

function DesignSystemSection({ designSystem, assetBaseUrl }) {
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

function PressKitSection({ pressKit: view, assetBaseUrl }) {
  const pressKit = view.pressKit;
  const boilerplates = new Map(
    pressKit.boilerplates.map((boilerplate) => [boilerplate.kind, boilerplate]),
  );
  const legal = pressKit.guidance.legal;
  return h(
    Section,
    {
      id: "press-kit",
      title: "Press and media kit",
      canonical: true,
    },
    h(
      "div",
      { className: "section-stack" },
      h(
        "article",
        { className: "panel" },
        h("p", { className: "eyebrow" }, "Generated projection"),
        h("h3", null, pressKit.project.displayName),
        h(
          "p",
          null,
          "This public view consumes only explicitly approved Press Kit records. Empty sections are declarations of absence, not invitations to invent facts.",
        ),
        h(DefinitionList, {
          entries: [
            ["Project kind", pressKit.project.kind],
            ["Projection schema", pressKit.schema],
            ["Source digest", pressKit.source.digest],
            ["Projection version", pressKit.source.projectionVersion],
          ],
        }),
      ),
      h(
        "article",
        { className: "panel" },
        h("h3", null, "Approved boilerplate"),
        h("h4", null, "Short"),
        h("p", null, boilerplates.get("short")?.text),
        h(
          "p",
          { className: "support-note" },
          `Approval: ${boilerplates.get("short")?.approval?.id}`,
        ),
        h("h4", null, "Long"),
        h("p", null, boilerplates.get("long")?.text),
        h(
          "p",
          { className: "support-note" },
          `Approval: ${boilerplates.get("long")?.approval?.id}`,
        ),
      ),
      pressKit.facts.length
        ? h(
            "article",
            { className: "panel" },
            h("h3", null, "Key facts"),
            h(DefinitionList, {
              entries: pressKit.facts.map((fact) => [fact.label, fact.value]),
            }),
          )
        : h(
            "article",
            { className: "panel empty-state" },
            h("h3", null, "Key facts not declared"),
            h("p", null, "The renderer does not infer or invent them."),
          ),
      pressKit.links.length || pressKit.contacts.length
        ? h(
            "article",
            { className: "panel" },
            h("h3", null, "Links and contact"),
            pressKit.links.length
              ? h(
                  "ul",
                  { className: "guidance-list" },
                  ...pressKit.links.map((link) =>
                    h(
                      "li",
                      { key: link.id },
                      h("a", { href: link.url }, link.label),
                      ` · ${link.kind}`,
                    ),
                  ),
                )
              : null,
            pressKit.contacts.length
              ? h(
                  "dl",
                  { className: "definition-list" },
                  ...pressKit.contacts.flatMap((contact) => [
                    h("dt", { key: `${contact.id}-label` }, contact.label),
                    h(
                      "dd",
                      { key: `${contact.id}-value` },
                      contact.kind === "email"
                        ? h("a", { href: `mailto:${contact.value}` }, contact.value)
                        : contact.kind === "url"
                          ? h("a", { href: contact.value }, contact.value)
                          : contact.value,
                      contact.notes ? ` — ${contact.notes}` : "",
                    ),
                  ]),
                )
              : null,
          )
        : h(
            "article",
            { className: "panel empty-state" },
            h("h3", null, "Links and contact not declared"),
            h("p", null, "The renderer does not infer or invent them."),
          ),
      pressKit.team.length
        ? h(
            "article",
            { className: "panel" },
            h("h3", null, "Public team information"),
            h(
              "div",
              { className: "handbook-principles" },
              ...pressKit.team.map((member) =>
                h(
                  "section",
                  { key: member.id },
                  h("h4", null, member.name),
                  h("p", null, member.role),
                  member.bio ? h("p", { className: "support-note" }, member.bio) : null,
                ),
              ),
            ),
          )
        : h(
            "article",
            { className: "panel empty-state" },
            h("h3", null, "Public team information not declared"),
            h("p", null, "The renderer does not infer or invent bios."),
          ),
      pressKit.assets.length
        ? h(
            "article",
            { className: "panel" },
            h("h3", null, "Approved media assets"),
            h(
              "div",
              { className: "download-list" },
              ...pressKit.assets.map((asset) =>
                h(
                  "div",
                  { className: "download-row", key: asset.id },
                  h(
                    "div",
                    null,
                    h("h4", null, asset.label),
                    h("p", { className: "support-note" }, asset.notes),
                    h(
                      "p",
                      { className: "support-note" },
                      `${asset.mediaType} · ${asset.license.spdx}`,
                    ),
                  ),
                  h(
                    "a",
                    {
                      className: "button button--secondary",
                      href: joinAssetUrl(assetBaseUrl, asset.downloadPath),
                      download: true,
                    },
                    "Download",
                  ),
                ),
              ),
            ),
          )
        : h(
            "article",
            { className: "panel empty-state" },
            h("h3", null, "Approved media assets not declared"),
            h("p", null, "The renderer does not substitute other Brand Kit assets."),
          ),
      h(
        "article",
        { className: "panel" },
        h("h3", null, "Usage and legal guidance"),
        pressKit.guidance.usageRules.length
          ? h(
              "ul",
              { className: "guidance-list" },
              ...pressKit.guidance.usageRules.map((rule) =>
                h(
                  "li",
                  { key: rule.id },
                  h("strong", null, `${rule.kind} · ${rule.category}: `),
                  rule.instruction,
                ),
              ),
            )
          : h("p", { className: "support-note" }, "Public usage rules are not declared."),
        legal.status === "declared"
          ? h(DefinitionList, {
              entries: [
                ["Trademark", legal.value.trademark],
                ["Copyright", legal.value.copyright],
                ["Attribution", legal.value.attribution],
              ],
            })
          : h("p", { className: "support-note" }, "Public legal guidance is not declared."),
      ),
      h(
        "article",
        { className: "panel" },
        h("h3", null, "Press Kit downloads"),
        h(
          "div",
          { className: "download-list" },
          ...view.artifacts.map((artifact) =>
            h(
              "div",
              { className: "download-row", key: artifact.id },
              h(
                "div",
                null,
                h("h4", null, artifact.label),
                h("p", { className: "support-note" }, artifact.intendedUse),
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

function AssetsSection({ assets, assetBaseUrl }) {
  return h(
    Section,
    { id: "logos", title: "Logo and marks", preview: true },
    assets.length === 0
      ? h(EmptyState, {
          title: "No approved marks",
          message:
            "The current release does not declare a public logo or mark.",
        })
      : h(
          "div",
          { className: "asset-grid" },
          ...assets.map((asset) =>
            h(
              "article",
              { className: "panel asset-card", key: asset.id },
              h(
                "div",
                { className: "asset-preview" },
                asset.mediaType.startsWith("image/")
                  ? h("img", {
                      src: sourceDataUrl(asset, assetBaseUrl),
                      alt: asset.altText,
                    })
                  : h("p", null, "Preview unavailable for this media type."),
              ),
              h("h3", null, asset.label),
              h(DefinitionList, {
                entries: [
                  ["Format", asset.mediaType],
                  ["Dimensions", asset.dimensions],
                  ["Intended use", asset.intendedUse],
                  ["Availability", humanize(asset.availability)],
                  ["SHA-256", asset.sha256],
                  [
                    "Safe zone",
                    asset.safeZone === null || asset.safeZone === undefined
                      ? "Not declared"
                      : `${Math.round(asset.safeZone * 100)}%`,
                  ],
                  [
                    "License",
                    asset.license
                      ? `${asset.license.spdx} · ${asset.license.status}`
                      : "Not declared",
                  ],
                ],
              }),
              asset.downloadPath
                ? h(
                    "a",
                    {
                      className: "text-link",
                      href: joinAssetUrl(assetBaseUrl, asset.downloadPath),
                      download: true,
                    },
                    `Download ${asset.label}`,
                  )
                : h(
                    "p",
                    { className: "support-note" },
                    "This approved source is embedded for review but has no generated download path.",
                  ),
            ),
          ),
        ),
  );
}

function ColorSection({ tokens }) {
  return h(
    Section,
    { id: "colors", title: "Color palette and approved pairings", preview: true },
    tokens.length === 0
      ? h(EmptyState, {
          title: "No color tokens",
          message:
            "The current release does not declare color tokens that the renderer can preview.",
        })
      : h(
          "div",
          { className: "section-stack" },
          h(
            "div",
            { className: "color-grid" },
            ...tokens.map((token) => {
              const cssValue = colorValueToCss(token.value);
              return h(
                "article",
                { className: "panel color-card", key: token.path },
                h("div", {
                  className: "color-swatch",
                  role: "img",
                  style: cssValue ? { backgroundColor: cssValue } : undefined,
                  "aria-label": cssValue
                    ? `${token.path} previewed as ${cssValue}`
                    : `${token.path} cannot be previewed`,
                }),
                h("h3", null, token.path),
                h("p", { className: "token-value" }, tokenValueToText(token)),
                h(CopyControl, {
                  label: token.path,
                  value: tokenValueToText(token),
                }),
                h(
                  "p",
                  { className: "support-note" },
                  `Source layer: ${token.sourceLayer}`,
                ),
              );
            }),
          ),
          h(EmptyState, {
            title: "Approved pairings not declared",
            message:
              "Semantic colors are previewed individually, but the current release does not declare canonical color pairings. The renderer does not infer combinations.",
          }),
        ),
  );
}

function TypographySection({ tokens }) {
  const hasTypeScale = tokens.some((token) =>
    [".size", ".lineHeight", ".line-height", ".weight", ".scale"].some(
      (fragment) => token.path.includes(fragment),
    ),
  );

  return h(
    Section,
    { id: "typography", title: "Typography and type scale", preview: true },
    tokens.length === 0
      ? h(EmptyState, {
          title: "Typography not declared",
          message:
            "The current release does not contain typography tokens. System defaults remain in effect.",
        })
      : h(
          "div",
          { className: "section-stack" },
          h(
            "div",
            { className: "typography-stack" },
            ...tokens.map((token) =>
              h(
                "article",
                { className: "panel typography-sample", key: token.path },
                h("p", { className: "eyebrow" }, token.path),
                h(
                  "p",
                  {
                    className: "type-preview",
                    style:
                      token.type === "fontFamily" && Array.isArray(token.value)
                        ? { fontFamily: token.value.join(", ") }
                        : undefined,
                  },
                  "Clarity makes a system easier to trust.",
                ),
                h("p", { className: "token-value" }, tokenValueToText(token)),
                h(CopyControl, {
                  label: token.path,
                  value: tokenValueToText(token),
                }),
              ),
            ),
          ),
          hasTypeScale
            ? null
            : h(EmptyState, {
                title: "Type scale not declared",
                message:
                  "Font family tokens are available, but the current release does not declare canonical sizes, weights, or line-height relationships.",
              }),
        ),
  );
}

function GuidanceSection({ id, title, guidance }) {
  const declared = guidance.status === "declared" && guidance.value;
  return h(
    Section,
    { id, title, canonical: true },
    declared
      ? h(GuidanceValue, { value: guidance.value })
      : h(EmptyState, {
          title: `${title} not declared`,
          message:
            "The canonical Identity source does not currently declare this guidance. The renderer does not infer or invent it.",
        }),
  );
}

function GuidanceValue({ value }) {
  if (Array.isArray(value)) {
    return h(
      "ul",
      { className: "guidance-list" },
      ...value.map((entry, index) =>
        h("li", { key: `${String(entry)}-${index}` }, String(entry)),
      ),
    );
  }
  if (!value || typeof value !== "object") {
    return h("p", null, String(value));
  }

  return h(
    "div",
    { className: "guidance-grid" },
    ...Object.entries(value).map(([key, entry]) =>
      h(
        "article",
        { className: "panel", key },
        h("h3", null, humanize(key)),
        Array.isArray(entry)
          ? h(
              "ul",
              { className: "guidance-list" },
              ...entry.map((item, index) =>
                h("li", { key: `${String(item)}-${index}` }, String(item)),
              ),
            )
          : h(
              "pre",
              { className: "structured-value" },
              JSON.stringify(entry, null, 2),
            ),
      ),
    ),
  );
}

function CreativeDirectionSection({ support }) {
  const entries = [
    ["Motion", support.motion],
    ["Imagery", support.imagery],
    ["Mascot", support.mascot],
  ];
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

function DownloadsSection({ packages, assetBaseUrl }) {
  return h(
    Section,
    { id: "downloads", title: "Downloads and package installation" },
    packages.length === 0
      ? h(EmptyState, {
          title: "No packages available",
          message:
            "This release does not expose downloadable generated packages.",
        })
      : h(
          "div",
          { className: "download-list" },
          ...packages.map((entry) =>
            h(
              "article",
              { className: "download-row", key: entry.id },
              h(
                "div",
                null,
                h("h3", null, entry.label),
                h("p", null, entry.intendedUse),
                h(
                  "p",
                  { className: "support-note" },
                  `${entry.mediaType} · ${entry.path}`,
                ),
              ),
              h(
                "a",
                {
                  className: "button button--secondary",
                  href: joinAssetUrl(assetBaseUrl, entry.path),
                  download: true,
                },
                "Download",
              ),
            ),
          ),
        ),
  );
}

function ProvenanceSection({ model, assetBaseUrl, publication }) {
  return h(
    Section,
    {
      id: "provenance",
      title: "Provenance, licenses, changelog, and support",
    },
    h(
      "div",
      { className: "provenance-grid" },
      publication
        ? h(
            "article",
            { className: "panel" },
            h("h3", null, "Published surface"),
            h(
              "p",
              null,
              `This page projects immutable Identity release ${publication.releaseTag}.`,
            ),
            h(
              "p",
              null,
              h(
                "a",
                { className: "text-link", href: publication.releaseUrl },
                "Inspect immutable release",
              ),
            ),
            h(
              "p",
              null,
              h(
                "a",
                {
                  className: "text-link",
                  href: joinAssetUrl(assetBaseUrl, publication.manifestPath),
                  download: true,
                },
                "Download publication manifest",
              ),
            ),
            h("p", { className: "support-note" }, "Manifest SHA-256"),
            h("code", null, publication.manifestSha256),
          )
        : null,
      h(
        "article",
        { className: "panel" },
        h("h3", null, "Release evidence"),
        h(DefinitionList, {
          entries: [
            ["Immutable ID", model.release.immutableId],
            ["Source digest", model.release.sourceDigest],
            ["Release status", model.release.status],
            ["Contract", model.schema],
          ],
        }),
      ),
      ...model.assets.map((asset) =>
        h(
          "article",
          { className: "panel", key: asset.id },
          h("h3", null, `${asset.label} governance`),
          h(DefinitionList, {
            entries: [
              [
                "License",
                asset.license
                  ? `${asset.license.spdx} · ${asset.license.status}`
                  : "Not declared",
              ],
              [
                "Attribution",
                asset.license?.attribution || "Not declared",
              ],
              ["Approval", asset.approval || "Not declared"],
              ["Creator", asset.origin?.creator || "Not declared"],
              ["Method", asset.origin?.method || "Not declared"],
              ["Source", asset.origin?.source || "Not declared"],
              ["Captured", asset.origin?.capturedAt || "Not declared"],
            ],
          }),
        ),
      ),
      h(
        "article",
        { className: "panel" },
        h("h3", null, "Changelog and support"),
        h(
          "p",
          null,
          "The immutable release ID is the comparison boundary for changelog entries. Support status is represented by explicit declared, not-declared, and unsupported states throughout this page.",
        ),
        h(
          "a",
          { className: "text-link", href: model.project.repository },
          "Review source and release history",
        ),
      ),
    ),
  );
}

function Section({ id, title, preview = false, canonical = false, children }) {
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

function DefinitionList({ entries }) {
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

function CopyControl({ label, value }) {
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

function EmptyState({ title, message }) {
  return h(
    "div",
    { className: "empty-state", role: "note" },
    h("h3", null, title),
    h("p", null, message),
  );
}

function humanize(value) {
  return value
    .split(/[-_]/u)
    .filter(Boolean)
    .map((segment) => `${segment[0].toUpperCase()}${segment.slice(1)}`)
    .join(" ");
}

function shouldUseCode(term) {
  return [
    "Immutable ID",
    "Source digest",
    "Contract",
    "SHA-256",
  ].includes(term);
}
