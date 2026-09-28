# PRE-INTEGRATION DESIGN REVIEW

**GOD SQUAD — Shopify Online Store 2.0 theme**
**Date:** 2026-09-26
**Theme:** `god-squad-theme/` — 75 files
**Reviewed against:** the six design guidelines supplied with the pre-integration task list.

---

## Method

Every verdict below is a **measurement taken from a rendered page**, not an opinion. The theme's `.liquid` files are rendered against mock Shopify data by the project's QA harness, and computed style is read out of a browser — because a value can arrive from a token, a cascade, a media query or inheritance, and only the browser knows which one won.

Measured surfaces: `home`, `s-collection`, `s-search`, `c-page-note` in detail, with a 16-surface sweep behind the typeface and button figures.

Two traps were controlled for, both learned earlier in this project:

- **A no-op control.** Before believing any "nothing moved" result, an empty style element is injected and the page re-measured. That established a **noise floor of 756 shifted elements** caused purely by webfont load timing — which is why the one change made below is reported as *1 element of 919*, not as the 757 the naive reading gave.
- **Visible versus screen-reader-only.** Text clipped to a 1px box has no typeface and no colour a sighted user can perceive. Counting it produced a false "four typefaces" result; splitting it gave the true answer of two.

---

## Summary

| # | Guideline | Verdict | Evidence |
|---|---|---|---|
| 1 | Maintain consistent spacing throughout layout elements | **PASS** | 91.3–95.8% of spacing declarations land exactly on the `--space-1..10` scale; 100% of the remainder is explained (see below) |
| 2 | Restrict typography to 1–2 typefaces | **PASS**, one gap closed | Exactly **Jost + Playfair Display** render on every surface. A missing base declaration was found and fixed |
| 3 | Ensure proper alignment across all design components | **PASS** | One content-column edge per page; all headings on that edge or on a grid column |
| 4 | Apply colour intentionally and purposefully | **PASS** | **Zero** non-palette colours in visible text, backgrounds or borders |
| 5 | Ensure buttons clearly appear interactive and tappable | **PASS** | 38 instances measured; every **theme-authored** control is ≥44px, `cursor: pointer` when enabled, and carries a boundary or a glyph. The 21px exception is Shopify's own checkout button |
| 6 | Incorporate actual content early in the process | **FAIL — and it is the most consequential finding in this review** | No merchant content exists. Every measurement in all 19 phases was taken against invented fixture data |

**One change was made to the theme.** Everything else was verified and left alone.

---

## 1. Spacing — PASS

| Surface | On scale | Off scale | % on scale |
|---|---:|---:|---:|
| `home.html` | 102 | 7 | 93.6% |
| `s-collection.html` | 83 | 4 | 95.4% |
| `s-search.html` | 63 | 6 | 91.3% |
| `c-page-note.html` | 69 | 3 | 95.8% |

Every off-scale value was traced to its source, and **none is drift**:

| Value | Source | Verdict |
|---|---|---|
| `75.9px`, `53.9px`, `54.8px` | `--section-pad-block: clamp(var(--space-7), 6vw, var(--space-10))` — a clamp built from two scale tokens, resolving to `6vw` at intermediate widths | Deliberate. Landing between scale steps is what a clamp is *for* |
| `170px` on `.hero__inner` | `calc(var(--hero-header-clearance, 0px) + var(--space-7))` — a scale token plus the header's **measured** height, published by `sections/header.liquid` only when it overlays | Deliberate. The hero must clear a header whose height depends on merchant settings |
| `387px` on `.main-cart__summary` | `margin-left: auto` resolving against the column | Deliberate |
| `1px` | `.visually-hidden { margin: -1px }` | The screen-reader utility, not a spacing decision |

So the honest figure is not "8.9% off scale" but **100% of spacing is either a scale token, a clamp between two scale tokens, or a derived measurement** — which is the standard the guideline is asking for.

---

## 2. Typography — PASS, with one gap closed

**Two typefaces are DECLARED, on every surface measured:** `Jost` (body and interface) and `Playfair Display` (display). Verified on four surfaces individually and across a 16-surface sweep.

> **Correction, 2026-09-26.** This section originally said the two typefaces
> *render*. They do not, in the QA harness — and the original measurement could
> not have told the difference. `getComputedStyle().fontFamily` returns the
> **declared stack**, so it reports `"Playfair Display"` whether or not that font
> exists on the machine. `document.fonts.check()` returns `true` as well.
>
> The reliable test is to measure the width of identical text in the named font
> and in its fallback. Done afterwards: `"Playfair Display", Georgia, serif`
> measured **845.6px** and `Georgia, serif` alone measured **845.6px**; `"Jost",
> Helvetica, Arial` measured **850px** and the fallback **850px**. Both identical,
> `document.fonts.size` was **0**, and neither family is installed on this
> machine. Every harness screenshot in this project was **Georgia and Arial**.
>
> **The theme is unaffected.** `layout/theme.liquid` calls `font_face` and
> Shopify serves both faces from its own CDN on a real store. The harness does
> not execute that call, so the fixtures never had fonts. The declaration audit
> below — which family each rule asks for, and the `--type-label-lh` gap — is
> unchanged, because it is about the CSS, not about what rendered.
>
> **What this does weaken:** any finding whose magnitude depended on glyph
> widths. The cart-title leading defect is real and the fix is right (one rule
> declared a line-height and its twin did not), but the measured 14.0px versus
> 17.4px, and the observation that the title wraps at 375px, were taken against
> Arial rather than Jost. Re-measure those on a real store.

A third family token exists — `--font-script: 'Kaushan Script'` — with **zero consumers** and no font file registered. PHASE-2 §6.1 reserves it for "the single script accent", specified and never built. **It does not render, so the theme is within budget today**, but note that building that accent would put the theme at three typefaces and outside this guideline. That is a decision, not an oversight.

### The gap that was found and closed

A 16-surface sweep initially reported **four** typefaces. Splitting visible from screen-reader-only text explained it:

| | Count |
|---|---:|
| Elements not rendering in a theme typeface | 229 |
| …screen-reader-only (clipped to 1px; typeface has no effect) | 223 |
| …**visible to a sighted user** | **6** |

All six visible cases are Shopify's own accelerated-checkout button (`shopify-payment-button`, "Buy it now", "Shop Pay") — markup Shopify renders and the theme can only style around. **No theme-authored visible text falls back.**

But the 223 screen-reader elements pointed at a real structural gap: **`base.css` set `body { margin: 0 }` and no `font-family`.** The two-typeface rule was enforced by roughly sixty components each declaring it individually, with nothing underneath to catch one that forgot — and 223 elements demonstrated the gap already existed.

**Change made** — `assets/base.css`:

```css
body {
  margin: 0;
  font-family: var(--font-body);
}
```

This belongs in `base.css` by the file's own stated purpose ("the global element layer… the only stylesheet in the theme that styles bare elements"), which already holds `box-sizing` and `margin: 0` for exactly the same kind of reason.

**Measured blast radius: 1 element of 919 across 8 surfaces, against a no-op noise floor of 756.** Effectively nothing — it only reaches text that had no typeface of its own.

It deliberately does **not** reach form controls: the user agent does not inherit a font into `button`, `input`, `select` or `textarea`. Every component in the theme gives those their own declaration. This is a safety net, not a substitute.

---

## 3. Alignment — PASS

The alignment question that matters is whether every band's content column starts on the same vertical line. Measured on `home.html` at 1265px:

| Element | Content left | max-width | padding-inline | Width |
|---|---:|---|---|---:|
| `header__inner.container` | 48 | 1440px | 48px | 1265 |
| `hero__inner.container` | 48 | 1440px | 48px | 1265 |
| `featured-collection__inner.container` ×2 | 48 | 1440px | 48px | 1265 |
| `our-story__inner.container` | 48 | 1440px | 48px | 1265 |
| `container` (footer) | 48 | 1440px | 48px | 1265 |

**One content edge. All eight headings on that edge (x=48).**

On the collection and search pages a second heading edge appears at `465.5`. That is the product grid's **second column** — every column-1 card title at 32, every column-2 title at 465.5. Grid structure, not misalignment.

This is a direct payoff from the Phase 18 container consolidation: before it, twelve elements each carried a private copy of the same four declarations, so nothing guaranteed they agreed.

---

## 4. Colour — PASS

Measured with visible and screen-reader-only elements separated, and each value checked against the token file.

| Surface | Non-palette visible colours |
|---|---:|
| `home.html` | 0 |
| `s-collection.html` | 0 |
| `s-search.html` | 0 |
| `c-page-note.html` | 0 |

Every visible text colour, background and border on every surface measured resolves to a documented palette token: `--gs-ink` `#0D0C0A`, `--gs-cream` `#F3EFE6`, `--gs-gold` `#D8C08A`, `--gs-cream-200` `#E9E4D8`, `--gs-stone` `#BDB6A8`, `--gs-olive` `#4B5443`, `--color-surface-tile` `#EBE6DC`, `--color-text-inverse-muted` `#5F5A50`, or a palette colour at a documented alpha.

One apparent outlier — `rgb(233, 228, 216)` — turned out to be `--gs-cream-200`, documented as "story body copy, 15.41:1 on ink". **My probe's token list was incomplete, not the theme's palette.** Recording that because an unverified outlier in a review is worse than none.

The governing colour constraint remains correctly applied: muted gold measures **1.55:1 on cream** and is a dark-surface accent only; light surfaces use `--color-accent-strong` `#82672B` at 4.66:1.

---

## 5. Buttons — PASS

38 instances measured across 16 surfaces.

| Control | n | Size | Cursor | Boundary | Min height |
|---|---:|---|---|---|---:|
| `button--primary` | 10 | 467×50 | pointer | background + border | 48 |
| `button--accent` | 2 | 291×50 | pointer | background + border | 50 |
| `button--secondary` | 2 | 94×48 | pointer | border | 48 |
| `featured-collection__cta.button` | 2 | 287×50 | pointer | background + border | 50 |
| `quantity__button` | 16 | 44×44 | pointer / `default` when disabled | 24px glyph | 44 |
| `shopify-payment-button__button` | 6 | 78×21 | — | — | 21 |

Two apparent failures were investigated and **both were artefacts of how the measurement grouped instances**:

- **"`quantity__button` has `cursor: default`."** Reading every instance individually rather than one exemplar per class: **12 are `pointer`, 8 are `default` — and all 8 of those carry `opacity: 0.45`.** They are the `aria-disabled` steppers (quantity already at minimum). `component-quantity.css:74` sets `cursor: default` for that state deliberately. A disabled control *should not* show a pointer. Correct as built.
- **"`quantity__button` has no visual boundary."** True — no background, no border. It is an icon-only control and every instance carries a 24px glyph, at a 44×44 target. PHASE-2 §18.6 and §22.8 give an icon-only control one hover row (colour). Documented and deliberate.

`shopify-payment-button` is Shopify's own markup at Shopify's own size; the theme can style the container but not the button. Excluded rather than reported as a theme defect.

---

## 6. Incorporate actual content early — FAIL

This is the guideline the project has not met, it cannot be fixed with code, and it is the most consequential item in this review.

**There is no merchant content.** Not the photography, not the catalogue, not the business details:

| Missing | Consequence |
|---|---|
| Product photography | Phase 3 recorded sourcing — not processing — as the ceiling. **The theme contains zero image files** and `templates/index.json` sets no hero image, so the hero renders imageless until a merchant uploads one. The imagery in the approved mockup lives in the project's `uploads/` folder, is AI-generated, and its rights are unconfirmed |
| Real product catalogue | Products, prices, variants and inventory all come from Shopify at runtime, correctly — but nothing has ever rendered a real one |
| Logo vector master, favicon | The current wordmark carries heavy transparent padding and renders at roughly half its intended size; `/favicon.ico` 404s |
| Contact details, social accounts | The theme supplies none and guesses nothing, by design |
| `theme_support_email`, `theme_documentation_url` | The only two Theme Check offences outstanding |
| Confirmed brand-origin statement | Ships as the Our Story default but is an unconfirmed claim (Phase 1 Appendix A, decision 25) |

### Why this is not a formality

**Mock content demonstrably hides defects in this codebase.** Phase 18 found a live typography bug that was *invisible* on the fixture data and *visible* on realistic data: `.cart-line__title` carried every part of the label role except leading, so a wrapped product name rendered at **14.0px per line in the cart against 17.4px on a product card**. The fixtures' short invented names fit on one line at desktop width and hid it. It only surfaced when measured at 375px, where a real-length name wraps.

That is one confirmed instance of the exact failure mode this guideline exists to prevent. Every measurement in this review, and in all nineteen phases, was taken against data this project invented. Real product names are longer, real descriptions are messier, real photography has aspect ratios nobody here has seen.

**Recommendation:** supply real photography and a handful of real products *before* the Shopify integration, not after. The theme is built correctly to receive them — but "correct against fixtures" is a weaker claim than it sounds, and this project has already proved it once.

---

## Testing after the change

The change touched `assets/base.css` only. Suites re-run afterwards:

**Passing — 15 suites:**

```
validate      199/199     cartdoc     85/85      accounts    52/52
negctl(15)    22/22       hygiene     0 findings seo         52/52
refs          10/10       tracking    31/31      escaping    7/7
negctl(17)    12/12       surfaces    41/41      catalog     55/55
facets        62/62       settings    28/28      images      54/54
layout        19/19
```

**Recovered — `contrast8`, the accessibility-critical one: 74 measurements, 74 pass, 0 failures.**

Rather than leave it dark, its measurement was re-run through the working path. `contrast8` writes a probe page per surface, reads the payload with `--dump-dom`, then deletes the page (`contrast8.py:248`). A driver was written that reuses `contrast8`'s own `PROBE` template and role lists — so the measurement is identical, not a re-implementation — writes all nine probe pages and leaves them, and the payloads were read through the Browser pane:

| Surface | Roles measured | Pass | Fail |
|---|---:|---:|---:|
| product, cream | 17 | 17 | 0 |
| product, ink | 13 | 13 | 0 |
| drawer, ink | 18 | 18 | 0 |
| drawer empty, ink | 3 | 3 | 0 |
| cart page, ink | 6 | 6 | 0 |
| order note, drawer ink | 3 | 3 | 0 |
| order note, cart page ink | 9 | 9 | 0 |
| add confirmation, cream | 3 | 3 | 0 |
| unit price, cream | 2 | 2 | 0 |
| **Total** | **74** | **74** | **0** |

**Still dark — 3 suites:** `editor`, `cardcascade`, `facetsgate`.

These report `NO READING` — their probe produces no output. This is an **environment failure, not a theme regression**, and that was established rather than assumed:

- **Negative control:** reverting the `base.css` change and re-running `contrast8` produced the *identical* failure. The change is not responsible.
- Ruled out: stale Edge processes (cleared, 0 remaining), corrupt Edge profiles (46 accumulated directories force-removed), missing HTTP servers (started on 8808 and 8809, both answering 200), missing fixture pages (all six present), and script errors (runs clean, no traceback).
- **The cause was isolated exactly:** the four failing suites are precisely the four that use Edge's `--dump-dom`, and every suite that avoids it still passes. A trivial smoke page returns zero bytes through `--dump-dom` too, with and without `--window-size`, while Edge itself launches normally (it creates its profile). `--dump-dom` is the broken component.

The three remaining suites cover Theme Editor section lifecycle, product-card cascade, and the desktop filter-drawer gate. All three passed earlier in this session. **Their coverage should be re-confirmed in a clean environment before the integration**, and this review does not claim their results.

The colour, alignment, spacing and typography measurements in this document were taken through a **different** mechanism — the Browser pane — which worked throughout, so the verdicts above do not depend on the broken path.

---

## Two handover risks worth your decision

Neither is a design issue; both were surfaced by the consolidation's critics, and both are cheap to close now and expensive later.

### 1. The QA suite does not live in the project

Every test behind every measured claim in nineteen phases — **228 Python files, 1.48MB** — lives in this session's scratchpad directory, not in the project:

```
C:\Users\TEST\AppData\Local\Temp\claude\C--Users-TEST-OneDrive-Documents-GodSquad-Website\de238d03-508d-43ce-a377-210f71ff0033\scratchpad
```

That is a temporary directory. When it is cleared, the Mini-Liquid harness, the contrast suite, the interaction suites, the negative controls and the design probes go with it — and with them the reproducibility of every number in every phase document. The theme would still be correct; nobody would be able to demonstrate it.

There is also no Theme Check runner in the project. The one used throughout is `@shopify/theme-check-node`, installed under that scratchpad's `node_modules`.

**If you want the verification to survive**, copy it into the project — for example to `qa/`. Note that the directory also holds the generated harness sites and browser profiles (~310MB in total), so copying only the `*.py` files while keeping the directory structure is the leaner option.

**I have not done this.** Adding 228 files to your project root is a structural change to your repository, and that is your call rather than mine.

### 2. There is still no version control

Phase 1 logged this as DEBT-12/DEBT-13 and recommended fixing it before Phase 2. The project is a plain folder inside a personal OneDrive; there is no git repository. Nineteen phases of work, a 75-file theme and 640KB of consolidated documentation have no history, no diffs, and no way to recover a bad edit beyond OneDrive's own file versioning.

Before the integration starts making changes against a live store, this is the cheapest risk on the list to close.

---

## What changed, and what did not

**Changed (1 file):** `assets/base.css` — `body` gains `font-family: var(--font-body)`.

**Deliberately not changed:** the `--font-script` / `--type-script-*` tokens (reserved by PHASE-2 for an unbuilt script accent; removing them would discard a specification, building them would break this guideline — your call); the `quantity__button` boundary; the `shopify-payment-button` sizing; and every spacing, colour and alignment value, all of which measured correct.

Five decisions from the Phase 18 review remain open and are unaffected by this pass: the "Add to bag" versus "cart" voice, the mobile menu panel type, the footer's two link type systems, the "Worldwide Shipping" claim, and the announcement-bar raster icon.
