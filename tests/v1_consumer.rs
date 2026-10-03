// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

//! End-to-end evidence for the reusable v1 consumer bridge.

use std::collections::BTreeSet;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;

use identity::brandkit::{
    BrandKitModel, GuidanceAudience, ProfileSelection, compiler_request, register_builtin_adapters,
};
use identity::compiler::{AdapterRegistry, Compiler, IdentityResolver, LocalArtifactStore};
use identity::reference_renderer::{register_reference_renderer_adapter, with_reference_renderer};
use identity::v1_consumer::V1ConsumerPipeline;
use serde_json::Value;
use tempfile::TempDir;

fn fixture_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/v1/valid/minimal")
}

#[test]
fn published_v1_source_contract_drives_selected_package_profiles() {
    let pipeline = V1ConsumerPipeline::load(&fixture_root()).expect("load valid v1 consumer");
    let profile_ids = pipeline
        .profiles()
        .iter()
        .map(|profile| profile.id.as_str())
        .collect::<Vec<_>>();
    assert_eq!(profile_ids, ["core", "metadata", "tokens"]);

    let temporary = TempDir::new().expect("create output repository");
    let request = with_reference_renderer(
        compiler_request("assets/identity", pipeline.profiles()).expect("build selected request"),
    );
    let mut registry = AdapterRegistry::new();
    register_builtin_adapters(&mut registry).expect("register package adapters");
    register_reference_renderer_adapter(&mut registry).expect("register renderer adapter");
    let mut store = LocalArtifactStore::new(temporary.path()).expect("create artifact store");
    let mut compiler = Compiler::new(&pipeline, &pipeline, &pipeline, &registry, &mut store);

    let prepared = compiler.prepare(request.clone()).expect("plan v1 package");
    assert!(!prepared.plan.has_blocking_diagnostics());
    let manifest = compiler
        .execute(&prepared, &BTreeSet::new())
        .expect("generate selected v1 package");
    assert_eq!(manifest.outputs.len(), request.targets.len());
    assert!(
        temporary
            .path()
            .join("assets/identity/packages/tokens/tokens.css")
            .is_file()
    );
    assert!(
        temporary
            .path()
            .join("assets/identity/packages/renderer/brand-kit.view-model.json")
            .is_file()
    );
    let css = fs::read_to_string(
        temporary
            .path()
            .join("assets/identity/packages/tokens/tokens.css"),
    )
    .expect("read generated CSS");
    assert!(css.contains("--identity-color-brand-primary: #6b33b8;"));
}

fn copy_tree(source: &Path, destination: &Path) {
    fs::create_dir_all(destination).expect("create fixture directory");
    for entry in fs::read_dir(source).expect("read fixture directory") {
        let entry = entry.expect("read fixture entry");
        let output = destination.join(entry.file_name());
        if entry.file_type().expect("read fixture entry type").is_dir() {
            copy_tree(&entry.path(), &output);
        } else {
            fs::copy(entry.path(), output).expect("copy fixture file");
        }
    }
}

fn guidance_documents(root: &Path) -> Value {
    let document = |name| {
        serde_json::from_slice::<Value>(
            &fs::read(root.join(format!(".identity/guidance/{name}.json")))
                .expect("read guidance source"),
        )
        .expect("parse guidance source")
    };
    serde_json::json!({"voice": document("voice"), "usage": document("usage")})
}

#[test]
fn public_packages_and_renderer_filter_shared_lifecycle_cases_without_mutating_review() {
    let cases: Value = serde_json::from_slice(
        &fs::read(
            PathBuf::from(env!("CARGO_MANIFEST_DIR"))
                .join("tests/fixtures/guidance-public-cases.json"),
        )
        .expect("read shared audience cases"),
    )
    .expect("parse shared audience cases");
    for case in cases["cases"].as_array().expect("shared case list") {
        let repository = TempDir::new().expect("create temporary consumer");
        copy_tree(&fixture_root(), repository.path());
        let mut source = guidance_documents(repository.path());
        for update in case["updates"].as_array().expect("case updates") {
            let document = update["document"].as_str().expect("document name");
            let pointer = update["pointer"].as_str().expect("record pointer");
            *source[document]
                .pointer_mut(pointer)
                .expect("existing record") = update["value"].clone();
        }
        for name in ["voice", "usage"] {
            fs::write(
                repository
                    .path()
                    .join(format!(".identity/guidance/{name}.json")),
                serde_json::to_vec_pretty(&source[name]).expect("serialize case source"),
            )
            .expect("write temporary guidance source");
        }
        let pipeline = V1ConsumerPipeline::load(repository.path()).expect("load case consumer");
        let intent = identity::compiler::IdentityReader::read(&pipeline).expect("read intent");
        let resolved = pipeline.resolve(&intent).expect("resolve source");
        let model = BrandKitModel::from_resolved(&resolved).expect("load Brand Kit model");
        let review = model.guidance.for_audience(GuidanceAudience::Review);
        assert_eq!(
            serde_json::to_value(&review).expect("serialize review"),
            source
        );
        let public = model.guidance.for_audience(GuidanceAudience::Public);
        let public_json = serde_json::to_vec(&public).expect("serialize public projection");
        assert_public_case(&public_json, case);
        assert_python_public_conformance(repository.path(), &public);

        let profiles = ["metadata", "archive"].map(|id| ProfileSelection {
            id: id.to_owned(),
            version: "1.0.0".to_owned(),
        });
        let request = with_reference_renderer(
            compiler_request("assets/identity", &profiles).expect("build public projections"),
        );
        let mut registry = AdapterRegistry::new();
        register_builtin_adapters(&mut registry).expect("register package adapters");
        register_reference_renderer_adapter(&mut registry).expect("register renderer adapter");
        let mut store = LocalArtifactStore::new(repository.path()).expect("create artifact store");
        let mut compiler = Compiler::new(&pipeline, &pipeline, &pipeline, &registry, &mut store);
        let prepared = compiler
            .prepare(request.clone())
            .expect("plan public projections");
        compiler
            .execute(&prepared, &BTreeSet::new())
            .expect("generate public projections");
        for path in [
            "packages/guidance/voice-and-usage.json",
            "packages/guidance/README.md",
            "packages/renderer/brand-kit.view-model.json",
            "packages/brand-kit/brand-kit.zip",
        ] {
            let bytes = fs::read(repository.path().join("assets/identity").join(path))
                .expect("read generated public artifact");
            assert_public_case(&bytes, case);
        }
        let repeated = compiler
            .prepare(request)
            .expect("replan public projections");
        assert!(
            !repeated.plan.has_mutations(),
            "public filtering must remain deterministic"
        );
        assert_eq!(
            guidance_documents(repository.path()),
            source,
            "canonical source is unchanged"
        );
        assert_eq!(
            model.guidance.for_audience(GuidanceAudience::Review),
            review
        );
    }
}

fn assert_public_case(bytes: &[u8], case: &Value) {
    for phrase in case["withheld"].as_array().expect("withheld phrases") {
        let phrase = phrase.as_str().expect("withheld text");
        assert!(
            !bytes
                .windows(phrase.len())
                .any(|part| part == phrase.as_bytes()),
            "{} leaked {phrase:?}",
            case["id"]
        );
    }
    for phrase in case["retained"].as_array().expect("retained phrases") {
        let phrase = phrase.as_str().expect("retained text");
        assert!(
            bytes
                .windows(phrase.len())
                .any(|part| part == phrase.as_bytes()),
            "{} lost approved public text {phrase:?}",
            case["id"]
        );
    }
}

fn assert_python_public_conformance(root: &Path, public: &identity::brandkit::BrandKitGuidance) {
    let output = Command::new(if cfg!(windows) { "python" } else { "python3" })
        .arg(PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("scripts/render_guidance.py"))
        .arg("--repository-root")
        .arg(root)
        .args(["--audience", "public", "--format", "json"])
        .output()
        .expect("run the standalone Python guidance projection");
    assert!(
        output.status.success(),
        "shared case must pass full source validation: {}",
        String::from_utf8_lossy(&output.stderr)
    );
    let python: Value = serde_json::from_slice(&output.stdout).expect("parse public Python model");
    let voice = public.voice.as_ref().expect("declared voice");
    let usage = public.usage.as_ref().expect("declared usage");
    for field in ["foundation", "characteristics", "contexts", "localization"] {
        assert_eq!(
            voice.get(field).unwrap_or(&Value::Null),
            &python[field],
            "Rust/Python voice field {field}"
        );
    }
    for field in ["sections", "accessibility", "legal"] {
        assert_eq!(
            usage.get(field).unwrap_or(&Value::Null),
            &python[field],
            "Rust/Python usage field {field}"
        );
    }
    let assets = python["downloads"]
        .as_array()
        .expect("public downloads")
        .iter()
        .chain(
            python["legacyAssets"]
                .as_array()
                .expect("public legacy records"),
        )
        .cloned()
        .collect::<Vec<_>>();
    assert_eq!(usage["assets"], serde_json::json!(assets));
}
