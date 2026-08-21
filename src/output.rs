// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

use std::fmt::Write as _;

use crate::contract::ResolvedPlan;

pub fn render_plan_markdown(plan: &ResolvedPlan) -> String {
    let mut output = String::new();
    writeln!(output, "# Identity asset plan — {}", plan.display_name)
        .expect("writing to String cannot fail");
    writeln!(output).expect("writing to String cannot fail");
    writeln!(output, "- Schema: `{}`", plan.schema).expect("writing to String cannot fail");
    writeln!(output, "- Project: `{}`", plan.project_id).expect("writing to String cannot fail");
    writeln!(output, "- Output root: `{}`", plan.output_root.display())
        .expect("writing to String cannot fail");
    writeln!(output, "- Targets: {}", plan.targets.len()).expect("writing to String cannot fail");
    writeln!(output).expect("writing to String cannot fail");

    for profile in &plan.profiles {
        writeln!(output, "## {} profile", profile.id).expect("writing to String cannot fail");
        writeln!(output).expect("writing to String cannot fail");
        writeln!(
            output,
            "Version `{}`; requirements verified `{}`.",
            profile.version, profile.verified_at
        )
        .expect("writing to String cannot fail");
        writeln!(output).expect("writing to String cannot fail");
        writeln!(
            output,
            "| Target | Output | Size | Source | Required | Purpose |"
        )
        .expect("writing to String cannot fail");
        writeln!(output, "| --- | --- | --- | --- | --- | --- |")
            .expect("writing to String cannot fail");
        for target in plan
            .targets
            .iter()
            .filter(|target| target.profile == profile.id)
        {
            writeln!(
                output,
                "| `{}` | `{}` | {} | `{}` | {} | {} |",
                target.id,
                target.path.display(),
                target.dimensions.as_deref().unwrap_or("vector/variable"),
                target.source_role,
                if target.required { "yes" } else { "no" },
                target.purpose.as_deref().unwrap_or(&target.description)
            )
            .expect("writing to String cannot fail");
        }
        writeln!(output).expect("writing to String cannot fail");
    }

    output
}
