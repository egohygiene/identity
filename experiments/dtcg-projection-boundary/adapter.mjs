import { readFile, writeFile } from "node:fs/promises";
import { pathToFileURL } from "node:url";

function isToken(value) {
  return value !== null && typeof value === "object" && "$value" in value;
}

function collectTokens(node, path = [], inheritedType = undefined, tokens = new Map()) {
  const groupType = node.$type ?? inheritedType;

  for (const key of Object.keys(node).filter((name) => !name.startsWith("$")).sort()) {
    const value = node[key];
    if (value === null || typeof value !== "object" || Array.isArray(value)) {
      throw new Error(`Expected an object at ${[...path, key].join(".")}`);
    }

    const tokenPath = [...path, key];
    if (isToken(value)) {
      const type = value.$type ?? groupType;
      if (type === undefined) {
        throw new Error(`Missing $type for ${tokenPath.join(".")}`);
      }
      tokens.set(tokenPath.join("."), { path: tokenPath, type, value: value.$value });
      continue;
    }

    collectTokens(value, tokenPath, value.$type ?? groupType, tokens);
  }

  return tokens;
}

function resolveToken(name, tokens, active = new Set()) {
  const token = tokens.get(name);
  if (token === undefined) {
    throw new Error(`Unknown token reference: ${name}`);
  }
  if (active.has(name)) {
    throw new Error(`Circular token reference: ${[...active, name].join(" -> ")}`);
  }

  if (typeof token.value === "string") {
    const match = token.value.match(/^\{([^{}]+)\}$/);
    if (match !== null) {
      const next = new Set(active);
      next.add(name);
      const resolved = resolveToken(match[1], tokens, next);
      if (resolved.type !== token.type) {
        throw new Error(`Type mismatch: ${name} (${token.type}) -> ${match[1]} (${resolved.type})`);
      }
      return { ...resolved, path: token.path };
    }
  }

  return token;
}

function formatValue(token) {
  if (token.type === "color") {
    if (
      token.value === null ||
      typeof token.value !== "object" ||
      token.value.colorSpace !== "srgb" ||
      typeof token.value.hex !== "string"
    ) {
      throw new Error(`Unsupported color value for ${token.path.join(".")}`);
    }
    return token.value.hex.toLowerCase();
  }

  if (token.type === "dimension") {
    if (
      token.value === null ||
      typeof token.value !== "object" ||
      typeof token.value.value !== "number" ||
      !["px", "rem"].includes(token.value.unit)
    ) {
      throw new Error(`Unsupported dimension value for ${token.path.join(".")}`);
    }
    return `${token.value.value}${token.value.unit}`;
  }

  throw new Error(`Unsupported token type: ${token.type}`);
}

function cssName(path) {
  return path
    .map((segment) => segment.replace(/([a-z0-9])([A-Z])/g, "$1-$2").toLowerCase())
    .join("-");
}

export function projectDtcgToCss(document) {
  const tokens = collectTokens(document);
  const declarations = [...tokens.keys()]
    .sort()
    .map((name) => {
      const token = resolveToken(name, tokens);
      return `  --${cssName(token.path)}: ${formatValue(token)};`;
    });

  return [":root {", ...declarations, "}", ""].join("\n");
}

export async function projectFile(inputPath, outputPath) {
  const source = await readFile(inputPath, "utf8");
  const document = JSON.parse(source);
  await writeFile(outputPath, projectDtcgToCss(document), "utf8");
}

if (process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const [inputPath, outputPath] = process.argv.slice(2);
  if (inputPath === undefined || outputPath === undefined) {
    throw new Error("Usage: node adapter.mjs <tokens.dtcg.json> <output.css>");
  }
  await projectFile(inputPath, outputPath);
}

