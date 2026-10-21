// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { createHash } from "node:crypto";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";

import { afterEach, describe, expect, test } from "vitest";

import { artifactPathFromUrl, verifyArtifactDownloads } from "../src/download-integrity.js";

const temporaryDirectories = [];
const digest = (bytes) => createHash("sha256").update(bytes).digest("hex");

afterEach(async () => {
  await Promise.all(temporaryDirectories.splice(0).map((directory) => fs.rm(directory, { recursive: true, force: true })));
});

async function fixture() {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "identity-download-integrity-"));
  temporaryDirectories.push(root);
  const files = new Map();
  const write = async (name, value) => {
    const bytes = Buffer.from(value);
    await fs.mkdir(path.dirname(path.join(root, name)), { recursive: true });
    await fs.writeFile(path.join(root, name), bytes);
    files.set(name, bytes);
  };
  await write("brand/source.svg", "<svg xmlns=\"http://www.w3.org/2000/svg\"/>");
  await write("web/icon.png", Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]));
  await write("web/site.webmanifest", JSON.stringify({ icons: [{ src: "icon.png", type: "image/png" }] }));
  await write("packages/kit.zip", "downloadable package bytes");
  const model = {
    projectId: "test-project",
    release: { version: "1.0.0", sourceDigest: "a".repeat(64) },
    assets: [{ id: "source", downloadPath: "brand/source.svg", sha256: digest(files.get("brand/source.svg")) }],
    packages: [{ path: "packages/kit.zip" }],
    downloads: [{ path: "web/icon.png", sourceSha256: digest(files.get("brand/source.svg")) }],
  };
  const compilerManifest = async () => {
    await write("packages/renderer/brand-kit.view-model.json", JSON.stringify(model));
    const manifest = {
      schema: "identity.compiler-manifest/v1", projectId: model.projectId, sourceDigest: model.release.sourceDigest,
      outputs: [...files].map(([name, bytes]) => ({
        targetId: name === "packages/renderer/brand-kit.view-model.json" ? "reference-renderer-view-model" : name,
        path: `custom/output/${name}`, sha256: digest(bytes), bytes: bytes.length,
      })),
    };
    const manifestPath = path.join(root, ".identity-manifest.json");
    await fs.writeFile(manifestPath, JSON.stringify(manifest));
    return { manifest, manifestPath };
  };
  return { root, model, write, files, compilerManifest };
}

describe("advertised artifact integrity", () => {
  test("verifies source bytes, derivative bytes, packages, and optional browser references against selected compiler output", async () => {
    const { root, model, compilerManifest } = await fixture();
    const { manifestPath } = await compilerManifest();
    const result = await verifyArtifactDownloads({ ...model, designSystem: { artifacts: [] } }, {
      artifactRoot: root, manifestPath, browserAssets: { icon: "web/icon.png", manifest: "web/site.webmanifest" },
    });
    expect(result.verifiedPaths).toContain("web/icon.png");
    expect(model.downloads[0].sourceSha256).not.toBe(digest(await fs.readFile(path.join(root, "web/icon.png"))));
  });

  test("permits omitted browser artifacts and root-only source verification", async () => {
    const { root, model } = await fixture();
    await expect(verifyArtifactDownloads(model, { artifactRoot: root })).resolves.toBeDefined();
  });

  test.each(["missing", "empty", "source-checksum"])("rejects %s advertised bytes", async (failure) => {
    const { root, model, write } = await fixture();
    if (failure === "missing") await fs.rm(path.join(root, "web/icon.png"));
    if (failure === "empty") await write("web/icon.png", "");
    if (failure === "source-checksum") await write("brand/source.svg", "changed source");
    await expect(verifyArtifactDownloads(model, { artifactRoot: root })).rejects.toThrow(/missing|non-empty|checksum/u);
  });

  test.each(["../private.txt", "%2e%2e/private.txt", "web/%2fprivate.png", "/private.txt", "https://example.com/file.png"])(
    "rejects unsafe path %s", async (unsafe) => {
      const { root, model } = await fixture();
      model.downloads[0].path = unsafe;
      await expect(verifyArtifactDownloads(model, { artifactRoot: root })).rejects.toThrow(/bundle-relative/u);
    },
  );

  test("rejects a symlink resolving outside the supplied root", async () => {
    const { root, model } = await fixture();
    const outside = await fs.mkdtemp(path.join(os.tmpdir(), "identity-outside-"));
    temporaryDirectories.push(outside);
    await fs.writeFile(path.join(outside, "private.png"), "private bytes");
    await fs.rm(path.join(root, "web/icon.png"));
    await fs.symlink(path.join(outside, "private.png"), path.join(root, "web/icon.png"));
    await expect(verifyArtifactDownloads(model, { artifactRoot: root })).rejects.toThrow(/outside its root/u);
  });

  test.each(["source-digest", "project", "file-checksum", "size"])("rejects mismatched compiler %s evidence", async (failure) => {
    const { root, model, compilerManifest } = await fixture();
    const { manifest, manifestPath } = await compilerManifest();
    if (failure === "source-digest") manifest.sourceDigest = "b".repeat(64);
    if (failure === "project") manifest.projectId = "another-project";
    if (failure === "file-checksum") manifest.outputs[1].sha256 = "b".repeat(64);
    if (failure === "size") manifest.outputs[1].bytes += 1;
    await fs.writeFile(manifestPath, JSON.stringify(manifest));
    await expect(verifyArtifactDownloads(model, { artifactRoot: root, manifestPath })).rejects.toThrow(/digest|project|checksum\/size/u);
  });

  test("binds model content to the verified renderer JSON, including release and advertised downloads", async () => {
    const { root, model, write, compilerManifest } = await fixture();
    const { manifestPath } = await compilerManifest();
    await write("private.txt", "must not be exposed by altering the renderer model");
    for (const changed of [
      { ...model, release: { ...model.release, version: "2.0.0" } },
      { ...model, packages: [...model.packages, { path: "private.txt" }] },
      { ...model, assets: [] },
    ]) {
      await expect(verifyArtifactDownloads(changed, { artifactRoot: root, manifestPath })).rejects.toThrow(/selected output/u);
    }
  });

  test.each(["missing", "unlisted", "unsafe"])("rejects %s browser-manifest icon references", async (failure) => {
    const { root, model, write, compilerManifest } = await fixture();
    if (failure === "unsafe") await write("web/site.webmanifest", JSON.stringify({ icons: [{ src: "../private.png" }] }));
    const { manifestPath } = await compilerManifest();
    if (failure === "missing") await fs.rm(path.join(root, "web/icon.png"));
    if (failure === "unlisted") {
      await write("web/extra.png", "unlisted browser icon");
      await write("web/site.webmanifest", JSON.stringify({ icons: [{ src: "extra.png" }] }));
      const manifest = JSON.parse(await fs.readFile(manifestPath, "utf8"));
      const entry = manifest.outputs.find((output) => output.path.endsWith("site.webmanifest"));
      entry.sha256 = digest(await fs.readFile(path.join(root, "web/site.webmanifest")));
      entry.bytes = (await fs.stat(path.join(root, "web/site.webmanifest"))).size;
      await fs.writeFile(manifestPath, JSON.stringify(manifest));
    }
    await expect(verifyArtifactDownloads(model, {
      artifactRoot: root, manifestPath, browserAssets: { manifest: "web/site.webmanifest" },
    })).rejects.toThrow(/missing|absent|bundle-relative/u);
  });
});

describe("public release manifests", () => {
  async function publicFixture() {
    const context = await fixture();
    const { root, model, files, write } = context;
    const archiveName = "identity-brand-kit-v1.0.0.zip";
    await write(`packages/${archiveName}`, "public archive bytes");
    const manifest = {
      schema: "identity.public-brand-kit-manifest/v1", sourceDigest: model.release.sourceDigest,
      release: { tag: "v1.0.0" },
      archive: { path: archiveName, sha256: digest(files.get(`packages/${archiveName}`)), sizeBytes: files.get(`packages/${archiveName}`).length },
      files: [...files].filter(([name]) => !name.startsWith("packages/")).map(([name, bytes]) => ({ path: name, sha256: digest(bytes), sizeBytes: bytes.length })),
    };
    const manifestName = "identity-brand-kit-v1.0.0.manifest.json";
    await write(`packages/${manifestName}`, JSON.stringify(manifest));
    await write("packages/identity-brand-kit-v1.0.0.SHA256SUMS", `${manifest.archive.sha256}  ${archiveName}\n${digest(files.get(`packages/${manifestName}`))}  ${manifestName}\n`);
    model.packages = [archiveName, manifestName, "identity-brand-kit-v1.0.0.SHA256SUMS"].map((name) => ({ path: `packages/${name}` }));
    return { ...context, manifest, manifestPath: path.join(root, "packages", manifestName) };
  }

  test("checks every release file plus archive/manifest/checksums and advertised browser paths", async () => {
    const { root, model, manifestPath } = await publicFixture();
    await expect(verifyArtifactDownloads(model, {
      artifactRoot: root, manifestPath, browserAssets: { manifest: "web/site.webmanifest" },
    })).resolves.toBeDefined();
    await fs.writeFile(path.join(root, "web/site.webmanifest"), "tampered unadvertised release metadata");
    await expect(verifyArtifactDownloads(model, { artifactRoot: root, manifestPath })).rejects.toThrow(/checksum\/size/u);
  });

  test("rejects another public release even when its source digest matches", async () => {
    const { root, model, manifestPath } = await publicFixture();
    model.release.version = "2.0.0";
    await expect(verifyArtifactDownloads(model, { artifactRoot: root, manifestPath })).rejects.toThrow(/release/u);
  });
});

test("maps local/subdirectory/CDN publication links to confined bundle paths without fetching", () => {
  for (const base of ["./", "/identity/", "https://cdn.example.com/releases/v1/"]) {
    expect(artifactPathFromUrl(`${base}web/icon.png`, base)).toBe("web/icon.png");
  }
  expect(() => artifactPathFromUrl("https://other.example.com/icon.png", "https://cdn.example.com/")).toThrow(/asset base/u);
  expect(() => artifactPathFromUrl("./%2e%2e/private.txt")).toThrow(/bundle-relative/u);
});
