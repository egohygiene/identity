// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

//! Consumer-owned Identity v1 source adapter.
//!
//! The compiler intentionally receives framework-neutral intent and resolved
//! data.  This adapter is the small, reusable boundary that turns the published
//! on-disk v1 contract into those compiler inputs.  Consumer repositories call
//! it through the `identity v1-*` commands; they never reproduce token merging
//! or package rendering locally.

use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::path::{Path, PathBuf};

use serde_json::{Map, Value};

use crate::brandkit::{
    BrandKitGuidance, BrandKitLicense, BrandKitOrigin, BrandKitProject, BrandKitSourceAsset,
    BrandKitSourceGovernance, BrandKitToken, ProfileSelection,
};
use crate::compiler::{
    CompilerError, CompilerResult, Diagnostic, FailureKind, IdentityIntent, IdentityReader,
    IdentityResolver, IdentityValidator, ResolvedIdentity, ValidationReport, sha256_hex,
};

/// Reusable, immutable in-memory view of one validated v1 consumer source.
#[derive(Clone, Debug)]
pub struct V1ConsumerPipeline {
    intent: IdentityIntent,
    resolved: ResolvedIdentity,
    profiles: Vec<ProfileSelection>,
}

impl V1ConsumerPipeline {
    /// Load local v1 source. Call the standalone validator first for its full,
    /// stable diagnostics; this loader then supplies the compiler's model.
    pub fn load(repository_root: &Path) -> CompilerResult<Self> {
        let project_path = repository_root.join(".identity/identity.json");
        let project = read_json(&project_path, ".identity/identity.json")?;
        let project_object = object(&project, ".identity/identity.json")?;
        let project_metadata = object_field(project_object, "project", "identity project")?;
        let project_id = string_field(project_metadata, "id", "project.id")?.to_owned();

        let documents = object_field(project_object, "documents", "identity project")?;
        let targets_path = path_field(documents, "targets", "documents.targets")?;
        let approvals_path = path_field(documents, "approvals", "documents.approvals")?;
        let provenance_path = path_field(documents, "provenance", "documents.provenance")?;
        let guidance = object_field(documents, "guidance", "documents.guidance")?;
        let voice_path = path_field(guidance, "voice", "documents.guidance.voice")?;
        let usage_path = path_field(guidance, "usage", "documents.guidance.usage")?;

        let source_digest = canonical_source_digest(repository_root)?;
        let profiles = profile_selection(repository_root, &targets_path)?;
        let approvals = approved_decisions(repository_root, &approvals_path)?;
        let tokens = resolve_tokens(repository_root, project_object)?;
        let (sources, source_governance) =
            source_assets(repository_root, &provenance_path, &approvals)?;
        let guidance = BrandKitGuidance {
            voice: Some(read_json(&repository_root.join(&voice_path), &voice_path)?),
            usage: Some(read_json(&repository_root.join(&usage_path), &usage_path)?),
        };
        let project_model = BrandKitProject {
            display_name: string_field(project_metadata, "displayName", "project.displayName")?
                .to_owned(),
            repository: string_field(project_metadata, "repository", "project.repository")?
                .to_owned(),
            tagline: string_field(project_metadata, "tagline", "project.tagline")?.to_owned(),
        };
        let values = BTreeMap::from([
            (
                "project".to_owned(),
                serde_json::to_value(project_model).map_err(|error| {
                    invalid(
                        "project",
                        format!("cannot serialize project model: {error}"),
                    )
                })?,
            ),
            (
                "tokens".to_owned(),
                serde_json::to_value(tokens).map_err(|error| {
                    invalid(
                        "tokens",
                        format!("cannot serialize resolved tokens: {error}"),
                    )
                })?,
            ),
            (
                "sources".to_owned(),
                serde_json::to_value(sources).map_err(|error| {
                    invalid(
                        "sources",
                        format!("cannot serialize source assets: {error}"),
                    )
                })?,
            ),
            (
                "sourceGovernance".to_owned(),
                serde_json::to_value(source_governance).map_err(|error| {
                    invalid(
                        "sourceGovernance",
                        format!("cannot serialize source governance: {error}"),
                    )
                })?,
            ),
            (
                "guidance".to_owned(),
                serde_json::to_value(guidance).map_err(|error| {
                    invalid("guidance", format!("cannot serialize guidance: {error}"))
                })?,
            ),
        ]);
        let intent = IdentityIntent {
            project_id: project_id.clone(),
            source_digest: source_digest.clone(),
            documents: BTreeMap::new(),
            approvals: approvals.clone(),
        };
        let resolved = ResolvedIdentity {
            project_id,
            source_digest,
            values,
            lineage: BTreeMap::new(),
            approvals,
        };
        Ok(Self {
            intent,
            resolved,
            profiles,
        })
    }

    #[must_use]
    pub fn profiles(&self) -> &[ProfileSelection] {
        &self.profiles
    }
}

impl IdentityReader for V1ConsumerPipeline {
    fn read(&self) -> CompilerResult<IdentityIntent> {
        Ok(self.intent.clone())
    }
}

impl IdentityValidator for V1ConsumerPipeline {
    fn validate(&self, _intent: &IdentityIntent) -> CompilerResult<ValidationReport> {
        // The Python stdlib validator is the published, complete v1 source
        // diagnostic contract. This adapter receives only a preflight-valid
        // source and prevents the compiler from inventing a second schema.
        Ok(ValidationReport::default())
    }
}

impl IdentityResolver for V1ConsumerPipeline {
    fn resolve(&self, _intent: &IdentityIntent) -> CompilerResult<ResolvedIdentity> {
        Ok(self.resolved.clone())
    }
}

#[derive(Clone, Debug)]
struct RawToken {
    token_type: String,
    value: Value,
    source_layer: String,
    override_reason: Option<String>,
    approval: Option<String>,
}

fn resolve_tokens(
    repository_root: &Path,
    project: &Map<String, Value>,
) -> CompilerResult<BTreeMap<String, BrandKitToken>> {
    let layers = array_field(project, "layers", "identity project")?;
    let mut raw = BTreeMap::new();
    for layer in layers {
        let layer = object(layer, "layer")?;
        let layer_id = string_field(layer, "id", "layer.id")?.to_owned();
        let token_path = path_field(layer, "tokens", "layer.tokens")?;
        let tokens = read_json(&repository_root.join(&token_path), &token_path)?;
        flatten_tokens(&tokens, "", None, &layer_id, &mut raw)?;
    }
    let mut resolved = BTreeMap::new();
    for path in raw.keys() {
        let mut chain = BTreeSet::new();
        let token = resolve_token(path, &raw, &mut chain)?;
        resolved.insert(path.clone(), token);
    }
    Ok(resolved)
}

fn flatten_tokens(
    value: &Value,
    prefix: &str,
    inherited_type: Option<&str>,
    layer_id: &str,
    output: &mut BTreeMap<String, RawToken>,
) -> CompilerResult<()> {
    let node = object(value, prefix)?;
    let current_type = node.get("$type").and_then(Value::as_str).or(inherited_type);
    if let Some(token_value) = node.get("$value") {
        let token_type = current_type.ok_or_else(|| {
            invalid(
                prefix,
                "a DTCG token must declare or inherit $type before it can be packaged",
            )
        })?;
        let (override_reason, approval) = override_metadata(node);
        output.insert(
            prefix.to_owned(),
            RawToken {
                token_type: token_type.to_owned(),
                value: token_value.clone(),
                source_layer: layer_id.to_owned(),
                override_reason,
                approval,
            },
        );
        return Ok(());
    }
    for (key, child) in node {
        if key.starts_with('$') {
            continue;
        }
        let path = if prefix.is_empty() {
            key.to_owned()
        } else {
            format!("{prefix}.{key}")
        };
        flatten_tokens(child, &path, current_type, layer_id, output)?;
    }
    Ok(())
}

fn override_metadata(node: &Map<String, Value>) -> (Option<String>, Option<String>) {
    let override_value = node
        .get("$extensions")
        .and_then(Value::as_object)
        .and_then(|extensions| extensions.get("org.egohygiene.identity"))
        .and_then(Value::as_object)
        .and_then(|identity| identity.get("override"))
        .and_then(Value::as_object);
    let reason = override_value
        .and_then(|value| value.get("reason"))
        .and_then(Value::as_str)
        .map(str::to_owned);
    let approval = override_value
        .and_then(|value| value.get("approval"))
        .and_then(Value::as_str)
        .map(str::to_owned);
    (reason, approval)
}

fn resolve_token(
    path: &str,
    raw: &BTreeMap<String, RawToken>,
    chain: &mut BTreeSet<String>,
) -> CompilerResult<BrandKitToken> {
    if !chain.insert(path.to_owned()) {
        return Err(invalid(path, "token aliases form a cycle"));
    }
    let token = raw
        .get(path)
        .ok_or_else(|| invalid(path, "token alias does not resolve to a declared token"))?;
    let value = if let Some(alias) = token
        .value
        .as_str()
        .and_then(|value| value.strip_prefix('{'))
        .and_then(|value| value.strip_suffix('}'))
    {
        resolve_token(alias, raw, chain)?.value
    } else {
        token.value.clone()
    };
    chain.remove(path);
    Ok(BrandKitToken {
        token_type: token.token_type.clone(),
        value,
        source_layer: token.source_layer.clone(),
        override_reason: token.override_reason.clone(),
        approval: token.approval.clone(),
    })
}

fn profile_selection(
    repository_root: &Path,
    targets_path: &str,
) -> CompilerResult<Vec<ProfileSelection>> {
    let targets = read_json(&repository_root.join(targets_path), targets_path)?;
    let targets = object(&targets, targets_path)?;
    let enabled = array_field(targets, "enabled", targets_path)?;
    let mut result = Vec::new();
    for item in enabled {
        let item = object(item, targets_path)?;
        result.push(ProfileSelection {
            id: string_field(item, "id", "profile.id")?.to_owned(),
            version: string_field(item, "version", "profile.version")?.to_owned(),
        });
    }
    Ok(result)
}

fn approved_decisions(
    repository_root: &Path,
    approvals_path: &str,
) -> CompilerResult<BTreeSet<String>> {
    let approvals = read_json(&repository_root.join(approvals_path), approvals_path)?;
    let approvals = object(&approvals, approvals_path)?;
    let decisions = array_field(approvals, "decisions", approvals_path)?;
    let mut result = BTreeSet::new();
    for decision in decisions {
        let decision = object(decision, approvals_path)?;
        if decision.get("status").and_then(Value::as_str) == Some("approved") {
            result.insert(string_field(decision, "id", "approval.id")?.to_owned());
        }
    }
    Ok(result)
}

fn source_assets(
    repository_root: &Path,
    provenance_path: &str,
    approvals: &BTreeSet<String>,
) -> CompilerResult<(
    BTreeMap<String, BrandKitSourceAsset>,
    BTreeMap<String, BrandKitSourceGovernance>,
)> {
    let provenance = read_json(&repository_root.join(provenance_path), provenance_path)?;
    let provenance = object(&provenance, provenance_path)?;
    let entries = array_field(provenance, "assets", provenance_path)?;
    let mut sources = BTreeMap::new();
    let mut governance = BTreeMap::new();
    for entry in entries {
        let entry = object(entry, provenance_path)?;
        let id = string_field(entry, "id", "provenance asset.id")?.to_owned();
        let path = path_field(entry, "path", "provenance asset.path")?;
        let bytes = fs::read(repository_root.join(&path)).map_err(|error| {
            invalid(&path, format!("cannot read approved source asset: {error}"))
        })?;
        let text = String::from_utf8(bytes.clone())
            .map_err(|error| invalid(&path, format!("approved source must be UTF-8: {error}")))?;
        let accessibility = object_field(entry, "accessibility", "provenance asset")?;
        let _usage = object_field(entry, "usage", "provenance asset")?;
        let license = object_field(entry, "license", "provenance asset")?;
        let origin = object_field(entry, "origin", "provenance asset")?;
        let approval = string_field(entry, "approval", "provenance asset.approval")?.to_owned();
        if !approvals.contains(&approval) {
            return Err(invalid(
                &path,
                "approved source references a decision that is not approved",
            ));
        }
        let declared = string_field(entry, "sha256", "provenance asset.sha256")?;
        let actual = sha256_hex(&bytes);
        if declared != actual {
            return Err(invalid(
                &path,
                "approved source bytes do not match their provenance digest",
            ));
        }
        sources.insert(
            id.clone(),
            BrandKitSourceAsset {
                media_type: media_type(&path)?.to_owned(),
                text,
                sha256: actual,
                alt_text: string_field(accessibility, "altText", "asset alt text")?.to_owned(),
                safe_zone: None,
            },
        );
        governance.insert(
            id,
            BrandKitSourceGovernance {
                license: BrandKitLicense {
                    spdx: string_field(license, "spdx", "asset license")?.to_owned(),
                    status: string_field(license, "status", "asset license")?.to_owned(),
                    attribution: string_field(license, "attribution", "asset license")?.to_owned(),
                },
                origin: BrandKitOrigin {
                    creator: string_field(origin, "creator", "asset origin")?.to_owned(),
                    method: string_field(origin, "method", "asset origin")?.to_owned(),
                    source: string_field(origin, "source", "asset origin")?.to_owned(),
                    captured_at: string_field(origin, "capturedAt", "asset origin")?.to_owned(),
                },
                approval,
            },
        );
    }
    Ok((sources, governance))
}

fn canonical_source_digest(repository_root: &Path) -> CompilerResult<String> {
    let identity_root = repository_root.join(".identity");
    let mut files = Vec::new();
    collect_canonical_files(&identity_root, &identity_root, &mut files)?;
    files.sort();
    let mut bytes = Vec::new();
    for path in files {
        let relative = path
            .strip_prefix(repository_root)
            .map_err(|error| invalid(".identity", error.to_string()))?
            .to_string_lossy();
        let content = fs::read(&path)
            .map_err(|error| invalid(path.display().to_string(), error.to_string()))?;
        bytes.extend_from_slice(relative.as_bytes());
        bytes.push(0);
        bytes.extend_from_slice(&content);
        bytes.push(0);
    }
    Ok(sha256_hex(&bytes))
}

fn collect_canonical_files(
    root: &Path,
    current: &Path,
    files: &mut Vec<PathBuf>,
) -> CompilerResult<()> {
    for entry in fs::read_dir(current)
        .map_err(|error| invalid(current.display().to_string(), error.to_string()))?
    {
        let entry =
            entry.map_err(|error| invalid(current.display().to_string(), error.to_string()))?;
        let path = entry.path();
        let relative = path
            .strip_prefix(root)
            .map_err(|error| invalid(root.display().to_string(), error.to_string()))?;
        if relative == Path::new("identity.toml")
            || relative.file_name().is_some_and(|name| name == "README.md")
        {
            continue;
        }
        if relative.components().next().is_some_and(|component| {
            matches!(
                component.as_os_str().to_str(),
                Some("candidates" | "references")
            )
        }) {
            continue;
        }
        if path.is_dir() {
            collect_canonical_files(root, &path, files)?;
        } else if path.is_file() {
            files.push(path);
        }
    }
    Ok(())
}

fn read_json(path: &Path, label: &str) -> CompilerResult<Value> {
    let content = fs::read_to_string(path)
        .map_err(|error| invalid(label, format!("cannot read JSON: {error}")))?;
    serde_json::from_str(&content).map_err(|error| invalid(label, format!("invalid JSON: {error}")))
}

fn object<'a>(value: &'a Value, label: &str) -> CompilerResult<&'a Map<String, Value>> {
    value
        .as_object()
        .ok_or_else(|| invalid(label, "expected a JSON object"))
}

fn object_field<'a>(
    object: &'a Map<String, Value>,
    field: &str,
    label: &str,
) -> CompilerResult<&'a Map<String, Value>> {
    object
        .get(field)
        .and_then(Value::as_object)
        .ok_or_else(|| invalid(format!("{label}.{field}"), "expected a JSON object"))
}

fn array_field<'a>(
    object: &'a Map<String, Value>,
    field: &str,
    label: &str,
) -> CompilerResult<&'a Vec<Value>> {
    object
        .get(field)
        .and_then(Value::as_array)
        .ok_or_else(|| invalid(format!("{label}.{field}"), "expected a JSON array"))
}

fn string_field<'a>(
    object: &'a Map<String, Value>,
    field: &str,
    label: &str,
) -> CompilerResult<&'a str> {
    object
        .get(field)
        .and_then(Value::as_str)
        .filter(|value| !value.trim().is_empty())
        .ok_or_else(|| invalid(format!("{label}.{field}"), "expected a non-empty string"))
}

fn path_field(object: &Map<String, Value>, field: &str, label: &str) -> CompilerResult<String> {
    let value = string_field(object, field, label)?;
    if value.starts_with('/') || value.contains("..") || value.contains('\\') {
        return Err(invalid(
            format!("{label}.{field}"),
            "path must be repository-relative",
        ));
    }
    Ok(value.to_owned())
}

fn media_type(path: &str) -> CompilerResult<&'static str> {
    match Path::new(path).extension().and_then(|value| value.to_str()) {
        Some("svg") => Ok("image/svg+xml"),
        _ => Err(invalid(
            path,
            "only canonical SVG source assets are packageable in v1",
        )),
    }
}

fn invalid(path: impl Into<String>, message: impl Into<String>) -> CompilerError {
    CompilerError::new(
        FailureKind::Invalid,
        Diagnostic::error(
            "IDN3301",
            FailureKind::Invalid,
            Some(path.into()),
            message.into(),
            "Run the published Identity v1 validator, then correct the consumer-owned source.",
        ),
    )
}
