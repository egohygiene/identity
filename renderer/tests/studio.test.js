// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { describe, expect, test } from "vitest";

import { createApprovedHandoff, inspectCandidateBundle } from "../src/studio.js";

const model = {
  projectId: "example",
  release: { sourceDigest: "sha256:example" },
};

const candidateBundle = {
  schema: "identity.brand-kit-candidate/v1",
  projectId: "example",
  sourceDigest: "sha256:example",
  profiles: ["pwa", "social"],
  candidates: [{ id: "candidate-mark", kind: "mark", state: "candidate", provenance: { source: "local" } }],
};

describe("candidate studio contract", () => {
  test("creates a review-only plan without canonical writes", () => {
    const inspected = inspectCandidateBundle(candidateBundle, model);
    expect(inspected.errors).toEqual([]);
    expect(inspected.plan.status).toBe("requires-human-approval");
    expect(inspected.plan.profiles).toEqual(["pwa", "social"]);
    expect(inspected.plan.writes[0].action).toBe("stage-for-compiler-review");
  });

  test("rejects a bundle from a different immutable release", () => {
    const inspected = inspectCandidateBundle({ ...candidateBundle, sourceDigest: "sha256:other" }, model);
    expect(inspected.plan).toBeNull();
    expect(inspected.errors.join(" ")).toContain("sourceDigest");
  });

  test("requires explicit reviewer identity before handoff", () => {
    const plan = inspectCandidateBundle(candidateBundle, model).plan;
    expect(() => createApprovedHandoff(plan, "")).toThrow("Reviewer identity");
    expect(createApprovedHandoff(plan, "reviewer").status).toBe("approved-for-compiler-handoff");
  });

  test("preserves candidate lifecycle states and rejects unsupported profiles", () => {
    const historical = {
      ...candidateBundle,
      candidates: [
        { id: "candidate", kind: "mark", state: "candidate", provenance: { source: "local" } },
        { id: "rejected", kind: "mark", state: "rejected", provenance: { source: "local" } },
        { id: "superseded", kind: "mark", state: "superseded", provenance: { source: "local" } },
        { id: "approved", kind: "mark", state: "approved", provenance: { source: "local" } },
      ],
    };
    const inspected = inspectCandidateBundle(historical, model);
    expect(inspected.errors).toEqual([]);
    expect(inspected.plan.writes).toEqual([{
      id: "candidate",
      kind: "mark",
      action: "stage-for-compiler-review",
    }]);
    const historicalOnly = inspectCandidateBundle({
      ...candidateBundle,
      candidates: [{ id: "rejected", kind: "mark", state: "rejected", provenance: { source: "local" } }],
    }, model).plan;
    expect(() => createApprovedHandoff(historicalOnly, "reviewer")).toThrow("current candidate");
    const unsupported = inspectCandidateBundle({ ...candidateBundle, profiles: ["imaginary"] }, model);
    expect(unsupported.plan).toBeNull();
    expect(unsupported.errors.join(" ")).toContain("Unsupported deterministic output profile");
  });
});
