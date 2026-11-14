// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

//! Internal motion provenance responsibilities; public contracts remain in the parent.

use super::{
    MotionPolicy, QualityCategory, QualityCheck, QualityInput, VisualMotionAsset,
    VisualMotionSourceMethod, make_check, status, valid_commit, valid_sha256,
};

pub(super) fn source_checks(
    input: &QualityInput<'_>,
    asset: &VisualMotionAsset,
) -> Vec<QualityCheck> {
    let mut checks = Vec::new();
    let source = &asset.source;
    let valid_base = !source.creator.trim().is_empty()
        && !source.reference.trim().is_empty()
        && valid_sha256(&source.sha256)
        && !source.license_spdx.trim().is_empty();
    checks.push(make_check(
        format!("motion.provenance.source.{}", asset.id),
        QualityCategory::Provenance,
        status(valid_base),
        true,
        true,
        Some(asset.id.clone()),
        Some(source.reference.clone()),
        Some(asset.output.path.clone()),
        if valid_base {
            "Visual-motion source records creator, reference, digest, and license."
        } else {
            "Visual-motion source provenance is incomplete or malformed."
        },
        "Record creator, source reference, SHA-256 digest, and SPDX license before release.",
    ));

    let approved = input.model.approvals.contains(&source.approval);
    checks.push(make_check(
        format!("motion.provenance.approval.{}", asset.id),
        QualityCategory::Provenance,
        status(approved),
        true,
        true,
        Some(asset.id.clone()),
        Some(source.reference.clone()),
        Some(asset.output.path.clone()),
        if approved {
            "Visual-motion source resolves to an approved human decision."
        } else {
            "Visual-motion source approval is absent from the resolved decision set."
        },
        "Approve the canonical source or candidate before deriving visual-motion assets.",
    ));

    let capture_lineage = if source.method == VisualMotionSourceMethod::Captured {
        source
            .repository
            .as_ref()
            .is_some_and(|value| !value.trim().is_empty())
            && source
                .commit
                .as_ref()
                .is_some_and(|value| valid_commit(value))
            && source
                .script_path
                .as_ref()
                .is_some_and(|value| !value.trim().is_empty())
            && source
                .fixture_path
                .as_ref()
                .is_some_and(|value| !value.trim().is_empty())
            && source
                .fixture_sha256
                .as_ref()
                .is_some_and(|value| valid_sha256(value))
    } else {
        true
    };
    checks.push(make_check(
        format!("motion.provenance.capture-lineage.{}", asset.id),
        QualityCategory::Provenance,
        status(capture_lineage),
        true,
        true,
        Some(asset.id.clone()),
        Some(source.reference.clone()),
        Some(asset.output.path.clone()),
        if capture_lineage {
            "Capture lineage is complete for the declared source method."
        } else {
            "Captured asset is missing immutable repository/script/fixture lineage."
        },
        "Record repository, 40-character commit, source script, fixture path, and fixture SHA-256.",
    ));
    checks
}

pub(super) fn capture_checks(
    policy: &MotionPolicy,
    asset: &VisualMotionAsset,
) -> Vec<QualityCheck> {
    let capture = &asset.capture;
    let deterministic = policy.allowed_network_modes.contains(&capture.network_mode);
    let privacy = capture.privacy_safe && capture.synthetic_data;
    let viewport = capture.viewport_width > 0
        && capture.viewport_height > 0
        && capture.viewport_width <= policy.maximum_dimension_pixels
        && capture.viewport_height <= policy.maximum_dimension_pixels;

    vec![
        make_check(
            format!("motion.capture.network.{}", asset.id),
            QualityCategory::Reproducibility,
            status(deterministic),
            true,
            true,
            Some(asset.id.clone()),
            Some(asset.source.reference.clone()),
            Some(asset.output.path.clone()),
            if deterministic {
                "Capture uses an offline or recorded-fixture network mode."
            } else {
                "Capture depends on live network state."
            },
            "Capture against offline or recorded fixtures so the asset is reproducible.",
        ),
        make_check(
            format!("motion.capture.privacy.{}", asset.id),
            QualityCategory::Provenance,
            status(privacy),
            true,
            true,
            Some(asset.id.clone()),
            Some(asset.source.reference.clone()),
            Some(asset.output.path.clone()),
            if privacy {
                "Capture is declared privacy-safe and uses synthetic data."
            } else {
                "Capture is not both privacy-safe and synthetic."
            },
            "Replace captured personal/secret data with deterministic synthetic fixtures.",
        ),
        make_check(
            format!("motion.capture.viewport.{}", asset.id),
            QualityCategory::Performance,
            status(viewport),
            true,
            true,
            Some(asset.id.clone()),
            Some(format!(
                "{}x{} {} {}",
                capture.viewport_width, capture.viewport_height, capture.locale, capture.timezone
            )),
            Some(asset.output.path.clone()),
            if viewport {
                "Capture viewport is within the configured deterministic dimension budget."
            } else {
                "Capture viewport is missing or exceeds the configured dimension budget."
            },
            "Use a versioned viewport no larger than the motion policy maximum dimension.",
        ),
    ]
}
