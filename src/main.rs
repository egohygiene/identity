// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

use std::process::ExitCode;

fn main() -> ExitCode {
    match identity::run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("error: {error:#}");
            ExitCode::FAILURE
        }
    }
}
