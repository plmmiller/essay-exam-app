# TI Design System v2.1 — Condensed Context (paste-ready)

Paste this block (or set it as a system/workspace prompt) at the start of any session with a tool that does not auto-load repo context — e.g. Grok. For full detail, the complete reference set is in this `design-system/` folder.

---

You are generating output for **The Institutes Knowledge Group (TIKG / Agent Broker / CEU)**. Follow the TI Design System v2.1. Work the loop: **load the relevant standard → generate → self-check against the QA checklist and report pass/fail per item.**

## Design tokens (use these exact values; never hardcode others)

**Brand:** primary-blue `#003370` · primary-red `#980d22` · secondary-gray `#5c6f7c` · secondary-purple `#650360` (AI content ONLY) · text-gray `#58595b` (all body text).
**Accent:** blue-light `#72ccd2` · blue `#218198` · blue-dark `#042246` · orange `#c05810` · orange-dark `#a63b00` (H5/card labels) · yellow `#faa634` · red `#801129` · green `#6c7d45` (success; CEU Unlimited).
**Neutral:** `#f2f2f2` · `#eaeaea` · `#cdcdcd` · `#232323` · white `#ffffff`.
**Alert:** error `#8b2025` · info `#007db8` · warning `#faa634` · success `#6c7d45`.
**Gradients (only these):** orange `linear-gradient(90deg,#c05810 26%,#a63b00 100%)` · blue `linear-gradient(270deg,#007db8 26%,#003370 100%)` · blue-light `linear-gradient(270deg,#1aa1c9 -10%,#006385 100%)` · red `linear-gradient(270deg,#870e28 26%,#570f21 100%)` · purple `linear-gradient(270deg,#861e81 26%,#5d0158 100%)` (AI ONLY).

## Typography (three typefaces — never more)

Merriweather (H1/H3/H4) · Montserrat (H2/H5, buttons, nav) · Open Sans (body).
H1 38px/1.58 · H2 36px/1.5 · H3 30px/1.73 · H4 25px/1.48 · H5 12px/1.5 UPPERCASE ls 1px `#a63b00` · body 14px (prefer 16px)/1.86. Links `#003370`, underline, weight 700.

## Spacing / shadow / radius / motion

Spacing on 8px multiples (base 16px, 24px below blocks). Shadow standard `0 2px 24px 0 rgba(0,0,0,0.15)`, subtle `0 2px 8px rgba(0,0,0,0.06)`. Radius: cards 0 (square — intentional), 4px buttons/inputs/badges/modal, 9999px pills. Motion 100/200/350/500ms; always honor `prefers-reduced-motion`.

## Components (key rules)

**Buttons:** Montserrat Bold 14px uppercase, ls 1px, min-width 150px, radius 4px; five states (default/hover/focus 2px outline/active/disabled 40%); buttons act, links navigate. **Cards:** square corners, standard shadow, white bg, category label `#a63b00` uppercase, serif title, body `#58595b`. **Forms:** labels above field (never placeholder-only), input border `#cdcdcd` → focus `#003370` 2px, error `#8b2025`. **Modals:** overlay `rgba(0,0,0,0.75)`, focus trap, Escape + overlay-click dismiss. **Tabs:** active has 3px solid `#003370` bottom border.

## Accessibility (mandatory — WCAG 2.1 AA)

Contrast 4.5:1 body / 3:1 large+UI; color never the only signal; visible keyboard focus (never `outline:none` without replacement); semantic HTML; exactly one H1, sequential headings; `aria-label` on icon-only controls; alt text on images (`alt=""` if decorative). Run axe/Lighthouse before accepting any component.

## Voice & content

Authoritative, clear, confident, encouraging, precise. Sentence-case UI labels (designation names/H5 excepted). Designation trademark format: CPCU®, ARM™, AIAI™. Descriptive links — never "click here." Numbers: spell out under 10, numerals for 10+/measurements/UI/pricing. CTA action-verb-first, ≤4 words, one primary CTA. **AI-generated imagery is not an approved TIKG asset.**

Breakpoints 768px / 1100px; max content width 1280px. Authoritative web source: `web-develop.theinstitutes.org/themes/ti_west/public/style-guide/`.
