# Platform Implementation Guides — TI Design System v2.1 (§12)

Inject the relevant section for the task at hand. Each platform has its own rules and (for non-web) its own named-color mapping.

---

## 12.1 Web — SCSS / CSS

The living style guide is authoritative for web. SCSS variables (`tokens.scss`) are the source; CSS custom properties (`tokens.css`) map to them. **Component CSS references variables — any new CSS with a hardcoded color value requires review.** The `prefers-reduced-motion` block is required. Breakpoints: 768px and 1100px. Max content width 1280px, centered. 12-col grid desktop / 2-col tablet / 1-col mobile; gutters 24px desktop, 16px tablet & below.

## 12.2 PowerPoint / Presentations

All presentations use the official template at `[SHARED DRIVE PATH — POPULATE]`. **AI drafts content and structure only; a human transfers it into the official template. AI-generated layout is never an acceptable final deliverable.** PowerPoint has no web fonts — fall back to **Arial** for Montserrat/Open Sans and **Georgia** for Merriweather.

Named colors: TI Navy `#003370` · TI Orange `#c05810` · TI Orange Dark `#a63b00` · TI Gray `#5c6f7c` · TI Text Gray `#58595b` · TI Purple `#650360` · TI Blue Light `#72ccd2` · TI Neutral `#cdcdcd`.

Type: Cover title 40pt white · Cover subtitle 20pt white/80% · Section divider 36pt white · Slide title 28pt `#003370` · Body 18pt `#58595b` · Caption 12pt `#5c6f7c`.

Slide rules: **one idea per slide**; **max 5 bullets**; **min 18pt body** (viewed at distance); alt text on every image (Format Picture → Alt Text); logo bottom-right on every content slide; slide numbers on every content slide except cover/end; no clip art; TI icon set only.

## 12.3 Webinars & Video

Open with the standard title card (template `[SHARED DRIVE PATH — POPULATE]`). Required: TI logo · title · speaker name + credentials · date + CE credit info · approved background (confirmed gradient or brand color). Lower-third: `#003370` at 90% opacity bg; speaker name white bold (Open Sans/Arial); title + credentials white regular; small right-aligned TI logo. Post-production: trim dead air; intro/outro use the same title card; **captions required and reviewed for accuracy before publishing**; CE credit count, state approvals, and credit type confirmed by the CEU team before airing.

## 12.4 Assessments & LMS

Apply the palette wherever the platform allows; nav components (prev/next, progress) match §8; all instructional text uses line-height 1.86.

**Exam environment:** question stem Open Sans 16px `#58595b` lh 1.86; answer choices Open Sans 16px with custom radio styling; selected answer `#003370` left-border highlight; timer = icon + countdown, `#faa634` below 5 min and `#8b2025` below 1 min; **no decorative imagery on question pages**. Pass = completed-ribbon icon, `#6c7d45`, congratulatory voice. Fail = supportive message in `#58595b` (not red) with clear next steps.

**Third-party LMS (when full CSS is unavailable), priority order:** (1) logo presence, (2) brand colors via theme settings, (3) typography via CSS injection if permitted, (4) component styling to max extent. Document all exceptions with PM + Design System Owner sign-off.

## 12.5 Email

Single-column, 600px wide, centered. Header: TI logo, white on `#003370`. Footer: physical address · unsubscribe (legally required) · social icons · copyright.

Type: body Arial/Helvetica/sans-serif (web fonts can't be guaranteed); min body 14px; min footer legal 10px; line-height 1.6.

Rules: alt text on all images (clients block by default); **CTA buttons are coded HTML/CSS, not images** (an image button vanishes when images are blocked); **one primary CTA**; unsubscribe always present and functional (CAN-SPAM / CASL); test at 375px before 600px; all color pairings pass WCAG AA.

---

## Sub-brands (§13)

TIKG is the parent. A sub-brand mark leads its own relationship; the parent appears at reduced scale in the footer with a connector phrase ("Part of The Institutes Knowledge Group"). **Agent Broker** inherits all tokens. **CEU** inherits all tokens; tone is more transactional; **CEU Unlimited uses Green accent `#6c7d45` as its primary identifier — keep this consistent.** Out of scope for v2.1: RIG, ClaimsPages, IAUM, InsureMyPath, global.theinstitutes.org — do not over-apply this standard to them.

## Imagery (§9)

Works: professionals in real work contexts, authentic expressions, diverse representation, insurance/risk contexts, aspirational. Avoid: cliché stock (handshakes, lightbulbs, puzzle pieces), non-diverse casts, overly posed shots, images with no plausible insurance context. **AI image generation is NOT an approved source for TIKG visual assets** (§2). Formats: WebP + JPEG fallback, PNG for transparency; descriptive alt text (not "image of"); lazy-load below the fold; responsive `srcset` (mobile + desktop minimum).
