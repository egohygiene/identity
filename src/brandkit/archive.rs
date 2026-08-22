// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

use crate::compiler::{CompilerError, CompilerResult, Diagnostic, FailureKind};

const LOCAL_FILE_HEADER: u32 = 0x0403_4b50;
const CENTRAL_DIRECTORY_HEADER: u32 = 0x0201_4b50;
const END_OF_CENTRAL_DIRECTORY: u32 = 0x0605_4b50;
const DOS_DATE_1980_01_01: u16 = 0x0021;
const ZIP_VERSION: u16 = 20;

#[derive(Clone, Debug)]
struct CentralEntry {
    name: String,
    crc32: u32,
    size: u32,
    local_offset: u32,
}

pub(super) fn deterministic_zip(entries: &[(String, Vec<u8>)]) -> CompilerResult<Vec<u8>> {
    let mut ordered = entries.to_vec();
    ordered.sort_by(|left, right| left.0.cmp(&right.0));

    let mut output = Vec::new();
    let mut central = Vec::new();
    for (name, bytes) in ordered {
        validate_entry_name(&name)?;
        let name_bytes = name.as_bytes();
        let size = u32::try_from(bytes.len()).map_err(|error| {
            archive_error(
                &name,
                format!("archive entry is too large for the deterministic ZIP32 writer: {error}"),
            )
        })?;
        let local_offset = u32::try_from(output.len()).map_err(|error| {
            archive_error(
                &name,
                format!("archive offset exceeds deterministic ZIP32 limits: {error}"),
            )
        })?;
        let name_length = u16::try_from(name_bytes.len()).map_err(|error| {
            archive_error(&name, format!("archive entry name is too long: {error}"))
        })?;
        let checksum = crc32(&bytes);

        push_u32(&mut output, LOCAL_FILE_HEADER);
        push_u16(&mut output, ZIP_VERSION);
        push_u16(&mut output, 0);
        push_u16(&mut output, 0);
        push_u16(&mut output, 0);
        push_u16(&mut output, DOS_DATE_1980_01_01);
        push_u32(&mut output, checksum);
        push_u32(&mut output, size);
        push_u32(&mut output, size);
        push_u16(&mut output, name_length);
        push_u16(&mut output, 0);
        output.extend_from_slice(name_bytes);
        output.extend_from_slice(&bytes);

        central.push(CentralEntry {
            name,
            crc32: checksum,
            size,
            local_offset,
        });
    }

    let central_offset = u32::try_from(output.len()).map_err(|error| {
        archive_error(
            "central-directory",
            format!("central directory offset exceeds ZIP32 limits: {error}"),
        )
    })?;
    for entry in &central {
        let name_length = u16::try_from(entry.name.len()).map_err(|error| {
            archive_error(
                &entry.name,
                format!("archive entry name is too long: {error}"),
            )
        })?;
        push_u32(&mut output, CENTRAL_DIRECTORY_HEADER);
        push_u16(&mut output, ZIP_VERSION);
        push_u16(&mut output, ZIP_VERSION);
        push_u16(&mut output, 0);
        push_u16(&mut output, 0);
        push_u16(&mut output, 0);
        push_u16(&mut output, DOS_DATE_1980_01_01);
        push_u32(&mut output, entry.crc32);
        push_u32(&mut output, entry.size);
        push_u32(&mut output, entry.size);
        push_u16(&mut output, name_length);
        push_u16(&mut output, 0);
        push_u16(&mut output, 0);
        push_u16(&mut output, 0);
        push_u16(&mut output, 0);
        push_u32(&mut output, 0);
        push_u32(&mut output, entry.local_offset);
        output.extend_from_slice(entry.name.as_bytes());
    }

    let central_size = u32::try_from(output.len())
        .map_err(|error| archive_error("central-directory", error.to_string()))?
        .checked_sub(central_offset)
        .ok_or_else(|| archive_error("central-directory", "invalid directory size".to_owned()))?;
    let entry_count = u16::try_from(central.len()).map_err(|error| {
        archive_error(
            "central-directory",
            format!("too many deterministic ZIP32 entries: {error}"),
        )
    })?;

    push_u32(&mut output, END_OF_CENTRAL_DIRECTORY);
    push_u16(&mut output, 0);
    push_u16(&mut output, 0);
    push_u16(&mut output, entry_count);
    push_u16(&mut output, entry_count);
    push_u32(&mut output, central_size);
    push_u32(&mut output, central_offset);
    push_u16(&mut output, 0);
    Ok(output)
}

pub(super) fn looks_like_deterministic_zip(bytes: &[u8]) -> bool {
    bytes.starts_with(&LOCAL_FILE_HEADER.to_le_bytes())
        && bytes
            .windows(END_OF_CENTRAL_DIRECTORY.to_le_bytes().len())
            .any(|window| window == END_OF_CENTRAL_DIRECTORY.to_le_bytes())
}

fn validate_entry_name(name: &str) -> CompilerResult<()> {
    if name.is_empty()
        || name.starts_with('/')
        || name.ends_with('/')
        || name.contains('\\')
        || name
            .split('/')
            .any(|segment| segment.is_empty() || matches!(segment, "." | ".."))
    {
        return Err(archive_error(
            name,
            "archive entry name must be a normalized relative path".to_owned(),
        ));
    }
    Ok(())
}

fn archive_error(path: &str, message: String) -> CompilerError {
    CompilerError::new(
        FailureKind::Failed,
        Diagnostic::error(
            "IDN3401",
            FailureKind::Failed,
            Some(path.to_owned()),
            message,
            "Use a normalized package path and keep the Brand Kit archive within ZIP32 limits.",
        ),
    )
}

fn crc32(bytes: &[u8]) -> u32 {
    let mut crc = 0xffff_ffff_u32;
    for byte in bytes {
        crc ^= u32::from(*byte);
        for _ in 0..8 {
            let mask = 0_u32.wrapping_sub(crc & 1);
            crc = (crc >> 1) ^ (0xedb8_8320_u32 & mask);
        }
    }
    !crc
}

fn push_u16(output: &mut Vec<u8>, value: u16) {
    output.extend_from_slice(&value.to_le_bytes());
}

fn push_u32(output: &mut Vec<u8>, value: u32) {
    output.extend_from_slice(&value.to_le_bytes());
}
