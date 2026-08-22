// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

use std::collections::{BTreeMap, BTreeSet};
use std::fs;

use serde::Serialize;
use serde_json::{Value, json};
use tempfile::TempDir;

use super::{
    AdapterDescriptor, AdapterKind, AdapterPlan, AdapterRegistry, Compiler, CompilerError,
    CompilerManifest, CompilerRequest, Diagnostic, DiagnosticSeverity, EvidenceRecord,
    EvidenceStatus, FailureKind, IdentityIntent, IdentityReader, IdentityResolver,
    IdentityValidator, LocalArtifactStore, ManifestOutput, PlanActionScope, PlanOperation,
    ProjectionAdapter, ProjectionTarget, ResolvedIdentity, ValidationReport, VerificationReport,
    manifest_bytes, sha256_hex,
};

const FIXTURE_ADAPTER_ID: &str = "fixture-json";
const FIXTURE_ADAPTER_VERSION: &str = "1.0.0";

#[derive(Clone)]
struct MemoryReader {
    intent: IdentityIntent,
}

impl IdentityReader for MemoryReader {
    fn read(&self) -> super::CompilerResult<IdentityIntent> {
        Ok(self.intent.clone())
    }
}

struct FixtureValidator;

impl IdentityValidator for FixtureValidator {
    fn validate(&self, intent: &IdentityIntent) -> super::CompilerResult<ValidationReport> {
        let diagnostics = if intent.documents.contains_key("invalid") {
            vec![Diagnostic::error(
                "IDN2090",
                FailureKind::Invalid,
                None,
                "fixture intent is invalid",
                "Remove the invalid fixture marker.",
            )]
        } else {
            Vec::new()
        };
        Ok(ValidationReport { diagnostics })
    }
}

struct FixtureResolver;

impl IdentityResolver for FixtureResolver {
    fn resolve(&self, intent: &IdentityIntent) -> super::CompilerResult<ResolvedIdentity> {
        Ok(ResolvedIdentity {
            project_id: intent.project_id.clone(),
            source_digest: intent.source_digest.clone(),
            values: intent.documents.clone(),
            lineage: BTreeMap::from([(
                "color.primary".to_owned(),
                "organization-defaults".to_owned(),
            )]),
            approvals: intent.approvals.clone(),
        })
    }
}

#[derive(Clone)]
struct FixtureAdapter {
    offline: bool,
    deterministic: bool,
    fail_verification: bool,
}

impl FixtureAdapter {
    fn deterministic() -> Self {
        Self {
            offline: true,
            deterministic: true,
            fail_verification: false,
        }
    }

    fn online() -> Self {
        Self {
            offline: false,
            deterministic: true,
            fail_verification: false,
        }
    }

    fn failing_verification() -> Self {
        Self {
            offline: true,
            deterministic: true,
            fail_verification: true,
        }
    }
}

impl ProjectionAdapter for FixtureAdapter {
    fn descriptor(&self) -> AdapterDescriptor {
        AdapterDescriptor {
            id: FIXTURE_ADAPTER_ID.to_owned(),
            version: FIXTURE_ADAPTER_VERSION.to_owned(),
            kind: AdapterKind::Metadata,
            compiler_api_major: 1,
            deterministic: self.deterministic,
            offline: self.offline,
            capabilities: BTreeSet::from(["application-json".to_owned()]),
        }
    }

    fn plan(
        &self,
        _identity: &ResolvedIdentity,
        target: &ProjectionTarget,
    ) -> super::CompilerResult<AdapterPlan> {
        let mut plan = AdapterPlan::default();
        if target.parameters.contains_key("warn") {
            plan.warnings.push("fixture warning".to_owned());
        }
        Ok(plan)
    }

    fn render(
        &self,
        identity: &ResolvedIdentity,
        target: &ProjectionTarget,
    ) -> super::CompilerResult<Vec<u8>> {
        #[derive(Serialize)]
        #[serde(rename_all = "camelCase")]
        struct FixtureProjection<'a> {
            project_id: &'a str,
            source_digest: &'a str,
            target_id: &'a str,
            values: &'a BTreeMap<String, Value>,
            parameters: &'a BTreeMap<String, Value>,
        }

        let mut bytes = serde_json::to_vec_pretty(&FixtureProjection {
            project_id: &identity.project_id,
            source_digest: &identity.source_digest,
            target_id: &target.id,
            values: &identity.values,
            parameters: &target.parameters,
        })
        .expect("fixture projection serializes");
        bytes.push(b'\n');
        Ok(bytes)
    }

    fn verify(
        &self,
        _identity: &ResolvedIdentity,
        target: &ProjectionTarget,
        bytes: &[u8],
    ) -> super::CompilerResult<VerificationReport> {
        if self.fail_verification {
            return Ok(VerificationReport {
                diagnostics: vec![Diagnostic::error(
                    "IDN2290",
                    FailureKind::Failed,
                    Some(target.relative_path.clone()),
                    "fixture verification failed",
                    "Fix the fixture adapter output before applying the plan.",
                )],
                evidence: Vec::new(),
            });
        }
        Ok(VerificationReport {
            diagnostics: Vec::new(),
            evidence: vec![EvidenceRecord {
                target_id: target.id.clone(),
                adapter_id: FIXTURE_ADAPTER_ID.to_owned(),
                check: "non-empty-json".to_owned(),
                status: EvidenceStatus::Verified,
                message: format!("verified {} bytes", bytes.len()),
            }],
        })
    }
}

fn fixture_intent() -> IdentityIntent {
    IdentityIntent {
        project_id: "fixture".to_owned(),
        source_digest: "a".repeat(64),
        documents: BTreeMap::from([
            ("color.primary".to_owned(), json!("#d4af6a")),
            ("spacing.base".to_owned(), json!(8)),
        ]),
        approvals: BTreeSet::new(),
    }
}

fn fixture_target(id: &str, path: &str) -> ProjectionTarget {
    ProjectionTarget {
        id: id.to_owned(),
        profile: "fixture".to_owned(),
        relative_path: path.to_owned(),
        adapter_id: FIXTURE_ADAPTER_ID.to_owned(),
        media_type: "application/json".to_owned(),
        parameters: BTreeMap::from([("format".to_owned(), json!("fixture"))]),
        required_approval: None,
        maximum_bytes: Some(16_384),
    }
}

fn fixture_request(path: &str) -> CompilerRequest {
    CompilerRequest {
        output_root: "assets/identity".to_owned(),
        targets: vec![fixture_target("metadata", path)],
    }
}

fn registry(adapter: FixtureAdapter) -> AdapterRegistry {
    let mut registry = AdapterRegistry::new();
    registry
        .register(adapter)
        .expect("fixture adapter registers");
    registry
}

fn write_previous_manifest(
    temporary: &TempDir,
    output_path: &str,
    output_bytes: &[u8],
) -> CompilerManifest {
    let repository_root = temporary.path();
    let output_file = repository_root.join(output_path);
    fs::create_dir_all(output_file.parent().expect("output has parent")).expect("create output");
    fs::write(&output_file, output_bytes).expect("write prior output");

    let manifest = CompilerManifest {
        schema: super::COMPILER_MANIFEST_SCHEMA.to_owned(),
        project_id: "fixture".to_owned(),
        source_digest: "a".repeat(64),
        plan_digest: "b".repeat(64),
        outputs: vec![ManifestOutput {
            target_id: "stale".to_owned(),
            profile: "fixture".to_owned(),
            path: output_path.to_owned(),
            media_type: "application/json".to_owned(),
            adapter_id: FIXTURE_ADAPTER_ID.to_owned(),
            adapter_version: FIXTURE_ADAPTER_VERSION.to_owned(),
            input_fingerprint: "c".repeat(64),
            sha256: sha256_hex(output_bytes),
            bytes: u64::try_from(output_bytes.len()).expect("fixture length fits u64"),
        }],
        adapters: vec![FixtureAdapter::deterministic().descriptor()],
        evidence: Vec::new(),
    };
    let manifest_path = repository_root.join("assets/identity/.identity-manifest.json");
    fs::write(
        manifest_path,
        manifest_bytes(&manifest).expect("manifest serializes"),
    )
    .expect("write prior manifest");
    manifest
}

#[test]
fn plan_enumerates_create_replace_remove_warnings_and_approvals_without_mutation() {
    let temporary = tempfile::tempdir().expect("create tempdir");
    write_previous_manifest(
        &temporary,
        "assets/identity/stale.json",
        b"{\"stale\":true}\n",
    );
    let unmanaged_path = temporary.path().join("assets/identity/unmanaged.json");
    fs::write(&unmanaged_path, b"manual\n").expect("write unmanaged output");
    let unmanaged_before = fs::read(&unmanaged_path).expect("read unmanaged output");

    let reader = MemoryReader {
        intent: fixture_intent(),
    };
    let validator = FixtureValidator;
    let resolver = FixtureResolver;
    let registry = registry(FixtureAdapter::deterministic());
    let mut store = LocalArtifactStore::new(temporary.path()).expect("create store");
    let mut compiler = Compiler::new(&reader, &validator, &resolver, &registry, &mut store);
    let request = CompilerRequest {
        output_root: "assets/identity".to_owned(),
        targets: vec![
            fixture_target("new", "new.json"),
            ProjectionTarget {
                parameters: BTreeMap::from([("warn".to_owned(), json!(true))]),
                ..fixture_target("unmanaged", "unmanaged.json")
            },
        ],
    };

    let prepared = compiler.prepare(request).expect("prepare compiler plan");
    let artifact_actions = prepared
        .plan
        .actions
        .iter()
        .filter(|action| action.scope == PlanActionScope::Artifact)
        .collect::<Vec<_>>();
    assert_eq!(artifact_actions.len(), 3);
    assert!(artifact_actions.iter().any(|action| {
        action.path == "assets/identity/new.json" && action.operation == PlanOperation::Create
    }));
    assert!(artifact_actions.iter().any(|action| {
        action.path == "assets/identity/unmanaged.json"
            && action.operation == PlanOperation::Replace
            && action.warnings.contains(&"fixture warning".to_owned())
    }));
    assert!(artifact_actions.iter().any(|action| {
        action.path == "assets/identity/stale.json" && action.operation == PlanOperation::Remove
    }));
    assert!(
        prepared
            .plan
            .required_approvals
            .contains("replace-unmanaged:assets/identity/unmanaged.json")
    );
    assert!(
        prepared
            .plan
            .required_approvals
            .contains("remove:assets/identity/stale.json")
    );
    assert_eq!(
        fs::read(&unmanaged_path).expect("read unmanaged after plan"),
        unmanaged_before
    );
    assert!(
        temporary
            .path()
            .join("assets/identity/stale.json")
            .is_file()
    );
    assert!(!temporary.path().join("assets/identity/new.json").exists());
}

#[test]
fn same_input_produces_byte_identical_output_and_manifest() {
    let first = tempfile::tempdir().expect("create first tempdir");
    let second = tempfile::tempdir().expect("create second tempdir");
    let mut outputs = Vec::new();

    for temporary in [&first, &second] {
        let reader = MemoryReader {
            intent: fixture_intent(),
        };
        let validator = FixtureValidator;
        let resolver = FixtureResolver;
        let registry = registry(FixtureAdapter::deterministic());
        let mut store = LocalArtifactStore::new(temporary.path()).expect("create store");
        let mut compiler = Compiler::new(&reader, &validator, &resolver, &registry, &mut store);
        let prepared = compiler
            .prepare(fixture_request("metadata.json"))
            .expect("prepare compiler plan");
        assert!(!prepared.plan.has_blocking_diagnostics());
        let manifest = compiler
            .execute(&prepared, &BTreeSet::new())
            .expect("execute compiler plan");
        outputs.push((
            fs::read(temporary.path().join("assets/identity/metadata.json"))
                .expect("read generated output"),
            manifest_bytes(&manifest).expect("serialize returned manifest"),
            fs::read(
                temporary
                    .path()
                    .join("assets/identity/.identity-manifest.json"),
            )
            .expect("read stored manifest"),
        ));
    }

    assert_eq!(outputs[0], outputs[1]);
}

#[test]
fn second_prepare_is_incremental_and_returns_existing_manifest_without_rewrite() {
    let temporary = tempfile::tempdir().expect("create tempdir");
    let reader = MemoryReader {
        intent: fixture_intent(),
    };
    let validator = FixtureValidator;
    let resolver = FixtureResolver;
    let registry = registry(FixtureAdapter::deterministic());

    let first_manifest = {
        let mut store = LocalArtifactStore::new(temporary.path()).expect("create first store");
        let mut compiler = Compiler::new(&reader, &validator, &resolver, &registry, &mut store);
        let prepared = compiler
            .prepare(fixture_request("metadata.json"))
            .expect("prepare first plan");
        compiler
            .execute(&prepared, &BTreeSet::new())
            .expect("execute first plan")
    };
    let manifest_path = temporary
        .path()
        .join("assets/identity/.identity-manifest.json");
    let before = fs::read(&manifest_path).expect("read first manifest");

    let second_manifest = {
        let mut store = LocalArtifactStore::new(temporary.path()).expect("create second store");
        let mut compiler = Compiler::new(&reader, &validator, &resolver, &registry, &mut store);
        let prepared = compiler
            .prepare(fixture_request("metadata.json"))
            .expect("prepare second plan");
        assert!(
            prepared
                .plan
                .actions
                .iter()
                .all(|action| action.operation == PlanOperation::Unchanged)
        );
        compiler
            .execute(&prepared, &BTreeSet::new())
            .expect("execute unchanged plan")
    };

    assert_eq!(first_manifest, second_manifest);
    assert_eq!(
        before,
        fs::read(manifest_path).expect("read unchanged manifest")
    );
}

#[test]
fn missing_or_networked_adapter_is_visible_and_blocks_execution() {
    let temporary = tempfile::tempdir().expect("create tempdir");
    let reader = MemoryReader {
        intent: fixture_intent(),
    };
    let validator = FixtureValidator;
    let resolver = FixtureResolver;

    let empty_registry = AdapterRegistry::new();
    let mut empty_store = LocalArtifactStore::new(temporary.path()).expect("create store");
    let mut compiler = Compiler::new(
        &reader,
        &validator,
        &resolver,
        &empty_registry,
        &mut empty_store,
    );
    let prepared = compiler
        .prepare(fixture_request("missing.json"))
        .expect("planning records unsupported adapter");
    assert!(prepared.plan.has_blocking_diagnostics());
    assert!(
        prepared
            .plan
            .compatibility
            .iter()
            .any(|record| !record.compatible)
    );
    let error = compiler
        .execute(&prepared, &BTreeSet::new())
        .expect_err("unsupported plan must not execute");
    assert_eq!(error.kind, FailureKind::Blocked);

    let online_registry = registry(FixtureAdapter::online());
    let mut online_store = LocalArtifactStore::new(temporary.path()).expect("create online store");
    let mut online_compiler = Compiler::new(
        &reader,
        &validator,
        &resolver,
        &online_registry,
        &mut online_store,
    );
    let online = online_compiler
        .prepare(fixture_request("online.json"))
        .expect("planning records network boundary");
    assert!(online.plan.diagnostics.iter().any(|diagnostic| {
        diagnostic.code == "IDN2104" && diagnostic.severity == DiagnosticSeverity::Error
    }));
    assert!(
        !temporary
            .path()
            .join("assets/identity/online.json")
            .exists()
    );
}

#[test]
fn verification_failure_never_mutates_generated_state() {
    let temporary = tempfile::tempdir().expect("create tempdir");
    let reader = MemoryReader {
        intent: fixture_intent(),
    };
    let validator = FixtureValidator;
    let resolver = FixtureResolver;
    let registry = registry(FixtureAdapter::failing_verification());
    let mut store = LocalArtifactStore::new(temporary.path()).expect("create store");
    let mut compiler = Compiler::new(&reader, &validator, &resolver, &registry, &mut store);
    let prepared = compiler
        .prepare(fixture_request("failed.json"))
        .expect("prepare plan");
    let error = compiler
        .execute(&prepared, &BTreeSet::new())
        .expect_err("verification failure must abort");
    assert!(matches!(
        error.kind,
        FailureKind::Failed | FailureKind::Partial
    ));
    assert!(
        !temporary
            .path()
            .join("assets/identity/failed.json")
            .exists()
    );
    assert!(
        !temporary
            .path()
            .join("assets/identity/.identity-manifest.json")
            .exists()
    );
}

#[test]
fn interrupted_transaction_can_be_recovered_without_touching_canonical_source() {
    let temporary = tempfile::tempdir().expect("create tempdir");
    fs::create_dir_all(temporary.path().join(".identity")).expect("create canonical directory");
    let canonical_path = temporary.path().join(".identity/identity.json");
    fs::write(&canonical_path, b"canonical\n").expect("write canonical fixture");
    fs::create_dir_all(temporary.path().join("assets/identity")).expect("create output directory");
    let output_path = temporary.path().join("assets/identity/a-existing.json");
    fs::write(&output_path, b"old-generated\n").expect("write old generated output");

    let reader = MemoryReader {
        intent: fixture_intent(),
    };
    let validator = FixtureValidator;
    let resolver = FixtureResolver;
    let registry = registry(FixtureAdapter::deterministic());
    let request = fixture_request("a-existing.json");
    let approval = "replace-unmanaged:assets/identity/a-existing.json".to_owned();

    {
        let mut store = LocalArtifactStore::new(temporary.path())
            .expect("create store")
            .fail_after_mutations(1);
        let mut compiler = Compiler::new(&reader, &validator, &resolver, &registry, &mut store);
        let prepared = compiler.prepare(request).expect("prepare replacement plan");
        let error = compiler
            .execute(&prepared, &BTreeSet::from([approval]))
            .expect_err("simulated interruption must fail commit");
        assert_eq!(error.kind, FailureKind::Failed);
    }

    let mut recovery_store =
        LocalArtifactStore::new(temporary.path()).expect("create recovery store");
    assert!(
        super::ArtifactStore::recovery_required(&recovery_store)
            .expect("inspect recovery requirement")
    );
    let report = super::ArtifactStore::recover(&mut recovery_store).expect("recover transaction");
    assert_eq!(report.recovered_transactions, 1);
    assert_eq!(
        fs::read(&output_path).expect("read restored output"),
        b"old-generated\n"
    );
    assert_eq!(
        fs::read(canonical_path).expect("read canonical source"),
        b"canonical\n"
    );
}

#[test]
fn invalid_source_validation_fails_before_plan_or_generated_reads() {
    let temporary = tempfile::tempdir().expect("create tempdir");
    let mut intent = fixture_intent();
    intent.documents.insert("invalid".to_owned(), json!(true));
    let reader = MemoryReader { intent };
    let validator = FixtureValidator;
    let resolver = FixtureResolver;
    let registry = registry(FixtureAdapter::deterministic());
    let mut store = LocalArtifactStore::new(temporary.path()).expect("create store");
    let mut compiler = Compiler::new(&reader, &validator, &resolver, &registry, &mut store);

    let error = compiler
        .prepare(fixture_request("never.json"))
        .expect_err("invalid source must fail before plan");
    assert_eq!(error.kind, FailureKind::Invalid);
    assert!(!temporary.path().join("assets").exists());
}

#[test]
fn duplicate_adapter_registration_is_rejected() {
    let mut registry = AdapterRegistry::new();
    registry
        .register(FixtureAdapter::deterministic())
        .expect("first adapter registers");
    let error: CompilerError = registry
        .register(FixtureAdapter::deterministic())
        .expect_err("duplicate adapter must be rejected");
    assert_eq!(error.kind, FailureKind::Invalid);
}
