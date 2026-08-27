// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

//! End-to-end evidence for the reusable v1 consumer bridge.

use std::collections::BTreeSet;
use std::fs;
use std::path::PathBuf;

use identity::brandkit::{compiler_request, register_builtin_adapters};
use identity::compiler::{AdapterRegistry, Compiler, LocalArtifactStore};
use identity::reference_renderer::{register_reference_renderer_adapter, with_reference_renderer};
use identity::v1_consumer::V1ConsumerPipeline;
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
