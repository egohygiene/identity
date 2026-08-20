import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import test from "node:test";

import { projectDtcgToCss } from "./adapter.mjs";

const sourceUrl = new URL("./tokens.dtcg.json", import.meta.url);
const expectedUrl = new URL("./expected.css", import.meta.url);

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

test("projects canonical DTCG input deterministically without mutation", async () => {
  const sourceBefore = await readFile(sourceUrl);
  const expected = await readFile(expectedUrl, "utf8");
  const sourceDocument = JSON.parse(sourceBefore.toString("utf8"));

  const first = projectDtcgToCss(sourceDocument);
  const second = projectDtcgToCss(sourceDocument);
  const sourceAfter = await readFile(sourceUrl);

  assert.equal(first, expected);
  assert.equal(second, first);
  assert.equal(sha256(sourceAfter), sha256(sourceBefore));
});

test("sorts projection paths independently of source insertion order", async () => {
  const source = JSON.parse(await readFile(sourceUrl, "utf8"));
  const reversed = Object.fromEntries(Object.entries(source).reverse());

  assert.equal(projectDtcgToCss(reversed), projectDtcgToCss(source));
});

test("fails closed for unsupported token types", () => {
  assert.throws(
    () =>
      projectDtcgToCss({
        identity: {
          unsafe: {
            $type: "made-up-type",
            $value: "invented",
          },
        },
      }),
    /Unsupported token type/,
  );
});

