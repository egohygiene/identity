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
        pipeline
            .compiler_request("assets/identity")
            .expect("build selected request"),
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

    let renderer: Value = serde_json::from_slice(
        &fs::read(
            temporary
                .path()
                .join("assets/identity/packages/renderer/brand-kit.view-model.json"),
        )
        .expect("read renderer model"),
    )
    .expect("parse renderer model");
    let provenance: Value = serde_json::from_slice(
        &fs::read(fixture_root().join(".identity/governance/provenance.json"))
            .expect("read source provenance"),
    )
    .expect("parse source provenance");
    let public_assets = renderer["assets"].as_array().expect("renderer assets");
    assert_eq!(public_assets.len(), 1);
    assert_eq!(public_assets[0]["id"], "mark");
    assert_eq!(public_assets[0]["usage"], provenance["assets"][0]["usage"]);
    assert_eq!(public_assets[0]["kind"], "mark");
    assert_eq!(public_assets[0]["notes"], public_assets[0]["intendedUse"]);
    assert_eq!(renderer["downloads"].as_array().unwrap().len(), 1);
    assert!(
        renderer["packages"]
            .as_array()
            .unwrap()
            .iter()
            .all(|package| package["id"] != "brand-kit-archive")
    );
    let serialized = serde_json::to_string(&renderer).unwrap();
    assert!(!serialized.contains("legacy-wordmark"));
    assert!(!serialized.contains("The retired Example Product"));
    assert!(!serialized.contains("mascot-kern"));
    let intent = identity::compiler::IdentityReader::read(&pipeline).unwrap();
    let local = BrandKitModel::from_resolved(&pipeline.resolve(&intent).unwrap()).unwrap();
    assert_eq!(
        local.sources.len(),
        3,
        "review/local sources remain complete"
    );
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

fn generate_request(
    root: &Path,
    pipeline: &V1ConsumerPipeline,
    request: identity::compiler::CompilerRequest,
) -> Value {
    let mut registry = AdapterRegistry::new();
    register_builtin_adapters(&mut registry).unwrap();
    register_reference_renderer_adapter(&mut registry).unwrap();
    let mut store = LocalArtifactStore::new(root).unwrap();
    let mut compiler = Compiler::new(pipeline, pipeline, pipeline, &registry, &mut store);
    let prepared = compiler.prepare(with_reference_renderer(request)).unwrap();
    compiler.execute(&prepared, &BTreeSet::new()).unwrap();
    serde_json::from_slice(
        &fs::read(root.join("assets/identity/packages/renderer/brand-kit.view-model.json"))
            .unwrap(),
    )
    .unwrap()
}

#[test]
fn github_profile_generates_an_uploadable_source_bound_preview_without_other_platforms() {
    let repository = TempDir::new().unwrap();
    copy_tree(&fixture_root(), repository.path());
    let pipeline = V1ConsumerPipeline::load(repository.path()).unwrap();
    let profiles = ["github", "metadata"].map(|id| ProfileSelection {
        id: id.to_owned(),
        version: "1.0.0".to_owned(),
    });
    let request = compiler_request("assets/identity", &profiles).unwrap();
    let renderer = generate_request(repository.path(), &pipeline, request.clone());
    let preview = repository
        .path()
        .join("assets/identity/github/social-preview.png");
    let bytes = fs::read(&preview).unwrap();
    assert!(bytes.starts_with(b"\x89PNG\r\n\x1a\n"));
    assert_eq!(u32::from_be_bytes(bytes[16..20].try_into().unwrap()), 1280);
    assert_eq!(u32::from_be_bytes(bytes[20..24].try_into().unwrap()), 640);
    assert!(bytes.len() < 1_000_000, "GitHub upload must be under 1 MB");
    let downloads = renderer["downloads"].as_array().unwrap();
    assert_eq!(downloads.len(), 1);
    assert_eq!(downloads[0]["id"], "github-social-preview");
    assert_eq!(
        downloads[0]["sourceSha256"],
        renderer["assets"][0]["sha256"]
    );
    let metadata: Value = serde_json::from_slice(
        &fs::read(
            repository
                .path()
                .join("assets/identity/packages/metadata/metadata.json"),
        )
        .unwrap(),
    )
    .unwrap();
    assert_eq!(
        metadata["social"],
        serde_json::json!({"githubPreview": "github/social-preview.png"})
    );
    assert!(!repository.path().join("assets/identity/social").exists());
    let second = generate_request(repository.path(), &pipeline, request);
    assert_eq!(second, renderer);
    assert_eq!(fs::read(preview).unwrap(), bytes);
}

#[test]
fn selected_outputs_bind_public_downloads_and_standalone_metadata() {
    let repository = TempDir::new().unwrap();
    copy_tree(&fixture_root(), repository.path());
    let pipeline = V1ConsumerPipeline::load(repository.path()).unwrap();
    let profiles = ["core", "web", "pwa", "social", "metadata"].map(|id| ProfileSelection {
        id: id.to_owned(),
        version: "1.0.0".to_owned(),
    });
    let request = compiler_request("assets/identity", &profiles).unwrap();
    let renderer = generate_request(repository.path(), &pipeline, request.clone());
    let source_digest = renderer["assets"][0]["sha256"].as_str().unwrap();
    let downloads = renderer["downloads"].as_array().unwrap();
    assert_eq!(downloads.len(), 8);
    for download in downloads {
        assert_eq!(download["sourceAssetId"], "mark");
        assert_eq!(download["sourceSha256"], source_digest);
        assert!(
            download.get("sha256").is_none(),
            "source hash does not claim output integrity"
        );
        let bytes = fs::read(
            repository
                .path()
                .join("assets/identity")
                .join(download["path"].as_str().unwrap()),
        )
        .unwrap();
        if download["mediaType"] == "image/png" {
            let width = u32::from_be_bytes(bytes[16..20].try_into().unwrap());
            let height = u32::from_be_bytes(bytes[20..24].try_into().unwrap());
            assert_eq!(download["dimensions"], format!("{width} × {height} pixels"));
        }
    }
    let metadata: Value = serde_json::from_slice(
        &fs::read(
            repository
                .path()
                .join("assets/identity/packages/metadata/metadata.json"),
        )
        .unwrap(),
    )
    .unwrap();
    assert_eq!(
        metadata["social"]["defaultCard"],
        "social/card-1200x630.png"
    );
    assert!(metadata["social"].get("githubPreview").is_none());
    let icons: Value = serde_json::from_slice(
        &fs::read(
            repository
                .path()
                .join("assets/identity/pwa/manifest-icons.json"),
        )
        .unwrap(),
    )
    .unwrap();
    assert_eq!(icons["icons"].as_array().unwrap().len(), 3);

    // Reusing a selected request after removing rasters must refresh its bindings.
    let metadata_only = TempDir::new().unwrap();
    let mut request = request;
    request.targets.retain(|target| {
        target.adapter_id == "identity-metadata" || target.adapter_id == "identity-guidance"
    });
    let renderer = generate_request(metadata_only.path(), &pipeline, request);
    assert!(renderer.get("downloads").is_none());
    assert_eq!(renderer["assets"][0]["availability"], "embedded-source");
    assert!(renderer["assets"][0]["downloadPath"].is_null());
    assert!(
        renderer["packages"]
            .as_array()
            .unwrap()
            .iter()
            .all(|package| package["id"] != "brand-kit-archive")
    );
    let metadata: Value = serde_json::from_slice(
        &fs::read(
            metadata_only
                .path()
                .join("assets/identity/packages/metadata/metadata.json"),
        )
        .unwrap(),
    )
    .unwrap();
    assert_eq!(metadata["social"], serde_json::json!({}));
    let icons: Value = serde_json::from_slice(
        &fs::read(
            metadata_only
                .path()
                .join("assets/identity/pwa/manifest-icons.json"),
        )
        .unwrap(),
    )
    .unwrap();
    assert_eq!(icons["icons"], serde_json::json!([]));
    let open_graph = fs::read_to_string(
        metadata_only
            .path()
            .join("assets/identity/packages/metadata/open-graph.html"),
    )
    .unwrap();
    assert!(!open_graph.contains("og:image"));
}

fn approve_distinct_master(root: &Path, download_name: &str) {
    let path = root.join(".identity/guidance/usage.json");
    let mut usage: Value = serde_json::from_slice(&fs::read(&path).unwrap()).unwrap();
    let asset = &mut usage["assets"][1];
    asset["status"] = serde_json::json!("active");
    asset["availability"] = serde_json::json!("public");
    asset["replacement"] = Value::Null;
    asset["downloadName"] = serde_json::json!(download_name);
    asset["label"] = serde_json::json!("Light background wordmark");
    asset["notes"] = serde_json::json!("Approved on light backgrounds.");
    asset["governance"]["subject"] = serde_json::json!("legacy-wordmark");
    asset["governance"]["state"] = serde_json::json!("approved");
    asset["governance"]["visibility"] = serde_json::json!("public");
    asset["governance"]["approval"] = serde_json::json!("approve-legacy-wordmark-source");
    fs::write(path, serde_json::to_vec_pretty(&usage).unwrap()).unwrap();
}

#[test]
fn core_copies_distinct_approved_masters_and_preserves_canonical_source() {
    use identity::compiler::IdentityReader;
    let repository = TempDir::new().unwrap();
    copy_tree(&fixture_root(), repository.path());
    approve_distinct_master(repository.path(), "example-wordmark-light.svg");
    let pipeline = V1ConsumerPipeline::load(repository.path()).unwrap();
    let before = pipeline.read().unwrap();
    let renderer = generate_request(
        repository.path(),
        &pipeline,
        pipeline.compiler_request("assets/identity").unwrap(),
    );
    let master = renderer["assets"]
        .as_array()
        .unwrap()
        .iter()
        .find(|asset| asset["id"] == "legacy-wordmark")
        .unwrap();
    assert_eq!(master["label"], "Light background wordmark");
    assert_eq!(master["kind"], "wordmark");
    assert_eq!(master["notes"], "Approved on light backgrounds.");
    assert_eq!(master["downloadPath"], "brand/example-wordmark-light.svg");
    assert_eq!(
        fs::read(
            repository
                .path()
                .join("assets/identity/brand/example-wordmark-light.svg")
        )
        .unwrap(),
        fs::read(
            repository
                .path()
                .join(".identity/sources/legacy-wordmark.svg")
        )
        .unwrap()
    );
    assert_eq!(renderer["downloads"].as_array().unwrap().len(), 2);
    assert_eq!(pipeline.read().unwrap(), before);
    let direct = compiler_request(
        "assets/identity",
        &[ProfileSelection {
            id: "metadata".to_owned(),
            version: "1.0.0".to_owned(),
        }],
    )
    .unwrap();
    assert!(
        !direct
            .targets
            .iter()
            .any(|target| target.adapter_id == "identity-source-svg")
    );
}

#[test]
fn unsafe_or_colliding_public_master_paths_fail_before_output_writes() {
    for download_name in [
        "../outside.svg",
        "logo#draft.svg",
        "logo?draft.svg",
        "logo%20draft.svg",
        "logo%.svg",
        "nested/logo.svg",
        "mark.svg",
    ] {
        let repository = TempDir::new().unwrap();
        copy_tree(&fixture_root(), repository.path());
        approve_distinct_master(repository.path(), download_name);
        let pipeline = V1ConsumerPipeline::load(repository.path()).unwrap();
        let request = pipeline.compiler_request("assets/identity");
        if download_name == "mark.svg" {
            let mut registry = AdapterRegistry::new();
            register_builtin_adapters(&mut registry).unwrap();
            register_reference_renderer_adapter(&mut registry).unwrap();
            let mut store = LocalArtifactStore::new(repository.path()).unwrap();
            let mut compiler =
                Compiler::new(&pipeline, &pipeline, &pipeline, &registry, &mut store);
            assert!(
                compiler
                    .prepare(with_reference_renderer(request.unwrap()))
                    .is_err()
            );
        } else {
            assert!(request.is_err());
        }
        assert!(!repository.path().join("assets").exists());
        assert!(!repository.path().join("outside.svg").exists());
    }
}

#[test]
fn historical_digest_survives_legacy_toml_coexistence_in_rust_and_python_projections() {
    use identity::compiler::IdentityReader;

    let root = TempDir::new().unwrap();
    copy_tree(&fixture_root(), root.path());
    for legacy in [false, true] {
        if legacy {
            fs::write(
                root.path().join(".identity/identity.toml"),
                b"legacy source\n",
            )
            .unwrap();
        }
        let pipeline = V1ConsumerPipeline::load(root.path()).expect("preflight valid consumer");
        let digest = pipeline.read().unwrap().source_digest;
        assert_eq!(
            digest,
            "1002ff75ea51f6e016929894ea30cc96565bdbbca749a0e7fff1ebd0d2f21353"
        );
        let python = std::env::var_os("IDENTITY_PYTHON")
            .unwrap_or_else(|| if cfg!(windows) { "python" } else { "python3" }.into());
        let output = Command::new(python)
            .arg(Path::new(env!("CARGO_MANIFEST_DIR")).join("scripts/render_design_system.py"))
            .arg("--repository-root")
            .arg(root.path())
            .args(["--format", "context-json"])
            .output()
            .expect("run Python projection");
        assert!(
            output.status.success(),
            "{}",
            String::from_utf8_lossy(&output.stderr)
        );
        let context: Value = serde_json::from_slice(&output.stdout).unwrap();
        assert_eq!(context["source"]["digest"], digest);
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
fn nullable_guidance_drives_packages_and_renderer_without_reading_absent_documents() {
    use identity::compiler::IdentityReader;

    for declared_voice in [false, true] {
        for declared_usage in [false, true] {
            let repository = TempDir::new().expect("create temporary consumer");
            copy_tree(&fixture_root(), repository.path());
            for (field, declared) in [("voice", declared_voice), ("usage", declared_usage)] {
                if !declared {
                    fs::remove_file(
                        repository
                            .path()
                            .join(format!(".identity/guidance/{field}.json")),
                    )
                    .unwrap();
                    change_json(
                        repository.path(),
                        ".identity/identity.json",
                        &format!("/documents/guidance/{field}"),
                        Value::Null,
                    );
                }
            }
            let pipeline =
                V1ConsumerPipeline::load(repository.path()).expect("load optional guidance");
            let intent = pipeline.read().unwrap();
            let resolved = pipeline.resolve(&intent).unwrap();
            let model = BrandKitModel::from_resolved(&resolved).unwrap();
            assert_eq!(model.guidance.voice.is_some(), declared_voice);
            assert_eq!(model.guidance.usage.is_some(), declared_usage);
            let profiles = ["metadata", "archive"].map(|id| ProfileSelection {
                id: id.to_owned(),
                version: "1.0.0".to_owned(),
            });
            let request =
                with_reference_renderer(compiler_request("assets/identity", &profiles).unwrap());
            let mut registry = AdapterRegistry::new();
            register_builtin_adapters(&mut registry).unwrap();
            register_reference_renderer_adapter(&mut registry).unwrap();
            let mut store = LocalArtifactStore::new(repository.path()).unwrap();
            let mut compiler =
                Compiler::new(&pipeline, &pipeline, &pipeline, &registry, &mut store);
            let prepared = compiler.prepare(request.clone()).unwrap();
            compiler.execute(&prepared, &BTreeSet::new()).unwrap();
            for relative in [
                "packages/guidance/voice-and-usage.json",
                "packages/renderer/brand-kit.view-model.json",
            ] {
                let output: Value = serde_json::from_slice(
                    &fs::read(repository.path().join("assets/identity").join(relative)).unwrap(),
                )
                .unwrap();
                for (field, declared) in [("voice", declared_voice), ("usage", declared_usage)] {
                    let expected = if declared { "declared" } else { "not-declared" };
                    if relative.contains("view-model") {
                        assert_eq!(output["guidance"][field]["status"], expected);
                        assert_eq!(output["guidance"][field]["value"].is_null(), !declared);
                        if !declared_usage {
                            assert_eq!(output["assets"], serde_json::json!([]));
                            assert!(output.get("downloads").is_none());
                            assert!(
                                output["packages"]
                                    .as_array()
                                    .unwrap()
                                    .iter()
                                    .all(|package| package["id"] != "brand-kit-archive")
                            );
                        }
                    } else {
                        assert_eq!(output["status"][field], expected);
                        assert_eq!(output[field].is_null(), !declared);
                    }
                }
            }
            assert!(!compiler.prepare(request).unwrap().plan.has_mutations());
            assert_eq!(
                pipeline.read().unwrap(),
                intent,
                "canonical source stays unchanged"
            );
        }
    }
}

#[test]
fn authoring_examples_generate_and_verify_through_the_published_cli() {
    for name in ["minimal", "expanded"] {
        let repository = TempDir::new().expect("create temporary authoring consumer");
        let example = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("examples/v1")
            .join(name);
        copy_tree(&example, repository.path());
        let pipeline =
            V1ConsumerPipeline::load(repository.path()).expect("load exact authoring example");
        let original = identity::compiler::IdentityReader::read(&pipeline).unwrap();
        for operation in ["v1-generate", "v1-verify"] {
            let output = Command::new(env!("CARGO_BIN_EXE_identity"))
                .arg(operation)
                .arg("--repository-root")
                .arg(repository.path())
                .output()
                .expect("run published CLI against authoring example");
            assert!(
                output.status.success(),
                "{name} {operation}: {}",
                String::from_utf8_lossy(&output.stderr)
            );
        }
        assert_eq!(
            identity::compiler::IdentityReader::read(&pipeline).unwrap(),
            original,
            "authoring example source stays unchanged"
        );
    }
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

fn change_json(root: &Path, relative: &str, pointer: &str, value: Value) {
    let path = root.join(relative);
    let mut document: Value = serde_json::from_slice(&fs::read(&path).unwrap()).unwrap();
    *document
        .pointer_mut(pointer)
        .expect("existing fixture field") = value;
    fs::write(path, serde_json::to_vec_pretty(&document).unwrap()).unwrap();
}

fn assert_preflight_rejected(root: &Path, code: &str) {
    let original_source = fs::read(root.join(".identity/identity.json")).unwrap();
    let error = V1ConsumerPipeline::load(root).expect_err("library must enforce preflight");
    assert!(
        error.diagnostics.iter().any(|value| value.code == code),
        "{error:?}"
    );
    for operation in ["v1-generate", "v1-verify"] {
        let output = Command::new(env!("CARGO_BIN_EXE_identity"))
            .arg(operation)
            .arg("--repository-root")
            .arg(root)
            .output()
            .unwrap();
        assert!(
            !output.status.success(),
            "{operation} accepted invalid source"
        );
        assert!(
            String::from_utf8_lossy(&output.stderr).contains(code),
            "{}",
            String::from_utf8_lossy(&output.stderr)
        );
    }
    assert_eq!(
        fs::read(root.join("assets/identity/sentinel")).unwrap(),
        b"keep"
    );
    assert_eq!(
        fs::read_dir(root.join("assets/identity")).unwrap().count(),
        1
    );
    assert!(!root.join(".cache").exists());
    assert_eq!(
        fs::read(root.join(".identity/identity.json")).unwrap(),
        original_source
    );
}

#[test]
fn cli_and_library_enforce_authoritative_source_diagnostics_before_mutation() {
    for (document, pointer, value, code) in [
        (
            ".identity/identity.json",
            "/schema",
            serde_json::json!("identity.project/v99"),
            "IDN1002",
        ),
        (
            ".identity/governance/approvals.json",
            "/decisions/0/subject",
            serde_json::json!("unrelated"),
            "IDN1404",
        ),
        (
            ".identity/identity.json",
            "/layers/0/sha256",
            serde_json::json!("0".repeat(64)),
            "IDN1302",
        ),
        (
            ".identity/governance/approvals.json",
            "/decisions/1/id",
            serde_json::json!("unrelated-decision"),
            "IDN1404",
        ),
    ] {
        let root = TempDir::new().unwrap();
        copy_tree(&fixture_root(), root.path());
        fs::create_dir_all(root.path().join("assets/identity")).unwrap();
        fs::write(root.path().join("assets/identity/sentinel"), b"keep").unwrap();
        change_json(root.path(), document, pointer, value);
        assert_preflight_rejected(root.path(), code);
    }
}

#[cfg(unix)]
#[test]
fn symlinked_sources_fail_preflight_for_cli_and_library() {
    for relative in [
        ".identity/identity.json",
        ".identity/defaults/organization.tokens.json",
        ".identity/sources/mark.svg",
        ".identity",
    ] {
        let root = TempDir::new().unwrap();
        copy_tree(&fixture_root(), root.path());
        fs::create_dir_all(root.path().join("assets/identity")).unwrap();
        fs::write(root.path().join("assets/identity/sentinel"), b"keep").unwrap();
        let original = root.path().join(relative);
        let moved = root.path().join("source-backup");
        fs::rename(&original, &moved).unwrap();
        std::os::unix::fs::symlink(moved, original).unwrap();
        assert_preflight_rejected(root.path(), "IDN1003");
    }
}

#[test]
fn unreferenced_symlinks_fail_preflight_for_cli_and_library() {
    let root = TempDir::new().unwrap();
    copy_tree(&fixture_root(), root.path());
    fs::create_dir_all(root.path().join("assets/identity")).unwrap();
    fs::write(root.path().join("assets/identity/sentinel"), b"keep").unwrap();
    let link = root.path().join(".identity/unreferenced-link");
    #[cfg(unix)]
    std::os::unix::fs::symlink("absent", &link).unwrap();
    #[cfg(windows)]
    std::os::windows::fs::symlink_file("absent", &link).unwrap();
    assert_preflight_rejected(root.path(), "IDN1003");
}

#[test]
fn source_changes_after_load_or_plan_require_new_preflight() {
    use identity::compiler::{IdentityReader, IdentityValidator};
    for after_plan in [false, true] {
        let root = TempDir::new().unwrap();
        copy_tree(&fixture_root(), root.path());
        // A declared document outside .identity must also be bound to preflight.
        fs::rename(
            root.path().join(".identity/guidance/voice.json"),
            root.path().join("voice.json"),
        )
        .unwrap();
        change_json(
            root.path(),
            ".identity/identity.json",
            "/documents/guidance/voice",
            serde_json::json!("voice.json"),
        );
        let pipeline = V1ConsumerPipeline::load(root.path()).unwrap();
        let intent = pipeline.read().unwrap();
        let request = compiler_request("assets/identity", pipeline.profiles()).unwrap();
        let mut registry = AdapterRegistry::new();
        register_builtin_adapters(&mut registry).unwrap();
        let mut store = LocalArtifactStore::new(root.path()).unwrap();
        let mut compiler = Compiler::new(&pipeline, &pipeline, &pipeline, &registry, &mut store);
        let prepared = after_plan.then(|| compiler.prepare(request.clone()).unwrap());
        let path = root.path().join("voice.json");
        let mut bytes = fs::read(&path).unwrap();
        bytes.push(b' '); // Even semantically valid changes invalidate the snapshot.
        fs::write(path, bytes).unwrap();
        assert!(pipeline.read().is_err());
        assert!(pipeline.validate(&intent).is_err());
        assert!(pipeline.resolve(&intent).is_err());
        if let Some(prepared) = prepared {
            assert!(compiler.execute(&prepared, &BTreeSet::new()).is_err());
        } else {
            assert!(compiler.prepare(request).is_err());
        }
        assert!(!root.path().join("assets").exists());
        assert!(!root.path().join(".cache").exists());
    }
}

#[test]
fn standalone_binary_uses_embedded_preflight_and_ignores_consumer_python_code() {
    let root = TempDir::new().unwrap();
    copy_tree(&fixture_root(), root.path());
    let bin = root.path().join(if cfg!(windows) {
        "identity.exe"
    } else {
        "identity"
    });
    fs::copy(env!("CARGO_BIN_EXE_identity"), &bin).unwrap();
    fs::create_dir(root.path().join("scripts")).unwrap();
    for relative in [
        "json.py",
        "sitecustomize.py",
        "scripts/validate_identity.py",
    ] {
        fs::write(
            root.path().join(relative),
            b"raise RuntimeError('consumer code must never run')\n",
        )
        .unwrap();
    }
    let missing = Command::new(&bin)
        .current_dir(root.path())
        .env("IDENTITY_PYTHON", root.path().join("missing-python"))
        .arg("v1-generate")
        .output()
        .unwrap();
    assert!(!missing.status.success());
    assert!(String::from_utf8_lossy(&missing.stderr).contains("IDN3302"));
    assert!(!root.path().join("assets").exists());
    for output_root in ["assets/identity", "generated/branding"] {
        for operation in ["v1-generate", "v1-verify"] {
            let output = Command::new(&bin)
                .current_dir(root.path())
                .env("PYTHONPATH", root.path())
                .arg(operation)
                .args(["--output-root", output_root])
                .output()
                .unwrap();
            assert!(
                output.status.success(),
                "{}",
                String::from_utf8_lossy(&output.stderr)
            );
        }
    }
}
