// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

use std::collections::BTreeSet;

use serde_json::Value;

use super::BrandKitGuidance;

/// Public artifacts and explicit maintainer review have different authority boundaries.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum GuidanceAudience {
    Public,
    Review,
}

impl BrandKitGuidance {
    /// Project validated guidance without changing its canonical or review source.
    ///
    /// Public outputs retain only approved/public governed records, including
    /// nested records. Review preserves the complete lifecycle history.
    #[must_use]
    pub fn for_audience(&self, audience: GuidanceAudience) -> Self {
        if audience == GuidanceAudience::Review {
            return self.clone();
        }
        let mut voice = self.voice.as_ref().and_then(public_records);
        let mut usage = self.usage.as_ref().and_then(public_records);
        if let Some(voice) = &mut voice {
            project_voice_references(voice);
        }
        if let Some(usage) = &mut usage {
            project_usage_sections_and_assets(usage);
        }
        Self { voice, usage }
    }
}

fn public_records(value: &Value) -> Option<Value> {
    match value {
        Value::Object(object) => {
            if let Some(governance) = object.get("governance")
                && (governance.get("state").and_then(Value::as_str) != Some("approved")
                    || governance.get("visibility").and_then(Value::as_str) != Some("public"))
            {
                return None;
            }
            Some(Value::Object(
                object
                    .iter()
                    .filter_map(|(key, child)| {
                        public_records(child).map(|value| (key.clone(), value))
                    })
                    .collect(),
            ))
        }
        Value::Array(items) => Some(Value::Array(
            items.iter().filter_map(public_records).collect(),
        )),
        _ => Some(value.clone()),
    }
}

fn project_voice_references(voice: &mut Value) {
    let Some(characteristics) = voice.get("characteristics").and_then(Value::as_array) else {
        return;
    };
    let public_ids: BTreeSet<String> = characteristics
        .iter()
        .filter_map(|item| item.get("id").and_then(Value::as_str).map(str::to_owned))
        .collect();
    if let Some(contexts) = voice.get_mut("contexts").and_then(Value::as_array_mut) {
        for context in contexts {
            if let Some(references) = context
                .get_mut("characteristics")
                .and_then(Value::as_array_mut)
            {
                references.retain(|id| id.as_str().is_some_and(|id| public_ids.contains(id)));
            }
        }
    }
}

fn project_usage_sections_and_assets(usage: &mut Value) {
    if let Some(sections) = usage.get_mut("sections").and_then(Value::as_array_mut) {
        sections.retain(|section| {
            section
                .get("rules")
                .and_then(Value::as_array)
                .is_some_and(|rules| !rules.is_empty())
        });
    }
    if let Some(assets) = usage.get_mut("assets").and_then(Value::as_array_mut) {
        assets.retain(|asset| asset.get("availability").and_then(Value::as_str) == Some("public"));
    }
}
