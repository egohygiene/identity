// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

//! Internal motion artifacts responsibilities; public contracts remain in the parent.

use super::{
    HumanReviewEvidence, MotionPolicy, QualityCategory, QualityCheck, QualityStatus,
    VisualMotionAsset, human_review_check, make_check, sha256_hex, status,
};

#[allow(clippy::too_many_lines)]
pub(super) fn output_checks(
    policy: &MotionPolicy,
    asset: &VisualMotionAsset,
    bytes: &[u8],
) -> Vec<QualityCheck> {
    let output = &asset.output;
    let actual_bytes = u64::try_from(bytes.len()).unwrap_or(u64::MAX);
    let digest_valid = sha256_hex(bytes) == output.sha256 && actual_bytes == output.bytes;
    let byte_budget = actual_bytes <= policy.byte_budget(asset.behavior.purpose);
    let dimensions = output.width > 0
        && output.height > 0
        && output.width <= policy.maximum_dimension_pixels
        && output.height <= policy.maximum_dimension_pixels;
    let frame_rate = output
        .frame_rate
        .is_none_or(|value| value.is_finite() && value > 0.0 && value <= policy.maximum_frame_rate);
    let duration = match policy.duration_budget(asset.behavior.purpose) {
        Some(maximum) => output.duration_ms.is_some_and(|value| value <= maximum),
        None => output.duration_ms.is_none_or(|value| value == 0),
    };

    vec![
        make_check(
            format!("motion.output-digest.{}", asset.id),
            QualityCategory::Reproducibility,
            status(digest_valid),
            true,
            true,
            Some(asset.id.clone()),
            Some(asset.source.reference.clone()),
            Some(output.path.clone()),
            if digest_valid {
                "Generated asset bytes match the visual-motion manifest digest and byte count."
            } else {
                "Generated asset bytes drift from the visual-motion manifest."
            },
            "Discard the drifted asset and regenerate from the recorded source/fixture.",
        ),
        make_check(
            format!("motion.file-size.{}", asset.id),
            QualityCategory::Performance,
            status(byte_budget),
            true,
            true,
            Some(asset.id.clone()),
            Some(asset.source.reference.clone()),
            Some(output.path.clone()),
            format!(
                "Generated asset is {actual_bytes} bytes; purpose budget is {} bytes.",
                policy.byte_budget(asset.behavior.purpose)
            ),
            "Optimize the asset or explicitly version a different purpose/profile budget.",
        ),
        make_check(
            format!("motion.dimensions.{}", asset.id),
            QualityCategory::Performance,
            status(dimensions),
            true,
            true,
            Some(asset.id.clone()),
            Some(asset.source.reference.clone()),
            Some(output.path.clone()),
            format!(
                "Generated asset dimensions are {}x{}.",
                output.width, output.height
            ),
            "Resize the capture/asset within the configured maximum output dimension.",
        ),
        make_check(
            format!("motion.frame-rate.{}", asset.id),
            QualityCategory::Performance,
            status(frame_rate),
            true,
            true,
            Some(asset.id.clone()),
            Some(asset.source.reference.clone()),
            Some(output.path.clone()),
            match output.frame_rate {
                Some(value) => format!("Generated asset frame rate is {value:.2} fps."),
                None => "Generated asset has no frame-rate field for this format.".to_owned(),
            },
            "Keep captured motion at or below the configured frame-rate budget.",
        ),
        make_check(
            format!("motion.duration.{}", asset.id),
            QualityCategory::Accessibility,
            status(duration),
            true,
            true,
            Some(asset.id.clone()),
            Some(asset.source.reference.clone()),
            Some(output.path.clone()),
            match (
                output.duration_ms,
                policy.duration_budget(asset.behavior.purpose),
            ) {
                (Some(value), Some(maximum)) => format!(
                    "Generated motion duration is {value} ms; purpose budget is {maximum} ms."
                ),
                (None, Some(maximum)) => {
                    format!("Generated motion has no duration; purpose budget is {maximum} ms.")
                }
                _ => "Static imagery has no motion duration budget.".to_owned(),
            },
            "Shorten the motion or intentionally version a different purpose-specific budget.",
        ),
    ]
}

pub(super) fn baseline_check(
    reviews: &[HumanReviewEvidence],
    asset: &VisualMotionAsset,
    baseline: Option<&crate::quality::VisualBaseline>,
    bytes: &[u8],
) -> QualityCheck {
    let check_id = format!("visual.regression.{}", asset.baseline_target_id);
    let Some(baseline) = baseline else {
        return human_review_check(
            reviews,
            check_id,
            QualityCategory::VisualIntegrity,
            &asset.id,
            &asset.source.reference,
            &asset.output.path,
            "No approved visual baseline exists for this generated surface.",
            "Review the generated surface and record an approved baseline before release.",
        );
    };
    if baseline.sha256 == sha256_hex(bytes) {
        return make_check(
            check_id,
            QualityCategory::VisualIntegrity,
            QualityStatus::Passed,
            true,
            true,
            Some(asset.id.clone()),
            Some(baseline.source_context.clone()),
            Some(baseline.generated_context.clone()),
            "Generated visual-motion bytes match the approved baseline.",
            "No recovery required.",
        );
    }
    human_review_check(
        reviews,
        check_id,
        QualityCategory::VisualIntegrity,
        &asset.id,
        &baseline.source_context,
        &baseline.generated_context,
        "Generated visual-motion bytes differ from the approved baseline.",
        "Compare source/generated context and record an explicit human decision before release.",
    )
}
