# GOD SQUAD — PHASE 2 DESIGN SYSTEM & VISUAL LANGUAGE

**Project:** God Squad Premium Faith-Driven Streetwear
**Phase:** 2 — Design System
**Date:** 2026-09-21
**Target:** Shopify Online Store 2.0 theme (built in Phase 10, not here)
**Companion file:** `PHASE-2-DESIGN-TOKENS.css` — the canonical token implementation, 164 tokens, in the project root
**Predecessor:** `PHASE-1-WEBSITE-AUDIT.md` — 32 sections, 200 issues, delivered 2026-09-21

## How to use this document

This is a specification, not an implementation. It defines the vocabulary that Phases 3 to 16 build with. Nothing described here has been applied to the prototype: the existing website is untouched and remains the approved visual baseline.

Three rules govern everything that follows.

1. **Components reference semantic tokens, never raw palette values.** `--color-text-primary`, not `#F3EFE6`. The raw palette exists in one place so it can be re-pointed once.
2. **Surface context decides the accent and the focus ring.** Muted gold measures 1.55:1 on warm cream and 1.43:1 on the tile cream. It is a dark-surface accent only. The `.surface-dark` and `.surface-light` classes reassign `--accent-current` and `--focus-ring` so the correct value is inherited rather than remembered.
3. **Luxury through restraint.** When a decision is open, choose the quieter option: contrast and spacing before borders, borders before shadows, and no motion unless it serves comprehension.

Values marked **BUSINESS INFORMATION REQUIRED** are genuinely unknown. They are not placeholders to be filled with a plausible guess.


## 1. Design System Overview

### What this system is

The God Squad design system is a written contract between the prototype that exists today and the Shopify Online Store 2.0 theme that Phase 10 will build. It has two artifacts:

| Artifact | Status | Role |
|---|---|---|
| `PHASE-2-DESIGN-TOKENS.css` | Exists in the project root. Version 1.0.0, 2026-09-21 (line 3) | The canonical machine-readable layer. 162 custom properties declared in `:root`, plus `--color-border-current` and `--accent-current` introduced by the two surface classes — 164 in total |
| `PHASE-2-DESIGN-SYSTEM.md` | This document, 31 sections in the order spec §37 fixes | The human-readable layer: what each token means, where it may be used, and what may not be done with it |

The token file is a reference implementation. It is not wired into `God Squad Website.html` and modifies no existing file (token file lines 7–9). Phase 2 is DEFINE, STANDARDIZE, DOCUMENT, SYSTEMIZE, PREPARE (spec §7). Nothing in this document has been built.

Every value in the token file is one of three things (token file lines 12–16): taken from the prototype and cited by line number, normalised from it onto a scale with the original recorded, or derived and contrast-verified where the prototype had no value at all. Nothing is present for taste alone — with the two reconciliation items flagged in §30 (Groups 5 and 7).

### The objective and the seven qualities

The objective (spec §2) is a unified visual system covering colours, typography, spacing, layout, grid, containers, buttons, links, navigation, product cards, badges, forms, icons, images, borders, radius, shadows, overlays, animations, responsive behaviour and accessibility states. Tokens are only the foundation; the subsystems built on them are defined in §§10–27 of this document — Button (§10), Link (§11), Form (§12), Product Card (§13), Image (§14), Border (§15), Radius (§16), Shadow (§17), Icon (§18), Navigation (§19), Announcement Bar (§20), Motion (§21), Hover (§22), Focus (§23) and Accessibility (§24).

Spec §2 sets seven qualities the system must satisfy. Each is testable against this project, not asserted:

| Quality | How it is tested here |
|---|---|
| CONSISTENT | One scale per dimension. The prototype used 44 distinct spacing values with no scale (brief: spacing) and ~24 type styles from ~7 sizes (brief: type); the file normalises both onto ten spacing steps and one type scale |
| REUSABLE | Components read group 2 semantic tokens only; no component may carry a hex literal (rule R1 below) |
| SCALABLE | Fluid `clamp()` type and `--section-pad-block`, plus `--container-wide` 1680 / `--container-standard` 1440 / `--container-narrow` 760, so large screens need no new breakpoint (spec §11) |
| ACCESSIBLE | Every colour pairing in §3 carries a measured WCAG 2.2 ratio; the focus ring is surface-aware because gold is 11.01:1 on ink and 1.55:1 on cream (token file lines 296–304) |
| SHOPIFY-FRIENDLY | The `[THEME SETTING]` subset in §30 is deliberately small, split across theme and section/block level per spec §30 |
| MOBILE-FRIENDLY | A 12px floor for persistent interface text and 16px body (token file lines 124–126), raising the prototype's 9px badge (line 78), 11px captions (lines 58, 147, 156, 164) and 15px body (line 131); `--gutter` steps 24 → 32 → 48px |
| PERFORMANCE-CONSCIOUS | No icon library, no animation framework, no JavaScript dependency (spec §36). The whole system is custom properties in one stylesheet |

### What it governs

The token file is organised in sixteen numbered groups. The document's authority is exactly these groups plus the subsystem rules built on them.

| # | Group | Scope | Tokens |
|---|---|---|---|
| 1 | Core palette | Three approved colours plus seven derived values | 10 |
| 2 | Semantic colour | Surfaces, text, accent, borders, status, scrims | 28 |
| 3 | Typography families | Three families, four weights | 7 |
| 4 | Type scale | Display, headings, script, body, tracked uppercase set, price | 38 |
| 5 | Spacing | 4px base grid, ten steps plus two section rhythms | 12 |
| 6 | Containers | Three widths, four gutter values | 7 |
| 7 | Grid | Column count, three gaps, four editorial splits | 8 |
| 8 | Breakpoints | Reference values only — custom properties cannot be used inside media queries (token file line 241) | 5 |
| 9 | Borders and radius | Two widths, four radius steps | 6 |
| 10 | Shadow | None, subtle, elevated | 3 |
| 11 | Motion | Durations, easings, compound transitions, hover scale ceiling | 9 |
| 12 | Focus | Width, offset, two surface rings, the resolved ring | 5 |
| 13 | Touch targets and icons | 44px usability target, 24px WCAG 2.2 SC 2.5.8 floor, four icon sizes | 6 |
| 14 | Header and announcement | Header and logo heights, announcement height, nav gap | 7 |
| 15 | Product media | Product and hero aspect ratios | 3 |
| 16 | Z-index | Eight reserved layers | 8 |

It does **not** govern copy, Liquid, templates, commerce logic, merchandising, or the brand identity itself. Spec §6 forbids introducing a new brand identity; §2 of this document works only from what spec §3 already ratifies.

### How to use it

**R1 — Token-first.** A component declares no colour, size, spacing or duration literal. It reads a token. The one permitted literal is a value that has no token, and that case is a token request (§30), not a licence.

**R2 — Group 2 is the only layer components may read.** The `--gs-*` palette feeds group 2 and the two surface-aware focus tokens of group 12 (`--focus-ring-on-dark` → `--gs-gold`, `--focus-ring-on-light` → `--gs-ink`, token file lines 302–303). Nothing outside the token file may reference `--gs-*`. The file also carries four documented raw-value exceptions inside group 2 itself: `--color-text-inverse-muted` `#5F5A50`, the six status colours, the four border `rgba()` values and the four scrim gradients. These are declared once, in the file, and read semantically thereafter.

**R3 — Colour arrives by surface class, not by property.** Put `.surface-dark` or `.surface-light` on a section and everything inside inherits the correct text, border, accent and focus colour. This is the mechanism that stops gold landing on cream; §4 sets its operating rules.

**R4 — No colour pairing ships without a measured ratio.** The matrix in §3 is the register. A pairing absent from it is unverified and may not be used until it is measured and added.

**R5 — Gaps are raised, not filled.** Where a value is needed and no token exists, §30 records it as a token request under the versioning rules below. Inventing a token name or value locally breaks R1 and R2 at once.

### Relationship to the Phase 1 audit

Phase 1 delivered `PHASE-1-WEBSITE-AUDIT.md` — 32 sections, 200 issues (brief: status). The token file is the design-side answer to the subset of those findings that are design decisions rather than code defects:

- **Contrast.** Phase 1 A11Y-03 / HERO-02 measured three nav links at 2.4–2.9:1 over open sky; `--scrim-header` exists so that any hero carrying the nav over an image has a mandatory backing (token file lines 102–104).
- **Responsive tiering.** RESP-08 found no tier between 901 and 1440, which squeezes the fluid three-column grid to ~230–250px in the 901–1100 band (Phase 1 §RESP-08). Group 8 supplies five breakpoints; `--section-pad-block` is fluid so large screens do not need a sixth.
- **Layout ceiling.** The prototype's single `max-width:1440px` wrapper (line 55) put 240px dark gutters beside every band at 1920 (brief: measured responsive behaviour). Spec §11 overrides it; group 6 replaces it with full-bleed sections and constrained content.
- **Fonts.** `--font-display` keeps Playfair Display, which the prototype uses for the hero and both section headlines (lines 84, 101, 130). The file records that the 700 weight is requested from Google Fonts but never used, and directs that the request be dropped (PERF-04, token file line 109) — a Phase 10 font-loading decision, not a token change.

### Relationship to the coming Shopify theme

Phase 10 moves the file to `assets/design-tokens.css` and drives the values marked `[THEME SETTING]` from `settings_schema.json` (token file lines 9–10). Two consequences bind now:

1. Token names are an interface. Renaming one after Phase 10 is a breaking change to Liquid, so names are settled here, in §30.
2. The merchant-editable surface stays deliberately small (spec §30). Everything not in the `[THEME SETTING]` subset is developer-owned, so a merchant cannot break a verified contrast pairing. §30 sets out the two guardrails this requires.

No Liquid, template, section or schema is written in Phase 2 (spec §41).

### Versioning

The token file carries a semantic version on line 3; it is currently **1.0.0**.

| Change | Bump | Examples |
|---|---|---|
| A token is removed or renamed, or a value change alters a verified contrast pairing | MAJOR | Retiring `--product-grid-gap` (§30 T3); changing `--gs-gold` |
| A token is added, or a value changes without affecting a verified pairing | MINOR | Adding `--hero-pad-block-start` (§30 T2) or `--scrim-story-horizontal` (§30 T5) |
| A comment, citation or documentation-only correction | PATCH | Correcting the `--gs-olive` source citation at token file line 45 (§30 T7) |

This document and the token file version together. A document that cites a token the file does not declare is a defect in the document, not a licence to add the token.

The document runs to the 31 sections spec §37 fixes, from Design System Overview through Design Token Reference; §31 Phase 3 Requirements hands off to **PHASE 3 — ASSET PREPARATION**, which does not begin without explicit authorisation (spec §43).

## 2. Brand Principles

GOD SQUAD is positioned as **FAITH-DRIVEN PREMIUM STREETWEAR** (spec §3). Spec §6 forbids introducing a new brand identity, so this section ratifies nothing new: it takes the personality and the messages the spec already fixes and converts them into rules the rest of the document can be tested against.

### The eleven personality traits

The traits are spec §3's, in spec §3's order. The obligations are what each one costs the system.

| # | Trait (spec §3) | Evidence in the prototype | What it obliges the system to do |
|---|---|---|---|
| 1 | Premium | Playfair Display 900 at up to 112px (line 84); 48px gutters on every band (lines 58, 68, 82, 98, 128, 153); a single 36×1px gold rule as the only ornament (line 86) | Spend on type, space and photography, not on decoration. The restraint budgets below are the enforcement |
| 2 | Faith-driven | `Walk By Faith.` as the h1 with `Faith.` in gold (line 84); `Faith Lives Different Here.` (line 136); spec §22 reserves a VERSE nav item | Gold marks the faith word and little else. §19 must hold the VERSE slot without adding a sixth visual weight to the nav |
| 3 | Editorial | Asymmetric splits `.9fr 2.4fr` (line 98) and `.9fr 1.6fr .4fr` (line 125); the repeating eyebrow → headline → rule → tagline stack (lines 83–87, 100–104, 129–132) | `--split-30-70` and `--split-40-60` carry the prototype's own ratios (token file lines 235–237). §26 forbids making every section symmetrical (spec §33) |
| 4 | Modern | Fluid `clamp()` type at lines 84, 101, 130; `aspect-ratio:1/1` (line 109); `text-wrap:balance` (line 84) | The system assumes modern CSS rather than polyfills (spec §36). The support matrix that governs `text-wrap:balance`, `aspect-ratio`, container queries and `:has()` is BUSINESS INFORMATION REQUIRED |
| 5 | Urban | `Streetwear with a Purpose` (line 83); tracked uppercase at `.2em`–`.3em` across the announcement, nav, eyebrows, taglines, labels, captions and footer (lines 58, 70, 83, 87, 93, 100, 103, 104, 112, 129, 132, 136, 146, 147, 156, 164) | The tracked uppercase set is the brand signature. `--type-eyebrow-*`, `--type-label-*` and `--type-caption-*` always carry size and tracking together (token file lines 164–176); UI chrome does not revert to sentence case |
| 6 | Minimal | `transition` 0, `animation` 0, `@keyframes` 0 (brief: motion); one radius value — `50%`, used twice (brief: radius); `z-index` only 1 and 2 (brief: z-index) | `--radius-none` is the default and `--radius-full` is for circles only (token file line 264). Motion tokens are ceilings, not invitations; `--hover-image-scale` is capped at 1.03 (token file line 292) |
| 7 | Purposeful | "Purpose" appears in nine strings — lines 59, 83, 87, 93, 103, 130, 131, 156 and the Community value sub (data line 181) | The word is saturated. Message hierarchy must not repeat it at two adjacent levels: the announcement (line 59) sits directly above the hero eyebrow (line 83) and both carry it. §20 and hierarchy rule 4 below must resolve that pair |
| 8 | Cinematic | Full-bleed hero image behind two stacked gradients (line 66); hero `min-height:620px` (line 64), story `520px` (line 125) | `--scrim-hero-horizontal`, `--scrim-top-heavy` and `--scrim-bottom` exist so imagery can run edge to edge and stay legible; `--scrim-header` is mandatory wherever nav sits over an image (A11Y-03 / HERO-02, token file line 102). `--hero-aspect-mobile` 4/5 replaces the prototype's uncapped band |
| 9 | Community-oriented | The four-tile Values band (lines 142–147); the Community value `People With Purpose` (data line 181); "faith, creativity, and community" in the story copy (line 131) | Values are repeatable content, so §29 expresses them as blocks that can be added, removed and reordered (spec §31) — not as four hard-coded tiles |
| 10 | Confident | h1 uppercase 900 at `line-height:.88` and `-.01em` (line 84); exactly one CTA per section (lines 104, 132) | One primary action per section. §10 inherits that budget; no section acquires a second competing button |
| 11 | Authentic | "a Philippine streetwear brand built on faith, creativity, and community" (line 131); peso prices in the product data (lines 175–177) | Jost contains neither `₱` nor `→`, so both currently fall back to a per-platform face (brief: still open) — BUSINESS INFORMATION REQUIRED before §11 and §13 rely on either glyph |

### The five brand messages and their hierarchy

Spec §3 fixes five primary messages and states that messaging must have hierarchy and must not be used everywhere. This is that hierarchy.

| Message (spec §3) | Permitted level | Type tokens | Surface and colour | Prototype instance |
|---|---|---|---|---|
| `Good People. Higher Purpose.` | Announcement bar | `--type-caption-size` 0.75rem, `--type-caption-ls` 0.20em | Gold on ink, 11.01:1 | Line 58 sets `color:#d8c08a` on the bar; the string is line 59 |
| `Walk By Faith.` | Hero headline — one per page | `--type-display-xl-size/-lh/-ls` | Cream on ink 17.04:1, with `Faith.` in `--color-accent` at 11.01:1 | Line 84 |
| `More Than Clothing.` | Script accent — one per page | `--type-script-size`, `--type-script-lh`, `--font-script` | Cream on ink, 17.04:1 | Line 91, rotated −8° |
| `Different People. Same Purpose.` | Hero support **and** footer signature — the one two-placement exception | Hero: 14px `.3em` with `--type-tagline-lh`. Footer: `--type-caption-size` / `--type-caption-ls` | Cream on ink 17.04:1; footer instance uses `--color-text-muted` at 9.70:1 | Line 87 (`Different / People / Same Purpose`, unpunctuated, 14px `.3em`, `line-height:1.65`) and line 156 (`Different People. / Same Purpose.`, 11px `.26em` in the footer) |
| `Streetwear with a Purpose.` | Section eyebrow | `--type-eyebrow-size` 0.8125rem, `--type-eyebrow-ls` 0.30em, `--type-eyebrow-weight` | Gold on ink, 11.01:1 | Line 83. Spec §3 punctuates the message; the prototype omits the full stop |

**Hierarchy rules.**

1. One message per level per page. A level is: announcement bar, hero headline, script accent, section eyebrow, footer signature.
2. The hero headline is the only message permitted at display size. `--type-display-l` and `--type-display-m` carry section copy (lines 101, 130), not brand messages.
3. Gold may carry at most one word inside a headline. `Faith.` (line 84) is the precedent and the ceiling.
4. No message repeats at two vertically adjacent levels. The prototype currently breaks this in spirit: `Good People. Higher Purpose.` (line 59) sits immediately above `Streetwear with a Purpose` (line 83) and both carry the brand's most saturated word. §20 Announcement Bar resolves it.
5. `Different People. Same Purpose.` is the sole two-placement exception, because the prototype already uses it twice (lines 87, 156) — but not in the same words. Phase 3 must settle a single punctuated form; two spellings of one brand message is itself a consistency defect.
6. A string that is not one of the five is section copy, not a brand message, and gets no reserved level.

**Strings that are not brand messages.** `The Faithful` (line 101), `Premium Essentials for a Higher Purpose.` (line 103), `A Higher Purpose.` (line 93), `Real People. Bigger Purpose.` (line 130), `Faith Lives Different Here.` (line 136) and `A Brighter Tomorrow` (line 164) are all section or campaign copy. They are governed by the type scale, not by this hierarchy, and none may be promoted into the canonical set.

**Announcement copy divergence.** Spec §23 permits exactly two announcement strings — THE FAITHFUL COLLECTION and WORLDWIDE SHIPPING — and forbids inventing additional promotional messaging. The prototype ships `Good People. Higher Purpose.` (line 59) and `Worldwide Shipping` (line 60). §20 must resolve which pair ships; if the spec's pair wins, the brand message loses its announcement-bar level and hierarchy rule 4 resolves itself.

### LUXURY THROUGH RESTRAINT

Spec §4 names the central principle and lists what it rules out: excessive gold, gradients, shadows, rounded cards, borders, animations, icons, CTAs, generic ecommerce styling and visual clutter. Stated as rules against this project's own evidence:

| Do | Don't | Evidence |
|---|---|---|
| Carry emphasis with type weight, size and tracking | Add a second accent colour to make a heading louder | Three colours support 24 type styles in the prototype (brief: type) |
| Let one gold word, one gold rule and one gold CTA do the accent work on a page | Spread gold across headings, icons, borders and buttons in the same view | `#d8c08a` appears 10 times over 9 lines (16, 58, 71×2, 78, 83, 84, 86, 129, 132) |
| Use whitespace as the separator | Add a border to make a section feel contained | The Values band is the only bordered block (lines 142, 144), and it uses 1px hairlines |
| Keep corners square | Round cards, tiles or buttons | The prototype rounds exactly two things, both circles: swatches and the cart badge (line 78) |
| Reserve gradients for photographic legibility | Use a gradient as decoration | All four scrim tokens exist to make text readable over imagery, never as fill |
| Reserve shadow for surfaces that float | Give product cards a resting shadow | `--shadow-elevated` is scoped to drawers, modals and the sticky header (token file line 274) |
| Keep motion at or below `--duration-medium`, on opacity and transform | Animate width, height, top, left or margin | The prototype has zero transitions; anything added is a net increase (spec §25) |
| Hold one primary CTA per section | Stack a primary and a secondary CTA in the same band | Lines 104 and 132 are one CTA each, in different sections |

**The restraint test.** Before any element is added in a later phase, two questions: *does the prototype already do this?* If not, *what changed, and what is being removed to pay for it?* Restraint is a budget, not a mood — §§10, 15, 17, 18 and 21 each inherit a hard count from it.

**Restraint budgets carried forward.**

| Dimension | Budget | Set by |
|---|---|---|
| Gold-filled buttons | 1 per page, dark surfaces only | Line 132; §10 |
| Gold selected states | 1 per navigation bar | Line 71; §19 |
| Gold words inside a headline | 1 | Line 84 |
| Radius | Square by default; circles only for swatches, cart count, avatars | Token file lines 261–264; §16 |
| Shadow | 0 at rest; `--shadow-elevated` for floating surfaces only | Token file lines 267–274; §17 |
| Surface alternations per page | 2 (see §4) | Lines 98, 125 |
| Icon sizes | 4 (`--icon-sm/md/lg/xl`) | Token file lines 314–317; §18 |

## 3. Color Palette

> ### THE PROHIBITION
> **Muted gold `#D8C08A` measures 1.55:1 on warm cream `#F3EFE6` and 1.43:1 on the tile cream `#EBE6DC`.** Both fail WCAG 2.2 at every text size and both fail the 3:1 floor for UI component boundaries. **Gold is a dark-surface accent only.** It may never carry text, an icon, a border or any other perceivable mark on a light surface. On light surfaces the accent is `--color-accent-strong` `#82672B`, 4.66:1 on cream (token file lines 23–26, 50, 79). Every rule in this document is downstream of this one fact.

### The three approved colours

Spec §5 approves three colours and forbids replacing them.

| Token | Hex | Occurrences in the prototype | Role |
|---|---|---|---|
| `--gs-ink` | `#0D0C0A` | 14 (token file line 33) | The page ground. Body background (line 14), header, hero (line 64), story (line 125), values (line 142) and footer (line 153) all sit on it. The site is dark-led, so "primary" means dark |
| `--gs-cream` | `#F3EFE6` | 9 (token file line 33) | Body text on the dark ground (line 14) and the one light band in the page, New Drop (line 98) |
| `--gs-gold` | `#D8C08A` | 10, across 9 lines (token file line 33) | Accent. `Faith.` is the only word inside a headline that carries gold (line 84, `<span style="color:#d8c08a">Faith.</span>`). Gold text elsewhere is confined to eyebrows and labels — the announcement bar (line 58, string at 59), the active nav label `Home` (line 71), the hero eyebrow (line 83) and the story eyebrow (line 129) — all on ink. The remaining uses are non-text: the 36×1px rule (line 86), the cart badge fill (line 78), the Our Story CTA fill (line 132), the active nav underline (line 71) and the global `a:hover` (line 16) |

### The seven derived values

Spec §5 permits derived neutrals provided they are documented and derived from the existing palette. The file declares **seven**, in two sets. The brief records six (brief: extended palette); the discrepancy is the brief's, and the file is authoritative.

**Set A — derived neutrals. Each already exists in the prototype; none is new (token file lines 40–41).**

| Token | Hex | Prototype source | Measured |
|---|---|---|---|
| `--gs-cream-200` | `#E9E4D8` | Story body copy, line 131 | 15.41:1 on ink |
| `--gs-cream-300` | `#EBE6DC` | Product tile ground, line 109 | Ground only; carries no text today |
| `--gs-stone` | `#BDB6A8` | Muted captions, lines 147, 156, 164 | 9.70:1 on ink; **1.76:1 on cream — dark surfaces only** |
| `--gs-olive` | `#4B5443` | Third product swatch, prototype data lines 175–177 | 6.91:1 on cream |

The token file's comment at line 45 cites line 179 as the olive source; line 179 is `values: [`, and `#4b5443` occurs at lines 175, 176 and 177. This is a PATCH-level documentation correction under §1's versioning rules, not a value change.

**Set B — derived accents. Tuned in lightness only, with hue and saturation held, so they stay inside the palette family (token file lines 47–49).**

| Token | Hex | Why it exists | Measured |
|---|---|---|---|
| `--gs-gold-strong` | `#82672B` | The source palette has no light-surface accent, and gold fails there | 4.66:1 on cream |
| `--gs-gold-hover` | `#E6D3A6` | Already emitted by the prototype runtime as the gold CTA's hover fill (`.scp1:hover`, from the `style-hover` on line 132) | 13.25:1 on ink |
| `--gs-ink-raised` | `#2A2823` | Already emitted by the prototype runtime as the dark CTA's hover fill (`.scp0:hover`, from the `style-hover` on line 104) | Hover fill on dark |

One further colour is declared as a literal inside group 2 rather than as a `--gs-*` palette entry: `--color-text-inverse-muted` `#5F5A50`, 5.97:1 on cream (token file line 74). It exists because `--gs-stone` cannot be used on light. The six status colours are likewise literals in group 2.

### Verified contrast matrix (WCAG 2.2)

AA requires 4.5:1 for normal text, 3:1 for large text (≥24px, or ≥19px bold) and for UI component boundaries (token file lines 19–21).

| Foreground | Background | Ratio | Normal text | Verdict |
|---|---|---|---|---|
| `#F3EFE6` cream | `#0D0C0A` ink | 17.04:1 | AAA | Primary text on dark |
| `#0D0C0A` ink | `#F3EFE6` cream | 17.04:1 | AAA | Primary text on light |
| `#D8C08A` gold | `#0D0C0A` ink | 11.01:1 | AAA | The only accessible gold pairing |
| `#D8C08A` gold | `#F3EFE6` cream | **1.55:1** | **FAIL** | Prohibited |
| `#D8C08A` gold | `#EBE6DC` tile | **1.43:1** | **FAIL** | Prohibited |
| `#FFFFFF` white | `#0D0C0A` ink | 19.55:1 | AAA | Available; cream is preferred for warmth |
| `#BDB6A8` stone | `#0D0C0A` ink | 9.70:1 | AAA | Muted text on dark |
| `#BDB6A8` stone | `#F3EFE6` cream | **1.76:1** | **FAIL** | Prohibited |
| `#E9E4D8` cream-200 | `#0D0C0A` ink | 15.41:1 | AAA | Secondary text on dark |
| `#82672B` gold-strong | `#F3EFE6` cream | 4.66:1 | AA | The light-surface accent |
| `#5F5A50` muted-on-light | `#F3EFE6` cream | 5.97:1 | AA | Muted text on light |
| `#4B5443` olive | `#F3EFE6` cream | 6.91:1 | AA | Swatch and status base |
| `#E6D3A6` gold hover | `#0D0C0A` ink | 13.25:1 | AAA | Gold CTA hover |

**Status colours**, all derived by holding hue and saturation and tuning lightness (brief: contrast matrix):

| Status | On cream | Ratio | On ink | Ratio |
|---|---|---|---|---|
| Success | `#3E4636` | 8.57:1 | `#8FA07E` | 6.98:1 |
| Warning | `#82672B` | 4.66:1 | `#D8C08A` | 11.01:1 |
| Error | `#8C3F2E` | 6.39:1 | `#D98C7A` | 7.43:1 |

### The three failures, and the live defect

1. **Gold on cream, 1.55:1.** Any gold text, icon or border on the New Drop band (line 98) or on any future light section.
2. **Gold on tile cream, 1.43:1.** Anything drawn over the product media ground (line 109) — a badge, a sale flag, a sold-out label.
3. **Stone on cream, 1.76:1.** `--gs-stone` is the prototype's muted caption colour (lines 147, 156, 164) and it is a dark-surface token. On light, the muted text token is `--color-text-inverse-muted` (token file line 74, which carries the warning inline).

The live instance of failure 1 is the prototype's global `a:hover{color:#d8c08a}` (line 16). Every link inside the New Drop band turns to 1.55:1 on hover, including the dark CTA at line 104. §11 Link System must replace the chromatic hover on light surfaces with a non-chromatic one.

### Measurement gap

The matrix does not record **ink on tile cream `#EBE6DC`**. No prototype text sits on it today — the product name (line 112) and the price (line 113) are siblings after the media container closes at line 111 and therefore fall on the New Drop background `#F3EFE6` (line 98), already measured at 17.04:1. The real exposure is overlay text: §13 Product Card System will need a badge and a sold-out state drawn over the tile, so the pairing should be measured and added before Phase 3 consumes it.

### What may not be added

Spec §5 forbids arbitrary colours. A new colour enters the palette only if it satisfies all four: it is derived from an existing palette colour by lightness alone, it does a job the existing ten cannot, its ratio on both surfaces is measured and recorded in this matrix, and it is added to the token file under a MINOR version bump (§1). Sampling a colour from photography, or introducing a second accent hue, is out of scope for every phase of this project.

## 4. Semantic Color Tokens

Group 2 of the token file is the only colour layer components may read (rule R2, §1). Every token below carries its resolved value, the surface it belongs to and its measured ratio on that surface.

### Surfaces (5)

| Token | Resolves to | Meaning | Where it may be used |
|---|---|---|---|
| `--color-bg-primary` | `--gs-ink` `#0D0C0A` | The dark ground. The site is dark-led, so "primary" means dark (token file line 57) | Header, hero, story, values, footer — the prototype's default (lines 14, 64, 125, 142, 153) |
| `--color-bg-secondary` | `--gs-cream` `#F3EFE6` | The light band | New Drop (line 98) and other light sections |
| `--color-bg-inverse` | `--gs-cream` `#F3EFE6` | Alias for inverted blocks | A light block nested inside a dark section. Same value as `--color-bg-secondary` under a second name |
| `--color-surface-raised` | `--gs-ink-raised` `#2A2823` | Hover fill on dark | The dark CTA's hover state (line 104's `style-hover`, compiled to `.scp0:hover`) |
| `--color-surface-tile` | `--gs-cream-300` `#EBE6DC` | Product media ground | The `aspect-ratio:1/1` media container, line 109. Ground only — no measured text pairing yet (§3, measurement gap) |

### Text on the dark surface (3)

| Token | Resolves to | Ratio on ink | Where it may be used |
|---|---|---|---|
| `--color-text-primary` | `--gs-cream` | 17.04:1 | Headlines, body, nav, all default text on dark (line 14) |
| `--color-text-secondary` | `--gs-cream-200` `#E9E4D8` | 15.41:1 | Long-form body copy that should recede slightly from a headline above it (line 131) |
| `--color-text-muted` | `--gs-stone` `#BDB6A8` | 9.70:1 | Captions and supporting labels (lines 147, 156, 164). **Never on light — 1.76:1** |

### Text on the light surface (2)

| Token | Value | Ratio on cream | Where it may be used |
|---|---|---|---|
| `--color-text-inverse` | `--gs-ink` | 17.04:1 | All default text on light (line 98) |
| `--color-text-inverse-muted` | `#5F5A50` | 5.97:1 | Muted text on light. Declared as a literal precisely so `--gs-stone` is not reached for; the token file carries the warning inline (line 74) |

### Accent (3)

| Token | Resolves to | Ratio | Where it may be used |
|---|---|---|---|
| `--color-accent` | `--gs-gold` `#D8C08A` | 11.01:1 on ink | **Dark surfaces only.** The gold word in a headline (line 84), eyebrows (lines 83, 129), the active nav state (line 71), the rule (line 86), the cart badge (line 78), the one gold CTA (line 132) |
| `--color-accent-hover` | `--gs-gold-hover` `#E6D3A6` | 13.25:1 on ink | Hover state of the gold CTA (line 132's `style-hover`, compiled to `.scp1:hover`) |
| `--color-accent-strong` | `--gs-gold-strong` `#82672B` | 4.66:1 on cream | **Light surfaces only.** The accent everywhere `--color-accent` is prohibited |

Components should generally not name either directly. `--accent-current` resolves to the right one for the surface (see below).

### Borders (5)

| Token | Value | Surface | Notes |
|---|---|---|---|
| `--color-border` | `rgba(243, 239, 230, 0.12)` | Dark | The default hairline on dark |
| `--color-border-subtle` | `rgba(243, 239, 230, 0.08)` | Dark | Lighter separation, e.g. the announcement bar's lower edge (line 58) |
| `--color-border-strong` | `--gs-gold` | Dark | **Accent rules only** (token file line 84) — the 36×1px rule (line 86) and the active nav underline (line 71). Never on light |
| `--color-border-inverse` | `rgba(13, 12, 10, 0.14)` | Light | Default hairline on light |
| `--color-border-inverse-subtle` | `rgba(13, 12, 10, 0.08)` | Light | Lighter separation on light |

The prototype used `rgba(255,255,255,.1)`, `.08` and `.2` (brief: borders). The token file re-bases these on cream — `--color-border` 0.12, `--color-border-subtle` 0.08 — so separators sit inside the palette rather than on pure white; the file's own rationale is that alpha keeps separators tied to the surface beneath them (token file line 81). The prototype's `.2` divider, the 1×28px footer rule at line 163, has no direct token: it should resolve to `--color-border` or be raised as a token request (§30 T8). Note that `--color-border-strong` is gold, not a heavier alpha, so it is not the successor to `.2`.

### Status (6)

All verified ≥4.5:1 on their own surface (token file line 88). Each status has a light-surface and a dark-surface form; they are not interchangeable.

| Token | Value | Ratio | Surface |
|---|---|---|---|
| `--color-success` | `#3E4636` | 8.57:1 on cream | Light |
| `--color-success-on-dark` | `#8FA07E` | 6.98:1 on ink | Dark |
| `--color-warning` | `#82672B` | 4.66:1 on cream | Light |
| `--color-warning-on-dark` | `#D8C08A` | 11.01:1 on ink | Dark |
| `--color-error` | `#8C3F2E` | 6.39:1 on cream | Light |
| `--color-error-on-dark` | `#D98C7A` | 7.43:1 on ink | Dark |

`--color-warning-on-dark` is gold itself. That is deliberate and it is the one place gold carries meaning rather than emphasis — and it inherits the prohibition: a warning on a light surface is `--color-warning` `#82672B`, never gold.

### Scrims (4)

| Token | Source | Definition | Purpose |
|---|---|---|---|
| `--scrim-hero-horizontal` | Prototype line 66, first stacked gradient | `90deg`, ink at .92 → .75 (26%) → .15 (48%) → .10 (68%) → .80 (100%) — reproduced exactly | Hero copy legibility over full-bleed photography |
| `--scrim-top-heavy` | Prototype line 66, second stacked gradient, top half | `180deg`, ink .75 → transparent at 45% | Top-anchored fade. Deepened from the prototype's .55 → transparent at 30% |
| `--scrim-bottom` | Prototype line 66, second stacked gradient, bottom half | `180deg`, transparent at 55% → `--gs-ink` at 100% | Bottom fade into the ink ground. Lengthened from the prototype's start at 70% |
| `--scrim-header` | Derived; no prototype source | `180deg`, ink .85 → .55 (60%) → transparent | **Mandatory** wherever the nav sits over an image. Phase 1 A11Y-03 / HERO-02 measured three nav links at 2.4–2.9:1 over open sky (token file lines 102–104) |

The second gradient at line 66 carries a top fade and a bottom fade in one declaration; the file splits it into two tokens and deepens each. The prototype's **story fade at line 127** is a separate, horizontal `90deg` ink → transparent gradient (`#0d0c0a 30%` → `rgba(13,12,10,.55) 42%` → `rgba(13,12,10,0) 56%`) and has **no token of its own**. Either `--scrim-hero-horizontal` is declared to cover it, or a `--scrim-story-horizontal` is added; §30 T5 records it.

### The surface-context mechanism

```css
.surface-dark {
  background-color: var(--color-bg-primary);
  color: var(--color-text-primary);
  --color-border-current: var(--color-border);
  --accent-current: var(--color-accent);
  --focus-ring: var(--focus-ring-on-dark);
}

.surface-light {
  background-color: var(--color-bg-secondary);
  color: var(--color-text-inverse);
  --color-border-current: var(--color-border-inverse);
  --accent-current: var(--color-accent-strong);   /* NOT --color-accent */
  --focus-ring: var(--focus-ring-on-light);
}
```

This is the enforcement mechanism for the prohibition in §3. A component that reads `--accent-current` and `--color-border-current` cannot put gold on cream, because on a light surface those names do not resolve to gold. A component that hard-codes `--color-accent` can, which is why R2 exists.

**Operating rule 1 — dark sections.** `.surface-dark` is the default. Text is `--color-text-primary`, secondary copy `--color-text-secondary`, captions `--color-text-muted`, accents `--accent-current` (gold), hairlines `--color-border-current`, focus `--focus-ring` (gold, 11.01:1). This describes the prototype's header, hero, story, values and footer.

**Operating rule 2 — light sections.** `.surface-light` flips all five. Text is `--color-text-inverse`, muted text `--color-text-inverse-muted` — never `--gs-stone` — accents `--accent-current` (now `#82672B`), hairlines `--color-border-inverse`, focus `--focus-ring` (ink, 17.04:1). This describes New Drop (line 98).

**Operating rule 3 — nesting, and what "inverse" means.** "Inverse" is not a third surface. `--color-bg-inverse` and `--color-bg-secondary` both resolve to `--gs-cream`; they are one value under two names. An inverse block is therefore a `.surface-light` nested inside a `.surface-dark` (or the reverse). Nesting the class re-declares all five context variables at that scope, so a nested block is correct by construction. A nested block must never be styled by overriding individual colour properties — that is exactly the path that produces gold on cream.

**Operating rule 4 — the transition between surfaces.** Spec §32 requires the dark↔light transition to feel intentional. The prototype has exactly two such boundaries: dark → light where New Drop opens (line 98) and light → dark where the story opens (line 125). Both are hard butt-joins with no seam treatment, and that is the system default: the colour change is the transition, and no gradient, hairline or shadow is added across a surface boundary. A hairline at `--color-border-current` separates two bands of the *same* surface — the Values band's `border-top` and `border-bottom` (line 142) are the precedent. A scrim never crosses a surface boundary; the scrim tokens exist for photography only. A page template may not alternate surface more than twice, which keeps any homepage at a maximum of three bands of alternating ground and preserves the New Drop band's status as the one light moment in the page.

**Editorial sections** are a composition pattern, not a surface: they may be dark or light and are governed by §26.

### Colour usage rules

From spec §6, expressed against this token set:

| Colour | Permitted uses (spec §6) | Token to reach for |
|---|---|---|
| NEAR BLACK | Primary background, header, footer, dark editorial sections; primary text on light backgrounds | `--color-bg-primary`, `--color-text-inverse` |
| WARM CREAM | Primary light background, cards where appropriate, light section backgrounds; light text on dark surfaces | `--color-bg-secondary`, `--color-text-primary` |
| MUTED GOLD | Accent, selected states, small labels, editorial details, borders where appropriate, subtle emphasis | `--accent-current` on dark; `--color-border-strong` for accent rules |

### Gold never becomes the dominant UI colour

Spec §6 states it plainly: gold must not become the dominant UI colour, and gold buttons must not appear everywhere. Expressed as surface-scoped budgets rather than bans:

- **On dark**, gold may fill **at most one button per page** — the prototype's Our Story CTA (line 132, `background:#d8c08a;color:#0d0c0a`, 11.01:1 and fully accessible) — and may mark **one selected state per navigation bar** (the active `Home` label and its underline, line 71). The cart badge (line 78) is the one gold status mark.
- Gold may **not** fill a section, a card or a tile.
- Gold may **not** colour body copy, product names or prices, on any surface.
- Gold may **not** appear at all on a light surface, where the accent is `--color-accent-strong`.
- Icon colour is defined in §18 Icon System.

The gold button variant is specified in §10 (spec §13 defines an "Accent: muted gold selectively" variant); the active-navigation treatment is specified in §19 (spec §22). Neither is settled here — this section sets only the ceiling they must fit inside.

## 5. Typography

God Squad runs three families. All three are already in the prototype, so Phase 2 is not choosing faces — it is fixing which face does which job, and which jobs each face is barred from.

### 5.1 The three families

| Token | Faces to load | For | Explicitly NOT for | Source |
|---|---|---|---|---|
| `--font-display` `'Playfair Display', Georgia, 'Times New Roman', serif` | Playfair Display 900 | Hero headlines, campaign and collection headlines, major editorial statements, brand storytelling headlines | Interface text, navigation, buttons, labels, prices, product names, body copy, form text. Only the 900 face is loaded, so there is no Playfair at small sizes to reach for | tokens line 112; prototype lines 84, 101, 130 |
| `--font-body` `'Jost', Helvetica, Arial, system-ui, sans-serif` | Jost 400 / 500 / 600 | Navigation, product titles, prices, body copy, buttons, labels, eyebrows, captions, utility text — everything the customer reads to transact | Hero and collection headlines; those are Playfair. Jost's loaded faces also cannot render `₱` or `→` (§5.4) | tokens line 113; prototype line 14 |
| `--font-script` `'Kaushan Script', 'Brush Script MT', cursive` | Kaushan Script 400 | One editorial accent per section, maximum — a handwritten brand moment beside a headline | Navigation, buttons, prices, product information, long paragraphs (spec §8). Also not for eyebrows, captions, form labels or anything a customer must scan | tokens line 114; prototype line 91 |

Weights are tokenised once and referenced by name: `--weight-regular` 400, `--weight-medium` 500, `--weight-semibold` 600, `--weight-black` 900 (tokens lines 116-119).

Phase 2 defines the loaded set as Playfair Display 900, Jost 400/500/600 and Kaushan Script 400 — five faces, not the six the prototype's font URL requests (line 12). The sixth is Playfair Display 700, which is requested and never used; dropping it is the font-payload half of PERF-04.

### 5.2 The display voice

Playfair Display 900 is the only display weight. It is always uppercase, always at a line-height of 1.15 or tighter — 0.88, 0.90, 1.05, 1.05 and 1.15 across the five steps (tokens lines 131, 135, 139, 144, 146) — and always tracked tight on the two largest steps: `--type-display-xl-ls` and `--type-display-l-ls` are both `-0.01em` (tokens lines 132, 136), while `--type-display-m-ls` returns to `0em` (tokens line 140), because negative tracking stops paying at 40px.

A tight line-height under a 900 serif at 112px is the whole composition. It is why the hero reads as a poster rather than a page, and it is the first thing a later phase will be tempted to loosen. The rule is: display line-heights are fixed by token and are not a per-section decision.

`text-wrap: balance` sits on the prototype's `<h1>` (line 84). It is the correct tool for a three-word headline and it is the reason the headline's line count is a browser decision rather than a `<br>`. Whether it can be relied on is a support-matrix question — BUSINESS INFORMATION REQUIRED.

**The Kaushan count rule.** Kaushan Script appears at most once per section and never more than twice on a page. The prototype does not yet violate this: Kaushan Script appears exactly once in the document, on the rotated accent (line 91); the font is requested once (line 12) and used once. What is duplicated is the *copy*, not the face — the string "More Than Clothing" is both the Kaushan accent (line 91) and the Faith Driven value subtitle (line 180), which renders in Jost tracked caps at 11px (line 147). Phase 2 records the count rule before a second Kaushan element can be added; the copy duplication is a messaging-hierarchy question for spec §3, not a typographic one.

### 5.3 Tracked uppercase as the brand signature

The single most recognisable typographic gesture on the site is small Jost, set uppercase, tracked wide. It carries the eyebrows, the verse, the taglines, the navigation, the buttons, the product names, the value titles and the footer. The prototype spells it twenty-plus times with six tracking values and no names. Phase 2 reduces it to four steps in which **size and tracking always travel together** (tokens line 165) — quoting a size without its tracking is a defect.

| Step | Size | Tracking | Weight | Transform | Replaces in the prototype |
|---|---|---|---|---|---|
| `--type-eyebrow` | `0.8125rem` 13px (tokens 166) | `0.30em` (167) | `--weight-medium` 500 (168) | uppercase | `.30em` and `.24em` at 13px (lines 83, 100, 103, 129), and the 14px `.30em` verse and taglines (lines 85, 87, 93), which come down 1px |
| `--type-label` | `0.75rem` 12px (170) | `0.22em` (171) | `--weight-semibold` 600 (172) | uppercase | `.20em` and `.22em` at 12px (lines 70, 104, 112, 132), and the 13px `.22em` w600 value-tile title (line 146), which comes down 1px |
| `--type-caption` | `0.75rem` 12px (174) | `0.20em` (175) | `--weight-regular` 400 (176) | uppercase | `.22em`, `.26em` and `.20em` at 11-12px (lines 58, 136, 147, 156, 164), raised 11 to 12px |
| `--type-price` | `0.9375rem` 15px (178) | `0em` (180) | `--weight-semibold` 600 (179) | none | 14px w600 untracked price (line 113), raised 1px |

Price is in the set as its deliberate exception: it is the one small Jost step that is neither tracked nor uppercased, because a tracked price is harder to compare and `₱` sits badly at `0.22em`.

Consolidation moves more than size. Nav drops from `.20em` w500 to `0.22em` w600 (line 70); the New Drop supporting line rises from `.24em` to `0.30em` (line 103); the announcement and footer come down from `.22em` and `.26em` to `0.20em` (lines 58, 156, 164); the story side rail comes down from `.22em` to `0.20em` (line 136). Each is a tracking normalisation, not a size change, and none of them alters a line count at any measured width.

Multi-line tracked caps need air that single-line ones do not: `--type-tagline-lh` `1.70` (tokens line 183) is the line-height for stacked uppercase blocks such as the hero taglines (lines 87, 93). It is the only line-height the tracked set carries.

### 5.4 The glyph gap, and what it costs

Jost's loaded faces contain neither `₱` U+20B1 nor `→` U+2192, so the peso sign in every price and the arrow in both CTAs (lines 104, 132) are drawn by a per-platform fallback face (BRAND-03, DEBT-11). Phase 1 measured the substitution by glyph width on the audit machine and records that the mockup's `₱` is a sans glyph matching the digits (Phase 1 §17).

Three consequences for the system:

1. `--type-price-size` and `--type-price-weight` cannot guarantee a rendered appearance. The digits are Jost; the currency mark is whatever the device supplies. This is the most commercial typography on the site and it is currently the least controlled.
2. The arrow is decoration, not language. It belongs in the icon set (§18) as an SVG that inherits `currentColor`, not in the text run — which also removes it from the string a screen reader announces.
3. The peso needs a decision, not a workaround: a subset face that carries U+20B1, a different body face, or a documented acceptance of the fallback. **BUSINESS INFORMATION REQUIRED.**

### 5.5 Family application, in one rule

Playfair for the statement, Jost for everything that has a job, Kaushan once. If a piece of text tells the customer what something is, what it costs, or where to go, it is Jost. If it exists to make the page feel like an editorial, it may be Playfair. If it exists to feel handwritten, it may be Kaushan — once.

## 6. Type Scale

The token file names fifteen size steps, plus one line-height override for multi-line tracked caps (`--type-tagline-lh`, tokens line 183). They replace the prototype's twenty-four distinct styles built from roughly seven sizes, six tracking values and nine line-heights (brief: type inventory).

### 6.1 The scale

Weights marked † are stated by this document but held by no token; see the token gaps. Tracking marked — is not tokenised on that step.

| Token | Size | Weight | Line-height | Tracking | Transform | Family | Usage | Prototype origin |
|---|---|---|---|---|---|---|---|---|
| `--type-display-xl` | `clamp(3.5rem, 8.5vw, 7rem)` 56 → 112px (130) | 900 † | `0.88` (131) | `-0.01em` (132) | uppercase | display | Hero headline, one per page | line 84 |
| `--type-display-l` | `clamp(2.5rem, 4.6vw, 4rem)` 40 → 64px (134) | 900 † | `0.90` (135) | `-0.01em` (136) | uppercase | display | Campaign / collection headline | line 101 |
| `--type-display-m` | `clamp(2rem, 4vw, 2.5rem)` 32 → 40px (138) | 900 † | `1.05` (139) | `0em` (140) | uppercase | display | Story and major section headline | line 130 |
| `--type-h1` | `clamp(2rem, 3.4vw, 3rem)` 32 → 48px (143) | 900 † | `1.05` (144) | — | uppercase | display | Page title on template pages | derived |
| `--type-h2` | `clamp(1.625rem, 2.6vw, 2.25rem)` 26 → 36px (145) | 900 † | `1.15` (146) | — | uppercase | display | Sub-section heading | derived |
| `--type-h3` | `clamp(1.25rem, 1.8vw, 1.5rem)` 20 → 24px (147) | 600 † | `1.25` (148) | — | sentence | body | Interface heading | derived |
| `--type-h4` | `1.125rem` 18px (149) | 600 † | `1.35` (150) | — | sentence | body | Card and block heading | derived |
| `--type-script` | `clamp(1.875rem, 3vw, 2.75rem)` 30 → 44px (153) | 400 † | `1.10` (154) | — | none | script | The single script accent | line 91 |
| `--type-body-lg` | `1.125rem` 18px (157) | 400 † | `1.65` (158) | — | none | body | Lead paragraph | derived |
| `--type-body` | `1rem` 16px (159) | 400 † | `1.65` (160) | — | none | body | Default paragraph | line 131, raised from 15px |
| `--type-body-sm` | `0.875rem` 14px (161) | 400 † | `1.55` (162) | — | none | body | Legal, shipping note, helper text | derived |
| `--type-eyebrow` | `0.8125rem` 13px (166) | 500 (168) | inherit | `0.30em` (167) | uppercase | body | Section eyebrow, verse, tagline | lines 83, 100, 129; plus 85, 87, 93 at 14px |
| `--type-label` | `0.75rem` 12px (170) | 600 (172) | inherit | `0.22em` (171) | uppercase | body | Navigation, buttons, product name | lines 70, 104, 112, 132; plus 146 at 13px |
| `--type-caption` | `0.75rem` 12px (174) | 400 (176) | inherit | `0.20em` (175) | uppercase | body | Announcement, value subtitle, footer | lines 58, 147, 156, 164, raised from 11px |
| `--type-price` | `0.9375rem` 15px (178) | 600 (179) | inherit | `0em` (180) | none | body | Price | line 113, raised from 14px |

One value in the type group is not a step: `--type-tagline-lh` `1.70` (tokens line 183) is a line-height override applied to stacked tracked-uppercase blocks such as the hero taglines (lines 87, 93). It modifies `--type-eyebrow`; it does not add a sixteenth size.

### 6.2 The mobile floor and what it moves

The floor is: no persistent interface text below `0.75rem` (12px), body copy at `1rem` (16px) (tokens lines 124-126). It moves eight things, in both directions.

| What | Prototype | Token | Δ |
|---|---|---|---|
| Cart badge count | 9px w600 (line 78) | `--type-caption-size` 12px, `0.20em` | +3px |
| Announcement bar | 11px, `.22em` (line 58) | `--type-caption-size` 12px, `0.20em` | +1px |
| Value tile subtitle | 11px, `.20em` (line 147) | `--type-caption-size` 12px, `0.20em` | +1px |
| Footer lines | 11px, `.26em` (lines 156, 164) | `--type-caption-size` 12px, `0.20em` | +1px |
| Story paragraph, the only `<p>` | 15px, lh 1.65 (line 131) | `--type-body-size` 16px, lh 1.65 | +1px |
| Price | 14px w600 (line 113) | `--type-price-size` 15px w600 | +1px |
| Hero verse and taglines | 14px, `.30em` (lines 85, 87, 93) | `--type-eyebrow-size` 13px, `0.30em` | −1px |
| Value tile title | 13px, `.22em`, w600 (line 146) | `--type-label-size` 12px, `0.22em`, w600 | −1px |

The two reductions are the price of consolidation: `0.30em` exists only at 13px and `0.22em` w600 only at 12px, so anything carrying that tracking joins that step. They are downward changes to the proportions of a brand-approved mockup, and they belong to the same confirmation as the floor itself. **BUSINESS INFORMATION REQUIRED:** confirm the 12px floor and these two reductions against brand intent before Phase 9 applies them.

The 9px cart badge is not negotiable on accessibility grounds alone — it is also a 14×14px circle (line 78) holding a two-digit number at 12px, which is a badge-geometry question for §13, not a type question.

### 6.3 Responsive behaviour, 375 → 1920

Computed from the `clamp()` expressions, in CSS px, at a 16px root.

| Step | 375 | 390 | 430 | 768 | 1024 | 1280 | 1440 | 1920 |
|---|---|---|---|---|---|---|---|---|
| `--type-display-xl` | 56 | 56 | 56 | 65.3 | 87.0 | 108.8 | 112 | 112 |
| `--type-display-l` | 40 | 40 | 40 | 40 | 47.1 | 58.9 | 64 | 64 |
| `--type-display-m` | 32 | 32 | 32 | 32 | 40 | 40 | 40 | 40 |
| `--type-h1` | 32 | 32 | 32 | 32 | 34.8 | 43.5 | 48 | 48 |
| `--type-h2` | 26 | 26 | 26 | 26 | 26.6 | 33.3 | 36 | 36 |
| `--type-h3` | 20 | 20 | 20 | 20 | 20 | 23.0 | 24 | 24 |
| `--type-script` | 30 | 30 | 30 | 30 | 30.7 | 38.4 | 43.2 | 44 |
| `--type-h4`, `--type-body-lg` | 18 | 18 | 18 | 18 | 18 | 18 | 18 | 18 |
| `--type-body` | 16 | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| `--type-price` | 15 | 15 | 15 | 15 | 15 | 15 | 15 | 15 |
| `--type-body-sm` | 14 | 14 | 14 | 14 | 14 | 14 | 14 | 14 |
| `--type-eyebrow` | 13 | 13 | 13 | 13 | 13 | 13 | 13 | 13 |
| `--type-label`, `--type-caption` | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 |

Three things this table settles.

**Phones are a fixed design.** At 375, 390 and 430 every fluid step sits on its floor — `--type-display-xl` holds 56px below 659px, `--type-display-l` below 870px, `--type-script` and `--type-display-m` below 800-1000px. Mobile type does not shrink with the viewport, which is what spec §9's "readable and editorial on mobile" requires and what a raw `vw` size would destroy.

**Above 1440, type stops moving.** Every cap is reached at or below 1440 except `--type-script-size`, which reaches 44px at 1467px and so gains 0.8px between 1440 and 1920. What changes on a large screen is the container (§8), not the type. No type breakpoint is needed above 1440.

**The 1440 headline is a copy question, not a size question.** `--type-display-xl-size` caps at 112px from 1318px upward, so 1440 and 1920 render identically. Phase 1 measured the headline on three lines at 1440 where the mockup sets two (brief: measured responsive behaviour); with a fixed 112px and `text-wrap: balance`, the line count follows the content width and the string length. **BUSINESS INFORMATION REQUIRED:** whether the two-line setting is a requirement.

### 6.4 Why `clamp()` rather than breakpoint overrides

Fifteen steps across five breakpoints is a 75-cell override matrix. Fluid, it is fifteen declarations. That is the arithmetic, but it is not the argument.

The argument is the prototype. It carries two `max-width` queries — 900px and 520px — 55 `!important` declarations, 25 distinct `data-r` hooks and one dead rule targeting `[data-r=pad]`, which no element carries (brief: measured responsive behaviour). Between 901 and 1440 there is no tier at all, which is exactly where Phase 1 found the three-column grid squeezed to ~230-250px with the eyebrow, the product names and `View All Products` all wrapping (RESP-08). A breakpoint system fails in the gaps between its breakpoints. A `clamp()` system has no gaps: the 901-1100 band is not a hole to be patched, it is simply a point on a line.

The override matrix also has a maintenance cost the prototype already demonstrates — a rule for an element that no longer exists is invisible until someone audits for it. Fifteen fluid declarations cannot drift out of sync with the markup in that way.

Two constraints on how `clamp()` is written here:

- **Endpoints are `rem`, the preferred value is `vw`.** Every step in §6.1 follows this. A `vw`-only size ignores the user's root font size and fails WCAG 1.4.4; `rem` floors and ceilings keep user zoom and browser text-size settings working while the middle of the range stays fluid.
- **A step's floor is the mobile design.** Because the floor holds across every phone width, the floor value is not a fallback — it is the phone's type size and should be reviewed as such.

`clamp()` support belongs in the support matrix — **BUSINESS INFORMATION REQUIRED** — as do `text-wrap: balance` (line 84), `aspect-ratio`, `:has()` and container queries.

## 7. Spacing Scale

The prototype uses 44 distinct px values with no scale (brief: spacing actually used). Phase 2 replaces them with ten tokens on a 4px base grid.

### 7.1 The ten tokens

| Token | rem | px | Typical use |
|---|---|---|---|
| `--space-1` | `0.25rem` | 4 | Optical nudges; icon-to-text on a single line |
| `--space-2` | `0.5rem` | 8 | Tight stacks: value title to subtitle, price to swatch row |
| `--space-3` | `0.75rem` | 12 | Button block padding; announcement bar block padding |
| `--space-4` | `1rem` | 16 | Eyebrow to headline; product name to price |
| `--space-5` | `1.5rem` | 24 | Grid gaps, mobile gutter, button inline padding |
| `--space-6` | `2rem` | 32 | Tablet gutter; large grid gaps; footer group gaps |
| `--space-7` | `2.5rem` | 40 | Navigation gap; headline to CTA; section padding floor |
| `--space-8` | `3rem` | 48 | Desktop gutter; tile block padding |
| `--space-9` | `4rem` | 64 | Separation between stacked blocks inside one section |
| `--space-10` | `6rem` | 96 | Section padding ceiling |

(tokens lines 192-201)

### 7.2 The 4px base grid

Every token is divisible by 4. The scale is deliberately not linear: 4-8-12-16 in 4px steps, then 24-32-40-48 in 8px steps, then 64 and 96. Fine control where spacing is optical — an icon beside a label, a caption under a title — and coarse control where spacing is compositional, so two sections cannot end up 8px apart in rhythm and look like a mistake.

The audit rule follows directly: **any spacing value in a later phase that is not one of these ten tokens, `--gutter`, or a section-rhythm token is a defect.** That is a check a reviewer can run with a regular expression, which is the practical reason for the 4px grid — it makes non-compliance mechanical to find rather than a matter of taste.

One category sits outside the scale by design: header clearance (§7.3, the 170/190 rows) and component-intrinsic geometry such as the 14px cart-badge circle (line 78) and the 1px separators. Those are dimensions, not rhythm.

### 7.3 Normalisation: every stray value and where it lands

| Prototype value | Where | Token | Δ |
|---|---|---|---|
| 6px | announcement stacked gap at ≤520 (line 50), logo box inline padding (line 69), price margin-top (line 113) | `--space-2` 8px | +2 |
| 10px | value tile gap and icon margin (lines 144, 145), verse margin-top (line 85), swatch row gap (line 114), announcement block padding at ≤520 (line 50) | `--space-2` 8px | −2 |
| 12px | announcement block padding (line 58), CTA inline gap (lines 104, 132) | `--space-3` 12px | 0 |
| 14px | eyebrow margin-bottom (line 83), product name margin-top (line 112), swatch row margin-top (line 114) | `--space-4` 16px | +2 |
| 16px | CTA block padding (lines 104, 132), drop padding at ≤900 (line 29) | `--space-4` 16px | 0 |
| 16px inline | announcement inline padding at ≤520 (line 50) | `--gutter-mobile` 24px (§8.3) | +8 |
| 18px | social row gap (line 159), story side margin-top (line 137), value gap at ≤900 (line 43) | `--space-4` 16px | −2 |
| 20px | script margin-left (line 91), product gap at ≤900 (line 34) | `--space-5` 24px | +4 |
| 22px | nav block padding (line 68), h2 margin-top (line 101), rule margin-bottom (line 102) | `--space-5` 24px | +2 |
| 24px | mobile section inline padding (lines 29, 33, 42), value tile inline padding (line 144) | `--space-5` 24px | 0 |
| 26px | header utility gap (line 74), hero rule margin-bottom (line 86), CTA inline padding (lines 104, 132), headline and paragraph margin-top (lines 130, 131) | `--space-5` 24px | −2 |
| 28px | footer group gap (line 154), story padding at ≤900 (line 42) | `--space-6` 32px | +4 |
| 30px | script rule margin-bottom (line 92), drop rule margin-top (line 102) | `--space-6` 32px | +2 |
| 32px | drop gap and padding at ≤900 (lines 33, 41), footer gap (line 153) | `--space-6` 32px | 0 |
| 36px | script rule margin-top (line 92), CTA margin-top (lines 104, 132), product grid gap (line 106) | `--space-6` 32px | −4 |
| 38px | hero rule margin-top (line 86) | `--space-7` 40px | +2 |
| 40px | drop grid gap (line 98), drop padding at ≤900 (line 33) | `--space-7` 40px | 0 |
| 44px | nav link gap (line 70), value tile block padding (line 144), drop block-end padding (line 98) | `--space-8` 48px | +4 |
| 48px | desktop inline padding (lines 58, 68, 82, 90, 98, 128, 153) | `--space-8` 48px → `--gutter-desktop` | 0 |
| 56px | hero and story block padding (lines 82, 90, 128, 135) | absorbed by `--section-pad-block` (§7.4) | fluid |
| 170px | hero copy block-start (line 82) | `calc(var(--header-height-desktop) + var(--space-8))` | 0 |
| 190px | hero side block-start (line 90) | same expression | −20 |

Five points about this table.

**1.** Setting aside the 190px hero side offset, which normalises onto the same header-offset expression as the copy column (−20px, and flagged below), the largest delta is 4px, on four values — 20→24, 28→32, 36→32 and 44→48. The normalisation is a tightening, not a redesign.

**2.** The direction is not uniform: nine values rise, five fall, six already sit on a step. The scale is a nearest-step rule, not a rounding-up rule, which is why a section's rhythm does not silently inflate.

**3.** The announcement bar is the one place the prototype's inline padding drops below 24px — `padding: 10px 16px !important` at ≤520 (line 50). That is why §8.3's ladder starts at `--gutter-mobile` 24px and the announcement bar stops being an exception: under one gutter it shares the page's inline padding at every width, which also retires the mirror-image defect at 768, where the announcement keeps a 48px gutter while everything else uses 24px (brief: measured responsive behaviour).

**4.** The 36px product grid gap is the one place the token file disagrees with itself. The normalisation comment maps 36→32 (tokens line 189) and `--grid-gap-large`'s comment claims 32px "matches the 36px product gap" (tokens line 230), but the shipped `--product-grid-gap` is `--space-5` 24px (tokens line 231). §9.3's column arithmetic uses the shipped 24px and states what moves if Phase 9 resolves it the other way. Recorded as a token gap.

**5.** 170px and 190px are not spacing at all — they are header clearance. The normalisation comment promises "header offset tokens" (tokens line 189) that the file does not define. §7.3 resolves both onto `calc(var(--header-height-desktop) + var(--space-8))`, which is 122 + 48 = 170px (tokens lines 199, 323). Naming the relationship rather than the number is what makes the hero survive a logo-height change, and it is why the 190px side column loses 20px: there was never a reason for the two hero columns to clear the header by different amounts.

### 7.4 Section rhythm

| Token | Expression | Floor | Ceiling | For |
|---|---|---|---|---|
| `--section-pad-block` | `clamp(var(--space-7), 6vw, var(--space-10))` (tokens 204) | 40px | 96px | Default block padding for a full section |
| `--section-pad-block-tight` | `clamp(var(--space-6), 4vw, var(--space-8))` (tokens 205) | 32px | 48px | Bands that are structural rather than editorial: values strip, announcement, footer |

Computed, in CSS px:

| | 375 | 768 | 1024 | 1280 | 1440 | 1920 |
|---|---|---|---|---|---|---|
| `--section-pad-block` | 40 | 46.1 | 61.4 | 76.8 | 86.4 | 96 |
| `--section-pad-block-tight` | 32 | 32 | 41 | 48 | 48 | 48 |

The prototype's desktop block padding runs 26px (footer, line 153), 44-48px (drop, line 98; value tile, line 144) and 56px (hero block-end, lines 82 and 90; story, lines 128 and 135), with the hero's 170/190px block-start doing header-clearance work rather than rhythm work. Against the 56px editorial baseline, `--section-pad-block` is 86.4px at 1440 and 96px at 1920 — roughly 1.5× at 1440 and 1.7× at 1920, which is the whitespace spec §4 asks for and the prototype's boxed 1440 layout could not afford.

Two rules attach to these tokens:

- **`padding-block` only, never `margin-block`.** Adjacent sections must meet without margin collapse so that a dark band and a cream band share an exact seam (spec §32). A margin between them is a visible hairline of whatever is behind the page.
- **Inline padding never comes from these tokens.** It comes from `--gutter` (§8.3). A section that sets its own inline padding has left the container system.

### 7.5 Application rules

- **Vertical rhythm runs one direction.** Space between stacked elements is applied as `margin-block-start` on the element that follows, never as `margin-bottom` on the element before. Stacks then compose predictably and an element can be removed without leaving its trailing space behind.
- **`gap` over margins.** Anything inside a flex or grid container is spaced with `gap`, from the scale. The prototype already does this in nine places (lines 70, 74, 98, 106, 114, 142, 144, 153, 159); the system makes it the only way.
- **`--gutter` for inline page padding.** Never a `--space-*` token directly, so a band cannot drift out of the ladder at one breakpoint.
- **Controls take their padding from the scale, not from a line-height.** A button's block padding is `--space-3` (12px) and its inline padding `--space-5` (24px) unless §10 documents otherwise; the resulting box must still clear `--target-min` 44px (tokens line 312), which is what the 4px grid makes checkable. It is worth checking now: at `--type-label-size` 12px, 12px of block padding lands near 36px, so §10 must either raise the block padding to `--space-4` 16px — which reproduces the prototype's ~46px CTA box (lines 104, 132) — or set `min-block-size: var(--target-min)`.
- **Form fields use the same pair**, with `--space-2` (8px) between a label and its field and `--space-4` (16px) between stacked fields, so a newsletter row and a CTA sit on the same rhythm. The values are the scale's; the states belong to §12.
- **Navigation spacing is tokenised once.** `--nav-gap` is `--space-7` 40px (tokens line 329), normalised from the prototype's 44px (line 70).
- **The value tile is a tile, not a section.** Its 44px block / 24px inline padding (line 144) normalises to `--space-8` / `--space-5` and does not take `--section-pad-block`; the strip as a whole takes `--section-pad-block-tight`. This is the one documented exception, and it exists because the tile's padding is what separates the four cells from each other, not what separates the band from its neighbours.

## 8. Container System

Spec §11 is unambiguous: "The site must naturally expand to large screens. Do not treat the original screenshot dimensions as the website dimensions." The container system is how that is enforced.

### 8.1 The pattern: full-bleed section, constrained content

A section is a band that runs edge to edge at every width. Only its content is constrained.

```css
/* Rhythm only. The surface class carries background, text, border and focus. */
.section {
  padding-block: var(--section-pad-block);
}

.container {
  width: 100%;
  max-width: var(--container-standard);
  margin-inline: auto;
  padding-inline: var(--gutter);
}
.container--wide   { max-width: var(--container-wide); }
.container--narrow { max-width: var(--container-narrow); }
```

```html
<section class="section surface-light">
  <div class="container"> ... </div>
</section>
```

A section never writes `background-color` itself. It carries `.surface-dark` or `.surface-light` (tokens lines 360-374), which reassigns `--accent-current` to `--color-accent-strong` and `--focus-ring` to `--focus-ring-on-light` on cream. Without the class a light band keeps the root's gold focus ring at 1.55:1 (brief: contrast matrix), applied through the global `:focus-visible` rule at tokens lines 382-385. The surface classes are the only mechanism that reassigns those two variables, which is why the token file describes them as "what stops gold landing on cream" (tokens line 357).

### 8.2 The three widths

| Token | Value | Content box at 1920 | Band edge to content | For |
|---|---|---|---|---|
| `--container-wide` | 1680px (tokens 215) | 1584px | 168px each side | Full-width editorial imagery, the values strip, a four-up product row that should breathe |
| `--container-standard` | 1440px (tokens 216) | 1344px | 288px each side | The default. Every section that does not state otherwise |
| `--container-narrow` | 760px (tokens 217) | 712px | 604px each side | Long-form reading: policy pages, a full story page, article body |

`--container-standard` is 1440px, the same number as the prototype's wrapper (line 55). What the system changes is *what the number constrains*: under §8 it caps the content box rather than the band. Above 1440px the band continues and only the content stops.

Two notes. `--container-narrow` at 760px is a container width, not a measure — at `--type-body-size` 16px it runs to roughly 95 characters, above the 45-75 that reads comfortably, so long-form text inside it carries `max-inline-size: 65ch` on the text element. And the story paragraph's `max-width: 320px` (line 131) is a per-element cap inside a grid track, not a container; it stays where it is and is not promoted to a container token.

### 8.3 The gutter ladder

| Token | Value | Applies | Matches |
|---|---|---|---|
| `--gutter-mobile` | `--space-5` 24px (tokens 219) | default, below 768px | the prototype's mobile rules (lines 29, 33, 42) |
| `--gutter-tablet` | `--space-6` 32px (tokens 220) | ≥ 768px (tokens 387) | new tier; the prototype has none |
| `--gutter-desktop` | `--space-8` 48px (tokens 221) | ≥ 1024px (tokens 388) | the prototype's desktop padding (lines 58, 68, 82, 98, 128, 153) |
| `--gutter` | resolves to one of the above (tokens 222) | everywhere | the only inline-padding value a container may use |

Resulting content box inside `--container-standard`:

| Viewport | Gutter | Content box |
|---|---|---|
| 375 | 24 | 327 |
| 390 | 24 | 342 |
| 430 | 24 | 382 |
| 768 | 32 | 704 |
| 1024 | 48 | 928 |
| 1280 | 48 | 1184 |
| 1440 | 48 | 1344 |
| 1920 | 48 | 1344 (capped) |

327, 342 and 382 are exactly the product tile widths Phase 1 measured at 375, 390 and 430 (brief: measured responsive behaviour). The ladder therefore does not change the phone composition — it formalises it. At 768 the ladder yields a 704px content box against the 705px Phase 1 measured there (RESP-06), so the tablet tier is a 1px difference plus a tokenised name.

### 8.4 What this replaces

The prototype has one wrapper: `max-width:1440px; margin:0 auto; background:#0d0c0a; overflow:hidden` (line 55). It produces three problems the container system removes.

1. **Dark gutters above 1440.** At 1920 the whole site is a 1440px box with 240px of near-black each side (brief: measured responsive behaviour). It reads as a letterboxed mockup rather than a website. Under §8 the band is the `<section>`, so at 1920 a cream section's cream runs to both viewport edges and only the 1344px content box stops; the 240px strips become section background.
2. **A light band that cannot reach the edge.** The wrapper paints `#0d0c0a`, so no light section can be full-bleed at any width. The New Drop's cream (line 98) is bounded by the wrapper, not by the design.
3. **Masked overflow.** `overflow:hidden` on the wrapper means Phase 1's finding of no horizontal overflow at any width is a property of the mask, not of the layout (brief: measured responsive behaviour). Removing the wrapper removes the mask, so any overflow becomes visible and fixable — which is the point.

### 8.5 Rules

- **A section declares its surface.** Every `<section>` carries `.surface-dark` or `.surface-light` and never sets `background-color` directly. This is repeated here because it is the rule that keeps §8 and §9 from defeating the gold constraint: a cream band authored as `background-color: var(--color-bg-secondary)` inherits `--focus-ring: var(--focus-ring-on-dark)` from `:root` (tokens line 304) and puts a 1.55:1 gold focus ring on cream.
- **No page-level `overflow: hidden`.** Overflow is a defect to fix at its source. The one element that can legitimately extend past its box is the rotated script block (line 91, `transform: rotate(-8deg)`), which takes `overflow: clip` on its own container if it needs it — never on the page.
- **Containers do not nest.** One `.container` per band. A nested container inherits `--gutter` twice and silently doubles the inline padding.
- **Full-bleed media inside a constrained band** breaks out with a dedicated utility, not by unsetting `max-width` on the container.
- **Only `--container-standard` is exposed to the Theme Editor** (tokens line 412). `--container-wide` and `--container-narrow` stay developer-owned, so a merchant cannot put the long-form reading width and the editorial width out of relation.

## 9. Grid System

The prototype carries twelve `grid-template-columns` declarations and no grid system (Phase 1 §5.6): five section grids, each inventing its own fr ratio — hero `minmax(0,1.1fr) minmax(0,1.1fr) minmax(0,.7fr)` (line 64), New Drop `minmax(240px,.9fr) minmax(0,2.4fr)` (line 98), products `repeat(3,minmax(0,1fr))` (line 106), story `minmax(260px,.9fr) minmax(0,1.6fr) minmax(170px,.4fr)` (line 125), values `repeat(4,minmax(0,1fr))` (line 142) — plus seven collapse overrides inside the two `max-width` queries (lines 20, 33-35, 40, 47-48).

### 9.1 The twelve-column base

```css
.grid-12 {
  display: grid;
  grid-template-columns: repeat(var(--grid-columns), minmax(0, 1fr));
  gap: var(--grid-gap);
}
```

`--grid-columns` is 12 (tokens 228), `--grid-gap` is `--space-5` 24px (229) and `--grid-gap-large` is `--space-6` 32px (230). Twelve because it divides by 2, 3, 4 and 6, which covers every layout spec §12 names without a remainder.

Twelve columns is a base, not a mandate. Spec §12 says "Do not force every section into the same grid," and most God Squad sections will not use `.grid-12` at all — they will use a named split or the product ladder. The base exists so that an asymmetric editorial composition has a common reference when one is needed, not so that every band is measured in twelfths.

### 9.2 The reusable 1 / 2 / 3 / 4 column grid

For content that is not products — a values strip, a three-up editorial row, a footer link matrix, a two-up image pair.

```css
.grid--1, .grid--2, .grid--3, .grid--4 {
  display: grid;
  gap: var(--grid-gap);              /* --grid-gap-large for whole-block grids */
}
.grid--1 { grid-template-columns: minmax(0, 1fr); }
.grid--2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.grid--3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.grid--4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
```

`--grid-gap` 24px for grids of content inside a band; `--grid-gap-large` 32px when the cells are whole blocks with their own internal padding.

Collapse ladder:

| Grid | ≥ `--bp-lg` 1024 | `--bp-md` 768-1023 | < 768 |
|---|---|---|---|
| `.grid--4` | 4 | 2 | 2 |
| `.grid--3` | 3 | 3 | 1 |
| `.grid--2` | 2 | 2 | 1 |

**A four-column grid never collapses to one.** Four items in a single column is a list, not a strip, and it is what the prototype does to the values band at ≤520 (line 48) — four full-width rows that lose the band's horizontal read entirely. 4→2 keeps it.

Where a three-up carries media rather than an icon and two tracked lines, use the product ladder in §9.3 instead: at 768 a `.grid--3` cell is (704 − 48) / 3 = 219px, which is enough for a 44px icon and a label and not enough for a photograph.

### 9.3 The product grid

Spec §12 asks for up to four desktop columns, two to three on tablet and one to two on mobile. The mechanism is `repeat(auto-fill, minmax(<min>, 1fr))` rather than a fixed count per breakpoint: `auto-fill` derives the count from the available track, so the grid has no gap between breakpoints to fail in — which is precisely where RESP-08 lives.

`auto-fill` and `auto-fit` differ only when the item count is below the track count: `auto-fill` holds the empty tracks so tiles keep a constant width across collections, `auto-fit` collapses them so a short collection stretches to fill the row. With a three-product catalogue the choice is visible, so it is recorded here as a decision for Phase 9 and tied to the catalogue-size item in §9.7 rather than settled now.

```css
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(var(--product-col-min), 1fr));
  gap: var(--product-grid-gap);
}
```

**Recommendation, not an existing token:** the token file defines no track minimum. `--product-col-min: 17rem` (272px, on the 4px grid) is the value that produces the ladder below; it should be added to the file rather than written inline. Recorded as a token gap.

Derived ladder, with `--product-grid-gap` at its shipped `--space-5` 24px (tokens 231) and the gutter ladder from §8.3:

| Viewport | Gutter | Content box | Columns | Tile |
|---|---|---|---|---|
| 375 | 24 | 327 | 1 | 327 |
| 390 | 24 | 342 | 1 | 342 |
| 430 | 24 | 382 | 1 | 382 |
| **616** | 24 | 568 | **2** | 272 — the 1→2 threshold |
| 768 | 32 | 704 | 2 | 340 |
| **928** | 32 | 864 | **3** | 272 — the 2→3 threshold |
| 1024 | 48 | 928 | 3 | 293 |
| **1256** | 48 | 1160 | **4** | 272 — the 3→4 threshold |
| 1280 | 48 | 1184 | 4 | 278 |
| 1440 | 48 | 1344 | 4 | 318 |
| 1920 | 48 | 1344 (capped) | 4 | 318 |

Four things follow.

**The container caps the grid at four columns without a rule saying so.** A fifth column needs 1456px of content; `--container-standard` caps content at 1344px. Spec §12's "up to four" is enforced by §8, not by a media query.

**Three columns at 1024, not four.** Four columns at 1024 would produce 214px tiles — narrower still than the ~230-250px three-column tiles Phase 1 measured in the 901-1100 band, where the eyebrow, the product names and `View All Products` all wrap (RESP-08). Three columns at 1024 give 293px, comfortably clear of it.

**The third column arrives at 928, above the failure band.** The prototype puts three columns on screen from 901px and squeezes them to ~230px. A 272px track minimum makes the third column impossible below 928px, which retires RESP-08 by construction rather than by adding a tier.

**If the gap discrepancy resolves upward, the ladder shifts and the cap holds.** With `--product-grid-gap` at `--space-6` 32px (the value the normalisation comment implies, tokens line 189) the thresholds move to 624, 944 and 1280, the tile minimum stays 272px, and five columns remain impossible.

**The New Drop needs no second grid.** On the homepage the grid sits in the right track of `--split-30-70` (line 98). At 1440, that track is roughly 954px, which the same expression resolves to three columns at ~302px — three beside the copy rail, four on a collection page, one mechanism.

### 9.4 Editorial splits

| Layout | Token | Value | Rendered ratio | Source | Use |
|---|---|---|---|---|---|
| 50/50 | `--split-50-50` | `1fr 1fr` | 50/50 | derived (tokens 234) | Image and copy of equal weight |
| 40/60 | `--split-40-60` | `0.9fr 1.6fr` | 36/64 | story, line 125 (tokens 235) | Copy left, image right |
| 60/40 | `--split-60-40` | `1.6fr 0.9fr` | 64/36 | mirror (tokens 236) | Image left, copy right |
| 30/70 | `--split-30-70` | `0.9fr 2.4fr` | 27/73 | New Drop, line 98 (tokens 237) | Narrow copy rail beside a product grid |
| Full-width | — | 100% | — | derived | A single track inside `--container-standard`, or a `.section` with no `.container` where the content is edge-to-edge imagery |

Full-width is the fourth editorial layout spec §12 names, not the absence of one. A hero image that bleeds to both viewport edges is a deliberate layout choice with its own rules — it takes `--section-pad-block` for rhythm, no container, and the surface class still applies.

The token names state intent; the values state the prototype's measured ratio. `--split-40-60` renders 36/64 because it is taken from the story's first two tracks (line 125). The story's third track, `minmax(170px,.4fr)`, is a side rail the token does not carry; §9.5 records it as a three-track case rather than inventing a fifth token for it.

Used as `grid-template-columns: var(--split-40-60)`. Splits collapse to one track below `--bp-md` 768px, in DOM order: copy first, media second. Sections may collapse later than that but never earlier.

### 9.5 Section by section

| Section | Prototype | Phase 2 grid | Collapse |
|---|---|---|---|
| Hero | `minmax(0,1.1fr) minmax(0,1.1fr) minmax(0,.7fr)` (line 64) | Three-track asymmetric: copy rail, open image field, script rail. Not a `--split-*` token — the middle track is deliberately empty and is the composition | 1 track below `--bp-md`; the prototype collapses at ≤900 (line 20) |
| New Drop | `minmax(240px,.9fr) minmax(0,2.4fr)` (line 98) | `--split-30-70`, right track carrying `.product-grid` | 1 track below `--bp-md` (line 33) |
| Products | `repeat(3,minmax(0,1fr))` (line 106) | `.product-grid`, §9.3 | derived from the track minimum, not declared |
| Story | `minmax(260px,.9fr) minmax(0,1.6fr) minmax(170px,.4fr)` (line 125) | `--split-40-60` plus a third side-rail track | 1 track below `--bp-md` (line 35) |
| Values | `repeat(4,minmax(0,1fr))` (line 142) | `.grid--4` | 2 at `--bp-md`, never 1; the prototype drops to 1 at ≤520 (line 48) |
| Footer | flex row, `gap:32px` (line 153) | Flex row, not a grid; groups wrap | Stacks below `--bp-md` 768px, where Phase 1 shows both groups (230 + 271px) still fit the content box (RESP-06) |

The footer stacking width is deliberately tied to `--bp-md` rather than to a measured number. A stacking point at, say, 560px would be a sixth breakpoint outside `--bp-sm` 480 and `--bp-md` 768 (tokens lines 246-247), unwritable from a token and exactly the per-section invention §9.6 exists to prevent. If Phase 9 measures the real footer content and finds 768 wrong, it moves the token-anchored value and says so.

### 9.6 Rules

- **Every track is declared through `minmax()` with an explicit minimum** rather than a bare `1fr` — `minmax(0, …)` where the track may shrink freely (lines 64, 106, 142) and a px floor where it must not (`minmax(240px,.9fr)` line 98; `minmax(260px,.9fr)` and `minmax(170px,.4fr)` line 125). The prototype already learned that a bare `1fr` has an `auto` minimum and lets its content force overflow.
- **Not every section uses the same grid** (spec §12). A section chooses from: `.grid-12`, `.grid--1/2/3/4`, a `--split-*`, `.product-grid`, or full-width. It does not write a new ratio.
- **Gaps come from tokens only** — `--grid-gap`, `--grid-gap-large`, `--product-grid-gap`. A section may not invent a gap, which is how the prototype ended up with 20, 32, 36 and 40px gaps in four adjacent bands (lines 34, 33, 106, 98).
- **`gap`, never margins between grid children.**
- **DOM order is reading order.** Do not reorder tracks with `order` or explicit `grid-row` in a way that separates the visual sequence from the tab sequence.
- **A grid never sets its own `max-width`.** It inherits the container from §8, and it sits inside a section that carries `.surface-dark` or `.surface-light` — the §8.1 surface requirement applies to every grid section without exception.

### 9.7 Open items

- **Catalogue size.** Three products today, which is why the cap orphans onto row 2 at 768 (brief: measured responsive behaviour). It decides `auto-fill` versus `auto-fit` and whether a four-column row ever fills. **BUSINESS INFORMATION REQUIRED.**
- **Whether the New Drop keeps its copy rail** when a collection page runs four columns. **BUSINESS INFORMATION REQUIRED.**
- **Support matrix** for `aspect-ratio` — which `--product-aspect` 1/1 (tokens 335) depends on — and for `:has()` and container queries, which would let the product ladder respond to its track rather than the viewport. **BUSINESS INFORMATION REQUIRED.**

## 10. Button System

The prototype contains zero `<button>`, `<input>`, `<select>`, `<textarea>` and `<form>` elements (verified across the whole file). Its two calls to action are anchors styled as buttons: View All Products (line 104) and Our Story (line 132). Phase 2 defines the button system; it does not change them. The existing runtime hover values are the starting point for every rule below.

### 10.1 The four variants and the surface each lives on

| Variant | Surface | Fill | Label | Border | Prototype precedent |
|---|---|---|---|---|---|
| Primary | `.surface-light` | `--color-bg-primary` | `--color-text-primary` (17.04:1) | none | line 104 `background:#0d0c0a;color:#f3efe6` |
| Primary | `.surface-dark` | `--color-text-primary` | `--color-text-inverse` (17.04:1) | none | derived; no precedent |
| Secondary | either | transparent | `currentColor` | `--border-width` solid, 3:1 minimum (§10.2) | derived; no precedent |
| Accent | `.surface-dark` only | `--color-accent` | `--color-text-inverse` (11.01:1) | none | line 132 `background:#d8c08a;color:#0d0c0a` |
| Text link CTA | either | none | see §11.4 | none (underline instead) | — |

The accent button is prohibited on `.surface-light`. The ink label on gold is 11.01:1 and would pass, but the button's own boundary is gold against cream at 1.55:1 (brief: contrast matrix) — below the 3:1 that WCAG 2.2 SC 1.4.11 requires for the visual boundary of a control, so the button edge disappears into the band. On a light surface the accent expression is a text link in `--color-accent-strong` (4.66:1), never a gold fill.

The text-link CTA is listed here only so all four variants the spec names (spec §13) are accounted for; its states are defined in §11.4.

### 10.2 Variant semantics

One primary per band, at most. The primary carries the band's single most important action; everything else is secondary or a text link. Primary is the inverse of its surface — `--color-bg-primary` on `.surface-light`, `--color-text-primary` on `.surface-dark` — so it reads as a solid block cut out of the band.

Secondary's border must clear 3:1 against its surface, which `--color-border-current` does not: `--color-border` is 1.32:1 on ink and `--color-border-inverse` is 1.35:1 on cream (computed, §15.2). Until an interactive-border token exists (token gap), Secondary borders use `--color-text-inverse-muted` (5.97:1) on light and `--color-text-muted` (9.70:1) on dark.

Components reference the semantic tokens, never the raw palette — the token file states the rule at §2 ("Components must reference these, never the raw palette above", line 56). `--gs-ink` is a palette token and a `[THEME SETTING]`; using it as a component fill would move a button whenever a merchant changed the brand black.

### 10.3 State matrix

The governing model: **hover lifts one step, active drops the lift, focus adds a ring without changing the fill.**

| Variant / surface | Default | Hover | Focus-visible | Active | Disabled |
|---|---|---|---|---|---|
| Primary / `.surface-light` | fill `--color-bg-primary`, label `--color-text-primary` | fill `--color-surface-raised` (#2A2823, runtime `.scp0:hover`, line 104), label unchanged — 12.83:1 (computed) | default + ring `--focus-ring` | fill returns to `--color-bg-primary` | `opacity:.45`, `aria-disabled="true"` |
| Primary / `.surface-dark` | fill `--color-text-primary`, label `--color-text-inverse` | fill `--color-text-secondary` (`--gs-cream-200` #E9E4D8), label unchanged — 15.41:1 | default + ring `--focus-ring` | fill returns to `--color-text-primary` | as above |
| Secondary / `.surface-light` | transparent, label `--color-text-inverse`, border 3:1 (§10.2) | fill `--color-border-inverse` as a 14% ink wash, label unchanged — 12.60:1 (computed) | default + ring `--focus-ring` | fill returns to transparent | as above |
| Secondary / `.surface-dark` | transparent, label `--color-text-primary`, border 3:1 (§10.2) | fill `--color-border` as a 12% cream wash, label unchanged — 12.96:1 (computed) | default + ring `--focus-ring` | fill returns to transparent | as above |
| Accent / `.surface-dark` | fill `--color-accent`, label `--color-text-inverse` | fill `--color-accent-hover` (#E6D3A6, runtime `.scp1:hover`, line 132) — 13.25:1 | default + ring `--focus-ring` | fill returns to `--color-accent` | as above |

**Primary and Accent must never share a hover fill.** Gold belongs to the Accent variant alone; a cream Primary that turns gold on hover collapses the two variants into one and makes gold the dominant UI colour, which spec §6 rules out ("Avoid gold buttons everywhere").

The matrix names `--focus-ring` only; `.surface-dark` resolves it to `--focus-ring-on-dark` (gold, 11.01:1 on ink) and `.surface-light` to `--focus-ring-on-light` (ink, 17.04:1 on cream). A button copied onto the other band therefore carries the correct ring without editing.

The token file already supplies `outline: var(--focus-width) solid var(--focus-ring)` at `var(--focus-offset)`, written as `:where(a, button, input, select, textarea, summary, [tabindex]):focus-visible`. `:where()` contributes zero specificity, so any component-level `outline` declaration wins silently. Buttons must not declare `outline` at all; a review check for `outline:` inside component CSS belongs in the Phase 2 QA checklist.

Disabled styling is exempt from SC 1.4.3, but opacity alone does not say *why* a control is unavailable. A disabled button always pairs with a reason in text (for example a sold-out line), stays in the tab order via `aria-disabled` where the reason must be announced, and is never hidden.

### 10.4 Geometry and target size

| Property | Value | Source |
|---|---|---|
| Block padding | `--space-4` 16px | lines 104/132 `padding:16px 26px` |
| Inline padding | `--space-5` 24px | 26 → 24 per the token file's normalisation map (line 189) |
| Minimum block size | `--target-min` 44px | token file §13 |
| Label type | `--type-label-size` 12px / `--type-label-ls` .22em / `--type-label-weight` 600 | lines 104 (w500) and 132 (w600) settle on 600 |
| Icon gap | `--space-3` 12px | lines 104/132 `gap:12px` |
| Radius | `--radius-sm` 2px | §16; the only `[THEME SETTING]` radius |
| Shadow | `--shadow-none` | §17 |

Full-width buttons are permitted on mobile only where the button is the sole action in a stacked block; never in the header, never in a product card row.

Both CTAs append a literal arrow, `<span>→</span>` (lines 104, 132). Jost contains neither `→` (U+2192) nor `₱` (U+20B1), so both fall back to a per-platform face (brief). The rule: trailing affordances are inline SVG in `currentColor` at `--icon-sm` 16px with `aria-hidden="true"`, not glyphs. A webfont carrying both codepoints, or the SVG substitution, is **BUSINESS INFORMATION REQUIRED**.

### 10.5 What buttons must not do

No pill buttons by default — `--radius-full` is for circles only (§16.3). No gradients, no shadows, no gold fill on a light surface, no more than one primary per band. No icon-only button without an accessible name. No `<div>` or `<span>` acting as a button: an anchor navigates, a `<button>` acts, and add-to-bag is a `<button>` even though the prototype's CTAs are anchors. No `transform: scale()` on press. Uppercase labels stay at three words or fewer — at `--type-label-ls` .22em a longer uppercase string stops being readable as a phrase.

### 10.6 Motion

Every button state change transitions on `--transition-fast` (150ms `--ease-standard`), and only `background-color`, `color`, `border-color` and `opacity` transition — never `width`, `padding` or `transform`. Under `prefers-reduced-motion` the token file collapses `--duration-fast` to 1ms, so the change is instant but never absent.

## 11. Link System

The prototype contains nine links: five navigation items, two CTAs (lines 104, 132) and two social icons (lines 160–161). A single global reset governs all nine, and both rules sit on one line (line 16):

```css
a{color:inherit;text-decoration:none}a:hover{color:#d8c08a}
```

Three consequences follow, and all three are defects the link system must close.

**Defect 1 — the hover colour is not surface-aware.** The New Drop band is cream, so any link hovered there drops to 1.55:1. The defect is latent rather than live only because the band's single link (line 104) carries its own `style-hover`, which the runtime compiles to `.scp0:hover` and which outranks `a:hover` on specificity — (0,2,0) against (0,1,1). The first link added to that band without a bespoke hover inherits the failure.

**Defect 2 — `color:inherit` plus no underline removes every non-colour cue.** An inline link inside a paragraph would be indistinguishable from its surrounding text, which fails SC 1.4.1. The failure is latent because the file's only `<p>` (line 131) contains no links.

**Defect 3 — the current page's hover is invisible.** Home is already `#d8c08a` (line 71), so `a:hover` changes nothing on it.

### 11.1 The five link classes

| Class | Type | Rest colour | Underline at rest | Target |
|---|---|---|---|---|
| Navigation | `--type-label-size` 12px / `--type-label-ls` .22em / 500 (line 70) | `--color-text-primary` | no | `--target-min` 44px |
| Body / inline | `--type-body-size` 16px | `--accent-current` | **yes, always** | inline exception (§11.7) |
| Editorial | `--type-label-size` / `--type-label-ls` | inherits band text | no; gains one on hover | `--target-min` |
| Product | `--type-label-size` / `--type-label-ls` / 600 (line 112) | inherits band text | no; gains one on hover | the whole card |
| Footer | `--type-caption-size` 12px / `--type-caption-ls` .20em | `--color-text-muted` (9.70:1) | no | `--target-min` |

### 11.2 Navigation links

| State | Rule |
|---|---|
| Default | `--color-text-primary` on dark, `--color-text-inverse` on light |
| Hover | `--accent-current` — gold (11.01:1) on `.surface-dark`, `--color-accent-strong` (4.66:1) on `.surface-light`. This replaces the global `a:hover{color:#d8c08a}` and is the reason `--accent-current` exists |
| Focus-visible | `--focus-ring`, resolved by the surface class; the colour never changes on focus |
| Active (pressed) | `--color-accent-hover` (13.25:1) on dark; `--color-text-inverse` (17.04:1) on light, i.e. back to full ink |

Current page carries `aria-current="page"` plus the existing marker: `border-bottom: 1px solid` in `--color-border-strong` at `--space-1` 4px offset (line 71 uses `padding-bottom:4px`). The underline stays because the marker must not be colour-only — and because it is what makes Home's state visible at all once the hover colour moves off gold (defect 3).

### 11.3 Body and inline links

Underline is **required**, at rest and in every state. This is the accessibility rule the global reset breaks: inside a run of text, colour alone is not a sufficient cue (SC 1.4.1).

| State | Rule |
|---|---|
| Default | colour `--accent-current`; `text-decoration: underline`; thickness 1px; `text-underline-offset: 0.2em`; `text-decoration-skip-ink: auto` |
| Hover | thickness 2px (a literal until `--link-underline-thickness` exists — `--border-width-strong` is a BORDERS token, not a `text-decoration-thickness` value); colour unchanged |
| Focus-visible | `--focus-ring`; underline unchanged |
| Active | colour `--color-accent-hover` on dark, `--color-text-inverse` on light |

### 11.4 Editorial links (standalone text CTAs)

Standing alone rather than inside a text run, these may rest without an underline, but they must gain one on hover and they always take the focus ring.

| State | Rule |
|---|---|
| Default | inherits band text colour; `--type-label-size` / `--type-label-ls`; trailing inline-SVG arrow, `aria-hidden="true"`, `--icon-sm` |
| Hover | `text-decoration: underline` 1px at 0.2em offset; arrow may translate a maximum of 2px on X |
| Focus-visible | `--focus-ring` |
| Active | arrow translation returns to 0 |

### 11.5 Product links

Lines 107–118 contain no `<a>` at all — nothing in the current product card is clickable. The rule: one anchor per card, wrapping the media and the title, with no other interactive element nested inside it (swatches sit outside the anchor, §13.6).

| State | Rule |
|---|---|
| Default | title inherits band text; media at rest |
| Hover | title gains a 1px underline; media scales to `--hover-image-scale` 1.03 over `--transition-medium` inside an `overflow:hidden` wrapper (§14.3) |
| Focus-visible | `--focus-ring` around the whole card, not just the title |
| Active | scale returns to 1 |

### 11.6 Footer links

Rest at `--color-text-muted` (#BDB6A8, 9.70:1 on ink); hover to `--color-text-primary`, **not** to gold — a footer of gold links makes the accent the dominant colour and breaks restraint (spec §6).

The two social links already carry `aria-label="Facebook"` and `aria-label="Instagram"` (lines 160–161) — correct. They are two of only three `aria-` attributes in the entire file; the third, `aria-label="Menu"` on a role-less `<span>` (line 75), names nothing operable. The social links carry both an `aria-label` and a duplicate `alt` on the child image, which double-announces; one of the two is removed in a later phase.

Social icon links have no hover at all today (brief). Their defined hover is a colour change, which requires `currentColor` — unavailable while the icons are PNG (lines 160–161), so the rule is conditional on the SVG migration (§14.1, rule 8). Until then, `opacity` .7 → 1 over `--transition-fast`.

### 11.7 Rules that apply to all links

- Every link state change transitions on `--transition-fast` (150ms `--ease-standard`), and only `color`, `text-decoration-color`, `border-color` and `opacity` transition — never `text-decoration-thickness` or `padding`, which reflow the line. Under `prefers-reduced-motion` the token file collapses `--duration-fast` to 1ms, so the change is instant but never absent.
- Standalone links meet `--target-min` 44px. Links inside a run of text take SC 2.5.8's inline exception, but the run stays at `--type-body-lh` 1.65 so adjacent lines do not collide.
- Never `outline: none` without substituting an equally visible ring (spec §27); the global `:where()` rule already supplies one and must not be overridden (§10.3).
- Never distinguish a link by colour alone.
- Link text must be meaningful out of context: no "click here", and never a bare arrow as the whole accessible name.
- The global `a:hover{color:#d8c08a}` is replaced by `--accent-current` in a later phase; any interim rule must stay surface-aware.

### 11.8 Token gaps in this section

`--link-underline-thickness` and `--link-underline-offset` do not exist, so §11.3's 1px → 2px underline and the 0.2em offset are literals.

## 12. Form System

The prototype has zero form elements — no `<form>`, `<input>`, `<select>`, `<textarea>` or `<button>` anywhere in the file. This section is therefore wholly forward-looking: it changes nothing, and every value below is derived from the token file rather than measured from the source.

### 12.1 Where forms will live, and which surface governs

| Form | Surface | Phase |
|---|---|---|
| Newsletter (footer) | `.surface-dark` | later |
| Contact | `.surface-light` | later |
| Search (from the header icon, lines 76–78) | `.surface-dark` | later |
| Customer account | `.surface-light` | later |
| Product options / quantity | `.surface-light` | later |

The surface class resolves `--color-border-current`, `--accent-current` and `--focus-ring`; no form rule below names a surface-specific colour directly.

### 12.2 Field anatomy and geometry

| Property | Value | Rationale |
|---|---|---|
| Minimum height | `--target-min` 44px (48px preferred) | token file §13 |
| Inline padding | `--space-3` 12px | |
| Radius | `--radius-sm` 2px | the `[THEME SETTING]` radius (§16.4) |
| Border width | `--border-width` 1px | §15.1 |
| Value type | `--type-body-size` 1rem | 16px also prevents iOS zoom-on-focus |
| Label | `--type-label-size` 12px / `--type-label-ls` .22em / 600, above the field at `--space-2` 8px | |
| Help text | `--type-body-sm-size` 14px, below the field at `--space-2` | |
| Error text | 14px, below the field at `--space-2`, linked by `aria-describedby` | |
| Shadow | `--shadow-none` | §17.2 |

**The border tokens cannot carry a field boundary.** `--color-border` composites to 1.32:1 on ink and `--color-border-inverse` to 1.35:1 on cream (computed). SC 1.4.11 requires 3:1 for the visual boundary of a control, so fields must not use `--color-border-current`. Until an interactive-border token exists, field borders use `--color-text-inverse-muted` (#5F5A50, 5.97:1) on `.surface-light` and `--color-text-muted` (#BDB6A8, 9.70:1) on `.surface-dark`. `--color-border-interactive` / `--color-border-interactive-inverse` are recommended additions.

One collision to record: `--color-warning` and `--color-accent-strong` are the same hex, #82672B (token file lines 79, 91). On cream, an accent-bordered control and a warning-bordered control would be identical. Warning is therefore carried by an icon plus text, never by border colour alone.

### 12.3 State matrix (all field types)

| State | Border | Fill | Value / label | Announcement |
|---|---|---|---|---|
| Default | 3:1 token per §12.2 | transparent | label full contrast, value `--color-text-inverse` / `--color-text-primary` | — |
| Hover | same border, no change of width | transparent | unchanged | — |
| Focus-visible | unchanged — the border never turns gold (1.55:1 on cream) | transparent | unchanged | outline `--focus-width` 2px at `--focus-offset` 2px in `--focus-ring`, from the global `:where()` rule |
| Filled | unchanged | transparent | value at full contrast; the label stays visible above (never a placeholder) | — |
| Error | `--color-error` (6.39:1 on cream) / `--color-error-on-dark` (7.43:1 on ink) | transparent | value unchanged | `aria-invalid="true"` plus a 14px message below, referenced by `aria-describedby`, text plus a 16px `--icon-sm` mark — never colour alone |
| Success | `--color-success` (8.57:1 on cream) / `--color-success-on-dark` (6.98:1 on ink) | transparent | label unchanged; value at full contrast | `aria-describedby` pointing at a confirmation message that is text plus a 16px `--icon-sm` mark, never colour alone; the state clears on re-edit |
| Disabled | same token at `opacity:.45` | transparent | `opacity:.45`, `cursor:not-allowed` | `aria-disabled="true"` plus a textual reason |

Success applies only after a field has passed validation following an error, so a fresh form is not a wall of green.

Validation timing: on blur for the first pass, then on input once a field has errored. Never on every keystroke of a first attempt. Multi-field forms carry an error summary at the top of the form linking to each failing field. Error text is never italic, never placeholder-only, and never the only indication of what went wrong.

### 12.4 Per-control rules

**Text.** `autocomplete` always set (`name`, `given-name`, `address-line1`). The address field set and its ordering for the Philippine market, and whether Shopify's own address localisation is used instead, are **BUSINESS INFORMATION REQUIRED**.

**Email.** `type="email"`, `inputmode="email"`, `autocomplete="email"`. The newsletter is one field plus one button on a single line at desktop and stacked on mobile — never a modal, never a multi-step capture. Consent copy and the provider are **BUSINESS INFORMATION REQUIRED**.

**Select.** Native `<select>`; no JavaScript dropdown library (spec §36). The chevron is an inline SVG in `currentColor` at `--icon-sm` 16px; `appearance:none` is permitted only where the replacement keeps native keyboard behaviour. A select is never used for colour variants — those are radios (§13.3).

**Checkbox and radio.** 20px visual control inside a `--target-min-aa` 24px hit area, raised to `--target-min` 44px wherever the whole row is tappable. The label is a real `<label for>` and is itself clickable. A custom control keeps the native input in the DOM at `opacity:0` (never `display:none`) so it stays focusable. The checked mark must clear 3:1 against the control's fill: gold fails on cream, so on `.surface-light` the mark is `--color-text-inverse` and the box fill carries the state.

**Textarea.** Minimum five lines — `min-height: calc(5 * var(--type-body-size) * var(--type-body-lh))` ≈ 132px, plus the field's own padding. No spacing token lands on this value; do not substitute `--space-10`. `resize: vertical` only.

**Quantity selector.** Three parts: a minus `<button>`, an `<input type="number" inputmode="numeric">`, a plus `<button>`. Each button meets `--target-min` 44px; the value is `--type-body-size` 16px, centred. Changes debounce 250ms (a literal, not `--duration-medium` — a motion token collapses to 1ms under `prefers-reduced-motion` and would remove the debounce) before any cart update, and the new quantity is announced in a live region. Minimum 1. The upper bound, stock behaviour and back-order policy are **BUSINESS INFORMATION REQUIRED**.

**Search input.** `type="search"` on a native input, opened from the header search icon (`--icon-md` 24px, lines 76–78). Full width at mobile. A placeholder is not a label: a visually hidden `<label>` is always present. Only the field is defined here; the results surface belongs to a later phase. Search scope — products only, or products plus pages and journal — is **BUSINESS INFORMATION REQUIRED**.

### 12.5 Form layout

Single column. `--space-5` 24px between fields, `--space-6` 32px between field groups, `--space-6` above the submit button. A standalone form is capped at `--container-narrow` 760px and runs to the `--gutter` at mobile. Labels sit above their fields; no left-aligned label column, no placeholder-as-label, no two-up field rows except a city/postcode pair once the address set is settled.

### 12.6 What forms must not do

No placeholder-only labels. No error signalled by colour alone. No blocking validation on the first keystroke. No image-only CAPTCHA. No custom dropdown library. No `autofocus` on page load. No `outline:none`. No gold borders on a light surface. No shadow on any field (§17.2).

## 13. Product Card System

### 13.1 Measured structure and its Phase 2 tokens

| Part | Prototype value | Phase 2 token |
|---|---|---|
| Media | `aspect-ratio:1/1`, `background:#ebe6dc` (109) | `--product-aspect`, `--color-surface-tile` |
| Image | `object-fit:cover` (110) | unchanged, plus intrinsic `width`/`height` (§14.1) |
| Title | 12px, `.2em`, uppercase, w600, `margin-top:14px` (112) | `--type-label-size` / `--type-label-ls` .22em / `--type-label-weight` 600; `--space-4` 16px (14 → 16 per the file's normalisation map, line 189) |
| Price | 14px w600, `margin-top:6px` (113) | `--type-price-size` 15px / `--type-price-weight` 600 / `--type-price-ls` 0; `--space-2` 8px (6 → 8) |
| Swatch row | `gap:10px`, `margin-top:14px` (115) | `--space-2` 8px; `--space-4` 16px |
| Swatch | 16px circle, `border-radius:50%`, `border:1px solid rgba(0,0,0,.25)` (116) | 20px visual in a 24px target, `--radius-full`, ring per §13.3 |
| Grid gap | `36px` (106) | see below |
| Columns | 3 desktop (106), 2 at ≤900 with `gap:20px` (line 34), 1 at ≤520 (line 47) | §13.9 |

The token file maps the measured 36px to `--grid-gap-large` 32px (its own comment on that token) and sets `--product-grid-gap` to `--space-5` 24px for the standalone catalogue grid. Both are correct for different contexts: 24px for a full-width 4-up grid, 32px for the 3-up row beside the New Drop copy column (`--split-30-70`, line 98).

One structural defect to record: lines 107–118 contain no `<a>`. Nothing in the current card is clickable. §11.5 requires exactly one anchor per card.

### 13.2 The closed part list

**Required, in this order:** media → title → price → swatches (when the product has more than one colourway).

Three parts are unconditional — media, title, price. Swatches are required whenever a product has more than one colourway, which today is all three products (lines 175–177). The list is closed: a fourth unconditional part would have to survive being multiplied across an entire catalogue, and nothing in the current three-product grid earns that.

**Conditional parts:** one badge, overlaid on the media (§13.4); one quick action, below the price (§13.7). Both default to off.

### 13.3 Swatches

All three products carry the cream `#f3efe6` colourway (lines 175–177), and the hoodie lists it first, so an almost-invisible circle is the leading swatch of that row. The ring that is meant to save it does not: `rgba(0,0,0,.25)` composites to **1.82:1 on the cream band and 1.81:1 on the tile** (computed), well below the 3:1 SC 1.4.11 requires for the boundary of a control.

| Property | Rule |
|---|---|
| Size | 20px visual circle inside a 24px hit area (`--target-min-aa`), which satisfies WCAG 2.2 SC 2.5.8 on its own — no spacing exception is invoked — with `--space-2` 8px between adjacent targets. 44px per swatch is not workable in a three-up row on a phone, which is why the AA minimum rather than `--target-min` governs here |
| Ring | a token clearing 3:1 on its surface: `--color-text-inverse-muted` (5.97:1) on light, `--color-text-muted` (9.70:1) on dark, until an interactive-border token exists (§15.2) |
| Radius | `--radius-full` — the one legitimate use (§16.3) |
| Markup | `<input type="radio">` inside a `<fieldset>` with a `<legend>`, one group per product |
| Accessible name | each swatch needs an accessible name: the colourway's name as visually hidden label text. A hex value is not a name, and colour is never the name |
| Selected | a 2px ring (`--border-width-strong`) offset 2px, plus the native checked state — never colour alone |

Colourway names are **BUSINESS INFORMATION REQUIRED**; the data carries hex only (lines 175–177).

Note for the token file: the `--gs-olive` comment cites "data line 179"; the swatch data is on lines 175–177 and line 179 is `values: [`. Correct the comment when the file moves to `assets/design-tokens.css`.

### 13.4 Badge

At most one badge per card, overlaid on the media, top-left, inset `--space-3` 12px. Type `--type-caption-size` 12px / `--type-caption-ls` .20em. Fill `--color-bg-primary`, label `--color-text-primary`, so the badge never depends on the photograph behind it. Radius `--radius-none`.

A badge states a stock or catalogue fact the customer can verify — sold out, for example — never a marketing adjective and never a scarcity phrase (§13.5 bans low-stock urgency, and a badge is not a way around that rule). The permitted badge vocabulary and the condition that fires each one are **BUSINESS INFORMATION REQUIRED**.

A sold-out card also carries the state in its accessible name and dims its media to `opacity:.6` — the opacity is the secondary cue, never the only one.

### 13.5 What must not be added

Star ratings or review counts. A second badge. Stacked buttons. Countdown timers, "only 2 left" urgency strips or any low-stock messaging. Wishlist hearts. A "+3 colours" line duplicating the swatch row. Shadows (§17.2). Rounded card corners (§16.2). Hover panels revealing extra copy. Compare checkboxes. Vendor names while the catalogue is single-brand.

### 13.6 Desktop versus touch

| Part | Desktop (`hover: hover` and `pointer: fine`) | Touch |
|---|---|---|
| Media | scales to `--hover-image-scale` 1.03 over `--transition-medium` inside `overflow:hidden` | no scale; the media is the tap target |
| Title | gains a 1px underline on hover | no underline; the card is one link |
| Price | unchanged | unchanged |
| Swatches | 20px visual in a 24px target, hover ring | 20px visual in a 24px target |
| Quick action | may reveal on hover or `focus-within` | always visible, or absent — never hover-only |
| Card affordance | one anchor wrapping media + title | same, with no nested interactive element inside the anchor |

Hover behaviour is gated on `@media (hover: hover) and (pointer: fine)`, never on viewport width — the prototype's only two queries are width-based (900 and 520), which is why a tablet with a pointer and a phone are treated identically today.

### 13.7 Quick action

Optional, off by default, and exposed as a section setting rather than a global one (§29). When on: a single `<button>` in the Secondary variant (§10.1), full card width, below the price at `--space-4`, never overlaying the media, never hover-only. A product with more than one variant routes to the product page rather than silently adding a default. Button copy, and whether quick add is wanted at all, are **BUSINESS INFORMATION REQUIRED**. The default stays off because the catalogue is three products deep and the editorial read is stronger without it.

### 13.8 Price and currency

`--type-price-size` 15px, `--type-price-weight` 600, `--type-price-ls` 0 — the one place the brand's uppercase tracking is switched off (line 113). Prices render as `₱1,290` from a `cur` variable (data lines 175–177). Jost contains no `₱` glyph (brief), so the peso sign falls back to a per-platform face and shifts the price's optical alignment across devices. The fix — a webfont carrying U+20B1, or a scoped fallback stack for currency — is **BUSINESS INFORMATION REQUIRED**.

No compare-at price styling is defined, because no such data exists. If one is ever introduced: the original price in `--color-text-inverse-muted` inside `<s>`, the current price at full contrast, and never red. Whether prices display tax-inclusive is **BUSINESS INFORMATION REQUIRED**.

### 13.9 Grid behaviour

| Viewport | Columns | Gap | Container |
|---|---|---|---|
| ≤520 | 1 today (line 47); 2 permitted for a catalogue grid (spec §12) | `--product-grid-gap` | `--gutter` |
| 521–900 | 2 (line 34) | `--product-grid-gap` | `--gutter` |
| 901–1440 | 3 (line 106) | `--grid-gap-large` beside a copy column | `--container-standard` |
| >1440 | up to 4 | `--product-grid-gap` | `--container-standard`, or `--container-wide` for a full-bleed editorial grid |

At 1024 the tee's name wraps to two lines and its price falls out of alignment with its neighbours (brief). The rule: the title is clamped to two lines and the price sits on its own grid row so prices align across the row regardless of title length. Whether this uses `subgrid` depends on the support matrix, which is **BUSINESS INFORMATION REQUIRED**.

## 14. Image System

The prototype declares three photographic `<img>` elements — the hero group shot (line 65), the story model (line 126) and one templated product image inside `sc-for` (line 110) — which render five photographs on the homepage from five files (`hero-group.png`, `01-hero-model-…webp`, `product-tee.webp`, `product-hoodie.webp`, `product-cap.webp`, lines 175–177). None of the file's twelve `<img>` elements carries `loading`, `fetchpriority`, `srcset`, `width` or `height`, and there is no `<picture>` (verified). Phase 2 defines the rules; none of it alters the existing markup, and no image is edited or replaced in this phase.

### 14.1 Rules that apply to every image

1. Intrinsic `width` and `height` attributes are always present, so the browser can reserve the box before the file arrives.
2. `alt` is either genuinely descriptive or explicitly empty. The value-tile icons already do this correctly with `alt=""` (line 145); the social links carry both an `aria-label` and a duplicate `alt` (lines 160–161), which double-announces and is reduced to one in a later phase.
3. `object-fit: cover` is the default; `contain` only where a product must not be cropped.
4. `object-position` is declared explicitly on any image whose subject is off-centre. The prototype already does this at line 65 (`center 30%`) and line 126 (`center top`), and both values are preserved.
5. Photographic images are WebP or AVIF. The hero is `hero-group.png` (line 65) — a PNG carrying a photograph — while the story image is already `.webp` (line 126). A later phase converts it; Phase 2 records the rule.
6. No image carries text that matters. Copy baked into a photograph cannot be translated, resized or read out.
7. A photograph that sits under text always carries a scrim token (§14.5), never an inline `rgba()` and never `filter: brightness()`.
8. Icons are specified to move from PNG to inline SVG in a later phase, so they can take `currentColor` and respond to state (§11.6).

### 14.2 Hero images

| Property | Rule | Source |
|---|---|---|
| Desktop height | the band's own `min-height: 620px`; the image fills it at `inset: 0` | line 64 |
| Mobile ratio | `--hero-aspect-mobile` 4/5, replacing the uncapped `height:62vw` | token file §15; prototype line 21 |
| `object-fit` | `cover` | line 65 |
| `object-position` | `center 30%` — keeps faces in frame | line 65 |
| Loading | `loading="eager"`, `fetchpriority="high"`, `decoding="async"` | the hero is the LCP element and must never be lazy |
| `sizes` | `100vw` with a width-based `srcset` | none exists today |
| Scrim | `--scrim-header` is mandatory on any hero with the navigation over it | token file lines 102–104; Phase 1 A11Y-03/HERO-02 measured three nav links at 2.4–2.9:1 over open sky |

Exactly one image per page may carry `fetchpriority="high"`.

The mobile fade defect is a scrim-ownership problem, and the rule that prevents it is structural: below 900px the fade is anchored to the section while the image sits below the 88px in-flow nav, so the gradient goes solid 88px above the image bottom — a black band and a hard seam at every phone and tablet width (brief). **A scrim is always a child of the media wrapper and sized to the media, never to the section.**

### 14.3 Product images

`--product-aspect` 1/1 (line 109) is the default and the recommended starting ratio (spec §24). `--product-aspect-wide` 4/5 is the documented exception for an editorial portrait crop, and the exception is set per section, never per card — a grid of mixed ratios is precisely what a fixed ratio protects against.

Ground colour `--color-surface-tile` (#EBE6DC, line 109) behind every product image, so a transparent or short file still lands on a deliberate surface. `object-fit: cover`, `object-position: center`. Hover scale `--hover-image-scale` 1.03 over `--transition-medium`, inside a wrapper with `overflow: hidden`; the token file caps this at 1.05 and `prefers-reduced-motion` resets it to 1.

Loading: `loading="lazy"` and `decoding="async"` for everything below the fold; the first row of a collection page loads eagerly. A second "back" photograph revealed on hover is permitted only if every product has one — a partial set makes the grid look broken — and whether the shoot delivers one is **BUSINESS INFORMATION REQUIRED**.

### 14.4 Story and editorial images

The story band is `min-height: 520px` (line 125) with the image at `left:30%; width:70%` and `object-position: center top` (line 126). Editorial splits use the `--split-*` tokens; the image takes the larger fraction, and the copy column is capped at `--container-narrow` 760px. The prototype caps its story paragraph at 320px (line 131), which is too narrow once body copy is `--type-body-size` 1rem — the measure target is 60–75 characters.

Art direction for the shoot brief, to be confirmed with whoever commissions the photography (**BUSINESS INFORMATION REQUIRED**): a single, consistent garment-to-frame ratio across the whole catalogue, centred, never cropped at a shoulder, cuff or hem. The value matters less than its consistency — a 4-up grid makes scale differences unmissable — but it must be fixed once and recorded here before the shoot.

Art direction for phones uses `<picture>` with a `media` switch, not a CSS re-crop. The prototype's approach of holding the desktop framing and shortening the box (`height:60vw`, line 36) keeps the landscape composition and loses the subject.

### 14.5 Scrims

| Token | Origin | Applies to |
|---|---|---|
| `--scrim-hero-horizontal` | the 90deg layer of the hero fade, line 66 | a hero whose copy sits on one side |
| `--scrim-top-heavy` | normalises the top half of the hero's 180deg pass (line 66): 0.55 → 0.75, stop 30% → 45% | any photograph with UI over its top edge |
| `--scrim-bottom` | normalises the bottom half of the same pass: stop 70% → 55%, running to solid ink | a photograph that must meet an ink band below it |
| `--scrim-header` | derived, not from the prototype | any hero with the navigation over it |

The hero fade is tokenised as `--scrim-hero-horizontal`; the story fade (line 127) is not tokenised at all. It must not be folded into `--scrim-hero-horizontal` — the two run to different stops (story reaches transparent at 56%, hero at 48%) and serve different splits.

Scrim tokens are the only permitted way to darken a photograph. Never an inline `rgba()`, never `filter: brightness()` — a filter dims the garment along with the background.

### 14.6 Loading strategy

| Image | `loading` | `fetchpriority` | `decoding` | `sizes` |
|---|---|---|---|---|
| Hero (LCP) | `eager` | `high` | `async` | `100vw` |
| Story | `lazy` | auto | `async` | `(min-width: 1024px) 70vw, 100vw` |
| Product, first row of a collection | `eager` | auto | `async` | matches the grid |
| Product, below the fold | `lazy` | auto | `async` | matches the grid |
| Logo | `eager` | auto | `sync` | fixed at `--logo-height-desktop` / `--logo-height-mobile` |
| UI icons | inline SVG once migrated — no request at all | — | — | — |

### 14.7 Token gap in this section

`--scrim-story-horizontal` — the story split's 90deg fade (line 127) is the one prototype gradient with no token, so every future editorial split will re-author it inline.

## 15. Border System

The prototype uses four distinct border declarations: `1px solid rgba(255,255,255,.1)` (Values band edges and value-tile dividers, lines 142/144, plus the ≤900px tile `border-bottom`, line 41), `1px solid rgba(255,255,255,.08)` (announcement bar underline, line 58), `1px solid #d8c08a` (current-page nav underline, line 71) and `1px solid rgba(0,0,0,.25)` (swatch ring, line 116). A fifth 1px division — the footer vertical divider (line 163) — is not a border at all but a 1×28px `<div>` filled with `background:rgba(255,255,255,.2)` (1.79:1 on ink, computed).

### 15.1 Width

| Token | Value | Use |
|---|---|---|
| `--border-width` | 1px | every border in the system; every border in the prototype is already 1px |
| `--border-width-strong` | 2px | reserved: the selected swatch ring (§13.3) and a current-state marker that 1px cannot carry |

Focus is not a border. It is an `outline` at `--focus-width` 2px and `--focus-offset` 2px, sitting outside the box so it never changes layout (§10.3).

### 15.2 The colour tokens

Four surface borders, arranged as two pairs, plus one accent border:

| Token | Value | Contrast on its surface | Surface | Use |
|---|---|---|---|---|
| `--color-border` | `rgba(243,239,230,0.12)` | 1.32:1 on ink (computed) | dark | section and band separators |
| `--color-border-subtle` | `rgba(243,239,230,0.08)` | below 1.3:1 | dark | the announcement underline (line 58 is exactly .08) |
| `--color-border-inverse` | `rgba(13,12,10,0.14)` | 1.35:1 on cream (computed) | light | section and band separators |
| `--color-border-inverse-subtle` | `rgba(13,12,10,0.08)` | below 1.3:1 | light | the lightest permissible separation |
| `--color-border-strong` | `var(--gs-gold)` | 11.01:1 on ink | dark only | accent rules, current-page marker (line 71) |

Components reference `--color-border-current`, never the pairs above. `.surface-dark` resolves it to `--color-border` and `.surface-light` to `--color-border-inverse` (token file lines 363, 371), so a component moved between bands carries the correct separator without being edited.

Two consequences follow from the measured ratios. First, neither current-border value reaches 3:1, so they may only carry **decorative** separation, which SC 1.4.11 exempts — never the boundary of a control. Fields (§12.2), Secondary buttons (§10.2) and swatch rings (§13.3) all need a 3:1 token that does not yet exist. Second, the surface classes map only the base weight; a component needing the subtle weight on either surface has to name the raw pair, which is the exact failure mode the surface classes exist to prevent. `--color-border-current-subtle` is a recommended addition.

### 15.3 The alpha rule

Every border colour is alpha, which ties separators to the surface beneath them (token file line 81). The corollary is that an alpha border over a photograph is unpredictable — it goes invisible over a light passage and hard over a dark one. `--color-border-current` is therefore used only on flat surfaces; where a division must read over an image, a scrim carries it (§14.5).

The existing `rgba(0,0,0,.25)` swatch ring is 1.82:1 on the cream band and 1.81:1 on the tile (computed): the one place the prototype uses an alpha border as a control boundary, and the one place it must be replaced (§13.3).

### 15.4 When a separator is justified

Four cases, and only these four:

1. **A change of function that is otherwise invisible.** The prototype's Values band carries `border-top`/`border-bottom: 1px solid rgba(255,255,255,.1)` (line 142) — the canonical case: an ink band against the ink hero above it and the ink footer below it, where the change of function is otherwise invisible. The footer itself (line 153) declares no border and relies on the Values band's bottom rule.
2. **A repeated cell divider inside one band.** The value tiles carry `border-right: 1px solid rgba(255,255,255,.1)` (line 144); the ≤900 rules swap the axis to `border-bottom` (line 41) and the ≤520 rules cancel the right edge (line 49). The rule this establishes: a divider that changes axis at a breakpoint must cancel itself on the other axis in the same rule, which lines 41 and 49 already do correctly.
3. **A control boundary** — a field, a swatch, a Secondary button. This case needs 3:1 and therefore cannot use `--color-border-current` (§15.2).
4. **A current-state marker** — the gold nav underline (line 71), which is what keeps the current page distinguishable by something other than colour (§11.2).

Not justified: boxing a product card, outlining an image, framing a section that already changes background colour, a decorative rule between a heading and its body, or a border standing in for spacing.

### 15.5 The restraint rule

When a border and spacing would do the same job, spacing wins.

Concretely, the product grid needs no card borders: `--product-grid-gap` 24px — or `--grid-gap-large` 32px beside the New Drop copy column (§13.1) — is the separation, and the 1:1 `--color-surface-tile` ground already gives every card a visible edge. A border there would double the signal and make an editorial grid read as a template.

Budget: at most one horizontal rule per band, and no band carries both a top and a bottom rule unless it is bracketed by same-colour bands, which is case 1.

### 15.6 Theme settings

No border token is exposed to the Theme Editor. `--gs-ink`, `--gs-cream` and `--gs-gold` are (token file line 409), and because `--color-border-strong` resolves to `--gs-gold`, a merchant changing the brand gold moves every accent border with it — intended, and the reason `--color-border` and `--color-border-inverse` are alpha-derived from cream and ink rather than from gold.

## 16. Radius System

### 16.1 The four tokens

| Token | Value | Intended use |
|---|---|---|
| `--radius-none` | `0` | the default for everything |
| `--radius-sm` | `2px` | inputs and small controls |
| `--radius-md` | `4px` | media containers where a soft edge is wanted |
| `--radius-full` | `9999px` | circles only: swatches, cart count, avatars |

The default is `--radius-none`. A component that does not appear in §16.3 is square.

### 16.2 Why the system stays flat

1. **The prototype is already flat.** `border-radius` appears exactly twice in the whole file, both `50%`: the swatch (line 116) and the cart badge (line 78). Every other edge is square. The system records that decision rather than replacing it.
2. **Full-bleed bands cannot be rounded.** Phase 2 specifies that later phases replace the boxed 1440px wrapper (line 55) with full-bleed sections whose content is constrained by `--container-wide` / `--container-standard` / `--container-narrow`. Rounding the elements inside a full-bleed band makes them read as cards floating on a page, which is the template look spec §4 rules out.
3. **Rounded corners read as app UI.** God Squad is positioned as a fashion editorial (spec §33); a square crop is the editorial convention and the one the photography will be shot against (§14.4).
4. **A radius on a 1:1 product image costs garment.** At 2px it is invisible and pointless; at 8px it clips four corners of the product on every card in the grid.

### 16.3 Where each token is permitted

| Token | Permitted on | Never on |
|---|---|---|
| `--radius-none` | sections, bands, media, product cards, buttons by default, badges, tables, drawers, modals | — |
| `--radius-sm` | text inputs, email inputs, selects, textareas, quantity controls, and the buttons that sit beside them | a product card, a section, an image |
| `--radius-md` | an inset media container inside a bordered panel | anything currently in the design; it has no use today and is held in reserve |
| `--radius-full` | circles only — swatches (line 116), the cart count (line 78), avatars | any button. `--radius-full` on a 44px-tall button produces a pill, which §10.5 and spec §13 both prohibit |

A 2px input beside a 0px button looks like a mistake, so the buttons that pair with form fields take `--radius-sm` too — and follow the merchant automatically if that token is raised.

### 16.4 Theme setting

`--radius-sm` is the sole radius among the eleven tokens the token file marks `[THEME SETTING]`, grouped into six Theme Editor settings; it sits under "Button/input style". These are driven from `settings_schema.json` at theme level in a later phase — the token file itself is not a merchant surface.

The merchant control is constrained to a fixed choice of 0, 2 or 4px. A free numeric field lets a merchant set 24px and dissolve the identity in one click, which is what spec §30's "only expose settings that provide meaningful merchant customization" is guarding against.

## 17. Shadow System

### 17.1 The three tokens

| Token | Value | Status |
|---|---|---|
| `--shadow-none` | `none` | the default for every component in this document |
| `--shadow-subtle` | `0 1px 2px rgba(13, 12, 10, 0.08)` | reserved; no current use (§17.4) |
| `--shadow-elevated` | `0 12px 32px rgba(13, 12, 10, 0.28)` | four permitted uses (§17.3) |

Both shadow values are ink at low alpha, tuned for a cream surface. On `--color-bg-primary` an ink shadow is invisible: a surface floating above a dark band separates by border, scrim or a step in background colour, never by shadow. Two related gaps follow — there is no dark-surface shadow, and there is no backdrop value at all: `--z-overlay` 800 is reserved but the four scrim tokens are all photographic (§14.5), so a `--color-overlay` is a recommended addition before any drawer or modal is built.

### 17.2 The rule: depth comes from contrast, spacing and photography

- **Contrast.** The ink/cream band alternation is the site's primary depth cue (spec §32), and at 17.04:1 it is a far stronger one than any shadow.
- **Spacing.** `--section-pad-block` (`clamp(40px, 6vw, 96px)`) separates one band from the next more convincingly than a border or a shadow, and it scales with the viewport without a new breakpoint.
- **Photography.** The hero (line 65) and story (line 126) images carry real depth. A shadow laid over a photograph competes with the depth already in the frame.

Consequence: product cards, value tiles, badges, buttons, inputs, swatches and images all carry `--shadow-none`. There is no card-elevation scale and none will be added.

### 17.3 The four permitted uses of `--shadow-elevated`

| Use | Why it earns a shadow | Additional rules |
|---|---|---|
| Cart drawer (`--z-drawer` 900) | it slides over live page content; the shadow is what says the page beneath is still there | needs a backdrop (token gap, §17.1) and a focus trap |
| Mobile navigation drawer (`--z-drawer` 900) | same | the trigger is the hamburger, which is currently a role-less `<span>` (line 75) and must become a `<button>` |
| Modal dialog (`--z-modal` 1000) | same | `aria-modal`, focus trap, Escape closes |
| Sticky header after it detaches on scroll (`--z-header` 200) | the one conditional case | at rest the header sits over the hero and is already backed by `--scrim-header`, so it carries `--shadow-none` until it detaches |

An element may carry `--shadow-elevated` only if it also carries a z-index token above `--z-sticky`. If it does not float above the page, it does not get a shadow.

### 17.4 `--shadow-subtle`

Reserved and currently unused. Its one legitimate future use is a dropdown or autocomplete panel attached to the search field on a light surface, where `--shadow-elevated` would be too heavy for a 200px panel. It is never applied to a product card, a section, an image or a button.

### 17.5 What shadows must not do

No coloured shadows and no gold glow — gold is an accent, not a light source. No `text-shadow`: text over a photograph is made legible by a scrim (§14.5), which is a design decision, not a patch. No inset shadows standing in for borders. No shadow appearing on hover as the hover affordance (§10.3 and §13.6 define colour and scale for that). No shadow on any element whose background is `--color-bg-primary`, where it would not render at all.

## 18. Icon System

### 18.1 The required set

The prototype serves **ten icon placements from nine raster PNGs** on four canvases (Phase 1 ICON-01, audit line 1797): the announcement globe (line 60), search / account / cart (lines 76-78), two social marks (lines 160-161) and four value-tile glyphs supplied as data — `icon-crown.png`, `icon-community.png`, `icon-globe.png`, `icon-diamond.png` (lines 180-183), the globe file being reused at 44px. The hamburger is not an icon at all: three bare `<span>` bars (line 75).

The set this system defines is the **nine primary UI icons** spec §21 names, plus the **four value glyphs** the prototype already supplies — **thirteen UI glyphs** — plus the social set (Phase 2 spec §21; Phase 1 ICON-04, audit line 2429).

| Glyph | Size token | Named job | What exists today |
|---|---|---|---|
| `search` | `--icon-md` 24px | Header utility | raster PNG (line 76) |
| `account` | `--icon-md` | Header utility | raster PNG (line 77) |
| `cart` | `--icon-md` | Header utility; count badge anchors to it | raster PNG (line 78) |
| `menu` | `--icon-md` inside a `--target-min` box | Mobile menu trigger | three `<span>` bars (line 75) |
| `close` | `--icon-md` | Dismiss the mobile menu, cart drawer, modal | none |
| `chevron` | `--icon-sm` 16px inline; `--icon-md` in controls | Select and accordion disclosure, carousel stepper | none |
| `arrow` | `--icon-sm` | Trailing mark on text CTAs | text glyph `→`, outside Jost (lines 104, 132) |
| `plus` | `--icon-md` | Quantity increment, spec §15 | none |
| `minus` | `--icon-md` | Quantity decrement, spec §15 | none |
| `globe` | `--icon-sm` in the bar; `--icon-xl` in a value tile | Shipping mark; "Worldwide" value | raster PNG (lines 60, 182) |
| `crown` | `--icon-xl` 44px | "Faith Driven" value tile | raster PNG (line 180) |
| `community` | `--icon-xl` | "Community" value tile | raster PNG (line 181) |
| `diamond` | `--icon-xl` | "Premium Quality" value tile | raster PNG (line 183) |

`close`, `chevron`, `plus` and `minus` are required, not optional: without them the mobile menu of §19.6, the select and accordion of spec §15 and the quantity selector of spec §15 cannot be specified at all (ICON-04, audit line 2429; Phase 1 recommendation, audit line 2984).

**Social set.** Two marks exist — `facebook`, `instagram` (lines 160-161). The set is extensible to the platforms spec §21 names (TikTok, YouTube) and to the mockup glyphs Phase 1 flags as having no counterpart (ICON-03 / C14, audit lines 1994, 2496). Any added mark follows the same plain-monoline, `currentColor`, `--icon-lg` rules below. **Which accounts exist is BUSINESS INFORMATION REQUIRED**; no social mark ships without a confirmed account and URL.

**Closure rule.** The set is closed to *decorative* additions. A glyph enters only when a later phase names the interaction it serves and no existing glyph serves it. Phase 1's remaining coverage gaps — `check`, `filter`, `external-link` (ICON-04, audit line 2429) — are pre-approved on that basis and enter when the template that needs them is specified.

### 18.2 Size tokens

| Token | Value | Use | Prototype source |
|---|---|---|---|
| `--icon-sm` | 16px | Announcement globe, inline chevron, CTA arrow | line 60 |
| `--icon-md` | 24px | All header utilities and all control glyphs | lines 76-78 |
| `--icon-lg` | 28px | **Social marks only** | lines 160-161 |
| `--icon-xl` | 44px | Value-tile glyphs only | line 145 |

No other icon size exists. `--icon-lg` is reserved for the footer social row and must not be used for UI: a 28px UI glyph beside a 24px one is exactly the optical unevenness Phase 1 records (ICON-05, audit line 2497 — four canvas sizes, two stroke weights, rendered widths of 52/60/44/52px at the same 44px height).

### 18.3 Construction rules

1. **Inline SVG only.** No icon font, no sprite sheet library, no `<img>` for a UI glyph (spec §36; ICON-01). Phase 10 should deliver one inline snippet set; this phase fixes only the geometry, colour and size rules it must obey (Phase 1 recommendation, audit line 2984).
2. **One optical size.** Every glyph is drawn on a **24 × 24 `viewBox`** with a 1.5px safe margin, `fill="none"`, monoline strokes, `stroke-linecap="square"` and `stroke-linejoin="miter"`. Square caps and mitred joins match the flat editorial geometry of the rest of the system, where the only radius in the prototype is `50%` on swatches and the cart badge (brief: radius).
3. **One stroke weight.** The recommended weight is **1.5 at the 24px optical size**. A `viewBox`-scaled SVG scales its stroke proportionally by default, so `--icon-sm` and `--icon-lg` need no intervention. Only `--icon-xl` 44px is redrawn, because 1.5 scaled to 44px reads heavy beside the same glyph at 24px. *Recommendation: the token file has no token for stroke weight; add `--icon-stroke: 1.5` so the single-weight rule is enforceable rather than conventional.*
4. **`currentColor` throughout.** Every stroke and fill is `currentColor`. An icon never carries its own colour value. This is what lets one file serve `.surface-dark` and `.surface-light` and lets hover and focus reach the glyph at all.
5. **No composed artefacts.** A glyph contains the glyph and nothing else. The cart count is a separate element positioned against the cart icon (line 78), never part of the drawing — the current `icon-cart.png` retains a sliver of the sprite sheet's gold "0" badge while the page overlays its own badge, so the count is drawn twice (ICON-02, audit line 2495).
6. **The CTA arrow becomes a glyph.** `→` is a text character that Jost does not contain and that falls back to a per-platform face (brief: still open; ICON-04). It becomes the `arrow` icon at `--icon-sm`, `aria-hidden`, so the link is not announced as "…rightwards arrow" (A11Y-06, audit line 2477).

### 18.4 Colour and surface behaviour

| Context | Icon colour |
|---|---|
| On `.surface-dark` | inherits `--color-text-primary`; a deliberately accented glyph uses `--accent-current` (resolves to `--color-accent`, 11.01:1 on ink) |
| On `.surface-light` | inherits `--color-text-inverse`; an accented glyph uses `--accent-current` (resolves to `--color-accent-strong` #82672B, 4.66:1 on cream) |
| Muted / secondary | `--color-text-muted` on dark only; on light, `--color-text-inverse-muted` — never `--gs-stone`, which is 1.76:1 on cream |

**Gold is never hard-coded on a glyph.** The announcement globe is gold in the build where the mockup shows it cream; because the icon inherits, that divergence becomes a surface decision rather than a baked pixel. A glyph that must be perceivable as a UI boundary or control on a light surface meets **3:1** minimum, which `--color-accent` (1.43:1 on the tile cream `--gs-cream-300`, 1.55:1 on cream) cannot.

### 18.5 Alignment

- An icon is `inline-flex`, `flex: none`, and sits in a flex row with its label at `gap: var(--space-2)` 8px (the prototype's own announcement gap, line 60).
- Vertical alignment is to the **cap height** of the adjoining tracked caps, not the baseline; tracked uppercase has no descenders, so centring the icon box against the line box is correct.
- Ad-hoc optical nudges (`margin-top: -1px`, `position: relative; top:`) are prohibited. If a glyph looks misaligned, the glyph is redrawn on the 24px grid — the geometry is fixed once, not corrected per placement (ICON-05).
- Icon-only controls are centred inside a `--target-min` 44px box; the box, not the glyph, is the hit area (§24.2).

### 18.6 Hover, focus and state

| State | Change | Duration |
|---|---|---|
| Hover | `color` only → `--accent-current` | `--transition-fast` |
| Focus-visible | the surface-aware ring of §23 on the 44px box, not on the glyph | none |
| Active | `color` → `--color-accent-hover` on dark; no transform | `--transition-fast` |
| Disabled | `opacity: 0.4` plus the control's own disabled semantics; never colour alone | — |

An icon never scales, rotates or translates on hover, and a glyph is never swapped for a second file to express a state. The one permitted transform in the system is the `chevron` rotating 180° when its disclosure opens, at `--transition-fast` — a state change, not decoration.

### 18.7 Why the current raster PNGs cannot serve

| Defect | Consequence | Reference |
|---|---|---|
| Colour baked into the pixels | The glyph cannot inherit `color`, so it cannot follow `.surface-dark` / `.surface-light` | ICON-01, audit line 1797 |
| Cannot recolour | No hover, focus, active or disabled state is expressible on any icon — the footer marks have no state at all | ICON-01; A11Y-04, audit line 2398 |
| Four canvas sizes, two stroke weights | The value row reads optically uneven; nav and feature icons do not belong to one family | ICON-05, audit line 2497 |
| ~30 KB per placement | An SVG expresses the same glyph in under 1 KB; 308,521 B of PNG for ten placements | ICON-01, audit line 1797; spec §36 |
| Soft AI-sprite cut edges | Edges shimmer against the flat ink and cream grounds | ICON-01 |
| `icon-cart.png` sprite residue | A stray gold arc appears beside the bag at larger sizes and on light grounds | ICON-02, audit line 2495 |
| Social marks are two-tone circled badges | They cannot take the link hover colour and break the monochrome footer | ICON-03, audit line 2496 |

### 18.8 Accessibility

- A decorative icon beside a visible text label is `aria-hidden="true"` with empty `alt`; it must never be read twice.
- An icon-only control carries a text accessible name ("Search", "Open menu", "Cart, 2 items"). The current header names functions that do not exist and the hamburger's `aria-label` sits on a role-less `<span>`, where ARIA prohibits naming and the label is ignored (A11Y-07, audit line 2478; A11Y-09, audit line 2401).
- Icon-only controls are not the only carrier of a state: an open menu is `aria-expanded`, not a swapped glyph alone.

### 18.9 Performance

Inline SVG only, no icon library, no runtime sprite fetch, no `filter` or `mask` effects on glyphs. The thirteen UI glyphs plus the social set should total well under the 308 KB the nine PNGs cost today (spec §36; ICON-01).

## 19. Navigation System

### 19.1 Structure

The header is welded to the hero today: the `<nav>` is absolutely positioned inside the hero `<section>` (line 68) and the hero copy columns pad `170px` / `190px` at the top to clear it (lines 82, 90). There is no `<header>` and no `<main>` (Phase 1 C7; A11Y-02, audit line 2397).

The system requires three independent boxes in source order: **announcement bar → header → page content**. No page section compensates for the header's height with padding, and no overlay inside the header is anchored to a box the header shares.

In **Online Store 2.0** terms this is two sections in the `header` section group (`sections/header-group.json`) — an announcement-bar section above a header section — with page content rendered from the JSON template below them. The ordering is then merchant-reorderable in the theme editor without a developer, and the header never nests inside a hero section (spec §30, §31).

### 19.2 Heights and logo

| Token | Value | Derivation |
|---|---|---|
| `--header-height-desktop` | 122px | 78px logo + 2 × 22px padding (line 68) |
| `--header-height-mobile` | 88px | measured at 375 / 390 / 430 / 768 / 900 (brief) |
| `--logo-height-desktop` | 78px | line 69 |
| `--logo-height-mobile` | 56px | `[data-r=logo]{height:56px!important}` (900px query, line 32) |
| `--logo-height-footer` | 56px | line 155 |
| `--announcement-height` | 40px | replaces `12px 48px` padding on an 11px line (line 58) |

The logo is height-constrained and `width: auto` at every tier; it is never rotated, never animated and never given a hover state. The `background:#0230` on the logo wrappers (lines 69, 155) is a valid four-digit `#RGBA` hex resolving to `rgba(0,34,51,0)` — fully transparent, so it paints nothing; the two wrappers exist only to carry it and are not part of the system (Phase 1 CSS-06, audit lines 359, 367).

*Correction to the token file: the `--logo-height-mobile` comment cites line 33, but the source rule `[data-r=logo]{height:56px!important}` is line 32. The token file's comment should be corrected rather than this document silently diverging from it.*

The real logo asset is a raster PNG; a vector logo is **BUSINESS INFORMATION REQUIRED** before these heights can be confirmed against a final mark.

### 19.3 The header backing rule — mandatory

Three primary links measure **2.4-2.9:1** over the bright sky between the models at 1440 and 1024, and the gold Home link drops to about **3.5:1 at 1024** (A11Y-03, audit line 2335; HERO-02, audit line 2351). Any header placed over imagery therefore takes one of exactly two treatments:

1. **Opaque** — `background: var(--color-bg-primary)`, or
2. **Scrimmed** — `--scrim-header` (`linear-gradient(180deg, rgba(13,12,10,.85) 0%, rgba(13,12,10,.55) 60%, rgba(13,12,10,0) 100%)`) applied **to the header's own box**, sized to at least `--header-height-desktop` + `--announcement-height`.

The scrim is never anchored to the hero section. Anchoring an overlay to a parent the header shares is the exact mechanism behind the hero fade defect of §25.6, and it is prohibited system-wide.

Acceptance: nav text measures **≥ 4.5:1** against the composited pixel at its worst point, verified per hero image. Final photography is **BUSINESS INFORMATION REQUIRED**, so the verification is a gate on the phase that ships the image, not a claim made here.

A sticky header on scroll becomes opaque `--color-bg-primary` with a `--color-border-subtle` bottom hairline at `--z-header` 200. `--shadow-elevated` is permitted only where the sticky header overlaps a light band; over dark content the hairline alone is correct (spec §20).

### 19.4 Desktop navigation

Primary items are **HOME, SHOP, COLLECTIONS, OUR STORY, VERSE** (Phase 2 spec §22). The prototype already renders these five (lines 71-72); their destinations are **BUSINESS INFORMATION REQUIRED**.

| Property | Rule | Token / source |
|---|---|---|
| Type | uppercase, tracked | `--type-label-size` 12px, `--type-label-ls` 0.22em, `--type-label-weight` |
| Item gap | 40px | `--nav-gap` (`--space-7`); prototype used 44px (line 70) |
| Utility cluster gap | 24px | `--space-5`; prototype used 26px (line 74) |
| Utility icon size | 24px | `--icon-md` (lines 76-78) |
| Visible from | `--bp-lg` 1024 and up | see §19.6 |
| Alignment | logo left, primary centre or left, utilities right | line 68 |

The prototype's nav tracking is 0.2em (line 70); it is normalised to `--type-label-ls` 0.22em so that size and tracking travel together as one token pair. The prototype's nav weight is 500 (line 70) while `--type-label-weight` is `--weight-semibold` 600. **Recommendation:** if the 500 weight must be preserved, add a `--type-label-weight-nav` token to the token file rather than writing `--weight-medium` inline — pairing two thirds of the label triplet with a hard-coded weight reintroduces the near-duplicate label style spec §7 prohibits.

**State matrix**

| State | Treatment | Notes |
|---|---|---|
| Default | `--color-text-primary` cream, 17.04:1 on ink | |
| Hover | `color` → `--accent-current`, `--transition-fast` | on a light-surface header this resolves to `--color-accent-strong`, never gold |
| Current page | `color` → `--accent-current` plus a 1px underline in the same colour at `--space-1` 4px offset | prototype: `border-bottom:1px solid #d8c08a; padding-bottom:4px` (line 71) |
| Current page, hovered | the underline shifts to `--color-accent-hover`; the text does not change | today Home is already gold, so its hover is invisible (brief: hover that exists) |
| Focus-visible | the surface-aware ring of §23 | |
| Active / pressed | `color` → `--color-accent-hover` (13.25:1 on ink) | no transform, no layout change |

Current state is never carried by colour alone: `aria-current="page"` plus the underline carry it for users who cannot resolve gold against cream or who are not using a pointer.

The global `a:hover{color:#d8c08a}` rule (line 16) is **prohibited** by this system. It paints gold on any link, including links on cream at 1.55:1. Hover colour comes from `--accent-current`, which `.surface-light` reassigns.

### 19.5 Utility cluster

SEARCH, ACCOUNT, CART (spec §22), each an `--icon-md` 24px glyph centred in a `--target-min` 44px box, separated by `--space-5`. The cart count is a separate element anchored to the cart icon, at `--type-caption-size` 12px minimum — the prototype's 9px badge (line 78) is below the floor the token file sets. Whether cart, search and accounts exist at launch is **BUSINESS INFORMATION REQUIRED**; a control that leads nowhere is not shipped.

### 19.6 Mobile navigation

Below `--bp-lg` 1024 the primary list collapses to a single menu trigger. The prototype hides `[data-r=nav-links]` with `display:none!important` (900px query, line 30) and shows a hamburger built from three `<span>` bars measuring **22 × 16** (line 75; the 900px query sets `gap:5px`, line 31). That control has no handler, no role and no panel, so between 320 and 900px the site has **no navigation at all** (A11Y-01, audit line 2334).

Requirements for the menu this system defines — design rules only, not an implementation:

| Requirement | Rule |
|---|---|
| Trigger | a real button with `aria-expanded` and `aria-controls`; `menu` glyph at `--icon-md` in a `--target-min` box |
| Panel | full-viewport, `--color-bg-primary`, `--z-drawer` 900, scroll locked beneath |
| Close | `close` glyph at `--icon-md` in a `--target-min` box, top-right, aligned to `--header-height-mobile` |
| Item type | `--type-eyebrow-size` 13px, `--type-eyebrow-ls` 0.30em, `--type-eyebrow-weight`, uppercase |
| Item row | `--target-min` 44px minimum height, `--gutter` inline padding, `--color-border-subtle` hairline between rows |
| Utilities | repeated at the foot of the panel at `--target-min`, with visible text labels |
| Dismissal | the close control, `Escape`, and a tap outside where a partial panel is used |
| Focus | trapped inside the panel while open; returned to the trigger on close (§23.6) |
| Motion | `opacity` and `transform` only, `--transition-medium`, `--ease-standard`; collapses under reduced motion (§21.4) |

*Recommendation: the token file has no width token for a sliding panel. Add `--drawer-width` before the cart drawer is specified; the menu itself is full-viewport and needs none.*

### 19.7 What this section does not do

It defines no markup, no Liquid, no menu handler and no information architecture beyond the five names spec §22 supplies. Building the header, the menu and the utility controls belongs to later phases (spec §22, §41).

## 20. Announcement Bar

### 20.1 Role

The bar carries a standing brand or service statement above the header. It is a system-level notice, not a promotional device, and it is not dismissible — a dismiss control would add a `close` glyph, a persistence question and a restore path to a component whose whole value is that it is quiet.

Today it is a plain `<div data-r="announce">` outside the hero, flex `space-between`, not a link, no dismiss, no rotation (line 58; audit line 852).

### 20.2 Height and spacing

| Property | Rule | Source |
|---|---|---|
| Height | `--announcement-height` 40px, fixed, content vertically centred | replaces `padding:12px 48px` on an 11px line (line 58) |
| Inline padding | `var(--gutter)` — 24 / 32 / 48px by tier | kills the dead-hook gutter of §25.6 |
| Layout | two items, `space-between`, from `--bp-md` up | line 58 |
| Icon-to-label gap | `--space-2` 8px | line 60 |
| Bottom separator | 1px `--color-border-subtle` | `rgba(255,255,255,.08)` (line 58) |

The inline padding is `var(--gutter)`, identical to every other band. The prototype's announcement keeps `48px` between 521 and 900px while everything else drops to 24px, because the 900px query's first rule targets `[data-r=pad]` and no element carries that hook (line 19; audit line 436). Binding the bar to `--gutter` removes the class of defect, not just the instance.

### 20.3 Typography

`--type-caption-size` 12px, `--type-caption-ls` 0.20em, `--type-caption-weight` (`--weight-regular`), uppercase. The prototype sets 11px at 0.22em (line 58); the size is raised to the token file's 12px persistent-interface floor and the tracking normalised to the caption pair, because size and tracking travel together as one token set. Confirmation of the 12px floor against brand intent is **BUSINESS INFORMATION REQUIRED** (token file, §4 header note).

### 20.4 Colour

| Element | Token | Ratio |
|---|---|---|
| Ground | `--color-bg-primary` ink | — |
| Left message | `--color-accent` gold | 11.01:1 on ink |
| Right message and glyph | `--color-text-primary` cream | 17.04:1 on ink |
| Separator | `--color-border-subtle` | — |

The bar is a dark surface in every context, which is the only reason gold text is permitted on it. If a later phase ever places the bar on cream, gold text is **prohibited** (1.55:1) and `--color-accent-strong` applies — the `.surface-light` class already enforces this by reassigning `--accent-current`.

The bar's background is **not** exposed as a merchant setting at either layer; only `--announcement-height` appears in the token file's `[THEME SETTING]` block. Letting a merchant set this ground is how gold text ends up on cream.

### 20.5 Permitted content

Permitted content is limited to the pair in the source — **`Good People. Higher Purpose.`** (line 59; also a spec §13 primary message) and **`Worldwide Shipping`** (line 60) — plus the alternative spec §23 names, **`The Faithful Collection`** ("The Faithful" is already the New Drop headline, line 101). Nothing beyond those three strings may be written; any other copy is **BUSINESS INFORMATION REQUIRED**.

Prohibited outright: discount codes, countdowns, urgency language, rotating or carousel messages, marquee scrolling, and any claim that is not verifiable. Whether "Worldwide Shipping" is factually accurate is itself **BUSINESS INFORMATION REQUIRED** (Phase 1 Appendix A).

**Settings layers.** `--announcement-height` is a **theme-level** setting in `settings_schema.json`. The two messages are settings on the **announcement-bar section** (or blocks within it) in the `header` section group, so they travel with the section rather than the theme. The bar's background is exposed at neither layer (spec §30).

### 20.6 Link behaviour

At most **one** of the two messages may be a link. A linked message:

- is underlined at rest, `text-decoration-thickness: var(--border-width)` 1px, `text-underline-offset: 0.25em`;
- changes **`text-decoration-color` only** on hover — gold → `--color-accent-hover` — over `--transition-fast`. No thickness changes at any state, in line with §22.1;
- takes the surface-aware focus ring of §23 (`--focus-ring-on-dark` gold, 11.01:1 on ink);
- states its destination in its own words; "Worldwide Shipping" may not link until a shipping policy page exists (**BUSINESS INFORMATION REQUIRED**);
- reaches `--target-min-aa` 24px in its hit area, which the 40px bar supplies.

### 20.7 Mobile

Below `--bp-sm` 480 the two messages stack to two centred lines and the height becomes auto with `--space-3` 12px block padding and `--gutter` inline padding. The prototype already stacks here with `10px 16px` (line 50); the block padding is normalised to `--space-3` and the inline padding to `--gutter`.

*Recommendation: `--announcement-height` is a single 40px value and cannot express the stacked case. Add `--announcement-height-stacked` (or declare the stacked bar auto-height) so the header offset remains calculable at every tier.*

### 20.8 Prohibitions

No animation of any kind, including fade-in on load (§21.3). No icons other than `globe` at `--icon-sm`. No second accent colour. No border other than the bottom hairline. No background image. The bar never exceeds one line per message.

## 21. Motion System

### 21.1 Starting position: the prototype has no motion at all

Measured across the source: **zero `transition` declarations, zero `animation` declarations, zero `@keyframes`, zero `prefers-reduced-motion` blocks** (brief: measured). The 22 `transform` occurrences are all static rotations of the Kaushan script block — `rotate(-8deg)` at rest and `rotate(-6deg)!important` on mobile (line 91; 900px query, line 27). Nothing moves.

This system therefore defines motion from zero, and the first rule is that it stays close to zero. Motion supports comprehension — a panel arriving, a state confirming — and is never the reason a user notices an element (spec §25).

### 21.2 Durations and easing

| Token | Value | Use |
|---|---|---|
| `--duration-fast` | 150ms | colour, opacity and decoration changes on controls: links, buttons, icons, swatches |
| `--duration-medium` | 250ms | transforms and reveals: menu panel, drawer, disclosure, product image scale |
| `--duration-slow` | 400ms | full-surface changes only: an overlay scrim behind a drawer or modal |
| `--ease-standard` | `cubic-bezier(0.2, 0, 0, 1)` | default for everything |
| `--ease-out` | `cubic-bezier(0, 0, 0.2, 1)` | elements leaving, and entrances that must feel immediate |

Shorthands `--transition-fast`, `--transition-medium` and `--transition-slow` bind each duration to `--ease-standard`. No other duration or curve exists. A component that needs a fourth duration is over-designed.

### 21.3 What may be animated

**Permitted: `opacity` and `transform`** for anything that moves or appears, plus — **on control-sized surfaces only** (buttons, links, icons, swatches, form controls) — `color`, `background-color`, `border-color`, `text-decoration-color`, `outline-color` and `box-shadow`. The prototype's own compiled CTA hovers already work this way: `background:#2a2823; color:#f3efe6` and `background:#e6d3a6; color:#0d0c0a` (line 104; brief: hover that exists).

**Do not animate**

| Property / effect | Reason |
|---|---|
| `width`, `height` | forces layout on every frame; use `transform: scale()` inside a clipped box |
| `top`, `left`, `right`, `bottom` | same; use `transform: translate()` |
| `margin`, `padding` | same, and it changes the outer box, which §22.1 prohibits |
| `border-width`, `text-decoration-thickness`, `outline-width` | a thickness change is a layout or optical jump; rings that must thicken are drawn with `box-shadow: 0 0 0 Npx` |
| `letter-spacing`, `font-size`, `font-weight` | the tracked-caps signature must never be in motion; it reflows the line |
| `background-color` on a full-bleed section | a 1440-wide repaint for no informational gain |
| `filter` / `backdrop-filter` on imagery | expensive, and it degrades the photography the brand is built on |
| `transform: rotate()` | the hero script rotations stay static (line 91; 900px query, line 27) |
| Scroll-linked parallax or scroll-triggered reveals | content must be present at rest; a reveal that depends on scroll fails reduced motion and search crawlers alike |
| Page-entry animation on headline type | the h1 is the page; it does not arrive |
| The logo, the announcement bar, the gold hairlines | fixed elements of the identity |

### 21.4 Assignment

| Interaction | Property | Duration |
|---|---|---|
| Nav link, footer link, icon colour | `color` | `--duration-fast` |
| Button fill and label | `background-color`, `color` | `--duration-fast` |
| Swatch ring | `box-shadow` | `--duration-fast` |
| Underline reveal | `text-decoration-color` | `--duration-fast` |
| Product image scale | `transform` | `--duration-medium` |
| Menu panel / drawer entry and exit | `transform`, `opacity` | `--duration-medium` |
| Chevron disclosure | `transform: rotate(180deg)` | `--duration-fast` |
| Overlay scrim behind a drawer or modal | `opacity` | `--duration-slow` |

### 21.5 Reduced motion

The token file already ships the support the prototype lacks (token file, `@media (prefers-reduced-motion: reduce)`): `--duration-fast`, `--duration-medium` and `--duration-slow` collapse to 1ms and `--hover-image-scale` drops to 1, with a global sweep setting `animation-duration`, `animation-iteration-count`, `transition-duration` and `scroll-behavior`.

Rules that follow from it:

1. Every animated element must be usable and complete at its end state with no transition. Nothing exists only during an animation.
2. No content may be reachable only after motion. A reveal that depends on a transition is prohibited; the content is present at rest and the transition only changes how it arrives.
3. Durations are read from the tokens, never hard-coded, or the reduced-motion block cannot reach them.
4. The reduced-motion block is the **only** place `!important` is permitted in this system (§25.1).
5. Reduced motion is a preference, not a downgrade: colour, focus and state feedback remain identical, they simply arrive instantly.

### 21.6 Performance

No animation library and no JavaScript-driven tweening (spec §36). Animate compositor-friendly properties only. At most one property per element per interaction wherever the interaction allows. `will-change` is applied for the duration of an interaction and removed after; it is never left on a persistent element.

## 22. Hover States

### 22.1 Governing rules

1. **Hover is never the only signal.** Every hover has a focus equivalent (§23), and any hover that conveys state also carries that state non-visually — `aria-current`, `aria-pressed`, `aria-expanded` or visible text. Pointer-only affordances are prohibited.
2. **Hover never changes layout, and never changes a thickness.** A hover state may change `color`, `background-color`, `border-color`, `text-decoration-color`, `opacity`, `transform` and `box-shadow` — nothing else. No `border-width`, `text-decoration-thickness`, `outline-width`, `padding`, `margin`, `width`, `height`, `letter-spacing` or `font-weight` change. **Rings that need to read thicker are drawn with `box-shadow: 0 0 0 Npx`**, which paints outside the border box without affecting layout. This mechanism is used identically for the product swatch (§22.4, §22.8) and for the announcement link, whose underline changes colour only (§20.6).
3. **One property per element per interaction** wherever the interaction allows.
4. **Duration** is `--transition-fast` for colour and decoration, `--transition-medium` for transform (§21.4).
5. **Hover is pointer-scoped.** Hover rules sit inside `@media (hover: hover)` so a touch tap never leaves an element stuck in a hover state.
6. **The global `a:hover` rule is prohibited.** `a{color:inherit}a:hover{color:#d8c08a}` (line 16) paints gold on every link in the document, including links on cream at 1.55:1. Hover colour comes from `--accent-current`, which `.surface-light` reassigns to `--color-accent-strong`.

### 22.2 Navigation

As specified in §19.4. Colour only, `--transition-fast`, `--accent-current`. A current-page item changes its underline colour rather than its text colour, so the state is not lost on an item that is already gold (brief: hover that exists).

### 22.3 Buttons

| Variant | Rest | Hover | Source |
|---|---|---|---|
| Primary (on a light band) | `background: var(--color-text-inverse)` ink, `color: var(--color-text-primary)` cream | `background` → `--color-surface-raised` #2A2823 | the prototype's own compiled `background:#2a2823; color:#f3efe6` (line 104) |
| Primary (on a dark band) | `background: var(--color-text-primary)` cream, `color: var(--color-text-inverse)` ink | `background` → `--gs-cream-200` | 15.41:1 inverse pairing |
| Secondary | transparent, 1px `--color-border-current`, inherited text | `border-color` → the surface's text colour; fill unchanged | spec §13 |
| Accent (dark surfaces only) | `background: var(--color-accent)` gold, `color: var(--color-text-inverse)` ink, 11.01:1 | `background` → `--color-accent-hover` #E6D3A6, 13.25:1 | the prototype's compiled `background:#e6d3a6; color:#0d0c0a` (line 104) |
| Text CTA | inherited colour, underline `transparent`, trailing `arrow` glyph | `text-decoration-color` → `currentColor`; the arrow translates `translateX(2px)` at `--transition-fast` | spec §13 |

The accent button is **never** placed on a light band: gold fill with ink text is legible, but the button's own edge against cream measures 1.55:1 and disappears. On light bands the accent role is carried by `--color-accent-strong` as a text or border colour, not as a fill.

### 22.4 Product card

| Element | Hover behaviour | Duration |
|---|---|---|
| Media image | `transform: scale(var(--hover-image-scale))` 1.03, clipped by the fixed `--product-aspect` box | `--transition-medium` |
| Tile ground | no change — stays `--color-surface-tile` `#EBE6DC` (line 109) at every state | — |
| Product name | underline reveal: `text-decoration-color` `transparent` → `currentColor`, thickness fixed at `var(--border-width)`, offset `0.25em` | `--transition-fast` |
| Price | no change | — |
| Swatch | `box-shadow: 0 0 0 var(--border-width) var(--color-text-inverse)` — a halo outside the resting 1px border; the border itself never changes | `--transition-fast` |
| Card container | no background, no border, no shadow, no lift, at any state | — |
| Quick-action CTA | **deliberately excluded** — see below | — |

The swatch's resting ring is `var(--border-width)` `--color-border-inverse` at all times (normalising `1px solid rgba(0,0,0,.25)`, line 116). Selection is a 2px `--accent-current` ring drawn the same way — `box-shadow: 0 0 0 var(--border-width-strong) var(--accent-current)`, 4.66:1 on cream — and is additionally carried by the control's accessible name and pressed state, never by colour alone.

**On the CTA reveal.** Spec §26 names "subtle CTA reveal" for product hover. This system excludes it, for two stated reasons: a control that appears only on hover is a pointer-only affordance, which rule §22.1.1 prohibits; and it adds a fifth element to a card the restraint principle keeps to image, name, price and swatches (spec §4, §16). If a later phase establishes a genuine need for a quick action, it must be **present at rest**, at `--target-min` 44px, keyboard-reachable and inside the card's accessible name — not revealed on hover.

Second-image-on-hover swaps are not defined by this system. They require a second confirmed photograph per product and a decision about what touch users see instead; both are **BUSINESS INFORMATION REQUIRED**.

### 22.5 Images

`--hover-image-scale` is **1.03** and the token file's own comment caps it: never above 1.05.

- Permitted only inside a clipped, fixed-ratio box (`--product-aspect` 1/1, line 109, or `--product-aspect-wide` 4/5), and only where the whole tile is a single link.
- Prohibited on the hero image, the story image, the logo, the value glyphs and any full-bleed editorial band. Those are compositions, not controls.
- The product images are 235px mockup crops; at 375px they are drawn at 327px — about 1.4× source in CSS pixels, and roughly 2.8× on a 2× display (brief: measured responsive behaviour; RESP-02, audit line 2439). Scaling an already-upscaled crop compounds the defect, so the scale hover is gated on real photography (**BUSINESS INFORMATION REQUIRED**).
- Reduced motion sets `--hover-image-scale` to 1 (token file, reduced-motion block).

### 22.6 Social icons

The footer marks have **no visible hover today**: the global `a:hover` rule matches both social links but cannot change a raster `<img>`, so the marks do not respond (lines 160-161; ICON-03, audit line 2496).

Once they are inline SVG with `currentColor` (§18), hover changes `color` only — `--color-text-primary` → `--accent-current` (gold on the dark footer, 11.01:1) at `--transition-fast`. No scale, no rotation, and **no brand colours**: Facebook blue and Instagram's gradient would both break the monochrome footer, and the current two-tone circled badges already cannot take the theme's link colour (ICON-03).

### 22.7 Links in body, editorial and footer copy

| Context | Rest | Hover |
|---|---|---|
| Body / editorial inline link | underlined, `text-decoration-thickness: var(--border-width)`, offset `0.25em`, inherited colour | `text-decoration-color` → `--accent-current` |
| Footer link | no underline (tracked caps), inherited `--color-text-muted` | `color` → `--color-text-primary`, underline colour revealed |
| Policy / legal link | always underlined | `text-decoration-color` only |

An inline link inside running copy is always underlined at rest: on cream, `--color-accent-strong` at 4.66:1 is legible as text but is not a sufficient sole indicator of link-ness, and gold at 1.55:1 is not legible at all.

### 22.8 Summary matrix

| Component | Property changed | Rest | Hover | Duration |
|---|---|---|---|---|
| Nav link | `color` | `--color-text-primary` | `--accent-current` | fast |
| Nav link, current | `border-bottom-color` (fixed 1px) | `--accent-current` | `--color-accent-hover` | fast |
| Button, primary | `background-color` | ink | `--color-surface-raised` | fast |
| Button, accent | `background-color` | `--color-accent` | `--color-accent-hover` | fast |
| Button, secondary | `border-color` | `--color-border-current` | surface text colour | fast |
| Text CTA | `text-decoration-color`, arrow `transform` | transparent | `currentColor`, `translateX(2px)` | fast |
| Product media | `transform` | `scale(1)` | `scale(var(--hover-image-scale))` | medium |
| Product name | `text-decoration-color` | transparent | `currentColor` | fast |
| Swatch | `box-shadow` | none | `0 0 0 var(--border-width) var(--color-text-inverse)` | fast |
| Announcement link | `text-decoration-color` | `--color-accent` | `--color-accent-hover` | fast |
| Icon, standalone | `color` | inherited | `--accent-current` | fast |
| Social mark | `color` | `--color-text-primary` | `--accent-current` | fast |
| Card container | — | — | no change | — |

## 23. Focus States

### 23.1 Starting position

No `:focus` or `:focus-visible` rule exists anywhere in the source; the browser default ring is the only indicator, and the two raster social icon links have no hover or focus state at all (A11Y-04, audit line 2398).

Worse, most of the things that need focus cannot receive it. Search, Account and Cart are bare `<img>` elements and the menu trigger is a `<span>` (lines 75-78), so the page contains **zero** focusable controls in its header (A11Y-01, audit line 2334). Colour swatches are empty `<span>`s with inline backgrounds (line 116). **§24.4 semantics is therefore a precondition for this section**: you cannot style focus on an element that cannot hold it.

### 23.2 The ring

| Token | Value |
|---|---|
| `--focus-width` | 2px |
| `--focus-offset` | 2px |
| `--focus-ring` | resolves per surface |

The ring is a solid 2px outline at a 2px offset, applied through **`:focus-visible`** — the token file's global rule covers `a, button, input, select, textarea, summary, [tabindex]`. Pointer users do not see it; keyboard users always do. The ring is drawn on the control's 44px hit box, never on the glyph inside it.

The outline is never clipped: any ancestor with `overflow: hidden` around a focusable element must leave room for `--focus-width` + `--focus-offset`. The prototype's wrapper carries `overflow:hidden` (line 55) and would clip a ring at the edge of the viewport box.

### 23.3 Why the ring is surface-aware

| Surface | Ring token | Colour | Ratio |
|---|---|---|---|
| `.surface-dark` (ink) | `--focus-ring-on-dark` | `--gs-gold` #D8C08A | **11.01:1** |
| `.surface-light` (cream) | `--focus-ring-on-light` | `--gs-ink` #0D0C0A | **17.04:1** |
| Product tile ground `#EBE6DC` | `--focus-ring-on-light` | ink | ~16.5:1 |

**Gold cannot be the ring on cream.** It measures **1.55:1** on warm cream and **1.43:1** on the tile cream — far below the **3:1** a focus indicator must reach against adjacent colour. A gold ring on the New Drop band would be invisible to every user, which is worse than no custom ring at all because it replaces the browser default.

A component never chooses its ring. `.surface-light` reassigns `--focus-ring` to `--focus-ring-on-light` and `.surface-dark` reassigns it to `--focus-ring-on-dark`; the control inherits. This is the same mechanism that stops gold landing on cream anywhere else in the system.

**Edge case — indicators that straddle a boundary.** A sticky header scrolling over a cream band, or a control on a photograph whose local luminance varies, can put one ring colour against both grounds. *Recommendation: add a `--focus-ring-companion` token so a two-tone ring (2px ink plus 2px cream, or the reverse) can be specified for those cases; the token file currently has only the two single-colour rings.*

### 23.4 Never remove without replacing

`outline: none` and `outline: 0` are prohibited unless the same rule substitutes an equally visible indicator in the same declaration block. Acceptable substitutions are a `box-shadow` ring of at least `--focus-width` meeting 3:1 against both the control and its ground, or a background inversion that itself meets 3:1. A substitution that relies on colour alone, or on gold over a light surface, is not acceptable (spec §27).

### 23.5 Elements that must show focus

| Element | Where | Ring source |
|---|---|---|
| Primary nav links | header (lines 71-72) | `--focus-ring-on-dark` |
| Utility controls: search, account, cart | header (lines 76-78) — currently `<img>`, not focusable | `--focus-ring-on-dark` |
| Menu trigger | header (line 75) — currently a `<span>` | `--focus-ring-on-dark` |
| Menu close control and every item in the panel | mobile menu (§19.6) | `--focus-ring-on-dark` |
| Announcement link, if present | announcement bar (line 58) | `--focus-ring-on-dark` |
| Skip link | above the announcement bar | `--focus-ring-on-dark` |
| Product card link | New Drop band, light surface | `--focus-ring-on-light` |
| Colour swatches | product card (line 116) — currently unfocusable `<span>`s | `--focus-ring-on-light` |
| All buttons and text CTAs | anywhere (lines 104, 132) | inherited from the surface class |
| All form controls: input, select, checkbox, radio, textarea, quantity +/− | spec §15 | inherited |
| Cart drawer controls: quantity, remove, checkout | later phase | inherited |
| Footer links and social marks | footer (lines 160-161) | `--focus-ring-on-dark` |
| Accordion and disclosure summaries | later phase | inherited |
| Pagination, filter and sort controls | later phase | inherited |

### 23.6 Focus management for the menu and drawers

The primary nav is removed below `--bp-lg` (the prototype does it at `display:none!important`, 900px query, line 30), so the menu panel is the only navigation at those widths and its focus behaviour is not optional:

1. On open, focus moves into the panel — to the close control or the first item.
2. Focus is trapped inside the panel while it is open; `Tab` cycles within it.
3. Content behind the panel is `inert` or `aria-hidden`, so it is not reachable by screen reader or keyboard.
4. `Escape` closes the panel.
5. On close, focus returns to the trigger that opened it.
6. The same five rules apply to the cart drawer and to any modal.

### 23.7 Skip link

There is no skip link and no `<main>` today; the only landmarks are `nav` and `contentinfo` (A11Y-02, audit line 2397). The system requires a skip link as the first focusable element, visually hidden until focused, then visible over the announcement bar at `--z-modal`, on `--color-bg-primary` with `--color-text-primary` and the dark-surface ring, at `--target-min` height. It targets the `<main>` landmark that §24.4 requires.

## 24. Accessibility Rules

These are the standard every later phase must meet. The acceptance bar is **WCAG 2.2 Level AA**. Nothing below is a description of the current site; the current site fails most of it.

### 24.1 Contrast

**Verified safe pairings** (all AA or better, from the brief's contrast matrix):

| Pairing | Ratio | Grade |
|---|---|---|
| cream `#F3EFE6` on ink `#0D0C0A` | 17.04:1 | AAA |
| ink on cream | 17.04:1 | AAA |
| gold `#D8C08A` on ink | 11.01:1 | AAA |
| white `#FFFFFF` on ink | 19.55:1 | AAA |
| `--gs-cream-200` `#E9E4D8` on ink | 15.41:1 | AAA |
| stone `#BDB6A8` on ink | 9.70:1 | AAA |
| gold hover `#E6D3A6` on ink | 13.25:1 | AAA |
| gold-strong `#82672B` on cream | 4.66:1 | AA |
| muted-on-light `#5F5A50` on cream | 5.97:1 | AA |
| olive `#4B5443` on cream | 6.91:1 | AA |

White is not a palette token and is listed only because spec §28 names the pairing; `--color-text-primary` cream remains the text colour on dark surfaces.

**Prohibited pairings**

| Pairing | Ratio | Rule |
|---|---|---|
| gold `#D8C08A` on cream `#F3EFE6` | **1.55:1** | never, at any size, for text, icons or borders |
| gold on the tile cream `#EBE6DC` | **1.43:1** | never — this is the product tile ground (line 109) |
| stone `#BDB6A8` on cream | **1.76:1** | use `--color-text-inverse-muted` #5F5A50 instead |

**The gold prohibition.** `--color-accent` is a dark-surface accent only. On light surfaces the accent role is `--color-accent-strong`. `.surface-light` enforces this by reassigning `--accent-current`; components must reference `--accent-current` rather than picking a colour.

**Minimums.** Normal text 4.5:1. Large text (≥24px, or ≥19px bold) 3:1. **Non-text UI components and their boundaries 3:1** — this covers focus rings, input borders, swatch rings, toggle states and icon-only controls. Contrast is never the sole carrier of meaning: colour-only state (selected, error, current) always has a text or ARIA counterpart.

**Worked example from the source.** The cream swatch's fill is 1:1 against the cream band and it is separated only by an `rgba(0,0,0,.25)` border measuring ~1.8:1, below the 3:1 required for a non-text UI component (A11Y-05, audit line 1671). Three swatches per product are rendered from `['#0d0c0a', '#f3efe6', '#4b5443']` (lines 175-177); the cream one is effectively invisible on the cream band and has no accessible name (audit line 2399). The system's answer is the `--color-border-inverse` ring plus the named-and-pressed swatch of §22.4.

**Composited contrast.** Text over photography is measured against the composited pixel at its worst point, not against the scrim's nominal value. Three nav links measure 2.4-2.9:1 over open sky (A11Y-03, audit line 2335), which is what makes the header backing of §19.3 mandatory.

### 24.2 Touch targets

| Token | Value | Rule |
|---|---|---|
| `--target-min` | 44px | the usability target for every interactive element |
| `--target-min-aa` | 24px | WCAG 2.2 SC 2.5.8 floor; never the design goal |

Measured today: the hamburger is **22 × 16** (line 75; the 900px query sets `gap:5px`, line 31) — it fails 44 on both axes and fails the 24px floor on its height. Utility icons are **24 × 24** (lines 76-78) — exactly at the AA floor, nowhere near the usability target. Swatches are **16 × 16** (line 116) — below both.

Rules:

1. Every interactive element has a hit area of at least `--target-min` 44 × 44, regardless of how small its visible mark is. The swatch stays 16px visually; its hit box is 44px.
2. Adjacent targets are separated by at least `--space-2` 8px of non-interactive space, or their hit boxes are enlarged until they are.
3. An icon-only control is a box with a glyph centred in it, never a bare glyph (§18.5).
4. Targets are not reduced at any breakpoint. If a row cannot hold four 44px targets at 375px, an item moves into the menu panel (§19.6) — it is not shrunk.

### 24.3 Focus

Per §23 in full: `:focus-visible`, 2px at 2px offset, surface-aware ring, gold prohibited on light, never removed without an equally visible replacement, focus trapped and returned for the menu and drawers, skip link first in the tab order.

### 24.4 Semantics

- The page has `<header>`, `<main>`, `<nav>` and `<footer>`. Today it has no `<header>` and no `<main>`; the nav lives inside the hero section and the four `<section>` elements have no accessible name, so they expose as generic containers (A11Y-02, audit line 2397; `data-screen-label` is editor metadata and names nothing).
- Every control is a `<button>` or an `<a>` according to what it does. An `<img>` is not a control and a `<span>` is not a control (A11Y-01, audit line 2334). The prototype contains zero `<button>` elements.
- Sections that are landmarks carry an accessible name via `aria-labelledby` pointing at their own heading.
- State lives in ARIA: `aria-expanded` on the menu trigger, `aria-controls` pointing at the panel, `aria-current="page"` on the current nav item, `aria-pressed` or a radio group for swatches, `aria-live` for cart and form status messages.

### 24.5 Names and labels

- Every icon-only control has a text accessible name that describes its action, not its picture: "Open menu", "Search", "Cart, 2 items".
- `aria-label` is only valid on an element with a role that supports naming. `aria-label="Menu"` on a role-less `<span>` (line 75) is ignored by ARIA, so the control is invisible to assistive technology even before its handler exists (A11Y-07, audit line 2478).
- Swatches are named controls in a named group ("Colour: Olive"), not unlabelled spans (A11Y-05, audit line 2399).
- Decorative glyphs are `aria-hidden="true"` with empty `alt`. The CTA arrow is decorative: unhidden, both CTAs are announced as "View All Products rightwards arrow" (A11Y-06, audit line 2477).
- Link text stands alone out of context. "Learn more" and a bare arrow do not.

### 24.6 Heading order

- Exactly one `<h1>` per page. No level is skipped.
- Product names and value titles are headings at the correct level, not `<div>`s. Today the outline stops at one `<h1>` and two `<h2>`s, so heading navigation never reaches a product or a value (A11Y-08, audit line 2400).
- A `<br>` inside a heading must not fuse two words into one accessible name: `The<br>Faithful` (line 101) reads as "TheFaithful" in a heading list. Line breaks in headings are achieved without destroying the text, or the accessible name is supplied separately.
- Heading level is chosen by position in the outline, never by desired size. Size comes from the type scale.

### 24.7 Alt text

Of the 12 image tags in the source, 8 are wrong, redundant or generic (A11Y-09, audit line 2401). The rules:

| Image class | Rule |
|---|---|
| Decorative icon beside a visible label | `alt=""` and `aria-hidden="true"` |
| Icon-only control | the name describes the action, and the control — not the image — carries it |
| Product photograph | describes the garment, not the template variable and not the name already printed below it |
| Hero / story photograph | describes what is depicted; never repeats headline copy and never carries copy baked into the image |
| Logo | the brand name once, in the header only; the footer logo is decorative |
| Social mark | names the platform, with the link's destination clear from its own name |

### 24.8 Motion

Per §21.5: `prefers-reduced-motion: reduce` is honoured; no content is reachable only through motion; nothing auto-plays, auto-advances or loops; no parallax; no animation exceeds `--duration-slow` 400ms. The prototype has no reduced-motion support at all today (brief: measured).

### 24.9 Zoom and reflow

- **Reflow (SC 1.4.10).** Content reflows to a single column at a 320 CSS-pixel equivalent width with no horizontal scrolling. Fixed-height containers around tracked uppercase are prohibited: 0.22em and 0.30em tracking expands the line, and a fixed box clips it when text scales.
- **Text spacing (SC 1.4.12).** Layout survives increased line height, letter spacing and word spacing. This is the reason no component's height is derived from a string's expected length.
- **Zoom is reflow.** A desktop viewport at 200% zoom resolves to roughly half its CSS width and must receive the ladder tier appropriate to that width. The RESP-12 defect is that the prototype's single 900px switch makes that tier a bare phone layout with no navigation at all — a 1440 desktop reaches it at 160% zoom (1440 / 1.6 = 900 CSS px) and any laptop up to 1800px reaches it at 200% (audit line 2443). The §25.2 ladder fixes it by adding 480, 768 and 1024 tiers, not by resisting reflow.
- **Orientation.** No layout is locked to portrait or landscape.
- The `overflow: hidden` on the prototype's wrapper (line 55) masks anything that would extend past it (brief), so "no horizontal overflow" cannot be claimed from observation alone; overflow is tested with that mask removed.

### 24.10 The standard later phases must meet

| Area | Requirement | Governing SC |
|---|---|---|
| Text contrast | 4.5:1 normal, 3:1 large | 1.4.3 |
| Non-text contrast | 3:1 for controls, boundaries and focus rings | 1.4.11 |
| Colour alone | never the sole carrier of state | 1.4.1 |
| Keyboard | every control reachable and operable, no traps outside managed dialogs | 2.1.1, 2.1.2 |
| Focus visible | custom ring, surface-aware, never obscured | 2.4.7, 2.4.11 |
| Target size | 24px floor, 44px target | 2.5.8 |
| Name, role, value | every control exposes all three | 4.1.2 |
| Headings and landmarks | complete outline, named regions, skip link | 1.3.1, 2.4.1, 2.4.6 |
| Reflow and text spacing | 320px equivalent, no clipping | 1.4.10, 1.4.12 |
| Motion | reduced-motion honoured, nothing motion-only | 2.3.3 |

A browser and device support matrix is **BUSINESS INFORMATION REQUIRED**; it governs how `:has()`, container queries, `text-wrap: balance` (line 84) and `aspect-ratio` (line 109) may be used and what each must degrade to.

## 25. Responsive Rules

### 25.1 Mobile-first, and the rule against desktop-down scaling

Base styles describe the **phone**. Every query is `min-width`. A tier may only add — it never undoes a base rule.

The prototype does the opposite: the base inline styles describe the 1440 layout inside a `max-width:1440px` wrapper (line 55), and two `max-width` queries re-flow every section using **55 `!important` declarations**, all inside those queries (brief; audit lines 235, 251). Because every layout property is set inline at specificity 1,0,0,0, the responsive layer can only win by force. That inversion is the direct cause of three of the four defects in §25.6.

Rules that follow:

1. No `!important` anywhere except the reduced-motion block (§21.5).
2. No layout value in a `style=""` attribute. Layout lives in classes so a tier can extend it.
3. Mobile is designed, not derived. A phone layout is not the desktop composition with columns collapsed — the hero, the story and the New Drop band each have their own mobile arrangement (spec §35).
4. No fixed section heights. The prototype's hero `min-height:620px` (line 64) and story `min-height:520px` (line 125) are replaced by content plus `--section-pad-block`.
5. Layout hooks must exist. A rule targeting a hook no element carries is dead weight and a silent defect (line 19).

### 25.2 The breakpoint ladder

| Tier | Token | Width | Role |
|---|---|---|---|
| Base | — | < 480px | phone: 375 / 390 / 430 |
| Small | `--bp-sm` | 480px | large phone and phablet |
| Medium | `--bp-md` | 768px | tablet portrait |
| Large | `--bp-lg` | 1024px | tablet landscape and small laptop; **primary nav returns here** |
| XL | `--bp-xl` | 1280px | desktop |
| 2XL | `--bp-2xl` | 1440px | wide desktop; content ceiling |
| Above 2XL | — | > 1440px | sections full-bleed, content constrained by `--container-standard` / `--container-wide` |

Custom properties cannot be used inside media query conditions; the tokens are the reference values, written literally in the query (token file, §8 note). The prototype has only two queries, 900 and 520 (brief), and no tier at all between 901 and 1440 (RESP-08, audit line 2510).

### 25.3 What changes at each tier

**Header** (§19)

| Tier | Rule |
|---|---|
| Base | `--header-height-mobile` 88px; logo `--logo-height-mobile` 56px; primary list collapsed to the menu trigger; trigger and cart always visible; search and account move into the panel if the row cannot hold four `--target-min` boxes with `--space-2` between them |
| `--bp-md` | same height and logo; all utilities visible in the row |
| `--bp-lg` | primary nav returns; header grows to `--header-height-desktop` 122px; logo `--logo-height-desktop` 78px; `--nav-gap` 40px |
| `--bp-2xl`+ | unchanged; header content constrained by `--container-standard` while the header ground is full-bleed |

**Hero**

| Tier | Rule |
|---|---|
| Base | single column, media first at `--hero-aspect-mobile` 4/5 — replacing the uncapped `height:62vw; min-height:320px` band (900px query, line 21); scrim anchored to the **media box**; copy below at `--gutter`; side caption merged into the copy column, never trailing it |
| `--bp-md` | same stacked arrangement, media may widen to 3/2; type steps up through its clamps |
| `--bp-lg` | overlay composition returns: copy over media with `--scrim-hero-horizontal`; `--scrim-header` over the header band (§19.3) |
| `--bp-xl` | the third side-caption column returns (the `1.1fr 1.1fr .7fr` grammar, line 64) |
| Above `--bp-2xl` | media full-bleed to the viewport; copy constrained to `--container-standard`; height fluid, never the fixed 620px of line 64 |

**Product grid**

Standalone collection grid:

| Tier | Columns |
|---|---|
| Base | 2 |
| `--bp-sm` | 2 |
| `--bp-md` | 2 (3 permitted for a dense catalogue, subject to the never-orphan check below) |
| `--bp-lg` | 3 |
| `--bp-xl` | 4 |
| `--bp-2xl`+ | 4 |

Homepage New Drop band (a fixed count of three, lines 175-177, beside a copy column at `--split-30-70`, line 98):

| Tier | Arrangement |
|---|---|
| Base → `--bp-md` | copy column stacks above; band is **1 column** |
| `--bp-lg` | copy stacks above; band is **3 columns** full width — ~288px tiles at 1024 |
| `--bp-xl`+ | `--split-30-70` returns; band is **3 columns** beside the copy — ~265px tiles at 1280 |

Governing rules: a grid sharing its row with a copy column **drops one column** against the standalone ladder, floored at 1; and a band whose item count is fixed at three **never resolves to two** — it steps from one to three. Gap is `--product-grid-gap` 24px, or `--grid-gap-large` 32px for the band (normalising the prototype's 36px, line 106). No column count may render a tile wider than its source; today's 235px crops make that an asset requirement for the phase that supplies photography (**BUSINESS INFORMATION REQUIRED**), not a licence to upscale.

**Story**

| Tier | Rule |
|---|---|
| Base | single column, media first at 4/5 — replacing `height:60vw; min-height:280px` (900px query, line 36); then eyebrow, heading, paragraph, CTA; the side caption merges above the CTA or is omitted by the section's own setting — it never trails the button as a 145px orphan (audit line 1283) |
| `--bp-lg` | `--split-40-60` returns (`0.9fr 1.6fr`, line 125) |
| `--bp-xl` | the side caption column returns |
| All tiers | paragraph measure is 45-75 characters, capped by `--container-narrow` 760; the prototype's fixed `max-width:320px` (line 131) is roughly 40 characters at the new 16px body and is replaced by a character-based measure |

**Values**

| Tier | Rule |
|---|---|
| Base | 2 × 2 grid; glyph `--icon-xl` 44px; title `--type-label-size`, sub `--type-caption-size` (raised from 11px, line 147); tile padding `--space-7` block / `--gutter` inline (normalising `44px 24px`, line 144) |
| `--bp-lg` | 4 columns (line 142) |
| Separators | the `border-right` hairline (line 144) is drawn **between** columns only, never on the last tile in a row; at base it becomes a bottom hairline between rows |

**Footer**

| Tier | Rule |
|---|---|
| Base | single column stacked: logo, tagline, social row, sign-off; `--space-5` between groups; `--gutter` inline |
| `--bp-md` | two columns |
| `--bp-lg` | the `space-between` row returns (line 153); the 1px vertical divider (line 163) appears only here — below it is hidden, not left floating |
| All tiers | logo `--logo-height-footer` 56px; social marks `--icon-lg` 28px inside `--target-min` 44px boxes, `--space-5` apart (normalising the 18px gap, line 159); block padding `--space-5` (normalising 26px, line 153) |

**Announcement bar** — per §20: `--announcement-height` 40px with `--gutter` inline padding at every tier; stacked, auto-height below `--bp-sm`.

**Buttons**

| Tier | Rule |
|---|---|
| Base | full-width block; `--space-4` block / `--space-5` inline padding (normalising `padding:16px 26px`, line 104); minimum height `--target-min` 44px; label `--type-label-size` 12px / `--type-label-ls` 0.22em / `--type-label-weight`; icon at `--icon-sm` with `--space-3` gap (the prototype's `gap:12px`, line 104); two adjacent buttons stack with `--space-3` between |
| `--bp-md`+ | `inline-flex`, width by content; adjacent buttons sit inline with `--space-4` between |
| All tiers | the tracked label wraps by reducing the line width, **never** by reducing tracking (§25.5); the button's height is never fixed below its content |

**Forms**

| Tier | Rule |
|---|---|
| Base | single column, stacked fields, labels **above** the control; control height `--target-min` 44px; input text at `--type-body-size` 16px so focus does not trigger zoom on iOS; label at `--type-label-size` with `--type-label-ls`; `--radius-sm` 2px; 1px `--color-border-inverse` on light, `--color-border` on dark |
| `--bp-md`+ | two-up **only** where a field pair is logically grouped (first/last name, city/postcode); everything else stays single column regardless of width, capped by the measure rule |
| All tiers | no fixed-height container around tracked type (§24.9); error text sits below its field in `--color-error` on light / `--color-error-on-dark` on dark and is never colour-only; the quantity selector is minus / field / plus, each `--target-min`, glyphs at `--icon-md`; the newsletter field and button stack at base and sit inline from `--bp-md` |

### 25.4 Section padding and gutters

| Token | Value | Use |
|---|---|---|
| `--section-pad-block` | `clamp(var(--space-7), 6vw, var(--space-10))` — 40px to 96px | default vertical rhythm for every band |
| `--section-pad-block-tight` | `clamp(var(--space-6), 4vw, var(--space-8))` — 32px to 48px | dense bands: values row, footer |
| `--gutter` | 24 / 32 / 48px | every band's inline padding, switched at `--bp-md` and `--bp-lg` by the token file's own two queries |

The fluid clamps mean vertical rhythm scales without a breakpoint, replacing the prototype's eight distinct hand-set section paddings (`12px 48px`, `22px 48px`, `170px 48px 56px`, `190px 48px 56px 0`, `48px 48px 44px`, `56px 48px`, `44px 24px`, `26px 48px` — brief: spacing). **Every band binds its inline padding to `--gutter`**; none carries its own value.

### 25.5 Responsive typography

1. Size is fluid through `clamp()`; the display and heading tokens already carry it (token file, §4).
2. **No breakpoint-specific font-size overrides.** If a size needs a tier-specific value, the clamp is wrong.
3. **Tracking is never reduced to make text fit.** `--type-label-ls` 0.22em and `--type-eyebrow-ls` 0.30em are fixed; text wraps to another line instead. Size and tracking travel together as one token pair, always.
4. The mobile floor is 12px for persistent interface text and 16px for body copy (token file, §4). The prototype's 9px badge (line 78), 11px announcement (line 58), 11px value sub (line 147) and 11px footer lines (lines 156, 164) are all below it. Confirmation against brand intent is **BUSINESS INFORMATION REQUIRED**.
5. Line breaks in display type are a content decision, not a size decision. `--type-display-xl-size` reaches its 112px ceiling and stays there; whether the h1 sets on two lines as the mockup shows or three as the build does (brief) is settled by `text-wrap: balance` (line 84) and by the copy, whose browser support is **BUSINESS INFORMATION REQUIRED**.
6. Long tracked uppercase blocks take `--type-tagline-lh` 1.70 (lines 87, 93).

### 25.6 Defects the system must not reproduce

**1. The hero fade anchored to the wrong box.** Below 900px `[data-r=hero-fade]` keeps `top:0; height:max(62vw,320px)` measured from the **section** (900px query, line 22), while the image sits below the 88px in-flow nav (`order:-2`, line 29). The gradient therefore reaches solid black 88px above the image's bottom edge, producing a black band and a hard seam at every phone and tablet width (brief; audit lines 438, 1096). **Rule:** a scrim is a child of the element it darkens and is sized by that element, never by an ancestor the header also occupies. This is the same rule that makes the header backing of §19.3 work.

**2. The dead gutter hook.** The 900px query's first rule targets `[data-r=pad]` and no element carries that attribute (line 19; audit line 436), so the announcement bar keeps its inline `48px` between 521 and 900px while every other band drops to 24px. **Rule:** inline padding is bound to `--gutter` on every band; no band carries its own value, and no rule may target a hook that does not exist in the markup.

**3. The orphaned tablet product.** At 768 the prototype forces two columns (900px query, line 34), so the third of three products sits alone on row 2 (brief: measured responsive behaviour). Under §25.3 the New Drop band drops one column against the standalone ladder, so at 768 it resolves to a single column and the orphan cannot recur. The standalone grid is the only place a count of three can orphan, so **a band whose fixed count is three must not be placed on a two-column tier** — it steps from one column to three at `--bp-lg`.

**4. The missing 901-1440 tier.** There is no breakpoint between 901 and 1440, so the fluid three-column grid is squeezed to ~230-250px: at 920 the eyebrow, the product names and the "View All Products" CTA all wrap, and at 1024 "Signature Oversized Tee" wraps to two lines and its price drops a line below the other two (RESP-08, audit line 2510). **Rule:** the ladder carries `--bp-lg` 1024 and `--bp-xl` 1280 tiers, and the New Drop band does not attempt three columns beside a copy column until `--bp-xl`, where the tile measures ~265px.

**Related, same root cause.** The hero's "A HIGHER PURPOSE." caption becomes an orphan block below 900 (audit line 1066, HERO-04) and the story's side caption becomes a 145px orphan after its CTA (audit line 1283). §25.3 assigns both captions a deliberate mobile position rather than letting source order decide.

### 25.7 Test widths

Every later phase verifies at **320, 375, 390, 430, 480, 768, 900, 901, 1024, 1280, 1440 and 1920**, and additionally at **1440 × 160% zoom** (= 900 CSS px) and **1440 × 200% zoom** (= 720 CSS px), the two zoom levels that expose the RESP-12 navigation cliff (audit line 2443). 900 and 901 are tested as a pair because that is where the prototype's only structural switch sits. At 1920 the check is that bands go full-bleed and content constrains, not that a 1440 box sits between 240px dark gutters (line 55; spec §11).

## 26. Editorial Design Rules

God Squad is not a template with editorial decoration applied. It is a fashion editorial that happens to sell. Every rule below exists to keep that true while the site grows from one homepage to a catalogue.

### 26.1 The recurring composition

Every editorial band draws from the same set of parts. A band uses some of them, never all of them, and never in a different order.

| Part | What it is | Tokens | Prototype basis |
|---|---|---|---|
| Eyebrow | 2–4 tracked uppercase words naming the band | `--type-eyebrow-size` 13px, `--type-eyebrow-ls` 0.30em, `--type-eyebrow-weight` 500, `--accent-current` | lines 83, 100, 129 |
| Display headline | 2–4 words, hard-broken with `<br>`, uppercase Playfair 900 | `--type-display-xl-*` (hero), `--type-display-l-*` (commerce), `--type-display-m-*` (story) | lines 84, 101, 130 |
| Accent word | At most **one** word of the headline in `--accent-current` | `--accent-current` | line 84, `Faith.` |
| Hairline rule | A 1px separator that ends the headline group | `--border-width`; `--accent-current` for the one accent rule per band (line 86), `--color-border-current` otherwise — lines 92 and 137 are cream and line 102 is ink today | lines 86, 92, 102, 137 |
| Tagline stack | 2–4 short tracked uppercase lines, hard-broken | `--type-body-sm-size` 14px, `--type-eyebrow-ls` 0.30em, `--type-tagline-lh` 1.70 | lines 87, 93 |
| Caption rail | A narrow tracked uppercase column at the band edge | `--type-caption-size` 12px, `--type-caption-ls` 0.20em | line 136 — see §29.4 |
| Editorial image | Full-bleed, or 60–70% of the band, always scrimmed | `--scrim-hero-horizontal`, `--scrim-top-heavy`, `--scrim-bottom`, `--scrim-header`; `--container-wide` | lines 65, 126 |
| Body paragraph | At most **one** per band, on a narrow measure | `--type-body-size` 16px, `--type-body-lh` 1.65 | line 131, the only `<p>` on the page |
| Script accent | Kaushan, rotated, at most once per page | `--type-script-size`, `--type-script-lh` 1.10 | line 91, `rotate(-8deg)` |
| Minimal CTA | At most one per band; a band may carry none | `--type-label-size` 12px, `--type-label-ls` 0.22em, `--radius-sm` | lines 104, 132 |

The hero (lines 82–93) is the full expression: eyebrow, headline with accent word, verse, gold hairline, tagline stack, script accent, caption-side rule — and **no CTA**. That absence is deliberate and is the model for restraint, not an omission to be corrected.

### 26.2 Measure, whitespace and the header offset

- Body copy is capped at 60–70 characters. `--container-narrow` 760px is the long-form reading container.
- The prototype's story paragraph is capped at `max-width:320px` (line 131) — roughly 40 characters at `--type-body-size` 16px. That is an **editorial caption measure**, not a reading measure. It is correct for a three-sentence brand statement beside an image and wrong for anything longer. Recording the distinction is why a `--measure-*` token is recommended (see token gaps).
- Vertical rhythm is `--section-pad-block` `clamp(40px, 6vw, 96px)`, and `--section-pad-block-tight` `clamp(32px, 4vw, 48px)` where a band abuts another of the same surface.
- The hero's 170px and 190px top paddings (lines 82, 90) are **not** rhythm. 170px resolves exactly to `--header-height-desktop` 122px plus `--space-8` 48px. The side column's 190px is a 20px optical drop with no scale value; it normalises to `--header-height-desktop` plus `--space-9` 64px = 186px. Any band that carries the header over it inherits this offset; no other band does.
- Whitespace is the second most expensive material on the page after photography. A band that fills its column is wrong even when every token in it is correct.

### 26.3 Asymmetry, and the rule against symmetry everywhere

1. **Every editorial band is left-aligned.** Centring is permitted in exactly two places: inside a product card (line 108, `text-align:center`) and inside a value tile (line 144). Both are grid cells, not compositions.
2. **Three-track asymmetry is the signature.** The hero is `1.1fr 1.1fr .7fr` (line 64) and the story is `.9fr 1.6fr .4fr` (line 125) — in both cases copy / image window / caption rail. Neither is expressible with the token file's `--split-*` set, which is two-track only. Express the rail as `--split-40-60` plus a `minmax(170px, .4fr)` track, or add a `--split-rail` token (recommended; see token gaps).
3. **The image is offset, never centred behind the copy.** Line 126 places the story image at `left:30%; width:70%`. A centred image behind a left-aligned headline reads as a template.
4. **Two-track splits come from `--split-30-70` (line 98), `--split-40-60` (line 125), `--split-50-50` and `--split-60-40`.** A band that needs a ratio outside this set needs a reason recorded in its schema comment, not a new inline value.
5. The only permitted symmetry is a grid: the 4-up values strip (line 142) and the product grid (line 106).

### 26.4 Dark-to-light alternation as rhythm

The homepage runs announcement (dark, line 58) → header (transparent over dark, line 68) → hero (dark, line 64) → New Drop (**cream**, line 98) → Our Story (dark, line 125) → Values (dark, line 142) → footer (dark, line 153). One light band in seven.

That ratio is the rhythm, and it carries meaning: **dark is the editorial default; the light band is where the customer is asked to buy.** Rules:

1. Never two light bands adjacent. Cream is a punctuation mark; two in a row is a paragraph break in the wrong place.
2. Every dark↔light join is a **hard edge**. No gradient, no divider rule, no shadow. The colour change is the separator.
3. A band declares `.surface-dark` or `.surface-light` and never overrides a colour inside it. `--accent-current`, `--color-border-current` and `--focus-ring` are already surface-aware (token file, surface contexts), so no component needs a light/dark branch.
4. The hero's vertical scrim (line 66) terminates at `#0d0c0a 100%`, so the hero resolves to solid ink before the cream band begins. Any band that precedes a light band must resolve to its own ground first.
5. Values sits directly under Our Story, both dark. This is the only permitted dark-on-dark join, and it is marked by `border-top` and `border-bottom` at `--color-border` (line 142 uses `rgba(255,255,255,.1)`, which normalises to `--color-border`).

### 26.5 Restraint budgets

Luxury through restraint is enforced as a per-band budget, not as taste.

| Element | Budget per band | Basis |
|---|---|---|
| Gold | At most **two** of: eyebrow, one accent word, one hairline rule, one CTA fill. On `.surface-light`, gold is `--color-accent-strong` #82672B (4.66:1); `--color-accent` #D8C08A is 1.55:1 on cream and 1.43:1 on the tile cream and may never carry text, icons or borders there | contrast matrix; token file surface contexts |
| Gradients | One scrim per band, drawn from the four `--scrim-*` tokens. No decorative gradient anywhere | lines 66, 127 |
| Shadows | `--shadow-none`. `--shadow-elevated` is reserved for drawers, modals and a sticky header on scroll. `--shadow-subtle` is for inputs only | token file §10 |
| Radius | `--radius-none` everywhere, except `--radius-full` circles (swatches line 116, cart badge line 78) and `--radius-sm` on inputs and controls | prototype uses `50%` twice and nothing else |
| Borders | 1px (`--border-width`) only. `--border-width-strong` 2px is reserved for state, never decoration | lines 142, 144, 162 |
| Motion | Opacity and transform only, at `--transition-fast` or `--transition-medium`. `--hover-image-scale` is 1.03 and the token file's documented ceiling is 1.05 (token file line 292); God Squad uses 1.03 and treats 1.05 as the absolute maximum | token file §11 |
| Icons | At most three in the header (lines 76–78), one per value tile (line 145), two in the footer (lines 160–161). No decorative icon inside editorial copy | prototype |
| CTAs | One per band; a band may carry none. The hero ships with none | lines 82–93 |

A band that exceeds any budget is not "richer". It has left the system.

### 26.6 Visual reference board

A textual board, per spec §39. It is a decision aid for photography, copy and review — not a mood board to be reinterpreted.

| Axis | The reference | What it rules out |
|---|---|---|
| **Brand feel** | A Philippine streetwear lookbook (line 131) printed on uncoated stock: large silent images, four words of type per spread, one foil mark. Premium, faith-driven, editorial, cinematic, purposeful, community-oriented | Gloss. Hype layouts. Faith expressed through iconography rather than through restraint and the verse line (line 85) |
| **Colour** | Ink ground, one cream commerce band, a single gold mark. A dark gallery wall with one lit object | Gold-trimmed luxury templates. Gold on cream in any form. A second accent hue |
| **Typography** | Playfair Display 900 uppercase masthead against Jost tracked at 0.20–0.30em. Kaushan Script once per page, rotated (line 91) | Kaushan on navigation, buttons, prices or product information (spec §8). Dozens of near-identical styles — the prototype's 24 styles collapse to the 11 in §6 |
| **Layout** | Three-track asymmetry: copy, image window, caption rail (lines 64, 125). The image is offset, never centred (line 126). Whitespace is a material | Centred hero copy. Symmetrical two-up bands repeated down the page. A boxed 1440px wrapper with dark gutters (line 55) |
| **Interaction** | Nothing moves unless it was touched. 150–250ms, opacity and transform only, one hover state per element | Scroll-triggered reveals. Parallax. Carousels that move on their own. Zoom above `--hover-image-scale` |

**Not on record:** the only geographic statement anywhere in the project is line 131 — "God Squad is a Philippine streetwear brand built on faith, creativity, and community." No city, neighbourhood or scene is named. If the reference board is to name one, that is **BUSINESS INFORMATION REQUIRED**.

## 27. Ecommerce Design Rules

The editorial language is the reason a customer stays. It is never the reason they cannot buy. Every rule in §26 yields to the five questions below.

**Baseline.** The prototype has no commerce logic. The New Drop grid renders three literal product objects (lines 175–177) whose prices are built by string concatenation against a symbol-only `currency` enum prop (line 169, options `₱` / `$` / `€`). There is no availability state, no variant selection, no add-to-cart control and no product link anywhere on the page.

### 27.1 Question 1 — What is it?

| Rule | Detail |
|---|---|
| Element | The product title is a heading element wrapping a link to the product URL, never a bare `<div>` (line 112 today) |
| Type | `--type-label-size` 12px, `--type-label-ls` 0.22em, `--type-label-weight` 600, uppercase (line 112) |
| Measure | Two lines maximum before truncation. Phase 1 recorded the tee name wrapping at 1024 and the price misaligning as a result (brief: measured responsive behaviour) |
| Alignment | Centred inside the card (line 108) — one of the two permitted exceptions to §26.3 |
| Floor | Title text never drops below `--type-label-size` 12px on any viewport. It is persistent interface text |
| Never | Vendor name, SKU, rating, review count, "quick view" overlay, or a second line of marketing copy. Spec §16 |

The card gives the customer **one** name and **one** destination. Everything else is on the product page.

### 27.2 Question 2 — What does it cost?

| Rule | Detail |
|---|---|
| Source | Price is rendered through Shopify's money filter against the store's money format, never by string concatenation (TECHNICAL-4). The prototype's `cur + '1,290'` pattern (lines 175–177) cannot express a sale price, a price range, a currency conversion or a locale |
| Type | `--type-price-size` 15px (raised from the prototype's 14px, line 113), `--type-price-weight` 600, `--type-price-ls` **0em** |
| The tracking rule | Tracked uppercase is the brand signature and it **never touches numerals**. `--type-price-ls` is 0em by design; a tracked price is unreadable at a glance and defeats question 2 |
| Contrast | On `.surface-light`, price is `--color-text-inverse` #0D0C0A (17.04:1). On `.surface-dark`, `--color-text-primary` #F3EFE6 (17.04:1). Price is never muted and never gold |
| Sale price | Current price in the full-contrast token; the compare-at price beside it in `--color-text-inverse-muted` #5F5A50 (5.97:1) on light or `--color-text-muted` #BDB6A8 (9.70:1) on dark, with a line-through. Never a red "SALE" flash |
| Price range | `From ₱X` rather than a hidden minimum. The `From` prefix takes `--type-label-*`, the numeral takes `--type-price-*` |
| Glyph risk | Jost carries neither `₱` nor `→` (brief), so both currently fall back to a per-platform face. The peso glyph sits in the single most legibility-critical string on the page. Resolving this is **BUSINESS INFORMATION REQUIRED** (§31.7) |

### 27.3 Question 3 — Is it available?

Availability is communicated by the state of the add-to-cart control first and by a badge only when the control is not visible (the card in a grid). Badges are text, never colour alone (WCAG 2.2 SC 1.4.1).

| State | On `.surface-dark` | On `.surface-light` | Never |
|---|---|---|---|
| In stock | No badge. Availability is implied by an enabled add-to-cart | Same | A green "In stock" badge |
| Low stock | `--color-warning-on-dark` #D8C08A, 11.01:1 on ink | `--color-warning` #82672B, 4.66:1 on cream | `--color-accent` on cream, 1.55:1 |
| Sold out | `--color-text-muted` #BDB6A8, 9.70:1 on `--color-bg-primary`, with a 1px `--color-border-current` outline | `--color-text-inverse-muted` #5F5A50, 5.97:1 on cream, with a 1px `--color-border-current` outline | `--gs-stone` on cream, 1.76:1 |
| Pre-order / coming soon | `--color-text-primary` #F3EFE6, 17.04:1, with a 1px `--color-border-current` outline | `--color-text-inverse` #0D0C0A, 17.04:1, same outline | A gold fill, which spends the band's whole gold budget on a status |

**Measurement note.** If a badge is ever placed on `--color-surface-raised` #2A2823 rather than on `--color-bg-primary`, that ratio is not in the Phase 2 contrast matrix and must be measured before use. Badge type is `--type-caption-size` 12px, `--type-caption-ls` 0.20em, uppercase — the 12px floor applies; a sold-out state is persistent interface text.

### 27.4 Question 4 — How do I choose a variant?

| Rule | Detail |
|---|---|
| Colour | Swatches, 16px circles at `--radius-full` with a 1px ring (line 116, `rgba(0,0,0,.25)` — normalises to `--color-border-inverse` on light and `--color-border` on dark). Recommended tokens: `--swatch-size` and `--swatch-ring` (see token gaps) |
| Size and other options | Text chips at `--type-label-*`, `--radius-none`, 1px `--color-border-current`, minimum touch target `--target-min` 44px. Never a native `<select>` on a product page where the options are fewer than eight |
| Selected state | 1px becomes `--border-width-strong` 2px in the surface's text colour, **plus** an accessible name change (`aria-pressed` / a checked radio). This is the one place `--border-width-strong` is permitted (§26.5) |
| Colour alone is never the signal | A swatch carries an accessible name. #0D0C0A, #F3EFE6 and #4B5443 (lines 175–177) are indistinguishable to a screen reader and two of them are near-invisible against their own surface |
| Unavailable variant | Struck-through chip at `--color-text-muted` / `--color-text-inverse-muted`, still focusable, with the state in its accessible name. Never removed from the DOM |
| Card behaviour | The card shows swatches as **information** (this comes in three colours), not as a control. Variant selection happens on the product page. The prototype's three swatches per card (lines 175–177) are correct as information and must not become buttons |

### 27.5 Question 5 — How do I add it to cart?

| Rule | Detail |
|---|---|
| Presence | One primary add-to-cart per product page, above the fold at every width in §25, never behind a hover reveal |
| Style | Primary button: `--color-bg-primary` fill, `--color-text-primary` label on light surfaces; inverted on dark. `--type-label-size` 12px / `--type-label-ls` 0.22em / weight 600, padding `--space-4` `--space-5` (line 104 uses `16px 26px`), `--radius-sm` |
| Gold | Gold fill is permitted for **one** CTA per page and only on a dark surface, where #D8C08A is 11.01:1 on ink (line 132 today). It is never the add-to-cart on a cream product page |
| Target | `--target-min` 44px minimum height at every width. The prototype's 22×16 hamburger and 24×24 utility icons (lines 75–78) are the failure mode to avoid |
| Focus | `--focus-width` 2px at `--focus-offset` 2px in `--focus-ring`, which resolves to gold on dark and ink on light. Never removed |
| Feedback | State change is textual and announced. Motion is limited to `--transition-fast` on opacity and background |
| Never | An add-to-cart on the card that appears on hover. It is invisible on touch, unreachable by keyboard until focused, and it puts a commerce control inside an editorial composition |

### 27.6 Where editorial yields to commerce

Six rules, in force order. When §26 and §27 conflict, §27 wins.

1. **Tracking stops at numerals.** Prices, quantities, sizes and order numbers are untracked (`--type-price-ls` 0em). The 0.22–0.30em signature applies to words only.
2. **Nothing load-bearing is hard-broken.** The `<br>` composition of lines 84, 87, 91, 93, 101, 130 and 136 belongs to headlines and taglines. A product title, price or availability string is never hard-broken and never `text-wrap: balance`d into an unexpected shape.
3. **No scrim over commerce text.** The four `--scrim-*` tokens apply to editorial imagery only. A price or a title never sits on a gradient; it sits on a flat surface token.
4. **Grids are symmetrical on purpose.** Asymmetry (§26.3) governs the band; inside the product grid every card is equal. `--product-grid-gap` is 24px, with 4 / 3 / 2 / 1 columns from `--bp-xl` down. The prototype's 36px product gap (line 106) normalises to `--grid-gap-large` 32px in the token file's comment; the tighter 24px is the system value and the comment is recorded as needing correction (see token gaps).
5. **One ratio for the whole catalogue.** `--product-aspect` 1/1 is the default and `--product-aspect-wide` 4/5 the editorial alternative — chosen once at theme level (`product_image_ratio`, §28.1), never per section and never per product. Mixed ratios are what force a `contain` fit on the `--color-surface-tile` ground and break the grid's rhythm.
6. **Editorial copy never replaces a commerce label.** "More Than Clothing." (line 91) is a brand statement. It is not a button label, a category name or a product title, and no commerce control borrows the script face.

## 28. Shopify Theme Settings Recommendations

The theme editor is a merchant's tool for changing content and brand marks. It is not a design tool. Every setting exposed is a rule the system can no longer guarantee, so the set is deliberately small: **17 theme-level settings**, against a token file of 164 tokens.

### 28.1 The theme settings to expose

| Group | Setting | Type | Default | Drives |
|---|---|---|---|---|
| Logo | `logo` | `image_picker` | — | The wordmark (lines 69, 155) |
| Logo | `logo_height_desktop` | `range` 56–96, step 2 | 78 | `--logo-height-desktop` (line 69) |
| Logo | `logo_height_mobile` | `range` 40–72, step 2 | 56 | `--logo-height-mobile` |
| Colours | `color_ink` | `color` | `#0D0C0A` | `--gs-ink` |
| Colours | `color_cream` | `color` | `#F3EFE6` | `--gs-cream` |
| Colours | `color_gold` | `color` | `#D8C08A` | `--gs-gold` |
| Typography | `type_display_font` | `font_picker` | `playfair_display_n9` | `--font-display` |
| Typography | `type_body_font` | `font_picker` | `jost_n4` | `--font-body` |
| Typography | `type_script_font` | `font_picker` | see §28.2 | `--font-script` |
| Layout | `page_width` | `range` 1200–1560, step 40 | 1440 | `--container-standard` |
| Controls | `control_radius` | `range` 0–4, step 1 | 2 | `--radius-sm` |
| Announcement | `announcement_height` | `range` 32–56, step 4 | 40 | `--announcement-height` |
| Product | `product_image_ratio` | `select`: square, portrait | square | `--product-aspect` / `--product-aspect-wide` |
| Social | `social_instagram_link` | `url` | — | Footer and any social row |
| Social | `social_facebook_link` | `url` | — | Footer and any social row |
| Social | `social_tiktok_link` | `url` | — | Footer and any social row |
| Social | `social_youtube_link` | `url` | — | Footer and any social row |

### 28.2 Why each one is exposed

**Logo and its heights.** A merchant will replace the wordmark; the system cannot predict its aspect ratio. Two heights are exposed because the prototype already uses two (78px at line 69, 56px at line 155) and because a wide wordmark needs a lower height than a stacked one. `--logo-height-footer` stays fixed at 56px: a merchant who changes it gains nothing and can misalign the footer row (line 153).

**The three colours.** Exposed because they are the brand, and a rebrand should not require a developer. They are also the **most dangerous** three settings in the theme: `--color-accent-strong` #82672B, `--color-text-inverse-muted` #5F5A50 and every status colour are tuned against these exact hex values, and the contrast matrix is computed from them. §28.3 records the guard rail.

**The three font choices — conditional.** `font_picker` presumes Shopify's font library. Whether that library carries Kaushan Script, and whether the brand self-hosts woff2 under licence instead, is **BUSINESS INFORMATION REQUIRED** (§31.7). If self-hosting is chosen, the three families become `@font-face` declarations driving `--font-display` / `--font-body` / `--font-script` and are **not merchant settings at all** — these three rows disappear and the theme drops to 14 settings. Note also that `font_picker` defaults are Shopify font handles (`playfair_display_n9`, `jost_n4`), not display strings; a display string does not validate.

**Container width.** `page_width` drives `--container-standard` only. `--container-wide` (1680) and `--container-narrow` (760) stay fixed so editorial imagery and reading measure keep their relationship to the standard width. The range ceiling stops at 1560, below `--container-wide` 1680, so the wide container always reads as wider than the standard one; a 1680 ceiling would collapse the three-container system to two.

**Button and input radius.** One control. `control_radius` 0 reproduces the prototype's CTAs exactly (lines 104, 132, which carry no radius); the token file's `--radius-sm` 2px is the system default. The range stops at 4 because a pill button is outside the brand (spec §13).

**Announcement copy is not here.** Announcement messages are **block content** in the announcement section, whose preset ships two blocks: "Good People. Higher Purpose." (line 59) and "Worldwide Shipping" (line 60). Only `--announcement-height` is load-bearing enough to be a theme value, because the header offset and the hero's top padding depend on it. Putting the copy at theme level as well would create two sources of truth for one string — exactly the duplication §28.4 forbids — and would not match how Online Store 2.0 carries an announcement bar.

**Product image ratio.** Catalogue-wide, therefore theme-level. Two different ratios on two collection pages is a bug, not a choice (§28.4's level test), and mixed ratios are what force the `contain` fit rule in §27.6.5.

**Social links.** URLs are content and every merchant has them. They live once at theme level and the footer renders whichever are filled, so a URL is never entered twice.

### 28.3 What stays developer-owned, and why

| Not exposed | Why |
|---|---|
| The spacing scale (`--space-1`…`--space-10`, `--section-pad-block`) | The prototype used 44 distinct px values with no scale. Exposing spacing recreates that by hand |
| The type scale (all `--type-*`) | Size and tracking travel together (`--type-eyebrow-size` with `--type-eyebrow-ls`). A merchant changing one produces an unpaired style, and the 12px persistent-text floor and 16px body floor stop being guarantees |
| Semantic colour tokens (`--color-text-*`, `--color-border-*`, `--color-accent-strong`) | These are **derived** from the three exposed colours and contrast-verified. Exposing the derivations lets a merchant break AA while the brand colours still look correct |
| Status colours | All six are tuned to ≥4.5:1 on their own surface. There is no merchant reason to change them |
| Scrims | The four `--scrim-*` tokens exist so the nav stays legible over photography (Phase 1 A11Y-03/HERO-02 measured three nav links at 2.4–2.9:1 over open sky). A merchant-editable scrim is a merchant-editable accessibility failure |
| Focus (`--focus-width`, `--focus-offset`, `--focus-ring*`) | Gold is 11.01:1 on ink and 1.55:1 on cream, so the ring must stay surface-aware. This is not negotiable |
| Motion, z-index, breakpoints, radius scale beyond `--radius-sm`, grid columns and gaps | No merchant customisation value; high breakage cost |

**The guard rail on the three colours.** Because `--color-accent-strong`, `--color-text-inverse-muted` and the status set are derived from and verified against the shipped hex values, changing `color_ink`, `color_cream` or `color_gold` invalidates the contrast matrix. The theme must carry a settings-schema `paragraph` stating this, and the Phase 3 QA checklist must re-run the matrix whenever one of the three changes. A merchant who sets `color_cream` to white, for example, moves every ratio on the light surface.

### 28.4 The level test, and the hierarchy used deliberately

Shopify offers settings at theme, section and block level. God Squad uses all three, decided by one question:

> **Would two different values on two pages be a bug?** If yes, it is a **theme** setting. If it is a legitimate per-placement choice, it is a **section** setting. If the merchant needs to add, remove or reorder it, it is a **block**.

- **Theme** — brand marks, the three colours, the three families, container width, control radius, announcement height, product ratio, social URLs. Seventeen settings.
- **Section** — the surface a band sits on, which collection it shows, its headline and eyebrow, how many columns. Per-placement by definition.
- **Block** — announcement messages, brand-value tiles, CTA buttons, footer link columns. Repeatable content.

**No setting is duplicated across levels.** One value, one place, one source of truth. A duplicated setting doubles QA and guarantees the two copies will disagree.

**`surface`, not `color_scheme`.** Each band exposes `surface` — a two-option select, dark or light, mapping to the `.surface-dark` / `.surface-light` classes — and nothing else. Shopify's native `color_scheme` setting type is deliberately **not** used: it resolves against a `color_scheme_group` declared in `config/settings_schema.json`, which would reintroduce merchant-editable background, text and accent pickers per scheme — the exact colour surface §28.3 exists to refuse. God Squad ships two fixed surface classes instead. `surface` is therefore the only colour control below theme level.

### 28.5 Editor experience rules

1. Every setting carries an `info` string naming its consequence, not restating its label.
2. Settings are grouped by what the merchant is trying to do ("Header", "Announcement", "Products"), never by token category.
3. No setting is named after a CSS property. `page_width`, not `max_width`.
4. A section with no content configured renders nothing, not a placeholder band.
5. The editor's left rail should read as the seven bands of §26.4 in order. If a merchant cannot find the hero by looking for "Hero", the hierarchy has failed regardless of how few settings it has.

## 29. Section/Block Principles

Every homepage band must become a section with a `{% schema %}`. None exists today: the page is one 190-line HTML file whose bands are inline-styled `<section>` elements, and the `<nav>` is absolutely positioned **inside** the hero `<section>` (line 68 inside line 64), so header and hero cannot be separated as authored (SHOP-04).

### 29.1 Where each section lives, and the level test

The level test is §28.4's: would two different values on two pages be a bug (theme), is it a legitimate per-placement choice (section), or does the merchant need to add, remove and reorder it (block)?

Online Store 2.0 places sections in two different kinds of file, and the header/hero problem above turns on the distinction:

| Section | File | Why |
|---|---|---|
| `hero` | `templates/index.json` | Homepage content; merchant may remove or reorder it |
| `featured-collection` | `templates/index.json` | Same, and repeatable — a second collection band is legitimate |
| `our-story` | `templates/index.json` | Same |
| `brand-values` | `templates/index.json` | Same |
| `announcement` | `sections/header-group.json` | Appears on every page above the header |
| `header` | `sections/header-group.json` | Appears on every page; this is what finally separates it from the hero (SHOP-04) |
| `footer` | `sections/footer-group.json` | Appears on every page |

Consequences that must be honoured:

- **`presets` apply only to the four index-template sections.** A `presets` entry has no effect on a section that only ever appears inside a section group; the announcement, header and footer carry their defaults in the group JSON instead.
- The hero declares whether it carries the header over it (`nav_scrim`, §29.2). It does not contain the header.
- The homepage settings budget (§29.6) is split across three files, not one.

### 29.2 Worked schema — `hero` (14 settings)

| Setting | Type | Default | Notes |
|---|---|---|---|
| `surface` | `select`: dark, light | dark | `.surface-dark` / `.surface-light` |
| `image` | `image_picker` | — | Landscape master; see §31.4 |
| `image_mobile` | `image_picker` | — | No default. Shopify cannot mark a setting required, so the section must fall back to `image` with a `--hero-aspect-mobile` 4/5 crop, and the theme's QA checklist must flag the fallback |
| `image_position` | `select`: centre 30%, centre, top, bottom | centre 30% | Reproduces line 65's `object-position: center 30%` |
| `eyebrow` | `text` | Streetwear with a Purpose | Line 83 |
| `heading` | `text` | Walk By | Line 84, before the accent word |
| `heading_accent` | `text` | Faith. | The single `--accent-current` word (line 84). Empty is valid |
| `verse` | `text` | 2 Corinthians 5:7 | Line 85 |
| `description` | `textarea` | *(empty)* | The hero has no equivalent in the prototype (lines 82–93). Measure is capped per §26.2; if filled, it replaces nothing and simply follows the tagline |
| `tagline` | `textarea` | Different / People / Same Purpose | Line 87; line breaks are authored |
| `script_text` | `textarea` | More / Than / Clothing. | Line 91, `--font-script`, rotated by the section, not by a setting |
| `scrim` | `select`: hero-horizontal, top, bottom, none | hero-horizontal | One of the four `--scrim-*` tokens |
| `nav_scrim` | `checkbox` | true | Applies `--scrim-header`. Required wherever the nav sits over photography (Phase 1 A11Y-03/HERO-02) |
| `height` | `select`: standard, tall | standard | Standard reproduces line 64's 620px floor. No px setting is exposed; recommended token `--band-min-height-hero` (see token gaps) |

**Blocks:** `button`, max 2, default 0 — fields `label` (text), `link` (url), `style` (select: primary, accent, text).

**Explicitly not settings:** letter-spacing, px font sizes, any colour, section padding, the rotation angle of the script block, grid track ratios. `alignment` is refused: §26.3 makes every editorial band left-aligned, with centring permitted only inside a product card (line 108) and a value tile (line 144). CTA and CTA URL are the `button` block rather than settings because the hero ships without one (lines 82–93) and the band may legitimately carry none.

### 29.3 Worked schema — `featured-collection` (12 settings)

| Setting | Type | Default | Notes |
|---|---|---|---|
| `surface` | `select`: dark, light | light | Line 98 is the one cream band |
| `layout` | `select`: with-copy-column, full-width | with-copy-column | With-copy-column is `--split-30-70` (line 98) |
| `collection` | `collection` | — | |
| `products_to_show` | `range` 3–12, step 1 | 3 | Line 106 shows 3 |
| `columns_desktop` | `range` 2–4, step 1 | 3 | Tablet and mobile counts are **derived**, not settings: `columns_desktop − 1` at `--bp-lg` and 1 at `--bp-md`, floored at 1. Two fewer settings, one fewer way to break the grid |
| `eyebrow` | `text` | New Drop / | Line 100 |
| `heading` | `text` | The Faithful | Line 101; line breaks authored |
| `subheading` | `textarea` | Premium Essentials for a Higher Purpose. | Line 103 |
| `button_label` | `text` | View All Products | Line 104 |
| `button_link` | `url` | *(blank)* | Merchant points this at the collection. A `url` setting's default must be a static string, so it cannot default to the collection's own URL |
| `image_fit` | `select`: cover, contain | cover | Line 110 uses `cover`. `contain` on the `--color-surface-tile` ground is the fallback where sources are not uniform (§27.6.5) |
| `show_swatches` | `checkbox` | true | Lines 114–117 |

`image_ratio` is **not** here. It is the theme setting `product_image_ratio` (§28.1), because a catalogue-wide ratio differing between two sections is a bug, not a choice. `show_vendor` is not offered: no God Squad surface uses a vendor line (§27.1).

### 29.4 Worked schema — `our-story` (10 settings)

| Setting | Type | Default | Notes |
|---|---|---|---|
| `surface` | `select`: dark, light | dark | Line 125 |
| `image` | `image_picker` | — | Story master; see §31.4 |
| `image_mobile` | `image_picker` | — | Same fallback rule as §29.2 |
| `image_side` | `select`: right, left | right | Line 126 places it `left:30%; width:70%` |
| `overlay_style` | `select`: hero-horizontal, top, bottom, none | hero-horizontal | One of the four `--scrim-*` tokens. The prototype's line-127 story fade is **not** among them — it is a three-stop 90deg gradient with no token, and a `--scrim-story-horizontal` addition is recommended (see token gaps) |
| `split` | `select`: 40-60, 50-50, 30-70 | 40-60 | `--split-40-60` (line 125) |
| `eyebrow` | `text` | Our Story | Line 129 |
| `heading` | `text` | Real People. / Bigger Purpose. | Line 130 |
| `body` | `richtext` | Line 131's paragraph | The only `<p>` on the page; measure capped per §26.2 |
| `caption` | `textarea` | Faith / Lives / Different / Here. | Line 136 — the **caption rail**, at `--type-caption-size` 12px and `--type-caption-ls` 0.20em, not the tagline pairing |

**Blocks:** `button`, max 1, default 1 — `label` (text, "Our Story"), `link` (url). Line 132 is the page's one gold CTA and is valid only because the band is dark (11.01:1 on ink).

### 29.5 Worked schema — `brand-values` (4 settings)

| Setting | Type | Default | Notes |
|---|---|---|---|
| `surface` | `select`: dark, light | dark | Line 142 |
| `heading` | `text` | *(empty)* | The prototype has none; an empty heading renders nothing |
| `columns_desktop` | `range` 2–4, step 1 | 4 | Line 142 |
| `show_dividers` | `checkbox` | true | The `border-top` / `border-bottom` (line 142) and per-tile `border-right` (line 144), all at `--color-border` |

**Blocks:** `value`, max 6, default 4 (line 143 renders four) — fields `icon` (select, from the Phase 3 icon set), `title` (text), `sub` (text), `link` (url, optional). Icon size is not a setting; it is `--icon-xl` 44px (line 145).

### 29.6 The settings budget

God Squad's ceiling is set from its own composition, not from an industry figure: seven bands, one `surface` select each, and **no spacing, colour, size or tracking setting anywhere**.

| Budget | Ceiling | Rationale |
|---|---|---|
| Theme settings | 17 | §28.1. Drops to 14 if fonts are self-hosted |
| Settings per section | 14 | Hero, the most complex, uses 14; featured collection uses 12 |
| Fields per block | 4 | Enough for icon + title + sub + link; more means the block is really a section |
| Blocks per section | 6 | Beyond six, a merchant is building a page, not configuring a band |
| Colour settings below theme level | 1 | `surface`, and only `surface` |
| Spacing / size / type settings anywhere | 0 | The scales are the system |

Split across the three files:

| File | Sections | Section settings | Block fields | Total |
|---|---|---|---|---|
| `templates/index.json` | hero 14, featured-collection 12, our-story 10, brand-values 4 | 40 | 8 (hero button 3, our-story button 2… normalised to 8 across three block types) | 48 |
| `sections/header-group.json` | announcement 2, header 6 | 8 | 3 (announcement `message`) | 11 |
| `sections/footer-group.json` | footer 6 | 6 | 2 (`link_list` block) | 8 |
| **Homepage total** | **7 bands** | **54** | **13** | **67** |

Plus 17 theme settings: **84 surfaces a merchant can touch in total**, against 164 tokens.

`announcement` exposes `surface` and `layout` (split — line 58's `justify-content:space-between` — or centred). `header` exposes `sticky`, `overlay_on_hero` (default true, reproducing line 68), `menu` (a `link_list`, which is how navigation is carried; there is no nav-link block), `show_search`, `show_account`, `show_cart` (lines 76–78). `footer` exposes `surface`, `tagline` (line 156), `strapline` (line 164), `show_logo`, `show_social` (which renders the theme-level URLs, never its own), and `layout`.

### 29.7 Block inventory, and the warning against over-granular blocks

| Block | Section | Max | Default | Basis |
|---|---|---|---|---|
| `message` | announcement | 3 | 2 | Lines 59–60 |
| `button` | hero | 2 | 0 | Lines 82–93 carry none |
| `button` | our-story | 1 | 1 | Line 132 |
| `value` | brand-values | 6 | 4 | Line 143 |
| `link_list` | footer | 4 | 0 | The prototype footer has no link columns |

**Shopify explicitly recommends against overly granular blocks** because they increase complexity for developers and merchants (spec §31). The failure mode is concrete here:

- The hero's eyebrow, headline, accent word, verse, tagline and script are **settings, not blocks**. They are a fixed composition (§26.1) and are never reordered. Six blocks in their place would let a merchant put the verse above the headline and destroy the composition, and would triple the section's Liquid.
- The story's eyebrow, heading, body and caption rail are settings for the same reason.
- A block exists only where the **count** is genuinely variable: two or three announcement messages, four or six value tiles, zero or one CTA. That is the whole list.
- If a block type has one field, it is a setting. If it has more than four, it is a section.
- A block is never created to let a merchant reorder two items that have a correct order.

## 30. Design Token Reference

The complete inventory of `PHASE-2-DESIGN-TOKENS.css`, version 1.0.0 (token file line 3), grouped exactly as the file groups it. 162 properties are declared in `:root`; `--color-border-current` and `--accent-current` are introduced by the two surface classes, for 164 in total. Notes flag places where the file contradicts itself and needs a decision in a later section — they are not corrections applied here.

### Group 1 — Core palette (10)

| Token | Value | Source |
|---|---|---|
| `--gs-ink` | `#0D0C0A` | Approved. 14 occurrences (token file line 33) |
| `--gs-cream` | `#F3EFE6` | Approved. 9 occurrences |
| `--gs-gold` | `#D8C08A` | Approved. 10 occurrences over 9 lines |
| `--gs-cream-200` | `#E9E4D8` | Story body copy, line 131. 15.41:1 on ink |
| `--gs-cream-300` | `#EBE6DC` | Product tile ground, line 109 |
| `--gs-stone` | `#BDB6A8` | Muted captions, lines 147/156/164. 9.70:1 on ink |
| `--gs-olive` | `#4B5443` | Third product swatch, prototype data lines 175–177 |
| `--gs-gold-strong` | `#82672B` | Derived. Gold for light surfaces, 4.66:1 on cream |
| `--gs-gold-hover` | `#E6D3A6` | Already emitted by the prototype runtime (`.scp1:hover`, from line 132) |
| `--gs-ink-raised` | `#2A2823` | Already emitted by the prototype runtime (`.scp0:hover`, from line 104) |

*Note.* The file's comment at line 45 cites line 179 as the `--gs-olive` source; line 179 is `values: [` and `#4b5443` occurs at lines 175–177. PATCH-level documentation correction (§1 versioning).

### Group 2 — Semantic colour (28)

Full definitions, meanings and ratios are in §4. Inventory only:

| Subgroup | Tokens |
|---|---|
| Surfaces (5) | `--color-bg-primary`, `--color-bg-secondary`, `--color-bg-inverse`, `--color-surface-raised`, `--color-surface-tile` |
| Text on dark (3) | `--color-text-primary`, `--color-text-secondary`, `--color-text-muted` |
| Text on light (2) | `--color-text-inverse`, `--color-text-inverse-muted` |
| Accent (3) | `--color-accent`, `--color-accent-hover`, `--color-accent-strong` |
| Borders (5) | `--color-border`, `--color-border-subtle`, `--color-border-strong`, `--color-border-inverse`, `--color-border-inverse-subtle` |
| Status (6) | `--color-success`, `--color-success-on-dark`, `--color-warning`, `--color-warning-on-dark`, `--color-error`, `--color-error-on-dark` |
| Scrims (4) | `--scrim-hero-horizontal` (line 66, first stacked gradient), `--scrim-top-heavy` (line 66, second gradient, top half re-tuned), `--scrim-bottom` (line 66, second gradient, bottom half re-tuned), `--scrim-header` (derived; A11Y-03 / HERO-02) |

*Note.* The prototype's story fade at line 127 is a separate `90deg` ink → transparent gradient with no token (T5). `--color-text-inverse-muted`, the six status colours and the four border values are raw literals rather than `--gs-*` references; this is the documented exception to R2 (§1).

### Group 3 — Typography families (7)

| Token | Value |
|---|---|
| `--font-display` | `'Playfair Display', Georgia, 'Times New Roman', serif` |
| `--font-body` | `'Jost', Helvetica, Arial, system-ui, sans-serif` |
| `--font-script` | `'Kaushan Script', 'Brush Script MT', cursive` |
| `--weight-regular` | `400` |
| `--weight-medium` | `500` |
| `--weight-semibold` | `600` |
| `--weight-black` | `900` |

*Note.* Playfair Display 700 is requested from Google Fonts by the prototype but never used; the file directs that the request be dropped (PERF-04, token file line 109). The family itself is used at lines 84, 101 and 130.

### Group 4 — Type scale (38)

| Token | Value | Prototype source |
|---|---|---|
| `--type-display-xl-size` | `clamp(3.5rem, 8.5vw, 7rem)` | 56 → 112px, line 84 |
| `--type-display-xl-lh` | `0.88` | Line 84 |
| `--type-display-xl-ls` | `-0.01em` | Line 84 |
| `--type-display-l-size` | `clamp(2.5rem, 4.6vw, 4rem)` | 40 → 64px, line 101 |
| `--type-display-l-lh` | `0.90` | Line 101 |
| `--type-display-l-ls` | `-0.01em` | Line 101 |
| `--type-display-m-size` | `clamp(2rem, 4vw, 2.5rem)` | 32 → 40px, line 130 |
| `--type-display-m-lh` | `1.05` | Line 130 |
| `--type-display-m-ls` | `0em` | Line 130 |
| `--type-h1-size` | `clamp(2rem, 3.4vw, 3rem)` | 32 → 48px, derived |
| `--type-h1-lh` | `1.05` | Derived |
| `--type-h2-size` | `clamp(1.625rem, 2.6vw, 2.25rem)` | 26 → 36px, derived |
| `--type-h2-lh` | `1.15` | Derived |
| `--type-h3-size` | `clamp(1.25rem, 1.8vw, 1.5rem)` | 20 → 24px, derived |
| `--type-h3-lh` | `1.25` | Derived |
| `--type-h4-size` | `1.125rem` | 18px, derived |
| `--type-h4-lh` | `1.35` | Derived |
| `--type-script-size` | `clamp(1.875rem, 3vw, 2.75rem)` | 30 → 44px, line 91 |
| `--type-script-lh` | `1.10` | Line 91 |
| `--type-body-lg-size` | `1.125rem` | 18px, derived |
| `--type-body-lg-lh` | `1.65` | Line 131 |
| `--type-body-size` | `1rem` | 16px — raised from the prototype's 15px, line 131 |
| `--type-body-lh` | `1.65` | Line 131 |
| `--type-body-sm-size` | `0.875rem` | 14px, lines 87/93 |
| `--type-body-sm-lh` | `1.55` | Derived |
| `--type-eyebrow-size` | `0.8125rem` | 13px, lines 83/100/129 |
| `--type-eyebrow-ls` | `0.30em` | Lines 83/129 |
| `--type-eyebrow-weight` | `var(--weight-medium)` | Line 100 |
| `--type-label-size` | `0.75rem` | 12px, lines 70/104/112/132 |
| `--type-label-ls` | `0.22em` | Lines 104/132 |
| `--type-label-weight` | `var(--weight-semibold)` | Lines 112/132 |
| `--type-caption-size` | `0.75rem` | 12px — raised from 11px, lines 58/147/156/164 |
| `--type-caption-ls` | `0.20em` | Line 147 |
| `--type-caption-weight` | `var(--weight-regular)` | Derived |
| `--type-price-size` | `0.9375rem` | 15px — raised from 14px, line 113 |
| `--type-price-weight` | `var(--weight-semibold)` | Line 113 |
| `--type-price-ls` | `0em` | Line 113, untracked |
| `--type-tagline-lh` | `1.70` | Lines 87/93 |

*Note.* The mobile floor — no persistent interface text below 0.75rem (12px), body at 1rem — raises the prototype's 9px cart badge (line 78) and 11px announcement, value sub and footer text (lines 58, 147, 156, 164). Brand confirmation is BUSINESS INFORMATION REQUIRED (token file lines 124–126).

### Group 5 — Spacing (12)

| Token | Value | px |
|---|---|---|
| `--space-1` | `0.25rem` | 4 |
| `--space-2` | `0.5rem` | 8 |
| `--space-3` | `0.75rem` | 12 |
| `--space-4` | `1rem` | 16 |
| `--space-5` | `1.5rem` | 24 |
| `--space-6` | `2rem` | 32 |
| `--space-7` | `2.5rem` | 40 |
| `--space-8` | `3rem` | 48 |
| `--space-9` | `4rem` | 64 |
| `--space-10` | `6rem` | 96 |
| `--section-pad-block` | `clamp(var(--space-7), 6vw, var(--space-10))` | 40 → 96 |
| `--section-pad-block-tight` | `clamp(var(--space-6), 4vw, var(--space-8))` | 32 → 48 |

Normalisation from the prototype's 44 unscaled values (token file lines 187–189): `6→8, 10→8, 14→16, 18→16, 20→24, 22→24, 26→24, 28→32, 30→32, 36→32, 38→40, 44→48, 56→56`; `170/190 → header offset tokens`.

*Note.* The map's `170/190 → header offset tokens` is unfulfilled — no hero or header offset token exists anywhere in the file; group 14 holds only header heights, logo heights, announcement height and nav gap. The prototype's `padding:170px 48px 56px` (line 82) and `190px 48px 56px 0` (line 90) therefore have no token. Recommend a single `--hero-pad-block-start` covering both (T2).

### Group 6 — Containers (7)

| Token | Value | Purpose |
|---|---|---|
| `--container-wide` | `1680px` | Full-width editorial imagery |
| `--container-standard` | `1440px` | Default content width |
| `--container-narrow` | `760px` | Long-form reading |
| `--gutter-mobile` | `var(--space-5)` | 24px — matches the prototype's mobile rules |
| `--gutter-tablet` | `var(--space-6)` | 32px |
| `--gutter-desktop` | `var(--space-8)` | 48px — matches the prototype's desktop padding |
| `--gutter` | `var(--gutter-mobile)` | Resolved value; steps up at 768 and 1024 (token file lines 387–388) |

Spec §11 replaces the prototype's single `max-width:1440px` wrapper (line 55): sections go full-bleed, their content is constrained.

### Group 7 — Grid (8)

| Token | Value | Source |
|---|---|---|
| `--grid-columns` | `12` | Derived |
| `--grid-gap` | `var(--space-5)` | 24px |
| `--grid-gap-large` | `var(--space-6)` | 32px, normalised from the 36px product gap, line 106 |
| `--product-grid-gap` | `var(--space-5)` | 24px |
| `--split-50-50` | `1fr 1fr` | Derived |
| `--split-40-60` | `0.9fr 1.6fr` | Story, line 125 |
| `--split-60-40` | `1.6fr 0.9fr` | Mirror of the above |
| `--split-30-70` | `0.9fr 2.4fr` | New Drop, line 98 |

*Note.* `--product-grid-gap` resolves to 24px while `--grid-gap-large` carries the 36→32 normalisation of the prototype's own product gap (line 106). Only one can be the product grid's gap; §9 Grid System must settle it, and the loser should be retired under a MAJOR bump (T3).

### Group 8 — Breakpoints (5)

| Token | Value |
|---|---|
| `--bp-sm` | `480px` |
| `--bp-md` | `768px` |
| `--bp-lg` | `1024px` |
| `--bp-xl` | `1280px` |
| `--bp-2xl` | `1440px` |

Reference only — custom properties cannot be used inside media queries (token file line 241). The prototype had two `max-width` queries, 900 and 520, and no tier between 901 and 1440 (Phase 1 RESP-08).

### Group 9 — Borders and radius (6)

| Token | Value | Purpose |
|---|---|---|
| `--border-width` | `1px` | Every hairline in the prototype |
| `--border-width-strong` | `2px` | Reserved |
| `--radius-none` | `0` | The default |
| `--radius-sm` | `2px` | Inputs, small controls |
| `--radius-md` | `4px` | Media containers where a soft edge is wanted |
| `--radius-full` | `9999px` | Circles only: swatches, cart count, avatars |

The prototype used exactly one radius, `50%`, twice. The system stays flat: God Squad is editorial, not app-like (token file lines 253–256).

### Group 10 — Shadow (3)

| Token | Value | Permitted on |
|---|---|---|
| `--shadow-none` | `none` | The default at rest |
| `--shadow-subtle` | `0 1px 2px rgba(13, 12, 10, 0.08)` | Last resort |
| `--shadow-elevated` | `0 12px 32px rgba(13, 12, 10, 0.28)` | Drawers, modals, sticky header on scroll |

### Group 11 — Motion (9)

| Token | Value |
|---|---|
| `--duration-fast` | `150ms` |
| `--duration-medium` | `250ms` |
| `--duration-slow` | `400ms` |
| `--ease-standard` | `cubic-bezier(0.2, 0, 0, 1)` |
| `--ease-out` | `cubic-bezier(0, 0, 0.2, 1)` |
| `--transition-fast` | `var(--duration-fast) var(--ease-standard)` |
| `--transition-medium` | `var(--duration-medium) var(--ease-standard)` |
| `--transition-slow` | `var(--duration-slow) var(--ease-standard)` |
| `--hover-image-scale` | `1.03` — never above 1.05 |

The prototype has zero transitions and no reduced-motion support. The file's `@media (prefers-reduced-motion: reduce)` block collapses all three durations to 1ms and `--hover-image-scale` to 1 (token file lines 390–403).

### Group 12 — Focus (5)

| Token | Value | Ratio |
|---|---|---|
| `--focus-width` | `2px` | — |
| `--focus-offset` | `2px` | — |
| `--focus-ring-on-dark` | `var(--gs-gold)` | 11.01:1 on ink |
| `--focus-ring-on-light` | `var(--gs-ink)` | 17.04:1 on cream |
| `--focus-ring` | `var(--focus-ring-on-dark)` | Resolved per surface class |

These two ring tokens are the documented exception to R2: they reference the raw palette because the ring must be a fixed colour, not a semantic one. Applied via `:where(a, button, input, select, textarea, summary, [tabindex]):focus-visible` (token file lines 382–385). An outline is never removed without substituting one of these.

### Group 13 — Touch targets and icons (6)

| Token | Value | Source |
|---|---|---|
| `--target-min` | `44px` | Usability target |
| `--target-min-aa` | `24px` | WCAG 2.2 SC 2.5.8 floor |
| `--icon-sm` | `16px` | Announcement globe, line 60 |
| `--icon-md` | `24px` | Header utilities, lines 76–78 |
| `--icon-lg` | `28px` | Social icons, lines 160–161 |
| `--icon-xl` | `44px` | Value tiles, line 145 |

The prototype measured 22×16 for the hamburger and 24×24 for the utility icons (brief: measured responsive behaviour) — the hamburger fails SC 2.5.8 on one axis today.

### Group 14 — Header and announcement (7)

| Token | Value | Source |
|---|---|---|
| `--header-height-desktop` | `122px` | 78px logo + 2×22px padding, line 68 |
| `--header-height-mobile` | `88px` | Measured at 375/390/430/768/900 |
| `--logo-height-desktop` | `78px` | Line 69 |
| `--logo-height-mobile` | `56px` | Line 33 |
| `--logo-height-footer` | `56px` | Line 155 |
| `--announcement-height` | `40px` | Derived from `12px 48px` padding at 11px, line 58 |
| `--nav-gap` | `var(--space-7)` | 40px; prototype used 44px, line 70 |

*Note.* `--nav-gap` at 40px departs from the group 5 map, which sends `44→48`. Either the map or the token should be reconciled in the next version (T4).

### Group 15 — Product media (3)

| Token | Value | Source |
|---|---|---|
| `--product-aspect` | `1 / 1` | Line 109; spec §24's recommended starting point |
| `--product-aspect-wide` | `4 / 5` | Optional editorial portrait crop |
| `--hero-aspect-mobile` | `4 / 5` | Replaces the prototype's uncapped 62vw band |

### Group 16 — Z-index (8)

| Token | Value |
|---|---|
| `--z-base` | `0` |
| `--z-raised` | `1` |
| `--z-sticky` | `100` |
| `--z-header` | `200` |
| `--z-overlay` | `800` |
| `--z-drawer` | `900` |
| `--z-modal` | `1000` |
| `--z-toast` | `1100` |

The prototype used only 1 (×4) and 2 (×1). The scale reserves room for commerce UI that does not exist yet.

### Surface classes and global behaviour

Beyond `:root`, the file declares `.surface-dark` and `.surface-light` (§4), the `box-sizing` reset, the `:focus-visible` rule, two `min-width` gutter queries, and the reduced-motion block. These two classes introduce `--color-border-current` and `--accent-current`, the only tokens not declared in `:root`.

### The `[THEME SETTING]` subset

Spec §30 requires the theme editor to stay simple and directs that Shopify's theme / section / block hierarchy be used deliberately. The file marks a small subset for exposure (token file lines 405–419); it is split here by the level at which each belongs.

**Theme level — `config/settings_schema.json`:**

| Setting | Tokens | Group |
|---|---|---|
| Colours | `--gs-ink`, `--gs-cream`, `--gs-gold` | Colors |
| Typography | `--font-display`, `--font-body`, `--font-script` | Typography |
| Layout width | `--container-standard` | Layout |
| Button/input style | `--radius-sm` | Buttons |
| Header | Logo image, `--logo-height-desktop`, `--logo-height-mobile` | Header |
| Announcement height | `--announcement-height` | Announcement bar |

**Section or block level — an announcement-bar section inside the header section group:**

| Setting | Why not theme level |
|---|---|
| Announcement copy | Merchant-editable content, not a design token. Spec §23 permits THE FAITHFUL COLLECTION and WORLDWIDE SHIPPING; §20 settles which ships |
| Announcement link | Per-message destination, and BUSINESS INFORMATION REQUIRED |
| Social links | Per spec §30, exposed as settings but owned by the footer section, not by the token layer |

**Not exposed at any level:** the spacing scale, the type scale, z-index, motion, focus, breakpoints, status colours and scrims. Merchants cannot break the system (token file lines 417–418).

**Two guardrails Phase 10 must add before the colour settings are safe.**

- **G1 — the colours cannot be free pickers.** A Shopify `color` setting is an unconstrained picker; `settings_schema.json` has no validation hook and no on-save callback, so there is no mechanism to check a ratio at save time. Expose the three colours instead as a fixed `select` of pre-verified schemes, or as Online Store 2.0 `color_scheme` / `color_scheme_group` settings whose schemes ship pre-measured against the matrix in §3. A merchant then chooses between verified combinations rather than authoring one.
- **G2 — a gold scheme must ship its light-surface partner.** `--color-accent-strong` `#82672B` is a fixed hex, not computed from `--gs-gold`. Changing the gold token alone leaves the light-surface accent behind, silently breaking the pairing the whole system depends on. Any scheme that sets a gold must set its `--color-accent-strong` in the same scheme, with the ratio on that scheme's light surface recorded.

### Open items and token requests

| # | Item | Resolves in |
|---|---|---|
| T1 | Ink on tile cream `#EBE6DC` is unmeasured. No prototype text sits on it — the product name (line 112) and price (line 113) fall on `#F3EFE6` (line 98), 17.04:1 — but overlay text (badge, sold-out) will need the ground, so the pairing must be measured and added to §3 | §13 |
| T2 | No hero or header offset token exists; lines 82 and 90 have none. Recommend `--hero-pad-block-start` | §25, MINOR bump |
| T3 | `--grid-gap-large` (32px) vs `--product-grid-gap` (24px) both claim the product grid | §9, MAJOR bump to retire the loser |
| T4 | `--nav-gap` 40px departs from the spacing map's `44→48` | §19 |
| T5 | The story fade (line 127, `90deg` ink → transparent) has no token. Either declare `--scrim-hero-horizontal` as covering it or add `--scrim-story-horizontal` | §14, MINOR bump |
| T6 | The prototype's only *inline-link* hover is the global colour change to gold (line 16), which is 1.55:1 on a light surface; the two CTAs have their own background hovers (`.scp0`, `.scp1`). A non-chromatic link hover on light needs underline tokens — offset, thickness, colour | §11, MINOR bump |
| T7 | `--gs-olive`'s comment cites line 179; occurrences are lines 175–177 | PATCH |
| T8 | The footer's `rgba(255,255,255,.2)` divider (line 163) has no direct token | §15 |
| T9 | The 12px persistent-text floor and 16px body raise four prototype sizes; brand confirmation outstanding | BUSINESS INFORMATION REQUIRED |

### 30.99 Token requests adopted after the documentation pass

The sections above were written against version 1.0.0 of the token file and
raised a number of token requests and two citation errors. Those were verified
against the source and the token file was corrected before this document was
issued, so the following requests are **already satisfied** in
`PHASE-2-DESIGN-TOKENS.css` and are recorded here only so the register above
reads accurately.

| Adopted | Resolution |
|---|---|
| `--scrim-story-horizontal` | Added, reproducing the story band's 90deg fade from line 127 |
| `--split-rail` | Added as `0.9fr 1.6fr 0.4fr` for the two three-track bands, lines 64 and 125 |
| `--measure-narrow`, `--measure-body` | Added, 40ch and 68ch; the 40ch value carries line 131's 320px caption measure |
| `--icon-stroke-width` | Added at 1.5, so the single-stroke rule is machine-checkable |
| `--swatch-size`, `--swatch-ring` | Added from line 116 |
| `--band-min-height-hero`, `--band-min-height-story` | Added, 620px and 520px, from lines 64 and 125 |
| `--color-overlay`, `--drawer-width` | Added; `--z-overlay` had reserved a layer with no value to fill it |
| `--color-divider` | Added from the footer rule on line 163 |
| `--link-underline-thickness`, `--link-underline-offset` | Added, so underlines do not borrow from the border system |
| `--control-height`, `--control-height-min` | Added, 48px and 44px |
| `--shadow-on-dark` | Added; the ink-based shadows are invisible on the dark surface |
| `--product-col-min` | Added at 17rem for the auto-fill product ladder |
| `--announcement-height-stacked` | Added at 64px for the two-line phone state, line 50 |
| `--hero-pad-block-start` | Satisfied under the clearer names `--header-offset-desktop` and `--header-offset-mobile`, computed from the header height rather than the prototype's hard-coded 170px and 190px |
| `--color-border-interactive`, `--color-border-interactive-inverse` | Added at 3.02:1 and 3.13:1. This closes a real accessibility gap: the four decorative border tokens composite to 1.17-1.35:1, correct for a hairline separator but failing SC 1.4.11 for a control boundary |
| Surface-class additions | `.surface-dark` and `.surface-light` now also map `--color-border-current-subtle`, `--color-border-current-interactive`, `--color-text-current-muted` and `--shadow-current` |
| `--product-grid-gap` conflict | Resolved to 32px, normalised from the 36px product gap on line 106; the contradictory comment on `--grid-gap-large` was corrected |
| `--gs-olive` citation | Corrected: the swatch data is on lines 175-177, not 179 |
| `--logo-height-mobile` citation | Corrected: the rule is on line 32, not 33 |
| Spacing normalisation map | Corrected for the 44px nav gap, the 56px value and the header-offset entries |

**Still open, and deliberately so.** `--focus-ring-companion` (a two-tone ring for
indicators straddling a dark/light boundary) and `--type-label-weight-nav` (the
prototype's 500 nav weight against the label triplet's 600) are recorded as
recommendations in §23 and §6. Both need a design decision rather than a
mechanical fix, so neither was added unilaterally.

The token file now declares 191 unique tokens. It validates: braces balanced,
comments balanced, no undefined `var()` reference, and every contrast figure in
its comments re-verified against computed values.


## 31. Phase 3 Requirements

Phase 3 is **asset preparation**. This section states what it must deliver for the system defined in §1–§30 to be usable, and what remains unanswerable until the business answers it. Nothing here is to be started before explicit authorisation.

### 31.1 SVG icon set

**Today.** Every icon on the page is a raster PNG: `images/icon-search.png` (28,336 B), `icon-account.png` (28,470 B), `icon-cart.png` (29,127 B), `icon-globe.png` (35,625 B), `icon-facebook.png` (36,771 B), `icon-instagram.png` (42,319 B), plus value marks `icon-crown.png` (33,339 B), `icon-diamond.png` (34,556 B) and `icon-community.png` (39,978 B) — and two unreferenced sprite sheets, `icons-sprite.png` (833,929 B) and `social-sprite.png` (927,973 B). The four-tile values strip (line 143) draws on three value marks on disk, so at least one of the four has no source.

**Required marks.** UI: `search`, `account`, `cart`, `menu`, `close`, `chevron` (one mark, rotated in CSS for all four directions), `arrow-right`, `plus`, `minus`. Content: `globe` (line 60). Social: `instagram`, `facebook`, `tiktok`, `youtube`. Value marks: four, replacing the crown / diamond / community set.

**Delivery.** Phase 3 delivers one inline icon snippet taking a name, a size defaulting to `--icon-md` 24px, and a class. Every icon draws on a 24×24 box at stroke-width 1.5 with no baked fill, and is marked decorative unless it carries the only label. Colour resolves from the surrounding text colour, so `.surface-dark` and `.surface-light` need no icon variants. Sizes come only from `--icon-sm` 16, `--icon-md` 24, `--icon-lg` 28, `--icon-xl` 44. Every icon must be legible at 16px and must carry a 44px (`--target-min`) hit area when it is interactive.

**The arrow is not optional.** The two CTAs use a literal `→` glyph inside a `<span>` (lines 104, 132), and Jost carries neither `→` nor `₱` (brief), so both currently fall back to a per-platform face. `arrow-right` must exist as an icon so the CTA stops depending on a font fallback.

**Token gap:** there is no `--icon-stroke-width` in the token file. Recommended addition at 1.5.

### 31.2 Vector wordmark

**Today.** `images/WHITE FONT LOGO.png` (37,836 B) is used at 78px in the nav (line 69) and 56px in the footer (line 155). Three further wordmark exports sit unreferenced: `images/logo.png` (47,147 B), `white-font-300x300-mu98qi59-mytq.png` (23,444 B), and two root exports both at 43,606 B (`white-font-trans-mu98q2ez-zrdd.png`, `white-font-trans-mu98qky0-5tt6.png`). The filename `WHITE FONT LOGO.png` contains two spaces.

**Required.** One SVG wordmark: a single path or a minimal group, no embedded raster, filled from the surrounding text colour so it inverts between surfaces without a second file, cropped to the glyph bounding box with no transparent padding — the prototype compensates for padding with a `padding:0 6px` wrapper (line 69), which stops being necessary. It must be legible at `--logo-height-mobile` 56px and `--logo-height-footer` 56px. A PNG fallback at twice `--logo-height-desktop` (156px tall) is required for email and OG use only.

**BUSINESS INFORMATION REQUIRED:** a vector original. None exists on disk.

### 31.3 Product photography at production resolution

**The defect.** Product sources are 235px wide (brief: measured responsive behaviour). They render at about 292 CSS px at 1440 — computed from line 98's `.9fr / 2.4fr` split with a 40px gap inside 48px padding, then line 106's three-up at 36px gaps — and at 327 / 342 / 382 CSS px on phones, i.e. 654–764 device pixels from a 235px source: a **2.8× to 3.3× upscale**. `product-tee.webp` is 9,012 B, `product-hoodie.webp` 12,328 B, `product-cap.webp` 10,002 B. These are prototype placeholders, not photography.

**Required.**

| Requirement | Value |
|---|---|
| Ratio | One ratio catalogue-wide: `--product-aspect` 1/1, or `--product-aspect-wide` 4/5, chosen once via the theme setting `product_image_ratio` (§28.1) |
| Minimum long edge | 1000px — the top of the card ladder in §31.5 |
| Ground | `--color-surface-tile` #EBE6DC (line 109), or a knocked-out subject placed on it |
| Fit | `cover` (line 110) is safe only when every source shares the ratio. Where it cannot, `contain` on the tile ground is the fallback (§27.6.5) |
| Colour | sRGB, no profile beyond sRGB, no baked drop shadow, no baked border |
| Per product | One primary image minimum; one alternate and one detail recommended. Swatch colours must correspond to real variants, not to the three literals on lines 175–177 |
| Naming | Per §31.6 |

**BUSINESS INFORMATION REQUIRED:** the real catalogue. Three literal products exist (lines 175–177) against a symbol-only `currency` enum prop (line 169).

### 31.4 Hero and story masters

**Today.** `images/hero-group.png` is **1,989,201 B** — a ~1.9 MB PNG for a full-bleed photograph. The story image is `./01-hero-model-mu98p88t-7jig.webp` (39,966 B, line 126).

**Hero, landscape.** The scrim dictates the crop. `--scrim-hero-horizontal` runs 0.92 at 0%, 0.75 at 26%, 0.15 at 48%, 0.10 at 68% and 0.80 at 100% (token file lines 97–99; prototype line 66), so the subject must sit between roughly **48% and 68%** of the frame — the only stretch under 0.15 alpha. The left 0–26% carries the copy column under 0.75–0.92 alpha and will not show a subject. The same line-66 stack also runs a vertical gradient — 0.55 at 0%, clear from 30% to 70%, solid ink at 100% — so the vertical clear window is **30% to 70%**. Brief the photographer to that box.

**Hero, portrait phone crop.** A separate master at `--hero-aspect-mobile` 4/5, not a re-crop of the landscape. Below 900px the prototype's fade is anchored to the section while the image sits below the 88px in-flow nav, so the gradient goes solid 88px above the image bottom — a black band plus a hard seam at every phone and tablet width (brief). A dedicated portrait master with its own scrim is the only asset-side fix.

**Story master.** The story fade (line 127) is solid ink to 30%, 0.55 at 42% and clear from 56%, so the story subject must sit **right of 56%**. The image is placed `left:30%; width:70%` with `object-position: center top` (line 126). Note this is a different gradient from the hero's: there is no token for it, and `--scrim-story-horizontal` is a recommended addition (see token gaps).

**Header legibility.** Any hero carrying the nav over it must apply `--scrim-header` (token file lines 102–104). Phase 1 A11Y-03 / HERO-02 measured three nav links at 2.4–2.9:1 over open sky.

### 31.5 The WebP ladder

| Asset class | Widest CSS slot | Ladder (px wide) | Byte budget, widest step |
|---|---|---|---|
| Hero, landscape | `--container-wide` 1680, full-bleed | 640, 960, 1280, 1680, 2400, 3360 | ≤320 KB |
| Hero, portrait phone | 100vw at `--hero-aspect-mobile` | 390, 585, 780, 1170 | ≤160 KB |
| Story | 70% of `--container-wide` ≈ 1176 | 480, 720, 960, 1176, 1680, 2352 | ≤240 KB |
| Product card | 378 (4-up at `--container-wide`) | 320, 480, 640, 800, 1000 | ≤90 KB |
| Collection banner | `--container-wide` 1680 | 640, 960, 1280, 1680, 2400, 3360 | ≤320 KB |
| Value icon | `--icon-xl` 44 | SVG only | ≤3 KB |
| Wordmark | `--logo-height-desktop` 78 | SVG only | ≤12 KB |

**The rule.** The widest ladder step must be at least twice the widest CSS slot the asset can occupy, so a 2× device pixel ratio is served natively rather than upscaled. Hero 1680 → 3360 ✓. Story 1176 → 2352 ✓. Banner 1680 → 3360 ✓. Product card 378 → 1000 (2.6×) ✓, which also covers a 382 CSS px card at 3× on a 430px phone.

**Card-width arithmetic.** `--product-grid-gap` is 24px. The prototype's 36px product gap (line 106) normalises to `--grid-gap-large` 32px in the token file's comment, while `--product-grid-gap` is `var(--space-5)` 24px; the tighter 24px is the system value and the comment is recorded as needing correction. At `--container-wide` 1680 with `--gutter-desktop` 48 and four columns: (1680 − 96 − 72) ÷ 4 = **378px**.

**Generation.** Derivatives are generated with `image_url` taking a `width` for each step, and `image_tag` taking `widths` and `sizes`, so the CDN serves WebP by content negotiation and JPEG as the floor. No AVIF is assumed. `loading="lazy"` on everything below the fold; the hero is eager with `fetchpriority="high"`. Every `<img>` carries explicit `width` and `height` so no band shifts on load.

### 31.6 Naming and folder conventions

Shopify flattens `assets/`, so the structure below is a **naming** convention, not a directory tree.

| Class | Pattern | Example |
|---|---|---|
| UI icon | `icon-<name>.svg` | `icon-cart.svg` |
| Social icon | `icon-social-<network>.svg` | `icon-social-instagram.svg` |
| Wordmark | `logo-godsquad.svg`, `logo-godsquad@2x.png` | |
| Hero master | `hero-<slug>-<orientation>.webp` | `hero-crew-landscape.webp`, `hero-crew-portrait.webp` |
| Story master | `story-<slug>-<orientation>.webp` | `story-community-landscape.webp` |
| Product | `product-<handle>-<nn>.webp` | `product-signature-oversized-tee-01.webp` |

**Rules.** Lowercase, hyphen-separated, ASCII only, no spaces (`WHITE FONT LOGO.png` has two), no hash suffixes, no `@` except the one explicit 2× wordmark fallback, no dates, no version numbers in filenames. Product images go to the Shopify product record, not `assets/`.

**Archive.** The editor-generated `.thumbnail` (25,542 B), the unreferenced sprite sheets (`icons-sprite.png` 833,929 B, `social-sprite.png` 927,973 B), and the loose hash-suffixed root exports are archive material and must stay out of the theme (SHOP-06). **One exception:** `01-hero-model-mu98p88t-7jig.webp` (39,966 B) is a loose hash-suffixed root export and is the currently referenced Our Story image (line 126), while `images/our-story.webp` (41,004 B) sits unreferenced. It is archive material only once the §31.4 story master replaces it; until then it is the live source.

**Duplicates to resolve before renaming.** `chatgpt-image-sep-20-2026-11_06_34-am-mu98j9xl-evm9.png` and `images/hero-group.png` are both 1,989,201 B. `images/hero-model.webp` and the root `01-hero-model-...webp` are both 39,966 B. The two `white-font-trans-*.png` root exports are both 43,606 B. `uploads/` holds a further five multi-megabyte PNGs including `GODSQUAD WEBSITE MOCKUP.png` (1,872,888 B) and two copies of the same 833,929 B file.

### 31.7 Business inputs still outstanding

None of these may be invented. Each blocks a specific Phase 3 deliverable.

1. **Browser and device support matrix.** Governs `text-wrap: balance` (already used at line 84), `aspect-ratio` (line 109), container queries and `:has()`. Without it, §25's fallbacks cannot be scoped.
2. **Mobile type floor confirmation.** Whether the prototype's 9px cart badge (line 78), 11px captions (lines 58, 147, 156, 164) and 15px body (line 131) are brand-mandated on phones, or may be raised to the token file's 12px persistent-text floor and 16px body.
3. **Typeface finality and hosting.** Whether Playfair Display, Jost and Kaushan Script are final, and whether Shopify's font library or self-hosted woff2 under licence is used. This determines whether §28.1's three `font_picker` rows exist at all, and whether Kaushan Script is available in the curated library.
4. **Glyph coverage.** Jost carries neither `₱` nor `→`, and both currently fall back to a per-platform face. The peso glyph sits in the most legibility-critical string on the page (§27.2).
5. **Real product photography** at the resolution and ratio in §31.3.
6. **A vector logo original** (§31.2).
7. **Catalogue facts.** Real product names, prices, variants, stock policy, store currency and money format. Three literals exist (lines 175–177).
8. **Every destination, policy and social URL** (Phase 1 Appendix A). The four social settings in §28.1 have no values, and every `href` on the page is `#`.
9. **Announcement messaging** beyond "Good People. Higher Purpose." (line 59) and "Worldwide Shipping" (line 60). Spec §23 forbids inventing further promotional copy.
10. **Brand-values content.** The four-tile strip (line 143) needs four confirmed titles, sub-lines and icon meanings; only three icon sources exist on disk.
11. **Product ratio decision.** Square (`--product-aspect` 1/1) or portrait (`--product-aspect-wide` 4/5), catalogue-wide (§28.1, `product_image_ratio`).
12. **A city or scene for the reference board**, if one is wanted. The only geographic fact on record is "Philippine" (line 131).

### 31.8 Phase 3 exit criteria

Phase 3 is complete when, and only when:

1. Every mark in §31.1 exists as an SVG on a 24×24 box at stroke-width 1.5, drawing its colour from the surrounding text, with no raster icon remaining in the theme.
2. One SVG wordmark exists, legible at 56px, with a single 2× PNG fallback.
3. Every catalogue product has photography at ≥1000px on the long edge, at one shared ratio, on the `--color-surface-tile` ground.
4. A hero landscape master, a hero portrait master at `--hero-aspect-mobile`, and a story master exist, each composed to the scrim windows in §31.4.
5. Every raster asset has a full ladder per §31.5, and every widest step is at least twice its widest CSS slot.
6. Every filename matches §31.6, and every archive file is out of the theme — except `01-hero-model-mu98p88t-7jig.webp` while it remains the live story source.
7. `images/hero-group.png` at 1,989,201 B is superseded by a WebP ladder, and every duplicate in §31.6 is resolved to one file.
8. Every item in §31.7 is answered by the business, or is recorded as still outstanding with the deliverable it blocks named.

**Do not start Phase 3.** Stop and wait for explicit authorisation.

## Appendix A. Design QA Checklist

The checklist below is the acceptance gate for every later phase. A section, component or template is not complete until it passes every applicable row. "Evidence" names how the check is made, so the result is verifiable rather than asserted.

### A.1 Colour

| # | Check | Evidence |
|---|---|---|
| 1 | Every colour comes from a semantic token; no raw hex in component code | Search the stylesheet for `#` outside the token file |
| 2 | Muted gold `#D8C08A` never carries text, icons or borders on a light surface | Visual pass plus contrast measurement on every cream band |
| 3 | Light surfaces use `--color-accent-strong` for accent text | Code review |
| 4 | Every text pairing meets 4.5:1, or 3:1 where the text is large | Contrast measurement against the §3 matrix |
| 5 | UI component boundaries and focus rings meet 3:1 | Contrast measurement |
| 6 | The muted stone tone never appears as text on cream (1.76:1) | Code review |
| 7 | Gold occupies a minority of any viewport; it is accent, never the dominant surface | Visual pass at 375, 768 and 1440 |

### A.2 Typography

| # | Check | Evidence |
|---|---|---|
| 8 | Every text element maps to a named scale step; no ad-hoc sizes | Code review |
| 9 | No persistent interface text below 12px; body copy at 16px | Computed-style audit at 375 |
| 10 | Playfair for display only; Jost for interface and body; Kaushan for accents only | Code review against §5 |
| 11 | Kaushan appears in no navigation, button, price, product field or paragraph | Code review |
| 12 | Tracked-uppercase steps carry their paired tracking value | Code review |
| 13 | Display steps use `clamp()` and never overflow their column at 320-1920 | Resize sweep |
| 14 | The peso sign and arrow render in an intended face, not a system fallback | Glyph-width check per platform |

### A.3 Spacing, layout and grid

| # | Check | Evidence |
|---|---|---|
| 15 | All spacing uses the scale; no stray values | Code review |
| 16 | Sections are full-bleed; content is constrained by a container token | Inspect at 1920 and 2560 |
| 17 | No dark gutters beside any band at any width above 1440 | Screenshot at 1920 |
| 18 | The gutter ladder applies at every breakpoint, including the announcement bar | Computed-style audit at 768 |
| 19 | Product grid resolves to a sensible column count with no orphaned single item | Visual pass at 375, 768, 1024, 1440 |
| 20 | Editorial splits use the split tokens rather than bespoke fractions | Code review |

### A.4 Components

| # | Check | Evidence |
|---|---|---|
| 21 | Every interactive element is a real `button` or `a`, never a styled `div` or `span` | Accessibility tree inspection |
| 22 | All five button states are defined and visually distinct | Interaction pass |
| 23 | Every control meets the 44x44 target, and never less than 24x24 | Measured bounding boxes |
| 24 | Product cards carry no more than title, price, swatches and one action | Visual pass |
| 25 | Every swatch has an accessible name; colour is never the only signal | Screen-reader pass |
| 26 | Form fields have persistent visible labels and programmatic association | Accessibility tree inspection |
| 27 | Error states convey meaning by text and icon, not colour alone | Visual and screen-reader pass |

### A.5 Imagery and icons

| # | Check | Evidence |
|---|---|---|
| 28 | Every image declares intrinsic width and height | Code review |
| 29 | The LCP hero loads eagerly with high fetch priority; everything below the fold is lazy | Network waterfall |
| 30 | Responsive sources are served with an explicit width ladder and sizes | Network waterfall |
| 31 | No image is upscaled beyond 1.0x of its natural size at any breakpoint | Rendered-versus-natural audit |
| 32 | Icons are inline SVG inheriting `currentColor` at one stroke weight | Code review |
| 33 | Decorative images are hidden from assistive technology; meaningful ones have accurate alt text | Accessibility tree inspection |

### A.6 Responsive and motion

| # | Check | Evidence |
|---|---|---|
| 34 | Media queries are mobile-first `min-width`; no `!important` in the responsive layer | Code review |
| 35 | Every styling hook is a class, not an attribute left over from a design tool | Code review |
| 36 | No horizontal overflow at 320, 375, 390, 430, 768, 1024, 1280, 1440, 1920 | Resize sweep with the overflow mask removed |
| 37 | Scrims are anchored to the element they darken, not to an ancestor | Visual pass below 900px |
| 38 | Layout survives 200% browser zoom and 400% for reflow at 320 CSS px | Zoom test |
| 39 | Motion animates only opacity and transform, within the duration tokens | Code review |
| 40 | `prefers-reduced-motion` removes non-essential motion | Emulated in devtools |

### A.7 Ecommerce and Theme Editor

| # | Check | Evidence |
|---|---|---|
| 41 | Product identity, price, availability and variant choice are legible without hovering | Visual pass |
| 42 | Add-to-cart state changes are announced to assistive technology | Screen-reader pass |
| 43 | Every merchant-facing setting has a clear label and a sensible default | Theme Editor walkthrough |
| 44 | Sections can be added, removed and reordered without breaking layout | Theme Editor walkthrough |
| 45 | No section exposes more settings than a merchant can reasonably use | Schema review |
| 46 | Blocks are used for repeatable content, never for individual text fragments | Schema review |


## Appendix B. Phase 2 Completion Criteria

The Phase 2 specification defines completion as the twenty-two items below.

- [x] **Brand direction documented** — §2, with message hierarchy and the restraint principle expressed as working rules.
- [x] **Colors standardized** — §3, three approved colours plus six derived values, each justified and contrast-verified.
- [x] **Semantic color tokens defined** — §4, with the surface-context mechanism that enforces correct accent use.
- [x] **Typography standardized** — §5, three families with explicit permitted and forbidden uses.
- [x] **Type scale defined** — §6, every step with size, weight, line-height, tracking, transform and prototype origin.
- [x] **Spacing system defined** — §7, ten tokens on a 4px grid with a normalisation map from the prototype's 44 stray values.
- [x] **Container system defined** — §8, full-bleed sections with constrained content, replacing the boxed 1440px wrapper.
- [x] **Grid system defined** — §9, twelve-column base, product grid ladder and editorial split tokens.
- [x] **Buttons defined** — §10, four variants with all five states.
- [x] **Links defined** — §11, five contexts with four states.
- [x] **Forms defined** — §12, eight control types with six states.
- [x] **Product card system defined** — §13, structure, ratio and explicit exclusions.
- [x] **Image rules defined** — §14, ratios, fit, art direction and loading strategy.
- [x] **Icon system defined** — §18, inline SVG with a single stroke weight and size ladder.
- [x] **Navigation rules defined** — §19, heights, spacing, states and the mandatory header backing rule.
- [x] **Motion system defined** — §21, three durations, transform and opacity only, reduced-motion support.
- [x] **Responsive rules defined** — §25, mobile-first ladder and the defects the system must not reproduce.
- [x] **Accessibility rules defined** — §24, contrast, targets, focus, semantics and labelling.
- [x] **Shopify settings principles defined** — §28, a deliberately small merchant surface.
- [x] **Section/block principles defined** — §29, worked schemas and the anti-granularity rule.
- [x] **Design tokens documented** — §30 and `PHASE-2-DESIGN-TOKENS.css`, 164 tokens, validated.
- [x] **Phase 3 requirements documented** — §31.

**Scope compliance.** No homepage was redesigned, no hero or header rebuilt, no product card implemented, no Liquid or Shopify template created, no cart, search or account built, no app installed, no asset deleted or replaced, no JavaScript rewritten, and nothing deployed. Two files were added to the project root: this document and `PHASE-2-DESIGN-TOKENS.css`. Every pre-existing project file is byte-identical.


## Appendix C. Business information required

These are inputs Phase 2 could not supply and did not invent. Each blocks the work named beside it.

- Browser and device support matrix — it governs whether `text-wrap:balance` (line 84), `aspect-ratio` (line 109), container queries and `:has()` may be relied on, and therefore whether any fallback tokens are needed (brief: still open).
- Confirmation of the 12px floor for persistent interface text and 16px body against brand intent (token file lines 124–126). It raises the prototype's 9px cart badge (line 78) and 11px announcement, value sub and footer text (lines 58, 147, 156, 164).
- Whether Playfair Display, Jost and Kaushan Script are final, and whether the Shopify font library or self-hosted woff2 is used — this decides the PERF-04 directive to drop the unused Playfair 700 request (token file line 109).
- The `₱` and `→` glyph gap: Jost contains neither, so the peso prices (data lines 175–177) and both CTA arrows (lines 104, 132) currently fall back to a per-platform face.
- Approval for the seven derived palette values plus `--color-text-inverse-muted` `#5F5A50` and the six status colours to enter the brand palette as documented derivations (spec §5 permits derived neutrals if documented).
- Which announcement strings ship. Spec §23 permits exactly THE FAITHFUL COLLECTION and WORLDWIDE SHIPPING; the prototype ships `Good People. Higher Purpose.` (line 59) and `Worldwide Shipping` (line 60). The answer determines whether that brand message keeps its announcement-bar level in §2's hierarchy.
- The single punctuated form of `Different People. Same Purpose.` — line 87 reads `Different / People / Same Purpose` unpunctuated, line 156 reads `Different People. / Same Purpose.`
- Whether the three approved colours may be merchant-editable at all in the Shopify theme editor. If they may not, §30's G1/G2 guardrails and the `[THEME SETTING]` colour row are removed rather than constrained.
- Real product photography and a vector logo — these govern `--product-aspect`, `--product-aspect-wide` and the three logo-height tokens.
- Every destination, policy, social and announcement URL and all catalogue facts from Phase 1 Appendix A, including the announcement bar's link target.
- Confirmation of the 12px mobile floor against brand intent. It raises the 9px cart badge (line 78), the 11px captions (lines 58, 147, 156, 164), the 15px body (line 131) and the 14px price (line 113), and it lowers the 14px hero verse and taglines to 13px (lines 85, 87, 93) and the 13px value-tile title to 12px (line 146). The two reductions are downward changes to the proportions of a brand-approved mockup and need explicit sign-off, not just the raises.
- Whether Playfair Display, Jost and Kaushan Script are final, and whether the faces come from Shopify's font library or self-hosted woff2. This fixes the five-face loaded set and retires the unused Playfair Display 700 the prototype requests at line 12 (PERF-04).
- How the peso sign U+20B1 and the arrow U+2192 are to be rendered. Jost's loaded faces contain neither, so every price and both CTA arrows currently fall back to a per-platform face (BRAND-03, DEBT-11). Options are a subset face carrying U+20B1, a different body face, or documented acceptance of the fallback.
- The browser and device support matrix. It governs clamp() across the whole type scale, text-wrap: balance on the hero headline (line 84), aspect-ratio for --product-aspect (tokens line 335), :has() and container queries for the product ladder.
- Catalogue size and typical collection length. Three products today, which orphans the cap onto row 2 at 768. It decides auto-fill versus auto-fit in the product grid and whether a four-column row ever fills.
- Whether the homepage New Drop keeps its narrow copy rail beside the grid when a collection page runs four columns, or whether the collection page drops the rail entirely.
- Maximum copy length for the hero tracked-tagline blocks (lines 87, 93), which --type-tagline-lh 1.70 assumes but does not bound.
- Whether the 1440px hero headline must hold two lines as the mockup sets. --type-display-xl-size reaches its 112px cap at 1318px, so 1440 and 1920 render identically; the line count is a copy-length and container decision, not a type-scale one.
- Badge vocabulary and the stock or catalogue condition that fires each badge (§13.4)
- Philippine address field set and ordering, and whether Shopify's own address localisation is used instead (§12.4)
- Garment-to-frame ratio and the rest of the shoot brief, confirmed with whoever commissions the photography (§14.4)
- Whether every product will have a second 'back' photograph, which gates the hover image swap (§14.3)
- Quantity upper bound, stock behaviour and back-order policy (§12.4)
- Search scope — products only, or products plus pages and journal (§12.4)
- Newsletter consent copy and email provider (§12.4)
- Swatch colourway names; the product data carries hex values only, lines 175–177 (§13.3)
- Quick-action button copy, and whether quick add is wanted at all (§13.7)
- Whether prices display tax-inclusive, and whether compare-at pricing is ever used (§13.8)
- Browser and device support matrix, which governs subgrid in §13.9 and aspect-ratio, picture art direction and :has() in §14
- Confirmation of the token file's 12px interface-text floor against brand intent, which sets button labels (§10.4), card titles (§13.1) and form help text (§12.2)
- A webfont carrying U+20B1 (₱) and U+2192 (→), or the inline-SVG substitution, since Jost contains neither (§10.4, §13.8)
- Error, success and out-of-stock message wording and tone (§12.3, §13.4)
- Which social accounts exist (Instagram, Facebook, TikTok, YouTube) and their URLs — the extent of the icon system's social set and the footer's mark count depend on it (spec §21; Phase 1 C14, audit line 1994)
- Whether 'Worldwide Shipping' is factually accurate, and the shipping policy page behind it, before the announcement bar's right-hand message may become a link (line 60; Phase 1 Appendix A)
- Whether 'The Faithful Collection' (spec §23) is a real collection with a destination URL or headline copy only — 'The Faithful' is currently the New Drop headline (line 101)
- Browser and device support matrix — it governs how ':has()', container queries, 'text-wrap: balance' (line 84) and 'aspect-ratio' (line 109) may be used and what each must degrade to
- Confirmation of the 12px persistent-interface floor and the 16px body size against brand intent, since it raises the prototype's 9px badge (line 78), 11px announcement (line 58), 11px value sub (line 147) and 11px footer lines (lines 156, 164)
- Destinations for HOME, SHOP, COLLECTIONS, OUR STORY and VERSE, and whether cart, search and customer accounts exist at launch — a utility control that leads nowhere is not shipped (spec §22)
- Real product photography and a vector logo: '--hover-image-scale' 1.03 and the product-grid column ladder are only safe against sources at least 2x the largest rendered CSS width, and today's 235px crops already upscale ~1.4x at 375px (RESP-02, audit line 2439)
- The peso '₱' (line 169) and arrow '→' (lines 104, 132) glyph gap — Jost contains neither and both fall back to a per-platform face; this decides whether the arrow becomes the SVG 'arrow' icon and how prices are set
- Whether a second product photograph exists per item, before any second-image-on-hover behaviour can be defined (§22.4)
- Browser and device support matrix (governs text-wrap:balance line 84, aspect-ratio line 109, container queries, :has())
- Confirmation of the mobile type floor: whether the 9px cart badge (line 78), 11px captions (lines 58/147/156/164) and 15px body (line 131) are brand-mandated on phones, or may be raised to the token file's 12px persistent-text floor and 16px body
- Whether Playfair Display, Jost and Kaushan Script are final typefaces
- Font hosting: Shopify's curated library versus self-hosted woff2 under licence, and specifically whether the library carries Kaushan Script — this determines whether the three font_picker theme settings exist at all (§28.1, §28.2)
- Glyph coverage for the peso sign and the right arrow: Jost carries neither, and both currently fall back to a per-platform face (lines 104, 132, 169)
- Real product photography at production resolution and a single catalogue-wide ratio (current sources are 235px wide; product-tee.webp is 9,012 B)
- A vector logo original: none exists on disk, only raster exports (images/WHITE FONT LOGO.png 37,836 B and three unreferenced variants)
- Catalogue facts: real product names, prices, variants, stock policy, store currency and money format (three literals on lines 175-177 against a symbol-only currency enum on line 169)
- Every destination, policy and social URL (Phase 1 Appendix A) — the four social theme settings have no values and every href on the page is '#'
- Announcement messaging beyond 'Good People. Higher Purpose.' (line 59) and 'Worldwide Shipping' (line 60); spec §23 forbids inventing further promotional copy
- Brand-values content: four confirmed titles, sub-lines and icon meanings for the four-tile strip (line 143); only three icon sources exist on disk
- Product image ratio decision, catalogue-wide: square (--product-aspect 1/1) or portrait (--product-aspect-wide 4/5), set once via the product_image_ratio theme setting
- A city or scene for the visual reference board, if one is wanted — the only geographic fact on record is 'Philippine' (line 131)
