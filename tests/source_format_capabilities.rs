// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

//! Source validity and producer format support are separate boundaries.

use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;

use identity::compiler::FailureKind;
use identity::v1_consumer::V1ConsumerPipeline;
use serde_json::Value;
use sha2::{Digest, Sha256};
use tempfile::TempDir;

fn fixture_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/v1/valid/minimal")
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

fn read_json(path: &Path) -> Value {
    serde_json::from_slice(&fs::read(path).expect("read source JSON")).expect("parse source JSON")
}

fn write_json(path: &Path, value: &Value) {
    fs::write(
        path,
        serde_json::to_vec_pretty(value).expect("serialize source JSON"),
    )
    .expect("write source JSON");
}

fn add_governed_asset(root: &Path, filename: &str, kind: &str, bytes: &[u8]) -> String {
    let source_path = format!(".identity/sources/{filename}");
    fs::write(root.join(&source_path), bytes).expect("write governed source bytes");

    let provenance_path = root.join(".identity/governance/provenance.json");
    let mut provenance = read_json(&provenance_path);
    let mut asset = provenance["assets"][0].clone();
    asset["id"] = "format-capability-probe".into();
    asset["path"] = source_path.clone().into();
    asset["kind"] = kind.into();
    asset["sha256"] = format!("{:x}", Sha256::digest(bytes)).into();
    asset["approval"] = "approve-format-capability-probe".into();
    provenance["assets"].as_array_mut().unwrap().push(asset);
    write_json(&provenance_path, &provenance);

    let approvals_path = root.join(".identity/governance/approvals.json");
    let mut approvals = read_json(&approvals_path);
    let mut decision = approvals["decisions"][0].clone();
    decision["id"] = "approve-format-capability-probe".into();
    decision["subject"] = "format-capability-probe".into();
    decision["candidate"] = source_path.clone().into();
    decision["notes"] = "Synthetic source-format capability test evidence.".into();
    approvals["decisions"]
        .as_array_mut()
        .unwrap()
        .push(decision);
    write_json(&approvals_path, &approvals);
    source_path
}

fn assert_valid_source(root: &Path) {
    let python = std::env::var_os("IDENTITY_PYTHON")
        .unwrap_or_else(|| if cfg!(windows) { "python" } else { "python3" }.into());
    let output = Command::new(python)
        .arg(Path::new(env!("CARGO_MANIFEST_DIR")).join("scripts/validate_identity.py"))
        .arg("--repository-root")
        .arg(root)
        .args(["--format", "json"])
        .output()
        .expect("run authoritative source validator");
    assert!(
        output.status.success(),
        "{}\n{}",
        String::from_utf8_lossy(&output.stdout),
        String::from_utf8_lossy(&output.stderr)
    );
    let report: Value = serde_json::from_slice(&output.stdout).expect("parse source diagnostics");
    assert_eq!(report["valid"], true);
}

#[test]
fn governed_binary_sources_are_valid_but_unsupported_by_the_package_producer() {
    let png = resvg::tiny_skia::Pixmap::new(1, 1)
        .expect("allocate PNG fixture")
        .encode_png()
        .expect("encode PNG fixture");
    for (filename, kind, bytes) in [
        ("capability.png", "imagery", png.as_slice()),
        ("capability.woff2", "font", b"wOF2\0\xff\x80\0".as_slice()),
    ] {
        let root = TempDir::new().expect("create temporary consumer");
        copy_tree(&fixture_root(), root.path());
        let source_path = add_governed_asset(root.path(), filename, kind, bytes);
        let targets_path = root.path().join(".identity/targets/profiles.json");
        let mut targets = read_json(&targets_path);
        targets["enabled"] = serde_json::json!([{"id": "tokens", "version": "1.0.0"}]);
        write_json(&targets_path, &targets);
        assert_valid_source(root.path());

        let error = V1ConsumerPipeline::load(root.path()).expect_err("reject unsupported format");
        assert_eq!(error.kind, FailureKind::Unsupported);
        assert_eq!(error.diagnostics.len(), 1);
        let diagnostic = &error.diagnostics[0];
        assert_eq!(diagnostic.code, "IDN3304");
        assert_eq!(diagnostic.failure, FailureKind::Unsupported);
        assert_eq!(diagnostic.path.as_deref(), Some(source_path.as_str()));
        assert!(diagnostic.message.contains(".svg"));
        assert!(diagnostic.recovery.contains("every provenance asset"));
        assert!(diagnostic.recovery.contains("reviewed UTF-8 .svg master"));
        for operation in ["v1-generate", "v1-verify"] {
            let output = Command::new(env!("CARGO_BIN_EXE_identity"))
                .arg(operation)
                .arg("--repository-root")
                .arg(root.path())
                .output()
                .expect("run unsupported source through published CLI");
            assert!(!output.status.success());
            let stderr = String::from_utf8_lossy(&output.stderr);
            for expected in [
                "IDN3304",
                source_path.as_str(),
                "reviewed UTF-8 .svg master",
                "separate producer that supports this format",
            ] {
                assert!(stderr.contains(expected), "{operation}: {stderr}");
            }
        }
        assert_eq!(fs::read(root.path().join(source_path)).unwrap(), bytes);
        assert!(!root.path().join("assets").exists());
    }
}

#[test]
fn unsupported_extension_is_reported_even_when_its_bytes_are_utf8() {
    let root = TempDir::new().expect("create temporary consumer");
    copy_tree(&fixture_root(), root.path());
    let source_path = add_governed_asset(
        root.path(),
        "capability.txt",
        "imagery",
        b"Governed text does not become SVG merely by being UTF-8.",
    );
    assert_valid_source(root.path());
    let error = V1ConsumerPipeline::load(root.path()).expect_err("reject unsupported extension");
    assert_eq!(error.kind, FailureKind::Unsupported);
    assert_eq!(error.diagnostics[0].code, "IDN3304");
    assert_eq!(
        error.diagnostics[0].path.as_deref(),
        Some(source_path.as_str())
    );
}

#[test]
fn non_utf8_svg_remains_an_invalid_source_for_the_package_producer() {
    let root = TempDir::new().expect("create temporary consumer");
    copy_tree(&fixture_root(), root.path());
    let source_path = add_governed_asset(root.path(), "capability.svg", "imagery", b"\xff\x80");
    assert_valid_source(root.path());
    let error = V1ConsumerPipeline::load(root.path()).expect_err("reject non-UTF-8 SVG");
    assert_eq!(error.kind, FailureKind::Invalid);
    assert_eq!(error.diagnostics[0].code, "IDN3301");
    assert_eq!(
        error.diagnostics[0].path.as_deref(),
        Some(source_path.as_str())
    );
    assert!(error.diagnostics[0].message.contains("UTF-8"));
}
