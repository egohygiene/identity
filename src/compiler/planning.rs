// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

//! Internal compiler planning responsibilities; public contracts remain in the parent.

use super::{
    AdapterDescriptor, AdapterRegistry, ArtifactStore, BTreeMap, BTreeSet, COMPILER_API_MAJOR,
    COMPILER_MANIFEST_SCHEMA, COMPILER_PLAN_SCHEMA, CompatibilityRecord, CompilerError,
    CompilerManifest, CompilerPlan, CompilerRequest, CompilerResult, Diagnostic, EvidenceRecord,
    FailureKind, ManifestOutput, PlanAction, PlanActionScope, PlanOperation, ProjectionTarget,
    RenderedArtifact, ResolvedIdentity, Serialize, join_portable, sha256_hex, sort_diagnostics,
};

pub(super) fn load_manifest(
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

#[allow(clippy::too_many_lines)]
pub(super) fn build_plan(
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

#[allow(clippy::too_many_lines)]
pub(super) fn build_manifest(
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

pub(super) fn blocked_action(target: &ProjectionTarget, path: &str) -> PlanAction {
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

pub(super) fn blocked_action_with_descriptor(
    target: &ProjectionTarget,
    path: &str,
    descriptor: &AdapterDescriptor,
) -> PlanAction {
    PlanAction {
        adapter_version: descriptor.version.clone(),
        ..blocked_action(target, path)
    }
}

pub(super) fn input_fingerprint(
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

pub(super) fn plan_digest(plan: &CompilerPlan) -> CompilerResult<String> {
    let mut normalized = plan.clone();
    normalized.plan_digest.clear();
    canonical_hash(&normalized)
}

pub(super) fn canonical_hash(value: &impl Serialize) -> CompilerResult<String> {
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

pub(super) fn byte_len(bytes: &[u8]) -> CompilerResult<u64> {
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
