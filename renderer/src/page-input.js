// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { normalizeArtifactPath, normalizeAssetBaseUrl } from "./artifact-paths.js";
import { foundationTokens } from "./foundations.js";
import { selectedPresentationProfiles } from "./presentation.js";
import { SECTION_DEFINITIONS, assertBrandKitViewModel } from "./model.js";

export function resolvePageInputs({ model, assetBaseUrl, publication, publicOnly }) {
  assertBrandKitViewModel(model);
  assetBaseUrl = normalizeAssetBaseUrl(assetBaseUrl);
  if (publication) {
    normalizeArtifactPath(publication.manifestPath, "Publication manifest path");
  }
  const colorTokens = model.tokens.filter((token) => token.type === "color");
  const foundations = model.designSystem ? foundationTokens(model.designSystem) : null;
  const typographyTokens = model.tokens.filter(
    (token) =>
      token.type === "fontFamily" || token.path.startsWith("typography."),
  );
  const completeKit = model.packages.find((entry) =>
    ["brand-kit-archive", "complete-brand-kit"].includes(entry.id)
    && entry.mediaType === "application/zip",
  );
  const sections = SECTION_DEFINITIONS.filter(([id]) => {
    if (id === "design-system") return Boolean(model.designSystem);
    if (id === "press-kit") return Boolean(model.pressKit);
    if (id === "presentation") return selectedPresentationProfiles(model).length > 0;
    if (!publicOnly) return true;
    if (id === "studio") return false;
    if (["voice", "usage"].includes(id)) return model.guidance[id].status === "declared" && Boolean(model.guidance[id].value);
    if (id === "creative-direction") return Object.values(model.support).some((entry) => entry.status === "declared");
    if (id === "logos") return model.assets.length > 0;
    if (id === "colors") return colorTokens.length > 0;
    if (id === "typography") return typographyTokens.length > 0;
    if (id === "downloads") return model.packages.length > 0;
    return true;
  });
  return { assetBaseUrl, colorTokens, foundations, typographyTokens, completeKit, sections };
}
