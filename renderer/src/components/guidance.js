// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import React from "react";

import { Section, DefinitionList, CopyControl, EmptyState, humanize } from "./shared.js";

const h = React.createElement;

export function GuidanceSection({ id, title, guidance }) {
  const declared = guidance.status === "declared" && guidance.value;
  return h(
    Section,
    { id, title, canonical: true },
    declared
      ? id === "voice" && isStructuredVoice(guidance.value)
        ? h(StructuredVoice, { value: guidance.value })
        : id === "usage" && (
            Array.isArray(guidance.value.sections)
            || Object.hasOwn(guidance.value, "legal")
          )
          ? h(StructuredUsage, { value: guidance.value })
          : h(GuidanceValue, { value: guidance.value })
      : h(EmptyState, {
          title: `${title} not declared`,
          message:
            "The canonical Identity source does not currently declare this guidance. The renderer does not infer or invent it.",
        }),
  );
}

export function isStructuredVoice(value) {
  return value && typeof value === "object" && !Array.isArray(value)
    && ["foundation", "characteristics", "contexts", "localization"].some(
      (key) => Object.hasOwn(value, key),
    );
}

export function StructuredVoice({ value }) {
  const { foundation, localization } = value;
  const characteristics = value.characteristics || [];
  const characteristicLabels = new Map(
    characteristics.map((entry) => [entry.id, entry.label]),
  );
  return h(
    "div",
    { className: "section-stack" },
    foundation
      ? h(
          "article",
          { className: "panel", "data-voice-foundation": true },
          h("h3", null, "Project profile"),
          h(VoiceText, { title: "Purpose", value: foundation.purpose, copy: true }),
          h(VoiceText, { title: "Positioning", value: foundation.positioning, copy: true }),
          h(VoiceList, { title: "Audience", values: foundation.audience }),
          h(VoiceList, { title: "Personality", values: foundation.personality }),
        )
      : null,
    characteristics.length
      ? h(
          "article",
          { className: "panel" },
          h("h3", null, "Voice characteristics"),
          ...characteristics.map((entry) => h(
            "section",
            { key: entry.id },
            h("h4", null, entry.label),
            h("p", null, entry.description),
          )),
        )
      : null,
    ...(value.contexts || []).map((context) => h(
      "article",
      { className: "panel", key: context.id, "data-voice-context": context.id },
      h("h3", null, context.label),
      ...["audience", "intent", "tone", "naming", "capitalization", "punctuation"]
        .map((key) => h(VoiceText, {
          key,
          title: humanize(key),
          value: context[key],
        })),
      h(VoiceList, {
        title: "Characteristics",
        values: context.characteristics?.map((id) => characteristicLabels.get(id) || id),
      }),
      h(VoiceList, { title: "Preferred vocabulary", values: context.preferredVocabulary }),
      h(VoiceList, { title: "Avoided language", values: context.avoidedLanguage }),
      h(VoiceExamples, { title: "Approved examples", examples: context.examples, copy: true }),
      h(VoiceExamples, { title: "Anti-examples", examples: context.antiExamples }),
    )),
    localization
      ? h(
          "article",
          { className: "panel", "data-voice-localization": true },
          h("h3", null, "Localization"),
          h(VoiceText, { title: "Source language", value: localization.sourceLanguage }),
          localization.supportedLanguages?.length
            ? h(
                "section",
                null,
                h("h4", null, "Supported languages"),
                h(
                  "ul",
                  { className: "guidance-list" },
                  ...localization.supportedLanguages.map((language) => h(
                    "li",
                    { key: language.tag },
                    `${language.tag} · ${language.coverage}`,
                    language.notes ? h("p", null, language.notes) : null,
                  )),
                ),
              )
            : null,
          h(VoiceText, { title: "Fallback", value: localization.fallback }),
        )
      : null,
  );
}

export function VoiceText({ title, value, copy = false }) {
  return typeof value === "string" && value.length
    ? h(
        "section",
        null,
        h("h4", null, title),
        h("p", null, value),
        copy ? h(CopyControl, { label: title, value }) : null,
      )
    : null;
}

export function VoiceList({ title, values }) {
  return values?.length
    ? h(
        "section",
        null,
        h("h4", null, title),
        h(
          "ul",
          { className: "guidance-list" },
          ...values.map((value) => h("li", { key: value }, value)),
        ),
      )
    : null;
}

export function VoiceExamples({ title, examples, copy = false }) {
  return examples?.length
    ? h(
        "section",
        null,
        h("h4", null, title),
        h(
          "ul",
          { className: "guidance-list" },
          ...examples.map((example) => h(
            "li",
            { key: example.id },
            h("p", null, example.text),
            h("p", { className: "support-note" }, example.rationale),
            copy ? h(CopyControl, { label: `${title}: ${example.id}`, value: example.text }) : null,
          )),
        ),
      )
    : null;
}

export function StructuredUsage({ value }) {
  const { sections = [], legal, ...remaining } = value;
  return h(
    "div",
    { className: "section-stack" },
    ...sections.map((section) => h(
      "article",
      { className: "panel", key: section.id, "data-usage-section": section.id },
      h("h3", null, section.title),
      h("p", null, section.description),
      ...section.rules.map((rule) => h(
        "section",
        {
          key: rule.id,
          "data-usage-rule": rule.id,
          "data-usage-kind": rule.kind,
          "data-usage-category": rule.category,
        },
        h("h4", null, `${rule.kind === "do" ? "Do" : "Don't"} · ${rule.category}`),
        h("p", null, rule.instruction),
        h("p", { className: "support-note" }, rule.rationale),
        h(
          "ul",
          { className: "guidance-list" },
          ...rule.details.map((detail) => h("li", { key: detail }, detail)),
        ),
        h("p", null, h("strong", null, "Contexts: "), rule.contexts.join(", ")),
      )),
    )),
    legal
      ? h(
          "article",
          { className: "panel", "data-legal-guidance": true },
          h("h3", null, "Legal guidance"),
          h(LegalGuidance, { legal }),
        )
      : null,
    Object.keys(remaining).length ? h(GuidanceValue, { value: remaining }) : null,
  );
}

export function LegalGuidance({ legal }) {
  return h(
    "div",
    null,
    h(DefinitionList, {
      entries: [
        ["Trademark rules", legal.trademark],
        ["Copyright", legal.copyright],
        ["Attribution", legal.attribution],
      ],
    }),
    legal.thirdPartyLicenses?.length
      ? h(
          "section",
          { "data-third-party-licenses": true },
          h("h4", null, "Third-party asset licenses"),
          h(
            "ul",
            { className: "guidance-list" },
            ...legal.thirdPartyLicenses.map((license) => h(
              "li",
              { key: `${license.name}-${license.spdx}` },
              h("strong", null, license.name),
              h(DefinitionList, {
                entries: [
                  ["Asset license", license.spdx],
                  ["Attribution", license.attribution],
                ],
              }),
            )),
          ),
        )
      : null,
  );
}

export function AssetRights({ asset }) {
  const approval = typeof asset.approval === "string"
    ? asset.approval
    : asset.approval?.id;
  const usage = asset.usage;
  return h(
    "div",
    { "data-asset-rights": asset.assetId || asset.id },
    h(DefinitionList, {
      entries: [
        ["Asset license", asset.license?.spdx || "Not declared"],
        ["License review", asset.license?.status || "Not declared"],
        ["Attribution", asset.license?.attribution || "Not declared"],
        [asset.assetId ? "Selection approval" : "Approval", approval || "Not declared"],
        ...(asset.approval?.subject ? [["Selection subject", asset.approval.subject]] : []),
        ["Creator", asset.origin?.creator || "Not declared"],
        ["Method", asset.origin?.method || "Not declared"],
        ["Source", asset.origin?.source || "Not declared"],
        ["Captured", asset.origin?.capturedAt || "Not declared"],
        ["SHA-256", asset.sha256],
        ["Safe zone", usage?.safeZone || "Not declared"],
        ["Minimum size", usage?.minimumSize || "Not declared"],
      ],
    }),
    h("h4", null, "Usage restrictions"),
    usage?.restrictions?.length
      ? h(
          "ul",
          { className: "guidance-list" },
          ...usage.restrictions.map((restriction) => h("li", { key: restriction }, restriction)),
        )
      : h("p", { className: "support-note" }, "No restrictions declared."),
  );
}

export function GuidanceValue({ value }) {
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
              { className: "structured-value", tabIndex: 0 },
              JSON.stringify(entry, null, 2),
            ),
      ),
    ),
  );
}
