// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

//! Release-oriented accessibility, provenance, and visual-quality evidence.
//!
//! The quality harness consumes the resolved Brand Kit model plus compiler
//! outputs. It never mutates canonical source or generated artifacts. Automated
//! checks, skipped coverage, and human-review requirements remain distinct so a
//! partial report cannot be mistaken for verified success.

mod source;
use source::{
    alt_text_check, approval_check, license_check, origin_check, source_digest_check,
    svg_source_checks,
};
mod artifacts;
use artifacts::{
    artifact_budget_check, artifact_digest_check, generated_svg_check, maskable_evidence_check,
    png_dimensions_check, visual_baseline_check,
};
mod tokens;
use tokens::{DurationExpectation, contrast_ratio, duration_check};

#[cfg(test)]
mod tests;

use std::collections::{BTreeMap, BTreeSet};
use std::fmt::Write as _;
use std::fs;
use std::path::PathBuf;

use resvg::{tiny_skia, usvg};
use serde::{Deserialize, Serialize};
use serde_json::Value;

use crate::brandkit::{
    BrandKitModel, BrandKitSourceAsset, BrandKitSourceGovernance, BrandKitToken,
};
use crate::compiler::{
    CompilerError, CompilerManifest, CompilerResult, Diagnostic, EvidenceStatus, FailureKind,
    ProjectionTarget, sha256_hex,
};

pub const QUALITY_REPORT_SCHEMA: &str = "identity.quality-report/v1";
pub const VISUAL_BASELINES_SCHEMA: &str = "identity.visual-baselines/v1";

#[derive(Clone, Copy, Debug, Deserialize, Eq, Ord, PartialEq, PartialOrd, Serialize)]
#[serde(rename_all = "kebab-case")]
pub enum QualityScope {
    Package,
    Publication,
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, Ord, PartialEq, PartialOrd, Serialize)]
#[serde(rename_all = "kebab-case")]
pub enum QualityCategory {
    Accessibility,
    VisualIntegrity,
    Provenance,
    Licensing,
    Performance,
    Reproducibility,
    Renderer,
}

#[derive(Clone, Copy, Debug, Deserialize, Eq, Ord, PartialEq, PartialOrd, Serialize)]
#[serde(rename_all = "kebab-case")]
pub enum QualityStatus {
    Passed,
    Warning,
    Failed,
    Skipped,
    ReviewRequired,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct QualityCheck {
    pub id: String,
    pub category: QualityCategory,
    pub status: QualityStatus,
    pub blocking: bool,
    pub automated: bool,
    #[serde(default)]
    pub subject: Option<String>,
    #[serde(default)]
    pub source_context: Option<String>,
    #[serde(default)]
    pub generated_context: Option<String>,
    pub message: String,
    pub recovery: String,
}

#[derive(Clone, Debug, Default, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct QualityCoverage {
    pub total: usize,
    pub automated: usize,
    pub passed: usize,
    pub warnings: usize,
    pub failed: usize,
    pub skipped: usize,
    pub review_required: usize,
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct QualityReport {
    pub schema: String,
    pub project_id: String,
    pub source_digest: String,
    pub scope: QualityScope,
    pub release_allowed: bool,
    pub coverage: QualityCoverage,
    pub checks: Vec<QualityCheck>,
}

impl QualityReport {
    #[must_use]
    pub fn human_summary(&self) -> String {
        let mut output = String::new();
        writeln!(
            output,
            "Brand Kit quality: {} ({:?} scope)",
            if self.release_allowed {
                "PASS"
            } else {
                "BLOCKED"
            },
            self.scope
        )
        .expect("writing to String cannot fail");
        writeln!(
            output,
            "{} checks: {} passed, {} warnings, {} failed, {} review-required, {} skipped",
            self.coverage.total,
            self.coverage.passed,
            self.coverage.warnings,
            self.coverage.failed,
            self.coverage.review_required,
            self.coverage.skipped
        )
        .expect("writing to String cannot fail");

        for check in self.checks.iter().filter(|check| {
            check.blocking
                && matches!(
                    check.status,
                    QualityStatus::Failed | QualityStatus::ReviewRequired
                )
        }) {
            writeln!(
                output,
                "- {}: {} Recovery: {}",
                check.id, check.message, check.recovery
            )
            .expect("writing to String cannot fail");
        }
        output
    }
}

#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct ContrastPair {
    pub foreground: String,
    pub background: String,
    pub minimum_ratio: f64,
}

#[derive(Clone, Debug, Deserialize, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct QualityPolicy {
    pub contrast_pairs: Vec<ContrastPair>,
    pub maximum_standard_motion_ms: u64,
    pub required_reduced_motion_ms: u64,
    pub maximum_motion_asset_bytes: u64,
    pub renderer_boot_budget_ms: u64,
    pub minimum_target_css_px: u32,
}

impl Default for QualityPolicy {
    fn default() -> Self {
        Self {
            contrast_pairs: vec![ContrastPair {
                foreground: "color.text".to_owned(),
                background: "color.canvas".to_owned(),
                minimum_ratio: 4.5,
            }],
            maximum_standard_motion_ms: 300,
            required_reduced_motion_ms: 0,
            maximum_motion_asset_bytes: 1_000_000,
            renderer_boot_budget_ms: 2_500,
            minimum_target_css_px: 24,
        }
    }
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct VisualBaseline {
    pub target_id: String,
    pub sha256: String,
    pub source_context: String,
    pub generated_context: String,
}

#[derive(Clone, Debug, Default, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct VisualBaselineSet {
    pub schema: String,
    #[serde(default)]
    pub baselines: Vec<VisualBaseline>,
}

impl VisualBaselineSet {
    pub fn by_target(&self) -> CompilerResult<BTreeMap<&str, &VisualBaseline>> {
        if self.schema != VISUAL_BASELINES_SCHEMA {
            return Err(quality_error(
                "visual-baselines",
                format!("unsupported visual baseline schema {:?}", self.schema),
                "Use identity.visual-baselines/v1 before running visual regression checks.",
            ));
        }
        let mut result = BTreeMap::new();
        for baseline in &self.baselines {
            if !valid_sha256(&baseline.sha256) {
                return Err(quality_error(
                    &baseline.target_id,
                    "visual baseline contains an invalid SHA-256 digest".to_owned(),
                    "Record a 64-character lowercase SHA-256 digest for the approved baseline.",
                ));
            }
            if result
                .insert(baseline.target_id.as_str(), baseline)
                .is_some()
            {
                return Err(quality_error(
                    &baseline.target_id,
                    "visual baseline target is declared more than once".to_owned(),
                    "Keep exactly one approved baseline per target id.",
                ));
            }
        }
        Ok(result)
    }
}

#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct HumanReviewEvidence {
    pub check_id: String,
    pub approved: bool,
    pub reviewer: String,
    pub reviewed_at: String,
    pub evidence: String,
}

pub trait QualityArtifactReader: Send + Sync {
    fn read(&self, relative_path: &str) -> CompilerResult<Option<Vec<u8>>>;
}

#[derive(Clone, Debug)]
pub struct FileSystemArtifactReader {
    root: PathBuf,
}

impl FileSystemArtifactReader {
    pub fn new(root: impl Into<PathBuf>) -> CompilerResult<Self> {
        let root = root.into();
        let canonical = root.canonicalize().map_err(|error| {
            quality_error(
                "artifact-root",
                format!("cannot resolve quality artifact root: {error}"),
                "Create the generated artifact root before quality validation.",
            )
        })?;
        Ok(Self { root: canonical })
    }
}

impl QualityArtifactReader for FileSystemArtifactReader {
    fn read(&self, relative_path: &str) -> CompilerResult<Option<Vec<u8>>> {
        validate_portable_path(relative_path)?;
        let path = self.root.join(relative_path);
        if !path.exists() {
            return Ok(None);
        }
        if path.is_symlink() || !path.is_file() {
            return Err(quality_error(
                relative_path,
                "generated artifact must be a regular non-symlink file".to_owned(),
                "Regenerate the artifact inside the isolated generated-output root.",
            ));
        }
        fs::read(path).map(Some).map_err(|error| {
            quality_error(
                relative_path,
                format!("cannot read generated artifact: {error}"),
                "Restore readable generated output and rerun the quality gate.",
            )
        })
    }
}

pub struct QualityInput<'a> {
    pub model: &'a BrandKitModel,
    pub manifest: &'a CompilerManifest,
    pub targets: &'a [ProjectionTarget],
    pub artifacts: &'a dyn QualityArtifactReader,
    pub baselines: &'a VisualBaselineSet,
    pub human_reviews: &'a [HumanReviewEvidence],
    pub scope: QualityScope,
}

#[derive(Clone, Debug, Default)]
pub struct QualityHarness {
    policy: QualityPolicy,
}

impl QualityHarness {
    #[must_use]
    pub fn new(policy: QualityPolicy) -> Self {
        Self { policy }
    }

    pub fn evaluate(&self, input: &QualityInput<'_>) -> CompilerResult<QualityReport> {
        validate_input(input)?;
        let baseline_by_target = input.baselines.by_target()?;
        let review_by_check = review_index(input.human_reviews)?;
        let target_by_id = input
            .targets
            .iter()
            .map(|target| (target.id.as_str(), target))
            .collect::<BTreeMap<_, _>>();
        let mut checks = Vec::new();

        self.check_contrast(input.model, &mut checks);
        self.check_motion(input.model, &mut checks);
        Self::check_sources(input.model, &review_by_check, &mut checks);
        Self::check_generated_artifacts(
            input,
            &target_by_id,
            &baseline_by_target,
            &review_by_check,
            &mut checks,
        )?;
        self.check_renderer_scope(input, &review_by_check, &mut checks);

        checks.sort_by(|left, right| {
            left.category
                .cmp(&right.category)
                .then_with(|| left.id.cmp(&right.id))
                .then_with(|| left.subject.cmp(&right.subject))
        });
        let coverage = coverage(&checks);
        let release_allowed = checks.iter().all(|check| {
            !check.blocking
                || !matches!(
                    check.status,
                    QualityStatus::Failed | QualityStatus::ReviewRequired
                )
        });

        Ok(QualityReport {
            schema: QUALITY_REPORT_SCHEMA.to_owned(),
            project_id: input.model.project_id.clone(),
            source_digest: input.model.source_digest.clone(),
            scope: input.scope,
            release_allowed,
            coverage,
            checks,
        })
    }

    fn check_contrast(&self, model: &BrandKitModel, checks: &mut Vec<QualityCheck>) {
        for pair in &self.policy.contrast_pairs {
            let id = format!(
                "accessibility.contrast.{}-on-{}",
                normalized_id(&pair.foreground),
                normalized_id(&pair.background)
            );
            let foreground = model.tokens.get(&pair.foreground);
            let background = model.tokens.get(&pair.background);
            let Some((foreground, background)) = foreground.zip(background) else {
                checks.push(check(
                    id,
                    QualityCategory::Accessibility,
                    QualityStatus::Skipped,
                    false,
                    true,
                    Some(format!("{} / {}", pair.foreground, pair.background)),
                    None,
                    None,
                    "Declared contrast pair is not present in this Brand Kit scope.",
                    "Add both semantic color tokens when the pairing is applicable.",
                ));
                continue;
            };
            match contrast_ratio(foreground, background) {
                Ok(ratio) if ratio >= pair.minimum_ratio => checks.push(check(
                    id,
                    QualityCategory::Accessibility,
                    QualityStatus::Passed,
                    true,
                    true,
                    Some(format!("{} / {}", pair.foreground, pair.background)),
                    None,
                    None,
                    format!(
                        "WCAG contrast ratio is {ratio:.2}:1, meeting the {:.2}:1 budget.",
                        pair.minimum_ratio
                    ),
                    "No recovery required.",
                )),
                Ok(ratio) => checks.push(check(
                    id,
                    QualityCategory::Accessibility,
                    QualityStatus::Failed,
                    true,
                    true,
                    Some(format!("{} / {}", pair.foreground, pair.background)),
                    None,
                    None,
                    format!(
                        "WCAG contrast ratio is {ratio:.2}:1, below the {:.2}:1 budget.",
                        pair.minimum_ratio
                    ),
                    "Adjust the semantic foreground/background colors and regenerate all projections.",
                )),
                Err(message) => checks.push(check(
                    id,
                    QualityCategory::Accessibility,
                    QualityStatus::Failed,
                    true,
                    true,
                    Some(format!("{} / {}", pair.foreground, pair.background)),
                    None,
                    None,
                    message,
                    "Use opaque sRGB color tokens with three numeric components for declared contrast pairs.",
                )),
            }
        }
    }

    fn check_motion(&self, model: &BrandKitModel, checks: &mut Vec<QualityCheck>) {
        checks.push(duration_check(
            model,
            "motion.duration.standard",
            "accessibility.motion-standard-budget",
            self.policy.maximum_standard_motion_ms,
            DurationExpectation::Maximum,
        ));
        checks.push(duration_check(
            model,
            "motion.duration.reduced",
            "accessibility.reduced-motion-budget",
            self.policy.required_reduced_motion_ms,
            DurationExpectation::Exact,
        ));
        checks.push(check(
            "performance.motion-asset-budget",
            QualityCategory::Performance,
            QualityStatus::Skipped,
            false,
            true,
            None,
            None,
            None,
            format!(
                "No motion asset profile is active; the reserved per-asset budget is {} bytes.",
                self.policy.maximum_motion_asset_bytes
            ),
            "Issue #3 will apply this budget when motion assets are introduced.",
        ));
    }

    fn check_sources(
        model: &BrandKitModel,
        reviews: &BTreeMap<&str, &HumanReviewEvidence>,
        checks: &mut Vec<QualityCheck>,
    ) {
        for (role, source) in &model.sources {
            checks.push(source_digest_check(role, source));
            checks.push(alt_text_check(role, source));
            let governance = model.source_governance.get(role);
            checks.push(license_check(role, governance));
            checks.push(origin_check(role, governance));
            checks.push(approval_check(role, governance, &model.approvals));
            if source.media_type == "image/svg+xml" {
                checks.extend(svg_source_checks(role, source));
                checks.push(review_check(
                    &format!("visual.small-size-legibility.{role}"),
                    QualityCategory::VisualIntegrity,
                    true,
                    reviews,
                    Some(role.clone()),
                    Some(format!("approved source role {role}")),
                    None,
                    "Small-size legibility at the documented minimum size requires human visual review.",
                    "Review the mark at 16 CSS pixels and record approval evidence before release.",
                ));
            }
        }
    }

    fn check_generated_artifacts(
        input: &QualityInput<'_>,
        targets: &BTreeMap<&str, &ProjectionTarget>,
        baselines: &BTreeMap<&str, &VisualBaseline>,
        reviews: &BTreeMap<&str, &HumanReviewEvidence>,
        checks: &mut Vec<QualityCheck>,
    ) -> CompilerResult<()> {
        for output in &input.manifest.outputs {
            let target = targets.get(output.target_id.as_str()).ok_or_else(|| {
                quality_error(
                    &output.target_id,
                    "compiler manifest references a target outside the quality request".to_owned(),
                    "Run quality validation against the exact profile request used for generation.",
                )
            })?;
            let Some(bytes) = input.artifacts.read(&output.path)? else {
                checks.push(check(
                    format!("reproducibility.artifact-present.{}", output.target_id),
                    QualityCategory::Reproducibility,
                    QualityStatus::Failed,
                    true,
                    true,
                    Some(output.target_id.clone()),
                    None,
                    Some(output.path.clone()),
                    "Generated artifact recorded in the manifest is missing.",
                    "Regenerate from the same canonical source and rerun quality validation.",
                ));
                continue;
            };

            checks.push(artifact_digest_check(output, &bytes));
            checks.push(artifact_budget_check(target, &bytes));
            if output.media_type == "image/png" {
                checks.push(png_dimensions_check(target, &bytes));
            }
            if output.media_type == "image/svg+xml" {
                checks.push(generated_svg_check(target, &bytes));
            }
            if target
                .parameters
                .get("maskable")
                .and_then(Value::as_bool)
                .unwrap_or(false)
            {
                checks.push(maskable_evidence_check(input.manifest, target));
            }
            if is_visual_regression_target(target) {
                checks.push(visual_baseline_check(
                    target,
                    &bytes,
                    baselines.get(target.id.as_str()).copied(),
                    reviews,
                ));
            }
        }
        Ok(())
    }

    fn check_renderer_scope(
        &self,
        input: &QualityInput<'_>,
        reviews: &BTreeMap<&str, &HumanReviewEvidence>,
        checks: &mut Vec<QualityCheck>,
    ) {
        let publication = input.scope == QualityScope::Publication;
        let status = if publication {
            QualityStatus::ReviewRequired
        } else {
            QualityStatus::Skipped
        };
        let blocking = publication;
        for (id, message, recovery) in [
            (
                "renderer.keyboard-operation",
                "Keyboard operation for the reference renderer is not automated by the package harness.",
                "Run the #14 renderer accessibility suite and attach keyboard evidence before publication.",
            ),
            (
                "renderer.focus-states",
                "Visible focus-state coverage belongs to the reference renderer surface.",
                "Validate focus visibility in the #14 renderer and record evidence before publication.",
            ),
            (
                "renderer.copy-download-controls",
                "Copy and download controls require rendered interaction evidence.",
                "Exercise every copy/download control with keyboard and pointer input before publication.",
            ),
            (
                "renderer.no-color-high-contrast",
                "No-color and high-contrast behavior requires a rendered surface.",
                "Validate forced-colors/high-contrast rendering in the #14 browser matrix before publication.",
            ),
            (
                "renderer.target-size",
                "Interactive target-size validation requires rendered layout geometry.",
                "Verify interactive targets are at least the configured CSS-pixel minimum before publication.",
            ),
            (
                "renderer.performance-budget",
                "Renderer performance requires browser timing evidence.",
                "Measure the reference renderer against the configured boot budget before publication.",
            ),
        ] {
            if publication {
                checks.push(review_check(
                    id,
                    QualityCategory::Renderer,
                    blocking,
                    reviews,
                    None,
                    None,
                    None,
                    format!(
                        "{message} Target-size budget: {} CSS px; renderer boot budget: {} ms.",
                        self.policy.minimum_target_css_px, self.policy.renderer_boot_budget_ms
                    ),
                    recovery,
                ));
            } else {
                checks.push(check(
                    id,
                    QualityCategory::Renderer,
                    status,
                    blocking,
                    false,
                    None,
                    None,
                    None,
                    format!(
                        "{message} Package scope records this as explicitly skipped rather than verified."
                    ),
                    recovery,
                ));
            }
        }
    }
}

#[allow(clippy::too_many_arguments)]
fn review_check(
    id: &str,
    category: QualityCategory,
    blocking: bool,
    reviews: &BTreeMap<&str, &HumanReviewEvidence>,
    subject: Option<String>,
    source_context: Option<String>,
    generated_context: Option<String>,
    message: impl Into<String>,
    recovery: impl Into<String>,
) -> QualityCheck {
    let message = message.into();
    let recovery = recovery.into();
    match reviews.get(id) {
        Some(review) if review.approved => check(
            id,
            category,
            QualityStatus::Passed,
            blocking,
            false,
            subject,
            source_context,
            generated_context,
            format!(
                "{message} Approved by {} at {}: {}",
                review.reviewer, review.reviewed_at, review.evidence
            ),
            "No recovery required.",
        ),
        Some(review) => check(
            id,
            category,
            QualityStatus::Failed,
            blocking,
            false,
            subject,
            source_context,
            generated_context,
            format!(
                "{message} Review by {} at {} rejected the evidence: {}",
                review.reviewer, review.reviewed_at, review.evidence
            ),
            recovery,
        ),
        None => check(
            id,
            category,
            QualityStatus::ReviewRequired,
            blocking,
            false,
            subject,
            source_context,
            generated_context,
            message,
            recovery,
        ),
    }
}

#[allow(clippy::too_many_arguments)]
fn check(
    id: impl Into<String>,
    category: QualityCategory,
    status: QualityStatus,
    blocking: bool,
    automated: bool,
    subject: Option<String>,
    source_context: Option<String>,
    generated_context: Option<String>,
    message: impl Into<String>,
    recovery: impl Into<String>,
) -> QualityCheck {
    QualityCheck {
        id: id.into(),
        category,
        status,
        blocking,
        automated,
        subject,
        source_context,
        generated_context,
        message: message.into(),
        recovery: recovery.into(),
    }
}

fn validate_input(input: &QualityInput<'_>) -> CompilerResult<()> {
    if input.model.project_id != input.manifest.project_id
        || input.model.source_digest != input.manifest.source_digest
    {
        return Err(quality_error(
            "quality-input",
            "Brand Kit model and compiler manifest do not describe the same canonical source"
                .to_owned(),
            "Validate the manifest produced from this exact resolved Brand Kit model.",
        ));
    }
    let target_ids = input
        .targets
        .iter()
        .map(|target| target.id.as_str())
        .collect::<BTreeSet<_>>();
    if target_ids.len() != input.targets.len() {
        return Err(quality_error(
            "quality-input",
            "quality target request contains duplicate target identifiers".to_owned(),
            "Use the exact deterministic compiler request without duplicate targets.",
        ));
    }
    Ok(())
}

fn review_index(
    reviews: &[HumanReviewEvidence],
) -> CompilerResult<BTreeMap<&str, &HumanReviewEvidence>> {
    let mut result = BTreeMap::new();
    for review in reviews {
        if review.check_id.trim().is_empty()
            || review.reviewer.trim().is_empty()
            || review.reviewed_at.trim().is_empty()
            || review.evidence.trim().is_empty()
        {
            return Err(quality_error(
                "human-review",
                "human review evidence requires check id, reviewer, time, and evidence".to_owned(),
                "Record complete review evidence before rerunning the quality gate.",
            ));
        }
        if result.insert(review.check_id.as_str(), review).is_some() {
            return Err(quality_error(
                &review.check_id,
                "human review evidence is declared more than once for one check".to_owned(),
                "Keep one current review decision per stable quality-check id.",
            ));
        }
    }
    Ok(result)
}

fn coverage(checks: &[QualityCheck]) -> QualityCoverage {
    let mut result = QualityCoverage {
        total: checks.len(),
        ..QualityCoverage::default()
    };
    for check in checks {
        if check.automated {
            result.automated += 1;
        }
        match check.status {
            QualityStatus::Passed => result.passed += 1,
            QualityStatus::Warning => result.warnings += 1,
            QualityStatus::Failed => result.failed += 1,
            QualityStatus::Skipped => result.skipped += 1,
            QualityStatus::ReviewRequired => result.review_required += 1,
        }
    }
    result
}

fn expected_dimensions(target: &ProjectionTarget) -> Option<(u32, u32)> {
    let width = target
        .parameters
        .get("width")
        .and_then(Value::as_u64)
        .and_then(|value| u32::try_from(value).ok())?;
    let height = target
        .parameters
        .get("height")
        .and_then(Value::as_u64)
        .and_then(|value| u32::try_from(value).ok())?;
    Some((width, height))
}

fn is_visual_regression_target(target: &ProjectionTarget) -> bool {
    target.media_type.starts_with("image/") || target.id == "metadata-open-graph"
}

fn contains_external_svg_resource(text: &str) -> bool {
    let lowercase = text.to_ascii_lowercase();
    lowercase.contains("href=\"http://")
        || lowercase.contains("href=\"https://")
        || lowercase.contains("href=\"file://")
        || lowercase.contains("xlink:href=\"http://")
        || lowercase.contains("xlink:href=\"https://")
        || lowercase.contains("xlink:href=\"file://")
}

fn normalized_id(value: &str) -> String {
    value
        .chars()
        .map(|character| {
            if character.is_ascii_alphanumeric() {
                character.to_ascii_lowercase()
            } else {
                '-'
            }
        })
        .collect()
}

fn validate_portable_path(path: &str) -> CompilerResult<()> {
    if path.is_empty()
        || path.starts_with('/')
        || path.ends_with('/')
        || path.contains('\\')
        || path
            .split('/')
            .any(|segment| segment.is_empty() || matches!(segment, "." | ".."))
    {
        return Err(quality_error(
            path,
            "quality artifact path must be a normalized repository-relative path".to_owned(),
            "Use forward-slash-separated path segments without absolute, dot, parent, or empty components.",
        ));
    }
    Ok(())
}

fn valid_sha256(value: &str) -> bool {
    value.len() == 64
        && value
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
}

fn quality_error(path: &str, message: String, recovery: &str) -> CompilerError {
    CompilerError::new(
        FailureKind::Invalid,
        Diagnostic::error(
            "IDN4001",
            FailureKind::Invalid,
            Some(path.to_owned()),
            message,
            recovery,
        ),
    )
}
