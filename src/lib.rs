// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

pub mod brandkit;
pub mod compiler;
pub mod motion;
pub mod quality;
pub mod reference_renderer;
pub mod v1_consumer;

mod cli;
mod commands;
mod contract;
mod output;

use anyhow::Result;
use clap::Parser;

use crate::cli::{Cli, Command};

pub fn run() -> Result<()> {
    let cli = Cli::parse();
    match cli.command {
        Command::Init(arguments) => commands::init(&arguments),
        Command::Validate(arguments) => commands::validate(&arguments),
        Command::Plan(arguments) => commands::plan(&arguments),
        Command::Handoff(arguments) => commands::handoff(&arguments),
        Command::StudioReview(arguments) => commands::studio_review(&arguments),
        Command::V1Generate(arguments) => commands::v1_generate(&arguments),
        Command::V1Verify(arguments) => commands::v1_verify(&arguments),
    }
}
