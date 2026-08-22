// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

use std::fmt::Write as _;

use identity::motion::{
    MOTION_POLICY_SCHEMA, MotionPolicy, VISUAL_MOTION_MANIFEST_SCHEMA, VisualMotionManifest,
};
use serde::de::DeserializeOwned;
use sha2::{Digest, Sha256};

const POLICY: &str = include_str!("fixtures/motion/motion-policy.json");
const MANIFEST: &str = include_str!("fixtures/motion/visual-motion-manifest.json");
const STORYBOARD: &[u8] = include_bytes!("fixtures/motion/identity-hero.storyboard.txt");
const HERO: &[u8] = include_bytes!("fixtures/motion/identity-hero.svg");
const REDUCED: &[u8] = include_bytes!("fixtures/motion/identity-hero-reduced.svg");

#[test]
fn checked_in_visual_motion_fixture_is_content_addressed() {
    let policy: MotionPolicy = contract_payload(POLICY);
    let manifest: VisualMotionManifest = contract_payload(MANIFEST);
    let reduced_sha = sha256_hex(REDUCED);

    assert_eq!(policy.schema, MOTION_POLICY_SCHEMA);
    assert_eq!(manifest.schema, VISUAL_MOTION_MANIFEST_SCHEMA);
    assert_eq!(manifest.assets.len(), 1);

    let asset = &manifest.assets[0];
    assert_eq!(asset.source.sha256, sha256_hex(STORYBOARD));
    assert_eq!(asset.output.sha256, sha256_hex(HERO));
    assert_eq!(
        asset.output.bytes,
        u64::try_from(HERO.len()).expect("fixture size fits u64")
    );
    assert_eq!(
        asset.behavior.fallback_sha256.as_deref(),
        Some(reduced_sha.as_str())
    );
}

fn contract_payload<T: DeserializeOwned>(text: &str) -> T {
    let mut value: serde_json::Value = serde_json::from_str(text).expect("parse contract JSON");
    value
        .as_object_mut()
        .expect("contract fixture is an object")
        .remove("$schema");
    serde_json::from_value(value).expect("deserialize semantic contract payload")
}

fn sha256_hex(bytes: &[u8]) -> String {
    let digest = Sha256::digest(bytes);
    let mut encoded = String::with_capacity(64);
    for byte in digest {
        write!(&mut encoded, "{byte:02x}").expect("writing to a String cannot fail");
    }
    encoded
}
