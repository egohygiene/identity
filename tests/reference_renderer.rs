// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

use std::collections::{BTreeMap, BTreeSet};
use std::fs;

use identity::brandkit::{
    BrandKitGuidance, BrandKitLicense, BrandKitOrigin, BrandKitProject, BrandKitSourceAsset,
    BrandKitSourceGovernance, BrandKitToken, all_profiles, compiler_request,
    register_builtin_adapters,
};
use identity::compiler::{
    AdapterRegistry, Compiler, CompilerResult, IdentityIntent, IdentityReader, IdentityResolver,
    IdentityValidator, LocalArtifactStore, ResolvedIdentity, ValidationReport,
};
use identity::reference_renderer::{
    BRAND_KIT_VIEW_MODEL_SCHEMA, BrandKitViewModel, register_reference_renderer_adapter,
    with_reference_renderer,
};
use serde_json::json;
use sha2::{Digest, Sha256};
use tempfile::TempDir;

const MARK_SVG: &str = include_str!("fixtures/v1/valid/minimal/.identity/sources/mark.svg");

#[derive(Clone)]
struct FixtureReader {
    intent: IdentityIntent,
}

impl IdentityReader for FixtureReader {
    fn read(&self) -> CompilerResult<IdentityIntent> {
        Ok(self.intent.clone())
    }
}

struct FixtureValidator;

impl IdentityValidator for FixtureValidator {
    fn validate(&self, _intent: &IdentityIntent) -> CompilerResult<ValidationReport> {
        Ok(ValidationReport::default())
    }
}

#[derive(Clone)]
struct FixtureResolver {
    resolved: ResolvedIdentity,
}

impl IdentityResolver for FixtureResolver {
    fn resolve(&self, _intent: &IdentityIntent) -> CompilerResult<ResolvedIdentity> {
        Ok(self.resolved.clone())
    }
}

#[test]
fn compiler_generates_an_immutable_reference_renderer_view_model() {
    let first = TempDir::new().expect("create first temporary repository");
    let second = TempDir::new().expect("create second temporary repository");

    let first_bytes = generate_view_model(&first);
    let second_bytes = generate_view_model(&second);
    assert_eq!(first_bytes, second_bytes);

    let view_model =
        serde_json::from_slice::<BrandKitViewModel>(&first_bytes).expect("parse view model");
    assert_eq!(view_model.schema, BRAND_KIT_VIEW_MODEL_SCHEMA);
    assert_eq!(view_model.project.display_name, "Example Product");
    assert_eq!(view_model.release.status, "generated");
    assert_eq!(view_model.release.immutable_id.len(), 71);
    assert_eq!(view_model.guidance.voice.status, "declared");
    assert_eq!(view_model.guidance.usage.status, "declared");
    assert!(view_model.guidance.voice.canonical);
    assert_eq!(view_model.support.motion.status, "declared");
    assert_eq!(view_model.support.imagery.status, "not-declared");
    assert_eq!(view_model.support.mascot.status, "not-declared");
    assert_eq!(view_model.assets.len(), 1);
    assert_eq!(
        view_model.assets[0].dimensions,
        "64 × 64 SVG viewBox units"
    );
    assert_eq!(
        view_model.assets[0].intended_use,
        "Primary scalable brand mark for approved product surfaces."
    );
    assert_eq!(
        view_model.assets[0].download_path.as_deref(),
        Some("brand/mark.svg")
    );
    assert_eq!(
        view_model.assets[0]
            .license
            .as_ref()
            .map(|license| license.spdx.as_str()),
        Some("MIT")
    );
    assert!(
        view_model
            .packages
            .iter()
            .any(|package| package.path == "packages/brand-kit/brand-kit.zip")
    );

    let rendered = String::from_utf8(first_bytes).expect("view model must be UTF-8");
    assert!(!rendered.contains("Ego Hygiene"));
}

#[test]
fn renderer_fixture_conforms_to_the_rust_contract() {
    let fixture = include_bytes!("../renderer/fixtures/example.brand-kit.view-model.json");
    let model =
        serde_json::from_slice::<BrandKitViewModel>(fixture).expect("parse renderer fixture");

    assert_eq!(model.schema, BRAND_KIT_VIEW_MODEL_SCHEMA);
    assert_eq!(model.project_id, "example-product");
    assert_eq!(model.release.profile_version, "1.0.0");
    assert!(
        model
            .tokens
            .iter()
            .any(|token| token.path == "color.canvas")
    );
    assert!(model.assets.iter().any(|asset| {
        asset.id == "mark"
            && asset.dimensions == "64 × 64 SVG viewBox units"
            && asset.intended_use
                == "Primary scalable brand mark for approved product surfaces."
    }));
}

fn generate_view_model(temporary: &TempDir) -> Vec<u8> {
    let (reader, validator, resolver) = fixture_pipeline();
    let request = with_reference_renderer(
        compiler_request("assets/identity", &all_profiles()).expect("build request"),
    );
    assert_eq!(request.targets.len(), 26);

    let mut registry = AdapterRegistry::new();
    register_builtin_adapters(&mut registry).expect("register Brand Kit adapters");
    register_reference_renderer_adapter(&mut registry)
        .expect("register reference renderer adapter");

    let mut store = LocalArtifactStore::new(temporary.path()).expect("create artifact store");
    let mut compiler = Compiler::new(&reader, &validator, &resolver, &registry, &mut store);
    let prepared = compiler
        .prepare(request)
        .expect("prepare complete Brand Kit");
    let manifest = compiler
        .execute(&prepared, &BTreeSet::new())
        .expect("generate complete Brand Kit");

    assert_eq!(manifest.outputs.len(), 26);
    assert!(manifest.evidence.iter().any(|evidence| {
        evidence.target_id == "reference-renderer-view-model"
            && evidence.check == "immutable-view-model"
    }));

    fs::read(
        temporary
            .path()
            .join("assets/identity/packages/renderer/brand-kit.view-model.json"),
    )
    .expect("read generated reference renderer model")
}

#[allow(clippy::too_many_lines)]
fn fixture_pipeline() -> (FixtureReader, FixtureValidator, FixtureResolver) {
    let source_digest = sha256_hex(b"identity-reference-renderer-fixture");
    let tokens = BTreeMap::from([
        (
            "color.brand.primary".to_owned(),
            color_token([0.42, 0.20, 0.72], "example-product"),
        ),
        (
            "color.canvas".to_owned(),
            color_token([0.98, 0.98, 1.0], "example-organization"),
        ),
        (
            "color.text".to_owned(),
            color_token([0.05, 0.06, 0.10], "example-organization"),
        ),
        (
            "typography.body.family".to_owned(),
            BrandKitToken {
                token_type: "fontFamily".to_owned(),
                value: json!(["Inter", "system-ui", "sans-serif"]),
                source_layer: "example-organization".to_owned(),
                override_reason: None,
                approval: None,
            },
        ),
        (
            "motion.duration.standard".to_owned(),
            BrandKitToken {
                token_type: "duration".to_owned(),
                value: json!({"value": 180, "unit": "ms"}),
                source_layer: "example-organization".to_owned(),
                override_reason: None,
                approval: None,
            },
        ),
    ]);

    let sources = BTreeMap::from([(
        "mark".to_owned(),
        BrandKitSourceAsset {
            media_type: "image/svg+xml".to_owned(),
            text: MARK_SVG.to_owned(),
            sha256: sha256_hex(MARK_SVG.as_bytes()),
            alt_text: "A violet diamond nested inside a rounded square.".to_owned(),
            safe_zone: Some(0.54),
        },
    )]);

    let source_governance = BTreeMap::from([(
        "mark".to_owned(),
        BrandKitSourceGovernance {
            license: BrandKitLicense {
                spdx: "MIT".to_owned(),
                status: "approved".to_owned(),
                attribution: "Example Product contributors".to_owned(),
            },
            origin: BrandKitOrigin {
                creator: "Example Product design team".to_owned(),
                method: "vector".to_owned(),
                source: ".identity/sources/mark.svg".to_owned(),
                captured_at: "2026-08-20".to_owned(),
            },
            approval: "approve-example-mark".to_owned(),
        },
    )]);

    let project = BrandKitProject {
        display_name: "Example Product".to_owned(),
        repository: "https://example.invalid/example-product".to_owned(),
        tagline: "A governed reference-renderer fixture.".to_owned(),
    };
    let guidance = BrandKitGuidance {
        voice: Some(json!({
            "personality": ["clear", "warm", "grounded"],
            "principles": ["Explain the reason before the mechanism."]
        })),
        usage: Some(json!({
            "do": ["Use semantic tokens."],
            "dont": ["Invent unreviewed brand facts."]
        })),
    };
    let values = BTreeMap::from([
        (
            "project".to_owned(),
            serde_json::to_value(project).expect("serialize project"),
        ),
        (
            "tokens".to_owned(),
            serde_json::to_value(tokens).expect("serialize tokens"),
        ),
        (
            "sources".to_owned(),
            serde_json::to_value(sources).expect("serialize sources"),
        ),
        (
            "sourceGovernance".to_owned(),
            serde_json::to_value(source_governance).expect("serialize governance"),
        ),
        (
            "guidance".to_owned(),
            serde_json::to_value(guidance).expect("serialize guidance"),
        ),
    ]);
    let approvals = BTreeSet::from([
        "approve-example-mark".to_owned(),
        "approve-product-primary".to_owned(),
    ]);
    let resolved = ResolvedIdentity {
        project_id: "example-product".to_owned(),
        source_digest: source_digest.clone(),
        values,
        lineage: BTreeMap::new(),
        approvals: approvals.clone(),
    };
    let intent = IdentityIntent {
        project_id: resolved.project_id.clone(),
        source_digest,
        documents: BTreeMap::new(),
        approvals,
    };

    (
        FixtureReader { intent },
        FixtureValidator,
        FixtureResolver { resolved },
    )
}

fn color_token(components: [f64; 3], source_layer: &str) -> BrandKitToken {
    BrandKitToken {
        token_type: "color".to_owned(),
        value: json!({
            "colorSpace": "srgb",
            "components": components,
            "alpha": 1
        }),
        source_layer: source_layer.to_owned(),
        override_reason: None,
        approval: None,
    }
}

fn sha256_hex(bytes: &[u8]) -> String {
    format!("{:x}", Sha256::digest(bytes))
}
