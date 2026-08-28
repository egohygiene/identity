// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import path from "node:path";
import { fileURLToPath } from "node:url";

import { defineConfig } from "vite";

const rendererRoot = path.dirname(fileURLToPath(import.meta.url));
const publicDirectory = process.env.IDENTITY_RENDERER_PUBLIC_DIR
  ? path.resolve(rendererRoot, process.env.IDENTITY_RENDERER_PUBLIC_DIR)
  : path.resolve(rendererRoot, "../assets/identity");

export default defineConfig({
  base: process.env.IDENTITY_RENDERER_BASE || "./",
  publicDir: publicDirectory,
  build: {
    outDir: "dist",
    emptyOutDir: true,
    assetsInlineLimit: 0,
    sourcemap: false,
  },
  preview: {
    host: "127.0.0.1",
    port: 4173,
    strictPort: true,
  },
  test: {
    environment: "node",
    include: ["tests/**/*.test.js"],
    passWithNoTests: false,
  },
});
