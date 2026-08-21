// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

use std::path::PathBuf;

use clap::{Args, Parser, Subcommand, ValueEnum};

#[derive(Debug, Parser)]
#[command(
    name = "identity",
    version,
    about = "Plan and compile a project's visual identity from a versioned specification"
)]
pub struct Cli {
    #[command(subcommand)]
    pub command: Command,
}

#[derive(Debug, Subcommand)]
pub enum Command {
    /// Initialize a consumer-owned .identity directory.
    Init(InitArguments),
    /// Validate the project specification and selected profiles.
    Validate(RepositoryArguments),
    /// Resolve selected profiles into an explainable asset plan.
    Plan(PlanArguments),
    /// Build a deterministic creative handoff for a human or external tool.
    Handoff(HandoffArguments),
}

#[derive(Debug, Args)]
pub struct RepositoryArguments {
    /// Root of the consumer repository.
    #[arg(long, default_value = ".")]
    pub repository_root: PathBuf,
}

#[derive(Debug, Args)]
pub struct InitArguments {
    /// Root of the consumer repository.
    #[arg(long, default_value = ".")]
    pub repository_root: PathBuf,
    /// Stable lowercase project identifier.
    #[arg(long)]
    pub project_id: String,
    /// Human-facing project name.
    #[arg(long)]
    pub display_name: String,
    /// Replace identity files that already exist.
    #[arg(long, default_value_t = false)]
    pub force: bool,
}

#[derive(Clone, Copy, Debug, ValueEnum)]
pub enum PlanFormat {
    Json,
    Markdown,
}

#[derive(Debug, Args)]
pub struct PlanArguments {
    /// Root of the consumer repository.
    #[arg(long, default_value = ".")]
    pub repository_root: PathBuf,
    /// Serialization used for the resolved plan.
    #[arg(long, value_enum, default_value = "markdown")]
    pub format: PlanFormat,
    /// Optional repository-relative output file. Stdout is used when omitted.
    #[arg(long)]
    pub output: Option<PathBuf>,
}

#[derive(Debug, Args)]
pub struct HandoffArguments {
    /// Root of the consumer repository.
    #[arg(long, default_value = ".")]
    pub repository_root: PathBuf,
    /// Repository-relative destination for generated handoff files.
    #[arg(long, default_value = ".cache/identity/handoff")]
    pub output_directory: PathBuf,
}
