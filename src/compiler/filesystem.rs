// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

#[cfg(test)]
mod tests;

use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::io::ErrorKind;
use std::path::{Path, PathBuf};

use serde::{Deserialize, Serialize};

use super::{
    ArtifactStore, CompilerError, CompilerManifest, CompilerPlan, CompilerResult, Diagnostic,
    FailureKind, PlanActionScope, PlanOperation, RecoveryReport, RenderedArtifact, manifest_bytes,
    sha256_hex, validate_portable_path,
};

const TRANSACTION_SCHEMA: &str = "identity.compiler-transaction/v2";
const TRANSACTION_ROOT: &str = ".cache/identity/transactions";

#[derive(Debug)]
pub struct LocalArtifactStore {
    repository_root: PathBuf,
    output_root: String,
    fail_after_mutations: Option<usize>,
    completed_mutations: usize,
}

impl LocalArtifactStore {
    /// Authorize generated-state writes and recovery beneath assets/identity.
    pub fn new(repository_root: impl AsRef<Path>) -> CompilerResult<Self> {
        Self::with_output_root(repository_root, "assets/identity")
    }

    /// Explicitly authorize a custom generated root independently of any journal.
    pub fn with_output_root(
        repository_root: impl AsRef<Path>,
        output_root: &str,
    ) -> CompilerResult<Self> {
        validate_portable_path(output_root, "authorized output root")?;
        if output_root.split('/').next().is_some_and(|part| {
            matches!(
                part.to_ascii_lowercase().as_str(),
                ".identity" | ".cache" | ".git"
            )
        }) {
            return Err(recovery_error(
                "output root overlaps canonical source, cache, or repository metadata",
            ));
        }
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
            output_root: output_root.to_owned(),
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

    fn validate_plan(&self, plan: &CompilerPlan) -> CompilerResult<()> {
        if plan.schema != super::COMPILER_PLAN_SCHEMA
            || plan.project_id.trim().is_empty()
            || !super::valid_sha256(&plan.source_digest)
            || !super::valid_sha256(&plan.plan_digest)
            || plan.plan_digest != super::plan_digest(plan)?
            || plan.output_root != self.output_root
            || plan.manifest_path != format!("{}/{}", self.output_root, super::MANIFEST_FILE_NAME)
            || plan.has_blocking_diagnostics()
        {
            return Err(recovery_error(
                "plan identity or output authority is invalid",
            ));
        }
        let mut paths = BTreeSet::new();
        let mut manifests = 0;
        for action in &plan.actions {
            self.resolve(&action.path)?;
            if !action.path.starts_with(&format!("{}/", self.output_root)) {
                return Err(recovery_error(
                    "action is outside the authorized output root",
                ));
            }
            let normalized = action.path.to_ascii_lowercase();
            if paths.iter().any(|path: &String| {
                *path == normalized
                    || path.starts_with(&format!("{normalized}/"))
                    || normalized.starts_with(&format!("{path}/"))
            }) {
                return Err(recovery_error(
                    "duplicate, aliased, or conflicting action paths",
                ));
            }
            paths.insert(normalized);
            if action.scope == PlanActionScope::Manifest {
                manifests += 1;
                if action.path != plan.manifest_path
                    || (plan.has_mutations() && action.operation == PlanOperation::Unchanged)
                    || !matches!(
                        action.operation,
                        PlanOperation::Create | PlanOperation::Replace | PlanOperation::Unchanged
                    )
                {
                    return Err(recovery_error("invalid manifest action"));
                }
            } else if action.path.eq_ignore_ascii_case(&plan.manifest_path) {
                return Err(recovery_error("artifact action targets the manifest"));
            }
            let has_current = action.current_sha256.is_some();
            if action
                .current_sha256
                .as_ref()
                .is_some_and(|digest| !super::valid_sha256(digest))
                || has_current != action.current_bytes.is_some()
                || match action.operation {
                    PlanOperation::Create => has_current,
                    PlanOperation::Replace | PlanOperation::Remove | PlanOperation::Unchanged => {
                        !has_current
                    }
                    PlanOperation::Blocked => true,
                }
            {
                return Err(recovery_error(
                    "action operation disagrees with its current-file evidence",
                ));
            }
        }
        if manifests != 1 {
            return Err(recovery_error(
                "plan must contain exactly one manifest action",
            ));
        }
        Ok(())
    }

    fn validate_artifacts(
        plan: &CompilerPlan,
        artifacts: &[RenderedArtifact],
        manifest: &CompilerManifest,
    ) -> CompilerResult<()> {
        if manifest.schema != super::COMPILER_MANIFEST_SCHEMA
            || manifest.project_id != plan.project_id
            || manifest.source_digest != plan.source_digest
            || (plan.has_mutations() && manifest.plan_digest != plan.plan_digest)
        {
            return Err(recovery_error(
                "manifest identity differs from the accepted plan",
            ));
        }
        let writes = plan
            .actions
            .iter()
            .filter(|action| {
                action.scope == PlanActionScope::Artifact
                    && matches!(
                        action.operation,
                        PlanOperation::Create | PlanOperation::Replace
                    )
            })
            .collect::<Vec<_>>();
        let mut seen = BTreeSet::new();
        if artifacts.len() != writes.len() {
            return Err(recovery_error("staged writes do not match the plan"));
        }
        for artifact in artifacts {
            if !seen.insert(&artifact.path)
                || !writes.iter().any(|action| {
                    action.path == artifact.path && action.target_id == artifact.target_id
                })
            {
                return Err(recovery_error("unexpected or duplicate staged artifact"));
            }
        }
        let outputs = plan
            .actions
            .iter()
            .filter(|action| {
                action.scope == PlanActionScope::Artifact
                    && action.operation != PlanOperation::Remove
            })
            .collect::<Vec<_>>();
        if outputs.len() != manifest.outputs.len() {
            return Err(recovery_error("manifest outputs do not match the plan"));
        }
        seen.clear();
        for output in &manifest.outputs {
            let action = outputs
                .iter()
                .find(|action| action.path == output.path && action.target_id == output.target_id)
                .ok_or_else(|| recovery_error("manifest output is absent from the plan"))?;
            if !seen.insert(&output.path) {
                return Err(recovery_error("duplicate manifest output"));
            }
            let (digest, bytes) =
                if let Some(artifact) = artifacts.iter().find(|value| value.path == output.path) {
                    (
                        sha256_hex(&artifact.bytes),
                        super::byte_len(&artifact.bytes)?,
                    )
                } else {
                    (
                        action
                            .current_sha256
                            .clone()
                            .ok_or_else(|| recovery_error("unchanged output lacks a digest"))?,
                        action
                            .current_bytes
                            .ok_or_else(|| recovery_error("unchanged output lacks a size"))?,
                    )
                };
            if output.sha256 != digest || output.bytes != bytes {
                return Err(recovery_error(
                    "manifest evidence differs from the verified output",
                ));
            }
        }
        Ok(())
    }

    fn checked_transaction_path(&self, path: &Path) -> CompilerResult<PathBuf> {
        let relative = path
            .strip_prefix(&self.repository_root)
            .map_err(|_| recovery_error("transaction path escaped the repository"))?;
        self.resolve(&relative.to_string_lossy().replace('\\', "/"))
    }

    fn inspect_transaction_tree(&self, directory: &Path) -> CompilerResult<()> {
        self.checked_transaction_path(directory)?;
        if !directory.is_dir() {
            return Err(recovery_error(
                "transaction workspace must be a regular directory",
            ));
        }
        for entry in fs::read_dir(directory).map_err(|error| recovery_error(error.to_string()))? {
            let entry = entry.map_err(|error| recovery_error(error.to_string()))?;
            let path = self.checked_transaction_path(&entry.path())?;
            let kind = entry
                .file_type()
                .map_err(|error| recovery_error(error.to_string()))?;
            if kind.is_dir() {
                self.inspect_transaction_tree(&path)?;
            } else if !kind.is_file() {
                return Err(recovery_error(
                    "transaction workspace contains a non-regular file",
                ));
            }
        }
        Ok(())
    }

    fn prepare_restore(
        &self,
        transaction: &Path,
        path: &str,
        before: Option<&str>,
        after: Option<&str>,
    ) -> CompilerResult<RestoreAction> {
        if after.is_some_and(|digest| !super::valid_sha256(digest)) {
            return Err(recovery_error("invalid staged-file digest"));
        }
        let destination = self.resolve(path)?;
        if destination.exists() && !destination.is_file() {
            return Err(recovery_error("recovery destination is not a regular file"));
        }
        let current = self.read(path)?.map(|bytes| sha256_hex(&bytes));
        // Missing is also legitimate between removing a destination and promoting
        // its staged replacement, and while retrying an interrupted rollback.
        if current
            .as_deref()
            .is_some_and(|digest| Some(digest) != before && Some(digest) != after)
        {
            return Err(recovery_error(format!(
                "destination changed outside this transaction: {path}"
            )));
        }
        let bytes = if let Some(digest) = before {
            let backup = self.checked_transaction_path(&Self::backup_path(transaction, path))?;
            if !backup.is_file() {
                return Err(recovery_error(format!(
                    "required backup is missing: {path}"
                )));
            }
            let bytes = fs::read(backup).map_err(|error| recovery_error(error.to_string()))?;
            if sha256_hex(&bytes) != digest {
                return Err(recovery_error(format!(
                    "backup digest differs from the plan: {path}"
                )));
            }
            Some(bytes)
        } else {
            None
        };
        Ok(RestoreAction {
            path: path.to_owned(),
            bytes,
        })
    }

    fn read_journal(transaction: &Path) -> CompilerResult<Option<TransactionJournal>> {
        let journal_path = Self::journal_path(transaction);
        let bytes = match fs::read(&journal_path) {
            Ok(bytes) => bytes,
            Err(error) if error.kind() == ErrorKind::NotFound => {
                // Only empty workspaces are disposable without evidence. A missing
                // journal in a populated workspace may represent corrupted recovery
                // evidence, so preserve its staged files and backups for review.
                if fs::read_dir(transaction)
                    .map_err(|error| recovery_error(error.to_string()))?
                    .next()
                    .is_some()
                {
                    return Err(recovery_error(
                        "populated transaction workspace has no journal",
                    ));
                }
                return Ok(None);
            }
            Err(error) => return Err(recovery_error(format!("cannot read journal: {error}"))),
        };
        let value: serde_json::Value = serde_json::from_slice(&bytes)
            .map_err(|error| recovery_error(format!("cannot parse journal: {error}")))?;
        if value.get("schema").and_then(serde_json::Value::as_str) != Some(TRANSACTION_SCHEMA) {
            return Err(CompilerError::new(
                FailureKind::Unsupported,
                Diagnostic::error(
                    "IDN2325",
                    FailureKind::Unsupported,
                    Some(journal_path.display().to_string()),
                    "unsupported transaction journal; legacy v1 journals lack recovery authority evidence",
                    "Preserve the workspace and restore files from independently reviewed backups; see docs/contracts/COMPILER_V1.md. Do not relabel the journal schema.",
                ),
            ));
        }
        let journal: TransactionJournal = serde_json::from_slice(&bytes)
            .map_err(|error| recovery_error(format!("cannot parse v2 journal: {error}")))?;
        Ok(Some(journal))
    }

    // Fully validate and read every backup before returning any mutation authority.
    fn preflight_recovery(&self, transaction: &Path) -> CompilerResult<RecoveryTransaction> {
        let name = transaction
            .file_name()
            .and_then(|value| value.to_str())
            .filter(|value| super::valid_sha256(value))
            .ok_or_else(|| recovery_error("transaction directory is not a plan digest"))?;
        self.inspect_transaction_tree(transaction)?;
        let recovery_temp = transaction.join("recovery.tmp");
        if recovery_temp.exists() && !recovery_temp.is_file() {
            return Err(recovery_error(
                "recovery staging path is not a regular file",
            ));
        }
        let Some(journal) = Self::read_journal(transaction)? else {
            return Ok(RecoveryTransaction {
                directory: transaction.to_path_buf(),
                plan_digest: None,
                restores: Vec::new(),
            });
        };
        self.validate_plan(&journal.plan)?;
        if journal.plan.plan_digest != name || !journal.plan.has_mutations() {
            return Err(recovery_error(
                "journal plan identity does not match its workspace",
            ));
        }
        let actions = journal
            .plan
            .actions
            .iter()
            .filter(|action| {
                action.scope == PlanActionScope::Artifact
                    && matches!(
                        action.operation,
                        PlanOperation::Create | PlanOperation::Replace | PlanOperation::Remove
                    )
            })
            .collect::<Vec<_>>();
        if actions.len() != journal.actions.len() {
            return Err(recovery_error(
                "journal actions do not match the complete plan",
            ));
        }
        let mut restores = Vec::new();
        for (planned, recorded) in actions.iter().zip(&journal.actions).rev() {
            if planned.path != recorded.path
                || planned.operation != recorded.operation
                || (planned.operation == PlanOperation::Remove) == recorded.after_sha256.is_some()
            {
                return Err(recovery_error("journal action disagrees with the plan"));
            }
            restores.push(self.prepare_restore(
                transaction,
                &planned.path,
                planned.current_sha256.as_deref(),
                recorded.after_sha256.as_deref(),
            )?);
        }
        let manifest = journal
            .plan
            .actions
            .iter()
            .find(|action| action.scope == PlanActionScope::Manifest)
            .expect("validated manifest action");
        restores.push(self.prepare_restore(
            transaction,
            &journal.plan.manifest_path,
            manifest.current_sha256.as_deref(),
            Some(&journal.manifest_after_sha256),
        )?);
        Ok(RecoveryTransaction {
            directory: transaction.to_path_buf(),
            plan_digest: Some(name.to_owned()),
            restores,
        })
    }

    fn apply_recovery(&mut self, transaction: &RecoveryTransaction) -> CompilerResult<()> {
        for action in &transaction.restores {
            let destination = self.resolve(&action.path)?;
            if let Some(bytes) = &action.bytes {
                let staged =
                    self.checked_transaction_path(&transaction.directory.join("recovery.tmp"))?;
                // Unlink any old temporary file first: never overwrite through
                // a hard link supplied in the untrusted transaction workspace.
                Self::remove_file_if_present(&staged)?;
                Self::write_bytes(&staged, bytes)?;
                self.promote(&staged, &destination)?;
            } else {
                Self::remove_file_if_present(&destination)?;
                self.after_mutation()?;
            }
        }
        fs::remove_dir_all(&transaction.directory)
            .map_err(|error| recovery_error(format!("cannot remove recovered workspace: {error}")))
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
        match fs::read_dir(self.resolve(TRANSACTION_ROOT)?) {
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

        self.validate_plan(plan)?;
        let artifacts_by_path = artifacts
            .iter()
            .map(|artifact| (artifact.path.as_str(), artifact))
            .collect::<BTreeMap<_, _>>();
        Self::validate_artifacts(plan, artifacts, manifest)?;
        for action in &plan.actions {
            self.verify_current(action)?;
            if matches!(
                action.operation,
                PlanOperation::Create | PlanOperation::Replace
            ) && action.scope == PlanActionScope::Artifact
                && !artifacts_by_path.contains_key(action.path.as_str())
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

        let transaction =
            self.checked_transaction_path(&self.transaction_directory(&plan.plan_digest))?;
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
        let manifest_content = manifest_bytes(manifest)?;
        Self::write_bytes(&staged_manifest, &manifest_content)?;

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
                after_sha256: artifacts_by_path
                    .get(action.path.as_str())
                    .map(|artifact| sha256_hex(&artifact.bytes)),
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
            plan: plan.clone(),
            manifest_after_sha256: sha256_hex(&manifest_content),
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
        // Publish the journal only after every backup and staged write exists.
        let pending_journal = transaction.join("journal.pending");
        Self::write_bytes(&pending_journal, &journal_bytes)?;
        fs::rename(&pending_journal, Self::journal_path(&transaction))
            .map_err(|error| recovery_error(format!("cannot publish journal: {error}")))?;
        self.preflight_recovery(&transaction)?;

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
        let root = self.resolve(TRANSACTION_ROOT)?;
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

        // Complete the entire batch preflight before rollback or orphan cleanup.
        let transactions = directories
            .iter()
            .map(|directory| self.preflight_recovery(directory))
            .collect::<CompilerResult<Vec<_>>>()?;
        let mut destinations = BTreeSet::new();
        for transaction in &transactions {
            for action in &transaction.restores {
                if !destinations.insert(action.path.to_ascii_lowercase()) {
                    return Err(recovery_error(
                        "transactions have conflicting recovery destinations",
                    ));
                }
            }
        }
        let mut report = RecoveryReport::default();
        for transaction in &transactions {
            self.apply_recovery(transaction)?;
            if let Some(plan_digest) = &transaction.plan_digest {
                report.recovered_transactions += 1;
                report.plan_digests.push(plan_digest.clone());
            }
        }
        Ok(report)
    }
}

#[derive(Clone, Debug, Deserialize, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
struct TransactionJournal {
    schema: String,
    plan: CompilerPlan,
    manifest_after_sha256: String,
    actions: Vec<TransactionAction>,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
struct TransactionAction {
    path: String,
    operation: PlanOperation,
    after_sha256: Option<String>,
}

struct RecoveryTransaction {
    directory: PathBuf,
    plan_digest: Option<String>,
    restores: Vec<RestoreAction>,
}

struct RestoreAction {
    path: String,
    bytes: Option<Vec<u8>>,
}

fn recovery_error(message: impl Into<String>) -> CompilerError {
    fs_error(
        "IDN2324",
        None,
        message,
        "Preserve the journal, outputs, and backups; restore trusted evidence and use the explicitly authorized output root before retrying recovery.",
    )
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
