// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

use std::collections::{BTreeMap, BTreeSet};

use serde_json::json;

use super::{
    MOTION_POLICY_SCHEMA, MotionBehavior, MotionCaptureContext, MotionNetworkMode, MotionPolicy,
    MotionPurpose, MotionQualityExtension, ReducedMotionBehavior, VISUAL_MOTION_MANIFEST_SCHEMA,
    VisualMotionAsset, VisualMotionGenerator, VisualMotionKind, VisualMotionManifest,
    VisualMotionOutput, VisualMotionSource, VisualMotionSourceMethod,
};
use crate::brandkit::{
    BRAND_KIT_MODEL_SCHEMA, BrandKitGuidance, BrandKitLicense, BrandKitModel, BrandKitOrigin,
    BrandKitProject, BrandKitSourceAsset, BrandKitSourceGovernance, BrandKitToken,
};
use crate::compiler::{
    COMPILER_MANIFEST_SCHEMA, CompilerManifest, CompilerResult, ManifestOutput, ProjectionTarget,
    sha256_hex,
};
use crate::quality::{
    HumanReviewEvidence, QualityArtifactReader, QualityHarness, QualityInput, QualityScope,
    QualityStatus, VISUAL_BASELINES_SCHEMA, VisualBaseline, VisualBaselineSet,
};

const MARK_SVG: &str = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 32 32\"><rect width=\"32\" height=\"32\" fill=\"#111827\"/><circle cx=\"16\" cy=\"16\" r=\"8\" fill=\"#f4e8cf\"/></svg>";
const HERO_SVG: &str = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 1200 630\"><rect width=\"1200\" height=\"630\" fill=\"#09090b\"/><path d=\"M600 120 700 315 600 510 500 315Z\" fill=\"#f4e8cf\"/></svg>";
const HERO_CHANGED_SVG: &str = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 1200 630\"><rect width=\"1200\" height=\"630\" fill=\"#09090b\"/><circle cx=\"600\" cy=\"315\" r=\"96\" fill=\"#f4e8cf\"/></svg>";
const REDUCED_SVG: &str = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 1200 630\"><rect width=\"1200\" height=\"630\" fill=\"#09090b\"/><path d=\"M600 140 680 315 600 490 520 315Z\" fill=\"#f4e8cf\"/></svg>";

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
fn valid_landing_sequence_extends_the_single_release_decision() {
    let fixture = fixture(HERO_SVG);
    let report = evaluate_motion(&fixture).expect("evaluate quality with motion extension");

    assert!(report.release_allowed, "{}", report.human_summary());
    assert!(report.checks.iter().any(|check| {
        check.id == "motion.reduced-motion.identity-hero" && check.status == QualityStatus::Passed
    }));
    assert!(report.checks.iter().any(|check| {
        check.id == "motion.capture.network.identity-hero" && check.status == QualityStatus::Passed
    }));
}

#[test]
fn layout_property_motion_fails_closed() {
    let mut fixture = fixture(HERO_SVG);
    fixture.motion_manifest.assets[0]
        .behavior
        .animated_properties
        .insert("width".to_owned());
    let report = evaluate_motion(&fixture).expect("evaluate layout-property failure");

    assert!(!report.release_allowed);
    assert!(report.checks.iter().any(|check| {
        check.id == "motion.properties.identity-hero" && check.status == QualityStatus::Failed
    }));
}

#[test]
fn live_network_or_real_data_capture_fails_closed() {
    let mut fixture = fixture(HERO_SVG);
    fixture.motion_manifest.assets[0].capture.network_mode = MotionNetworkMode::Live;
    fixture.motion_manifest.assets[0].capture.synthetic_data = false;
    let report = evaluate_motion(&fixture).expect("evaluate unsafe capture");

    assert!(!report.release_allowed);
    assert!(report.checks.iter().any(|check| {
        check.id == "motion.capture.network.identity-hero" && check.status == QualityStatus::Failed
    }));
    assert!(report.checks.iter().any(|check| {
        check.id == "motion.capture.privacy.identity-hero" && check.status == QualityStatus::Failed
    }));
}

#[test]
fn landing_sequence_requires_digest_bound_reduced_motion_fallback() {
    let mut fixture = fixture(HERO_SVG);
    fixture.motion_manifest.assets[0].behavior.fallback_path = None;
    fixture.motion_manifest.assets[0].behavior.fallback_sha256 = None;
    let report = evaluate_motion(&fixture).expect("evaluate missing fallback");

    assert!(!report.release_allowed);
    assert!(report.checks.iter().any(|check| {
        check.id == "motion.reduced-motion.identity-hero" && check.status == QualityStatus::Failed
    }));
}

#[test]
fn visual_motion_diff_requires_explicit_human_review() {
    let mut fixture = fixture(HERO_CHANGED_SVG);
    fixture.motion_baseline_sha = sha256_hex(HERO_SVG.as_bytes());
    fixture.rebuild_baselines();

    let blocked = evaluate_motion(&fixture).expect("evaluate changed baseline");
    assert!(!blocked.release_allowed);
    assert!(blocked.checks.iter().any(|check| {
        check.id == "visual.regression.identity-hero-motion"
            && check.status == QualityStatus::ReviewRequired
    }));

    fixture
        .reviews
        .push(review("visual.regression.identity-hero-motion"));
    let approved = evaluate_motion(&fixture).expect("evaluate approved changed baseline");
    assert!(approved.release_allowed, "{}", approved.human_summary());
}

#[test]
fn captured_demo_requires_immutable_script_and_fixture_lineage() {
    let mut fixture = fixture(HERO_SVG);
    let asset = &mut fixture.motion_manifest.assets[0];
    asset.kind = VisualMotionKind::DemoCapture;
    asset.behavior.purpose = MotionPurpose::DemoCapture;
    asset.behavior.autoplay = false;
    asset.behavior.animated_properties.clear();
    asset.behavior.easing = "n/a".to_owned();
    asset.source.method = VisualMotionSourceMethod::Captured;
    asset.source.repository = Some("https://github.com/egohygiene/egohygiene.io".to_owned());
    asset.source.commit = None;
    asset.source.script_path = Some("tests/capture/identity.ts".to_owned());
    asset.source.fixture_path = Some("tests/fixtures/identity.json".to_owned());
    asset.source.fixture_sha256 = Some(sha256_hex(b"fixture"));

    let report = evaluate_motion(&fixture).expect("evaluate captured lineage");
    assert!(!report.release_allowed);
    assert!(report.checks.iter().any(|check| {
        check.id == "motion.provenance.capture-lineage.identity-hero"
            && check.status == QualityStatus::Failed
    }));
}

#[test]
fn purpose_specific_duration_and_file_size_budgets_block_regressions() {
    let mut fixture = fixture(HERO_SVG);
    fixture.motion_manifest.assets[0].output.duration_ms = Some(2_001);
    fixture.policy.asset_bytes.landing_sequence = 8;

    let report = evaluate_motion(&fixture).expect("evaluate budget failures");
    assert!(!report.release_allowed);
    assert!(report.checks.iter().any(|check| {
        check.id == "motion.duration.identity-hero" && check.status == QualityStatus::Failed
    }));
    assert!(report.checks.iter().any(|check| {
        check.id == "motion.file-size.identity-hero" && check.status == QualityStatus::Failed
    }));
}

#[test]
fn motion_policy_and_manifest_versions_fail_before_evidence_is_claimed() {
    let mut fixture = fixture(HERO_SVG);
    fixture.policy.schema = "identity.motion-policy/v2".to_owned();

    let error = evaluate_motion(&fixture).expect_err("unsupported policy version must fail");
    assert_eq!(error.diagnostics[0].code, "IDN3301");
}

fn evaluate_motion(fixture: &MotionFixture) -> CompilerResult<crate::quality::QualityReport> {
    MotionQualityExtension::new(&fixture.policy, &fixture.motion_manifest)
        .evaluate(&QualityHarness::default(), &fixture.quality_input())
}

struct MotionFixture {
    policy: MotionPolicy,
    model: BrandKitModel,
    compiler_manifest: CompilerManifest,
    targets: Vec<ProjectionTarget>,
    reader: MemoryReader,
    baselines: VisualBaselineSet,
    reviews: Vec<HumanReviewEvidence>,
    motion_manifest: VisualMotionManifest,
    motion_baseline_sha: String,
}

impl MotionFixture {
    fn quality_input(&self) -> QualityInput<'_> {
        QualityInput {
            model: &self.model,
            manifest: &self.compiler_manifest,
            targets: &self.targets,
            artifacts: &self.reader,
            baselines: &self.baselines,
            human_reviews: &self.reviews,
            scope: QualityScope::Package,
        }
    }

    fn rebuild_baselines(&mut self) {
        self.baselines = VisualBaselineSet {
            schema: VISUAL_BASELINES_SCHEMA.to_owned(),
            baselines: vec![
                VisualBaseline {
                    target_id: "fixture-mark".to_owned(),
                    sha256: sha256_hex(MARK_SVG.as_bytes()),
                    source_context: "canonical mark fixture".to_owned(),
                    generated_context: "fixture/mark.svg".to_owned(),
                },
                VisualBaseline {
                    target_id: "identity-hero-motion".to_owned(),
                    sha256: self.motion_baseline_sha.clone(),
                    source_context: "approved landing hero source".to_owned(),
                    generated_context: "motion/identity-hero.svg".to_owned(),
                },
            ],
        };
    }
}

#[allow(clippy::too_many_lines)]
fn fixture(hero_svg: &str) -> MotionFixture {
    let source_digest = sha256_hex(b"motion-fixture-source");
    let mark_sha = sha256_hex(MARK_SVG.as_bytes());
    let hero_sha = sha256_hex(hero_svg.as_bytes());
    let reduced_sha = sha256_hex(REDUCED_SVG.as_bytes());
    let mut tokens = BTreeMap::new();
    tokens.insert(
        "color.canvas".to_owned(),
        token(
            "color",
            json!({"colorSpace":"srgb","components":[0.02,0.02,0.03],"alpha":1}),
        ),
    );
    tokens.insert(
        "color.text".to_owned(),
        token(
            "color",
            json!({"colorSpace":"srgb","components":[0.96,0.91,0.81],"alpha":1}),
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

    let model = BrandKitModel {
        schema: BRAND_KIT_MODEL_SCHEMA.to_owned(),
        project_id: "identity".to_owned(),
        source_digest: source_digest.clone(),
        project: BrandKitProject {
            display_name: "identity".to_owned(),
            repository: "https://github.com/egohygiene/identity".to_owned(),
            tagline: "brand kit generator".to_owned(),
        },
        tokens,
        sources: BTreeMap::from([(
            "mark".to_owned(),
            BrandKitSourceAsset {
                media_type: "image/svg+xml".to_owned(),
                text: MARK_SVG.to_owned(),
                sha256: mark_sha.clone(),
                alt_text: "A geometric Identity fixture mark.".to_owned(),
                safe_zone: Some(0.54),
            },
        )]),
        source_governance: BTreeMap::from([(
            "mark".to_owned(),
            BrandKitSourceGovernance {
                license: BrandKitLicense {
                    spdx: "MIT".to_owned(),
                    status: "approved".to_owned(),
                    attribution: "Copyright 2026 Ego Hygiene".to_owned(),
                },
                origin: BrandKitOrigin {
                    creator: "Ego Hygiene".to_owned(),
                    method: "first-party".to_owned(),
                    source: "motion fixture".to_owned(),
                    captured_at: "2026-08-22T12:00:00Z".to_owned(),
                },
                approval: "approve-mark".to_owned(),
            },
        )]),
        approvals: BTreeSet::from(["approve-mark".to_owned(), "approve-motion".to_owned()]),
        guidance: BrandKitGuidance::default(),
    };

    let target = ProjectionTarget {
        id: "fixture-mark".to_owned(),
        profile: "fixture".to_owned(),
        relative_path: "fixture/mark.svg".to_owned(),
        adapter_id: "identity-source-svg".to_owned(),
        media_type: "image/svg+xml".to_owned(),
        parameters: BTreeMap::from([("role".to_owned(), json!("mark"))]),
        required_approval: None,
        maximum_bytes: Some(64_000),
    };
    let compiler_manifest = CompilerManifest {
        schema: COMPILER_MANIFEST_SCHEMA.to_owned(),
        project_id: model.project_id.clone(),
        source_digest: source_digest.clone(),
        plan_digest: sha256_hex(b"motion-plan"),
        outputs: vec![ManifestOutput {
            target_id: target.id.clone(),
            profile: target.profile.clone(),
            path: target.relative_path.clone(),
            media_type: target.media_type.clone(),
            adapter_id: target.adapter_id.clone(),
            adapter_version: "1.0.0".to_owned(),
            input_fingerprint: sha256_hex(b"motion-input"),
            sha256: mark_sha,
            bytes: u64::try_from(MARK_SVG.len()).expect("fixture length fits u64"),
        }],
        adapters: Vec::new(),
        evidence: Vec::new(),
    };

    let motion_asset = VisualMotionAsset {
        id: "identity-hero".to_owned(),
        kind: VisualMotionKind::Animation,
        source: VisualMotionSource {
            creator: "Ego Hygiene".to_owned(),
            method: VisualMotionSourceMethod::FirstParty,
            reference: "docs/identity-hero.storyboard.md".to_owned(),
            sha256: sha256_hex(b"identity-hero-storyboard"),
            license_spdx: "MIT".to_owned(),
            approval: "approve-motion".to_owned(),
            repository: None,
            commit: None,
            script_path: None,
            fixture_path: None,
            fixture_sha256: None,
        },
        generator: VisualMotionGenerator {
            id: "identity-fixture-renderer".to_owned(),
            version: "1.0.0".to_owned(),
        },
        output: VisualMotionOutput {
            path: "motion/identity-hero.svg".to_owned(),
            media_type: "image/svg+xml".to_owned(),
            sha256: hero_sha.clone(),
            bytes: u64::try_from(hero_svg.len()).expect("fixture length fits u64"),
            width: 1_200,
            height: 630,
            frame_rate: Some(60.0),
            duration_ms: Some(1_200),
        },
        behavior: MotionBehavior {
            purpose: MotionPurpose::LandingSequence,
            animated_properties: BTreeSet::from(["opacity".to_owned(), "transform".to_owned()]),
            easing: "standard".to_owned(),
            blocks_interaction: false,
            autoplay: true,
            looped: false,
            muted: true,
            reduced_motion: ReducedMotionBehavior::StaticFallback,
            fallback_path: Some("motion/identity-hero-reduced.svg".to_owned()),
            fallback_sha256: Some(reduced_sha),
        },
        capture: MotionCaptureContext {
            viewport_width: 1_200,
            viewport_height: 630,
            locale: "en-US".to_owned(),
            timezone: "UTC".to_owned(),
            network_mode: MotionNetworkMode::Offline,
            privacy_safe: true,
            synthetic_data: true,
        },
        baseline_target_id: "identity-hero-motion".to_owned(),
    };
    let motion_manifest = VisualMotionManifest {
        schema: VISUAL_MOTION_MANIFEST_SCHEMA.to_owned(),
        project_id: model.project_id.clone(),
        source_digest,
        assets: vec![motion_asset],
    };

    let mut fixture = MotionFixture {
        policy: MotionPolicy {
            schema: MOTION_POLICY_SCHEMA.to_owned(),
            ..MotionPolicy::default()
        },
        model,
        compiler_manifest,
        targets: vec![target],
        reader: MemoryReader {
            files: BTreeMap::from([
                ("fixture/mark.svg".to_owned(), MARK_SVG.as_bytes().to_vec()),
                (
                    "motion/identity-hero.svg".to_owned(),
                    hero_svg.as_bytes().to_vec(),
                ),
                (
                    "motion/identity-hero-reduced.svg".to_owned(),
                    REDUCED_SVG.as_bytes().to_vec(),
                ),
            ]),
        },
        baselines: VisualBaselineSet::default(),
        reviews: vec![
            review("visual.small-size-legibility.mark"),
            review("motion.meaning.identity-hero"),
            review("motion.direction.identity-hero"),
        ],
        motion_manifest,
        motion_baseline_sha: hero_sha,
    };
    fixture.rebuild_baselines();
    fixture
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

fn review(check_id: &str) -> HumanReviewEvidence {
    HumanReviewEvidence {
        check_id: check_id.to_owned(),
        approved: true,
        reviewer: "fixture-reviewer".to_owned(),
        reviewed_at: "2026-08-22T12:00:00Z".to_owned(),
        evidence: "tests/fixtures/motion/review.md".to_owned(),
    }
}
