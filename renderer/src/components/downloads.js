// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import React from "react";

import { joinAssetUrl } from "../model.js";
import { Section, DefinitionList, EmptyState } from "./shared.js";
import { AssetRights } from "./guidance.js";

const h = React.createElement;

export function DownloadsSection({ packages, assetBaseUrl }) {
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

export function ProvenanceSection({ model, assetBaseUrl, publication }) {
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
            publication.inventoryDigest ? h("p", { className: "support-note" },
              "Published asset inventory SHA-256: ", h("code", null, publication.inventoryDigest)) : null,
            publication.archivePath ? h("p", null, h("a", {
              className: "text-link", href: joinAssetUrl(assetBaseUrl, publication.archivePath), download: true,
            }, "Download published kit")) : null,
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
          h(AssetRights, { asset }),
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
