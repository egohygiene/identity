// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

//! Shipping CLI boundaries over explicit synthetic v2 recovery fixtures.
//!
//! These fixtures model retained journal states; they do not claim a naturally
//! interrupted shipping process. A separate compiler unit worker exercises an
//! actual interrupted generation using the existing test-only checkpoints.

use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::io::{BufRead, BufReader, Read, Write};
use std::path::{Path, PathBuf};
use std::process::{Child, Command, Output, Stdio};
use std::sync::mpsc;
use std::time::{Duration, Instant};

use identity::compiler::{
    COMPILER_PLAN_SCHEMA, CompilerPlan, PlanAction, PlanActionScope, PlanOperation,
};
use serde_json::{Value, json};
use sha2::{Digest, Sha256};
use tempfile::TempDir;

const OUTPUT: &str = "assets/identity";
const TRANSACTIONS: &str = ".cache/identity/transactions";
const LOCK: &str = ".cache/identity/writer.lock";
const PROCESS_TIMEOUT: Duration = Duration::from_secs(30);
const OWNER_READY: &str = "IDENTITY_RECOVERY_OWNER_READY";

fn digest(bytes: &[u8]) -> String {
    format!("{:x}", Sha256::digest(bytes))
}

fn write(path: &Path, bytes: &[u8]) {
    fs::create_dir_all(path.parent().unwrap()).unwrap();
    fs::write(path, bytes).unwrap();
}

fn copy_tree(source: &Path, destination: &Path) {
    fs::create_dir_all(destination).unwrap();
    for entry in fs::read_dir(source).unwrap() {
        let entry = entry.unwrap();
        let output = destination.join(entry.file_name());
        if entry.file_type().unwrap().is_dir() {
            copy_tree(&entry.path(), &output);
        } else {
            fs::copy(entry.path(), output).unwrap();
        }
    }
}

fn consumer() -> TempDir {
    let root = TempDir::new().unwrap();
    copy_tree(
        &PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/v1/valid/minimal"),
        root.path(),
    );
    write(
        &root.path().join("notes/unrelated.txt"),
        b"unrelated source stays unchanged",
    );
    root
}

fn snapshot(root: &Path, active_owner: bool) -> BTreeMap<PathBuf, Vec<u8>> {
    fn collect(
        root: &Path,
        directory: &Path,
        active: bool,
        entries: &mut BTreeMap<PathBuf, Vec<u8>>,
    ) {
        for entry in fs::read_dir(directory).unwrap() {
            let entry = entry.unwrap();
            let path = entry.path();
            let relative = path.strip_prefix(root).unwrap().to_path_buf();
            let kind = entry.file_type().unwrap();
            let bytes = if kind.is_dir() {
                collect(root, &path, active, entries);
                Vec::new()
            } else if active && relative == Path::new(LOCK) {
                // Windows can deny reads of bytes under an exclusive native lock.
                // Retain the exact regular entry/length; compare bytes after release.
                assert!(kind.is_file());
                path.metadata().unwrap().len().to_le_bytes().to_vec()
            } else {
                assert!(kind.is_file());
                fs::read(path).unwrap()
            };
            entries.insert(relative, bytes);
        }
    }
    let mut entries = BTreeMap::new();
    collect(root, root, active_owner, &mut entries);
    entries
}

struct Process(Child);

impl Process {
    fn wait(&mut self) -> std::process::ExitStatus {
        let started = Instant::now();
        loop {
            if let Some(status) = self.0.try_wait().unwrap() {
                return status;
            }
            assert!(
                started.elapsed() < PROCESS_TIMEOUT,
                "child process timed out"
            );
            std::thread::sleep(Duration::from_millis(10));
        }
    }
}

impl Drop for Process {
    fn drop(&mut self) {
        let _ = self.0.kill();
        let _ = self.0.wait();
    }
}

fn run(mut command: Command) -> Output {
    let mut child = Process(
        command
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()
            .unwrap(),
    );
    let read = |mut pipe: Box<dyn Read + Send>| {
        let (sender, receiver) = mpsc::channel();
        std::thread::spawn(move || {
            let mut bytes = Vec::new();
            let result = pipe.read_to_end(&mut bytes).map(|_| bytes);
            let _ = sender.send(result);
        });
        receiver
    };
    let stdout = read(Box::new(child.0.stdout.take().unwrap()));
    let stderr = read(Box::new(child.0.stderr.take().unwrap()));
    let status = child.wait();
    Output {
        status,
        stdout: stdout.recv_timeout(PROCESS_TIMEOUT).unwrap().unwrap(),
        stderr: stderr.recv_timeout(PROCESS_TIMEOUT).unwrap().unwrap(),
    }
}

fn success(output: Output) -> String {
    assert!(
        output.status.success(),
        "stdout: {}\nstderr: {}",
        String::from_utf8_lossy(&output.stdout),
        String::from_utf8_lossy(&output.stderr)
    );
    String::from_utf8(output.stdout).unwrap()
}

fn failure(output: Output, code: &str) -> String {
    assert!(!output.status.success(), "command unexpectedly succeeded");
    let stderr = String::from_utf8(output.stderr).unwrap();
    assert!(stderr.contains(code), "missing {code}: {stderr}");
    stderr
}

struct Standalone {
    _directory: TempDir,
    binary: PathBuf,
}

impl Standalone {
    fn new() -> Self {
        let directory = TempDir::new().unwrap();
        let binary = directory.path().join(if cfg!(windows) {
            "identity.exe"
        } else {
            "identity"
        });
        fs::copy(env!("CARGO_BIN_EXE_identity"), &binary).unwrap();
        Self {
            _directory: directory,
            binary,
        }
    }

    fn command(
        &self,
        operation: &str,
        root: &Path,
        output_root: impl AsRef<std::ffi::OsStr>,
    ) -> Command {
        let mut command = Command::new(&self.binary);
        command
            .current_dir(root)
            .arg(operation)
            .arg("--repository-root")
            .arg(root)
            .arg("--output-root")
            .arg(output_root.as_ref());
        if matches!(operation, "v1-inspect" | "v1-recover") {
            command.env("IDENTITY_PYTHON", root.join("missing-python"));
        }
        command
    }
}

fn action(
    path: String,
    operation: PlanOperation,
    before: Option<&[u8]>,
    manifest: bool,
) -> PlanAction {
    PlanAction {
        scope: if manifest {
            PlanActionScope::Manifest
        } else {
            PlanActionScope::Artifact
        },
        target_id: path.clone(),
        path,
        adapter_id: "synthetic-recovery-fixture".to_owned(),
        adapter_version: "1.0.0".to_owned(),
        operation,
        input_fingerprint: "a".repeat(64),
        current_sha256: before.map(digest),
        current_bytes: before.map(|bytes| u64::try_from(bytes.len()).unwrap()),
        previous_sha256: before.map(digest),
        required_approvals: BTreeSet::new(),
        warnings: Vec::new(),
    }
}

// Construct a small explicit retained v2 journal over two actual generated files.
// This is synthetic fixture construction, not a claim of process interruption.
fn retained_transaction(root: &Path, output_root: &str) -> PathBuf {
    let manifest_path = format!("{output_root}/.identity-manifest.json");
    let original_manifest = fs::read(root.join(&manifest_path)).unwrap();
    let manifest: Value = serde_json::from_slice(&original_manifest).unwrap();
    let outputs = manifest["outputs"].as_array().unwrap();
    let replaced = outputs[0]["path"].as_str().unwrap();
    let removed = outputs[1]["path"].as_str().unwrap();
    let replaced_before = fs::read(root.join(replaced)).unwrap();
    let removed_before = fs::read(root.join(removed)).unwrap();
    let created = format!("{output_root}/synthetic-created.json");
    let after = b"synthetic interrupted replacement";
    let created_after = b"synthetic created output";
    let mut plan = CompilerPlan {
        schema: COMPILER_PLAN_SCHEMA.to_owned(),
        project_id: manifest["projectId"].as_str().unwrap().to_owned(),
        source_digest: manifest["sourceDigest"].as_str().unwrap().to_owned(),
        plan_digest: String::new(),
        output_root: output_root.to_owned(),
        manifest_path: manifest_path.clone(),
        actions: vec![
            action(created.clone(), PlanOperation::Create, None, false),
            action(
                replaced.to_owned(),
                PlanOperation::Replace,
                Some(&replaced_before),
                false,
            ),
            action(
                removed.to_owned(),
                PlanOperation::Remove,
                Some(&removed_before),
                false,
            ),
            action(
                manifest_path.clone(),
                PlanOperation::Replace,
                Some(&original_manifest),
                true,
            ),
        ],
        compatibility: Vec::new(),
        diagnostics: Vec::new(),
        required_approvals: BTreeSet::new(),
    };
    // Plan v1 frames its own serialized public model with an empty digest field.
    plan.plan_digest = digest(&serde_json::to_vec(&plan).unwrap());
    let transaction = root.join(TRANSACTIONS).join(&plan.plan_digest);
    for (path, bytes) in [
        (replaced, replaced_before.as_slice()),
        (removed, removed_before.as_slice()),
        (manifest_path.as_str(), original_manifest.as_slice()),
    ] {
        write(&transaction.join("backup").join(path), bytes);
    }
    write(&root.join(&created), created_after);
    write(&root.join(replaced), after);
    fs::remove_file(root.join(removed)).unwrap();
    write(
        &transaction.join("journal.json"),
        &serde_json::to_vec_pretty(&json!({
            "schema": "identity.compiler-transaction/v2",
            "plan": plan,
            "manifestAfterSha256": digest(b"synthetic unpublished manifest"),
            "actions": [
                {"path": created, "operation": "create", "afterSha256": digest(created_after)},
                {"path": replaced, "operation": "replace", "afterSha256": digest(after)},
                {"path": removed, "operation": "remove", "afterSha256": null}
            ]
        }))
        .unwrap(),
    );
    transaction
}

#[test]
fn inspection_of_absent_state_needs_no_python_or_identity_source_and_creates_nothing() {
    let binary = Standalone::new();
    let root = TempDir::new().unwrap();
    write(
        &root.path().join("notes/sentinel"),
        b"preserve unrelated file",
    );
    let mut before = snapshot(root.path(), false);
    let output = success(run(binary.command("v1-inspect", root.path(), OUTPUT)));
    assert!(output.contains("Pending transactions: 0"));
    assert!(output.contains("Empty workspaces: 0"));
    assert!(output.contains("uncoordinated observation (no existing writer lock)"));
    assert_eq!(snapshot(root.path(), false), before);
    assert!(!root.path().join(".cache").exists());
    let recovered = success(run(binary.command("v1-recover", root.path(), OUTPUT)));
    assert!(recovered.contains("Recovered 0 v1 Identity transactions"));
    for relative in [".cache", ".cache/identity", LOCK] {
        before.insert(PathBuf::from(relative), Vec::new());
    }
    assert_eq!(snapshot(root.path(), false), before);
}

#[test]
fn standalone_inspection_recovery_and_regeneration_preserve_the_real_consumer() {
    let binary = Standalone::new();
    for output_root in [OUTPUT, "generated/branding"] {
        let root = consumer();
        success(run(binary.command("v1-generate", root.path(), output_root)));
        let original = snapshot(root.path(), false);
        let transaction = retained_transaction(root.path(), output_root);
        if output_root != OUTPUT {
            let pending = snapshot(root.path(), false);
            for operation in ["v1-inspect", "v1-recover"] {
                failure(
                    run(binary.command(operation, root.path(), OUTPUT)),
                    "IDN2324",
                );
                assert_eq!(snapshot(root.path(), false), pending);
            }
            // Model retained evidence from before the persistent-lock protocol.
            // No participant is active; inspection must not create a new file.
            fs::remove_file(root.path().join(LOCK)).unwrap();
        }
        let pending = snapshot(root.path(), false);
        let inspection = success(run(binary.command("v1-inspect", root.path(), output_root)));
        assert!(inspection.contains("Pending transactions: 1"));
        let coordination = if output_root == OUTPUT {
            "Writer coordination: shared lock held"
        } else {
            "uncoordinated observation (no existing writer lock)"
        };
        assert!(inspection.contains(coordination));
        assert!(inspection.contains("Restore: "));
        assert!(inspection.contains("Remove: "));
        assert!(inspection.contains(transaction.file_name().unwrap().to_str().unwrap()));
        assert_eq!(snapshot(root.path(), false), pending);
        for operation in ["v1-generate", "v1-verify"] {
            let guidance = failure(
                run(binary.command(operation, root.path(), output_root)),
                "IDN2301",
            );
            for text in [
                "v1-inspect",
                "v1-recover",
                "--repository-root",
                "--output-root",
            ] {
                assert!(
                    guidance.contains(text),
                    "missing recovery route {text}: {guidance}"
                );
            }
            assert_eq!(snapshot(root.path(), false), pending);
        }
        let recovered = success(run(binary.command("v1-recover", root.path(), output_root)));
        assert!(recovered.contains("Recovered 1 v1 Identity transactions"));
        assert!(!transaction.exists());
        assert_eq!(snapshot(root.path(), false), original);
        let empty = success(run(binary.command("v1-recover", root.path(), output_root)));
        assert!(empty.contains("Recovered 0 v1 Identity transactions"));
        success(run(binary.command("v1-generate", root.path(), output_root)));
        success(run(binary.command("v1-verify", root.path(), output_root)));
        assert_eq!(snapshot(root.path(), false), original);
    }
}

#[test]
fn recovery_ignores_broken_source_and_python_but_preserves_canonical_bytes() {
    let binary = Standalone::new();
    let root = consumer();
    success(run(binary.command("v1-generate", root.path(), OUTPUT)));
    retained_transaction(root.path(), OUTPUT);
    let source = root.path().join(".identity/identity.json");
    fs::write(&source, b"deliberately invalid canonical input").unwrap();
    let canonical = snapshot(&root.path().join(".identity"), false);
    let pending = snapshot(root.path(), false);
    success(run(binary.command("v1-inspect", root.path(), OUTPUT)));
    assert_eq!(snapshot(root.path(), false), pending);
    success(run(binary.command("v1-recover", root.path(), OUTPUT)));
    assert_eq!(snapshot(&root.path().join(".identity"), false), canonical);
    assert_eq!(
        fs::read(root.path().join("notes/unrelated.txt")).unwrap(),
        b"unrelated source stays unchanged"
    );
}

#[test]
fn corrupt_legacy_and_drifted_transactions_fail_closed_through_both_commands() {
    let binary = Standalone::new();
    for corruption in ["journal", "legacy", "backup", "destination"] {
        let root = consumer();
        success(run(binary.command("v1-generate", root.path(), OUTPUT)));
        let transaction = retained_transaction(root.path(), OUTPUT);
        let journal_path = transaction.join("journal.json");
        let journal: Value = serde_json::from_slice(&fs::read(&journal_path).unwrap()).unwrap();
        let replaced = journal["actions"][1]["path"].as_str().unwrap();
        match corruption {
            "journal" => fs::write(journal_path, b"invalid JSON").unwrap(),
            "legacy" => {
                let mut legacy = journal.clone();
                legacy["schema"] = json!("identity.compiler-transaction/v1");
                fs::write(journal_path, serde_json::to_vec(&legacy).unwrap()).unwrap();
            }
            "backup" => {
                fs::write(transaction.join("backup").join(replaced), b"damaged backup").unwrap();
            }
            "destination" => fs::write(
                root.path().join(replaced),
                b"unrelated edit after interruption",
            )
            .unwrap(),
            _ => unreachable!(),
        }
        let before = snapshot(root.path(), false);
        for operation in ["v1-inspect", "v1-recover"] {
            let code = if corruption == "legacy" {
                "IDN2325"
            } else {
                "IDN2324"
            };
            failure(run(binary.command(operation, root.path(), OUTPUT)), code);
            assert_eq!(
                snapshot(root.path(), false),
                before,
                "{corruption} {operation}"
            );
        }
    }
}

#[test]
fn missing_lock_inspection_and_empty_workspace_cleanup_remain_explicit() {
    let binary = Standalone::new();
    let root = TempDir::new().unwrap();
    let orphan = root.path().join(TRANSACTIONS).join("a".repeat(64));
    fs::create_dir_all(&orphan).unwrap();
    let before = snapshot(root.path(), false);
    let inspected = success(run(binary.command("v1-inspect", root.path(), OUTPUT)));
    assert!(inspected.contains("Pending transactions: 0"));
    assert!(inspected.contains("Empty workspaces: 1"));
    assert!(inspected.contains("uncoordinated observation (no existing writer lock)"));
    assert_eq!(snapshot(root.path(), false), before);
    success(run(binary.command("v1-recover", root.path(), OUTPUT)));
    assert!(!orphan.exists());
    assert_eq!(fs::read(root.path().join(LOCK)).unwrap(), b"");
    let recovered = snapshot(root.path(), false);
    success(run(binary.command("v1-inspect", root.path(), OUTPUT)));
    assert_eq!(snapshot(root.path(), false), recovered);
}

#[test]
fn unsupported_output_roots_fail_before_coordination_metadata_or_source_changes() {
    let binary = Standalone::new();
    let root = TempDir::new().unwrap();
    write(&root.path().join(".identity/sentinel"), b"canonical source");
    let before = snapshot(root.path(), false);
    for output_root in [
        ".identity",
        ".cache",
        ".git",
        "../escape",
        "assets/identity:stream",
    ] {
        for operation in ["v1-inspect", "v1-recover"] {
            let output = run(binary.command(operation, root.path(), output_root));
            assert!(
                !output.status.success(),
                "{operation} accepted {output_root}"
            );
            assert_eq!(snapshot(root.path(), false), before);
        }
    }
}

#[cfg(unix)]
#[test]
fn unix_cli_output_scope_preserves_literal_names_and_rejects_non_utf8() {
    use std::ffi::OsString;
    use std::os::unix::ffi::OsStringExt;

    let binary = Standalone::new();
    let root = consumer();
    write(
        &root.path().join(r"generated\branding/sentinel"),
        b"literal backslash directory is unrelated source",
    );
    let invalid = [
        OsString::from(r"generated\branding"),
        OsString::from_vec(b"generated/\xffbranding".to_vec()),
    ];
    let assert_rejected = |before: &BTreeMap<PathBuf, Vec<u8>>| {
        for output_root in &invalid {
            for operation in ["v1-inspect", "v1-recover", "v1-generate", "v1-verify"] {
                let output = run(binary.command(operation, root.path(), output_root));
                assert!(
                    !output.status.success(),
                    "{operation} accepted or aliased raw output root {output_root:?}"
                );
                assert_eq!(
                    &snapshot(root.path(), false),
                    before,
                    "{operation} changed state for raw output root {output_root:?}"
                );
            }
        }
    };

    // Valid canonical input ensures source validation does not mask the CLI
    // boundary. Rejected raw names cannot create even coordination metadata.
    assert_rejected(&snapshot(root.path(), false));
    assert!(!root.path().join(".cache").exists());

    // A retained transaction for the portable spelling must not become recovery
    // authority for the different Unix filename containing a literal backslash.
    let output_root = "generated/branding";
    success(run(binary.command("v1-generate", root.path(), output_root)));
    let transaction = retained_transaction(root.path(), output_root);
    assert_rejected(&snapshot(root.path(), false));
    assert!(transaction.join("journal.json").is_file());
    success(run(binary.command("v1-inspect", root.path(), output_root)));
    success(run(binary.command("v1-recover", root.path(), output_root)));
    assert!(!transaction.exists());
    success(run(binary.command("v1-generate", root.path(), output_root)));
    success(run(binary.command("v1-verify", root.path(), output_root)));
    assert_eq!(
        fs::read(root.path().join(r"generated\branding/sentinel")).unwrap(),
        b"literal backslash directory is unrelated source"
    );
}

#[test]
fn help_advertises_the_supported_read_only_and_explicit_recovery_route() {
    let binary = Standalone::new();
    let mut command = Command::new(&binary.binary);
    command.arg("--help");
    let help = success(run(command));
    assert!(help.contains("v1-inspect"));
    assert!(help.contains("v1-recover"));
    for operation in ["v1-inspect", "v1-recover"] {
        let mut command = Command::new(&binary.binary);
        command.args([operation, "--help"]);
        let help = success(run(command));
        assert!(help.contains("--repository-root"));
        assert!(help.contains("--output-root"));
        assert!(help.contains(OUTPUT));
    }
}

#[test]
#[ignore = "independent native-lock owner; invoked only by the bounded CLI test"]
fn exclusive_owner() {
    let root = PathBuf::from(std::env::var_os("IDENTITY_RECOVERY_OWNER_ROOT").unwrap());
    let file = fs::OpenOptions::new()
        .read(true)
        .write(true)
        .open(root.join(LOCK))
        .unwrap();
    file.try_lock().unwrap();
    println!("{OWNER_READY}");
    std::io::stdout().flush().unwrap();
    std::io::stdin().read_exact(&mut [0_u8; 1]).unwrap();
    file.unlock().unwrap();
}

fn owner(root: &Path) -> Process {
    let mut child = Process(
        Command::new(std::env::current_exe().unwrap())
            .args([
                "--exact",
                "exclusive_owner",
                "--ignored",
                "--nocapture",
                "--test-threads=1",
            ])
            .env("IDENTITY_RECOVERY_OWNER_ROOT", root)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::inherit())
            .spawn()
            .unwrap(),
    );
    let stdout = child.0.stdout.take().unwrap();
    let (sender, receiver) = mpsc::channel();
    std::thread::spawn(move || {
        for line in BufReader::new(stdout).lines() {
            let Ok(line) = line else { break };
            if sender.send(line).is_err() {
                break;
            }
        }
    });
    let started = Instant::now();
    loop {
        let remaining = PROCESS_TIMEOUT.saturating_sub(started.elapsed());
        let line = receiver
            .recv_timeout(remaining)
            .expect("native owner readiness");
        if line.contains(OWNER_READY) {
            break;
        }
    }
    assert!(child.0.try_wait().unwrap().is_none());
    child
}

#[test]
fn active_native_writer_blocks_inspection_and_recovery_without_touching_its_workspace() {
    let binary = Standalone::new();
    let root = consumer();
    success(run(binary.command("v1-generate", root.path(), OUTPUT)));
    retained_transaction(root.path(), OUTPUT);
    let before = snapshot(root.path(), false);
    let mut owner = owner(root.path());
    let held = snapshot(root.path(), true);
    for operation in ["v1-inspect", "v1-recover"] {
        failure(
            run(binary.command(operation, root.path(), OUTPUT)),
            "IDN2346",
        );
        assert_eq!(snapshot(root.path(), true), held);
    }
    owner.0.kill().unwrap();
    assert!(!owner.wait().success());
    assert_eq!(snapshot(root.path(), false), before);
    success(run(binary.command("v1-inspect", root.path(), OUTPUT)));
    success(run(binary.command("v1-recover", root.path(), OUTPUT)));
    success(run(binary.command("v1-verify", root.path(), OUTPUT)));
}
