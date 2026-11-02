// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { createHash } from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

import { JSDOM } from "jsdom";

import { artifactPathFromUrl, verifyArtifactDownloads, verifyArtifactPaths } from "../src/download-integrity.js";
import { assertBrandKitViewModel } from "../src/model.js";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const rendererRoot = path.resolve(scriptDirectory, "..");
const argumentsMap = parseArguments(process.argv.slice(2));
const outputDirectory = path.resolve(
  rendererRoot,
  argumentsMap["output-directory"] || "dist",
);

await assertFile("CNAME");
await assertFile("index.html");
await assertFile("brand-kit/index.html");
await assertFile("site.json");

const site = await readJson("site.json");
const version = assertStableRelease(site.release.tag);
const packageDirectory = "packages";
const archiveName = `identity-brand-kit-v${version}.zip`;
const manifestName = `identity-brand-kit-v${version}.manifest.json`;
const checksumsName = `identity-brand-kit-v${version}.SHA256SUMS`;
await Promise.all([
  assertFile(`${packageDirectory}/${archiveName}`),
  assertFile(`${packageDirectory}/${manifestName}`),
  assertFile(`${packageDirectory}/${checksumsName}`),
  assertFile("brand/emblem.svg"),
  assertFile("brand/lockup-horizontal.svg"),
  assertFile("brand/social-preview.svg"),
  assertFile("brand/open-graph.svg"),
  assertFile("web/site.webmanifest"),
]);

const canonicalUrl = "https://identity.egohygiene.io/";
if (site.canonicalUrl !== canonicalUrl) {
  throw new Error(`Unexpected canonical URL: ${site.canonicalUrl}`);
}
if (!Array.isArray(site.aliases) || !site.aliases.includes("/brand-kit/")) {
  throw new Error("The public site must declare its /brand-kit/ compatibility route.");
}
if (!/^[0-9a-f]{64}$/u.test(site.sourceDigest)) {
  throw new Error("The public site must expose a SHA-256 source digest.");
}
if (!/^[0-9a-f]{64}$/u.test(site.publicationManifestSha256)) {
  throw new Error("The public site must expose a SHA-256 publication manifest checksum.");
}

const [index, redirect, manifest, checksums] = await Promise.all([
  readText("index.html"),
  readText("brand-kit/index.html"),
  readJson(`${packageDirectory}/${manifestName}`),
  readText(`${packageDirectory}/${checksumsName}`),
]);
for (const expected of [
  `<link rel="canonical" href="${canonicalUrl}"`,
  `<meta property="og:url" content="${canonicalUrl}"`,
  "application/ld+json",
  `Release ${version}`,
  site.sourceDigest,
  site.publicationManifestSha256,
]) {
  if (!index.includes(expected)) {
    throw new Error(`The rendered page is missing expected publication evidence: ${expected}`);
  }
}
if (
  !redirect.includes(`href="${canonicalUrl}"`)
  || !redirect.includes(`url=${canonicalUrl}`)
) {
  throw new Error("The /brand-kit/ compatibility route must redirect to the canonical URL.");
}
if (manifest.release.tag !== site.release.tag || manifest.release.commit !== site.release.commit) {
  throw new Error("The publication manifest and public site disagree about their release source.");
}
if (manifest.sourceDigest !== site.sourceDigest) {
  throw new Error("The publication manifest and public site disagree about source integrity.");
}
if (sha256(await fs.readFile(resolve(site.publicationManifest))) !== site.publicationManifestSha256) {
  throw new Error("The published manifest checksum does not match its manifest file.");
}

const expectedChecksums = new Map([
  [archiveName, manifest.archive.sha256],
  [manifestName, site.publicationManifestSha256],
]);
for (const line of checksums.trim().split("\n")) {
  const match = /^([0-9a-f]{64})  (.+)$/u.exec(line);
  if (!match) {
    throw new Error(`Malformed public checksum entry: ${line}`);
  }
  const [, digest, fileName] = match;
  if (expectedChecksums.get(fileName) !== digest) {
    throw new Error(`Unexpected public checksum entry: ${line}`);
  }
  expectedChecksums.delete(fileName);
}
if (expectedChecksums.size > 0) {
  throw new Error(`Missing public checksum entries: ${[...expectedChecksums.keys()].join(", ")}`);
}
if (sha256(await fs.readFile(resolve(`${packageDirectory}/${archiveName}`))) !== manifest.archive.sha256) {
  throw new Error("The public archive does not match the publication manifest checksum.");
}

const document = new JSDOM(index).window.document;
const modelElement = document.querySelector("#identity-brand-kit-model");
if (!modelElement) throw new Error("The published page must embed its selected renderer model.");
const model = assertBrandKitViewModel(JSON.parse(modelElement.textContent));
const assetBaseUrl = site.assetBaseUrl || "./";
const browserAssets = {};
for (const [key, relation] of [
  ["icon", "icon"], ["appleTouchIcon", "apple-touch-icon"], ["manifest", "manifest"],
]) {
  const links = [...document.querySelectorAll(`link[rel="${relation}"]`)];
  if (links.length > 1) throw new Error(`The published page repeats browser asset role: ${key}`);
  if (links.length) browserAssets[key] = artifactPathFromUrl(links[0].getAttribute("href"), assetBaseUrl);
  if (site.browserAssets?.[key] !== browserAssets[key]) {
    throw new Error(`The published browser asset disagrees with site configuration: ${key}`);
  }
}
const verified = await verifyArtifactDownloads(model, {
  artifactRoot: outputDirectory,
  manifestPath: resolve(`${packageDirectory}/${manifestName}`),
  browserAssets,
});
const emittedDownloads = [...document.querySelectorAll("a[download]")].map(
  (link) => artifactPathFromUrl(link.getAttribute("href"), assetBaseUrl),
);
for (const relativePath of emittedDownloads) {
  if (!verified.verifiedPaths.includes(relativePath)) {
    throw new Error(`The published page advertises a download absent from its selected model: ${relativePath}`);
  }
}
await verifyArtifactPaths(emittedDownloads, { artifactRoot: outputDirectory });

process.stdout.write(`Verified public Brand Kit site: ${outputDirectory}\n`);

function assertStableRelease(tag) {
  const match = /^v(\d+\.\d+\.\d+)$/u.exec(tag || "");
  if (!match) {
    throw new Error("The deployed Brand Kit must be tied to a stable semantic-version release.");
  }
  return match[1];
}

async function assertFile(relativePath) {
  await verifyArtifactPaths([relativePath], { artifactRoot: outputDirectory });
}

async function readJson(relativePath) {
  return JSON.parse(await readText(relativePath));
}

async function readText(relativePath) {
  return fs.readFile(resolve(relativePath), "utf8");
}

function resolve(relativePath) {
  const resolved = path.resolve(outputDirectory, relativePath);
  if (resolved !== outputDirectory && !resolved.startsWith(`${outputDirectory}${path.sep}`)) {
    throw new Error(`Public path escapes the output directory: ${relativePath}`);
  }
  return resolved;
}

function sha256(contents) {
  return createHash("sha256").update(contents).digest("hex");
}

function parseArguments(values) {
  const result = {};
  const argumentValues = values[0] === "--" ? values.slice(1) : values;
  for (let index = 0; index < argumentValues.length; index += 1) {
    const value = argumentValues[index];
    if (!value.startsWith("--")) {
      throw new Error(`Unexpected positional argument: ${value}`);
    }
    const key = value.slice(2);
    const next = argumentValues[index + 1];
    if (!next || next.startsWith("--")) {
      throw new Error(`Argument --${key} requires a value.`);
    }
    result[key] = next;
    index += 1;
  }
  return result;
}
