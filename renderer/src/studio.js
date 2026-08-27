// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

export const CANDIDATE_BUNDLE_SCHEMA = "identity.brand-kit-candidate/v1";

export const CANDIDATE_STATES = Object.freeze([
  "candidate",
  "approved",
  "rejected",
  "superseded",
]);

export const SUPPORTED_OUTPUT_PROFILES = Object.freeze([
  "core",
  "web",
  "pwa",
  "github",
  "docs",
  "social",
  "tokens",
  "metadata",
]);

const candidateStates = new Set(CANDIDATE_STATES);
const supportedOutputProfiles = new Set(SUPPORTED_OUTPUT_PROFILES);

export function inspectCandidateBundle(value, model) {
  const errors = [];
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    return { bundle: null, errors: ["Candidate bundle must be a JSON object."], plan: null };
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

  const profiles = normalizeProfiles(value.profiles, errors);
  const candidates = normalizeCandidates(value.candidates, model, errors);
  if (errors.length > 0) return { bundle: null, errors, plan: null };

  const bundle = {
    schema: CANDIDATE_BUNDLE_SCHEMA,
    projectId: model.projectId,
    sourceDigest: model.release.sourceDigest,
    profiles,
    candidates,
  };
  return {
    bundle,
    errors: [],
    plan: {
      schema: "identity.studio-plan/v1",
      projectId: model.projectId,
      sourceDigest: model.release.sourceDigest,
      profiles,
      status: "requires-human-approval",
      decisions: candidates.map((candidate) => ({
        id: candidate.id,
        kind: candidate.kind,
        state: candidate.state,
        action: candidate.state === "candidate" ? "stage-for-compiler-review" : "preserve-review-history",
      })),
      writes: candidates
        .filter((candidate) => candidate.state === "candidate")
        .map((candidate) => ({
          id: candidate.id,
          kind: candidate.kind,
          action: "stage-for-compiler-review",
        })),
      warnings: [
        "No canonical .identity/ or generated asset files have been changed.",
        "Applying this review record requires the compiler and a separate explicit approval step.",
      ],
    },
  };
}

export function createApprovedHandoff(plan, reviewer) {
  if (!plan || plan.status !== "requires-human-approval") {
    throw new Error("A reviewable plan is required.");
  }
  if (!Array.isArray(plan.writes) || plan.writes.length === 0) {
    throw new Error("At least one current candidate is required for compiler handoff.");
  }
  if (!reviewer?.trim()) throw new Error("Reviewer identity is required.");
  return {
    ...plan,
    status: "approved-for-compiler-handoff",
    approval: {
      reviewer: reviewer.trim(),
      method: "explicit-local-studio",
    },
  };
}

function normalizeProfiles(value, errors) {
  if (!Array.isArray(value) || value.length === 0) {
    errors.push("Candidate bundle must select at least one deterministic output profile.");
    return [];
  }
  const profiles = [...new Set(value)];
  if (profiles.length !== value.length) {
    errors.push("Candidate bundle output profiles must not contain duplicates.");
  }
  for (const profile of profiles) {
    if (!supportedOutputProfiles.has(profile)) {
      errors.push(`Unsupported deterministic output profile: ${profile}.`);
    }
  }
  return profiles.sort();
}

function normalizeCandidates(value, model, errors) {
  if (!Array.isArray(value) || value.length === 0) {
    errors.push("Candidate bundle must declare at least one candidate.");
    return [];
  }

  const candidateIds = new Set();
  const candidateAssetIds = new Set((model.assets || []).map((asset) => asset.id));
  return value.map((candidate) => {
    if (!candidate || typeof candidate !== "object") {
      errors.push("Every candidate must be a JSON object.");
      return {};
    }
    if (!candidate.id || !candidate.kind || !candidate.provenance) {
      errors.push("Every candidate requires id, kind, and provenance.");
    }
    if (!candidateStates.has(candidate.state)) {
      errors.push(`Candidate ${candidate.id || "(unknown)"} must use a supported review state.`);
    }
    if (candidateIds.has(candidate.id)) {
      errors.push(`Candidate id ${candidate.id} is duplicated.`);
    }
    candidateIds.add(candidate.id);
    if (candidate.approvedAssetId && !candidateAssetIds.has(candidate.approvedAssetId)) {
      errors.push(`Candidate ${candidate.id} references an unavailable approved asset.`);
    }
    if (candidate.preview && !isLocalImagePreview(candidate.preview)) {
      errors.push(`Candidate ${candidate.id} preview must be a local image data URL.`);
    }
    return {
      id: candidate.id,
      kind: candidate.kind,
      state: candidate.state,
      provenance: candidate.provenance,
      ...(candidate.approvedAssetId ? { approvedAssetId: candidate.approvedAssetId } : {}),
      ...(candidate.preview ? { preview: { dataUrl: candidate.preview.dataUrl } } : {}),
    };
  });
}

function isLocalImagePreview(preview) {
  return Boolean(
    preview
      && typeof preview === "object"
      && typeof preview.dataUrl === "string"
      && /^data:image\/(?:png|jpeg|webp|svg\+xml);/u.test(preview.dataUrl),
  );
}
