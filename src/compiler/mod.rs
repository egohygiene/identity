// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

//! Framework-neutral Identity compiler contracts and orchestration.
//!
//! The compiler core owns authority boundaries and deterministic state transitions.
//! Concrete renderers and package projections remain replaceable adapters.

mod filesystem;

mod validation;
use validation::{
    valid_sha256, validate_adapter_descriptor, validate_intent, validate_request,
    validate_resolved_identity,
};
mod planning;
use planning::{build_manifest, build_plan, byte_len, load_manifest, plan_digest};

#[cfg(test)]
mod tests;

pub use filesystem::{
    LocalArtifactStore, RecoveryActionInspection, RecoveryInspection, RecoveryOperation,
    RecoveryWorkspaceInspection,
};

use std::collections::{BTreeMap, BTreeSet};
use std::error::Error;
use std::fmt;

use serde::{Deserialize, Serialize};
use serde_json::Value;
use sha2::{Digest, Sha256};

pub const COMPILER_PLAN_SCHEMA: &str = "identity.compiler-plan/v1";
pub const COMPILER_MANIFEST_SCHEMA: &str = "identity.compiler-manifest/v1";
pub const COMPILER_API_MAJOR: u32 = 1;
const MANIFEST_FILE_NAME: &str = ".identity-manifest.json";

pub type CompilerResult<T> = Result<T, CompilerError>;

#[derive(Clone, Copy, Debug, Deserialize, Eq, Ord, PartialEq, PartialOrd, Serialize)]
#[serde(rename_all = "kebab-case")]
pub enum FailureKind {
    Invalid,
    Unsupported,
    Blocked,
    Partial,
    Failed,
    Drifted,
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, Ord, PartialEq, PartialOrd, Serialize)]
#[serde(rename_all = "lowercase")]
pub enum DiagnosticSeverity {
    Warning,
    Error,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct Diagnostic {
    pub code: String,
    pub severity: DiagnosticSeverity,
    pub failure: FailureKind,
    pub path: Option<String>,
    pub message: String,
    pub recovery: String,
}

impl Diagnostic {
    #[must_use]
    pub fn error(
        code: impl Into<String>,
        failure: FailureKind,
        path: Option<String>,
        message: impl Into<String>,
        recovery: impl Into<String>,
    ) -> Self {
        Self {
            code: code.into(),
            severity: DiagnosticSeverity::Error,
            failure,
            path,
            message: message.into(),
            recovery: recovery.into(),
        }
    }

    #[must_use]
    pub fn warning(
        code: impl Into<String>,
        failure: FailureKind,
        path: Option<String>,
        message: impl Into<String>,
        recovery: impl Into<String>,
    ) -> Self {
        Self {
            code: code.into(),
            severity: DiagnosticSeverity::Warning,
            failure,
            path,
            message: message.into(),
            recovery: recovery.into(),
        }
    }
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct CompilerError {
    pub kind: FailureKind,
    pub diagnostics: Vec<Diagnostic>,
}

impl CompilerError {
    #[must_use]
    pub fn new(kind: FailureKind, diagnostic: Diagnostic) -> Self {
        Self {
            kind,
            diagnostics: vec![diagnostic],
        }
    }

    #[must_use]
    pub fn from_diagnostics(kind: FailureKind, mut diagnostics: Vec<Diagnostic>) -> Self {
        sort_diagnostics(&mut diagnostics);
        Self { kind, diagnostics }
    }
}

impl fmt::Display for CompilerError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        if let Some(first) = self.diagnostics.first() {
            write!(formatter, "{}: {}", first.code, first.message)
        } else {
            write!(formatter, "identity compiler {:?} failure", self.kind)
        }
    }
}

impl Error for CompilerError {}

#[derive(Clone, Debug, Default, Deserialize, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct IdentityIntent {
    pub project_id: String,
    pub source_digest: String,
    #[serde(default)]
    pub documents: BTreeMap<String, Value>,
    #[serde(default)]
    pub approvals: BTreeSet<String>,
}

#[derive(Clone, Debug, Default, Deserialize, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct ResolvedIdentity {
    pub project_id: String,
    pub source_digest: String,
    #[serde(default)]
    pub values: BTreeMap<String, Value>,
    #[serde(default)]
    pub lineage: BTreeMap<String, String>,
    #[serde(default)]
    pub approvals: BTreeSet<String>,
}

#[derive(Clone, Debug, Default, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct ValidationReport {
    #[serde(default)]
    pub diagnostics: Vec<Diagnostic>,
}

impl ValidationReport {
    #[must_use]
    pub fn has_errors(&self) -> bool {
        self.diagnostics
            .iter()
            .any(|diagnostic| diagnostic.severity == DiagnosticSeverity::Error)
    }
}

pub trait IdentityReader: Send + Sync {
    fn read(&self) -> CompilerResult<IdentityIntent>;
}

pub trait IdentityValidator: Send + Sync {
    fn validate(&self, intent: &IdentityIntent) -> CompilerResult<ValidationReport>;
}

pub trait IdentityResolver: Send + Sync {
    fn resolve(&self, intent: &IdentityIntent) -> CompilerResult<ResolvedIdentity>;
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, Ord, PartialEq, PartialOrd, Serialize)]
#[serde(rename_all = "kebab-case")]
pub enum AdapterKind {
    TokenTransformer,
    VectorRenderer,
    RasterRenderer,
    Font,
    Metadata,
    Archive,
    Publication,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct AdapterDescriptor {
    pub id: String,
    pub version: String,
    pub kind: AdapterKind,
    pub compiler_api_major: u32,
    pub deterministic: bool,
    pub offline: bool,
    #[serde(default)]
    pub capabilities: BTreeSet<String>,
}

#[derive(Clone, Debug, Default, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct AdapterPlan {
    #[serde(default)]
    pub warnings: Vec<String>,
    #[serde(default)]
    pub required_approvals: BTreeSet<String>,
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, Ord, PartialEq, PartialOrd, Serialize)]
#[serde(rename_all = "kebab-case")]
pub enum EvidenceStatus {
    Verified,
    Warning,
    Skipped,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct EvidenceRecord {
    pub target_id: String,
    pub adapter_id: String,
    pub check: String,
    pub status: EvidenceStatus,
    pub message: String,
}

#[derive(Clone, Debug, Default, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct VerificationReport {
    #[serde(default)]
    pub diagnostics: Vec<Diagnostic>,
    #[serde(default)]
    pub evidence: Vec<EvidenceRecord>,
}

impl VerificationReport {
    #[must_use]
    pub fn has_errors(&self) -> bool {
        self.diagnostics
            .iter()
            .any(|diagnostic| diagnostic.severity == DiagnosticSeverity::Error)
    }
}

#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct ProjectionTarget {
    pub id: String,
    pub profile: String,
    pub relative_path: String,
    pub adapter_id: String,
    pub media_type: String,
    #[serde(default)]
    pub parameters: BTreeMap<String, Value>,
    #[serde(default)]
    pub required_approval: Option<String>,
    #[serde(default)]
    pub maximum_bytes: Option<u64>,
}

pub trait ProjectionAdapter: Send + Sync {
    fn descriptor(&self) -> AdapterDescriptor;

    fn plan(
        &self,
        identity: &ResolvedIdentity,
        target: &ProjectionTarget,
    ) -> CompilerResult<AdapterPlan>;

    fn render(
        &self,
        identity: &ResolvedIdentity,
        target: &ProjectionTarget,
    ) -> CompilerResult<Vec<u8>>;

    fn verify(
        &self,
        identity: &ResolvedIdentity,
        target: &ProjectionTarget,
        bytes: &[u8],
    ) -> CompilerResult<VerificationReport>;
}

#[derive(Default)]
pub struct AdapterRegistry {
    adapters: BTreeMap<String, Box<dyn ProjectionAdapter>>,
}

impl AdapterRegistry {
    #[must_use]
    pub fn new() -> Self {
        Self::default()
    }

    pub fn register<A>(&mut self, adapter: A) -> CompilerResult<()>
    where
        A: ProjectionAdapter + 'static,
    {
        let descriptor = adapter.descriptor();
        validate_adapter_descriptor(&descriptor)?;
        if self.adapters.contains_key(&descriptor.id) {
            return Err(CompilerError::new(
                FailureKind::Invalid,
                Diagnostic::error(
                    "IDN2100",
                    FailureKind::Invalid,
                    None,
                    format!("adapter {:?} is registered more than once", descriptor.id),
                    "Register one implementation for each stable adapter identifier.",
                ),
            ));
        }
        self.adapters.insert(descriptor.id, Box::new(adapter));
        Ok(())
    }

    #[must_use]
    pub fn descriptor(&self, adapter_id: &str) -> Option<AdapterDescriptor> {
        self.adapters
            .get(adapter_id)
            .map(|adapter| adapter.descriptor())
    }

    #[must_use]
    pub fn descriptors(&self) -> Vec<AdapterDescriptor> {
        self.adapters
            .values()
            .map(|adapter| adapter.descriptor())
            .collect()
    }

    fn get(&self, adapter_id: &str) -> Option<&dyn ProjectionAdapter> {
        self.adapters.get(adapter_id).map(Box::as_ref)
    }
}

#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct CompilerRequest {
    pub output_root: String,
    pub targets: Vec<ProjectionTarget>,
}

impl CompilerRequest {
    #[must_use]
    pub fn manifest_path(&self) -> String {
        format!(
            "{}/{}",
            self.output_root.trim_end_matches('/'),
            MANIFEST_FILE_NAME
        )
    }
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, Ord, PartialEq, PartialOrd, Serialize)]
#[serde(rename_all = "kebab-case")]
pub enum PlanActionScope {
    Artifact,
    Manifest,
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, Ord, PartialEq, PartialOrd, Serialize)]
#[serde(rename_all = "kebab-case")]
pub enum PlanOperation {
    Create,
    Replace,
    Remove,
    Unchanged,
    Blocked,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct PlanAction {
    pub scope: PlanActionScope,
    pub target_id: String,
    pub path: String,
    pub adapter_id: String,
    pub adapter_version: String,
    pub operation: PlanOperation,
    pub input_fingerprint: String,
    pub current_sha256: Option<String>,
    pub current_bytes: Option<u64>,
    pub previous_sha256: Option<String>,
    #[serde(default)]
    pub required_approvals: BTreeSet<String>,
    #[serde(default)]
    pub warnings: Vec<String>,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct CompatibilityRecord {
    pub target_id: String,
    pub adapter_id: String,
    pub adapter_version: Option<String>,
    pub compatible: bool,
    #[serde(default)]
    pub reasons: Vec<String>,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct CompilerPlan {
    pub schema: String,
    pub project_id: String,
    pub source_digest: String,
    pub plan_digest: String,
    pub output_root: String,
    pub manifest_path: String,
    pub actions: Vec<PlanAction>,
    pub compatibility: Vec<CompatibilityRecord>,
    #[serde(default)]
    pub diagnostics: Vec<Diagnostic>,
    #[serde(default)]
    pub required_approvals: BTreeSet<String>,
}

impl CompilerPlan {
    #[must_use]
    pub fn has_blocking_diagnostics(&self) -> bool {
        self.diagnostics
            .iter()
            .any(|diagnostic| diagnostic.severity == DiagnosticSeverity::Error)
    }

    #[must_use]
    pub fn has_mutations(&self) -> bool {
        self.actions.iter().any(|action| {
            matches!(
                action.operation,
                PlanOperation::Create | PlanOperation::Replace | PlanOperation::Remove
            )
        })
    }
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct ManifestOutput {
    pub target_id: String,
    pub profile: String,
    pub path: String,
    pub media_type: String,
    pub adapter_id: String,
    pub adapter_version: String,
    pub input_fingerprint: String,
    pub sha256: String,
    pub bytes: u64,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct CompilerManifest {
    pub schema: String,
    pub project_id: String,
    pub source_digest: String,
    pub plan_digest: String,
    pub outputs: Vec<ManifestOutput>,
    pub adapters: Vec<AdapterDescriptor>,
    #[serde(default)]
    pub evidence: Vec<EvidenceRecord>,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct RenderedArtifact {
    pub target_id: String,
    pub path: String,
    pub bytes: Vec<u8>,
}

#[derive(Clone, Debug, Default, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct RecoveryReport {
    pub recovered_transactions: u64,
    #[serde(default)]
    pub plan_digests: Vec<String>,
}

pub trait ArtifactStore {
    fn read(&self, relative_path: &str) -> CompilerResult<Option<Vec<u8>>>;

    fn recovery_required(&self) -> CompilerResult<bool>;

    fn commit(
        &mut self,
        plan: &CompilerPlan,
        artifacts: &[RenderedArtifact],
        manifest: &CompilerManifest,
    ) -> CompilerResult<()>;

    fn recover(&mut self) -> CompilerResult<RecoveryReport>;
}

#[derive(Clone, Debug)]
pub struct PreparedCompilation {
    pub identity: ResolvedIdentity,
    pub request: CompilerRequest,
    pub plan: CompilerPlan,
    previous_manifest: Option<CompilerManifest>,
}

pub struct Compiler<'a> {
    reader: &'a dyn IdentityReader,
    validator: &'a dyn IdentityValidator,
    resolver: &'a dyn IdentityResolver,
    adapters: &'a AdapterRegistry,
    store: &'a mut dyn ArtifactStore,
}

impl<'a> Compiler<'a> {
    #[must_use]
    pub fn new(
        reader: &'a dyn IdentityReader,
        validator: &'a dyn IdentityValidator,
        resolver: &'a dyn IdentityResolver,
        adapters: &'a AdapterRegistry,
        store: &'a mut dyn ArtifactStore,
    ) -> Self {
        Self {
            reader,
            validator,
            resolver,
            adapters,
            store,
        }
    }

    pub fn prepare(&mut self, request: CompilerRequest) -> CompilerResult<PreparedCompilation> {
        if self.store.recovery_required()? {
            return Err(CompilerError::new(
                FailureKind::Blocked,
                Diagnostic::error(
                    "IDN2301",
                    FailureKind::Blocked,
                    None,
                    "a previous compiler transaction requires recovery",
                    "Run identity v1-inspect --repository-root <consumer> --output-root <authorized-root>, review the reported rollback, then explicitly run identity v1-recover with the same arguments before planning new mutations.",
                ),
            ));
        }

        validate_request(&request)?;
        let intent = self.reader.read()?;
        validate_intent(&intent)?;

        let mut validation = self.validator.validate(&intent)?;
        sort_diagnostics(&mut validation.diagnostics);
        if validation.has_errors() {
            return Err(CompilerError::from_diagnostics(
                FailureKind::Invalid,
                validation.diagnostics,
            ));
        }

        let identity = self.resolver.resolve(&intent)?;
        validate_resolved_identity(&identity)?;
        if identity.project_id != intent.project_id
            || identity.source_digest != intent.source_digest
        {
            return Err(CompilerError::new(
                FailureKind::Invalid,
                Diagnostic::error(
                    "IDN2004",
                    FailureKind::Invalid,
                    None,
                    "resolver changed the project or canonical source identity",
                    "Preserve projectId and sourceDigest across the resolve boundary.",
                ),
            ));
        }

        let manifest_path = request.manifest_path();
        let previous_manifest = load_manifest(self.store, &manifest_path)?;
        let plan = build_plan(
            self.store,
            self.adapters,
            &identity,
            &request,
            previous_manifest.as_ref(),
        )?;

        self.verify_source(&identity)?;

        Ok(PreparedCompilation {
            identity,
            request,
            plan,
            previous_manifest,
        })
    }

    fn verify_source(&self, expected: &ResolvedIdentity) -> CompilerResult<()> {
        let intent = self.reader.read()?;
        validate_intent(&intent)?;
        let validation = self.validator.validate(&intent)?;
        if validation.has_errors() {
            return Err(CompilerError::from_diagnostics(
                FailureKind::Invalid,
                validation.diagnostics,
            ));
        }
        let current = self.resolver.resolve(&intent)?;
        if &current != expected {
            return Err(CompilerError::new(
                FailureKind::Drifted,
                Diagnostic::error(
                    "IDN2006",
                    FailureKind::Drifted,
                    None,
                    "source changed after preparation",
                    "Reload the source and create a new plan.",
                ),
            ));
        }
        Ok(())
    }

    // Execution keeps the render/verify/apply authority sequence visible in one place.
    #[allow(clippy::too_many_lines)]
    pub fn execute(
        &mut self,
        prepared: &PreparedCompilation,
        approvals: &BTreeSet<String>,
    ) -> CompilerResult<CompilerManifest> {
        if self.store.recovery_required()? {
            return Err(CompilerError::new(
                FailureKind::Blocked,
                Diagnostic::error(
                    "IDN2301",
                    FailureKind::Blocked,
                    None,
                    "a previous compiler transaction requires recovery",
                    "Run identity v1-inspect --repository-root <consumer> --output-root <authorized-root>, review the reported rollback, then explicitly run identity v1-recover with the same arguments before applying the plan.",
                ),
            ));
        }
        self.verify_source(&prepared.identity)?;
        if prepared.plan.has_blocking_diagnostics() {
            return Err(CompilerError::from_diagnostics(
                FailureKind::Blocked,
                prepared.plan.diagnostics.clone(),
            ));
        }

        let missing_approvals = prepared
            .plan
            .required_approvals
            .difference(approvals)
            .cloned()
            .collect::<Vec<_>>();
        if !missing_approvals.is_empty() {
            let diagnostics = missing_approvals
                .into_iter()
                .map(|approval| {
                    Diagnostic::error(
                        "IDN2304",
                        FailureKind::Blocked,
                        None,
                        format!("required approval {approval:?} was not supplied"),
                        "Review the plan and pass the exact recorded approval identifier.",
                    )
                })
                .collect();
            return Err(CompilerError::from_diagnostics(
                FailureKind::Blocked,
                diagnostics,
            ));
        }

        let target_by_id = prepared
            .request
            .targets
            .iter()
            .map(|target| (target.id.as_str(), target))
            .collect::<BTreeMap<_, _>>();
        let mut rendered = Vec::new();
        let mut verification_evidence = Vec::new();

        for action in prepared.plan.actions.iter().filter(|action| {
            action.scope == PlanActionScope::Artifact
                && matches!(
                    action.operation,
                    PlanOperation::Create | PlanOperation::Replace
                )
        }) {
            let target = target_by_id.get(action.target_id.as_str()).ok_or_else(|| {
                CompilerError::new(
                    FailureKind::Invalid,
                    Diagnostic::error(
                        "IDN2005",
                        FailureKind::Invalid,
                        Some(action.path.clone()),
                        format!(
                            "plan target {:?} is absent from the execution request",
                            action.target_id
                        ),
                        "Execute the plan with the exact target request used during planning.",
                    ),
                )
            })?;
            let adapter = self.adapters.get(&action.adapter_id).ok_or_else(|| {
                CompilerError::new(
                    FailureKind::Unsupported,
                    Diagnostic::error(
                        "IDN2101",
                        FailureKind::Unsupported,
                        Some(action.path.clone()),
                        format!("adapter {:?} is no longer available", action.adapter_id),
                        "Restore the exact adapter version used to create the plan.",
                    ),
                )
            })?;

            let bytes = match adapter.render(&prepared.identity, target) {
                Ok(bytes) => bytes,
                Err(error) => {
                    return Err(partialize_error(error, !rendered.is_empty()));
                }
            };
            if let Some(maximum_bytes) = target.maximum_bytes {
                let actual_bytes = byte_len(&bytes)?;
                if actual_bytes > maximum_bytes {
                    return Err(partialize_error(
                        CompilerError::new(
                            FailureKind::Failed,
                            Diagnostic::error(
                                "IDN2203",
                                FailureKind::Failed,
                                Some(action.path.clone()),
                                format!(
                                    "rendered target is {actual_bytes} bytes, above the {maximum_bytes} byte budget"
                                ),
                                "Reduce the artifact size or intentionally revise the target budget.",
                            ),
                        ),
                        !rendered.is_empty(),
                    ));
                }
            }

            let mut verification = adapter.verify(&prepared.identity, target, &bytes)?;
            sort_diagnostics(&mut verification.diagnostics);
            if verification.has_errors() {
                let error =
                    CompilerError::from_diagnostics(FailureKind::Failed, verification.diagnostics);
                return Err(partialize_error(error, !rendered.is_empty()));
            }
            verification_evidence.append(&mut verification.evidence);
            rendered.push(RenderedArtifact {
                target_id: action.target_id.clone(),
                path: action.path.clone(),
                bytes,
            });
        }

        let manifest = build_manifest(
            &prepared.identity,
            &prepared.request,
            &prepared.plan,
            prepared.previous_manifest.as_ref(),
            &rendered,
            self.adapters,
            verification_evidence,
        )?;
        self.verify_source(&prepared.identity)?;
        self.store.commit(&prepared.plan, &rendered, &manifest)?;
        Ok(manifest)
    }

    pub fn recover(&mut self) -> CompilerResult<RecoveryReport> {
        self.store.recover()
    }
}

// Planning is intentionally linear so every mutation and approval decision is inspectable.

// Manifest assembly keeps one ordered projection-to-evidence pass for deterministic review.

pub(crate) fn manifest_bytes(manifest: &CompilerManifest) -> CompilerResult<Vec<u8>> {
    let mut bytes = serde_json::to_vec_pretty(manifest).map_err(|error| {
        CompilerError::new(
            FailureKind::Failed,
            Diagnostic::error(
                "IDN2206",
                FailureKind::Failed,
                None,
                format!("cannot serialize compiler manifest: {error}"),
                "Report the manifest serialization failure; no generated state was changed.",
            ),
        )
    })?;
    bytes.push(b'\n');
    Ok(bytes)
}

pub(crate) fn sha256_hex(bytes: &[u8]) -> String {
    let digest = Sha256::digest(bytes);
    format!("{digest:x}")
}

pub(crate) fn validate_portable_path(path: &str, label: &str) -> CompilerResult<()> {
    if path.is_empty()
        || path.starts_with('/')
        || path.ends_with('/')
        || path
            .chars()
            .any(|character| character.is_control() || "\\:*?\"<>|".contains(character))
        || path.split('/').any(|segment| {
            let stem = segment
                .split('.')
                .next()
                .unwrap_or_default()
                .to_ascii_uppercase();
            segment.is_empty()
                || matches!(segment, "." | "..")
                || segment.ends_with(['.', ' '])
                || matches!(stem.as_str(), "CON" | "PRN" | "AUX" | "NUL")
                || ["COM", "LPT"].iter().any(|prefix| {
                    stem.strip_prefix(prefix).is_some_and(|suffix| {
                        matches!(
                            suffix,
                            "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "¹" | "²" | "³"
                        )
                    })
                })
        })
    {
        return Err(CompilerError::new(
            FailureKind::Invalid,
            Diagnostic::error(
                "IDN2011",
                FailureKind::Invalid,
                Some(path.to_owned()),
                format!("{label} must be a normalized repository-relative path"),
                "Use forward-slash-separated path segments without empty, dot, parent, or absolute components.",
            ),
        ));
    }
    Ok(())
}

pub(crate) fn join_portable(root: &str, child: &str) -> String {
    format!(
        "{}/{}",
        root.trim_end_matches('/'),
        child.trim_start_matches('/')
    )
}

fn sort_diagnostics(diagnostics: &mut [Diagnostic]) {
    diagnostics.sort_by(|left, right| {
        left.path
            .cmp(&right.path)
            .then_with(|| left.code.cmp(&right.code))
            .then_with(|| left.message.cmp(&right.message))
    });
}

fn partialize_error(mut error: CompilerError, partial: bool) -> CompilerError {
    if partial {
        error.kind = FailureKind::Partial;
        for diagnostic in &mut error.diagnostics {
            diagnostic.failure = FailureKind::Partial;
        }
    }
    error
}
