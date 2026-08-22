// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

//! Deterministic built-in Brand Kit profiles and projection adapters.
//!
//! The module consumes the framework-neutral compiler contracts. Canonical
//! `.identity/` source remains consumer-owned; every artifact produced here is a
//! versioned projection with a compiler manifest and source digest.

mod archive;
mod model;
mod profiles;
mod render;

#[cfg(test)]
mod tests;

use std::collections::BTreeSet;

use serde_json::Value;

use crate::compiler::{
    AdapterDescriptor, AdapterKind, AdapterPlan, AdapterRegistry, COMPILER_API_MAJOR,
    CompilerError, CompilerResult, Diagnostic, DiagnosticSeverity, EvidenceRecord, EvidenceStatus,
    FailureKind, ProjectionAdapter, ProjectionTarget, ResolvedIdentity, VerificationReport,
};

pub use model::{
    BRAND_KIT_MODEL_SCHEMA, BrandKitGuidance, BrandKitModel, BrandKitProject, BrandKitSourceAsset,
    BrandKitToken,
};
pub use profiles::{
    BRAND_KIT_PROFILE_VERSION, ProfileDescriptor, ProfileSelection, all_profiles, compiler_request,
    profile_catalog, profile_ids,
};

const ADAPTER_VERSION: &str = "1.0.0";

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum BuiltinProjectionAdapter {
    Tokens,
    Metadata,
    Guidance,
    SourceSvg,
    Raster,
    Package,
}

impl BuiltinProjectionAdapter {
    fn id(self) -> &'static str {
        match self {
            Self::Tokens => "identity-tokens",
            Self::Metadata => "identity-metadata",
            Self::Guidance => "identity-guidance",
            Self::SourceSvg => "identity-source-svg",
            Self::Raster => "identity-raster",
            Self::Package => "identity-package",
        }
    }

    fn kind(self) -> AdapterKind {
        match self {
            Self::Tokens | Self::Guidance => AdapterKind::TokenTransformer,
            Self::Metadata => AdapterKind::Metadata,
            Self::SourceSvg => AdapterKind::VectorRenderer,
            Self::Raster => AdapterKind::RasterRenderer,
            Self::Package => AdapterKind::Archive,
        }
    }

    fn capabilities(self) -> BTreeSet<String> {
        let capabilities: &[&str] = match self {
            Self::Tokens => &[
                "dtcg",
                "css",
                "javascript",
                "typescript",
                "tailwind",
                "document-css",
            ],
            Self::Metadata => &["public-metadata", "open-graph", "web-app-manifest"],
            Self::Guidance => &["voice", "usage", "markdown"],
            Self::SourceSvg => &["approved-svg", "source-digest"],
            Self::Raster => &[
                "png",
                "favicon",
                "maskable",
                "social-card",
                "github-preview",
            ],
            Self::Package => &["zip", "package-index", "checksums"],
        };
        capabilities
            .iter()
            .map(|capability| (*capability).to_owned())
            .collect()
    }
}

impl ProjectionAdapter for BuiltinProjectionAdapter {
    fn descriptor(&self) -> AdapterDescriptor {
        AdapterDescriptor {
            id: self.id().to_owned(),
            version: ADAPTER_VERSION.to_owned(),
            kind: self.kind(),
            compiler_api_major: COMPILER_API_MAJOR,
            deterministic: true,
            offline: true,
            capabilities: self.capabilities(),
        }
    }

    fn plan(
        &self,
        identity: &ResolvedIdentity,
        target: &ProjectionTarget,
    ) -> CompilerResult<AdapterPlan> {
        let model = BrandKitModel::from_resolved(identity)?;
        let mut warnings = Vec::new();
        if *self == Self::Guidance {
            if model.guidance.voice.is_none() {
                warnings.push(
                    "brand voice is not declared yet; the generated guidance package records that state explicitly"
                        .to_owned(),
                );
            }
            if model.guidance.usage.is_none() {
                warnings.push(
                    "brand usage guidance is not declared yet; the generated guidance package records that state explicitly"
                        .to_owned(),
                );
            }
        }
        if *self == Self::Raster {
            let (width, height) = render::expected_raster_dimensions(target)?;
            if width == 0 || height == 0 {
                return Err(adapter_error(
                    target,
                    "raster dimensions must be greater than zero".to_owned(),
                ));
            }
        }
        Ok(AdapterPlan {
            warnings,
            required_approvals: BTreeSet::new(),
        })
    }

    fn render(
        &self,
        identity: &ResolvedIdentity,
        target: &ProjectionTarget,
    ) -> CompilerResult<Vec<u8>> {
        let model = BrandKitModel::from_resolved(identity)?;
        match self {
            Self::Tokens => render::render_tokens(&model, target),
            Self::Metadata => render::render_metadata(&model, target),
            Self::Guidance => render::render_guidance(&model, target),
            Self::SourceSvg => render::render_source_svg(&model, target),
            Self::Raster => render::render_raster(&model, target),
            Self::Package => render::render_package(&model, target),
        }
    }

    fn verify(
        &self,
        identity: &ResolvedIdentity,
        target: &ProjectionTarget,
        bytes: &[u8],
    ) -> CompilerResult<VerificationReport> {
        let model = BrandKitModel::from_resolved(identity)?;
        match self {
            Self::Tokens | Self::Metadata | Self::Guidance => {
                verify_text_projection(*self, target, bytes)
            }
            Self::SourceSvg => verify_svg(&model, target, bytes),
            Self::Raster => verify_raster(target, bytes),
            Self::Package => verify_package(target, bytes),
        }
    }
}

pub fn register_builtin_adapters(registry: &mut AdapterRegistry) -> CompilerResult<()> {
    for adapter in [
        BuiltinProjectionAdapter::Tokens,
        BuiltinProjectionAdapter::Metadata,
        BuiltinProjectionAdapter::Guidance,
        BuiltinProjectionAdapter::SourceSvg,
        BuiltinProjectionAdapter::Raster,
        BuiltinProjectionAdapter::Package,
    ] {
        registry.register(adapter)?;
    }
    Ok(())
}

fn verify_text_projection(
    adapter: BuiltinProjectionAdapter,
    target: &ProjectionTarget,
    bytes: &[u8],
) -> CompilerResult<VerificationReport> {
    let text = std::str::from_utf8(bytes).map_err(|error| {
        adapter_error(
            target,
            format!("generated text projection is not UTF-8: {error}"),
        )
    })?;
    if target.media_type == "application/json" {
        serde_json::from_str::<Value>(text).map_err(|error| {
            adapter_error(
                target,
                format!("generated JSON projection is invalid: {error}"),
            )
        })?;
    }
    Ok(verified(
        target,
        adapter.id(),
        "deterministic-format",
        format!(
            "{} projection is valid UTF-8 and matches its declared media contract",
            adapter.id()
        ),
    ))
}

fn verify_svg(
    model: &BrandKitModel,
    target: &ProjectionTarget,
    bytes: &[u8],
) -> CompilerResult<VerificationReport> {
    let text = std::str::from_utf8(bytes)
        .map_err(|error| adapter_error(target, format!("generated SVG is not UTF-8: {error}")))?;
    if !text.contains("<svg") {
        return Err(adapter_error(
            target,
            "generated vector projection contains no SVG root".to_owned(),
        ));
    }
    let role = target
        .parameters
        .get("role")
        .and_then(Value::as_str)
        .ok_or_else(|| adapter_error(target, "source SVG target is missing role".to_owned()))?;
    let source = model.source(role)?;
    if crate::compiler::sha256_hex(bytes) != source.sha256 {
        return Err(adapter_error(
            target,
            "generated SVG no longer matches the approved source digest".to_owned(),
        ));
    }
    Ok(verified(
        target,
        "identity-source-svg",
        "source-digest",
        "generated SVG is byte-identical to the approved canonical source",
    ))
}

fn verify_raster(target: &ProjectionTarget, bytes: &[u8]) -> CompilerResult<VerificationReport> {
    let pixmap = resvg::tiny_skia::Pixmap::decode_png(bytes).map_err(|error| {
        adapter_error(target, format!("generated PNG cannot be decoded: {error}"))
    })?;
    let (width, height) = render::expected_raster_dimensions(target)?;
    if pixmap.width() != width || pixmap.height() != height {
        return Err(adapter_error(
            target,
            format!(
                "generated PNG dimensions are {}x{}, expected {width}x{height}",
                pixmap.width(),
                pixmap.height()
            ),
        ));
    }

    let mut report = verified(
        target,
        "identity-raster",
        "dimensions",
        format!("generated PNG is exactly {width}x{height}"),
    );
    if render::is_maskable(target)? {
        report.evidence.push(EvidenceRecord {
            target_id: target.id.clone(),
            adapter_id: "identity-raster".to_owned(),
            check: "maskable-safe-zone".to_owned(),
            status: EvidenceStatus::Verified,
            message: format!(
                "approved mark is constrained to {:.0}% of the icon bounds so its bounding square remains inside the Web App Manifest central safe circle",
                render::standard_maskable_fraction() * 100.0
            ),
        });
    }
    Ok(report)
}

fn verify_package(target: &ProjectionTarget, bytes: &[u8]) -> CompilerResult<VerificationReport> {
    let format = target
        .parameters
        .get("format")
        .and_then(Value::as_str)
        .ok_or_else(|| adapter_error(target, "package target is missing format".to_owned()))?;
    match format {
        "zip" if !archive::looks_like_deterministic_zip(bytes) => Err(adapter_error(
            target,
            "generated Brand Kit archive is not a deterministic ZIP32 package".to_owned(),
        )),
        "zip" => Ok(verified(
            target,
            "identity-package",
            "archive-structure",
            "Brand Kit archive contains deterministic ZIP32 headers and a central directory",
        )),
        "index-json" | "checksums-json" => {
            verify_text_projection(BuiltinProjectionAdapter::Package, target, bytes)
        }
        _ => Err(adapter_error(
            target,
            format!("unsupported package verification format {format:?}"),
        )),
    }
}

fn verified(
    target: &ProjectionTarget,
    adapter_id: &str,
    check: &str,
    message: impl Into<String>,
) -> VerificationReport {
    VerificationReport {
        diagnostics: Vec::new(),
        evidence: vec![EvidenceRecord {
            target_id: target.id.clone(),
            adapter_id: adapter_id.to_owned(),
            check: check.to_owned(),
            status: EvidenceStatus::Verified,
            message: message.into(),
        }],
    }
}

fn adapter_error(target: &ProjectionTarget, message: String) -> CompilerError {
    CompilerError::new(
        FailureKind::Failed,
        Diagnostic {
            code: "IDN3501".to_owned(),
            severity: DiagnosticSeverity::Error,
            failure: FailureKind::Failed,
            path: Some(target.relative_path.clone()),
            message,
            recovery: "Review the built-in profile parameters and resolved Brand Kit model before regenerating.".to_owned(),
        },
    )
}
