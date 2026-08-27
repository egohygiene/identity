// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

export const CANDIDATE_BUNDLE_SCHEMA = "identity.brand-kit-candidate/v1";

export function inspectCandidateBundle(value, model) {
  const errors = [];
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    return { errors: ["Candidate bundle must be a JSON object."], plan: null };
  }
  if (value.schema !== CANDIDATE_BUNDLE_SCHEMA) {
    errors.push(`Expected schema ${CANDIDATE_BUNDLE_SCHEMA}.`);
  }
  if (value.projectId !== model.projectId) {
    errors.push("Candidate bundle projectId does not match this immutable release.");
  }
  if (value.sourceDigest !== model.release.sourceDigest) {
    errors.push("Candidate bundle sourceDigest does not match this immutable release.");
  }
  if (!Array.isArray(value.candidates) || value.candidates.length === 0) {
    errors.push("Candidate bundle must declare at least one candidate.");
  }
  const candidates = Array.isArray(value.candidates) ? value.candidates : [];
  const candidateIds = new Set();
  for (const candidate of candidates) {
    if (!candidate || typeof candidate !== "object" || !candidate.id || !candidate.kind || !candidate.provenance) {
      errors.push("Every candidate requires id, kind, and provenance.");
      continue;
    }
    if (candidateIds.has(candidate.id)) errors.push(`Candidate id ${candidate.id} is duplicated.`);
    candidateIds.add(candidate.id);
  }
  if (errors.length > 0) return { errors, plan: null };
  return {
    errors: [],
    plan: {
      schema: "identity.studio-plan/v1",
      projectId: model.projectId,
      sourceDigest: model.release.sourceDigest,
      status: "requires-human-approval",
      writes: candidates.map((candidate) => ({ id: candidate.id, kind: candidate.kind, action: "stage-for-compiler-review" })),
      warnings: ["No canonical .identity/ or generated asset files have been changed."],
    },
  };
}

export function createApprovedHandoff(plan, reviewer) {
  if (!plan || plan.status !== "requires-human-approval") throw new Error("A reviewable plan is required.");
  if (!reviewer?.trim()) throw new Error("Reviewer identity is required.");
  return { ...plan, status: "approved-for-compiler-handoff", approval: { reviewer: reviewer.trim(), method: "explicit-local-studio" } };
}
