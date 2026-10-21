// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

//! Framework-neutral public Brand Kit view model and reference-renderer adapter.
//!
//! The Rust compiler owns the immutable renderer input. Presentation code may
//! change or be replaced without changing canonical `.identity/` source.

use std::collections::{BTreeMap, BTreeSet};

use serde::{Deserialize, Serialize};
use serde_json::Value;

use crate::brandkit::{
    BrandKitAssetUsage, BrandKitLicense, BrandKitModel, BrandKitOrigin, BrandKitSourceAsset,
};
use crate::compiler::{
    AdapterDescriptor, AdapterKind, AdapterPlan, AdapterRegistry, COMPILER_API_MAJOR,
    CompilerError, CompilerRequest, CompilerResult, Diagnostic, DiagnosticSeverity, EvidenceRecord,
    EvidenceStatus, FailureKind, ProjectionAdapter, ProjectionTarget, ResolvedIdentity,
    VerificationReport,
};

pub const BRAND_KIT_VIEW_MODEL_SCHEMA: &str = "identity.brand-kit-view-model/v1";
pub const REFERENCE_RENDERER_PROFILE_VERSION: &str = "1.0.0";

const REFERENCE_RENDERER_ADAPTER_ID: &str = "identity-reference-renderer-model";
const REFERENCE_RENDERER_ADAPTER_VERSION: &str = "1.0.0";
const REFERENCE_RENDERER_OUTPUT_PATH: &str = "packages/renderer/brand-kit.view-model.json";

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct BrandKitViewRelease {
    pub version: String,
    pub profile_version: String,
    pub source_digest: String,
    pub immutable_id: String,
    pub status: String,
}

#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct BrandKitViewToken {
    pub path: String,
    #[serde(rename = "type")]
    pub token_type: String,
    pub value: Value,
    pub source_layer: String,
    #[serde(default)]
    pub override_reason: Option<String>,
    #[serde(default)]
    pub approval: Option<String>,
}

#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct BrandKitViewAsset {
    pub id: String,
    pub label: String,
    pub media_type: String,
    pub sha256: String,
    pub alt_text: String,
    pub dimensions: String,
    pub intended_use: String,
    #[serde(default)]
    pub safe_zone: Option<f64>,
    pub text: String,
    pub availability: String,
    #[serde(default)]
    pub download_path: Option<String>,
    #[serde(default)]
    pub license: Option<BrandKitLicense>,
    #[serde(default)]
    pub origin: Option<BrandKitOrigin>,
    #[serde(default)]
    pub approval: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub usage: Option<BrandKitAssetUsage>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub kind: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub notes: Option<String>,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct BrandKitViewDownload {
    pub id: String,
    pub label: String,
    pub path: String,
    pub media_type: String,
    pub profile: String,
    pub source_asset_id: String,
    pub source_sha256: String,
    pub dimensions: String,
}

#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct BrandKitViewGuidanceSection {
    pub status: String,
    pub canonical: bool,
    #[serde(default)]
    pub value: Option<Value>,
}

#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct BrandKitViewGuidance {
    pub voice: BrandKitViewGuidanceSection,
    pub usage: BrandKitViewGuidanceSection,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct BrandKitViewPackage {
    pub id: String,
    pub label: String,
    pub path: String,
    pub media_type: String,
    pub intended_use: String,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct BrandKitViewSupportSection {
    pub status: String,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct BrandKitViewSupport {
    pub motion: BrandKitViewSupportSection,
    pub imagery: BrandKitViewSupportSection,
    pub mascot: BrandKitViewSupportSection,
}

#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct BrandKitViewModel {
    pub schema: String,
    pub project_id: String,
    pub project: crate::brandkit::BrandKitProject,
    pub release: BrandKitViewRelease,
    pub tokens: Vec<BrandKitViewToken>,
    pub assets: Vec<BrandKitViewAsset>,
    pub guidance: BrandKitViewGuidance,
    pub support: BrandKitViewSupport,
    pub packages: Vec<BrandKitViewPackage>,
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub downloads: Vec<BrandKitViewDownload>,
}

impl BrandKitViewModel {
    #[must_use]
    pub fn from_brand_kit(model: &BrandKitModel) -> Self {
        Self::from_selected_targets(model, &[])
    }

    fn from_selected_targets(model: &BrandKitModel, targets: &[ProjectionTarget]) -> Self {
        let guidance = model
            .guidance
            .for_audience(crate::brandkit::GuidanceAudience::Public);
        let tokens = model
            .tokens
            .iter()
            .map(|(path, token)| BrandKitViewToken {
                path: path.clone(),
                token_type: token.token_type.clone(),
                value: token.value.clone(),
                source_layer: token.source_layer.clone(),
                override_reason: token.override_reason.clone(),
                approval: token.approval.clone(),
            })
            .collect();

        let public_assets = model.public_assets();
        let assets = public_assets
            .iter()
            .map(|(role, declaration)| {
                let source = &model.sources[role];
                let governance = model.source_governance.get(role);
                let download_path = targets.iter().find_map(|target| {
                    (target.adapter_id == "identity-source-svg"
                        && target.media_type == "image/svg+xml"
                        && target.parameters.get("role").and_then(Value::as_str)
                            == Some(role.as_str()))
                    .then(|| target.relative_path.clone())
                });
                BrandKitViewAsset {
                    id: role.clone(),
                    label: declaration.label.clone(),
                    media_type: source.media_type.clone(),
                    sha256: source.sha256.clone(),
                    alt_text: source.alt_text.clone(),
                    dimensions: asset_dimensions(source),
                    intended_use: declaration.notes.clone(),
                    safe_zone: source.safe_zone,
                    text: source.text.clone(),
                    availability: if download_path.is_some() {
                        "generated-download".to_owned()
                    } else {
                        "embedded-source".to_owned()
                    },
                    download_path,
                    license: governance.map(|entry| entry.license.clone()),
                    origin: governance.map(|entry| entry.origin.clone()),
                    approval: governance.map(|entry| entry.approval.clone()),
                    usage: governance.and_then(|entry| entry.usage.clone()),
                    kind: Some(declaration.kind.clone()),
                    notes: Some(declaration.notes.clone()),
                }
            })
            .collect();

        Self {
            schema: BRAND_KIT_VIEW_MODEL_SCHEMA.to_owned(),
            project_id: model.project_id.clone(),
            project: model.project.clone(),
            release: BrandKitViewRelease {
                version: REFERENCE_RENDERER_ADAPTER_VERSION.to_owned(),
                profile_version: REFERENCE_RENDERER_PROFILE_VERSION.to_owned(),
                source_digest: model.source_digest.clone(),
                immutable_id: format!("sha256:{}", model.source_digest),
                status: "generated".to_owned(),
            },
            tokens,
            assets,
            guidance: BrandKitViewGuidance {
                voice: guidance_section(guidance.voice),
                usage: guidance_section(guidance.usage),
            },
            support: BrandKitViewSupport {
                motion: BrandKitViewSupportSection {
                    status: if model.tokens.keys().any(|path| path.starts_with("motion.")) {
                        "declared".to_owned()
                    } else {
                        "not-declared".to_owned()
                    },
                },
                imagery: BrandKitViewSupportSection {
                    status: "not-declared".to_owned(),
                },
                mascot: BrandKitViewSupportSection {
                    status: "not-declared".to_owned(),
                },
            },
            packages: package_catalog()
                .into_iter()
                .filter(|package| {
                    targets
                        .iter()
                        .any(|target| package_target_matches(package, target))
                        && (package.id != "brand-kit-archive" || public_assets.contains_key("mark"))
                })
                .collect(),
            downloads: targets
                .iter()
                .filter_map(|target| {
                    let role = match target.adapter_id.as_str() {
                        "identity-source-svg" if target.media_type == "image/svg+xml" => {
                            target.parameters.get("role")?
                        }
                        "identity-raster" if target.media_type == "image/png" => {
                            target.parameters.get("sourceRole")?
                        }
                        _ => return None,
                    }
                    .as_str()?;
                    public_assets.get(role)?;
                    let source = model.sources.get(role)?;
                    let dimensions = if target.adapter_id == "identity-raster" {
                        let width = target.parameters.get("width")?.as_u64()?;
                        let height = target.parameters.get("height")?.as_u64()?;
                        format!("{width} × {height} pixels")
                    } else {
                        asset_dimensions(source)
                    };
                    Some(BrandKitViewDownload {
                        id: target.id.clone(),
                        label: humanize_identifier(&target.id),
                        path: target.relative_path.clone(),
                        media_type: target.media_type.clone(),
                        profile: target.profile.clone(),
                        source_asset_id: role.to_owned(),
                        source_sha256: source.sha256.clone(),
                        dimensions,
                    })
                })
                .collect(),
        }
    }
}

#[must_use]
pub fn reference_renderer_target() -> ProjectionTarget {
    ProjectionTarget {
        id: "reference-renderer-view-model".to_owned(),
        profile: "renderer".to_owned(),
        relative_path: REFERENCE_RENDERER_OUTPUT_PATH.to_owned(),
        adapter_id: REFERENCE_RENDERER_ADAPTER_ID.to_owned(),
        media_type: "application/json".to_owned(),
        parameters: BTreeMap::new(),
        required_approval: None,
        maximum_bytes: Some(8_000_000),
    }
}

#[must_use]
pub fn with_reference_renderer(mut request: CompilerRequest) -> CompilerRequest {
    crate::brandkit::bind_selected_output_targets(&mut request.targets);
    let mut renderer = reference_renderer_target();
    renderer.parameters.insert(
        "selectedTargets".to_owned(),
        serde_json::to_value(&request.targets).expect("compiler targets serialize to JSON"),
    );
    request.targets.push(renderer);
    request.targets.sort_by(|left, right| {
        left.profile
            .cmp(&right.profile)
            .then_with(|| left.relative_path.cmp(&right.relative_path))
            .then_with(|| left.id.cmp(&right.id))
    });
    request
}

pub fn register_reference_renderer_adapter(registry: &mut AdapterRegistry) -> CompilerResult<()> {
    registry.register(ReferenceRendererAdapter)
}

#[derive(Clone, Copy, Debug)]
struct ReferenceRendererAdapter;

impl ProjectionAdapter for ReferenceRendererAdapter {
    fn descriptor(&self) -> AdapterDescriptor {
        AdapterDescriptor {
            id: REFERENCE_RENDERER_ADAPTER_ID.to_owned(),
            version: REFERENCE_RENDERER_ADAPTER_VERSION.to_owned(),
            kind: AdapterKind::Metadata,
            compiler_api_major: COMPILER_API_MAJOR,
            deterministic: true,
            offline: true,
            capabilities: BTreeSet::from([
                "brand-kit-view-model".to_owned(),
                "static-renderer-input".to_owned(),
            ]),
        }
    }

    fn plan(
        &self,
        identity: &ResolvedIdentity,
        target: &ProjectionTarget,
    ) -> CompilerResult<AdapterPlan> {
        let model = BrandKitModel::from_resolved(identity)?;
        let _view_model =
            BrandKitViewModel::from_selected_targets(&model, &selected_targets(target)?);
        Ok(AdapterPlan {
            warnings: Vec::new(),
            required_approvals: BTreeSet::new(),
        })
    }

    fn render(
        &self,
        identity: &ResolvedIdentity,
        target: &ProjectionTarget,
    ) -> CompilerResult<Vec<u8>> {
        let model = BrandKitModel::from_resolved(identity)?;
        let view_model =
            BrandKitViewModel::from_selected_targets(&model, &selected_targets(target)?);
        let mut bytes = serde_json::to_vec_pretty(&view_model).map_err(|error| {
            renderer_error(
                REFERENCE_RENDERER_OUTPUT_PATH,
                format!("cannot serialize renderer view model: {error}"),
            )
        })?;
        bytes.push(b'\n');
        Ok(bytes)
    }

    fn verify(
        &self,
        identity: &ResolvedIdentity,
        target: &ProjectionTarget,
        bytes: &[u8],
    ) -> CompilerResult<VerificationReport> {
        let view_model = serde_json::from_slice::<BrandKitViewModel>(bytes).map_err(|error| {
            renderer_error(
                &target.relative_path,
                format!("renderer view model is not valid contract JSON: {error}"),
            )
        })?;
        if view_model.schema != BRAND_KIT_VIEW_MODEL_SCHEMA {
            return Err(renderer_error(
                &target.relative_path,
                format!("renderer view model schema must be {BRAND_KIT_VIEW_MODEL_SCHEMA:?}"),
            ));
        }
        if view_model.project_id != identity.project_id
            || view_model.release.source_digest != identity.source_digest
        {
            return Err(renderer_error(
                &target.relative_path,
                "renderer view model does not match the resolved identity".to_owned(),
            ));
        }

        Ok(VerificationReport {
            diagnostics: Vec::new(),
            evidence: vec![EvidenceRecord {
                target_id: target.id.clone(),
                adapter_id: REFERENCE_RENDERER_ADAPTER_ID.to_owned(),
                check: "immutable-view-model".to_owned(),
                status: EvidenceStatus::Verified,
                message: format!(
                    "renderer input conforms to {BRAND_KIT_VIEW_MODEL_SCHEMA} and source digest {}",
                    identity.source_digest
                ),
            }],
        })
    }
}

fn guidance_section(value: Option<Value>) -> BrandKitViewGuidanceSection {
    BrandKitViewGuidanceSection {
        status: if value.is_some() {
            "declared".to_owned()
        } else {
            "not-declared".to_owned()
        },
        canonical: true,
        value,
    }
}

fn selected_targets(target: &ProjectionTarget) -> CompilerResult<Vec<ProjectionTarget>> {
    target
        .parameters
        .get("selectedTargets")
        .map(|value| {
            serde_json::from_value(value.clone()).map_err(|error| {
                renderer_error(
                    &target.relative_path,
                    format!("selected output targets are invalid: {error}"),
                )
            })
        })
        .transpose()
        .map(Option::unwrap_or_default)
}

fn asset_dimensions(source: &BrandKitSourceAsset) -> String {
    if source.media_type != "image/svg+xml" {
        return "Not declared".to_owned();
    }

    let Some(view_box) = attribute_value(&source.text, "viewBox") else {
        return "Scalable vector; viewBox not declared".to_owned();
    };
    let components = view_box.split_whitespace().collect::<Vec<_>>();
    if components.len() != 4
        || components
            .iter()
            .any(|component| component.parse::<f64>().is_err())
    {
        return "Scalable vector; viewBox is not machine-readable".to_owned();
    }

    format!("{} × {} SVG viewBox units", components[2], components[3])
}

fn attribute_value<'a>(text: &'a str, name: &str) -> Option<&'a str> {
    for quote in ['"', '\''] {
        let marker = format!("{name}={quote}");
        if let Some(attribute_start) = text.find(&marker) {
            let value_start = attribute_start + marker.len();
            if let Some(value_length) = text[value_start..].find(quote) {
                return Some(&text[value_start..value_start + value_length]);
            }
        }
    }
    None
}

fn humanize_identifier(value: &str) -> String {
    value
        .split(['-', '_'])
        .filter(|segment| !segment.is_empty())
        .map(|segment| {
            let mut characters = segment.chars();
            let Some(first) = characters.next() else {
                return String::new();
            };
            first.to_uppercase().chain(characters).collect::<String>()
        })
        .collect::<Vec<_>>()
        .join(" ")
}

fn package_target_matches(package: &BrandKitViewPackage, target: &ProjectionTarget) -> bool {
    let (adapter, format) = match package.id.as_str() {
        "brand-kit-archive" => ("identity-package", "zip"),
        "design-tokens" => ("identity-tokens", "dtcg-json"),
        "public-metadata" => ("identity-metadata", "metadata-json"),
        "guidance" => ("identity-guidance", "markdown"),
        _ => return false,
    };
    target.relative_path == package.path
        && target.media_type == package.media_type
        && target.adapter_id == adapter
        && target.parameters.get("format").and_then(Value::as_str) == Some(format)
}

fn package_catalog() -> Vec<BrandKitViewPackage> {
    vec![
        BrandKitViewPackage {
            id: "brand-kit-archive".to_owned(),
            label: "Complete Brand Kit".to_owned(),
            path: "packages/brand-kit/brand-kit.zip".to_owned(),
            media_type: "application/zip".to_owned(),
            intended_use: "Versioned offline archive of approved generated assets.".to_owned(),
        },
        BrandKitViewPackage {
            id: "design-tokens".to_owned(),
            label: "Design tokens".to_owned(),
            path: "packages/tokens/tokens.json".to_owned(),
            media_type: "application/json".to_owned(),
            intended_use: "DTCG-compatible semantic token projection.".to_owned(),
        },
        BrandKitViewPackage {
            id: "public-metadata".to_owned(),
            label: "Public metadata".to_owned(),
            path: "packages/metadata/metadata.json".to_owned(),
            media_type: "application/json".to_owned(),
            intended_use: "Project metadata for public integrations.".to_owned(),
        },
        BrandKitViewPackage {
            id: "guidance".to_owned(),
            label: "Voice and usage guidance".to_owned(),
            path: "packages/guidance/README.md".to_owned(),
            media_type: "text/markdown".to_owned(),
            intended_use: "Human-readable projection of canonical guidance.".to_owned(),
        },
    ]
}

fn renderer_error(path: &str, message: String) -> CompilerError {
    CompilerError::new(
        FailureKind::Failed,
        Diagnostic {
            code: "IDN3601".to_owned(),
            severity: DiagnosticSeverity::Error,
            failure: FailureKind::Failed,
            path: Some(path.to_owned()),
            message,
            recovery: "Resolve and verify the Identity v1 Brand Kit before generating the immutable renderer view model.".to_owned(),
        },
    )
}
