# AGENTS.md — Agent & contributor guide


<!-- ti-design-system -->
## Design system

All UI and content follows the **TI Design System v2.1** (TIKG/AB/CEU). Tokens only — never hardcoded hex/fonts/spacing (run `node design-system/lint.mjs` to check). Three typefaces (Merriweather/Montserrat/Open Sans). Cards are square-cornered with the standard shadow. WCAG 2.1 AA is mandatory. Purple is reserved for AI content. Full rules and exact values are in `design-system/` — start with `design-system/CONTEXT.md` for a paste-ready summary, or `design-system/README.md` for the index. Loop: **context in → generate → checklist out** (`design-system/qa-checklist.md`).

Per-tool entry: **Claude Code** reads `CLAUDE.md` (includes the Design system section). **Cursor** auto-loads `.cursor/rules/design-system.mdc`. **Grok** reads this `AGENTS.md` + `CLAUDE.md`; load `design-system/CONTEXT.md` before any UI/copy work.
<!-- /ti-design-system -->
