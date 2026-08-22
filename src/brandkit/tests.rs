// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

use std::collections::{BTreeMap, BTreeSet};
use std::fs;

use serde_json::json;
use tempfile::TempDir;

use crate::brandkit::{
    BrandKitGuidance, BrandKitProject, BrandKitSourceAsset, BrandKitToken, ProfileSelection,
    all_profiles, compiler_request, register_builtin_adapters,
};
use crate::compiler::{
    AdapterRegistry, Compiler, CompilerResult, IdentityIntent, IdentityReader, IdentityResolver,
    IdentityValidator, LocalArtifactStore, ResolvedIdentity, ValidationReport, sha256_hex,
};

const MARK_SVG: &str =
    include_str!("../../tests/fixtures/v1/valid/minimal/.identity/sources/mark.svg");

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
fn all_profiles_generate_complete_versioned_brand_kit() {
    let temporary = TempDir::new().expect("create temp repo");
    let (reader, validator, resolver) = fixture_pipeline();
    let request = compiler_request("assets/identity", &all_profiles()).expect("build request");
    let mut registry = AdapterRegistry::new();
    register_builtin_adapters(&mut registry).expect("register built-ins");
    let mut store = LocalArtifactStore::new(temporary.path()).expect("create store");
    let mut compiler = Compiler::new(&reader, &validator, &resolver, &registry, &mut store);

    let prepared = compiler.prepare(request.clone()).expect("prepare full kit");
    assert_eq!(prepared.plan.actions.len(), request.targets.len() + 1);
    assert!(!prepared.plan.has_blocking_diagnostics());
    let manifest = compiler
        .execute(&prepared, &BTreeSet::new())
        .expect("generate full kit");

    assert_eq!(manifest.outputs.len(), request.targets.len());
    assert_eq!(manifest.outputs.len(), 25);
    assert!(
        temporary
            .path()
            .join("assets/identity/packages/tokens/tokens.css")
            .is_file()
    );
    assert!(
        temporary
            .path()
            .join("assets/identity/packages/tokens/tailwind.theme.json")
            .is_file()
    );
    assert!(
        temporary
            .path()
            .join("assets/identity/packages/metadata/metadata.json")
            .is_file()
    );
    assert!(
        temporary
            .path()
            .join("assets/identity/docs/document.css")
            .is_file()
    );
    assert!(
        temporary
            .path()
            .join("assets/identity/social/card-1200x630.png")
            .is_file()
    );
    assert!(
        temporary
            .path()
            .join("assets/identity/github/social-preview.png")
            .is_file()
    );
    assert!(
        temporary
            .path()
            .join("assets/identity/pwa/icon-maskable-512.png")
            .is_file()
    );
    assert!(
        temporary
            .path()
            .join("assets/identity/packages/brand-kit/brand-kit.zip")
            .is_file()
    );

    let css = fs::read_to_string(
        temporary
            .path()
            .join("assets/identity/packages/tokens/tokens.css"),
    )
    .expect("read CSS package");
    assert!(css.contains("--identity-color-brand-primary: #6b33b8;"));
    assert!(css.contains("--identity-color-canvas: #fafaff;"));

    let tailwind: serde_json::Value = serde_json::from_slice(
        &fs::read(
            temporary
                .path()
                .join("assets/identity/packages/tokens/tailwind.theme.json"),
        )
        .expect("read Tailwind package"),
    )
    .expect("parse Tailwind package");
    assert_eq!(
        tailwind["theme"]["extend"]["colors"]["brand-primary"],
        "#6b33b8"
    );

    let maskable = resvg::tiny_skia::Pixmap::decode_png(
        &fs::read(
            temporary
                .path()
                .join("assets/identity/pwa/icon-maskable-512.png"),
        )
        .expect("read maskable icon"),
    )
    .expect("decode maskable icon");
    assert_eq!((maskable.width(), maskable.height()), (512, 512));
    assert!(manifest.evidence.iter().any(|evidence| {
        evidence.target_id == "pwa-maskable-512" && evidence.check == "maskable-safe-zone"
    }));
}

#[test]
fn same_source_generates_byte_identical_packages_across_repositories() {
    let first = TempDir::new().expect("create first temp repo");
    let second = TempDir::new().expect("create second temp repo");
    let first_manifest = generate_all(&first);
    let second_manifest = generate_all(&second);
    assert_eq!(first_manifest, second_manifest);

    for relative in [
        "assets/identity/packages/tokens/tokens.json",
        "assets/identity/packages/tokens/tokens.css",
        "assets/identity/social/card-1200x630.png",
        "assets/identity/packages/brand-kit/checksums.json",
        "assets/identity/packages/brand-kit/brand-kit.zip",
    ] {
        assert_eq!(
            fs::read(first.path().join(relative)).expect("read first package"),
            fs::read(second.path().join(relative)).expect("read second package"),
            "{relative} differs across repositories"
        );
    }
}

#[test]
fn repeated_generation_is_incremental_and_does_not_rewrite_packages() {
    let temporary = TempDir::new().expect("create temp repo");
    let first_manifest = generate_all(&temporary);
    let manifest_path = temporary
        .path()
        .join("assets/identity/.identity-manifest.json");
    let manifest_before = fs::read(&manifest_path).expect("read initial manifest");

    let (reader, validator, resolver) = fixture_pipeline();
    let request = compiler_request("assets/identity", &all_profiles()).expect("build request");
    let mut registry = AdapterRegistry::new();
    register_builtin_adapters(&mut registry).expect("register built-ins");
    let mut store = LocalArtifactStore::new(temporary.path()).expect("create store");
    let mut compiler = Compiler::new(&reader, &validator, &resolver, &registry, &mut store);
    let prepared = compiler.prepare(request).expect("prepare repeated build");

    assert!(!prepared.plan.has_mutations());
    let second_manifest = compiler
        .execute(&prepared, &BTreeSet::new())
        .expect("execute repeated build");
    assert_eq!(first_manifest, second_manifest);
    assert_eq!(
        manifest_before,
        fs::read(manifest_path).expect("read repeated manifest")
    );
}

#[test]
fn consumers_can_select_only_the_profiles_they_need() {
    let temporary = TempDir::new().expect("create temp repo");
    let selections = vec![
        ProfileSelection {
            id: "tokens".to_owned(),
            version: "1.0.0".to_owned(),
        },
        ProfileSelection {
            id: "metadata".to_owned(),
            version: "1.0.0".to_owned(),
        },
    ];
    let request = compiler_request("assets/identity", &selections).expect("build subset request");
    assert_eq!(request.targets.len(), 11);

    let (reader, validator, resolver) = fixture_pipeline();
    let mut registry = AdapterRegistry::new();
    register_builtin_adapters(&mut registry).expect("register built-ins");
    let mut store = LocalArtifactStore::new(temporary.path()).expect("create store");
    let mut compiler = Compiler::new(&reader, &validator, &resolver, &registry, &mut store);
    let prepared = compiler.prepare(request).expect("prepare subset");
    compiler
        .execute(&prepared, &BTreeSet::new())
        .expect("execute subset");

    assert!(
        temporary
            .path()
            .join("assets/identity/packages/tokens/tokens.css")
            .is_file()
    );
    assert!(
        temporary
            .path()
            .join("assets/identity/packages/metadata/metadata.json")
            .is_file()
    );
    assert!(
        !temporary
            .path()
            .join("assets/identity/pwa/icon-512.png")
            .exists()
    );
    assert!(
        !temporary
            .path()
            .join("assets/identity/packages/brand-kit/brand-kit.zip")
            .exists()
    );
}

#[test]
fn incompatible_profile_versions_fail_before_planning() {
    let error = compiler_request(
        "assets/identity",
        &[ProfileSelection {
            id: "tokens".to_owned(),
            version: "2.0.0".to_owned(),
        }],
    )
    .expect_err("incompatible profile version must fail");
    assert_eq!(error.diagnostics[0].code, "IDN3201");
}

fn generate_all(temporary: &TempDir) -> crate::compiler::CompilerManifest {
    let (reader, validator, resolver) = fixture_pipeline();
    let request = compiler_request("assets/identity", &all_profiles()).expect("build request");
    let mut registry = AdapterRegistry::new();
    register_builtin_adapters(&mut registry).expect("register built-ins");
    let mut store = LocalArtifactStore::new(temporary.path()).expect("create store");
    let mut compiler = Compiler::new(&reader, &validator, &resolver, &registry, &mut store);
    let prepared = compiler.prepare(request).expect("prepare full kit");
    compiler
        .execute(&prepared, &BTreeSet::new())
        .expect("generate full kit")
}

// Keep the fixture's resolved Brand Kit state visible in one deterministic builder.
#[allow(clippy::too_many_lines)]
fn fixture_pipeline() -> (FixtureReader, FixtureValidator, FixtureResolver) {
    let source_digest = sha256_hex(b"identity-v1-fixture");
    let mut tokens = BTreeMap::new();
    tokens.insert(
        "color.brand.primary".to_owned(),
        BrandKitToken {
            token_type: "color".to_owned(),
            value: json!({
                "colorSpace": "srgb",
                "components": [0.42, 0.20, 0.72],
                "alpha": 1
            }),
            source_layer: "example-product".to_owned(),
            override_reason: Some(
                "Give the product a distinct violet technical accent.".to_owned(),
            ),
            approval: Some("approve-product-primary".to_owned()),
        },
    );
    tokens.insert(
        "color.action.primary".to_owned(),
        BrandKitToken {
            token_type: "color".to_owned(),
            value: json!({
                "colorSpace": "srgb",
                "components": [0.42, 0.20, 0.72],
                "alpha": 1
            }),
            source_layer: "example-product".to_owned(),
            override_reason: None,
            approval: None,
        },
    );
    tokens.insert(
        "color.canvas".to_owned(),
        BrandKitToken {
            token_type: "color".to_owned(),
            value: json!({
                "colorSpace": "srgb",
                "components": [0.98, 0.98, 1.0],
                "alpha": 1
            }),
            source_layer: "example-organization".to_owned(),
            override_reason: None,
            approval: None,
        },
    );
    tokens.insert(
        "color.text".to_owned(),
        BrandKitToken {
            token_type: "color".to_owned(),
            value: json!({
                "colorSpace": "srgb",
                "components": [0.05, 0.06, 0.10],
                "alpha": 1
            }),
            source_layer: "example-organization".to_owned(),
            override_reason: None,
            approval: None,
        },
    );
    tokens.insert(
        "typography.body.family".to_owned(),
        BrandKitToken {
            token_type: "fontFamily".to_owned(),
            value: json!(["Inter", "system-ui", "sans-serif"]),
            source_layer: "example-organization".to_owned(),
            override_reason: None,
            approval: None,
        },
    );
    tokens.insert(
        "motion.duration.standard".to_owned(),
        BrandKitToken {
            token_type: "duration".to_owned(),
            value: json!({"value": 180, "unit": "ms"}),
            source_layer: "example-organization".to_owned(),
            override_reason: None,
            approval: None,
        },
    );
    tokens.insert(
        "motion.duration.reduced".to_owned(),
        BrandKitToken {
            token_type: "duration".to_owned(),
            value: json!({"value": 0, "unit": "ms"}),
            source_layer: "example-organization".to_owned(),
            override_reason: None,
            approval: None,
        },
    );

    let mut sources = BTreeMap::new();
    sources.insert(
        "mark".to_owned(),
        BrandKitSourceAsset {
            media_type: "image/svg+xml".to_owned(),
            text: MARK_SVG.to_owned(),
            sha256: sha256_hex(MARK_SVG.as_bytes()),
            alt_text: "A violet diamond nested inside a rounded square.".to_owned(),
            safe_zone: None,
        },
    );

    let project = BrandKitProject {
        display_name: "Example Product".to_owned(),
        repository: "https://example.invalid/example-product".to_owned(),
        tagline: "A complete, governed Identity v1 fixture.".to_owned(),
    };
    let guidance = BrandKitGuidance::default();
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
            "guidance".to_owned(),
            serde_json::to_value(guidance).expect("serialize guidance"),
        ),
    ]);
    let resolved = ResolvedIdentity {
        project_id: "example-product".to_owned(),
        source_digest: source_digest.clone(),
        values,
        lineage: BTreeMap::new(),
        approvals: BTreeSet::from(["approve-product-primary".to_owned()]),
    };
    let intent = IdentityIntent {
        project_id: resolved.project_id.clone(),
        source_digest,
        documents: BTreeMap::new(),
        approvals: resolved.approvals.clone(),
    };

    (
        FixtureReader { intent },
        FixtureValidator,
        FixtureResolver { resolved },
    )
}
