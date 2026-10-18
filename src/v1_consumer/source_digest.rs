// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

//! egohygiene.identity.source-digest/v1; see `docs/contracts/SOURCE_DIGEST_V1.md`.

use std::fs;
use std::path::{Path, PathBuf};

use crate::compiler::{CompilerResult, sha256_hex, validate_portable_path};

use super::invalid;

// Components are ordered by their exact UTF-8 bytes, independently of the host
// filesystem's path ordering. In particular, Windows must not fold case here.
type SourceFile = (Vec<String>, PathBuf);

pub(super) fn canonical_source_digest(repository_root: &Path) -> CompilerResult<String> {
    let mut bytes = Vec::new();
    for (components, path) in canonical_source_files(repository_root)? {
        let relative = components.join("/");
        let content = fs::read(path).map_err(|error| invalid(&relative, error.to_string()))?;
        bytes.extend_from_slice(relative.as_bytes());
        bytes.push(0);
        bytes.extend_from_slice(&content);
        bytes.push(0);
    }
    Ok(sha256_hex(&bytes))
}

fn is_link(metadata: &fs::Metadata) -> bool {
    #[cfg(windows)]
    {
        use std::os::windows::fs::MetadataExt;
        // Includes junctions and other reparse points, not only symlinks.
        if metadata.file_attributes() & 0x400 != 0 {
            return true;
        }
    }
    metadata.file_type().is_symlink()
}

fn canonical_source_files(repository_root: &Path) -> CompilerResult<Vec<SourceFile>> {
    let root = repository_root.join(".identity");
    let metadata = root
        .symlink_metadata()
        .map_err(|error| invalid(".identity", error.to_string()))?;
    if is_link(&metadata) || !metadata.is_dir() {
        return Err(invalid(
            ".identity",
            "canonical source must be a local directory",
        ));
    }
    let mut files = Vec::new();
    collect_canonical_files(&root, &[".identity".to_owned()], &mut files)?;
    files.sort_by(|left, right| left.0.cmp(&right.0));
    Ok(files)
}

fn collect_canonical_files(
    current: &Path,
    prefix: &[String],
    files: &mut Vec<SourceFile>,
) -> CompilerResult<()> {
    let label = prefix.join("/");
    for entry in fs::read_dir(current).map_err(|error| invalid(&label, error.to_string()))? {
        let entry = entry.map_err(|error| invalid(&label, error.to_string()))?;
        let name = entry
            .file_name()
            .into_string()
            .map_err(|_| invalid(&label, "canonical source path must use valid UTF-8"))?;
        // Exclude by lexical name before inspecting or descending into the entry.
        if name == "README.md"
            || (prefix.len() == 1
                && matches!(name.as_str(), "identity.toml" | "candidates" | "references"))
        {
            continue;
        }
        let mut components = prefix.to_vec();
        components.push(name);
        let relative = components.join("/");
        validate_portable_path(&relative, "canonical source path")?;
        let path = entry.path();
        let metadata = path
            .symlink_metadata()
            .map_err(|error| invalid(&relative, error.to_string()))?;
        if is_link(&metadata) {
            return Err(invalid(
                &relative,
                "canonical source traverses a symbolic link or reparse point",
            ));
        }
        if metadata.is_dir() {
            collect_canonical_files(&path, &components, files)?;
        } else if metadata.is_file() {
            files.push((components, path));
        } else {
            return Err(invalid(
                &relative,
                "canonical source must contain only regular files and directories",
            ));
        }
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    use serde::Deserialize;
    use tempfile::TempDir;

    #[derive(Deserialize)]
    struct Vectors {
        contract: String,
        cases: Vec<Case>,
        paths: Vec<PathCase>,
    }

    #[derive(Deserialize)]
    struct Case {
        id: String,
        directories: Vec<String>,
        files: Vec<File>,
        links: Vec<Link>,
        inventory: Option<Vec<String>>,
        sha256: Option<String>,
    }

    #[derive(Deserialize)]
    struct File {
        path: String,
        hex: String,
    }

    #[derive(Deserialize)]
    struct Link {
        path: String,
        target: String,
        directory: bool,
    }

    #[derive(Deserialize)]
    struct PathCase {
        path: String,
        valid: bool,
    }

    fn vectors() -> Vectors {
        serde_json::from_str(include_str!("../../tests/fixtures/source-digest-v1.json"))
            .expect("parse shared Rust/Python digest vectors")
    }

    fn materialize(root: &Path, case: &Case) {
        for relative in &case.directories {
            fs::create_dir_all(root.join(relative)).expect("create vector directory");
        }
        for file in &case.files {
            let path = root.join(&file.path);
            fs::create_dir_all(path.parent().unwrap()).expect("create vector file parent");
            let bytes = file
                .hex
                .as_bytes()
                .chunks_exact(2)
                .map(|pair| {
                    u8::from_str_radix(std::str::from_utf8(pair).unwrap(), 16)
                        .expect("decode exact vector bytes")
                })
                .collect::<Vec<_>>();
            fs::write(path, bytes).expect("write exact vector bytes");
        }
        for link in &case.links {
            let path = root.join(&link.path);
            fs::create_dir_all(path.parent().unwrap()).expect("create vector link parent");
            create_symlink(link, &path);
        }
    }

    #[cfg(unix)]
    fn create_symlink(link: &Link, path: &Path) {
        // Unix does not distinguish file/directory links at creation time.
        let _ = link.directory;
        std::os::unix::fs::symlink(&link.target, path).expect("create shared vector link");
    }

    #[cfg(windows)]
    fn create_symlink(link: &Link, path: &Path) {
        if link.directory {
            std::os::windows::fs::symlink_dir(&link.target, path)
        } else {
            std::os::windows::fs::symlink_file(&link.target, path)
        }
        .expect("shared link vectors require symlink privilege on the Windows CI runner");
    }

    fn check_vector(case: &Case) {
        let repository = TempDir::new().expect("create vector repository");
        materialize(repository.path(), case);
        let result = canonical_source_digest(repository.path());
        if let Some(expected) = &case.sha256 {
            assert_eq!(&result.expect("hash vector"), expected, "{}", case.id);
            let inventory = canonical_source_files(repository.path())
                .expect("inventory vector")
                .into_iter()
                .map(|(components, _)| components.join("/"))
                .collect::<Vec<_>>();
            assert_eq!(Some(inventory), case.inventory, "{}", case.id);
        } else {
            assert!(result.is_err(), "{} must fail closed", case.id);
        }
    }

    #[test]
    fn shared_inventory_and_digest_vectors() {
        let vectors = vectors();
        assert_eq!(vectors.contract, "egohygiene.identity.source-digest/v1");
        for case in vectors.cases.iter().filter(|case| case.links.is_empty()) {
            check_vector(case);
        }
    }

    #[test]
    fn shared_symlink_vectors() {
        for case in vectors().cases.iter().filter(|case| !case.links.is_empty()) {
            check_vector(case);
        }
    }

    #[test]
    fn shared_portable_path_vectors() {
        for case in vectors().paths {
            assert_eq!(
                validate_portable_path(&case.path, "canonical source path").is_ok(),
                case.valid,
                "{:?}",
                case.path
            );
        }
    }

    #[cfg(unix)]
    #[test]
    fn non_utf8_source_names_are_rejected_without_lossy_conversion() {
        use std::os::unix::ffi::OsStrExt;

        let repository = TempDir::new().unwrap();
        let root = repository.path().join(".identity");
        fs::create_dir(&root).unwrap();
        fs::write(
            root.join(std::ffi::OsStr::from_bytes(b"invalid-\xff")),
            b"source",
        )
        .unwrap();
        assert!(canonical_source_digest(repository.path()).is_err());
    }

    #[cfg(unix)]
    #[test]
    fn non_regular_source_entries_are_rejected_without_reading() {
        let repository = TempDir::new().unwrap();
        let root = repository.path().join(".identity");
        fs::create_dir(&root).unwrap();
        let python = std::env::var_os("IDENTITY_PYTHON").unwrap_or_else(|| "python3".into());
        let output = std::process::Command::new(python)
            .args(["-I", "-S", "-c", "import os, sys; os.mkfifo(sys.argv[1])"])
            .arg(root.join("pipe"))
            .output()
            .expect("create FIFO vector without opening it");
        assert!(output.status.success(), "{:?}", output.stderr);
        assert!(canonical_source_digest(repository.path()).is_err());
    }

    #[cfg(windows)]
    #[test]
    fn windows_junctions_are_rejected_as_reparse_points() {
        let repository = TempDir::new().unwrap();
        let root = repository.path().join(".identity");
        let target = repository.path().join("outside");
        fs::create_dir(&root).unwrap();
        fs::create_dir(&target).unwrap();
        let output = std::process::Command::new("cmd")
            .args(["/C", "mklink", "/J"])
            .arg(root.join("junction"))
            .arg(target)
            .output()
            .expect("create Windows junction vector");
        assert!(output.status.success(), "{:?}", output.stderr);
        assert!(canonical_source_digest(repository.path()).is_err());
    }
}
