// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import React from "react";

import { normalizeArtifactPath } from "../artifact-paths.js";
import { joinAssetUrl, sourceDataUrl } from "../model.js";
import { Section, DefinitionList, EmptyState, humanize } from "./shared.js";
import { AssetRights } from "./guidance.js";

const h = React.createElement;

export function AssetsSection({ assets, downloads, assetBaseUrl }) {
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
              asset.kind ? h("p", { className: "eyebrow" }, humanize(asset.kind)) : null,
              asset.notes ? h("p", null, asset.notes) : null,
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
              asset.usage ? h(AssetRights, { asset }) : null,
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
              h(AssetDownloads, {
                asset,
                downloads: downloads.filter((download) =>
                  download.sourceAssetId === asset.id
                  && (!asset.downloadPath || normalizeArtifactPath(download.path)
                    !== normalizeArtifactPath(asset.downloadPath)),
                ),
                assetBaseUrl,
              }),
            ),
          ),
        ),
  );
}

export function AssetDownloads({ asset, downloads, assetBaseUrl }) {
  return downloads.length
    ? h(
        "section",
        { "data-asset-downloads": asset.id },
        h("h4", null, "Available downloads"),
        h(
          "ul",
          { className: "guidance-list" },
          ...downloads.map((download) => h(
            "li",
            { key: download.id },
            h("a", {
              className: "text-link",
              href: joinAssetUrl(assetBaseUrl, download.path),
              download: true,
            }, download.label),
            h("p", { className: "support-note" },
              `${download.dimensions} · ${download.mediaType} · ${download.profile}`,
            ),
            h(DefinitionList, { entries: [
              ["Source asset", download.sourceAssetId],
              ["Source SHA-256", download.sourceSha256],
            ] }),
          )),
        ),
      )
    : null;
}
