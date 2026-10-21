// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import React from "react";

import { joinAssetUrl } from "./model.js";

const h = React.createElement;
const GITHUB_PREVIEW_GUIDE = "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview";

// These are the two existing native output targets, not a platform fact catalog.
const PRESENTATION_TARGETS = new Map([
  ["github-social-preview", {
    profile: "github", title: "GitHub repository preview",
    instruction: "Review the image and its usage terms, then upload it under repository Settings → Social preview → Edit.",
    guide: GITHUB_PREVIEW_GUIDE,
  }],
  ["social-card-1200x630", {
    profile: "social", title: "Generic link card",
    instruction: "This is a portable card. Check the destination’s current requirements before using it; it does not declare support for a particular social platform.",
  }],
]);

export function selectedPresentationProfiles(model) {
  const assets = new Map(model.assets.map((asset) => [asset.id, asset]));
  return (model.downloads || []).flatMap((download) => {
    const target = PRESENTATION_TARGETS.get(download.id);
    const source = assets.get(download.sourceAssetId);
    return target && target.profile === download.profile && download.mediaType === "image/png"
      && source && source.sha256 === download.sourceSha256
      ? [{ ...target, download, source }]
      : [];
  });
}

export function presentationCopy(model) {
  const pressKit = model.pressKit?.pressKit;
  return [
    { id: "project-name", label: "Project name", value: model.project.displayName },
    { id: "project-tagline", label: "Project tagline", value: model.project.tagline },
    { id: "project-repository", label: "Project repository", value: model.project.repository },
    ...(pressKit?.boilerplates || []).map((entry) => ({
      id: `boilerplate:${entry.id}`, label: `${entry.kind} description`, value: entry.text,
    })),
    ...(pressKit?.facts || []).map((entry) => ({
      id: `fact:${entry.id}`, label: entry.label, value: entry.value,
    })),
    ...(pressKit?.links || []).map((entry) => ({
      id: `link:${entry.id}`, label: entry.label, value: entry.url,
    })),
  ];
}

export function PresentationProfiles({ model, assetBaseUrl, CopyControl, DefinitionList, AssetRights }) {
  const profiles = selectedPresentationProfiles(model);
  if (!profiles.length) return null;
  return h(React.Fragment, null,
    h("p", null, "Download a selected image and reuse the supplied text below. Review the result and the destination’s requirements before uploading."),
    h("div", { className: "asset-grid" },
      ...profiles.map(({ title, instruction, guide, download, source }) => h("article", {
        className: "panel", key: download.id, "data-presentation-profile": download.profile,
      },
      h("h3", null, title),
      h("img", {
        className: "presentation-preview", src: joinAssetUrl(assetBaseUrl, download.path),
        alt: source.altText, loading: "lazy",
      }),
      h(DefinitionList, { entries: [
        ["Dimensions", download.dimensions], ["Format", download.mediaType],
        ["Approved source", download.sourceAssetId], ["Intended use", source.intendedUse],
      ] }),
      h("p", null, instruction),
      guide ? h("p", null, h("a", { href: guide }, "Current GitHub upload requirements")) : null,
      h("a", { className: "button button--secondary", href: joinAssetUrl(assetBaseUrl, download.path), download: true }, `Download ${title}`),
      h(AssetRights, { asset: source }),
      )),
    ),
    h("article", { className: "panel" },
      h("h3", null, "Copy text and links"),
      h("p", { className: "support-note" }, "Descriptions, package identifiers, discovery keywords and account links appear here when supplied in the approved Press Kit. Text is copied as supplied; check each destination’s length and formatting limits."),
      ...presentationCopy(model).map((entry) => h("div", {
        className: "presentation-copy", key: entry.id, "data-presentation-copy": entry.id,
      },
      h("h4", null, entry.label),
      h("p", null, entry.value),
      h(CopyControl, { label: entry.label, value: entry.value }),
      )),
      !model.pressKit ? h("p", { className: "support-note" }, "Approved Press Kit descriptions, discovery facts and account links are not declared for this kit.") : null,
    ),
  );
}
