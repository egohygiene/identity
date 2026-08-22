// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

//! Framework-neutral Identity compiler contracts and orchestration.
//!
//! The compiler core owns authority boundaries and deterministic state transitions.
//! Concrete renderers and package projections remain replaceable adapters.

mod filesystem;

#[cfg(test)]
mod tests;

pub use filesystem::LocalArtifactStore;

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
                    "Run the explicit recovery operation before planning new mutations.",
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

        Ok(PreparedCompilation {
            identity,
            request,
            plan,
            previous_manifest,
        })
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
                    "Run the explicit recovery operation before applying the plan.",
                ),
            ));
        }
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
        self.store.commit(&prepared.plan, &rendered, &manifest)?;
        Ok(manifest)
    }

    pub fn recover(&mut self) -> CompilerResult<RecoveryReport> {
        self.store.recover()
    }
}

fn validate_adapter_descriptor(descriptor: &AdapterDescriptor) -> CompilerResult<()> {
    if !valid_identifier(&descriptor.id) || descriptor.version.trim().is_empty() {
        return Err(CompilerError::new(
            FailureKind::Invalid,
            Diagnostic::error(
                "IDN2105",
                FailureKind::Invalid,
                None,
                "adapter descriptors require a stable identifier and version",
                "Use a lowercase kebab-case adapter id and a non-empty version.",
            ),
        ));
    }
    Ok(())
}

fn validate_request(request: &CompilerRequest) -> CompilerResult<()> {
    validate_portable_path(&request.output_root, "output root")?;
    let manifest_path = request.manifest_path();
    let mut ids = BTreeSet::new();
    let mut paths = BTreeSet::new();
    for target in &request.targets {
        if !valid_identifier(&target.id) || target.profile.trim().is_empty() {
            return Err(CompilerError::new(
                FailureKind::Invalid,
                Diagnostic::error(
                    "IDN2001",
                    FailureKind::Invalid,
                    None,
                    format!("invalid projection target identity: {:?}", target.id),
                    "Use a lowercase kebab-case target id and a non-empty profile id.",
                ),
            ));
        }
        validate_portable_path(&target.relative_path, "target path")?;
        if target.media_type.trim().is_empty() || !valid_identifier(&target.adapter_id) {
            return Err(CompilerError::new(
                FailureKind::Invalid,
                Diagnostic::error(
                    "IDN2002",
                    FailureKind::Invalid,
                    Some(target.relative_path.clone()),
                    "target media type and adapter id must be explicit",
                    "Declare a media type and stable lowercase adapter id for every target.",
                ),
            ));
        }
        let full_path = join_portable(&request.output_root, &target.relative_path);
        if full_path == manifest_path {
            return Err(CompilerError::new(
                FailureKind::Invalid,
                Diagnostic::error(
                    "IDN2003",
                    FailureKind::Invalid,
                    Some(full_path),
                    "projection target collides with the compiler manifest path",
                    "Choose a target path other than .identity-manifest.json.",
                ),
            ));
        }
        if !ids.insert(target.id.as_str()) || !paths.insert(full_path) {
            return Err(CompilerError::new(
                FailureKind::Invalid,
                Diagnostic::error(
                    "IDN2006",
                    FailureKind::Invalid,
                    Some(target.relative_path.clone()),
                    "projection target ids and paths must be unique",
                    "Remove the duplicate target id or path before planning.",
                ),
            ));
        }
    }
    Ok(())
}

fn validate_intent(intent: &IdentityIntent) -> CompilerResult<()> {
    if !valid_identifier(&intent.project_id) || !valid_sha256(&intent.source_digest) {
        return Err(CompilerError::new(
            FailureKind::Invalid,
            Diagnostic::error(
                "IDN2007",
                FailureKind::Invalid,
                None,
                "identity intent has an invalid project id or source digest",
                "Provide a lowercase project id and 64-character lowercase SHA-256 source digest.",
            ),
        ));
    }
    Ok(())
}

fn validate_resolved_identity(identity: &ResolvedIdentity) -> CompilerResult<()> {
    if !valid_identifier(&identity.project_id) || !valid_sha256(&identity.source_digest) {
        return Err(CompilerError::new(
            FailureKind::Invalid,
            Diagnostic::error(
                "IDN2008",
                FailureKind::Invalid,
                None,
                "resolved identity has an invalid project id or source digest",
                "Preserve the validated source identity during resolution.",
            ),
        ));
    }
    Ok(())
}

fn load_manifest(
    store: &dyn ArtifactStore,
    manifest_path: &str,
) -> CompilerResult<Option<CompilerManifest>> {
    let Some(bytes) = store.read(manifest_path)? else {
        return Ok(None);
    };
    let manifest: CompilerManifest = serde_json::from_slice(&bytes).map_err(|error| {
        CompilerError::new(
            FailureKind::Drifted,
            Diagnostic::error(
                "IDN2305",
                FailureKind::Drifted,
                Some(manifest_path.to_owned()),
                format!("existing compiler manifest is invalid: {error}"),
                "Restore a valid generated manifest or explicitly remove the invalid generated state.",
            ),
        )
    })?;
    if manifest.schema != COMPILER_MANIFEST_SCHEMA {
        return Err(CompilerError::new(
            FailureKind::Unsupported,
            Diagnostic::error(
                "IDN2306",
                FailureKind::Unsupported,
                Some(manifest_path.to_owned()),
                format!("unsupported compiler manifest schema {:?}", manifest.schema),
                "Migrate or remove the unsupported generated manifest before continuing.",
            ),
        ));
    }
    Ok(Some(manifest))
}

// Planning is intentionally linear so every mutation and approval decision is inspectable.
#[allow(clippy::too_many_lines)]
fn build_plan(
    store: &dyn ArtifactStore,
    adapters: &AdapterRegistry,
    identity: &ResolvedIdentity,
    request: &CompilerRequest,
    previous_manifest: Option<&CompilerManifest>,
) -> CompilerResult<CompilerPlan> {
    let mut targets = request.targets.clone();
    targets.sort_by(|left, right| {
        left.relative_path
            .cmp(&right.relative_path)
            .then_with(|| left.id.cmp(&right.id))
    });
    let previous_by_path = previous_manifest
        .map(|manifest| {
            manifest
                .outputs
                .iter()
                .map(|output| (output.path.as_str(), output))
                .collect::<BTreeMap<_, _>>()
        })
        .unwrap_or_default();

    let mut desired_paths = BTreeSet::new();
    let mut actions = Vec::new();
    let mut compatibility = Vec::new();
    let mut diagnostics = Vec::new();

    for target in &targets {
        let path = join_portable(&request.output_root, &target.relative_path);
        desired_paths.insert(path.clone());
        let Some(adapter) = adapters.get(&target.adapter_id) else {
            diagnostics.push(Diagnostic::error(
                "IDN2101",
                FailureKind::Unsupported,
                Some(path.clone()),
                format!("no adapter is registered for {:?}", target.adapter_id),
                "Install or register an adapter that declares the requested capability.",
            ));
            compatibility.push(CompatibilityRecord {
                target_id: target.id.clone(),
                adapter_id: target.adapter_id.clone(),
                adapter_version: None,
                compatible: false,
                reasons: vec!["adapter is not registered".to_owned()],
            });
            actions.push(blocked_action(target, &path));
            continue;
        };

        let descriptor = adapter.descriptor();
        let mut reasons = Vec::new();
        if descriptor.compiler_api_major != COMPILER_API_MAJOR {
            reasons.push(format!(
                "compiler API major {} is incompatible with {}",
                descriptor.compiler_api_major, COMPILER_API_MAJOR
            ));
            diagnostics.push(Diagnostic::error(
                "IDN2102",
                FailureKind::Unsupported,
                Some(path.clone()),
                format!(
                    "adapter {:?} uses an incompatible compiler API",
                    descriptor.id
                ),
                "Use an adapter built for the current Identity compiler API major.",
            ));
        }
        if !descriptor.deterministic {
            reasons.push("adapter does not guarantee deterministic output".to_owned());
            diagnostics.push(Diagnostic::error(
                "IDN2103",
                FailureKind::Blocked,
                Some(path.clone()),
                format!("adapter {:?} is not deterministic", descriptor.id),
                "Use a deterministic projection adapter for compiler-owned output.",
            ));
        }
        if !descriptor.offline {
            reasons.push("adapter requires network access".to_owned());
            diagnostics.push(Diagnostic::error(
                "IDN2104",
                FailureKind::Blocked,
                Some(path.clone()),
                format!("adapter {:?} is not offline-safe", descriptor.id),
                "Move provider-backed creation behind an explicit creative handoff boundary.",
            ));
        }

        let adapter_plan = match adapter.plan(identity, target) {
            Ok(plan) => plan,
            Err(error) => {
                reasons.push(format!("adapter planning failed: {error}"));
                diagnostics.extend(error.diagnostics.clone());
                compatibility.push(CompatibilityRecord {
                    target_id: target.id.clone(),
                    adapter_id: descriptor.id.clone(),
                    adapter_version: Some(descriptor.version.clone()),
                    compatible: false,
                    reasons,
                });
                actions.push(blocked_action_with_descriptor(target, &path, &descriptor));
                continue;
            }
        };

        let compatible = reasons.is_empty();
        compatibility.push(CompatibilityRecord {
            target_id: target.id.clone(),
            adapter_id: descriptor.id.clone(),
            adapter_version: Some(descriptor.version.clone()),
            compatible,
            reasons,
        });
        if !compatible {
            actions.push(blocked_action_with_descriptor(target, &path, &descriptor));
            continue;
        }

        let fingerprint = input_fingerprint(identity, target, &descriptor)?;
        let current = store.read(&path)?;
        let current_sha256 = current.as_deref().map(sha256_hex);
        let current_bytes = current.as_deref().map(byte_len).transpose()?;
        let previous = previous_by_path.get(path.as_str()).copied();
        let mut required_approvals = adapter_plan.required_approvals;
        if let Some(approval) = &target.required_approval {
            required_approvals.insert(approval.clone());
        }
        let mut warnings = adapter_plan.warnings;

        let operation = match (&current_sha256, previous) {
            (None, _) => PlanOperation::Create,
            (Some(current_sha), Some(previous_output))
                if current_sha == &previous_output.sha256
                    && previous_output.input_fingerprint == fingerprint
                    && previous_output.adapter_version == descriptor.version =>
            {
                PlanOperation::Unchanged
            }
            (Some(current_sha), Some(previous_output)) => {
                if current_sha != &previous_output.sha256 {
                    diagnostics.push(Diagnostic::warning(
                        "IDN2302",
                        FailureKind::Drifted,
                        Some(path.clone()),
                        "generated output differs from the previous manifest",
                        "Review the drift before replacing the generated projection.",
                    ));
                    warnings
                        .push("current output has drifted from the previous manifest".to_owned());
                    required_approvals.insert(format!("replace-drifted:{path}"));
                }
                PlanOperation::Replace
            }
            (Some(_), None) => {
                warnings.push(
                    "target path exists but is not tracked by the previous manifest".to_owned(),
                );
                required_approvals.insert(format!("replace-unmanaged:{path}"));
                PlanOperation::Replace
            }
        };

        actions.push(PlanAction {
            scope: PlanActionScope::Artifact,
            target_id: target.id.clone(),
            path,
            adapter_id: descriptor.id,
            adapter_version: descriptor.version,
            operation,
            input_fingerprint: fingerprint,
            current_sha256,
            current_bytes,
            previous_sha256: previous.map(|output| output.sha256.clone()),
            required_approvals,
            warnings,
        });
    }

    if let Some(previous_manifest) = previous_manifest {
        for output in &previous_manifest.outputs {
            if desired_paths.contains(output.path.as_str()) {
                continue;
            }
            let current = store.read(&output.path)?;
            let Some(current_bytes_value) = current else {
                continue;
            };
            let current_sha256 = sha256_hex(&current_bytes_value);
            let mut required_approvals = BTreeSet::new();
            required_approvals.insert(format!("remove:{}", output.path));
            let mut warnings = vec!["target is no longer selected and will be removed".to_owned()];
            if current_sha256 != output.sha256 {
                diagnostics.push(Diagnostic::warning(
                    "IDN2302",
                    FailureKind::Drifted,
                    Some(output.path.clone()),
                    "stale generated output was modified after the previous manifest",
                    "Review the drift before approving removal.",
                ));
                warnings.push("stale output has drifted from the previous manifest".to_owned());
            }
            actions.push(PlanAction {
                scope: PlanActionScope::Artifact,
                target_id: output.target_id.clone(),
                path: output.path.clone(),
                adapter_id: output.adapter_id.clone(),
                adapter_version: output.adapter_version.clone(),
                operation: PlanOperation::Remove,
                input_fingerprint: output.input_fingerprint.clone(),
                current_sha256: Some(current_sha256),
                current_bytes: Some(byte_len(&current_bytes_value)?),
                previous_sha256: Some(output.sha256.clone()),
                required_approvals,
                warnings,
            });
        }
    }

    actions.sort_by(|left, right| {
        left.scope
            .cmp(&right.scope)
            .then_with(|| left.path.cmp(&right.path))
            .then_with(|| left.target_id.cmp(&right.target_id))
    });
    compatibility.sort_by(|left, right| left.target_id.cmp(&right.target_id));
    sort_diagnostics(&mut diagnostics);

    let artifact_mutation = actions.iter().any(|action| {
        action.scope == PlanActionScope::Artifact
            && matches!(
                action.operation,
                PlanOperation::Create | PlanOperation::Replace | PlanOperation::Remove
            )
    });
    let manifest_path = request.manifest_path();
    let manifest_current = store.read(&manifest_path)?;
    let manifest_operation = if previous_manifest.is_some() && !artifact_mutation {
        PlanOperation::Unchanged
    } else if manifest_current.is_some() {
        PlanOperation::Replace
    } else {
        PlanOperation::Create
    };
    actions.push(PlanAction {
        scope: PlanActionScope::Manifest,
        target_id: "compiler-manifest".to_owned(),
        path: manifest_path.clone(),
        adapter_id: "identity-compiler".to_owned(),
        adapter_version: env!("CARGO_PKG_VERSION").to_owned(),
        operation: manifest_operation,
        input_fingerprint: identity.source_digest.clone(),
        current_sha256: manifest_current.as_deref().map(sha256_hex),
        current_bytes: manifest_current.as_deref().map(byte_len).transpose()?,
        previous_sha256: manifest_current.as_deref().map(sha256_hex),
        required_approvals: BTreeSet::new(),
        warnings: Vec::new(),
    });

    let required_approvals = actions
        .iter()
        .flat_map(|action| action.required_approvals.iter().cloned())
        .collect();
    let mut plan = CompilerPlan {
        schema: COMPILER_PLAN_SCHEMA.to_owned(),
        project_id: identity.project_id.clone(),
        source_digest: identity.source_digest.clone(),
        plan_digest: String::new(),
        output_root: request.output_root.clone(),
        manifest_path,
        actions,
        compatibility,
        diagnostics,
        required_approvals,
    };
    plan.plan_digest = plan_digest(&plan)?;
    Ok(plan)
}

// Manifest assembly keeps one ordered projection-to-evidence pass for deterministic review.
#[allow(clippy::too_many_lines)]
fn build_manifest(
    identity: &ResolvedIdentity,
    request: &CompilerRequest,
    plan: &CompilerPlan,
    previous_manifest: Option<&CompilerManifest>,
    rendered: &[RenderedArtifact],
    adapters: &AdapterRegistry,
    mut evidence: Vec<EvidenceRecord>,
) -> CompilerResult<CompilerManifest> {
    if !plan.has_mutations()
        && let Some(previous_manifest) = previous_manifest
    {
        return Ok(previous_manifest.clone());
    }
    let rendered_by_id = rendered
        .iter()
        .map(|artifact| (artifact.target_id.as_str(), artifact))
        .collect::<BTreeMap<_, _>>();
    let previous_by_id = previous_manifest
        .map(|manifest| {
            manifest
                .outputs
                .iter()
                .map(|output| (output.target_id.as_str(), output))
                .collect::<BTreeMap<_, _>>()
        })
        .unwrap_or_default();
    let action_by_path = plan
        .actions
        .iter()
        .filter(|action| action.scope == PlanActionScope::Artifact)
        .map(|action| (action.path.as_str(), action))
        .collect::<BTreeMap<_, _>>();

    let mut outputs = Vec::new();
    let mut adapter_ids = BTreeSet::new();
    for target in &request.targets {
        let target_path = join_portable(&request.output_root, &target.relative_path);
        let action = action_by_path.get(target_path.as_str()).ok_or_else(|| {
            CompilerError::new(
                FailureKind::Invalid,
                Diagnostic::error(
                    "IDN2009",
                    FailureKind::Invalid,
                    Some(target.relative_path.clone()),
                    format!("target {:?} has no plan action", target.id),
                    "Recreate the plan from the exact execution request.",
                ),
            )
        })?;
        if action.operation == PlanOperation::Blocked {
            return Err(CompilerError::new(
                FailureKind::Blocked,
                Diagnostic::error(
                    "IDN2010",
                    FailureKind::Blocked,
                    Some(action.path.clone()),
                    "blocked plan action cannot produce a manifest",
                    "Resolve the blocking diagnostic and create a new plan.",
                ),
            ));
        }
        adapter_ids.insert(action.adapter_id.clone());
        let (sha256, bytes) = match action.operation {
            PlanOperation::Create | PlanOperation::Replace => {
                let artifact = rendered_by_id.get(target.id.as_str()).ok_or_else(|| {
                    CompilerError::new(
                        FailureKind::Partial,
                        Diagnostic::error(
                            "IDN2204",
                            FailureKind::Partial,
                            Some(action.path.clone()),
                            "rendered artifact is missing before manifest assembly",
                            "Retry rendering from the accepted plan without applying partial state.",
                        ),
                    )
                })?;
                (sha256_hex(&artifact.bytes), byte_len(&artifact.bytes)?)
            }
            PlanOperation::Unchanged => {
                let previous = previous_by_id.get(target.id.as_str()).ok_or_else(|| {
                    CompilerError::new(
                        FailureKind::Drifted,
                        Diagnostic::error(
                            "IDN2307",
                            FailureKind::Drifted,
                            Some(action.path.clone()),
                            "unchanged target has no previous manifest evidence",
                            "Recreate the target so its output can be verified and manifested.",
                        ),
                    )
                })?;
                (previous.sha256.clone(), previous.bytes)
            }
            PlanOperation::Remove => continue,
            PlanOperation::Blocked => unreachable!("blocked actions are rejected above"),
        };
        outputs.push(ManifestOutput {
            target_id: target.id.clone(),
            profile: target.profile.clone(),
            path: action.path.clone(),
            media_type: target.media_type.clone(),
            adapter_id: action.adapter_id.clone(),
            adapter_version: action.adapter_version.clone(),
            input_fingerprint: action.input_fingerprint.clone(),
            sha256,
            bytes,
        });
    }
    outputs.sort_by(|left, right| left.path.cmp(&right.path));

    let mut descriptors = adapter_ids
        .into_iter()
        .filter_map(|adapter_id| adapters.descriptor(&adapter_id))
        .collect::<Vec<_>>();
    descriptors.sort_by(|left, right| left.id.cmp(&right.id));
    evidence.sort_by(|left, right| {
        left.target_id
            .cmp(&right.target_id)
            .then_with(|| left.check.cmp(&right.check))
    });

    Ok(CompilerManifest {
        schema: COMPILER_MANIFEST_SCHEMA.to_owned(),
        project_id: identity.project_id.clone(),
        source_digest: identity.source_digest.clone(),
        plan_digest: plan.plan_digest.clone(),
        outputs,
        adapters: descriptors,
        evidence,
    })
}

fn blocked_action(target: &ProjectionTarget, path: &str) -> PlanAction {
    PlanAction {
        scope: PlanActionScope::Artifact,
        target_id: target.id.clone(),
        path: path.to_owned(),
        adapter_id: target.adapter_id.clone(),
        adapter_version: String::new(),
        operation: PlanOperation::Blocked,
        input_fingerprint: String::new(),
        current_sha256: None,
        current_bytes: None,
        previous_sha256: None,
        required_approvals: BTreeSet::new(),
        warnings: Vec::new(),
    }
}

fn blocked_action_with_descriptor(
    target: &ProjectionTarget,
    path: &str,
    descriptor: &AdapterDescriptor,
) -> PlanAction {
    PlanAction {
        adapter_version: descriptor.version.clone(),
        ..blocked_action(target, path)
    }
}

fn input_fingerprint(
    identity: &ResolvedIdentity,
    target: &ProjectionTarget,
    descriptor: &AdapterDescriptor,
) -> CompilerResult<String> {
    #[derive(Serialize)]
    #[serde(rename_all = "camelCase")]
    struct Fingerprint<'a> {
        source_digest: &'a str,
        target: &'a ProjectionTarget,
        adapter: &'a AdapterDescriptor,
    }

    canonical_hash(&Fingerprint {
        source_digest: &identity.source_digest,
        target,
        adapter: descriptor,
    })
}

fn plan_digest(plan: &CompilerPlan) -> CompilerResult<String> {
    let mut normalized = plan.clone();
    normalized.plan_digest.clear();
    canonical_hash(&normalized)
}

fn canonical_hash(value: &impl Serialize) -> CompilerResult<String> {
    let bytes = serde_json::to_vec(value).map_err(|error| {
        CompilerError::new(
            FailureKind::Failed,
            Diagnostic::error(
                "IDN2205",
                FailureKind::Failed,
                None,
                format!("cannot serialize deterministic compiler state: {error}"),
                "Report the compiler serialization failure; no generated state was changed.",
            ),
        )
    })?;
    Ok(sha256_hex(&bytes))
}

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

fn byte_len(bytes: &[u8]) -> CompilerResult<u64> {
    u64::try_from(bytes.len()).map_err(|error| {
        CompilerError::new(
            FailureKind::Failed,
            Diagnostic::error(
                "IDN2207",
                FailureKind::Failed,
                None,
                format!("artifact length cannot be represented as u64: {error}"),
                "Use an artifact size supported by the current compiler platform.",
            ),
        )
    })
}

pub(crate) fn validate_portable_path(path: &str, label: &str) -> CompilerResult<()> {
    if path.is_empty()
        || path.starts_with('/')
        || path.ends_with('/')
        || path.contains('\\')
        || path
            .split('/')
            .any(|segment| segment.is_empty() || matches!(segment, "." | ".."))
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

fn valid_identifier(value: &str) -> bool {
    !value.is_empty()
        && value.bytes().enumerate().all(|(index, byte)| {
            byte.is_ascii_lowercase()
                || byte.is_ascii_digit()
                || (byte == b'-' && index > 0 && index + 1 < value.len())
        })
        && !value.contains("--")
}

fn valid_sha256(value: &str) -> bool {
    value.len() == 64
        && value
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
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
