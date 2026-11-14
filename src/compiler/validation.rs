// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

//! Internal compiler validation responsibilities; public contracts remain in the parent.

use super::{
    AdapterDescriptor, BTreeSet, CompilerError, CompilerRequest, CompilerResult, Diagnostic,
    FailureKind, IdentityIntent, ResolvedIdentity, join_portable, validate_portable_path,
};

pub(super) fn validate_adapter_descriptor(descriptor: &AdapterDescriptor) -> CompilerResult<()> {
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

pub(super) fn validate_request(request: &CompilerRequest) -> CompilerResult<()> {
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

pub(super) fn validate_intent(intent: &IdentityIntent) -> CompilerResult<()> {
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

pub(super) fn validate_resolved_identity(identity: &ResolvedIdentity) -> CompilerResult<()> {
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

pub(super) fn valid_identifier(value: &str) -> bool {
    !value.is_empty()
        && value.bytes().enumerate().all(|(index, byte)| {
            byte.is_ascii_lowercase()
                || byte.is_ascii_digit()
                || (byte == b'-' && index > 0 && index + 1 < value.len())
        })
        && !value.contains("--")
}

pub(super) fn valid_sha256(value: &str) -> bool {
    value.len() == 64
        && value
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
}
