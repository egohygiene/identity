// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, Output};

use serde_json::Value;
use tempfile::TempDir;

fn identity_command() -> Command {
    Command::new(env!("CARGO_BIN_EXE_identity"))
}

fn run(command: &mut Command) -> Output {
    let output = command.output().expect("identity command must start");
    assert!(
        output.status.success(),
        "command failed\nstdout:\n{}\nstderr:\n{}",
        String::from_utf8_lossy(&output.stdout),
        String::from_utf8_lossy(&output.stderr)
    );
    output
}

fn initialized_project() -> TempDir {
    let repository = TempDir::new().expect("temporary repository must be created");
    run(identity_command().args([
        "init",
        "--repository-root",
        repository
            .path()
            .to_str()
            .expect("temporary path must be UTF-8"),
        "--project-id",
        "example-project",
        "--display-name",
        "Example Project",
    ]));
    repository
}

fn read(path: impl AsRef<Path>) -> Vec<u8> {
    fs::read(path).expect("generated file must be readable")
}

#[test]
fn init_preserves_the_incubated_source_contract() {
    let repository = initialized_project();
    let identity_root = repository.path().join(".identity");

    assert!(identity_root.join("identity.toml").is_file());
    assert!(identity_root.join("brief.md").is_file());
    assert!(identity_root.join("sources/README.md").is_file());

    let specification = fs::read_to_string(identity_root.join("identity.toml"))
        .expect("initialized specification must be readable");
    assert!(specification.contains("schema = \"identity.project/v0\""));
    assert!(specification.contains("approval = \"human\""));
}

#[test]
fn validate_preserves_eight_profiles_and_forty_five_targets() {
    let repository = initialized_project();
    let output = run(identity_command().args([
        "validate",
        "--repository-root",
        repository
            .path()
            .to_str()
            .expect("temporary path must be UTF-8"),
    ]));
    let stdout = String::from_utf8(output.stdout).expect("stdout must be UTF-8");

    assert!(stdout.contains("Validated 8 profiles and 45 targets"));
    assert!(stdout.contains("Example Project"));
}

#[test]
fn plan_is_machine_readable_complete_and_deterministically_ordered() {
    let repository = initialized_project();
    let output = run(identity_command().args([
        "plan",
        "--repository-root",
        repository
            .path()
            .to_str()
            .expect("temporary path must be UTF-8"),
        "--format",
        "json",
    ]));
    let plan: Value = serde_json::from_slice(&output.stdout).expect("plan must be valid JSON");
    let targets = plan["targets"]
        .as_array()
        .expect("plan targets must be an array");

    assert_eq!(plan["schema"], "identity.plan/v0");
    assert_eq!(plan["profiles"].as_array().map(Vec::len), Some(8));
    assert_eq!(targets.len(), 45);

    let paths = targets
        .iter()
        .map(|target| {
            target["path"]
                .as_str()
                .expect("target path must be a string")
        })
        .collect::<Vec<_>>();
    let mut sorted = paths.clone();
    sorted.sort_unstable();
    assert_eq!(paths, sorted);
}

#[test]
fn handoff_is_complete_and_byte_stable() {
    let repository = initialized_project();
    let relative_output = PathBuf::from(".cache/identity/handoff");
    let absolute_output = repository.path().join(&relative_output);
    let arguments = [
        "handoff",
        "--repository-root",
        repository
            .path()
            .to_str()
            .expect("temporary path must be UTF-8"),
        "--output-directory",
        relative_output
            .to_str()
            .expect("handoff output path must be UTF-8"),
    ];

    run(identity_command().args(arguments));
    let first = [
        read(absolute_output.join("identity-handoff.md")),
        read(absolute_output.join("candidate-manifest.template.json")),
        read(absolute_output.join("handoff-manifest.json")),
    ];
    run(identity_command().args(arguments));
    let second = [
        read(absolute_output.join("identity-handoff.md")),
        read(absolute_output.join("candidate-manifest.template.json")),
        read(absolute_output.join("handoff-manifest.json")),
    ];

    assert_eq!(first, second);
    let manifest: Value = serde_json::from_slice(&first[2]).expect("manifest must be valid JSON");
    assert_eq!(manifest["schema"], "identity.handoff-manifest/v0");
    assert_eq!(
        manifest["profiles"].as_object().map(|value| value.len()),
        Some(8)
    );
}
