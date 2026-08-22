// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

use std::collections::BTreeMap;

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
    pub guidance: BrandKitGuidance,
}

impl BrandKitModel {
    pub fn from_resolved(identity: &ResolvedIdentity) -> CompilerResult<Self> {
        let project = parse_value::<BrandKitProject>(identity, "project")?;
        let tokens = parse_value::<BTreeMap<String, BrandKitToken>>(identity, "tokens")?;
        let sources = parse_value::<BTreeMap<String, BrandKitSourceAsset>>(identity, "sources")?;
        let guidance = identity
            .values
            .get("guidance")
            .cloned()
            .map(serde_json::from_value)
            .transpose()
            .map_err(|error| model_error("guidance", error.to_string()))?
            .unwrap_or_default();

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
