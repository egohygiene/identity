// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

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
    }
}
