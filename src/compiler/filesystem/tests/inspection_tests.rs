// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

use super::*;

#[test]
fn clean_inspection_never_creates_coordination_metadata_or_requires_source() {
    let root = TempDir::new().unwrap();
    write_fixture(&root.path().join("notes/sentinel"), b"unrelated bytes").unwrap();
    let before = tree(root.path());
    let inspection = LocalArtifactStore::new(root.path())
        .unwrap()
        .inspect_recovery()
        .unwrap();
    assert!(!inspection.coordinated);
    assert!(inspection.workspaces.is_empty());
    assert_eq!(tree(root.path()), before);
    assert!(!root.path().join(".cache").exists());
}

#[test]
fn inspection_opens_an_existing_read_only_lock_without_changing_its_bytes() {
    let root = TempDir::new().unwrap();
    let lock = root.path().join(WRITER_LOCK);
    write_fixture(&lock, b"existing coordination evidence").unwrap();
    let original = lock.metadata().unwrap().permissions();
    let mut read_only = original.clone();
    read_only.set_readonly(true);
    fs::set_permissions(&lock, read_only).unwrap();
    let before = tree(root.path());
    let inspection = LocalArtifactStore::new(root.path())
        .unwrap()
        .inspect_recovery()
        .unwrap();
    assert!(inspection.coordinated);
    assert!(inspection.workspaces.is_empty());
    assert_eq!(tree(root.path()), before);
    fs::set_permissions(lock, original).unwrap();
}

#[test]
fn inspection_previews_complete_rollback_without_restoring_or_removing_any_file() {
    let root = TempDir::new().unwrap();
    let transaction = interrupted(root.path(), OUTPUT, 4);
    write_fixture(&root.path().join(".identity/sentinel"), b"canonical bytes").unwrap();
    write_fixture(&root.path().join("notes/sentinel"), b"unrelated bytes").unwrap();
    let before = tree(root.path());
    let mut store = LocalArtifactStore::new(root.path()).unwrap();
    let inspection = store.inspect_recovery().unwrap();
    assert!(inspection.coordinated);
    assert_eq!(inspection.workspaces.len(), 1);
    let workspace = &inspection.workspaces[0];
    assert_eq!(
        workspace.workspace,
        transaction.file_name().unwrap().to_str().unwrap()
    );
    assert_eq!(
        workspace.plan_digest.as_deref(),
        Some(workspace.workspace.as_str())
    );
    let actions = workspace
        .actions
        .iter()
        .map(|action| (action.path.clone(), action.operation))
        .collect::<BTreeMap<_, _>>();
    assert_eq!(
        actions,
        BTreeMap::from([
            (format!("{OUTPUT}/created.json"), RecoveryOperation::Remove),
            (
                format!("{OUTPUT}/replaced.json"),
                RecoveryOperation::Restore
            ),
            (format!("{OUTPUT}/removed.json"), RecoveryOperation::Restore),
            (
                format!("{OUTPUT}/.identity-manifest.json"),
                RecoveryOperation::Restore
            ),
        ])
    );
    assert_eq!(tree(root.path()), before);
    assert_eq!(store.recover().unwrap().recovered_transactions, 1);
    assert_eq!(
        fs::read(root.path().join(".identity/sentinel")).unwrap(),
        b"canonical bytes"
    );
    assert_eq!(
        fs::read(root.path().join("notes/sentinel")).unwrap(),
        b"unrelated bytes"
    );
    assert!(store.inspect_recovery().unwrap().workspaces.is_empty());
}

#[test]
fn a_legacy_missing_lock_remains_an_uncoordinated_nonmutating_observation() {
    let root = TempDir::new().unwrap();
    interrupted(root.path(), OUTPUT, 2);
    fs::remove_file(root.path().join(WRITER_LOCK)).unwrap();
    let before = tree(root.path());
    let inspection = LocalArtifactStore::new(root.path())
        .unwrap()
        .inspect_recovery()
        .unwrap();
    assert!(!inspection.coordinated);
    assert_eq!(inspection.workspaces.len(), 1);
    assert!(inspection.workspaces[0].plan_digest.is_some());
    assert_eq!(tree(root.path()), before);
    assert!(!root.path().join(WRITER_LOCK).exists());
}

#[test]
fn inspection_preserves_empty_orphans_until_explicit_recovery() {
    let root = TempDir::new().unwrap();
    let orphan = root.path().join(TRANSACTION_ROOT).join("0".repeat(64));
    fs::create_dir_all(&orphan).unwrap();
    let before = tree(root.path());
    let mut store = LocalArtifactStore::new(root.path()).unwrap();
    let inspection = store.inspect_recovery().unwrap();
    assert!(!inspection.coordinated);
    assert_eq!(inspection.workspaces.len(), 1);
    assert!(inspection.workspaces[0].plan_digest.is_none());
    assert!(inspection.workspaces[0].actions.is_empty());
    assert_eq!(tree(root.path()), before);
    assert_eq!(store.recover().unwrap().recovered_transactions, 0);
    assert!(!orphan.exists());
}

#[test]
fn inspection_and_recovery_share_complete_validation_and_preserve_rejected_evidence() {
    for case in 0..5 {
        let root = TempDir::new().unwrap();
        let transaction = interrupted(root.path(), OUTPUT, 4);
        let orphan = root.path().join(TRANSACTION_ROOT).join("0".repeat(64));
        fs::create_dir_all(&orphan).unwrap();
        match case {
            0 => fs::remove_file(transaction.join("journal.json")).unwrap(),
            1 => fs::write(transaction.join("journal.json"), b"{").unwrap(),
            2 => fs::write(
                transaction
                    .join("backup")
                    .join(OUTPUT)
                    .join("replaced.json"),
                b"untrusted backup",
            )
            .unwrap(),
            3 => fs::write(
                root.path().join(OUTPUT).join("replaced.json"),
                b"unrelated edit",
            )
            .unwrap(),
            4 => {
                let mut value: serde_json::Value =
                    serde_json::from_slice(&fs::read(transaction.join("journal.json")).unwrap())
                        .unwrap();
                value["schema"] = "identity.compiler-transaction/v1".into();
                fs::write(
                    transaction.join("journal.json"),
                    serde_json::to_vec(&value).unwrap(),
                )
                .unwrap();
            }
            _ => unreachable!(),
        }
        let before = tree(root.path());
        let mut store = LocalArtifactStore::new(root.path()).unwrap();
        let inspection = store.inspect_recovery().unwrap_err();
        assert_eq!(tree(root.path()), before, "inspection case {case}");
        let recovery = store.recover().unwrap_err();
        assert_eq!(inspection.kind, recovery.kind);
        assert_eq!(inspection.diagnostics[0].code, recovery.diagnostics[0].code);
        assert_eq!(tree(root.path()), before, "recovery case {case}");
        assert!(orphan.exists());
    }
}

#[test]
fn inspection_uses_the_callers_output_scope_instead_of_journal_authority() {
    let root = TempDir::new().unwrap();
    interrupted(root.path(), "generated/branding", 2);
    let before = tree(root.path());
    assert!(
        LocalArtifactStore::new(root.path())
            .unwrap()
            .inspect_recovery()
            .is_err()
    );
    let inspection = LocalArtifactStore::with_output_root(root.path(), "generated/branding")
        .unwrap()
        .inspect_recovery()
        .unwrap();
    assert_eq!(inspection.workspaces.len(), 1);
    assert!(
        inspection.workspaces[0]
            .actions
            .iter()
            .all(|action| action.path.starts_with("generated/branding/"))
    );
    assert_eq!(tree(root.path()), before);
}

#[test]
fn shared_inspection_ownership_excludes_writers_and_allows_other_inspectors() {
    let root = TempDir::new().unwrap();
    let (plan, artifacts, manifest) = fixture(root.path(), OUTPUT);
    write_fixture(&root.path().join(WRITER_LOCK), b"persistent bytes").unwrap();
    let mut store = LocalArtifactStore::new(root.path()).unwrap();
    let guard = store.try_inspection_lock().unwrap().unwrap();
    let before = tree_with_writer_lock_metadata(root.path(), true);
    assert!(store.inspect_recovery().unwrap().coordinated);
    for error in [
        store.commit(&plan, &artifacts, &manifest).unwrap_err(),
        store.recover().unwrap_err(),
    ] {
        assert_eq!(error.kind, FailureKind::Blocked);
        assert_eq!(error.diagnostics[0].code, "IDN2346");
    }
    assert_eq!(tree_with_writer_lock_metadata(root.path(), true), before);
    drop(guard);
    store.commit(&plan, &artifacts, &manifest).unwrap();
    assert_eq!(
        fs::read(root.path().join(WRITER_LOCK)).unwrap(),
        b"persistent bytes"
    );
}

#[test]
fn an_active_writer_blocks_inspection_without_repair_or_metadata_changes() {
    let root = TempDir::new().unwrap();
    let store = LocalArtifactStore::new(root.path()).unwrap();
    let guard = store.acquire_writer_lock().unwrap();
    let before = tree_with_writer_lock_metadata(root.path(), true);
    let error = store.inspect_recovery().unwrap_err();
    assert_eq!(error.kind, FailureKind::Blocked);
    assert_eq!(error.diagnostics[0].code, "IDN2346");
    assert_eq!(tree_with_writer_lock_metadata(root.path(), true), before);
    drop(guard);
    assert!(store.inspect_recovery().unwrap().coordinated);
}

// This worker uses the actual v1 source bridge and production adapters. The
// parent pauses it after the first promotion, kills/reaps it, then invokes the
// separately built shipping CLI against its original journal and canonical tree.
#[test]
#[ignore = "actual consumer interruption worker; explicitly invoked by the bounded CLI proof"]
fn interrupted_consumer_worker() {
    use crate::brandkit::{compiler_request, register_builtin_adapters};
    use crate::compiler::{AdapterRegistry, Compiler};
    use crate::reference_renderer::{register_reference_renderer_adapter, with_reference_renderer};
    use crate::v1_consumer::V1ConsumerPipeline;

    let root = PathBuf::from(std::env::var_os("IDENTITY_RECOVERY_TEST_ROOT").unwrap());
    let output_root =
        std::env::var("IDENTITY_RECOVERY_TEST_OUTPUT_ROOT").unwrap_or_else(|_| OUTPUT.to_owned());
    let pipeline = V1ConsumerPipeline::load(&root).unwrap();
    let request = with_reference_renderer(
        compiler_request(output_root.clone(), pipeline.profiles()).unwrap(),
    );
    let mut registry = AdapterRegistry::new();
    register_builtin_adapters(&mut registry).unwrap();
    register_reference_renderer_adapter(&mut registry).unwrap();
    let mut store = LocalArtifactStore::with_output_root(&root, &output_root)
        .unwrap()
        .pause_at(TestCheckpoint::Mutation(1));
    let mut compiler = Compiler::new(&pipeline, &pipeline, &pipeline, &registry, &mut store);
    let prepared = compiler.prepare(request).unwrap();
    compiler.execute(&prepared, &BTreeSet::new()).unwrap();
}
