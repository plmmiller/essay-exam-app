#!/usr/bin/env node
/**
 * TI Design System lint gate — dependency-free.
 *
 * Turns the QA checklist's machine-checkable rules into an actual gate.
 * Flags, in source files (not the token files themselves):
 *   R1 hardcoded-hex   — literal #hex colors. Use a token instead.
 *   R2 disallowed-font — font-family using anything outside the three approved
 *                        typefaces + permitted fallbacks.
 *   R3 outline-none    — outline:none / outline:0 without a focus replacement
 *                        (keyboard-focus visibility is mandatory, WCAG 2.1 AA).
 *
 * Suppress a single line with a trailing `ds-allow` comment when there is a
 * documented, reviewed reason.
 *
 * Modes:
 *   (default)   report — prints findings, ALWAYS exits 0. Safe for existing repos.
 *   --strict    exits 1 if any violation is found (use once a repo's baseline is clean).
 *   --changed   only scan files changed vs origin/main (the doc's "new code" rule).
 *   --json      machine-readable output.
 *   [paths...]  limit the scan to specific files/dirs.
 *
 * Usage:  node design-system/lint.mjs [--strict] [--changed] [--json] [paths...]
 */
import { readFileSync, statSync, readdirSync } from "node:fs";
import { execSync } from "node:child_process";
import { join, extname, sep } from "node:path";

const args = process.argv.slice(2);
const STRICT = args.includes("--strict");
const CHANGED = args.includes("--changed");
const JSON_OUT = args.includes("--json");
const paths = args.filter((a) => !a.startsWith("--"));

const EXTS = new Set([".css", ".scss", ".sass", ".less", ".ts", ".tsx", ".js", ".jsx", ".vue", ".svelte", ".html", ".astro"]);
const SKIP_DIRS = new Set(["node_modules", ".next", ".git", "dist", "build", "coverage", ".vercel", ".turbo", "out", "design-system"]);
// Token definition files legitimately contain hex; never flag them.
const TOKEN_FILE = /(^|[\\/])tokens\.(scss|css|json|js|ts)$/i;

// Approved typefaces + permitted generic/system fallbacks (lowercased).
const APPROVED_FONTS = new Set([
  "merriweather", "montserrat", "open sans", "georgia", "arial", "helvetica",
  "helvetica neue", "segoe ui", "system-ui", "ui-sans-serif", "ui-serif",
  "-apple-system", "blinkmacsystemfont", "sans-serif", "serif", "monospace",
  "inherit", "initial", "unset", "var", // var(...) references pass through
]);

function listFiles(root) {
  const out = [];
  let st;
  try { st = statSync(root); } catch { return out; }
  if (st.isFile()) { if (EXTS.has(extname(root))) out.push(root); return out; }
  for (const name of readdirSync(root)) {
    if (SKIP_DIRS.has(name)) continue;
    const full = join(root, name);
    let s;
    try { s = statSync(full); } catch { continue; }
    if (s.isDirectory()) out.push(...listFiles(full));
    else if (EXTS.has(extname(full))) out.push(full);
  }
  return out;
}

function changedFiles() {
  try {
    const base = execSync("git merge-base origin/main HEAD 2>/dev/null || echo HEAD", { encoding: "utf8" }).trim();
    const diff = execSync(`git diff --name-only ${base} -- 2>/dev/null`, { encoding: "utf8" });
    return diff.split("\n").map((f) => f.trim()).filter(Boolean).filter((f) => EXTS.has(extname(f)));
  } catch {
    return null;
  }
}

const HEX = /#[0-9a-fA-F]{3,8}\b/g;
const FONT_FAMILY = /font-family\s*[:=]\s*([^;}\n]+)/gi;
const OUTLINE_NONE = /outline\s*:\s*(none|0)\b/i;

function scanFile(file) {
  const violations = [];
  let text;
  try { text = readFileSync(file, "utf8"); } catch { return violations; }
  if (TOKEN_FILE.test(file)) return violations;
  const lines = text.split("\n");
  lines.forEach((line, i) => {
    if (/ds-allow/.test(line)) return; // explicit, reviewed suppression
    const ln = i + 1;

    // R1 hardcoded hex
    const hex = line.match(HEX);
    if (hex) {
      for (const h of hex) violations.push({ rule: "hardcoded-hex", file, line: ln, snippet: h, hint: "use a design token (tokens.scss/.css/.json)" });
    }

    // R2 disallowed font-family
    let m;
    FONT_FAMILY.lastIndex = 0;
    while ((m = FONT_FAMILY.exec(line))) {
      const families = m[1].replace(/['"]/g, "").split(",").map((s) => s.trim().toLowerCase()).filter(Boolean);
      for (const fam of families) {
        if (fam.startsWith("var(") || fam.startsWith("$") || fam.startsWith("--")) continue;
        if (!APPROVED_FONTS.has(fam)) {
          violations.push({ rule: "disallowed-font", file, line: ln, snippet: fam, hint: "only Merriweather, Montserrat, Open Sans (+ approved fallbacks)" });
        }
      }
    }

    // R3 outline:none without replacement on the same line
    if (OUTLINE_NONE.test(line) && !/box-shadow|outline-offset|:focus-visible|border/i.test(line)) {
      violations.push({ rule: "outline-none", file, line: ln, snippet: line.trim().slice(0, 80), hint: "keep a visible focus indicator (WCAG 2.1 AA)" });
    }
  });
  return violations;
}

// --- collect target files ---
let files;
if (paths.length) files = paths.flatMap(listFiles);
else if (CHANGED) {
  const c = changedFiles();
  files = c === null ? listFiles(process.cwd()) : c;
} else files = listFiles(process.cwd());

const all = files.flatMap(scanFile);

if (JSON_OUT) {
  console.log(JSON.stringify({ violations: all, count: all.length, strict: STRICT }, null, 2));
} else {
  const byRule = all.reduce((acc, v) => ((acc[v.rule] ||= []).push(v), acc), {});
  const rel = (f) => f.replace(process.cwd() + sep, "");
  console.log("\nTI Design System lint");
  console.log("=".repeat(40));
  if (!all.length) {
    console.log("No violations found in", files.length, "file(s). On-brand. ✓\n");
  } else {
    for (const [rule, vs] of Object.entries(byRule)) {
      console.log(`\n[${rule}] — ${vs.length}`);
      for (const v of vs.slice(0, 200)) console.log(`  ${rel(v.file)}:${v.line}  ${v.snippet}   → ${v.hint}`);
      if (vs.length > 200) console.log(`  …and ${vs.length - 200} more`);
    }
    console.log(`\nTotal: ${all.length} violation(s) across ${new Set(all.map((v) => v.file)).size} file(s).`);
    console.log("Suppress a reviewed exception with a trailing `ds-allow` comment.\n");
  }
}

process.exit(STRICT && all.length ? 1 : 0);
