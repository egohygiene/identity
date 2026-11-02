// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

use std::collections::{BTreeMap, BTreeSet};

use serde::{Deserialize, Serialize};
use serde_json::Value;

use crate::compiler::{CompilerError, CompilerResult, Diagnostic, FailureKind, ResolvedIdentity};

pub const BRAND_KIT_MODEL_SCHEMA: &str = "identity.brand-kit-model/v1";

#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct BrandKitProject {
    pub display_name: String,
    pub repository: String,
    pub tagline: String,
}

#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct BrandKitToken {
    #[serde(rename = "type")]
    pub token_type: String,
    pub value: Value,
    pub source_layer: String,
    #[serde(default)]
    pub override_reason: Option<String>,
    #[serde(default)]
    pub approval: Option<String>,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct BrandKitLicense {
    pub spdx: String,
    pub status: String,
    #[serde(default)]
    pub attribution: String,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct BrandKitOrigin {
    pub creator: String,
    pub method: String,
    pub source: String,
    pub captured_at: String,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct BrandKitAssetUsage {
    pub safe_zone: String,
    pub minimum_size: String,
    pub restrictions: Vec<String>,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct BrandKitSourceGovernance {
    pub license: BrandKitLicense,
    pub origin: BrandKitOrigin,
    pub approval: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub usage: Option<BrandKitAssetUsage>,
}

#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct BrandKitSourceAsset {
    pub media_type: String,
    pub text: String,
    pub sha256: String,
    pub alt_text: String,
    #[serde(default)]
    pub safe_zone: Option<f64>,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct BrandKitPublicAsset {
    pub label: String,
    pub kind: String,
    pub notes: String,
    pub download_name: String,
}

#[derive(Clone, Debug, Default, Deserialize, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct BrandKitGuidance {
    #[serde(default)]
    pub voice: Option<Value>,
    #[serde(default)]
    pub usage: Option<Value>,
}

#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct BrandKitModel {
    pub schema: String,
    pub project_id: String,
    pub source_digest: String,
    pub project: BrandKitProject,
    pub tokens: BTreeMap<String, BrandKitToken>,
    pub sources: BTreeMap<String, BrandKitSourceAsset>,
    #[serde(default)]
    pub source_governance: BTreeMap<String, BrandKitSourceGovernance>,
    #[serde(default)]
    pub approvals: BTreeSet<String>,
    #[serde(default)]
    pub guidance: BrandKitGuidance,
}

impl BrandKitModel {
    /// Select only affirmative current public declarations from governed usage.
    /// Provenance approval alone does not declare an asset public.
    #[must_use]
    pub fn public_assets(&self) -> BTreeMap<String, BrandKitPublicAsset> {
        self.guidance
            .usage
            .as_ref()
            .and_then(|usage| usage.get("assets"))
            .and_then(Value::as_array)
            .into_iter()
            .flatten()
            .filter_map(|asset| {
                let governance = asset.get("governance")?;
                if asset.get("status")?.as_str()? != "active"
                    || asset.get("availability")?.as_str()? != "public"
                    || governance.get("state")?.as_str()? != "approved"
                    || governance.get("visibility")?.as_str()? != "public"
                    || !self
                        .approvals
                        .contains(governance.get("approval")?.as_str()?)
                {
                    return None;
                }
                let id = asset.get("id")?.as_str()?;
                self.sources.get(id)?;
                let rights = self.source_governance.get(id)?;
                if rights.license.status != "approved" || !self.approvals.contains(&rights.approval)
                {
                    return None;
                }
                Some((
                    id.to_owned(),
                    BrandKitPublicAsset {
                        label: asset.get("label")?.as_str()?.to_owned(),
                        kind: asset.get("kind")?.as_str()?.to_owned(),
                        notes: asset.get("notes")?.as_str()?.to_owned(),
                        download_name: asset.get("downloadName")?.as_str()?.to_owned(),
                    },
                ))
            })
            .collect()
    }

    pub fn from_resolved(identity: &ResolvedIdentity) -> CompilerResult<Self> {
        let project = parse_value::<BrandKitProject>(identity, "project")?;
        let tokens = parse_value::<BTreeMap<String, BrandKitToken>>(identity, "tokens")?;
        let sources = parse_value::<BTreeMap<String, BrandKitSourceAsset>>(identity, "sources")?;
        let source_governance = optional_value::<BTreeMap<String, BrandKitSourceGovernance>>(
            identity,
            "sourceGovernance",
        )?
        .unwrap_or_default();
        let guidance =
            optional_value::<BrandKitGuidance>(identity, "guidance")?.unwrap_or_default();

        if tokens.is_empty() {
            return Err(model_error(
                "tokens",
                "resolved Brand Kit contains no semantic tokens".to_owned(),
            ));
        }
        if sources.is_empty() {
            return Err(model_error(
                "sources",
                "resolved Brand Kit contains no approved source assets".to_owned(),
            ));
        }

        Ok(Self {
            schema: BRAND_KIT_MODEL_SCHEMA.to_owned(),
            project_id: identity.project_id.clone(),
            source_digest: identity.source_digest.clone(),
            project,
            tokens,
            sources,
            source_governance,
            approvals: identity.approvals.clone(),
            guidance,
        })
    }

    pub fn token(&self, path: &str) -> CompilerResult<&BrandKitToken> {
        self.tokens.get(path).ok_or_else(|| {
            model_error(
                path,
                format!("required semantic token {path:?} is absent from the resolved identity"),
            )
        })
    }

    pub fn source(&self, role: &str) -> CompilerResult<&BrandKitSourceAsset> {
        self.sources.get(role).ok_or_else(|| {
            model_error(
                role,
                format!(
                    "required approved source role {role:?} is absent from the resolved identity"
                ),
            )
        })
    }
}

fn parse_value<T>(identity: &ResolvedIdentity, key: &str) -> CompilerResult<T>
where
    T: for<'de> Deserialize<'de>,
{
    let value = identity.values.get(key).cloned().ok_or_else(|| {
        model_error(
            key,
            format!("resolved identity is missing the {key:?} Brand Kit projection input"),
        )
    })?;
    serde_json::from_value(value).map_err(|error| model_error(key, error.to_string()))
}

fn optional_value<T>(identity: &ResolvedIdentity, key: &str) -> CompilerResult<Option<T>>
where
    T: for<'de> Deserialize<'de>,
{
    identity
        .values
        .get(key)
        .cloned()
        .map(serde_json::from_value)
        .transpose()
        .map_err(|error| model_error(key, error.to_string()))
}

fn model_error(path: &str, message: String) -> CompilerError {
    CompilerError::new(
        FailureKind::Invalid,
        Diagnostic::error(
            "IDN3101",
            FailureKind::Invalid,
            Some(path.to_owned()),
            message,
            "Resolve the validated Identity v1 source into the documented Brand Kit model before rendering packages.",
        ),
    )
}
