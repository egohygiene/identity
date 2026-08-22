// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

use std::collections::{BTreeMap, BTreeSet};

use serde::{Deserialize, Serialize};
use serde_json::{Value, json};

use crate::compiler::{
    CompilerError, CompilerRequest, CompilerResult, Diagnostic, FailureKind, ProjectionTarget,
};

pub const BRAND_KIT_PROFILE_VERSION: &str = "1.0.0";

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct ProfileSelection {
    pub id: String,
    pub version: String,
}

#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct ProfileDescriptor {
    pub id: String,
    pub version: String,
    pub description: String,
    pub targets: Vec<ProjectionTarget>,
}

#[must_use]
pub fn profile_ids() -> &'static [&'static str] {
    &[
        "core", "web", "pwa", "github", "docs", "social", "tokens", "metadata", "archive",
    ]
}

#[must_use]
pub fn profile_catalog() -> BTreeMap<String, ProfileDescriptor> {
    [
        core_profile(),
        web_profile(),
        pwa_profile(),
        github_profile(),
        docs_profile(),
        social_profile(),
        tokens_profile(),
        metadata_profile(),
        archive_profile(),
    ]
    .into_iter()
    .map(|profile| (profile.id.clone(), profile))
    .collect()
}

pub fn compiler_request(
    output_root: impl Into<String>,
    selections: &[ProfileSelection],
) -> CompilerResult<CompilerRequest> {
    let catalog = profile_catalog();
    let mut selected_ids = BTreeSet::new();
    let mut targets = Vec::new();

    for selection in selections {
        if !selected_ids.insert(selection.id.as_str()) {
            return Err(profile_error(
                &selection.id,
                "profile was selected more than once".to_owned(),
            ));
        }
        let profile = catalog.get(&selection.id).ok_or_else(|| {
            profile_error(
                &selection.id,
                format!("unknown Brand Kit output profile {:?}", selection.id),
            )
        })?;
        if selection.version != profile.version {
            return Err(profile_error(
                &selection.id,
                format!(
                    "profile {:?} requires version {}, found {}",
                    selection.id, profile.version, selection.version
                ),
            ));
        }
        targets.extend(profile.targets.clone());
    }

    targets.sort_by(|left, right| {
        left.profile
            .cmp(&right.profile)
            .then_with(|| left.relative_path.cmp(&right.relative_path))
            .then_with(|| left.id.cmp(&right.id))
    });

    Ok(CompilerRequest {
        output_root: output_root.into(),
        targets,
    })
}

#[must_use]
pub fn all_profiles() -> Vec<ProfileSelection> {
    profile_ids()
        .iter()
        .map(|id| ProfileSelection {
            id: (*id).to_owned(),
            version: BRAND_KIT_PROFILE_VERSION.to_owned(),
        })
        .collect()
}

fn core_profile() -> ProfileDescriptor {
    profile(
        "core",
        "Canonical scalable marks and source-safe vector projections.",
        vec![target(
            "core-mark-svg",
            "core",
            "brand/mark.svg",
            "identity-source-svg",
            "image/svg+xml",
            params([("role", json!("mark"))]),
            Some(512_000),
        )],
    )
}

fn web_profile() -> ProfileDescriptor {
    profile(
        "web",
        "Browser favicon and lightweight web identity projections.",
        vec![
            target(
                "web-favicon-svg",
                "web",
                "web/favicon.svg",
                "identity-source-svg",
                "image/svg+xml",
                params([("role", json!("mark"))]),
                Some(256_000),
            ),
            raster_target(
                "web-favicon-32",
                "web",
                "web/favicon-32.png",
                32,
                32,
                "icon",
                false,
            ),
            raster_target(
                "web-favicon-64",
                "web",
                "web/favicon-64.png",
                64,
                64,
                "icon",
                false,
            ),
        ],
    )
}

fn pwa_profile() -> ProfileDescriptor {
    profile(
        "pwa",
        "Portable PWA icons and manifest icon metadata.",
        vec![
            raster_target(
                "pwa-icon-192",
                "pwa",
                "pwa/icon-192.png",
                192,
                192,
                "icon",
                false,
            ),
            raster_target(
                "pwa-icon-512",
                "pwa",
                "pwa/icon-512.png",
                512,
                512,
                "icon",
                false,
            ),
            raster_target(
                "pwa-maskable-512",
                "pwa",
                "pwa/icon-maskable-512.png",
                512,
                512,
                "icon",
                true,
            ),
            target(
                "pwa-manifest-icons",
                "pwa",
                "pwa/manifest-icons.json",
                "identity-metadata",
                "application/json",
                params([("format", json!("web-manifest-icons"))]),
                Some(64_000),
            ),
        ],
    )
}

fn github_profile() -> ProfileDescriptor {
    profile(
        "github",
        "GitHub repository social preview projection.",
        vec![raster_target(
            "github-social-preview",
            "github",
            "github/social-preview.png",
            1280,
            640,
            "social-card",
            false,
        )],
    )
}

fn docs_profile() -> ProfileDescriptor {
    profile(
        "docs",
        "Document and presentation style projection from semantic tokens.",
        vec![target(
            "docs-document-css",
            "docs",
            "docs/document.css",
            "identity-tokens",
            "text/css",
            params([("format", json!("document-css"))]),
            Some(128_000),
        )],
    )
}

fn social_profile() -> ProfileDescriptor {
    profile(
        "social",
        "Portable 1200×630 social-card projection.",
        vec![raster_target(
            "social-card-1200x630",
            "social",
            "social/card-1200x630.png",
            1200,
            630,
            "social-card",
            false,
        )],
    )
}

fn tokens_profile() -> ProfileDescriptor {
    profile(
        "tokens",
        "DTCG, CSS, JavaScript, TypeScript, and Tailwind-compatible token packages.",
        vec![
            token_target(
                "tokens-dtcg-json",
                "packages/tokens/tokens.json",
                "dtcg-json",
                "application/json",
            ),
            token_target(
                "tokens-css",
                "packages/tokens/tokens.css",
                "css",
                "text/css",
            ),
            token_target(
                "tokens-javascript",
                "packages/tokens/tokens.js",
                "javascript",
                "text/javascript",
            ),
            token_target(
                "tokens-typescript",
                "packages/tokens/tokens.d.ts",
                "typescript",
                "text/plain",
            ),
            token_target(
                "tokens-tailwind-theme",
                "packages/tokens/tailwind.theme.json",
                "tailwind",
                "application/json",
            ),
            token_target(
                "tokens-package-json",
                "packages/tokens/package.json",
                "package-json",
                "application/json",
            ),
        ],
    )
}

fn metadata_profile() -> ProfileDescriptor {
    profile(
        "metadata",
        "Public identity metadata, Open Graph markup, and guidance package projections.",
        vec![
            metadata_target(
                "metadata-json",
                "packages/metadata/metadata.json",
                "metadata-json",
                "application/json",
            ),
            metadata_target(
                "metadata-open-graph",
                "packages/metadata/open-graph.html",
                "open-graph",
                "text/html",
            ),
            metadata_target(
                "metadata-package-json",
                "packages/metadata/package.json",
                "package-json",
                "application/json",
            ),
            target(
                "guidance-json",
                "metadata",
                "packages/guidance/voice-and-usage.json",
                "identity-guidance",
                "application/json",
                params([("format", json!("json"))]),
                Some(256_000),
            ),
            target(
                "guidance-markdown",
                "metadata",
                "packages/guidance/README.md",
                "identity-guidance",
                "text/markdown",
                params([("format", json!("markdown"))]),
                Some(256_000),
            ),
        ],
    )
}

fn archive_profile() -> ProfileDescriptor {
    profile(
        "archive",
        "Complete downloadable Brand Kit archive plus deterministic package indexes and checksums.",
        vec![
            package_target(
                "brand-kit-package-index",
                "packages/brand-kit/index.json",
                "index-json",
                "application/json",
            ),
            package_target(
                "brand-kit-checksums",
                "packages/brand-kit/checksums.json",
                "checksums-json",
                "application/json",
            ),
            package_target(
                "brand-kit-archive",
                "packages/brand-kit/brand-kit.zip",
                "zip",
                "application/zip",
            ),
        ],
    )
}

fn profile(id: &str, description: &str, targets: Vec<ProjectionTarget>) -> ProfileDescriptor {
    ProfileDescriptor {
        id: id.to_owned(),
        version: BRAND_KIT_PROFILE_VERSION.to_owned(),
        description: description.to_owned(),
        targets,
    }
}

fn target(
    id: &str,
    profile: &str,
    relative_path: &str,
    adapter_id: &str,
    media_type: &str,
    parameters: BTreeMap<String, Value>,
    maximum_bytes: Option<u64>,
) -> ProjectionTarget {
    ProjectionTarget {
        id: id.to_owned(),
        profile: profile.to_owned(),
        relative_path: relative_path.to_owned(),
        adapter_id: adapter_id.to_owned(),
        media_type: media_type.to_owned(),
        parameters,
        required_approval: None,
        maximum_bytes,
    }
}

fn raster_target(
    id: &str,
    profile: &str,
    relative_path: &str,
    width: u32,
    height: u32,
    mode: &str,
    maskable: bool,
) -> ProjectionTarget {
    target(
        id,
        profile,
        relative_path,
        "identity-raster",
        "image/png",
        params([
            ("width", json!(width)),
            ("height", json!(height)),
            ("mode", json!(mode)),
            ("maskable", json!(maskable)),
            ("sourceRole", json!("mark")),
        ]),
        Some(2_000_000),
    )
}

fn token_target(id: &str, path: &str, format: &str, media_type: &str) -> ProjectionTarget {
    target(
        id,
        "tokens",
        path,
        "identity-tokens",
        media_type,
        params([("format", json!(format))]),
        Some(512_000),
    )
}

fn metadata_target(id: &str, path: &str, format: &str, media_type: &str) -> ProjectionTarget {
    target(
        id,
        "metadata",
        path,
        "identity-metadata",
        media_type,
        params([("format", json!(format))]),
        Some(256_000),
    )
}

fn package_target(id: &str, path: &str, format: &str, media_type: &str) -> ProjectionTarget {
    target(
        id,
        "archive",
        path,
        "identity-package",
        media_type,
        params([("format", json!(format))]),
        Some(8_000_000),
    )
}

fn params<const N: usize>(entries: [(&str, Value); N]) -> BTreeMap<String, Value> {
    entries
        .into_iter()
        .map(|(key, value)| (key.to_owned(), value))
        .collect()
}

fn profile_error(path: &str, message: String) -> CompilerError {
    CompilerError::new(
        FailureKind::Unsupported,
        Diagnostic::error(
            "IDN3201",
            FailureKind::Unsupported,
            Some(path.to_owned()),
            message,
            format!(
                "Select one of the built-in profiles at version {BRAND_KIT_PROFILE_VERSION}: {}.",
                profile_ids().join(", ")
            ),
        ),
    )
}
