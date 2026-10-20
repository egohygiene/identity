// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

use super::*;
use crate::compiler::{ManifestOutput, PlanAction};
use tempfile::TempDir;

mod inspection_tests;
mod process_tests;

const OUTPUT: &str = "assets/identity";

fn write_fixture(path: &Path, bytes: &[u8]) -> std::io::Result<()> {
    fs::create_dir_all(path.parent().unwrap())?;
    fs::write(path, bytes)
}

fn fixture(
    root: &Path,
    output_root: &str,
) -> (CompilerPlan, Vec<RenderedArtifact>, CompilerManifest) {
    let manifest_path = format!("{output_root}/.identity-manifest.json");
    let mut actions = Vec::new();
    let mut artifacts = Vec::new();
    for (name, operation, old) in [
        ("created.json", PlanOperation::Create, None),
        (
            "replaced.json",
            PlanOperation::Replace,
            Some(b"old replaced".as_slice()),
        ),
        (
            "removed.json",
            PlanOperation::Remove,
            Some(b"old removed".as_slice()),
        ),
        (
            ".identity-manifest.json",
            PlanOperation::Replace,
            Some(b"old manifest".as_slice()),
        ),
    ] {
        let path = format!("{output_root}/{name}");
        if let Some(bytes) = old {
            write_fixture(&root.join(&path), bytes).unwrap();
        }
        actions.push(PlanAction {
            scope: if path == manifest_path {
                PlanActionScope::Manifest
            } else {
                PlanActionScope::Artifact
            },
            target_id: name.to_owned(),
            path: path.clone(),
            adapter_id: "fixture".to_owned(),
            adapter_version: "1.0.0".to_owned(),
            operation,
            input_fingerprint: "a".repeat(64),
            current_sha256: old.map(sha256_hex),
            current_bytes: old.map(|bytes| u64::try_from(bytes.len()).unwrap()),
            previous_sha256: old.map(sha256_hex),
            required_approvals: BTreeSet::new(),
            warnings: Vec::new(),
        });
        if path != manifest_path
            && matches!(operation, PlanOperation::Create | PlanOperation::Replace)
        {
            artifacts.push(RenderedArtifact {
                target_id: name.to_owned(),
                path,
                bytes: format!("new {name}").into_bytes(),
            });
        }
    }
    let mut plan = CompilerPlan {
        schema: crate::compiler::COMPILER_PLAN_SCHEMA.to_owned(),
        project_id: "fixture".to_owned(),
        source_digest: "a".repeat(64),
        plan_digest: String::new(),
        output_root: output_root.to_owned(),
        manifest_path,
        actions,
        compatibility: Vec::new(),
        diagnostics: Vec::new(),
        required_approvals: BTreeSet::new(),
    };
    plan.plan_digest = crate::compiler::plan_digest(&plan).unwrap();
    let manifest = CompilerManifest {
        schema: crate::compiler::COMPILER_MANIFEST_SCHEMA.to_owned(),
        project_id: plan.project_id.clone(),
        source_digest: plan.source_digest.clone(),
        plan_digest: plan.plan_digest.clone(),
        outputs: artifacts
            .iter()
            .map(|artifact| ManifestOutput {
                target_id: artifact.target_id.clone(),
                profile: "fixture".to_owned(),
                path: artifact.path.clone(),
                media_type: "application/json".to_owned(),
                adapter_id: "fixture".to_owned(),
                adapter_version: "1.0.0".to_owned(),
                input_fingerprint: "a".repeat(64),
                sha256: sha256_hex(&artifact.bytes),
                bytes: u64::try_from(artifact.bytes.len()).unwrap(),
            })
            .collect(),
        adapters: Vec::new(),
        evidence: Vec::new(),
    };
    (plan, artifacts, manifest)
}

fn interrupted(root: &Path, output_root: &str, after: usize) -> PathBuf {
    let (plan, artifacts, manifest) = fixture(root, output_root);
    let mut store = LocalArtifactStore::with_output_root(root, output_root)
        .unwrap()
        .fail_after_mutations(after);
    let error = store
        .commit(&plan, &artifacts, &manifest)
        .expect_err("inject interruption");
    assert_eq!(error.diagnostics[0].code, "IDN2399", "{error:?}");
    store.transaction_directory(&plan.plan_digest)
}

fn journal(transaction: &Path) -> TransactionJournal {
    serde_json::from_slice(&fs::read(LocalArtifactStore::journal_path(transaction)).unwrap())
        .unwrap()
}

fn rewrite(transaction: &Path, mut journal: TransactionJournal, rehash: bool) -> PathBuf {
    if rehash {
        journal.plan.plan_digest = crate::compiler::plan_digest(&journal.plan).unwrap();
    }
    let destination = if rehash {
        transaction
            .parent()
            .unwrap()
            .join(&journal.plan.plan_digest)
    } else {
        transaction.to_path_buf()
    };
    if destination != transaction {
        fs::rename(transaction, &destination).unwrap();
    }
    fs::write(
        LocalArtifactStore::journal_path(&destination),
        serde_json::to_vec(&journal).unwrap(),
    )
    .unwrap();
    destination
}

fn tree(root: &Path) -> BTreeMap<PathBuf, Vec<u8>> {
    tree_with_writer_lock_metadata(root, false)
}

fn tree_with_writer_lock_metadata(root: &Path, metadata_only: bool) -> BTreeMap<PathBuf, Vec<u8>> {
    fn collect(
        root: &Path,
        path: &Path,
        entries: &mut BTreeMap<PathBuf, Vec<u8>>,
        metadata_only: bool,
    ) {
        for entry in fs::read_dir(path).unwrap() {
            let entry = entry.unwrap();
            let path = entry.path();
            let kind = entry.file_type().unwrap();
            let redirected = kind.is_symlink();
            #[cfg(windows)]
            let redirected = {
                use std::os::windows::fs::MetadataExt;
                redirected || path.symlink_metadata().unwrap().file_attributes() & 0x400 != 0
            };
            let bytes = if redirected {
                fs::read_link(&path)
                    .unwrap()
                    .to_string_lossy()
                    .as_bytes()
                    .to_vec()
            } else if kind.is_dir() {
                collect(root, &path, entries, metadata_only);
                Vec::new()
            } else if kind.is_file() {
                if metadata_only
                    && path.strip_prefix(root).unwrap() == Path::new(".cache/identity/writer.lock")
                {
                    // Windows native locks can deny byte reads while held. Keep
                    // the path/type and length in active-owner snapshots; process
                    // tests verify exact coordination bytes after releasing it.
                    path.metadata().unwrap().len().to_le_bytes().to_vec()
                } else {
                    fs::read(&path).unwrap()
                }
            } else {
                b"non-regular filesystem entry".to_vec()
            };
            entries.insert(path.strip_prefix(root).unwrap().to_path_buf(), bytes);
        }
    }
    let mut result = BTreeMap::new();
    collect(root, root, &mut result, metadata_only);
    result
}

fn assert_only_writer_lock_created(root: &Path, mut before: BTreeMap<PathBuf, Vec<u8>>) {
    let lock = PathBuf::from(".cache/identity/writer.lock");
    assert!(!before.contains_key(&lock));
    assert_eq!(fs::read(root.join(&lock)).unwrap(), b"");
    before.insert(lock, Vec::new());
    assert_eq!(
        tree(root),
        before,
        "only the persistent empty coordination file may appear"
    );
}

fn assert_blocked_without_mutation(root: &Path) {
    let before = tree(root);
    let mut store = LocalArtifactStore::new(root).unwrap();
    assert!(store.recover().is_err(), "untrusted recovery must fail");
    assert_eq!(
        tree(root),
        before,
        "all outputs, sentinels, journals, and backups must survive"
    );
}

#[test]
fn recovery_rejects_every_operation_outside_its_independently_authorized_scope() {
    for target in [
        ".identity/sentinel",
        "notes/sentinel",
        "assets/identity-other/sentinel",
        ".IDENTITY/sentinel",
    ] {
        for index in 0..4 {
            let root = TempDir::new().unwrap();
            let transaction = interrupted(root.path(), OUTPUT, 4);
            write_fixture(&root.path().join(target), b"user sentinel").unwrap();
            let mut journal = journal(&transaction);
            journal.plan.actions[index].path = target.to_owned();
            if index == 3 {
                journal.plan.manifest_path = target.to_owned();
            } else {
                journal.actions[index].path = target.to_owned();
            }
            rewrite(&transaction, journal, true); // Pass digest checks; exercise authority checks.
            assert_blocked_without_mutation(root.path());
        }
    }
    for scope in [
        ".identity",
        ".Identity/generated",
        ".git/objects",
        ".cache/generated",
    ] {
        let root = TempDir::new().unwrap();
        assert!(LocalArtifactStore::with_output_root(root.path(), scope).is_err());
    }
}

#[test]
// Keep the corruption matrix together so every case shares the no-mutation assertion.
#[allow(clippy::too_many_lines)]
fn complete_preflight_rejects_corrupt_journals_and_backups_without_partial_rollback() {
    for corruption in [
        "directory",
        "digest",
        "plan",
        "duplicate",
        "conflict",
        "case-alias",
        "missing-backup",
        "bad-backup",
        "missing-manifest-backup",
        "missing-action",
        "extra-action",
        "bad-operation",
        "missing-after",
        "destination-drift",
        "manifest-drift",
    ] {
        let root = TempDir::new().unwrap();
        let transaction = interrupted(root.path(), OUTPUT, 4);
        let mut evidence = journal(&transaction);
        let mut rehash = false;
        match corruption {
            "directory" => {
                fs::rename(
                    &transaction,
                    transaction.parent().unwrap().join("bad-plan-id"),
                )
                .unwrap();
            }
            "digest" => {
                evidence.plan.plan_digest = "f".repeat(64);
            }
            "plan" => {
                evidence.plan.project_id = "tampered".to_owned();
            }
            "duplicate" => {
                evidence.plan.actions[0] = evidence.plan.actions[1].clone();
                rehash = true;
            }
            "conflict" => {
                evidence.plan.actions[0].path = format!("{OUTPUT}/replaced.json/child");
                rehash = true;
            }
            "case-alias" => {
                evidence.plan.actions[0].path = format!("{OUTPUT}/REPLACED.json");
                rehash = true;
            }
            "missing-backup" => {
                fs::remove_file(LocalArtifactStore::backup_path(
                    &transaction,
                    &evidence.plan.actions[1].path,
                ))
                .unwrap();
            }
            "bad-backup" => {
                fs::write(
                    LocalArtifactStore::backup_path(&transaction, &evidence.plan.actions[1].path),
                    b"tampered backup",
                )
                .unwrap();
            }
            "missing-manifest-backup" => {
                fs::remove_file(LocalArtifactStore::backup_path(
                    &transaction,
                    &evidence.plan.manifest_path,
                ))
                .unwrap();
            }
            "missing-action" => {
                evidence.actions.pop();
            }
            "extra-action" => {
                evidence.actions.push(evidence.actions[0].clone());
            }
            "bad-operation" => {
                evidence.actions[0].operation = PlanOperation::Remove;
            }
            "missing-after" => {
                evidence.actions[0].after_sha256 = None;
            }
            "destination-drift" => {
                fs::write(
                    root.path().join(&evidence.actions[0].path),
                    b"unrelated user edit",
                )
                .unwrap();
            }
            "manifest-drift" => {
                fs::write(
                    root.path().join(&evidence.plan.manifest_path),
                    b"unrelated manifest edit",
                )
                .unwrap();
            }
            _ => unreachable!(),
        }
        if corruption != "directory" {
            rewrite(&transaction, evidence, rehash);
        }
        assert_blocked_without_mutation(root.path());
    }
}

#[test]
fn preflight_covers_all_transactions_before_recovery_or_orphan_cleanup() {
    let root = TempDir::new().unwrap();
    let transaction = interrupted(root.path(), OUTPUT, 4);
    fs::create_dir_all(transaction.parent().unwrap().join("0".repeat(64))).unwrap();
    let corrupt = transaction.parent().unwrap().join("f".repeat(64));
    fs::create_dir_all(&corrupt).unwrap();
    fs::write(corrupt.join("journal.json"), b"invalid journal").unwrap();
    assert_blocked_without_mutation(root.path());
    fs::remove_dir_all(corrupt).unwrap();
    let mut store = LocalArtifactStore::new(root.path()).unwrap();
    assert_eq!(store.recover().unwrap().recovered_transactions, 1);
    assert!(!store.recovery_required().unwrap());
}

#[test]
fn legacy_v1_journals_are_preserved_for_explicit_review_without_automatic_migration() {
    let root = TempDir::new().unwrap();
    let transaction = interrupted(root.path(), OUTPUT, 4);
    fs::write(
        transaction.join("journal.json"),
        serde_json::to_vec(&serde_json::json!({
            "schema": "identity.compiler-transaction/v1", "planDigest": "a".repeat(64),
            "manifestPath": ".identity/sentinel", "manifestExisted": false,
            "actions": [{"path": "notes/sentinel", "operation": "create"}]
        }))
        .unwrap(),
    )
    .unwrap();
    assert_blocked_without_mutation(root.path());
    let error = LocalArtifactStore::new(root.path())
        .unwrap()
        .recover()
        .unwrap_err();
    assert_eq!(error.kind, FailureKind::Unsupported);
    assert_eq!(error.diagnostics[0].code, "IDN2325");
}

#[test]
fn every_interruption_point_and_repeated_recovery_restore_previous_state() {
    for after in 1..=4 {
        for recover_after in 0..=4 {
            let root = TempDir::new().unwrap();
            interrupted(root.path(), OUTPUT, after);
            if recover_after > 0 {
                let mut store = LocalArtifactStore::new(root.path())
                    .unwrap()
                    .fail_after_mutations(recover_after);
                assert!(store.recover().is_err());
            }
            let mut store = LocalArtifactStore::new(root.path()).unwrap();
            assert_eq!(store.recover().unwrap().recovered_transactions, 1);
            assert_eq!(store.recover().unwrap().recovered_transactions, 0);
            assert!(!root.path().join(format!("{OUTPUT}/created.json")).exists());
            for (path, bytes) in [
                ("replaced.json", b"old replaced".as_slice()),
                ("removed.json", b"old removed".as_slice()),
                (".identity-manifest.json", b"old manifest".as_slice()),
            ] {
                assert_eq!(
                    fs::read(root.path().join(OUTPUT).join(path)).unwrap(),
                    bytes
                );
            }
        }
    }
}

#[test]
fn custom_scope_must_be_authorized_by_the_caller_for_both_commit_and_recovery() {
    let root = TempDir::new().unwrap();
    interrupted(root.path(), "generated/branding", 2);
    assert_blocked_without_mutation(root.path());
    let mut store =
        LocalArtifactStore::with_output_root(root.path(), "generated/branding").unwrap();
    assert_eq!(store.recover().unwrap().recovered_transactions, 1);
}

#[cfg(unix)]
#[test]
fn recovery_rejects_symlinked_cache_destinations_journals_and_backups() {
    for location in [
        "cache",
        "cache-identity",
        "transaction-root",
        "transaction",
        "staging-root",
        "journal",
        "backup-root",
        "backup-file",
        "manifest-backup",
        "output-root",
        "output-file",
    ] {
        let root = TempDir::new().unwrap();
        let transaction = interrupted(root.path(), OUTPUT, 4);
        let source = match location {
            "cache" => root.path().join(".cache"),
            "cache-identity" => root.path().join(".cache/identity"),
            "transaction-root" => root.path().join(TRANSACTION_ROOT),
            "transaction" => transaction.clone(),
            "staging-root" => transaction.join("staged"),
            "journal" => transaction.join("journal.json"),
            "backup-root" => transaction.join("backup"),
            "backup-file" => transaction.join(format!("backup/{OUTPUT}/replaced.json")),
            "manifest-backup" => {
                transaction.join(format!("backup/{OUTPUT}/.identity-manifest.json"))
            }
            "output-root" => root.path().join(OUTPUT),
            "output-file" => root.path().join(format!("{OUTPUT}/created.json")),
            _ => unreachable!(),
        };
        let moved = root.path().join("symlink-target");
        fs::rename(&source, &moved).unwrap();
        std::os::unix::fs::symlink(moved, source).unwrap();
        assert_blocked_without_mutation(root.path());
    }
}

#[test]
fn commit_rejects_unplanned_writes_and_portable_path_aliases_before_creating_cache() {
    for path in [
        "../sentinel",
        ".identity/sentinel",
        "assets/identity/a:stream",
        "assets/identity/NUL",
        "assets/identity/trailing.",
        "assets/identity/space ",
        "assets/identity/back\\slash",
        "assets/identity/nul\0byte",
    ] {
        let root = TempDir::new().unwrap();
        let (mut plan, mut artifacts, manifest) = fixture(root.path(), OUTPUT);
        plan.actions[0].path = path.to_owned();
        plan.plan_digest = crate::compiler::plan_digest(&plan).unwrap();
        artifacts[0].path = path.to_owned();
        let before = tree(root.path());
        assert!(
            LocalArtifactStore::new(root.path())
                .unwrap()
                .commit(&plan, &artifacts, &manifest)
                .is_err()
        );
        assert_eq!(tree(root.path()), before);
        assert!(!root.path().join(".cache").exists());
    }
    let root = TempDir::new().unwrap();
    let (plan, mut artifacts, manifest) = fixture(root.path(), OUTPUT);
    artifacts.push(RenderedArtifact {
        target_id: "unplanned".to_owned(),
        path: ".identity/sentinel".to_owned(),
        bytes: b"bad".to_vec(),
    });
    let before = tree(root.path());
    assert!(
        LocalArtifactStore::new(root.path())
            .unwrap()
            .commit(&plan, &artifacts, &manifest)
            .is_err()
    );
    assert_eq!(tree(root.path()), before);
}

#[test]
fn missing_journal_preserves_populated_transaction_evidence() {
    let root = TempDir::new().unwrap();
    let transaction = interrupted(root.path(), OUTPUT, 2);
    fs::remove_file(transaction.join("journal.json")).unwrap();
    assert_blocked_without_mutation(root.path());
}

#[test]
fn conflicting_transactions_are_rejected_before_either_is_recovered() {
    let root = TempDir::new().unwrap();
    let transaction = interrupted(root.path(), OUTPUT, 4);
    let copy = transaction.parent().unwrap().join("copy");
    let bytes = tree(&transaction);
    for (path, content) in bytes {
        let source = transaction.join(&path);
        if source.is_file() {
            write_fixture(&copy.join(path), &content).unwrap();
        } else {
            fs::create_dir_all(copy.join(path)).unwrap();
        }
    }
    let mut evidence = journal(&copy);
    evidence.plan.project_id = "second-transaction".to_owned();
    rewrite(&copy, evidence, true);
    assert_blocked_without_mutation(root.path());
}

#[test]
fn rollback_does_not_write_through_a_preexisting_hard_link_in_its_workspace() {
    let root = TempDir::new().unwrap();
    let transaction = interrupted(root.path(), OUTPUT, 4);
    let sentinel = root.path().join(".identity/sentinel");
    write_fixture(&sentinel, b"canonical sentinel").unwrap();
    fs::hard_link(&sentinel, transaction.join("recovery.tmp")).unwrap();
    LocalArtifactStore::new(root.path())
        .unwrap()
        .recover()
        .unwrap();
    assert_eq!(fs::read(sentinel).unwrap(), b"canonical sentinel");
}

#[test]
fn unusable_recovery_staging_path_is_rejected_before_restoring_any_file() {
    let root = TempDir::new().unwrap();
    let transaction = interrupted(root.path(), OUTPUT, 4);
    fs::create_dir(transaction.join("recovery.tmp")).unwrap();
    assert_blocked_without_mutation(root.path());
}

#[cfg(unix)]
#[test]
fn commit_rejects_each_redirected_cache_component_without_touching_either_tree() {
    for relative in [".cache", ".cache/identity", TRANSACTION_ROOT] {
        let root = TempDir::new().unwrap();
        let external = TempDir::new().unwrap();
        let (plan, artifacts, manifest) = fixture(root.path(), OUTPUT);
        write_fixture(&external.path().join("sentinel"), b"external sentinel").unwrap();
        let link = root.path().join(relative);
        fs::create_dir_all(link.parent().unwrap()).unwrap();
        std::os::unix::fs::symlink(external.path(), link).unwrap();
        let before = tree(root.path());
        let external_before = tree(external.path());
        let mut store = LocalArtifactStore::new(root.path()).unwrap();
        assert!(store.inspect_recovery().is_err());
        assert_eq!(tree(root.path()), before, "inspection {relative}");
        assert_eq!(
            tree(external.path()),
            external_before,
            "inspection {relative}"
        );
        assert!(store.commit(&plan, &artifacts, &manifest).is_err());
        assert!(store.recovery_required().is_err());
        assert!(store.recover().is_err());
        assert_eq!(tree(root.path()), before, "{relative}");
        assert_eq!(tree(external.path()), external_before, "{relative}");
    }
}

#[test]
fn cache_components_must_be_directories_before_generation_or_recovery() {
    for relative in [".cache", ".cache/identity", TRANSACTION_ROOT] {
        let root = TempDir::new().unwrap();
        let (plan, artifacts, manifest) = fixture(root.path(), OUTPUT);
        write_fixture(&root.path().join(relative), b"user-owned cache blocker").unwrap();
        let before = tree(root.path());
        let mut store = LocalArtifactStore::new(root.path()).unwrap();
        assert!(store.commit(&plan, &artifacts, &manifest).is_err());
        assert!(store.recovery_required().is_err());
        assert!(store.recover().is_err());
        assert_eq!(tree(root.path()), before, "{relative}");
    }
}

#[test]
fn commit_never_reuses_a_preexisting_empty_or_populated_workspace() {
    for marker in [
        None,
        Some("staged/sentinel"),
        Some("backup/sentinel"),
        Some("journal.pending"),
        Some("journal.json"),
    ] {
        let root = TempDir::new().unwrap();
        let (plan, artifacts, manifest) = fixture(root.path(), OUTPUT);
        let mut store = LocalArtifactStore::new(root.path()).unwrap();
        let workspace = store.transaction_directory(&plan.plan_digest);
        fs::create_dir_all(&workspace).unwrap();
        if let Some(marker) = marker {
            write_fixture(&workspace.join(marker), b"preserve transaction evidence").unwrap();
        }
        let before = tree(root.path());
        let error = store.commit(&plan, &artifacts, &manifest).unwrap_err();
        assert_eq!(error.kind, FailureKind::Blocked);
        assert_eq!(error.diagnostics[0].code, "IDN2301");
        assert_only_writer_lock_created(root.path(), before);
    }
}

#[test]
fn recovery_inspection_does_not_create_repair_or_clean_workspaces() {
    let root = TempDir::new().unwrap();
    let store = LocalArtifactStore::new(root.path()).unwrap();
    let before = tree(root.path());
    assert!(!store.recovery_required().unwrap());
    assert_eq!(tree(root.path()), before);
    interrupted(root.path(), OUTPUT, 2);
    let before = tree(root.path());
    assert!(store.recovery_required().unwrap());
    assert_eq!(tree(root.path()), before);
}

#[test]
fn repository_root_must_be_a_directory() {
    let root = TempDir::new().unwrap();
    let file = root.path().join("not-a-repository");
    fs::write(&file, b"user sentinel").unwrap();
    let before = tree(root.path());
    assert!(LocalArtifactStore::new(file).is_err());
    assert_eq!(tree(root.path()), before);
}

#[test]
fn recovery_reads_hard_linked_evidence_without_overwriting_its_other_names() {
    for relative in [
        "journal.json",
        "backup/assets/identity/replaced.json",
        "backup/assets/identity/.identity-manifest.json",
        "staged/unconsumed-evidence",
    ] {
        let root = TempDir::new().unwrap();
        let external = TempDir::new().unwrap();
        let transaction = interrupted(root.path(), OUTPUT, 4);
        let evidence = transaction.join(relative);
        if !evidence.exists() {
            write_fixture(&evidence, b"preserved evidence bytes").unwrap();
        }
        fs::hard_link(&evidence, external.path().join("evidence-alias")).unwrap();
        let external_before = tree(external.path());
        let source = root.path().join(".identity/sentinel");
        write_fixture(&source, b"canonical sentinel").unwrap();
        let mut store = LocalArtifactStore::new(root.path()).unwrap();
        assert_eq!(store.recover().unwrap().recovered_transactions, 1);
        assert_eq!(tree(external.path()), external_before, "{relative}");
        assert_eq!(fs::read(source).unwrap(), b"canonical sentinel");
        assert!(!store.recovery_required().unwrap());
    }
}

#[test]
fn transaction_helpers_cannot_write_outside_their_namespace() {
    let root = TempDir::new().unwrap();
    let external = TempDir::new().unwrap();
    let store = LocalArtifactStore::new(root.path()).unwrap();
    let canonical = root.path().join(".identity/sentinel");
    write_fixture(&canonical, b"canonical sentinel").unwrap();
    let source = store.resolve(&format!("{OUTPUT}/previous.json")).unwrap();
    write_fixture(&source, b"generated previous state").unwrap();
    for destination in [
        canonical.clone(),
        root.path().join("notes/sentinel"),
        root.path()
            .join(".cache/identity/transactions-neighbor/sentinel"),
        store.transaction_root().join("../sentinel"),
        store.transaction_root().join("staged/NUL"),
        external.path().join("sentinel"),
    ] {
        let before = tree(root.path());
        let external_before = tree(external.path());
        assert!(store.write_bytes(&destination, b"replacement").is_err());
        assert!(store.copy_file(&source, &destination).is_err());
        assert_eq!(tree(root.path()), before);
        assert_eq!(tree(external.path()), external_before);
    }
    let before = tree(root.path());
    let backup = store
        .transaction_directory(&"a".repeat(64))
        .join("backup/file");
    assert!(store.copy_file(&canonical, &backup).is_err());
    assert_eq!(tree(root.path()), before);
}

#[test]
fn fresh_transaction_writes_never_overwrite_existing_files_or_hard_links() {
    for relative in [
        "staged/assets/identity/created.json",
        "backup/assets/identity/replaced.json",
        "journal.pending",
        "journal.json",
    ] {
        for hard_link in [false, true] {
            let root = TempDir::new().unwrap();
            let external = TempDir::new().unwrap();
            let store = LocalArtifactStore::new(root.path()).unwrap();
            let workspace = store.transaction_directory(&"a".repeat(64));
            let destination = workspace.join(relative);
            fs::create_dir_all(destination.parent().unwrap()).unwrap();
            let sentinel = external.path().join("sentinel");
            fs::write(&sentinel, b"external sentinel").unwrap();
            if hard_link {
                fs::hard_link(&sentinel, &destination).unwrap();
            } else {
                fs::write(&destination, b"transaction sentinel").unwrap();
            }
            let before = tree(root.path());
            let external_before = tree(external.path());
            assert!(
                store
                    .write_bytes(&destination, b"staged replacement")
                    .is_err()
            );
            assert_eq!(
                tree(root.path()),
                before,
                "{relative}, hard_link={hard_link}"
            );
            assert_eq!(tree(external.path()), external_before);
        }
    }
}

#[test]
fn fresh_backups_never_overwrite_existing_files_or_hard_links() {
    for relative in [
        "backup/assets/identity/replaced.json",
        "backup/assets/identity/.identity-manifest.json",
    ] {
        for hard_link in [false, true] {
            let root = TempDir::new().unwrap();
            let external = TempDir::new().unwrap();
            let store = LocalArtifactStore::new(root.path()).unwrap();
            let source = store.resolve(&format!("{OUTPUT}/replaced.json")).unwrap();
            write_fixture(&source, b"generated previous state").unwrap();
            let destination = store.transaction_directory(&"a".repeat(64)).join(relative);
            fs::create_dir_all(destination.parent().unwrap()).unwrap();
            let sentinel = external.path().join("sentinel");
            fs::write(&sentinel, b"external sentinel").unwrap();
            if hard_link {
                fs::hard_link(&sentinel, &destination).unwrap();
            } else {
                fs::write(&destination, b"transaction sentinel").unwrap();
            }
            let before = tree(root.path());
            let external_before = tree(external.path());
            assert!(store.copy_file(&source, &destination).is_err());
            assert_eq!(
                tree(root.path()),
                before,
                "{relative}, hard_link={hard_link}"
            );
            assert_eq!(tree(external.path()), external_before);
        }
    }
}

#[cfg(unix)]
#[test]
fn transaction_writes_and_backups_reject_every_redirected_parent_and_leaf() {
    for relative in [
        "staged",
        "staged/assets",
        "staged/assets/identity",
        "staged/assets/identity/created.json",
        "backup",
        "backup/assets",
        "backup/assets/identity",
        "backup/assets/identity/replaced.json",
        "journal.pending",
        "journal.json",
    ] {
        let root = TempDir::new().unwrap();
        let external = TempDir::new().unwrap();
        let store = LocalArtifactStore::new(root.path()).unwrap();
        let workspace = store.transaction_directory(&"a".repeat(64));
        let link = workspace.join(relative);
        fs::create_dir_all(link.parent().unwrap()).unwrap();
        let sentinel = external.path().join("sentinel");
        fs::write(&sentinel, b"external sentinel").unwrap();
        let leaf = Path::new(relative).extension().is_some();
        std::os::unix::fs::symlink(if leaf { &sentinel } else { external.path() }, &link).unwrap();
        let source = store.resolve(&format!("{OUTPUT}/replaced.json")).unwrap();
        write_fixture(&source, b"generated previous state").unwrap();
        let before = tree(root.path());
        let external_before = tree(external.path());
        if relative.starts_with("backup") {
            let destination = workspace.join("backup/assets/identity/replaced.json");
            assert!(store.copy_file(&source, &destination).is_err());
        } else {
            let destination = if relative.starts_with("staged") {
                workspace.join("staged/assets/identity/created.json")
            } else {
                link
            };
            assert!(
                store
                    .write_bytes(&destination, b"staged replacement")
                    .is_err()
            );
        }
        assert_eq!(tree(root.path()), before, "{relative}");
        assert_eq!(tree(external.path()), external_before, "{relative}");
    }
}

#[cfg(unix)]
#[test]
fn transaction_paths_reject_special_entries_without_opening_them() {
    for relative in [
        "staged/assets/identity/created.json",
        "backup/assets/identity/replaced.json",
        "journal.pending",
    ] {
        let root = TempDir::new().unwrap();
        let mut store = LocalArtifactStore::new(root.path()).unwrap();
        let destination = store.transaction_directory(&"a".repeat(64)).join(relative);
        fs::create_dir_all(destination.parent().unwrap()).unwrap();
        let status = std::process::Command::new("mkfifo")
            .arg(&destination)
            .status()
            .unwrap();
        assert!(status.success());
        let before = tree(root.path());
        assert!(store.checked_transaction_path(&destination).is_err());
        assert!(store.recover().is_err());
        assert_only_writer_lock_created(root.path(), before);
    }
}

#[cfg(windows)]
#[test]
fn windows_junction_cache_components_are_rejected_without_redirected_writes() {
    for relative in [
        ".cache".to_owned(),
        ".cache/identity".to_owned(),
        TRANSACTION_ROOT.to_owned(),
        format!("{TRANSACTION_ROOT}/{}", "a".repeat(64)),
    ] {
        let root = TempDir::new().unwrap();
        let external = TempDir::new().unwrap();
        let (plan, artifacts, manifest) = fixture(root.path(), OUTPUT);
        write_fixture(&external.path().join("sentinel"), b"external sentinel").unwrap();
        let junction = append_portable(root.path(), &relative);
        fs::create_dir_all(junction.parent().unwrap()).unwrap();
        let result = std::process::Command::new("cmd")
            .args(["/C", "mklink", "/J"])
            .arg(&junction)
            .arg(external.path())
            .output()
            .unwrap();
        assert!(
            result.status.success(),
            "{}",
            String::from_utf8_lossy(&result.stderr)
        );
        let before = tree(root.path());
        let external_before = tree(external.path());
        let mut store = LocalArtifactStore::new(root.path()).unwrap();
        assert!(store.inspect_recovery().is_err());
        assert_eq!(tree(root.path()), before, "inspection {relative}");
        assert_eq!(
            tree(external.path()),
            external_before,
            "inspection {relative}"
        );
        assert!(store.commit(&plan, &artifacts, &manifest).is_err());
        assert!(store.recover().is_err());
        if relative.starts_with(&format!("{TRANSACTION_ROOT}/")) {
            assert_only_writer_lock_created(root.path(), before);
        } else {
            assert_eq!(tree(root.path()), before, "{relative}");
        }
        assert_eq!(tree(external.path()), external_before, "{relative}");
    }
}

#[cfg(windows)]
#[test]
fn windows_junction_recovery_paths_preserve_outputs_and_external_evidence() {
    for location in [
        "cache",
        "cache-identity",
        "transaction-root",
        "workspace",
        "staged",
        "staged/assets",
        "backup",
        "backup/assets",
    ] {
        let root = TempDir::new().unwrap();
        let external = TempDir::new().unwrap();
        let transaction = interrupted(root.path(), OUTPUT, 4);
        let source = match location {
            "cache" => root.path().join(".cache"),
            "cache-identity" => append_portable(root.path(), ".cache/identity"),
            "transaction-root" => append_portable(root.path(), TRANSACTION_ROOT),
            "workspace" => transaction,
            relative => append_portable(&transaction, relative),
        };
        let target = external.path().join("relocated-evidence");
        fs::rename(&source, &target).unwrap();
        let result = std::process::Command::new("cmd")
            .args(["/C", "mklink", "/J"])
            .arg(&source)
            .arg(&target)
            .output()
            .unwrap();
        assert!(
            result.status.success(),
            "{}",
            String::from_utf8_lossy(&result.stderr)
        );
        let external_before = tree(external.path());
        assert_blocked_without_mutation(root.path());
        assert_eq!(tree(external.path()), external_before, "{location}");
    }
}
