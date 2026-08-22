// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

use std::collections::{BTreeMap, BTreeSet};

use serde_json::json;

use super::{
    HumanReviewEvidence, QualityArtifactReader, QualityCategory, QualityHarness, QualityInput,
    QualityScope, QualityStatus, VisualBaseline, VisualBaselineSet, svg_source_checks,
};
use crate::brandkit::{
    BRAND_KIT_MODEL_SCHEMA, BrandKitGuidance, BrandKitLicense, BrandKitModel, BrandKitOrigin,
    BrandKitProject, BrandKitSourceAsset, BrandKitSourceGovernance, BrandKitToken,
};
use crate::compiler::{
    COMPILER_MANIFEST_SCHEMA, CompilerManifest, CompilerResult, ManifestOutput, ProjectionTarget,
    sha256_hex,
};

const NORMAL_SVG: &str = include_str!("../../tests/fixtures/quality/mark-normal.svg");
const WIDE_SVG: &str = include_str!("../../tests/fixtures/quality/mark-extreme-wide.svg");
const TRANSPARENT_SVG: &str = include_str!("../../tests/fixtures/quality/mark-transparent.svg");
const BASELINES_JSON: &str = include_str!("../../tests/fixtures/quality/visual-baselines.json");

#[derive(Default)]
struct MemoryReader {
    files: BTreeMap<String, Vec<u8>>,
}

impl QualityArtifactReader for MemoryReader {
    fn read(&self, relative_path: &str) -> CompilerResult<Option<Vec<u8>>> {
        Ok(self.files.get(relative_path).cloned())
    }
}

#[test]
fn package_scope_passes_with_automated_and_human_evidence() {
    let model = valid_model(NORMAL_SVG);
    let target = svg_target("fixture-mark-normal", "fixture/mark-normal.svg");
    let bytes = NORMAL_SVG.as_bytes().to_vec();
    let manifest = manifest(&model, &target, &bytes);
    let reader = reader(&target, bytes);
    let baselines: VisualBaselineSet =
        serde_json::from_str(BASELINES_JSON).expect("parse visual baselines");
    let reviews = vec![approved_review("visual.small-size-legibility.mark")];

    let report = evaluate(
        &model,
        &manifest,
        &target,
        &reader,
        &baselines,
        &reviews,
        QualityScope::Package,
    );

    assert!(report.release_allowed, "{}", report.human_summary());
    assert!(report.coverage.skipped > 0);
    assert!(report.checks.iter().any(|check| {
        check.id == "accessibility.contrast.color-text-on-color-canvas"
            && check.status == QualityStatus::Passed
    }));
    assert!(report.checks.iter().any(|check| {
        check.id == "visual.regression.fixture-mark-normal" && check.status == QualityStatus::Passed
    }));
    assert!(report.checks.iter().any(|check| {
        check.category == QualityCategory::Renderer && check.status == QualityStatus::Skipped
    }));
}

#[test]
fn visual_diff_blocks_until_a_human_approves_the_change() {
    let model = valid_model(NORMAL_SVG);
    let target = svg_target("fixture-mark-normal", "fixture/mark-normal.svg");
    let bytes = TRANSPARENT_SVG.as_bytes().to_vec();
    let manifest = manifest(&model, &target, &bytes);
    let reader = reader(&target, bytes);
    let baselines: VisualBaselineSet =
        serde_json::from_str(BASELINES_JSON).expect("parse visual baselines");
    let mut reviews = vec![approved_review("visual.small-size-legibility.mark")];

    let blocked = evaluate(
        &model,
        &manifest,
        &target,
        &reader,
        &baselines,
        &reviews,
        QualityScope::Package,
    );
    assert!(!blocked.release_allowed);
    let visual_diff = blocked
        .checks
        .iter()
        .find(|check| check.id == "visual.regression.fixture-mark-normal")
        .expect("visual diff check");
    assert_eq!(visual_diff.status, QualityStatus::ReviewRequired);
    assert!(visual_diff.source_context.is_some());
    assert!(visual_diff.generated_context.is_some());

    reviews.push(approved_review("visual.regression.fixture-mark-normal"));
    let approved = evaluate(
        &model,
        &manifest,
        &target,
        &reader,
        &baselines,
        &reviews,
        QualityScope::Package,
    );
    assert!(approved.release_allowed, "{}", approved.human_summary());
}

#[test]
fn publication_scope_requires_renderer_evidence() {
    let model = valid_model(NORMAL_SVG);
    let target = svg_target("fixture-mark-normal", "fixture/mark-normal.svg");
    let bytes = NORMAL_SVG.as_bytes().to_vec();
    let manifest = manifest(&model, &target, &bytes);
    let reader = reader(&target, bytes);
    let baselines: VisualBaselineSet =
        serde_json::from_str(BASELINES_JSON).expect("parse visual baselines");
    let mut reviews = vec![approved_review("visual.small-size-legibility.mark")];

    let blocked = evaluate(
        &model,
        &manifest,
        &target,
        &reader,
        &baselines,
        &reviews,
        QualityScope::Publication,
    );
    assert!(!blocked.release_allowed);
    assert_eq!(blocked.coverage.review_required, 6);

    for check_id in [
        "renderer.keyboard-operation",
        "renderer.focus-states",
        "renderer.copy-download-controls",
        "renderer.no-color-high-contrast",
        "renderer.target-size",
        "renderer.performance-budget",
    ] {
        reviews.push(approved_review(check_id));
    }
    let approved = evaluate(
        &model,
        &manifest,
        &target,
        &reader,
        &baselines,
        &reviews,
        QualityScope::Publication,
    );
    assert!(approved.release_allowed, "{}", approved.human_summary());
}

#[test]
fn missing_license_and_approval_fail_closed() {
    let mut model = valid_model(NORMAL_SVG);
    model.source_governance.clear();
    let target = svg_target("fixture-mark-normal", "fixture/mark-normal.svg");
    let bytes = NORMAL_SVG.as_bytes().to_vec();
    let manifest = manifest(&model, &target, &bytes);
    let reader = reader(&target, bytes);
    let baselines: VisualBaselineSet =
        serde_json::from_str(BASELINES_JSON).expect("parse visual baselines");
    let reviews = vec![approved_review("visual.small-size-legibility.mark")];

    let report = evaluate(
        &model,
        &manifest,
        &target,
        &reader,
        &baselines,
        &reviews,
        QualityScope::Package,
    );
    assert!(!report.release_allowed);
    assert!(report.checks.iter().any(|check| {
        check.id == "licensing.approved.mark" && check.status == QualityStatus::Failed
    }));
    assert!(report.checks.iter().any(|check| {
        check.id == "provenance.approval.mark" && check.status == QualityStatus::Failed
    }));
}

#[test]
fn extreme_aspect_ratio_fixture_is_visible_as_a_warning() {
    let source = source_asset(WIDE_SVG);
    let checks = svg_source_checks("wide", &source);
    assert!(checks.iter().any(|check| {
        check.id == "visual.svg-aspect-ratio.wide" && check.status == QualityStatus::Warning
    }));
}

#[test]
fn external_svg_resource_is_a_blocking_failure() {
    let source = source_asset(
        "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 10 10\"><image href=\"https://example.invalid/a.png\"/></svg>",
    );
    let checks = svg_source_checks("remote", &source);
    assert!(checks.iter().any(|check| {
        check.id == "visual.svg-external-resources.remote"
            && check.status == QualityStatus::Failed
            && check.blocking
    }));
}

#[test]
fn generated_png_dimensions_are_enforced() {
    let model = valid_model(NORMAL_SVG);
    let mut pixmap = resvg::tiny_skia::Pixmap::new(16, 16).expect("create pixmap");
    pixmap.fill(resvg::tiny_skia::Color::from_rgba8(102, 51, 170, 255));
    let bytes = pixmap.encode_png().expect("encode PNG");
    let target = png_target("fixture-icon", "fixture/icon.png", 32, 32);
    let manifest = manifest(&model, &target, &bytes);
    let reader = reader(&target, bytes.clone());
    let baselines = VisualBaselineSet {
        schema: super::VISUAL_BASELINES_SCHEMA.to_owned(),
        baselines: vec![VisualBaseline {
            target_id: target.id.clone(),
            sha256: sha256_hex(&bytes),
            source_context: "synthetic fixture".to_owned(),
            generated_context: target.relative_path.clone(),
        }],
    };
    let reviews = vec![approved_review("visual.small-size-legibility.mark")];

    let report = evaluate(
        &model,
        &manifest,
        &target,
        &reader,
        &baselines,
        &reviews,
        QualityScope::Package,
    );
    assert!(!report.release_allowed);
    assert!(report.checks.iter().any(|check| {
        check.id == "visual.png-dimensions.fixture-icon" && check.status == QualityStatus::Failed
    }));
}

#[test]
fn checked_in_visual_baseline_registry_is_valid_and_complete() {
    let baselines: VisualBaselineSet =
        serde_json::from_str(BASELINES_JSON).expect("parse visual baselines");
    let by_target = baselines.by_target().expect("index visual baselines");
    assert_eq!(by_target.len(), 3);
    assert_eq!(
        by_target["fixture-mark-transparent"].sha256,
        sha256_hex(TRANSPARENT_SVG.as_bytes())
    );
}

#[allow(clippy::too_many_arguments)]
fn evaluate(
    model: &BrandKitModel,
    manifest: &CompilerManifest,
    target: &ProjectionTarget,
    reader: &MemoryReader,
    baselines: &VisualBaselineSet,
    reviews: &[HumanReviewEvidence],
    scope: QualityScope,
) -> super::QualityReport {
    QualityHarness::default()
        .evaluate(&QualityInput {
            model,
            manifest,
            targets: std::slice::from_ref(target),
            artifacts: reader,
            baselines,
            human_reviews: reviews,
            scope,
        })
        .expect("evaluate quality")
}

fn valid_model(source_text: &str) -> BrandKitModel {
    let mut tokens = BTreeMap::new();
    tokens.insert(
        "color.canvas".to_owned(),
        token(
            "color",
            json!({"colorSpace":"srgb","components":[0.98,0.98,1.0],"alpha":1}),
        ),
    );
    tokens.insert(
        "color.text".to_owned(),
        token(
            "color",
            json!({"colorSpace":"srgb","components":[0.05,0.06,0.10],"alpha":1}),
        ),
    );
    tokens.insert(
        "motion.duration.standard".to_owned(),
        token("duration", json!({"value":180,"unit":"ms"})),
    );
    tokens.insert(
        "motion.duration.reduced".to_owned(),
        token("duration", json!({"value":0,"unit":"ms"})),
    );
    BrandKitModel {
        schema: BRAND_KIT_MODEL_SCHEMA.to_owned(),
        project_id: "fixture".to_owned(),
        source_digest: sha256_hex(b"fixture-source"),
        project: BrandKitProject {
            display_name: "Fixture".to_owned(),
            repository: "https://example.invalid/fixture".to_owned(),
            tagline: "Quality fixture".to_owned(),
        },
        tokens,
        sources: BTreeMap::from([("mark".to_owned(), source_asset(source_text))]),
        source_governance: BTreeMap::from([("mark".to_owned(), source_governance())]),
        approvals: BTreeSet::from(["approve-mark".to_owned()]),
        guidance: BrandKitGuidance::default(),
    }
}

fn token(token_type: &str, value: serde_json::Value) -> BrandKitToken {
    BrandKitToken {
        token_type: token_type.to_owned(),
        value,
        source_layer: "fixture".to_owned(),
        override_reason: None,
        approval: None,
    }
}

fn source_asset(text: &str) -> BrandKitSourceAsset {
    BrandKitSourceAsset {
        media_type: "image/svg+xml".to_owned(),
        text: text.to_owned(),
        sha256: sha256_hex(text.as_bytes()),
        alt_text: "A geometric fixture mark.".to_owned(),
        safe_zone: Some(0.54),
    }
}

fn source_governance() -> BrandKitSourceGovernance {
    BrandKitSourceGovernance {
        license: BrandKitLicense {
            spdx: "MIT".to_owned(),
            status: "approved".to_owned(),
            attribution: "Copyright 2026 Ego Hygiene".to_owned(),
        },
        origin: BrandKitOrigin {
            creator: "Ego Hygiene".to_owned(),
            method: "first-party".to_owned(),
            source: "tests/fixtures/quality".to_owned(),
            captured_at: "2026-08-22T12:00:00Z".to_owned(),
        },
        approval: "approve-mark".to_owned(),
    }
}

fn svg_target(id: &str, path: &str) -> ProjectionTarget {
    ProjectionTarget {
        id: id.to_owned(),
        profile: "fixture".to_owned(),
        relative_path: path.to_owned(),
        adapter_id: "identity-source-svg".to_owned(),
        media_type: "image/svg+xml".to_owned(),
        parameters: BTreeMap::from([("role".to_owned(), json!("mark"))]),
        required_approval: None,
        maximum_bytes: Some(64_000),
    }
}

fn png_target(id: &str, path: &str, width: u32, height: u32) -> ProjectionTarget {
    ProjectionTarget {
        id: id.to_owned(),
        profile: "fixture".to_owned(),
        relative_path: path.to_owned(),
        adapter_id: "identity-raster".to_owned(),
        media_type: "image/png".to_owned(),
        parameters: BTreeMap::from([
            ("width".to_owned(), json!(width)),
            ("height".to_owned(), json!(height)),
            ("maskable".to_owned(), json!(false)),
        ]),
        required_approval: None,
        maximum_bytes: Some(64_000),
    }
}

fn manifest(model: &BrandKitModel, target: &ProjectionTarget, bytes: &[u8]) -> CompilerManifest {
    CompilerManifest {
        schema: COMPILER_MANIFEST_SCHEMA.to_owned(),
        project_id: model.project_id.clone(),
        source_digest: model.source_digest.clone(),
        plan_digest: sha256_hex(b"quality-plan"),
        outputs: vec![ManifestOutput {
            target_id: target.id.clone(),
            profile: target.profile.clone(),
            path: target.relative_path.clone(),
            media_type: target.media_type.clone(),
            adapter_id: target.adapter_id.clone(),
            adapter_version: "1.0.0".to_owned(),
            input_fingerprint: sha256_hex(b"quality-input"),
            sha256: sha256_hex(bytes),
            bytes: u64::try_from(bytes.len()).expect("fixture length fits u64"),
        }],
        adapters: Vec::new(),
        evidence: Vec::new(),
    }
}

fn reader(target: &ProjectionTarget, bytes: Vec<u8>) -> MemoryReader {
    MemoryReader {
        files: BTreeMap::from([(target.relative_path.clone(), bytes)]),
    }
}

fn approved_review(check_id: &str) -> HumanReviewEvidence {
    HumanReviewEvidence {
        check_id: check_id.to_owned(),
        approved: true,
        reviewer: "reviewer".to_owned(),
        reviewed_at: "2026-08-22T12:30:00Z".to_owned(),
        evidence: "Reviewed against source and generated context.".to_owned(),
    }
}
