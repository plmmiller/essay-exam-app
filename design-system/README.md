# TI Design System — Machine-Readable Reference Set

The single source of truth that every AI assistant (Claude Code, Cursor, Grok) and every workflow (code, content, slides, email, documents) draws from. Generated from **The Institutes Knowledge Group Digital Design System v2.1 (May 2026)**, scope **TIKG · Agent Broker · CEU**.

Authoritative web reference: `web-develop.theinstitutes.org/themes/ti_west/public/style-guide/`. Any discrepancy with the living style guide resolves in the style guide's favor for web; this reference set is reviewed for alignment within 30 days of a style-guide change.

## Files

| File | Use it for |
|------|-----------|
| `tokens.scss` | Web/app SCSS — the source of truth for color, type, spacing, shadow, radius, motion, breakpoints |
| `tokens.css` | Same tokens as CSS custom properties (non-SCSS consumers) |
| `tokens.json` | Portable token set for any tool/language; flags unconfirmed values with `confirm:false` |
| `components.md` | Component specs (§8) + iconography (§6) |
| `voice-and-content.md` | Voice, tone, and content rules (§10) — for copy, email, docs |
| `accessibility.md` | WCAG 2.1 AA requirements + testing (§11) |
| `platform-guides.md` | Web, PowerPoint, webinar, LMS/assessment, email, sub-brands, imagery (§9, §12, §13) |
| `qa-checklist.md` | The "checklist out" gate (§15) |
| `CONTEXT.md` | Condensed paste-ready block for tools without auto-loaded repo context (e.g. Grok) |

## How it's wired to the tools

One canonical block, three entry points, all pointing here:

- **Claude Code / Cowork** → the "Design system" section in the repo's `CLAUDE.md` (auto-read on session start).
- **Cursor** → `.cursor/rules/design-system.mdc` (auto-applied per workspace).
- **Grok** → `AGENTS.md` at repo root + `CONTEXT.md` here, pasted or set as a system/workspace prompt (Grok has no guaranteed auto-loaded repo file).

## The workflow

**Context in → generate → checklist out.** Before generating, the assistant loads the files relevant to the task. After generating, it runs the matching section of `qa-checklist.md` and reports pass/fail per item. AI-origin output is held to the same review bar as human work.

## Open items (from the source document)

- PowerPoint and webinar template paths are `[SHARED DRIVE PATH — POPULATE]` in the source — fill in when available.
- A few accent colors (Blue Alt, Green Alt, Green Dark, Lavender, Blue tint, Medium Dark) appear in the §4.1 tables without a confirmed SCSS variable name, and Blue Alt shows a `#19a1c9` vs `#1aa1c9` discrepancy between the accent table and Gradient Blue Light. These are marked `confirm:false` / TODO and should be reconciled against the living style guide.
- AI image generation is not an approved source for TIKG visual assets.

## Maintenance

When the design system version changes, update these files and the three tool entry points together. Keeping the version in the AI context matched to the current document is what keeps AI output on-brand.
