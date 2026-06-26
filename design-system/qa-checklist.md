# QA Checklist — TI Design System v2.1 (§15)

The "checklist out" half of the **context in, checklist out** loop. Run the relevant section against any AI- or human-produced output before it ships. AI generation speed does not change the review requirement — it raises its importance.

## Visual standards

- [ ] All colors from the confirmed palette — no hardcoded/arbitrary hex
- [ ] Typography uses Merriweather / Montserrat / Open Sans correctly per heading level
- [ ] Spacing uses the 16px base scale — no arbitrary values
- [ ] Logo in an approved variation with clear space respected
- [ ] Icons from the TI icon set only; icon-only elements have `aria-label`
- [ ] No unsanctioned colors, fonts, gradients, or decorative treatments
- [ ] Purple gradient used only for AI-related content

## Component standards

- [ ] Cards: square corners (border-radius 0); standard shadow `0 2px 24px 0 rgba(0,0,0,0.15)`
- [ ] Buttons: correct variant; all five states (default, hover, focus, active, disabled)
- [ ] Forms: labels above fields; required indicator; error state; visible focus ring
- [ ] Navigation: keyboard navigable; mobile-responsive; hamburger below 768px
- [ ] Modals: focus trapped; Escape dismisses; overlay click dismisses
- [ ] Tabs: active tab has 3px solid `#003370` bottom border

## Accessibility standards

- [ ] All images have meaningful alt text (`alt=""` for purely decorative)
- [ ] Contrast: 4.5:1 body text; 3:1 large text and UI
- [ ] Color is not the only means of communicating information
- [ ] Exactly one H1; heading hierarchy sequential
- [ ] All interactive elements keyboard-reachable with visible focus indicator
- [ ] `prefers-reduced-motion` respected
- [ ] Automated scan (axe or Lighthouse) shows no critical violations

## Content standards

- [ ] UI labels sentence case (H5/uppercase labels and designation names excepted)
- [ ] Designation names use correct trademark symbols
- [ ] Button labels action-verb-first, four words or fewer
- [ ] No "click here" link text — all links descriptive

## Platform-specific

**Web** — SCSS uses variables (no hardcoded hex) · responsive at 768px and 1100px · lazy-load below-fold images.

**Email** — images have alt text · CTA is a coded button, not an image · unsubscribe present and functional · tested at 375px and 600px.

**PowerPoint** — official template master used · named colors from confirmed palette · images have alt text in Format Picture.

**Assessment** — no decorative images on question pages · timer color states implemented · completion messages follow voice.

**Webinar** — title card at session open · lower-third templates applied · captions enabled and verified.
