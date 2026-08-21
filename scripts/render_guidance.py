#!/usr/bin/env python3
# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Render validated Identity v1 voice and usage guidance without inventing prose."""

from __future__ import annotations

import argparse
from html import escape
import json
from pathlib import Path
import sys
from typing import Any, Sequence

import validate_identity as validator

BRAND_GUIDANCE_SCHEMA = "identity.brand-guidance/v1"


class GuidanceError(ValueError):
    """Raised when reviewed guidance cannot produce the requested projection."""


def load_json(path: Path) -> dict[str, Any]:
    """Load one already-validated JSON document."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise GuidanceError(f"document must be an object: {path}")
    return value


def guidance_documents(
    repository_root: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Load project, voice, usage, and decisions through declared local paths."""

    project = load_json(repository_root / ".identity/identity.json")
    documents = project["documents"]
    voice = load_json(repository_root / documents["guidance"]["voice"])
    usage = load_json(repository_root / documents["guidance"]["usage"])
    approvals = load_json(repository_root / documents["approvals"])
    return project, voice, usage, approvals


def context_rules(sections: list[dict[str, Any]], context: str | None) -> list[dict[str, Any]]:
    """Return rules that apply globally or to the selected consumer context."""

    rules = [rule for section in sections for rule in section["rules"]]
    if context is None:
        return rules
    return [rule for rule in rules if context in rule["contexts"] or "all" in rule["contexts"]]


def is_public(value: dict[str, Any]) -> bool:
    """Return whether one governed record is approved for public projection."""

    governance = value["governance"]
    return governance["state"] == "approved" and governance["visibility"] == "public"


def approval_ids(value: object) -> set[str]:
    """Collect decision IDs referenced by a projected model."""

    result: set[str] = set()
    if isinstance(value, dict):
        governance = value.get("governance")
        if isinstance(governance, dict) and isinstance(governance.get("approval"), str):
            result.add(governance["approval"])
        for child in value.values():
            result.update(approval_ids(child))
    elif isinstance(value, list):
        for child in value:
            result.update(approval_ids(child))
    return result


def build_view_model(
    repository_root: Path,
    context: str | None = None,
    audience: str = "review",
) -> dict[str, Any]:
    """Build the stable renderer model from validated, human-reviewed source."""

    diagnostics = validator.validate_identity(repository_root)
    if diagnostics:
        first = diagnostics[0]
        raise GuidanceError(f"[{first.code}] {first.path}: {first.message}")
    if audience not in {"public", "review"}:
        raise GuidanceError("audience must be public or review")
    project, voice, usage, approvals = guidance_documents(repository_root)

    contexts = voice["contexts"]
    if context is not None:
        contexts = [item for item in contexts if item["id"] == context]
        if not contexts:
            available = ", ".join(item["id"] for item in voice["contexts"])
            raise GuidanceError(f"unknown context {context!r}; available: {available}")
    if audience == "public":
        contexts = [item for item in contexts if is_public(item)]
        contexts = [
            {
                **item,
                "examples": [value for value in item["examples"] if is_public(value)],
                "antiExamples": [
                    value for value in item["antiExamples"] if is_public(value)
                ],
            }
            for item in contexts
        ]
    characteristic_ids = {
        identifier
        for item in contexts
        for identifier in item["characteristics"]
    }
    characteristics = voice["characteristics"]
    if context is not None:
        characteristics = [
            item for item in characteristics if item["id"] in characteristic_ids
        ]
    if audience == "public":
        characteristics = [item for item in characteristics if is_public(item)]

    rules = context_rules(usage["sections"], context)
    if audience == "public":
        rules = [item for item in rules if is_public(item)]
    selected_rule_ids = {item["id"] for item in rules}
    sections = []
    for section in usage["sections"]:
        selected = [item for item in section["rules"] if item["id"] in selected_rule_ids]
        if selected:
            sections.append({**section, "rules": selected})

    downloads = [
        item
        for item in usage["assets"]
        if item["status"] == "active"
        and item["availability"] == "public"
        and item["governance"]["state"] == "approved"
    ]
    legacy_assets = [item for item in usage["assets"] if item["status"] == "legacy"]
    if audience == "public":
        legacy_assets = [
            item
            for item in legacy_assets
            if item["availability"] == "public" and is_public(item)
        ]
    model = {
        "schema": BRAND_GUIDANCE_SCHEMA,
        "audience": audience,
        "project": {
            field: project["project"][field]
            for field in ("id", "displayName", "tagline", "repository")
        },
        "selectedContext": context,
        "foundation": voice["foundation"],
        "characteristics": characteristics,
        "contexts": contexts,
        "localization": voice["localization"],
        "sections": sections,
        "doDont": rules,
        "downloads": downloads,
        "legacyAssets": legacy_assets,
        "accessibility": usage["accessibility"],
        "legal": usage["legal"],
        "decisions": sorted(approvals["decisions"], key=lambda item: item["id"]),
    }
    if audience == "public":
        projected = {key: value for key, value in model.items() if key != "decisions"}
        referenced = approval_ids(projected)
        model["decisions"] = [
            item for item in model["decisions"] if item["id"] in referenced
        ]
    return model


def governance_label(value: dict[str, Any]) -> str:
    """Return a compact, visible lifecycle label."""

    governance = value["governance"]
    return f"{governance['state']} · {governance['visibility']}"


def render_json(model: dict[str, Any]) -> str:
    """Render the stable machine-readable projection."""

    return f"{json.dumps(model, indent=2, sort_keys=True, ensure_ascii=False)}\n"


def markdown_governance(value: dict[str, Any]) -> list[str]:
    """Render provenance and authority without hiding lifecycle state."""

    governance = value["governance"]
    approval = governance["approval"] or "pending human review"
    provenance = governance["provenance"]
    return [
        f"- State: **{governance_label(value)}**",
        f"- Approval: `{approval}`",
        (
            "- Provenance: "
            f"`{provenance['method']}` from `{provenance['source']}` "
            f"at `{provenance['capturedAt']}`"
        ),
    ]


def render_markdown(model: dict[str, Any]) -> str:
    """Render reviewed guidance as portable Markdown."""

    project = model["project"]
    foundation = model["foundation"]
    lines = [
        f"# {project['displayName']} Brand Kit",
        "",
        project["tagline"],
        "",
        f"Source: {project['repository']}",
        "",
        f"Audience: **{model['audience']}**",
        "",
    ]
    if model["selectedContext"] is not None:
        lines.extend([f"Selected context: `{model['selectedContext']}`", ""])
    lines.extend(
        [
            "## Foundation",
            "",
            f"**Purpose:** {foundation['purpose']}",
            "",
            f"**Positioning:** {foundation['positioning']}",
            "",
            f"**Audience:** {', '.join(foundation['audience'])}",
            "",
            f"**Personality:** {', '.join(foundation['personality'])}",
            "",
            *markdown_governance(foundation),
            "",
            "## Voice characteristics",
            "",
        ]
    )
    for item in model["characteristics"]:
        lines.extend(
            [
                f"### {item['label']}",
                "",
                item["description"],
                "",
                *markdown_governance(item),
                "",
            ]
        )
    lines.extend(["## Tone by context", ""])
    for context in model["contexts"]:
        lines.extend(
            [
                f"### {context['label']} (`{context['id']}`)",
                "",
                f"**Audience:** {context['audience']}",
                "",
                f"**Intent:** {context['intent']}",
                "",
                f"**Tone:** {context['tone']}",
                "",
                f"**Preferred vocabulary:** {', '.join(context['preferredVocabulary'])}",
                "",
                f"**Avoided language:** {', '.join(context['avoidedLanguage'])}",
                "",
                f"**Naming:** {context['naming']}",
                "",
                f"**Capitalization:** {context['capitalization']}",
                "",
                f"**Punctuation:** {context['punctuation']}",
                "",
                "#### Examples",
                "",
            ]
        )
        for item in context["examples"]:
            lines.extend(
                [
                    f"> {item['text']}",
                    ">",
                    f"> {item['rationale']}",
                    "",
                    *markdown_governance(item),
                    "",
                ]
            )
        lines.extend(["#### Anti-examples", ""])
        for item in context["antiExamples"]:
            lines.extend(
                [
                    f"> {item['text']}",
                    ">",
                    f"> {item['rationale']}",
                    "",
                    *markdown_governance(item),
                    "",
                ]
            )

    lines.extend(["## Usage: do / don’t", ""])
    for section in model["sections"]:
        lines.extend([f"### {section['title']}", "", section["description"], ""])
        for rule in section["rules"]:
            prefix = "Do" if rule["kind"] == "do" else "Don’t"
            lines.extend(
                [
                    f"#### {prefix}: {rule['instruction']}",
                    "",
                    rule["rationale"],
                    "",
                    *(f"- {detail}" for detail in rule["details"]),
                    f"- Contexts: {', '.join(rule['contexts'])}",
                    *markdown_governance(rule),
                    "",
                ]
            )

    lines.extend(["## Downloads", ""])
    for asset in model["downloads"]:
        lines.extend(
            [
                f"- [{asset['label']}]({asset['path']}) — `{asset['downloadName']}`",
                f"  - {asset['notes']}",
                f"  - State: **{governance_label(asset)}**",
            ]
        )
    lines.extend(["", "## Legacy assets", ""])
    for asset in model["legacyAssets"]:
        lines.extend(
            [
                f"### {asset['label']} — LEGACY / {asset['availability'].upper()}",
                "",
                asset["notes"],
                "",
                f"Replacement: `{asset['replacement']}`",
                "",
                *markdown_governance(asset),
                "",
            ]
        )

    accessibility = model["accessibility"]
    lines.extend(["## Accessibility", "", accessibility["summary"], ""])
    lines.extend(f"- {item}" for item in accessibility["rules"])
    legal = model["legal"]
    lines.extend(
        [
            "",
            "## Legal and attribution",
            "",
            f"- Trademark: {legal['trademark']}",
            f"- Copyright: {legal['copyright']}",
            f"- Attribution: {legal['attribution']}",
            "",
            "## Decision ledger",
            "",
            "| Decision | Subject | Candidate | Status | Reviewer | Evidence |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for decision in model["decisions"]:
        lines.append(
            "| "
            f"`{decision['id']}` | `{decision['subject']}` | "
            f"`{decision['candidate']}` | **{decision['status']}** | "
            f"{decision['reviewedBy']} | {decision['evidence']} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def badge(value: dict[str, Any]) -> str:
    """Render one visible lifecycle badge."""

    governance = value["governance"]
    label = governance_label(value)
    return (
        f'<span class="badge badge-{escape(governance["state"])}">'
        f"{escape(label)}</span>"
    )


def html_governance(value: dict[str, Any]) -> str:
    """Render provenance and approval metadata for one governed item."""

    governance = value["governance"]
    provenance = governance["provenance"]
    approval = governance["approval"] or "pending human review"
    return (
        '<dl class="governance">'
        f"<dt>State</dt><dd>{badge(value)}</dd>"
        f"<dt>Approval</dt><dd><code>{escape(approval)}</code></dd>"
        f"<dt>Provenance</dt><dd><code>{escape(provenance['method'])}</code> "
        f"from <code>{escape(provenance['source'])}</code> at "
        f"<time>{escape(provenance['capturedAt'])}</time></dd>"
        "</dl>"
    )


def html_list(items: Sequence[str]) -> str:
    """Render escaped strings as one HTML list."""

    return "<ul>" + "".join(f"<li>{escape(item)}</li>" for item in items) + "</ul>"


def render_html(model: dict[str, Any]) -> str:
    """Render a framework-neutral, accessible reference Brand Kit page."""

    project = model["project"]
    foundation = model["foundation"]
    language = model["localization"]["sourceLanguage"]
    styles = """
    :root { color-scheme: light dark; font-family: system-ui, sans-serif; }
    body { margin: 0 auto; max-width: 76rem; padding: 2rem; line-height: 1.55; }
    header, section { margin-block: 2.5rem; }
    h1, h2, h3, h4 { line-height: 1.15; }
    .grid { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr)); }
    .card { border: 1px solid currentColor; border-radius: .75rem; padding: 1rem; }
    .badge { border: 1px solid currentColor; border-radius: 999px; padding: .15rem .55rem; }
    .badge-approved { color: #176b3a; }
    .badge-candidate { color: #805b00; }
    .badge-rejected { color: #a12622; }
    .badge-superseded { color: #665b70; }
    .governance { display: grid; grid-template-columns: max-content 1fr; gap: .25rem .75rem; }
    .governance dt { font-weight: 700; }
    blockquote {
      border-inline-start: .3rem solid currentColor;
      margin-inline: 0;
      padding-inline: 1rem;
    }
    table { border-collapse: collapse; display: block; max-width: 100%; overflow-x: auto; }
    th, td {
      border: 1px solid currentColor;
      padding: .5rem;
      text-align: start;
      vertical-align: top;
    }
    a:focus-visible { outline: .2rem solid currentColor; outline-offset: .2rem; }
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after { scroll-behavior: auto !important; }
    }
    """.strip()
    parts = [
        "<!doctype html>",
        f'<html lang="{escape(language)}">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{escape(project['displayName'])} Brand Kit</title>",
        f"<style>{styles}</style>",
        "</head>",
        "<body>",
        "<header>",
        f"<h1>{escape(project['displayName'])} Brand Kit</h1>",
        f"<p>{escape(project['tagline'])}</p>",
        f'<p><a href="{escape(project["repository"])}">Source repository</a></p>',
        f"<p><strong>Audience:</strong> {escape(model['audience'])}</p>",
    ]
    if model["selectedContext"] is not None:
        parts.append(
            f'<p>Selected context: <code>{escape(model["selectedContext"])}</code></p>'
        )
    parts.extend(
        [
            "</header>",
            '<main id="main">',
            '<section aria-labelledby="foundation">',
            '<h2 id="foundation">Foundation</h2>',
            f"<p><strong>Purpose:</strong> {escape(foundation['purpose'])}</p>",
            f"<p><strong>Positioning:</strong> {escape(foundation['positioning'])}</p>",
            "<h3>Audience</h3>",
            html_list(foundation["audience"]),
            "<h3>Personality</h3>",
            html_list(foundation["personality"]),
            html_governance(foundation),
            "</section>",
            '<section aria-labelledby="voice-characteristics">',
            '<h2 id="voice-characteristics">Voice characteristics</h2>',
            '<div class="grid">',
        ]
    )
    for item in model["characteristics"]:
        parts.extend(
            [
                '<article class="card">',
                f"<h3>{escape(item['label'])}</h3>",
                f"<p>{escape(item['description'])}</p>",
                html_governance(item),
                "</article>",
            ]
        )
    parts.extend(["</div>", "</section>"])
    for context in model["contexts"]:
        parts.extend(
            [
                f'<section aria-labelledby="context-{escape(context["id"])}">',
                f'<h2 id="context-{escape(context["id"])}">{escape(context["label"])}</h2>',
                f"<p><strong>Audience:</strong> {escape(context['audience'])}</p>",
                f"<p><strong>Intent:</strong> {escape(context['intent'])}</p>",
                f"<p><strong>Tone:</strong> {escape(context['tone'])}</p>",
                "<h3>Preferred vocabulary</h3>",
                html_list(context["preferredVocabulary"]),
                "<h3>Avoided language</h3>",
                html_list(context["avoidedLanguage"]),
                f"<p><strong>Naming:</strong> {escape(context['naming'])}</p>",
                f"<p><strong>Capitalization:</strong> {escape(context['capitalization'])}</p>",
                f"<p><strong>Punctuation:</strong> {escape(context['punctuation'])}</p>",
                "<h3>Examples</h3>",
            ]
        )
        for item in context["examples"]:
            parts.extend(
                [
                    '<article class="card">',
                    f"<blockquote><p>{escape(item['text'])}</p></blockquote>",
                    f"<p>{escape(item['rationale'])}</p>",
                    html_governance(item),
                    "</article>",
                ]
            )
        parts.append("<h3>Anti-examples</h3>")
        for item in context["antiExamples"]:
            parts.extend(
                [
                    '<article class="card">',
                    f"<blockquote><p>{escape(item['text'])}</p></blockquote>",
                    f"<p>{escape(item['rationale'])}</p>",
                    html_governance(item),
                    "</article>",
                ]
            )
        parts.append("</section>")

    parts.extend(
        [
            '<section aria-labelledby="usage">',
            '<h2 id="usage">Usage: do / don’t</h2>',
        ]
    )
    for section in model["sections"]:
        parts.extend(
            [
                f"<h3>{escape(section['title'])}</h3>",
                f"<p>{escape(section['description'])}</p>",
                '<div class="grid">',
            ]
        )
        for rule in section["rules"]:
            prefix = "Do" if rule["kind"] == "do" else "Don’t"
            parts.extend(
                [
                    '<article class="card">',
                    f"<h4>{prefix}: {escape(rule['instruction'])}</h4>",
                    f"<p>{escape(rule['rationale'])}</p>",
                    html_list(rule["details"]),
                    f"<p><strong>Contexts:</strong> {escape(', '.join(rule['contexts']))}</p>",
                    html_governance(rule),
                    "</article>",
                ]
            )
        parts.append("</div>")
    parts.extend(["</section>", '<section aria-labelledby="downloads">'])
    parts.append('<h2 id="downloads">Downloads</h2>')
    for asset in model["downloads"]:
        parts.extend(
            [
                '<article class="card">',
                f"<h3>{escape(asset['label'])}</h3>",
                f"<p>{escape(asset['notes'])}</p>",
                (
                    f'<a href="{escape(asset["path"])}" '
                    f'download="{escape(asset["downloadName"])}">Download asset</a>'
                ),
                html_governance(asset),
                "</article>",
            ]
        )
    parts.extend(["</section>", '<section aria-labelledby="legacy">'])
    parts.append('<h2 id="legacy">Legacy assets</h2>')
    for asset in model["legacyAssets"]:
        parts.extend(
            [
                '<article class="card">',
                f"<h3>{escape(asset['label'])} — LEGACY</h3>",
                f"<p><strong>Availability:</strong> {escape(asset['availability'])}</p>",
                f"<p>{escape(asset['notes'])}</p>",
                f"<p>Replacement: <code>{escape(asset['replacement'])}</code></p>",
                html_governance(asset),
                "</article>",
            ]
        )
    accessibility = model["accessibility"]
    legal = model["legal"]
    parts.extend(
        [
            "</section>",
            '<section aria-labelledby="accessibility">',
            '<h2 id="accessibility">Accessibility</h2>',
            f"<p>{escape(accessibility['summary'])}</p>",
            html_list(accessibility["rules"]),
            "</section>",
            '<section aria-labelledby="legal">',
            '<h2 id="legal">Legal and attribution</h2>',
            f"<p><strong>Trademark:</strong> {escape(legal['trademark'])}</p>",
            f"<p><strong>Copyright:</strong> {escape(legal['copyright'])}</p>",
            f"<p><strong>Attribution:</strong> {escape(legal['attribution'])}</p>",
            "</section>",
            '<section aria-labelledby="decisions">',
            '<h2 id="decisions">Decision ledger</h2>',
            "<table>",
            "<thead><tr><th>Decision</th><th>Subject</th><th>Candidate</th>"
            "<th>Status</th><th>Reviewer</th><th>Evidence</th></tr></thead>",
            "<tbody>",
        ]
    )
    for decision in model["decisions"]:
        evidence = escape(decision["evidence"])
        if decision["evidence"].startswith("https://"):
            evidence = f'<a href="{evidence}">review evidence</a>'
        parts.append(
            "<tr>"
            f"<td><code>{escape(decision['id'])}</code></td>"
            f"<td><code>{escape(decision['subject'])}</code></td>"
            f"<td><code>{escape(decision['candidate'])}</code></td>"
            f"<td>{escape(decision['status'])}</td>"
            f"<td>{escape(decision['reviewedBy'])}</td>"
            f"<td>{evidence}</td>"
            "</tr>"
        )
    parts.extend(["</tbody>", "</table>", "</section>", "</main>", "</body>", "</html>"])
    return "\n".join(parts) + "\n"


def render(model: dict[str, Any], output_format: str) -> str:
    """Dispatch one deterministic output format."""

    if output_format == "json":
        return render_json(model)
    if output_format == "markdown":
        return render_markdown(model)
    if output_format == "html":
        return render_html(model)
    raise GuidanceError(f"unsupported output format: {output_format}")


def output_path(repository_root: Path, value: Path) -> Path:
    """Resolve a generated output without allowing canonical-source writes."""

    raw = value.as_posix()
    if value.is_absolute() or not validator.valid_relative_path(raw):
        raise GuidanceError("--output must be a normalized repository-relative path")
    destination = repository_root / value
    identity_root = (repository_root / ".identity").resolve()
    try:
        destination.resolve().relative_to(identity_root)
    except ValueError:
        return destination
    raise GuidanceError("renderer output cannot overwrite canonical .identity source")


def build_parser() -> argparse.ArgumentParser:
    """Build the stable guidance-rendering command interface."""

    parser = argparse.ArgumentParser(
        description="Render validated Identity voice and usage guidance."
    )
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
        help="Consumer repository containing .identity/identity.json.",
    )
    parser.add_argument(
        "--format",
        choices=("json", "markdown", "html"),
        default="markdown",
        help="Renderer output format.",
    )
    parser.add_argument(
        "--audience",
        choices=("public", "review"),
        default="public",
        help="Public output excludes every internal or unapproved record.",
    )
    parser.add_argument(
        "--context",
        help="Optional voice and usage context ID to retrieve.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional repository-relative generated output path outside .identity/.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Render to standard output or one explicitly selected generated path."""

    arguments = build_parser().parse_args(argv)
    try:
        model = build_view_model(
            arguments.repository_root,
            arguments.context,
            arguments.audience,
        )
        content = render(model, arguments.format)
        if arguments.output is None:
            print(content, end="")
        else:
            destination = output_path(arguments.repository_root, arguments.output)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8")
    except (GuidanceError, OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"error: cannot render guidance: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
