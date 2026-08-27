// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, Output};

use serde_json::{Value, json};
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

const STUDIO_SOURCE_DIGEST: &str =
    "545e54ad462fa84807ef594110a6742bf861bdf90a7e71fd60e1729b05d58516";

fn approved_studio_handoff(source_digest: &str) -> Value {
    json!({
        "schema": "identity.studio-plan/v1",
        "projectId": "example-project",
        "sourceDigest": source_digest,
        "profiles": ["pwa", "social"],
        "status": "approved-for-compiler-handoff",
        "decisions": [
            {
                "id": "candidate-mark",
                "kind": "mark",
                "state": "candidate",
                "action": "stage-for-compiler-review"
            },
            {
                "id": "rejected-mark",
                "kind": "mark",
                "state": "rejected",
                "action": "preserve-review-history"
            }
        ],
        "writes": [{
            "id": "candidate-mark",
            "kind": "mark",
            "action": "stage-for-compiler-review"
        }],
        "warnings": [],
        "approval": {
            "reviewer": "local reviewer",
            "method": "explicit-local-studio"
        }
    })
}

fn studio_release_view_model(source_digest: &str) -> Value {
    json!({
        "schema": "identity.brand-kit-view-model/v1",
        "projectId": "example-project",
        "release": { "sourceDigest": source_digest }
    })
}

fn write_json(path: impl AsRef<Path>, value: &Value) {
    fs::write(
        path,
        serde_json::to_vec_pretty(value).expect("test JSON must serialize"),
    )
    .expect("test JSON must be written");
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
        manifest["profiles"].as_object().map(serde_json::Map::len),
        Some(8)
    );
}

#[test]
fn approved_studio_handoff_resolves_the_selected_cli_plan() {
    let repository = initialized_project();
    write_json(
        repository.path().join("identity-approved-handoff.json"),
        &approved_studio_handoff(STUDIO_SOURCE_DIGEST),
    );
    write_json(
        repository.path().join("brand-kit-view-model.json"),
        &studio_release_view_model(STUDIO_SOURCE_DIGEST),
    );

    let output = run(identity_command().args([
        "studio-review",
        "--repository-root",
        repository
            .path()
            .to_str()
            .expect("temporary path must be UTF-8"),
        "--handoff",
        "identity-approved-handoff.json",
        "--release-view-model",
        "brand-kit-view-model.json",
    ]));
    let review: Value = serde_json::from_slice(&output.stdout).expect("review must be valid JSON");
    let profiles = review["plan"]["profiles"]
        .as_array()
        .expect("review plan profiles must be an array");
    let target_profiles = review["plan"]["targets"]
        .as_array()
        .expect("review plan targets must be an array")
        .iter()
        .map(|target| {
            target["profile"]
                .as_str()
                .expect("profile must be a string")
        })
        .collect::<Vec<_>>();

    assert_eq!(review["schema"], "identity.studio-review-plan/v1");
    assert_eq!(review["sourceDigest"], STUDIO_SOURCE_DIGEST);
    assert_eq!(review["approval"]["reviewer"], "local reviewer");
    assert_eq!(profiles.len(), 2);
    assert!(
        target_profiles
            .iter()
            .all(|profile| matches!(*profile, "pwa" | "social"))
    );
}

#[test]
fn studio_review_rejects_historical_assets_as_staged_writes() {
    let repository = initialized_project();
    let mut handoff = approved_studio_handoff(STUDIO_SOURCE_DIGEST);
    handoff["writes"] = json!([{
        "id": "rejected-mark",
        "kind": "mark",
        "action": "stage-for-compiler-review"
    }]);
    write_json(
        repository.path().join("identity-approved-handoff.json"),
        &handoff,
    );
    write_json(
        repository.path().join("brand-kit-view-model.json"),
        &studio_release_view_model(STUDIO_SOURCE_DIGEST),
    );

    let output = identity_command()
        .args([
            "studio-review",
            "--repository-root",
            repository
                .path()
                .to_str()
                .expect("temporary path must be UTF-8"),
            "--handoff",
            "identity-approved-handoff.json",
            "--release-view-model",
            "brand-kit-view-model.json",
        ])
        .output()
        .expect("identity command must start");

    assert!(!output.status.success());
    assert!(String::from_utf8_lossy(&output.stderr).contains("only current candidate assets"));
}

#[test]
fn studio_review_rejects_a_handoff_from_a_different_immutable_release() {
    let repository = initialized_project();
    write_json(
        repository.path().join("identity-approved-handoff.json"),
        &approved_studio_handoff(STUDIO_SOURCE_DIGEST),
    );
    write_json(
        repository.path().join("brand-kit-view-model.json"),
        &studio_release_view_model(&"a".repeat(64)),
    );

    let output = identity_command()
        .args([
            "studio-review",
            "--repository-root",
            repository
                .path()
                .to_str()
                .expect("temporary path must be UTF-8"),
            "--handoff",
            "identity-approved-handoff.json",
            "--release-view-model",
            "brand-kit-view-model.json",
        ])
        .output()
        .expect("identity command must start");

    assert!(!output.status.success());
    assert!(
        String::from_utf8_lossy(&output.stderr).contains("does not match the immutable release")
    );
}

#[test]
fn studio_review_refuses_to_write_canonical_or_generated_identity_paths() {
    let repository = initialized_project();
    let canonical_specification = read(repository.path().join(".identity/identity.toml"));
    write_json(
        repository.path().join("identity-approved-handoff.json"),
        &approved_studio_handoff(STUDIO_SOURCE_DIGEST),
    );
    write_json(
        repository.path().join("brand-kit-view-model.json"),
        &studio_release_view_model(STUDIO_SOURCE_DIGEST),
    );

    for (output_path, expected_error) in [
        (".identity/identity.toml", "canonical .identity source"),
        (
            "assets/identity/studio-review.json",
            "generated identity assets",
        ),
    ] {
        let output = identity_command()
            .args([
                "studio-review",
                "--repository-root",
                repository
                    .path()
                    .to_str()
                    .expect("temporary path must be UTF-8"),
                "--handoff",
                "identity-approved-handoff.json",
                "--release-view-model",
                "brand-kit-view-model.json",
                "--output",
                output_path,
            ])
            .output()
            .expect("identity command must start");

        assert!(!output.status.success());
        assert!(String::from_utf8_lossy(&output.stderr).contains(expected_error));
    }
    assert_eq!(
        read(repository.path().join(".identity/identity.toml")),
        canonical_specification
    );
}
