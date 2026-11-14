// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import React from "react";

import { joinAssetUrl } from "../model.js";
import { Section, DefinitionList, CopyControl, humanize } from "./shared.js";
import { LegalGuidance, AssetRights } from "./guidance.js";

const h = React.createElement;

export function PressKitSection({ pressKit: view, assetBaseUrl }) {
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
        ...["short", "paragraph", "long"].flatMap((kind) => {
          const boilerplate = boilerplates.get(kind);
          return boilerplate
            ? [h(
                "section",
                { key: kind },
                h("h4", null, humanize(kind)),
                h("p", null, boilerplate.text),
                h(CopyControl, {
                  label: `${humanize(kind)} description`,
                  value: boilerplate.text,
                }),
                boilerplate.approval?.id
                  ? h(
                      "p",
                      { className: "support-note" },
                      `Approval: ${boilerplate.approval.id}`,
                    )
                  : null,
              )]
            : [];
        }),
      ),
      pressKit.facts.length
        ? h(
            "article",
            { className: "panel" },
            h("h3", null, "Key facts"),
            h(
              "dl",
              { className: "definition-list" },
              ...pressKit.facts.flatMap((fact) => [
                h("dt", { key: `${fact.id}-label` }, fact.label),
                h(
                  "dd",
                  { key: `${fact.id}-value` },
                  h("p", null, fact.value),
                  h(CopyControl, { label: fact.label, value: fact.value }),
                ),
              ]),
            ),
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
                    h("p", { className: "support-note" }, asset.mediaType),
                    h(AssetRights, { asset }),
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
          ? h(LegalGuidance, { legal: legal.value })
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
