// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

//! Internal quality tokens responsibilities; public contracts remain in the parent.

use super::{
    BrandKitModel, BrandKitToken, QualityCategory, QualityCheck, QualityStatus, Value, check,
};

pub(super) fn duration_check(
    model: &BrandKitModel,
    token_path: &str,
    check_id: &str,
    budget_ms: u64,
    expectation: DurationExpectation,
) -> QualityCheck {
    let Some(token) = model.tokens.get(token_path) else {
        return check(
            check_id,
            QualityCategory::Accessibility,
            QualityStatus::Skipped,
            false,
            true,
            Some(token_path.to_owned()),
            None,
            None,
            "Motion token is not declared in this Brand Kit scope.",
            "Declare the motion token when animated behavior is applicable.",
        );
    };
    let Some(milliseconds) = duration_ms(token) else {
        return check(
            check_id,
            QualityCategory::Accessibility,
            QualityStatus::Failed,
            true,
            true,
            Some(token_path.to_owned()),
            None,
            None,
            "Motion token is not a non-negative millisecond duration.",
            "Use a DTCG duration value with unit \"ms\" and a non-negative integer value.",
        );
    };
    let passes = match expectation {
        DurationExpectation::Maximum => milliseconds <= budget_ms,
        DurationExpectation::Exact => milliseconds == budget_ms,
    };
    let relation = match expectation {
        DurationExpectation::Maximum => format!("at or below {budget_ms} ms"),
        DurationExpectation::Exact => format!("exactly {budget_ms} ms"),
    };
    check(
        check_id,
        QualityCategory::Accessibility,
        if passes {
            QualityStatus::Passed
        } else {
            QualityStatus::Failed
        },
        true,
        true,
        Some(token_path.to_owned()),
        None,
        None,
        format!("Motion duration is {milliseconds} ms; required budget is {relation}."),
        "Adjust the semantic motion duration and regenerate affected projections.",
    )
}

pub(super) fn contrast_ratio(
    foreground: &BrandKitToken,
    background: &BrandKitToken,
) -> Result<f64, String> {
    let foreground = srgb_color(foreground)?;
    let background = srgb_color(background)?;
    let foreground_luminance = relative_luminance(foreground);
    let background_luminance = relative_luminance(background);
    let lighter = foreground_luminance.max(background_luminance);
    let darker = foreground_luminance.min(background_luminance);
    Ok((lighter + 0.05) / (darker + 0.05))
}

pub(super) fn srgb_color(token: &BrandKitToken) -> Result<[f64; 3], String> {
    if token.token_type != "color" {
        return Err("Declared contrast token is not a color token.".to_owned());
    }
    let value = token
        .value
        .as_object()
        .ok_or_else(|| "Color token value must be an object.".to_owned())?;
    if value.get("colorSpace").and_then(Value::as_str) != Some("srgb") {
        return Err("Declared contrast token must use the sRGB color space.".to_owned());
    }
    let alpha = value.get("alpha").and_then(Value::as_f64).unwrap_or(1.0);
    if (alpha - 1.0).abs() > f64::EPSILON {
        return Err("Declared contrast tokens must be opaque before WCAG evaluation.".to_owned());
    }
    let components = value
        .get("components")
        .and_then(Value::as_array)
        .filter(|components| components.len() == 3)
        .ok_or_else(|| "sRGB color token must contain exactly three components.".to_owned())?;
    let mut color = [0.0; 3];
    for (index, component) in components.iter().enumerate() {
        let value = component
            .as_f64()
            .filter(|value| (0.0..=1.0).contains(value))
            .ok_or_else(|| "sRGB components must be numeric values in [0, 1].".to_owned())?;
        color[index] = value;
    }
    Ok(color)
}

pub(super) fn relative_luminance(color: [f64; 3]) -> f64 {
    let red = linear_channel(color[0]);
    let green = linear_channel(color[1]);
    let blue = linear_channel(color[2]);
    0.2126 * red + 0.7152 * green + 0.0722 * blue
}

pub(super) fn linear_channel(value: f64) -> f64 {
    if value <= 0.04045 {
        value / 12.92
    } else {
        ((value + 0.055) / 1.055).powf(2.4)
    }
}

pub(super) fn duration_ms(token: &BrandKitToken) -> Option<u64> {
    if token.token_type != "duration" {
        return None;
    }
    let value = token.value.as_object()?;
    if value.get("unit").and_then(Value::as_str)? != "ms" {
        return None;
    }
    value.get("value").and_then(Value::as_u64)
}

#[derive(Clone, Copy)]
pub(super) enum DurationExpectation {
    Maximum,
    Exact,
}
