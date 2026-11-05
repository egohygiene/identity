// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

//! Optional source preparation shares the v1 isolated Python runtime boundary.
//! Only trusted, release-embedded code executes; a consumer supplies data paths.

use std::io::Write;
use std::process::{Command, Stdio};

use anyhow::{Context, Result, bail};

use crate::cli::V1InitArguments;
use crate::compiler::sha256_hex;

const INITIALIZER: &str = include_str!("../scripts/initialize_identity.py");
const VALIDATOR: &str = include_str!("../scripts/validate_identity.py");

pub(crate) fn run(arguments: &V1InitArguments) -> Result<()> {
    let python = std::env::var_os("IDENTITY_PYTHON")
        .unwrap_or_else(|| if cfg!(windows) { "python" } else { "python3" }.into());
    let mut child = Command::new(python)
        .args(["-I", "-S", "-", "--repository-root"])
        .arg(&arguments.repository_root)
        .arg("--request")
        .arg(&arguments.request)
        .arg("--output-directory")
        .arg(&arguments.output_directory)
        .stdin(Stdio::piped())
        .spawn()
        .context(
            "v1-init requires Python 3.11+; install it separately or select IDENTITY_PYTHON",
        )?;
    let mut stdin = child
        .stdin
        .take()
        .context("initializer stdin is unavailable")?;
    let program = format!(
        "import sys\nif sys.version_info < (3, 11):\n    raise SystemExit('Python 3.11 or newer is required')\n__identity_validator_source = {}\n__identity_initializer_sha256 = {}\n__identity_implementation_version = {}\nexec({})\n",
        serde_json::to_string(VALIDATOR)?,
        serde_json::to_string(&sha256_hex(INITIALIZER.as_bytes()))?,
        serde_json::to_string(env!("CARGO_PKG_VERSION"))?,
        serde_json::to_string(INITIALIZER)?,
    );
    let sent = stdin.write_all(program.as_bytes());
    drop(stdin);
    let status = child.wait().context("cannot wait for v1 initializer")?;
    sent.context("cannot send embedded initializer to Python")?;
    if !status.success() {
        bail!("v1 candidate preparation failed; supplied source is not adopted or regenerated");
    }
    Ok(())
}
