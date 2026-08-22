// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

use std::collections::BTreeMap;
use std::fs;
use std::io::ErrorKind;
use std::path::{Path, PathBuf};

use serde::{Deserialize, Serialize};

use super::{
    ArtifactStore, CompilerError, CompilerManifest, CompilerPlan, CompilerResult, Diagnostic,
    FailureKind, PlanActionScope, PlanOperation, RecoveryReport, RenderedArtifact, manifest_bytes,
    sha256_hex, validate_portable_path,
};

const TRANSACTION_SCHEMA: &str = "identity.compiler-transaction/v1";
const TRANSACTION_ROOT: &str = ".cache/identity/transactions";

#[derive(Debug)]
pub struct LocalArtifactStore {
    repository_root: PathBuf,
    fail_after_mutations: Option<usize>,
    completed_mutations: usize,
}

impl LocalArtifactStore {
    pub fn new(repository_root: impl AsRef<Path>) -> CompilerResult<Self> {
        let repository_root = repository_root.as_ref().canonicalize().map_err(|error| {
            fs_error(
                "IDN2310",
                None,
                format!("cannot resolve repository root: {error}"),
                "Use an existing repository directory for the local artifact store.",
            )
        })?;
        Ok(Self {
            repository_root,
            fail_after_mutations: None,
            completed_mutations: 0,
        })
    }

    #[cfg(test)]
    pub(crate) fn fail_after_mutations(mut self, mutations: usize) -> Self {
        self.fail_after_mutations = Some(mutations);
        self
    }

    fn transaction_root(&self) -> PathBuf {
        self.repository_root.join(TRANSACTION_ROOT)
    }

    fn transaction_directory(&self, plan_digest: &str) -> PathBuf {
        self.transaction_root().join(plan_digest)
    }

    fn resolve(&self, relative_path: &str) -> CompilerResult<PathBuf> {
        validate_portable_path(relative_path, "artifact path")?;
        let mut current = self.repository_root.clone();
        for segment in relative_path.split('/') {
            current.push(segment);
            if current
                .symlink_metadata()
                .is_ok_and(|metadata| metadata.file_type().is_symlink())
            {
                return Err(fs_error(
                    "IDN2311",
                    Some(relative_path.to_owned()),
                    "artifact path traverses a symbolic link",
                    "Use a real repository-relative directory tree for generated artifacts.",
                ));
            }
        }
        Ok(current)
    }

    fn staged_path(transaction: &Path, relative_path: &str) -> PathBuf {
        append_portable(&transaction.join("staged"), relative_path)
    }

    fn backup_path(transaction: &Path, relative_path: &str) -> PathBuf {
        append_portable(&transaction.join("backup"), relative_path)
    }

    fn journal_path(transaction: &Path) -> PathBuf {
        transaction.join("journal.json")
    }

    fn write_bytes(path: &Path, bytes: &[u8]) -> CompilerResult<()> {
        if let Some(parent) = path.parent() {
            fs::create_dir_all(parent).map_err(|error| {
                fs_error(
                    "IDN2312",
                    Some(parent.display().to_string()),
                    format!("cannot create transaction directory: {error}"),
                    "Check local filesystem permissions and retry.",
                )
            })?;
        }
        fs::write(path, bytes).map_err(|error| {
            fs_error(
                "IDN2313",
                Some(path.display().to_string()),
                format!("cannot write transaction file: {error}"),
                "Check local filesystem permissions and retry.",
            )
        })
    }

    fn copy_file(source: &Path, destination: &Path) -> CompilerResult<()> {
        if let Some(parent) = destination.parent() {
            fs::create_dir_all(parent).map_err(|error| {
                fs_error(
                    "IDN2314",
                    Some(parent.display().to_string()),
                    format!("cannot create backup directory: {error}"),
                    "Check local filesystem permissions and retry.",
                )
            })?;
        }
        fs::copy(source, destination).map_err(|error| {
            fs_error(
                "IDN2315",
                Some(source.display().to_string()),
                format!("cannot copy generated artifact: {error}"),
                "Check local filesystem permissions and retry before mutation.",
            )
        })?;
        Ok(())
    }

    fn remove_file_if_present(path: &Path) -> CompilerResult<()> {
        match fs::remove_file(path) {
            Ok(()) => Ok(()),
            Err(error) if error.kind() == ErrorKind::NotFound => Ok(()),
            Err(error) => Err(fs_error(
                "IDN2318",
                Some(path.display().to_string()),
                format!("cannot remove generated artifact: {error}"),
                "Check local filesystem permissions and recover the transaction if necessary.",
            )),
        }
    }

    fn promote(&mut self, staged: &Path, destination: &Path) -> CompilerResult<()> {
        if let Some(parent) = destination.parent() {
            fs::create_dir_all(parent).map_err(|error| {
                fs_error(
                    "IDN2319",
                    Some(parent.display().to_string()),
                    format!("cannot create generated output directory: {error}"),
                    "Check local filesystem permissions and recover if necessary.",
                )
            })?;
        }
        Self::remove_file_if_present(destination)?;
        fs::rename(staged, destination).map_err(|error| {
            fs_error(
                "IDN2320",
                Some(destination.display().to_string()),
                format!("cannot promote staged artifact: {error}"),
                "Run recovery to restore the previous generated state, then retry.",
            )
        })?;
        self.after_mutation()
    }

    fn after_mutation(&mut self) -> CompilerResult<()> {
        self.completed_mutations += 1;
        if self.fail_after_mutations == Some(self.completed_mutations) {
            return Err(fs_error(
                "IDN2399",
                None,
                "simulated interruption after filesystem mutation",
                "Create a fresh local artifact store and run explicit recovery.",
            ));
        }
        Ok(())
    }

    fn verify_current(&self, action: &super::PlanAction) -> CompilerResult<()> {
        let destination = self.resolve(&action.path)?;
        let current = match fs::read(destination) {
            Ok(bytes) => Some(sha256_hex(&bytes)),
            Err(error) if error.kind() == ErrorKind::NotFound => None,
            Err(error) => {
                return Err(fs_error(
                    "IDN2321",
                    Some(action.path.clone()),
                    format!("cannot inspect planned artifact before apply: {error}"),
                    "Discard the stale plan and create a new plan.",
                ));
            }
        };
        if current != action.current_sha256 {
            return Err(CompilerError::new(
                FailureKind::Drifted,
                Diagnostic::error(
                    "IDN2308",
                    FailureKind::Drifted,
                    Some(action.path.clone()),
                    "generated state changed after the plan was created",
                    "Discard the stale plan and create a new mutation-free plan.",
                ),
            ));
        }
        Ok(())
    }

    fn recover_transaction(&mut self, transaction: &Path) -> CompilerResult<Option<String>> {
        let journal_path = Self::journal_path(transaction);
        let bytes = match fs::read(&journal_path) {
            Ok(bytes) => bytes,
            Err(error) if error.kind() == ErrorKind::NotFound => {
                fs::remove_dir_all(transaction).map_err(|remove_error| {
                    fs_error(
                        "IDN2322",
                        Some(transaction.display().to_string()),
                        format!("cannot remove orphan transaction workspace: {remove_error}"),
                        "Remove the orphan transaction directory manually.",
                    )
                })?;
                return Ok(None);
            }
            Err(error) => {
                return Err(fs_error(
                    "IDN2323",
                    Some(journal_path.display().to_string()),
                    format!("cannot read transaction journal: {error}"),
                    "Restore access to the journal before recovery.",
                ));
            }
        };
        let journal: TransactionJournal = serde_json::from_slice(&bytes).map_err(|error| {
            fs_error(
                "IDN2324",
                Some(journal_path.display().to_string()),
                format!("cannot parse transaction journal: {error}"),
                "Restore the journal from trusted evidence before recovery.",
            )
        })?;
        if journal.schema != TRANSACTION_SCHEMA {
            return Err(CompilerError::new(
                FailureKind::Unsupported,
                Diagnostic::error(
                    "IDN2325",
                    FailureKind::Unsupported,
                    Some(journal_path.display().to_string()),
                    format!("unsupported transaction schema {:?}", journal.schema),
                    "Use a compatible Identity version to recover this transaction.",
                ),
            ));
        }

        for action in journal.actions.iter().rev() {
            let destination = self.resolve(&action.path)?;
            match action.operation {
                PlanOperation::Create => Self::remove_file_if_present(&destination)?,
                PlanOperation::Replace | PlanOperation::Remove => {
                    let backup = Self::backup_path(transaction, &action.path);
                    if !backup.is_file() {
                        return Err(fs_error(
                            "IDN2326",
                            Some(action.path.clone()),
                            "transaction backup is missing",
                            "Restore the backup from trusted evidence before recovery.",
                        ));
                    }
                    Self::remove_file_if_present(&destination)?;
                    Self::copy_file(&backup, &destination)?;
                }
                PlanOperation::Unchanged | PlanOperation::Blocked => {}
            }
        }

        let manifest_destination = self.resolve(&journal.manifest_path)?;
        if journal.manifest_existed {
            let backup = Self::backup_path(transaction, &journal.manifest_path);
            Self::remove_file_if_present(&manifest_destination)?;
            Self::copy_file(&backup, &manifest_destination)?;
        } else {
            Self::remove_file_if_present(&manifest_destination)?;
        }

        fs::remove_dir_all(transaction).map_err(|error| {
            fs_error(
                "IDN2327",
                Some(transaction.display().to_string()),
                format!("cannot remove recovered transaction workspace: {error}"),
                "Remove the recovered transaction directory manually before continuing.",
            )
        })?;
        Ok(Some(journal.plan_digest))
    }
}

impl ArtifactStore for LocalArtifactStore {
    fn read(&self, relative_path: &str) -> CompilerResult<Option<Vec<u8>>> {
        let path = self.resolve(relative_path)?;
        match fs::read(path) {
            Ok(bytes) => Ok(Some(bytes)),
            Err(error) if error.kind() == ErrorKind::NotFound => Ok(None),
            Err(error) => Err(fs_error(
                "IDN2330",
                Some(relative_path.to_owned()),
                format!("cannot read generated artifact: {error}"),
                "Check local filesystem permissions and retry.",
            )),
        }
    }

    fn recovery_required(&self) -> CompilerResult<bool> {
        match fs::read_dir(self.transaction_root()) {
            Ok(mut entries) => Ok(entries.next().is_some()),
            Err(error) if error.kind() == ErrorKind::NotFound => Ok(false),
            Err(error) => Err(fs_error(
                "IDN2331",
                Some(self.transaction_root().display().to_string()),
                format!("cannot inspect transaction workspace: {error}"),
                "Check local filesystem permissions before compiler operations.",
            )),
        }
    }

    // Transaction apply stays linear so write authority and recovery order remain auditable.
    #[allow(clippy::too_many_lines)]
    fn commit(
        &mut self,
        plan: &CompilerPlan,
        artifacts: &[RenderedArtifact],
        manifest: &CompilerManifest,
    ) -> CompilerResult<()> {
        if self.recovery_required()? {
            return Err(CompilerError::new(
                FailureKind::Blocked,
                Diagnostic::error(
                    "IDN2301",
                    FailureKind::Blocked,
                    None,
                    "a previous compiler transaction requires recovery",
                    "Run explicit recovery before applying another plan.",
                ),
            ));
        }

        let artifacts_by_path = artifacts
            .iter()
            .map(|artifact| (artifact.path.as_str(), artifact))
            .collect::<BTreeMap<_, _>>();
        for action in plan
            .actions
            .iter()
            .filter(|action| action.scope == PlanActionScope::Artifact)
        {
            self.verify_current(action)?;
            if matches!(
                action.operation,
                PlanOperation::Create | PlanOperation::Replace
            ) && !artifacts_by_path.contains_key(action.path.as_str())
            {
                return Err(fs_error(
                    "IDN2336",
                    Some(action.path.clone()),
                    "planned write has no verified staged artifact",
                    "Render and verify every write before entering the transaction boundary.",
                ));
            }
            if action.operation == PlanOperation::Blocked {
                return Err(CompilerError::new(
                    FailureKind::Blocked,
                    Diagnostic::error(
                        "IDN2337",
                        FailureKind::Blocked,
                        Some(action.path.clone()),
                        "blocked plan action reached the transaction boundary",
                        "Resolve the blocking diagnostic and create a new plan.",
                    ),
                ));
            }
        }

        if !plan.has_mutations() {
            verify_manifested_outputs(self, manifest)?;
            return Ok(());
        }

        let transaction = self.transaction_directory(&plan.plan_digest);
        fs::create_dir_all(&transaction).map_err(|error| {
            fs_error(
                "IDN2338",
                Some(transaction.display().to_string()),
                format!("cannot create compiler transaction workspace: {error}"),
                "Check local filesystem permissions before applying the plan.",
            )
        })?;

        for artifact in artifacts {
            Self::write_bytes(
                &Self::staged_path(&transaction, &artifact.path),
                &artifact.bytes,
            )?;
        }
        let staged_manifest = Self::staged_path(&transaction, &plan.manifest_path);
        Self::write_bytes(&staged_manifest, &manifest_bytes(manifest)?)?;

        let mut journal_actions = Vec::new();
        for action in plan.actions.iter().filter(|action| {
            action.scope == PlanActionScope::Artifact
                && matches!(
                    action.operation,
                    PlanOperation::Create | PlanOperation::Replace | PlanOperation::Remove
                )
        }) {
            let destination = self.resolve(&action.path)?;
            if matches!(
                action.operation,
                PlanOperation::Replace | PlanOperation::Remove
            ) {
                if !destination.is_file() {
                    return Err(fs_error(
                        "IDN2339",
                        Some(action.path.clone()),
                        "planned replacement or removal disappeared before backup",
                        "Discard the stale plan and re-plan from current generated state.",
                    ));
                }
                Self::copy_file(&destination, &Self::backup_path(&transaction, &action.path))?;
            }
            journal_actions.push(TransactionAction {
                path: action.path.clone(),
                operation: action.operation,
            });
        }

        let manifest_destination = self.resolve(&plan.manifest_path)?;
        let manifest_existed = manifest_destination.is_file();
        if manifest_existed {
            Self::copy_file(
                &manifest_destination,
                &Self::backup_path(&transaction, &plan.manifest_path),
            )?;
        }
        let journal = TransactionJournal {
            schema: TRANSACTION_SCHEMA.to_owned(),
            plan_digest: plan.plan_digest.clone(),
            manifest_path: plan.manifest_path.clone(),
            manifest_existed,
            actions: journal_actions,
        };
        let mut journal_bytes = serde_json::to_vec_pretty(&journal).map_err(|error| {
            fs_error(
                "IDN2340",
                None,
                format!("cannot serialize transaction journal: {error}"),
                "Report the transaction serialization failure.",
            )
        })?;
        journal_bytes.push(b'\n');
        Self::write_bytes(&Self::journal_path(&transaction), &journal_bytes)?;

        for action in plan
            .actions
            .iter()
            .filter(|action| action.scope == PlanActionScope::Artifact)
        {
            let destination = self.resolve(&action.path)?;
            match action.operation {
                PlanOperation::Create | PlanOperation::Replace => {
                    self.promote(&Self::staged_path(&transaction, &action.path), &destination)?;
                }
                PlanOperation::Remove => {
                    Self::remove_file_if_present(&destination)?;
                    self.after_mutation()?;
                }
                PlanOperation::Unchanged => {}
                PlanOperation::Blocked => {
                    unreachable!("blocked actions are rejected before mutation")
                }
            }
        }
        self.promote(&staged_manifest, &manifest_destination)?;
        verify_manifested_outputs(self, manifest)?;

        fs::remove_dir_all(&transaction).map_err(|error| {
            fs_error(
                "IDN2341",
                Some(transaction.display().to_string()),
                format!("commit succeeded but transaction cleanup failed: {error}"),
                "Remove the completed transaction workspace before the next compiler operation.",
            )
        })?;
        Ok(())
    }

    fn recover(&mut self) -> CompilerResult<RecoveryReport> {
        let root = self.transaction_root();
        let entries = match fs::read_dir(&root) {
            Ok(entries) => entries,
            Err(error) if error.kind() == ErrorKind::NotFound => {
                return Ok(RecoveryReport::default());
            }
            Err(error) => {
                return Err(fs_error(
                    "IDN2342",
                    Some(root.display().to_string()),
                    format!("cannot list compiler transactions: {error}"),
                    "Check local filesystem permissions and retry recovery.",
                ));
            }
        };
        let mut directories = entries
            .map(|entry| entry.map(|value| value.path()))
            .collect::<Result<Vec<_>, _>>()
            .map_err(|error| {
                fs_error(
                    "IDN2343",
                    Some(root.display().to_string()),
                    format!("cannot enumerate compiler transactions: {error}"),
                    "Check local filesystem permissions and retry recovery.",
                )
            })?;
        directories.sort();

        let mut report = RecoveryReport::default();
        for directory in directories {
            if !directory.is_dir() {
                continue;
            }
            if let Some(plan_digest) = self.recover_transaction(&directory)? {
                report.recovered_transactions += 1;
                report.plan_digests.push(plan_digest);
            }
        }
        Ok(report)
    }
}

#[derive(Clone, Debug, Deserialize, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
struct TransactionJournal {
    schema: String,
    plan_digest: String,
    manifest_path: String,
    manifest_existed: bool,
    actions: Vec<TransactionAction>,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
struct TransactionAction {
    path: String,
    operation: PlanOperation,
}

fn append_portable(root: &Path, relative_path: &str) -> PathBuf {
    relative_path
        .split('/')
        .fold(root.to_path_buf(), |path, segment| path.join(segment))
}

fn verify_manifested_outputs(
    store: &LocalArtifactStore,
    manifest: &CompilerManifest,
) -> CompilerResult<()> {
    for output in &manifest.outputs {
        let bytes = store.read(&output.path)?.ok_or_else(|| {
            fs_error(
                "IDN2344",
                Some(output.path.clone()),
                "verified manifest output is missing after commit",
                "Run recovery if pending, then rebuild the generated output.",
            )
        })?;
        if sha256_hex(&bytes) != output.sha256 {
            return Err(CompilerError::new(
                FailureKind::Drifted,
                Diagnostic::error(
                    "IDN2345",
                    FailureKind::Drifted,
                    Some(output.path.clone()),
                    "generated output checksum differs from the compiler manifest",
                    "Run recovery if pending, then rebuild from canonical source.",
                ),
            ));
        }
    }
    Ok(())
}

fn fs_error(
    code: &str,
    path: Option<String>,
    message: impl Into<String>,
    recovery: impl Into<String>,
) -> CompilerError {
    CompilerError::new(
        FailureKind::Failed,
        Diagnostic::error(code, FailureKind::Failed, path, message, recovery),
    )
}
