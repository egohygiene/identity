// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

//! Internal motion behavior responsibilities; public contracts remain in the parent.

use super::{
    CompilerResult, HumanReviewEvidence, MotionPolicy, MotionPurpose, QualityCategory,
    QualityCheck, QualityInput, QualityStatus, ReducedMotionBehavior, VisualMotionAsset,
    human_review_check, make_check, sha256_hex, status, valid_sha256,
};

#[allow(clippy::too_many_lines)]
pub(super) fn behavior_checks(
    policy: &MotionPolicy,
    reviews: &[HumanReviewEvidence],
    asset: &VisualMotionAsset,
) -> Vec<QualityCheck> {
    let behavior = &asset.behavior;
    let properties_valid = if behavior.purpose == MotionPurpose::StaticImagery
        || behavior.purpose == MotionPurpose::DemoCapture
    {
        behavior.animated_properties.is_empty()
            || behavior
                .animated_properties
                .iter()
                .all(|property| policy.allowed_animated_properties.contains(property))
    } else {
        !behavior.animated_properties.is_empty()
            && behavior
                .animated_properties
                .iter()
                .all(|property| policy.allowed_animated_properties.contains(property))
    };
    let easing_valid = behavior.purpose == MotionPurpose::StaticImagery
        || behavior.purpose == MotionPurpose::DemoCapture
        || policy.allowed_easing.contains(&behavior.easing);
    let autoplay_valid = !behavior.autoplay
        || (behavior.purpose == MotionPurpose::LandingSequence
            && behavior.muted
            && !behavior.looped);
    let loop_valid = !behavior.looped || behavior.purpose == MotionPurpose::ContinuousStatus;

    let mut checks = vec![
        make_check(
            format!("motion.properties.{}", asset.id),
            QualityCategory::Performance,
            status(properties_valid),
            true,
            true,
            Some(asset.id.clone()),
            Some(asset.source.reference.clone()),
            Some(asset.output.path.clone()),
            if properties_valid {
                "Declared UI movement uses only policy-approved cheap properties."
            } else {
                "Declared UI movement uses missing or disallowed animated properties."
            },
            "Prefer transform/opacity and avoid layout-property animation.",
        ),
        make_check(
            format!("motion.easing.{}", asset.id),
            QualityCategory::VisualIntegrity,
            status(easing_valid),
            true,
            true,
            Some(asset.id.clone()),
            Some(asset.source.reference.clone()),
            Some(asset.output.path.clone()),
            if easing_valid {
                "Motion easing is compatible with the meaning-first decelerating policy."
            } else {
                "Motion easing is outside the approved standard/ease-out family."
            },
            "Use a standard decelerating easing; bounce/elastic motion requires a versioned exception.",
        ),
        make_check(
            format!("motion.interaction.{}", asset.id),
            QualityCategory::Accessibility,
            status(!behavior.blocks_interaction),
            true,
            true,
            Some(asset.id.clone()),
            Some(asset.source.reference.clone()),
            Some(asset.output.path.clone()),
            if behavior.blocks_interaction {
                "Motion blocks the user's next interaction."
            } else {
                "Motion does not gate subsequent interaction."
            },
            "Make content interactive immediately; animation must never become a wait state.",
        ),
        make_check(
            format!("motion.autoplay.{}", asset.id),
            QualityCategory::Accessibility,
            status(autoplay_valid),
            true,
            true,
            Some(asset.id.clone()),
            Some(asset.source.reference.clone()),
            Some(asset.output.path.clone()),
            if autoplay_valid {
                "Autoplay behavior is absent or bounded to a muted non-looping landing sequence."
            } else {
                "Autoplay is not a muted non-looping landing sequence."
            },
            "Disable autoplay, or constrain it to a muted bounded landing sequence with a reduced-motion fallback.",
        ),
        make_check(
            format!("motion.loop.{}", asset.id),
            QualityCategory::Accessibility,
            status(loop_valid),
            true,
            true,
            Some(asset.id.clone()),
            Some(asset.source.reference.clone()),
            Some(asset.output.path.clone()),
            if loop_valid {
                "Looping is absent or limited to semantic continuous-status motion."
            } else {
                "Non-status motion is configured to loop indefinitely."
            },
            "Remove the loop or reclassify a genuine status indicator with a reduced-motion fallback.",
        ),
    ];

    if behavior.purpose != MotionPurpose::StaticImagery {
        checks.push(human_review_check(
            reviews,
            format!("motion.meaning.{}", asset.id),
            QualityCategory::VisualIntegrity,
            &asset.id,
            &asset.source.reference,
            &asset.output.path,
            "A human must confirm that the motion communicates a meaningful state or narrative change.",
            "Review the sequence in context and record the semantic-purpose decision.",
        ));
    }
    if matches!(
        behavior.purpose,
        MotionPurpose::Transition
            | MotionPurpose::LandingSequence
            | MotionPurpose::MicroInteraction
    ) {
        checks.push(human_review_check(
            reviews,
            format!("motion.direction.{}", asset.id),
            QualityCategory::VisualIntegrity,
            &asset.id,
            &asset.source.reference,
            &asset.output.path,
            "A human must confirm that movement direction/origin matches the interaction or narrative context.",
            "Review entrance/exit symmetry and trigger origin, then record the direction decision.",
        ));
    }
    checks
}

pub(super) fn requires_fallback(asset: &VisualMotionAsset) -> bool {
    if asset.behavior.purpose == MotionPurpose::StaticImagery {
        return false;
    }
    match asset.behavior.reduced_motion {
        ReducedMotionBehavior::Instant => matches!(
            asset.behavior.purpose,
            MotionPurpose::LandingSequence
                | MotionPurpose::ContinuousStatus
                | MotionPurpose::DemoCapture
        ),
        ReducedMotionBehavior::StaticFallback | ReducedMotionBehavior::PairedReducedCapture => true,
    }
}

pub(super) fn fallback_check(
    input: &QualityInput<'_>,
    asset: &VisualMotionAsset,
) -> CompilerResult<QualityCheck> {
    let Some(path) = asset.behavior.fallback_path.as_deref() else {
        return Ok(make_check(
            format!("motion.reduced-motion.{}", asset.id),
            QualityCategory::Accessibility,
            QualityStatus::Failed,
            true,
            true,
            Some(asset.id.clone()),
            Some(asset.source.reference.clone()),
            Some(asset.output.path.clone()),
            "Motion requires a reduced-motion fallback but no fallback path is declared.",
            "Provide a static or paired reduced-motion asset with an immutable digest.",
        ));
    };
    let Some(expected) = asset.behavior.fallback_sha256.as_deref() else {
        return Ok(make_check(
            format!("motion.reduced-motion.{}", asset.id),
            QualityCategory::Accessibility,
            QualityStatus::Failed,
            true,
            true,
            Some(asset.id.clone()),
            Some(asset.source.reference.clone()),
            Some(path.to_owned()),
            "Reduced-motion fallback has no SHA-256 digest.",
            "Record the exact fallback digest before release.",
        ));
    };
    let bytes = input.artifacts.read(path)?;
    let valid = bytes
        .as_ref()
        .is_some_and(|bytes| valid_sha256(expected) && sha256_hex(bytes) == expected);
    Ok(make_check(
        format!("motion.reduced-motion.{}", asset.id),
        QualityCategory::Accessibility,
        status(valid),
        true,
        true,
        Some(asset.id.clone()),
        Some(asset.source.reference.clone()),
        Some(path.to_owned()),
        if valid {
            "Reduced-motion fallback exists and matches its immutable digest."
        } else {
            "Reduced-motion fallback is missing or does not match its digest."
        },
        "Generate the declared static/paired reduced-motion projection and update provenance through human review.",
    ))
}
