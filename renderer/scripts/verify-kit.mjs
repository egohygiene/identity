// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

import { parseArguments, verifyKit } from "../lib/kit-bundle.mjs";

const args = parseArguments(process.argv.slice(2), ["output-directory"]);
if (!args["output-directory"]) throw new Error("--output-directory is required.");
const receipt = await verifyKit(args["output-directory"]);
process.stdout.write(`Verified consumer Brand Kit: ${receipt.projectId} (${receipt.release.immutableId})\n`);
