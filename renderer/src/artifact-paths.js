// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

/**
 * Artifact paths are bundle-relative URL paths, never deployment bases. Decode
 * each segment once to reject encoded traversal/separators, then serialize it
 * canonically. A decoded percent sign is forbidden to avoid nested encoding.
 */
export function normalizeArtifactPath(value, label = "Artifact path") {
  const fail = () => {
    throw new TypeError(`${label} must be a non-empty bundle-relative path without traversal, URLs, or encoded separators.`);
  };
  if (typeof value !== "string" || value.length === 0) {
    return fail();
  }
  const relative = value.startsWith("./") ? value.slice(2) : value;
  try {
    return relative.split("/").map((segment) => {
      const decoded = decodeURIComponent(segment);
      if (
        decoded.length === 0 || decoded === "." || decoded === ".."
        || /[\\/%:?#\u0000-\u001f\u007f]/u.test(decoded)
      ) {
        return fail();
      }
      return encodeURIComponent(decoded);
    }).join("/");
  } catch (error) {
    if (error instanceof URIError) {
      return fail();
    }
    throw error;
  }
}

export function normalizeArtifactDirectory(value, label = "Artifact directory") {
  const directory = typeof value === "string" && value.endsWith("/")
    ? value.slice(0, -1)
    : value;
  return `${normalizeArtifactPath(directory, label)}/`;
}

/** Explicit renderer configuration may select a local or HTTP(S) directory. */
export function normalizeAssetBaseUrl(value = "./") {
  if (value === "") {
    return "./";
  }
  const fail = () => {
    throw new TypeError("Asset base URL must be a local or HTTP(S) directory without credentials, query, fragment, backslashes, or control characters.");
  };
  if (
    typeof value !== "string" || /[\\?#\u0000-\u0020\u007f]/u.test(value)
    || value.startsWith("//")
  ) {
    return fail();
  }
  let base = value;
  if (/^https?:\/\//iu.test(value)) {
    let url;
    try {
      url = new URL(value);
    } catch {
      return fail();
    }
    if (!url.hostname || url.username || url.password || url.search || url.hash) {
      return fail();
    }
    base = url.toString();
  } else if (value.includes(":")) {
    return fail();
  }
  return base.endsWith("/") ? base : `${base}/`;
}
