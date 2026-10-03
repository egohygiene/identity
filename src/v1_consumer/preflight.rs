// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

//! The release embeds the authoritative stdlib validator; consumer checkouts
//! never supply executable validation code. Python runs without site packages,
//! PYTHONPATH, or imports from the current working directory.

use std::collections::BTreeMap;
use std::fs;
use std::io::Write;
use std::path::Path;
use std::process::{Command, Stdio};

use serde::Deserialize;

use crate::compiler::{CompilerError, CompilerResult, Diagnostic, FailureKind, sha256_hex};

const VALIDATOR: &str = include_str!("../../scripts/validate_identity.py");

#[derive(Clone, Debug, Deserialize)]
#[serde(deny_unknown_fields)]
pub(super) struct Snapshot {
    files: BTreeMap<String, String>,
    directories: Vec<String>,
}

impl Snapshot {
    pub(super) fn verify(&self, root: &Path) -> CompilerResult<()> {
        for (relative, digest) in &self.files {
            let path = checked_path(root, relative)?;
            let metadata = fs::metadata(&path).map_err(|error| stale(relative, error))?;
            if !metadata.is_file() {
                return Err(stale(relative, "source is no longer a regular file"));
            }
            let bytes = fs::read(path).map_err(|error| stale(relative, error))?;
            if sha256_hex(&bytes) != *digest {
                return Err(stale(relative, "source bytes changed after preflight"));
            }
        }
        for relative in &self.directories {
            if !checked_path(root, relative)?.is_dir() {
                return Err(stale(relative, "source directory changed after preflight"));
            }
        }
        Ok(())
    }
}

fn checked_path(root: &Path, relative: &str) -> CompilerResult<std::path::PathBuf> {
    crate::compiler::validate_portable_path(relative, "source path")?;
    let mut path = root.to_path_buf();
    for segment in relative.split('/') {
        path.push(segment);
        let metadata = path
            .symlink_metadata()
            .map_err(|error| stale(relative, error))?;
        if metadata.file_type().is_symlink() {
            return Err(stale(relative, "source path traverses a symbolic link"));
        }
    }
    Ok(path)
}

pub(super) fn stale(path: &str, message: impl std::fmt::Display) -> CompilerError {
    CompilerError::new(
        FailureKind::Drifted,
        Diagnostic::error(
            "IDN3303",
            FailureKind::Drifted,
            Some(path.to_owned()),
            message.to_string(),
            "Reload and validate the source, then create a new plan.",
        ),
    )
}

fn unavailable(message: impl std::fmt::Display) -> CompilerError {
    CompilerError::new(
        FailureKind::Unsupported,
        Diagnostic::error(
            "IDN3302",
            FailureKind::Unsupported,
            None,
            format!("cannot run embedded v1 source preflight: {message}"),
            "Install Python 3.11 or newer on PATH (python3 on Unix, python on Windows), or set IDENTITY_PYTHON to its executable path.",
        ),
    )
}

#[derive(Deserialize)]
struct PreflightResult {
    schema: String,
    valid: bool,
    diagnostics: Vec<SourceDiagnostic>,
    snapshot: Snapshot,
}

#[derive(Deserialize)]
struct SourceDiagnostic {
    code: String,
    path: String,
    message: String,
    recovery: String,
    severity: String,
}

pub(super) fn validate(root: &Path) -> CompilerResult<Snapshot> {
    let python = std::env::var_os("IDENTITY_PYTHON")
        .unwrap_or_else(|| if cfg!(windows) { "python" } else { "python3" }.into());
    let mut child = Command::new(python)
        .args(["-I", "-S", "-", "--repository-root"])
        .arg(root)
        .args(["--format", "json", "--snapshot"])
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(unavailable)?;
    let mut stdin = child.stdin.take().expect("piped preflight stdin");
    let sent = stdin.write_all(
        b"import sys\nif sys.version_info < (3, 11):\n    raise SystemExit('Python 3.11 or newer is required')\n"
    ).and_then(|()| {
        // Future imports must stay at the beginning of the embedded module.
        // exec also preserves its normal __main__ entry point.
        let source = serde_json::to_string(VALIDATOR).expect("serialize embedded validator");
        writeln!(stdin, "exec({source})")
    });
    drop(stdin);
    let output = child.wait_with_output().map_err(unavailable)?;
    sent.map_err(unavailable)?;
    let result: PreflightResult = serde_json::from_slice(&output.stdout).map_err(|error| {
        unavailable(format!(
            "{error}; {}",
            String::from_utf8_lossy(&output.stderr)
        ))
    })?;
    if result.schema != "identity.diagnostics/v1"
        || result.valid != result.diagnostics.is_empty()
        || result.valid != output.status.success()
        || result
            .diagnostics
            .iter()
            .any(|value| value.severity != "error")
    {
        return Err(unavailable("invalid authoritative validator response"));
    }
    if !result.valid {
        return Err(CompilerError::from_diagnostics(
            FailureKind::Invalid,
            result
                .diagnostics
                .into_iter()
                .map(|value| {
                    Diagnostic::error(
                        value.code,
                        FailureKind::Invalid,
                        Some(value.path),
                        value.message,
                        value.recovery,
                    )
                })
                .collect(),
        ));
    }
    result.snapshot.verify(root)?;
    Ok(result.snapshot)
}
