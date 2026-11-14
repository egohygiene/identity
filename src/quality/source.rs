// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

//! Internal quality source responsibilities; public contracts remain in the parent.

use super::{
    BTreeSet, BrandKitSourceAsset, BrandKitSourceGovernance, QualityCategory, QualityCheck,
    QualityStatus, check, contains_external_svg_resource, sha256_hex, usvg,
};

pub(super) fn source_digest_check(role: &str, source: &BrandKitSourceAsset) -> QualityCheck {
    let actual = sha256_hex(source.text.as_bytes());
    check(
        format!("provenance.source-digest.{role}"),
        QualityCategory::Provenance,
        if actual == source.sha256 {
            QualityStatus::Passed
        } else {
            QualityStatus::Failed
        },
        true,
        true,
        Some(role.to_owned()),
        Some(format!("source role {role}")),
        None,
        if actual == source.sha256 {
            "Approved source bytes match their recorded SHA-256 digest.".to_owned()
        } else {
            "Approved source bytes differ from their recorded SHA-256 digest.".to_owned()
        },
        "Restore the approved source bytes or record a new human-reviewed provenance entry.",
    )
}

pub(super) fn alt_text_check(role: &str, source: &BrandKitSourceAsset) -> QualityCheck {
    let valid = !source.alt_text.trim().is_empty();
    check(
        format!("accessibility.alt-text.{role}"),
        QualityCategory::Accessibility,
        if valid {
            QualityStatus::Passed
        } else {
            QualityStatus::Failed
        },
        true,
        true,
        Some(role.to_owned()),
        Some(format!("source role {role}")),
        None,
        if valid {
            "Approved source has non-empty alternative text."
        } else {
            "Approved source has no alternative text."
        },
        "Add concise human-reviewed alternative text to the source provenance record.",
    )
}

pub(super) fn license_check(
    role: &str,
    governance: Option<&BrandKitSourceGovernance>,
) -> QualityCheck {
    let valid = governance.is_some_and(|governance| {
        !governance.license.spdx.trim().is_empty() && governance.license.status == "approved"
    });
    check(
        format!("licensing.approved.{role}"),
        QualityCategory::Licensing,
        if valid {
            QualityStatus::Passed
        } else {
            QualityStatus::Failed
        },
        true,
        true,
        Some(role.to_owned()),
        Some(format!("source role {role}")),
        None,
        if valid {
            "Source has an approved SPDX license record."
        } else {
            "Source is missing an approved SPDX license record."
        },
        "Record the asset license, approval status, and attribution before distribution.",
    )
}

pub(super) fn origin_check(
    role: &str,
    governance: Option<&BrandKitSourceGovernance>,
) -> QualityCheck {
    let valid = governance.is_some_and(|governance| {
        !governance.origin.creator.trim().is_empty()
            && !governance.origin.method.trim().is_empty()
            && !governance.origin.source.trim().is_empty()
            && !governance.origin.captured_at.trim().is_empty()
    });
    check(
        format!("provenance.origin.{role}"),
        QualityCategory::Provenance,
        if valid {
            QualityStatus::Passed
        } else {
            QualityStatus::Failed
        },
        true,
        true,
        Some(role.to_owned()),
        Some(format!("source role {role}")),
        None,
        if valid {
            "Source has creator, method, origin, and capture-time provenance."
        } else {
            "Source provenance is incomplete."
        },
        "Record creator, acquisition/generation method, source reference, and capture time.",
    )
}

pub(super) fn approval_check(
    role: &str,
    governance: Option<&BrandKitSourceGovernance>,
    approvals: &BTreeSet<String>,
) -> QualityCheck {
    let approved = governance.is_some_and(|governance| approvals.contains(&governance.approval));
    check(
        format!("provenance.approval.{role}"),
        QualityCategory::Provenance,
        if approved {
            QualityStatus::Passed
        } else {
            QualityStatus::Failed
        },
        true,
        true,
        Some(role.to_owned()),
        Some(format!("source role {role}")),
        None,
        if approved {
            "Source approval is present in the resolved human-decision set."
        } else {
            "Source does not resolve to an approved human decision."
        },
        "Record and resolve the exact approval identifier before generation or release.",
    )
}

pub(super) fn svg_source_checks(role: &str, source: &BrandKitSourceAsset) -> Vec<QualityCheck> {
    let mut checks = Vec::new();
    let external = contains_external_svg_resource(&source.text);
    checks.push(check(
        format!("visual.svg-external-resources.{role}"),
        QualityCategory::VisualIntegrity,
        if external {
            QualityStatus::Failed
        } else {
            QualityStatus::Passed
        },
        true,
        true,
        Some(role.to_owned()),
        Some(format!("source role {role}")),
        None,
        if external {
            "SVG contains an external network or file resource."
        } else {
            "SVG contains no external network or file resources."
        },
        "Inline or vendor every approved SVG dependency before deterministic generation.",
    ));

    let options = usvg::Options::default();
    match usvg::Tree::from_data(source.text.as_bytes(), &options) {
        Ok(tree) => {
            let has_view_box = source.text.contains("viewBox=") || source.text.contains("viewbox=");
            checks.push(check(
                format!("visual.svg-structure.{role}"),
                QualityCategory::VisualIntegrity,
                if has_view_box {
                    QualityStatus::Passed
                } else {
                    QualityStatus::Failed
                },
                true,
                true,
                Some(role.to_owned()),
                Some(format!("source role {role}")),
                None,
                if has_view_box {
                    "SVG parses successfully and declares a viewBox."
                } else {
                    "SVG parses but does not declare a viewBox."
                },
                "Add a finite viewBox so the mark scales predictably across target sizes.",
            ));
            let size = tree.size();
            let ratio = f64::from(size.width()) / f64::from(size.height());
            let extreme = !(0.125..=8.0).contains(&ratio);
            checks.push(check(
                format!("visual.svg-aspect-ratio.{role}"),
                QualityCategory::VisualIntegrity,
                if extreme {
                    QualityStatus::Warning
                } else {
                    QualityStatus::Passed
                },
                false,
                true,
                Some(role.to_owned()),
                Some(format!("source role {role}")),
                None,
                format!("SVG aspect ratio is {ratio:.2}:1."),
                "Confirm extreme aspect ratios are intentional and covered by a visual fixture.",
            ));
        }
        Err(error) => checks.push(check(
            format!("visual.svg-structure.{role}"),
            QualityCategory::VisualIntegrity,
            QualityStatus::Failed,
            true,
            true,
            Some(role.to_owned()),
            Some(format!("source role {role}")),
            None,
            format!("SVG cannot be parsed by the pinned renderer: {error}"),
            "Repair the SVG and regenerate from the approved source.",
        )),
    }
    checks
}
