# Component Specifications — TI Design System v2.1 (§8)

Confirmed values from the living style guide. The style guide defines **69 named components**; this file captures the key ones with exact values. For web, the living style guide at `web-develop.theinstitutes.org/themes/ti_west/public/style-guide/` is authoritative — resolve any discrepancy in its favor.

All component CSS references the tokens in `tokens.scss` / `tokens.css` / `tokens.json`. **No hardcoded hex.**

---

## Buttons (§8.1)

Base: Montserrat Bold · 14px · **UPPERCASE** · letter-spacing 1px · min-width 150px · border-radius 4px (`--radius-sm`). Icon variant `.btn--icon` = inline SVG with 5px left margin.

| Class | Variant | Specification |
|-------|---------|---------------|
| `.btn--primary` | Primary | Solid navy (`--brand-primary-blue`) fill; white text; slides to white background on hover |
| `.btn--secondary` | Secondary | Transparent bg; `--brand-primary-blue` border and text |
| `.btn--secondary--light` | Secondary Light | White border + text; **dark/navy backgrounds only** — never on white |
| `.btn--text` | Text Button | No border/padding; underline; uppercase; tertiary actions only |

Rules: Labels sentence case, ≤4 words (except established uppercase patterns like `ADD TO CART`). Buttons act; links navigate — never use a button for navigation. **All five states required:** default, hover, focus (2px outline), active, disabled (40% opacity).

## Cards (§8.2)

Base: shadow `0 2px 24px 0 rgba(0,0,0,0.15)` (`--shadow-standard`) · background `--white` · **border-radius 0 (square — intentional, do not round)** · flex column.

**Course / Product card anatomy (top→bottom):**
1. Image area 16:9 — or `--accent-lavender (#e1ecf5)` / `--accent-blue-tint (#d0e6e9)` placeholder background
2. Category label: 14px, uppercase, letter-spacing 1px, weight 700, color `--accent-orange-dark (#a63b00)`
3. Title: Georgia/Merriweather serif, 20px
4. Description: Open Sans, 14px, `--brand-text-gray`, line-height 1.6, 3-line clamp
5. Metadata row: flat icon variants + text
6. CTA: `.btn--primary`, full card width

Card types: Article · Basic · Designation · Designation AIS · Designation (Courses) · Designation (Prepaid) · Essentials · Event · Filter · Headshot · Hubspot · Listing · Role · Seminar · Step · Topic Course · YMABII · Modal.

## Navigation (§8.3)

**Global header:** logo left-aligned 24px from edge; horizontal primary nav at desktop, hamburger below 768px; utility icons (cart, account, search) right-aligned; sticky/fixed at top.

**Mega menu:** white bg; up to 4 columns; category headings Montserrat Bold uppercase small; featured slot in right column (thumb + description + CTA); top border 3px solid `--brand-primary-blue`; dismiss on click-outside / Escape / explicit close.

**Mobile menu:** full-screen overlay; `--brand-primary-blue` bg; white text; drawer expand/collapse via chevron-right, back via chevron-left; **touch target ≥44px** per item.

**Tabs:** active = Montserrat Bold 14px uppercase 1px letter-spacing `--brand-primary-blue` + bottom border 3px solid `--brand-primary-blue`; inactive = same size, `#5c6f7c`, no border; padding 12px 24px; container bottom border 3px solid `--brand-primary-blue`.

## Forms (§8.4)

**Text input:** border 1px solid `--neutral (#cdcdcd)` at rest; padding 10px 12px; Open Sans 14px; focus = border `--brand-primary-blue` 2px; error = border `#8b2025` + message below in Alert Red.

**Labels:** Montserrat Bold or Open Sans Bold; 12px; uppercase; letter-spacing 1px; color `--brand-text-gray`; **always above the field — never placeholder-only.**

**Select/dropdown:** same visual treatment as text input; custom-styled — never browser-default appearance.

## Accordion (§8.5)

Item border 1px solid `--neutral`; 24px margin between items; header padding 16px 24px; header font Montserrat Bold; toggle `+`/`−` (or chevron-down rotating 180°); expanded header bg `--accent-blue-tint (#d0e6e9)`; panel content 16px 24px, Open Sans 14px, line-height 1.6.

## Alerts & Notifications (§8.6)

Padding 12px 24px · 14px · weight 700 · icon from the TI icon set alongside the message.

| Type | Background | Text |
|------|-----------|------|
| Info | `--alert-blue (#007db8)` | White |
| Error | `--alert-red (#8b2025)` | White |
| Warning | `--accent-yellow (#faa634)` | Dark |
| Success | `--accent-green (#6c7d45)` | White |

## Modals (§8.7)

Overlay `rgba(0,0,0,0.75)` · container white, border-radius 4px, padding 32px, max-width 400px (900px for video) · shadow `--shadow-standard` · title Montserrat 20px · body Open Sans 14px `--brand-text-gray` · dismiss on overlay click / Escape / close button · **focus trap required** (keyboard must not escape while open).

## Badges (§8.8)

Inline-block · uppercase · letter-spacing 1px · 12–14px · border-radius 4px · background determined by content from the confirmed palette.

## Tables (§8.9)

Cell padding 10px 16px · row border 1px solid `--neutral-light (#eaeaea)` · even rows `--neutral-xlight (#f2f2f2)` · header `--brand-primary-blue` bg, white text · Open Sans 14px · responsive = horizontal scroll within a container at mobile (never squash columns).

## Tooltip (§8.10)

Trigger = dashed underline `--brand-primary-blue` on the hover target · bg `--neutral-dark (#232323)` · white 12px · border-radius 4px · padding 8px 12px · positioned above trigger, 8px offset.

## Progress indicators (§8.11)

Track `--neutral (#cdcdcd)` · fill `--brand-primary-blue` · height 8px · border-radius 9999px · always with a visible text label. Step indicators: filled = complete, outlined = current, gray = future.

## Pagination (§8.12)

Active page `--brand-primary-blue` bg + white text + weight 700 · other pages `--brand-primary-blue` text links · Previous/Next `«` `»` in `--brand-secondary-gray (#5c6f7c)` · padding 8px 12px · 14px.

---

## Iconography (§6)

Custom SVG sprite; full vocabulary in the living style guide. **Icon names are fixed — do not create new icons without governance approval, and never recreate icons as standalone SVG/PNG.** Default 24×24px; small 16px (use `-flat` variants); large 32px for feature callouts. Every icon needs a visible label or `aria-label`. Color inherits from surrounding text unless overridden. `-gray` variants = disabled/inactive only.
