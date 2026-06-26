# Accessibility Standards — TI Design System v2.1 (§11)

**Minimum standard: WCAG 2.1 Level AA.** Not optional — ethical and increasingly legal. Applies to all digital properties under this standard.

## Color contrast

- Body text (below 18pt / 14pt bold): **≥ 4.5:1** against background.
- Large text and UI components: **≥ 3:1**.
- Confirmed: `#58595b` (Text Gray) on white = 5.9:1 (AA pass). `#003370` (Primary Blue) on white = 12.6:1 (AAA pass).
- **Color is never the only means of communicating information** — always pair with shape, label, or icon.

## Keyboard navigation

- All interactive elements reachable and operable by keyboard alone.
- Tab order matches visual reading order.
- Focus indicator always visible — **never `outline: none` without a replacement.**
- Skip-to-main-content link is the first focusable element on every page.

## Screen reader compatibility

- All images have meaningful alt text (`alt=""` for purely decorative images).
- All form inputs have associated labels.
- All icon-only buttons have an `aria-label`.
- Semantic HTML: `header`, `nav`, `main`, `section`, `footer`.
- Heading hierarchy is sequential — exactly one H1 per page; never skip levels.

## Motion

- All animations respect `prefers-reduced-motion` (transitions → ~0 duration).
- No content flashes more than 3 times per second.

## Testing requirements (do before launch)

- **Automated scan:** axe, Lighthouse, or WAVE against all key page templates.
- **Manual keyboard test:** complete the core flow (find designation → add to cart → checkout) by keyboard only.
- **Screen reader test:** NVDA on Windows and VoiceOver on macOS.
- **Contrast check:** verify all color pairings with a WCAG contrast tool.

## For AI-generated code (§2)

Run axe or Lighthouse before accepting any AI-generated component. Confirm tokens are used (not hardcoded hex) and that every interactive element has a visible keyboard focus state.
