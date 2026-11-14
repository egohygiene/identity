// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

//! A copied binary must prepare candidates using release-embedded trusted code.

use std::collections::BTreeMap;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, Output};

use serde_json::{Value, json};
use sha2::{Digest, Sha256};
use tempfile::TempDir;

fn inventory(root: &Path) -> BTreeMap<PathBuf, Vec<u8>> {
    fn walk(root: &Path, directory: &Path, result: &mut BTreeMap<PathBuf, Vec<u8>>) {
        for entry in fs::read_dir(directory).unwrap() {
            let path = entry.unwrap().path();
            if path.is_dir() {
                walk(root, &path, result);
            } else {
                result.insert(
                    path.strip_prefix(root).unwrap().to_path_buf(),
                    fs::read(path).unwrap(),
                );
            }
        }
    }
    let mut result = BTreeMap::new();
    walk(root, root, &mut result);
    result
}

fn invoke(binary: &Path, root: &Path, output: &str, missing_python: bool) -> Output {
    let mut command = Command::new(binary);
    command
        .current_dir(root)
        .env("PYTHONPATH", root)
        .args(["v1-init", "--repository-root"])
        .arg(root)
        .args(["--request", "request.json", "--output-directory", output]);
    if missing_python {
        command.env("IDENTITY_PYTHON", root.join("missing-python"));
    }
    command.output().unwrap()
}

fn report(root: &Path, output: &str) -> Value {
    serde_json::from_slice(&fs::read(root.join(output).join("initialization-report.json")).unwrap())
        .unwrap()
}

#[test]
fn copied_binary_preserves_v0_and_imports_v1_without_consumer_python_or_installation() {
    let tools = TempDir::new().unwrap();
    let binary = tools.path().join(if cfg!(windows) {
        "identity.exe"
    } else {
        "identity"
    });
    fs::copy(env!("CARGO_BIN_EXE_identity"), &binary).unwrap();
    let consumer = TempDir::new().unwrap();
    let root = consumer.path();
    for name in ["json.py", "sitecustomize.py"] {
        fs::write(
            root.join(name),
            b"raise RuntimeError('consumer Python must never execute')\n",
        )
        .unwrap();
    }
    fs::write(root.join("notes.txt"), b"unrelated source").unwrap();
    fs::write(
        root.join("request.json"),
        json!({"schema": "identity.initialization-request/v1"}).to_string(),
    )
    .unwrap();
    let before = inventory(root);
    assert!(invoke(&binary, root, "starter", false).status.success());
    assert!(
        before
            .iter()
            .all(|(path, bytes)| fs::read(root.join(path)).unwrap() == *bytes)
    );
    let starter = report(root, "starter");
    assert_eq!(starter["status"], "incomplete");
    assert_eq!(starter["sourceValid"], false);
    assert_eq!(
        starter["implementation"]["initializerSha256"],
        format!(
            "{:x}",
            Sha256::digest(include_bytes!("../scripts/initialize_identity.py"))
        )
    );
    assert_eq!(
        starter["implementation"]["validatorSha256"],
        format!(
            "{:x}",
            Sha256::digest(include_bytes!("../scripts/validate_identity.py"))
        )
    );
    let before_failure = inventory(root);
    assert!(!invoke(&binary, root, "starter", false).status.success());
    assert!(
        !invoke(&binary, root, "missing-runtime", true)
            .status
            .success()
    );
    assert_eq!(inventory(root), before_failure);
    assert!(!root.join(".identity").exists());
    assert!(!root.join("assets").exists());

    assert_v0_preserved(&binary, root);
    assert_v1_import(&binary);
}

fn assert_v0_preserved(binary: &Path, root: &Path) {
    assert!(
        Command::new(binary)
            .args(["init", "--repository-root"])
            .arg(root)
            .args(["--project-id", "v0-example", "--display-name", "V0 Example"])
            .output()
            .unwrap()
            .status
            .success()
    );
    let legacy = inventory(&root.join(".identity"));
    assert!(invoke(binary, root, "v0-candidate", false).status.success());
    assert_eq!(inventory(&root.join(".identity")), legacy);
    assert!(
        Command::new(binary)
            .args(["validate", "--repository-root"])
            .arg(root)
            .output()
            .unwrap()
            .status
            .success()
    );
}

fn assert_v1_import(binary: &Path) {
    let native = TempDir::new().unwrap();
    let fixture =
        Path::new(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/v1/valid/minimal/.identity");
    for (relative, bytes) in inventory(&fixture) {
        let destination = native.path().join(".identity").join(relative);
        fs::create_dir_all(destination.parent().unwrap()).unwrap();
        fs::write(destination, bytes).unwrap();
    }
    fs::write(
        native.path().join("request.json"),
        json!({"schema": "identity.initialization-request/v1", "sourceRoot": "."}).to_string(),
    )
    .unwrap();
    let canonical = inventory(&native.path().join(".identity"));
    assert!(
        invoke(binary, native.path(), "review", false)
            .status
            .success()
    );
    assert_eq!(
        report(native.path(), "review")["status"],
        "ready-for-review"
    );
    assert_eq!(
        inventory(&native.path().join("review/.identity")),
        canonical
    );
    assert_eq!(inventory(&native.path().join(".identity")), canonical);
    assert!(!native.path().join("assets").exists());
}
