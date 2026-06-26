
<!-- status-md-discipline -->
## STATUS.md discipline (required)

Maintain `docs/planning/STATUS.md` as the single source of truth for completion state.
It is a burndown, not a plan. Rules:

1. One row per work item (reuse the plan's IDs, e.g. F-01..F-N), each marked:
   ✅ done · 🟡 partial · ⬜ not started · 🚫 blocked.
2. VERIFY, NEVER ASSUME. Before marking ✅ or 🟡, confirm against the actual code
   (read the source/tests/migrations or the PR) and cite evidence — a real path,
   test, or PR. If you can't verify it, it's ⬜. A plan saying "this was sprint 1"
   is NOT evidence it shipped.
3. Update STATUS.md in the SAME change as the work that lands. It must never lag the
   repo. Refresh the header (date + current git SHA) every update.
4. Keep an append-only Changelog (e.g. "F-03 ⬜→✅") and Decisions log.
5. When asked for status, read this file and give a grouped view: counts, current
   focus, what shipped recently, what's next, what's blocked.
6. Planning docs describe intent and sequence; STATUS.md tracks state. Don't merge them.
<!-- /status-md-discipline -->

<!-- ti-design-system -->
## Design system (TI Design System v2.1 — TIKG/AB/CEU)

This repo follows **The Institutes Knowledge Group Digital Design System v2.1**. The machine-readable reference set lives in **`./design-system/`** and is the source of truth for all visual and content decisions. Load the relevant file(s) before generating UI, copy, slides, or email; run `design-system/qa-checklist.md` against the output before it ships. **Context in → generate → checklist out.**

**Non-negotiables for any UI work:**

- **Tokens only — never hardcoded hex, fonts, spacing, shadow, radius, or motion values.** Import from `design-system/tokens.scss` (SCSS) or `design-system/tokens.css` (CSS custom properties). Any new CSS with a literal color requires review. Run `node design-system/lint.mjs` to check.
- **Three typefaces only:** Merriweather (H1/H3/H4), Montserrat (H2/H5, buttons, nav), Open Sans (body). Never add a fourth.
- **Cards:** `border-radius: 0` (square — intentional) + shadow `0 2px 24px 0 rgba(0,0,0,0.15)`.
- **Buttons:** Montserrat Bold, 14px, uppercase, letter-spacing 1px, min-width 150px, radius 4px; all five states (default, hover, focus 2px outline, active, disabled 40%).
- **Body text** is always `$brand-text-gray (#58595b)` — never a brand color. The **purple gradient / `$brand-secondary-purple` is reserved for AI-related content only.**
- **Breakpoints:** 768px (tablet) and 1100px (desktop). Max content width 1280px.
- **Accessibility: WCAG 2.1 AA is mandatory** — 4.5:1 body / 3:1 large+UI contrast; visible keyboard focus (never `outline:none` without replacement); semantic HTML; one H1; honor `prefers-reduced-motion`; icon-only controls need `aria-label`. Run axe/Lighthouse before accepting any generated component.
- **Voice & content:** see `design-system/voice-and-content.md` — sentence-case UI labels, designation trademark format (CPCU®, ARM™), descriptive links (never "click here"), confident not hedged.
- **AI image generation is NOT an approved source for TIKG visual assets.**

Authoritative web reference: `web-develop.theinstitutes.org/themes/ti_west/public/style-guide/` (wins over the local reference set for web specifics). Same `design-system/` set is mirrored to Cursor (`.cursor/rules/design-system.mdc`) and Grok (`AGENTS.md` + `design-system/CONTEXT.md`).
<!-- /ti-design-system -->
