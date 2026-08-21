// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::path::{Component, Path, PathBuf};

use anyhow::{Context, Result, bail};
use serde::{Deserialize, Serialize};

pub const PROJECT_SCHEMA: &str = "identity.project/v0";
pub const PROFILE_SCHEMA: &str = "identity.profile/v0";

#[derive(Clone, Debug, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct ProjectSpec {
    pub schema: String,
    pub project: ProjectMetadata,
    pub paths: ProjectPaths,
    pub profiles: ProfileSelection,
    pub sources: SourceSelection,
    #[serde(default)]
    pub context: ContextSelection,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct ProjectMetadata {
    pub id: String,
    pub display_name: String,
    pub repository: String,
    pub tagline: String,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct ProjectPaths {
    pub output_root: PathBuf,
    pub source_root: PathBuf,
    pub brief: PathBuf,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct ProfileSelection {
    pub enabled: Vec<String>,
    #[serde(default)]
    pub inapplicable: Vec<String>,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct SourceSelection {
    pub approval: String,
    pub required: Vec<SourceRequirement>,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct SourceRequirement {
    pub role: String,
    pub path: PathBuf,
    pub format: String,
    pub description: String,
}

#[derive(Clone, Debug, Default, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct ContextSelection {
    #[serde(default)]
    pub files: Vec<PathBuf>,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct Profile {
    pub schema: String,
    pub id: String,
    pub version: String,
    pub verified_at: String,
    #[serde(default)]
    pub references: Vec<String>,
    pub targets: Vec<Target>,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct Target {
    pub id: String,
    pub path: PathBuf,
    pub format: String,
    pub source_role: String,
    pub description: String,
    #[serde(default)]
    pub width: Option<u32>,
    #[serde(default)]
    pub height: Option<u32>,
    #[serde(default)]
    pub purpose: Option<String>,
    #[serde(default)]
    pub maximum_bytes: Option<u64>,
    #[serde(default = "default_required")]
    pub required: bool,
}

const fn default_required() -> bool {
    true
}

#[derive(Clone, Debug, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct ResolvedPlan {
    pub schema: &'static str,
    pub project_id: String,
    pub display_name: String,
    pub output_root: PathBuf,
    pub profiles: Vec<ResolvedProfile>,
    pub targets: Vec<ResolvedTarget>,
}

#[derive(Clone, Debug, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct ResolvedProfile {
    pub id: String,
    pub version: String,
    pub verified_at: String,
    pub references: Vec<String>,
}

#[derive(Clone, Debug, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct ResolvedTarget {
    pub profile: String,
    pub id: String,
    pub path: PathBuf,
    pub format: String,
    pub source_role: String,
    pub description: String,
    pub dimensions: Option<String>,
    pub purpose: Option<String>,
    pub maximum_bytes: Option<u64>,
    pub required: bool,
}

#[derive(Debug)]
pub struct ValidatedProject {
    pub repository_root: PathBuf,
    pub spec_path: PathBuf,
    pub spec: ProjectSpec,
    pub profiles: Vec<Profile>,
}

pub fn validate_repository(repository_root: &Path) -> Result<ValidatedProject> {
    let repository_root = repository_root.canonicalize().with_context(|| {
        format!(
            "repository root does not exist: {}",
            repository_root.display()
        )
    })?;
    let spec_path = repository_root.join(".identity/identity.toml");
    let contents = fs::read_to_string(&spec_path)
        .with_context(|| format!("cannot read project specification: {}", spec_path.display()))?;
    let spec: ProjectSpec = toml::from_str(&contents)
        .with_context(|| format!("invalid TOML in {}", spec_path.display()))?;

    let mut errors = Vec::new();
    validate_project_contract(&repository_root, &spec, &mut errors);
    validate_profile_selection(&spec, &mut errors);
    let source_roles = validate_source_selection(&spec, &mut errors);
    let profiles = load_selected_profiles(&spec, &mut errors);
    validate_loaded_profiles(&profiles, &source_roles, &mut errors);

    if !errors.is_empty() {
        bail!(
            "identity specification failed validation:\n- {}",
            errors.join("\n- ")
        );
    }

    Ok(ValidatedProject {
        repository_root,
        spec_path,
        spec,
        profiles,
    })
}

fn validate_project_contract(repository_root: &Path, spec: &ProjectSpec, errors: &mut Vec<String>) {
    if spec.schema != PROJECT_SCHEMA {
        errors.push(format!(
            "schema must be {PROJECT_SCHEMA:?}, found {:?}",
            spec.schema
        ));
    }
    if !valid_identifier(&spec.project.id) {
        errors.push("project.id must use lowercase letters, digits, and hyphens".to_owned());
    }
    if spec.project.display_name.trim().is_empty() {
        errors.push("project.display_name must not be empty".to_owned());
    }
    if spec.project.tagline.trim().is_empty() {
        errors.push("project.tagline must not be empty".to_owned());
    }
    if spec.sources.approval != "human" {
        errors.push("sources.approval must be \"human\" in the v0 contract".to_owned());
    }

    let paths = [
        ("paths.output_root", &spec.paths.output_root),
        ("paths.source_root", &spec.paths.source_root),
        ("paths.brief", &spec.paths.brief),
    ];
    for (label, path) in paths {
        if let Err(error) = validate_relative_path(path, label) {
            errors.push(error.to_string());
        }
    }
    for path in &spec.context.files {
        if let Err(error) = validate_relative_path(path, "context.files entry") {
            errors.push(error.to_string());
        } else if let Err(error) =
            validate_existing_path(repository_root, path, true, "context file")
        {
            errors.push(error.to_string());
        }
    }

    if let Err(error) = validate_existing_path(repository_root, &spec.paths.brief, true, "brief") {
        errors.push(error.to_string());
    }
    if let Err(error) = validate_existing_path(
        repository_root,
        &spec.paths.source_root,
        false,
        "source root",
    ) {
        errors.push(error.to_string());
    }

    let context_paths: BTreeSet<&PathBuf> = spec.context.files.iter().collect();
    if context_paths.len() != spec.context.files.len() {
        errors.push("context.files contains duplicate paths".to_owned());
    }
}

fn validate_profile_selection(spec: &ProjectSpec, errors: &mut Vec<String>) {
    let mut profile_ids = BTreeSet::new();
    if spec.profiles.enabled.is_empty() {
        errors.push("profiles.enabled must select at least one profile".to_owned());
    }
    for profile_id in &spec.profiles.enabled {
        if !valid_identifier(profile_id) {
            errors.push(format!("invalid enabled profile id: {profile_id:?}"));
        }
        if !profile_ids.insert(profile_id.as_str()) {
            errors.push(format!("duplicate enabled profile: {profile_id:?}"));
        }
    }
    let mut inapplicable_ids = BTreeSet::new();
    for profile_id in &spec.profiles.inapplicable {
        if !valid_identifier(profile_id) {
            errors.push(format!("invalid inapplicable profile id: {profile_id:?}"));
        }
        if !inapplicable_ids.insert(profile_id.as_str()) {
            errors.push(format!("duplicate inapplicable profile: {profile_id:?}"));
        }
        if profile_ids.contains(profile_id.as_str()) {
            errors.push(format!(
                "profile cannot be enabled and inapplicable: {profile_id:?}"
            ));
        }
    }
}

fn validate_source_selection<'a>(
    spec: &'a ProjectSpec,
    errors: &mut Vec<String>,
) -> BTreeSet<&'a str> {
    let source_roles: BTreeSet<&str> = spec
        .sources
        .required
        .iter()
        .map(|source| source.role.as_str())
        .collect();
    if source_roles.len() != spec.sources.required.len() {
        errors.push("sources.required contains duplicate roles".to_owned());
    }
    if spec.sources.required.is_empty() {
        errors.push("sources.required must declare at least one canonical source".to_owned());
    }
    for source in &spec.sources.required {
        if !valid_identifier(&source.role) {
            errors.push(format!("invalid source role: {:?}", source.role));
        }
        if let Err(error) = validate_relative_path(&source.path, "source path") {
            errors.push(error.to_string());
        }
        if source.format.trim().is_empty() || source.description.trim().is_empty() {
            errors.push(format!(
                "source role {:?} must declare format and description",
                source.role
            ));
        }
    }
    source_roles
}

fn load_selected_profiles(spec: &ProjectSpec, errors: &mut Vec<String>) -> Vec<Profile> {
    let mut profiles = Vec::new();
    for profile_id in &spec.profiles.enabled {
        match load_profile(profile_id) {
            Ok(profile) => profiles.push(profile),
            Err(error) => errors.push(format!("profile {profile_id:?}: {error:#}")),
        }
    }
    profiles
}

fn validate_loaded_profiles(
    profiles: &[Profile],
    source_roles: &BTreeSet<&str>,
    errors: &mut Vec<String>,
) {
    let mut target_ids = BTreeSet::new();
    let mut target_paths = BTreeMap::<PathBuf, String>::new();
    for profile in profiles {
        if profile.schema != PROFILE_SCHEMA {
            errors.push(format!(
                "profile {:?} schema must be {PROFILE_SCHEMA:?}",
                profile.id
            ));
        }
        if profile.id.trim().is_empty() || profile.version.trim().is_empty() {
            errors.push(format!("profile {:?} has incomplete identity", profile.id));
        }
        if !valid_semantic_version(&profile.version) {
            errors.push(format!(
                "profile {:?} version must use MAJOR.MINOR.PATCH",
                profile.id
            ));
        }
        if profile.verified_at.trim().is_empty() {
            errors.push(format!("profile {:?} has no verified_at date", profile.id));
        }
        if profile.targets.is_empty() {
            errors.push(format!("profile {:?} has no targets", profile.id));
        }
        for target in &profile.targets {
            let composite_id = format!("{}:{}", profile.id, target.id);
            if !valid_identifier(&target.id) {
                errors.push(format!("invalid target id: {composite_id:?}"));
            }
            if !target_ids.insert(composite_id.clone()) {
                errors.push(format!("duplicate target id: {composite_id}"));
            }
            if let Err(error) = validate_relative_path(&target.path, "target path") {
                errors.push(format!("{composite_id}: {error}"));
            }
            if let Some(previous) = target_paths.insert(target.path.clone(), composite_id.clone()) {
                errors.push(format!(
                    "target path {} is shared by {previous} and {composite_id}",
                    target.path.display()
                ));
            }
            if !source_roles.contains(target.source_role.as_str())
                && !matches!(
                    target.source_role.as_str(),
                    "project-spec" | "identity-brief"
                )
            {
                errors.push(format!(
                    "{composite_id} requires undeclared source role {:?}",
                    target.source_role
                ));
            }
            if target.width.is_some() != target.height.is_some() {
                errors.push(format!(
                    "{composite_id} must declare both width and height or neither"
                ));
            }
            if target.width == Some(0) || target.height == Some(0) {
                errors.push(format!(
                    "{composite_id} dimensions must be greater than zero"
                ));
            }
            if target.format.trim().is_empty() || target.description.trim().is_empty() {
                errors.push(format!(
                    "{composite_id} must declare format and description"
                ));
            }
        }
    }
}

pub fn resolve_plan(project: &ValidatedProject) -> ResolvedPlan {
    let profiles = project
        .profiles
        .iter()
        .map(|profile| ResolvedProfile {
            id: profile.id.clone(),
            version: profile.version.clone(),
            verified_at: profile.verified_at.clone(),
            references: profile.references.clone(),
        })
        .collect();

    let mut targets = project
        .profiles
        .iter()
        .flat_map(|profile| {
            profile.targets.iter().map(|target| ResolvedTarget {
                profile: profile.id.clone(),
                id: target.id.clone(),
                path: project.spec.paths.output_root.join(&target.path),
                format: target.format.clone(),
                source_role: target.source_role.clone(),
                description: target.description.clone(),
                dimensions: target
                    .width
                    .zip(target.height)
                    .map(|(width, height)| format!("{width}x{height}")),
                purpose: target.purpose.clone(),
                maximum_bytes: target.maximum_bytes,
                required: target.required,
            })
        })
        .collect::<Vec<_>>();
    targets.sort_by(|left, right| left.path.cmp(&right.path));

    ResolvedPlan {
        schema: "identity.plan/v0",
        project_id: project.spec.project.id.clone(),
        display_name: project.spec.project.display_name.clone(),
        output_root: project.spec.paths.output_root.clone(),
        profiles,
        targets,
    }
}

pub fn validate_relative_path(path: &Path, label: &str) -> Result<()> {
    if path.as_os_str().is_empty() {
        bail!("{label} must not be empty");
    }
    if path.is_absolute() {
        bail!("{label} must be repository-relative: {}", path.display());
    }
    for component in path.components() {
        if matches!(
            component,
            Component::ParentDir | Component::RootDir | Component::Prefix(_)
        ) {
            bail!("{label} may not escape the repository: {}", path.display());
        }
    }
    Ok(())
}

pub fn reject_symlink_components(repository_root: &Path, path: &Path, label: &str) -> Result<()> {
    validate_relative_path(path, label)?;
    let mut current = repository_root.to_path_buf();
    for component in path.components() {
        if let Component::Normal(segment) = component {
            current.push(segment);
            if current
                .symlink_metadata()
                .is_ok_and(|metadata| metadata.file_type().is_symlink())
            {
                bail!(
                    "{label} may not traverse a symbolic link: {}",
                    path.display()
                );
            }
        }
    }
    Ok(())
}

fn validate_existing_path(
    repository_root: &Path,
    path: &Path,
    require_file: bool,
    label: &str,
) -> Result<()> {
    let candidate = repository_root.join(path);
    let canonical = candidate
        .canonicalize()
        .with_context(|| format!("{label} does not exist: {}", path.display()))?;
    if !canonical.starts_with(repository_root) {
        bail!("{label} escapes the repository: {}", path.display());
    }
    if require_file && !canonical.is_file() {
        bail!("{label} is not a file: {}", path.display());
    }
    if !require_file && !canonical.is_dir() {
        bail!("{label} is not a directory: {}", path.display());
    }
    Ok(())
}

fn load_profile(profile_id: &str) -> Result<Profile> {
    let profile_path = Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("profiles")
        .join(format!("{profile_id}.json"));
    let contents = fs::read_to_string(&profile_path)
        .with_context(|| format!("cannot read {}", profile_path.display()))?;
    let profile: Profile = serde_json::from_str(&contents)
        .with_context(|| format!("invalid JSON in {}", profile_path.display()))?;
    if profile.id != profile_id {
        bail!(
            "profile id {:?} does not match filename {profile_id:?}",
            profile.id
        );
    }
    Ok(profile)
}

pub(crate) fn valid_identifier(value: &str) -> bool {
    !value.is_empty()
        && !value.starts_with('-')
        && !value.ends_with('-')
        && value
            .bytes()
            .all(|byte| byte.is_ascii_lowercase() || byte.is_ascii_digit() || byte == b'-')
}

fn valid_semantic_version(value: &str) -> bool {
    let valid_segment =
        |segment: &str| !segment.is_empty() && segment.bytes().all(|byte| byte.is_ascii_digit());
    let mut segments = value.split('.');
    segments.next().is_some_and(valid_segment)
        && segments.next().is_some_and(valid_segment)
        && segments.next().is_some_and(valid_segment)
        && segments.next().is_none()
}

#[cfg(test)]
mod tests {
    use std::path::Path;

    use super::{valid_identifier, validate_relative_path};

    #[test]
    fn identifiers_are_stable_and_path_safe() {
        assert!(valid_identifier("project-2"));
        assert!(!valid_identifier("Project"));
        assert!(!valid_identifier("-project"));
    }

    #[test]
    fn repository_paths_cannot_escape() {
        assert!(validate_relative_path(Path::new("assets/identity"), "path").is_ok());
        assert!(validate_relative_path(Path::new("../outside"), "path").is_err());
        assert!(validate_relative_path(Path::new("/absolute"), "path").is_err());
    }
}
