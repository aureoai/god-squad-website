# GOD SQUAD — PHASE 9: MOBILE UX + RESPONSIVE POLISH

Phase 9 deliverable. Built against the Phase 9 brief as issued, `PHASE-2-DESIGN-SYSTEM.md`, and the
sections delivered in Phases 4–8.

This phase adds no feature and no content. It is responsive engineering: every band the theme
already ships, measured at twelve viewports in both orientations, and corrected where the
measurement — not an opinion — said it was wrong.

Status: **delivered**. Nine defects found, nine fixed. Zero horizontal overflow and zero
sub-24px touch targets at any tested viewport on any page. The Phase 8 suites re-run green against
the changed CSS: 197 structural checks, 92 browser-driven interaction assertions, 56 contrast
measurements, and no console errors across 27 rendered pages.

No new file was created in the theme. Six existing files changed, all of them CSS except one Liquid
arithmetic block that had to follow a CSS change or it would have lied to the browser.

---

## 1. Mobile strategy

The brief's instruction was *"Do NOT simply scale the desktop layout down. Mobile must be
intentionally designed."* That is the standard everything below was held to, and it is worth being
precise about what it meant in practice, because most of this theme already passed it.

Phases 4–8 were authored mobile-first: every section's base rules are the phone layout and the
desktop composition is added at `min-width` breakpoints. So the work here was not to build a mobile
layout — it was to find the places where the phone had inherited a decision that was only ever
correct on a large screen. There turned out to be three kinds, and naming them is the strategy:

**A value that is right in portrait and impossible in landscape.** The hero's `min-height` floor is
`32rem` — 512px — which is larger than a landscape phone's entire viewport, so the hero could never
be shorter than the screen and its call to action was always below the fold. The cart drawer's
fixed header and footer added up to 375px of chrome in a 375px-tall viewport, leaving the scroller
at exactly zero. Neither is a scaling problem; both are a floor that outgrew its container.

**A value that is right in absolute terms and wrong in proportion.** The product grid's 32px column
gap is correct at 1440px. At 375px it sat between two 147px cards inside a 24px gutter, so the space
*between* two cards was wider than the space *around* the row — the row stopped reading as a row,
and each card paid 8px it could not spare.

**A viewport unit that assumes a browser with no chrome of its own.** `100vh` is the large viewport.
On a phone whose toolbar retracts, a `100vh` element is taller than what the customer can see, and a
fixed element pinned to its bottom edge — the one holding Checkout — hides underneath the browser.

Everything in §14 and §15 is one of those three. The corrections are all tokens and media queries;
no component was rebuilt, no markup was restructured, and no JavaScript was added. The brief's
*"Do not add JavaScript solely to make CSS responsive"* was not a constraint that had to be worked
around — Phase 9 shipped zero lines of JavaScript.

### What was deliberately not changed

Three things the brief raised that measurement said to leave alone. They are decisions, not
oversights, and each is recorded with its reason in §16.

- The cart drawer stays `min(90vw, 420px)` rather than becoming full-screen on a phone.
- No sticky mobile purchase bar was added to the product page.
- The header keeps two navigation trees (desktop list and mobile panel).

---

## 2. Breakpoints

Phase 2 set the tiers and Phase 9 did not move them. The complete set of media queries in the
theme's CSS, by count:

| Query | Uses | What it is |
|---|---|---|
| `(min-width: 768px)` | 5 | `--bp-md`, the tablet tier |
| `(min-width: 1024px)` | 7 | `--bp-lg`, where desktop compositions begin |
| `(min-width: 1280px)` | 1 | `--bp-xl`, gallery refinement |
| `(min-width: 1440px)` | 2 | `--bp-2xl`, the widest grid tier |
| `(max-width: 767px)` | 2 | phone-only, below the tablet tier |
| `(max-height: 540px) and (max-width: 1023px)` | 2 | **new in Phase 9** — landscape |
| `(hover: hover) and (pointer: fine)` | 12 | hover effects, gated away from touch |
| `(prefers-reduced-motion: reduce)` | 6 | motion suppression |

Two things about that table matter.

**The `max-width` queries are deliberately few.** A mobile-first theme expresses itself in
`min-width`; a `max-width` query is an admission that the phone needs something the larger screens
must not inherit. There are two, and both are in this phase's scope: the product grid's tightened
column gap, and the relaxed column floor that lets a phone hold two cards.

**The landscape query is bounded on both axes.** `(max-height: 540px)` alone would fire on a desktop
window someone has made short, and re-proportion a composition that is perfectly fine at 1440×520.
Adding `(max-width: 1023px)` restricts it to phones and small tablets turned sideways, which is the
only place the problem exists. Both new blocks — hero and cart drawer — carry both conditions.

There is no `orientation: landscape` query anywhere, and that is on purpose: orientation says
nothing about how much height there is. A tablet in landscape has 1024px of it and needs no help; a
phone in landscape has 375px and needs a lot. Height is the thing being reacted to, so height is
what the query asks about.

---

## 3. Header behavior

### Below `--bp-lg`

The header is a three-part bar: menu button, centred logo, and the search / account / cart controls.
`min-height` is `--header-height-mobile` (88px) and every control in it is at least 44×44px. On the
home page it overlays the hero, and publishes `--header-overlay-offset` so the hero can pad itself
clear of it.

The navigation lives in `.header__panel`, a fixed panel that slides from the leading edge, holding
the five top-level links and its own close button. It is opened by `[data-menu-toggle]`, traps
focus, closes on Escape and on overlay tap, and returns focus to the toggle.

### What Phase 9 changed

**The closed panel is now `display: none`.** This is the headline accessibility fix of the phase and
it had been carried in the phase documents as a known defect since Phase 4.

`.header__panel` sets `display: flex`. The user agent's `[hidden] { display: none }` is a
presentational hint at the same specificity as an author class selector, so the author rule won and
`hidden` removed the panel from *view* — via `translateX(-100%)` — and from nothing else. Every link
inside it stayed in the accessibility tree and the tab order, on every page, at every width below
the desktop tier.

Measured on the home page at 375×812, with the menu shut:

| | reachable controls, menu closed | menu open |
|---|---|---|
| before | **22** | 22 |
| after | **16** | 22 |

Six controls — five links and the close button — left the tab order, which is exactly the panel's
contents. A keyboard user pressing Tab from the logo previously walked five invisible menu links
before reaching the page. At 1440px the count is 20 either way, because the panel is already
`display: none` at the desktop tier: nothing about desktop changed.

The rule is written as `.header__panel[hidden]` (specificity 0,2,0) so it beats
`.header__panel` (0,1,0) regardless of source order, and it does not cost the slide-in animation —
`assets/header.js` already sets `hidden = false`, forces a reflow, and only then adds the open
class, which is the exact sequence a transition out of `display: none` requires.

**The skip link is 44px tall.** It was 38px. Phase 2 §23.7 specifies `--target-min` and the brief
repeats it; the skip link is the first control a keyboard user reaches. Fixed with
`display: inline-flex; align-items: center; min-height: var(--target-min)`.

**The panel reserves the safe area.** `padding-block-start`, `padding-block-end` and
`padding-inline-start` now take `max()` of the designed padding and the corresponding
`env(safe-area-inset-*)`. See §11 for the important caveat about when those values are non-zero.

### Landscape

The header is unchanged in landscape and keeps its full 88px height and every control. The brief's
*"Do not allow controls to disappear in landscape mode"* is satisfied by not touching it: nothing in
the header is hidden, shrunk or collapsed at any viewport. The space the landscape hero needed was
found inside the hero instead — see §4.

---

## 4. Hero behavior

### Portrait

Unchanged by this phase, and deliberately so. `min-height` is `clamp(32rem, 68svh, 45rem)` for the
medium preset, the heading is `--type-display-xl-size`, and the lockup runs eyebrow → heading →
scripture → rule → description → call to action in DOM order.

Measured, before and after Phase 9, identical at every portrait viewport:

| viewport | hero height | h1 | CTA lower edge |
|---|---|---|---|
| 375×812 | 552px | 56px | 489px |
| 430×932 | 634px | 56px | 530px |
| 768×1024 | 696px | 65.3px | 568px |
| 1440×900 | 678px | 112px | 614px |

### Landscape — the defect and the fix

A phone turned sideways was the worst viewport in the theme.

The cause was the `min-height` clamp **floor**, not the `svh` unit. `32rem` is 512px, which exceeds a
landscape phone's whole viewport, so the hero was structurally incapable of being shorter than the
screen; on top of that the lockup carried its portrait vertical rhythm. The call to action — the one
control the entire band exists to present — was below the fold at every landscape size.

Measured with a call to action present (see the note below), before and after:

| viewport | hero height before | CTA lower edge before | hero height after | CTA lower edge after |
|---|---|---|---|---|
| 812×375 | 542px | 494px — **below fold** | 335px | **319px** |
| 932×430 | 560px | 512px — **below fold** | 343px | **327px** |
| 667×375 | 522px | 474px — **below fold** | 335px | **319px** |
| 568×320 | 522px | 474px — **below fold** | 326px | **310px** |
| 812×342 | — | — | 329px | **313px** |

The last row is the one that decided the size of the fix. The 375px readings are the *layout*
viewport; a landscape iPhone showing its own compact toolbar leaves roughly 342px actually visible.
Because the landscape hero is sized by its **content** rather than by `min-height`, `svh` and `dvh`
units cannot recover that difference — only the content can. A first attempt that only removed the
floor left the button's lower edge at 359px, which clears a 375px fold by 16px and misses a real one
entirely. The rhythm was then tightened one step, and the button now clears a 342px fold by 29px.

The block is additive and bounded to `(max-height: 540px) and (max-width: 1023px)`:

```css
@media (max-height: 540px) and (max-width: 1023px) {
  .hero--h-small, .hero--h-medium, .hero--h-large, .hero--h-full {
    min-height: calc(100svh - var(--header-overlay-offset, 0px));
  }
  .hero__inner { padding-block: var(--header-overlay-offset, 0px) var(--space-4); }
  .hero__heading { font-size: clamp(1.75rem, 9svh, 3rem); }
  /* eyebrow, scripture, rule, description and CTA each drop one spacing step */
}
```

Three notes on the choices. The top padding clears the overlaid header **exactly**, with no
additional band: the header is transparent and its controls sit along the top edge, so the eyebrow
starting at the header's lower boundary is the whole requirement, and the extra `--space-4` that
portrait uses for composition is 16px this layout does not have. The heading is re-clamped against
*height* because the display scale is normally set from viewport **width**, which in landscape is
the dimension that is not scarce — 9svh is 33.8px on a 375px-tall phone and 38.7px on a 430px one,
and the lockup keeps its two lines. And nothing is removed, reordered or hidden: every element of
the approved composition is present in landscape.

**A measurement correction worth recording.** An earlier reading in this phase reported the hero CTA
moving from y=497 to y=359. That reading was not measuring the CTA. `templates/index.json` ships
`button_label` with no `button_link`, because a merchant has to choose the collection — so `has_cta`
is false and the hero renders **no button at all** in the default fixture. Every number in the table
above was re-taken against a fixture with `button_link` set, which is what production will have.
The harness now builds `home-cta.html` for exactly this reason.

---

## 5. Product grid behavior

### Columns

The grid is `repeat(auto-fill, minmax(var(--product-col-min), 1fr))` with the floor relaxed below
`--bp-md`. Phase 2 §13.9 permits two columns on a phone; the 272px catalogue floor would force one,
because a 375px viewport has only 327px of content box.

Measured column counts and card widths:

| viewport | columns | card width | column gap |
|---|---|---|---|
| 320 | 2 | 128px | 16px |
| 375×812 | 2 | 156px | 16px |
| 390×844 | 2 | 163px | 16px |
| 430×932 | 2 | 183px | 16px |
| 480×1040 | 2 | 208px | 16px |
| 768×1024 | 2 | 336px | 32px |
| 834×1194 | 2 | 369px | 32px |
| 1024×1366 | 2 | 301px | 32px |
| 1280×800 | 2 | 396px | 32px |
| 1440×900 | 3 | 297px | 32px |
| 1920×1080 | 3 | 297px | 32px |

### The gap

The column gap below `--bp-md` is now `--space-4` (16px) and the row gap stays `--space-6` (32px).

The reason is proportional, not aesthetic. At 375px the old 32px gap sat between two 147px cards
inside a 24px gutter: the space between the cards was wider than the space around the row, which
reads as two separate bands rather than one row, and it cost each card 8px. Phase 2 §27.6 rule 4
already records 24px as the intended grid gap and the token's 32px as a comment needing correction;
this is the mobile half of that correction. The row gap is deliberately left alone — vertical space
is not the scarce dimension on a phone, and two rows of cards need the separation.

Card widths gained accordingly: 148→156 at 375, 155→163 at 390, 175→183 at 430, 200→208 at 480. A
320px viewport now holds two columns at 128px where it previously could not.

### The `sizes` attribute had to follow

A narrower gap makes cards **wider**, and a `sizes` attribute computed against the old gap would
under-declare the slot and let the browser pick an image too small for it. `sections/featured-collection.liquid`
now carries `gap_m = 16` and uses it in the three mobile clauses (`need_m`, `threshold_m`, `gaps_m`,
`gaps_m_low`), and `capped_track` rounds **up** rather than down. Verified exact at all eleven
tested widths, with zero under-declarations.

### Card internals

The title is clamped to exactly two lines and holds two lines at every width down to a 128px card —
verified, because a title that collapses to one line on the narrowest card would break row
alignment. Price, compare-at price and colour swatches all sit above the 24px floor.

---

## 6. Story behavior

The Our Story band changes composition twice.

**Below 1024px** the inner is not a grid at all: the photograph is a full-bleed block and the copy
flows beneath it, in DOM order. The media crop is 4:5 portrait on a phone and 3:2 from the tablet
tier up.

**At 1024px and above** the inner becomes a three-track grid —
`minmax(26rem, 0.9fr) minmax(0, 1.6fr) minmax(9rem, 0.4fr)` — with the copy in track 1, the
photograph showing through the empty middle track, and the caption in track 3.

Measured:

| viewport | media box | body width | body type | value columns |
|---|---|---|---|---|
| 375×812 | 360×450 (4:5) | 312px | 16px | 1 |
| 430×932 | 415×519 (4:5) | 367px | 16px | 1 |
| 480×1040 | 465×581 (4:5) | 417px | 16px | 1 |
| 768×1024 | 753×502 (3:2) | 605px | 16px | 2 |
| 834×1194 | 819×546 (3:2) | 605px | 16px | 2 |
| 1024×1366 | 706×520 | 356px | 16px | 3 |
| 1440×900 | 998×649 | 356px | 16px | 3 |
| 812×375 (landscape) | 797×531 (3:2) | 605px | 16px | 2 |

The body measure is capped at `--measure-narrow` (605px) from the tablet tier up, so the paragraph
never runs the full width of a tablet. Body type is 16px at every viewport — it is never reduced on
mobile.

The value list steps 1 → 2 → 3 columns across the tiers, which is the one place a phone reads a
genuinely different layout from a desktop rather than a narrower one.

**Phase 9 changed nothing in this section.** It is included because the brief requires it documented
and because it had to be verified: no overflow, no sub-24px target, no fixed width, correct image
`sizes` (`(min-width: 1024px) 70vw, 100vw`, which over-declares slightly at every width and
therefore never under-serves), and a landscape composition that is the tablet one rather than a
broken desktop one.

---

## 7. Product page behavior

### Composition

Below 1024px the page is a single column in DOM order: gallery, title, price, variant picker,
quantity, add to cart, buy now, description. At 1024px and above it becomes `--split-60-40`, media
left and buying right.

Measured:

| viewport | columns | h1 | h1 lines | reachable controls | overflow |
|---|---|---|---|---|---|
| 375×812 | single | 32px | 2 | 15 | none |
| 430×932 | single | 32px | 2 | 15 | none |
| 768×1024 | single | 32px | 1 | 15 | none |
| 1024×1366 | 544px / 352px | 40px | 2 | 15 | none |
| 1440×900 | 840px / 472px | 40px | 2 | 15 | none |
| 812×375 (landscape) | single | 32.5px | 1 | 15 | none |

The control count is identical at every viewport, which is the property that matters: the phone
offers exactly the same purchasing controls as the desktop, in the same order, with nothing hidden
behind a disclosure.

### What Phase 9 changed

One value. `section-main-product.css` used `max-height: calc(100vh - …)` to bound the gallery on
small screens; it is now `100dvh`. On a phone with a retracting toolbar, `100vh` is the large
viewport, so the bound was computed against a height the customer could not see.

The gallery's `sizes` attribute, its four-region formula and the variant picker were all delivered
in Phase 8 and are unchanged. No sticky purchase bar was added — see §16.

---

## 8. Cart behavior

### The drawer in portrait

`--drawer-width` is `min(90vw, 420px)`, so on a 375px phone it is 338px — 90% of the viewport, with
the remaining 37px of scrim left tappable to dismiss. The scroller gets 437px of the 812px viewport
at 375×812 and scrolls a 1127px list. Header, footer and both actions are present at every viewport.

### The drawer in landscape — the defect and the fix

At 812×375 the drawer's fixed chrome measured 375px — an 85px header plus a 290px footer — inside a
375px-tall viewport. The scroller was therefore **0px** against a 1091px list. A customer who turned
their phone sideways could not see or change a single line of their cart; only Checkout was
reachable, which is the worst possible subset to leave working. At 932×430 the scroller was 55px, a
sliver.

| viewport | header | footer | scroller (before) | scroller (after) |
|---|---|---|---|---|
| 812×375 | 85 → 69px | 290 → 206px | **0px** | **100px** |
| 932×430 | 85 → 69px | 290 → 206px | 55px | **155px** |

Nothing was removed. The chrome was re-proportioned: the header loses its generous padding, the
totals tighten, the line padding compresses, and the two actions sit side by side instead of
stacked — which is the one layout change landscape actually invites, because width is the dimension
it has to spare. Both actions remain, both clear the target minimum inside a 420px-wide panel, and
Checkout is in view. Every control inside a cart line keeps its 44px target; that is not what was
compressed.

### Viewport units and safe areas

`.cart-drawer` was `position: fixed; inset: 0`, which lays it out against the **large** viewport, so
its footer — the one holding Checkout — could sit behind a phone browser's own chrome. It is now
`inset-inline: 0; inset-block-start: 0; height: 100vh; height: 100dvh`, with the `vh` line as the
fallback for a browser that does not know `dvh` (which is the behaviour this replaces, not a
regression).

The footer reserves `max(var(--space-5), env(safe-area-inset-bottom))`, the header the top inset,
and the panel publishes `--drawer-pad-inline-end` so the header, footer and scroller all clear a
landscape notch on the trailing edge — the edge the close button and both action buttons live
against. See §11 for when these are non-zero.

### The cart page

`section-main-cart.css` used `min-height: 60vh`; it is now `60svh`. Otherwise unchanged from
Phase 8, and verified clean at all twelve viewports.

---

## 9. Touch target strategy

The brief asked for *"at least approximately 44 × 44 px and preferably around 48 × 48 px where space
permits"*. Phase 2 tokenised two floors: `--target-min` at 44px (WCAG 2.5.5 AAA, and the platform
guidance from both Apple and Google) and `--target-min-aa` at 24px (WCAG 2.5.8 AA, the conformance
level this theme is held to).

Every interactive element on every page was enumerated at all twelve viewports and measured.

**Result: zero elements below 24px anywhere.** The complete list of elements between 24px and 44px:

| element | size | pages |
|---|---|---|
| `.cart-line__title` | 230×24 to 202×28 | cart drawer, cart page |

That is the only one, and it is a deliberate decision rather than an outstanding defect. It is a
text link inside a list, not one of the primary controls the brief enumerates; it meets the 24px AA
minimum on its own; and the 76px product thumbnail immediately beside it links to the same product,
which satisfies SC 2.5.8's explicit "equivalent control on the same page" exception. Growing it to
44px would add 20px per line to a drawer where §8 has just finished fighting for 100px of scroller
in landscape. It stays at 24px, recorded here so the next phase inherits the reasoning rather than
re-deriving it.

Two targets were corrected this phase: the skip link (38 → 44px) and — indirectly — the five mobile
menu links, which were previously *focusable while invisible*, the most severe possible form of
target failure.

---

## 10. Image optimization

Every image-emitting call in the theme was audited. All of them go through `image_url | image_tag`,
none through a hand-written `<img>`.

| call site | widths | sizes | loading | priority |
|---|---|---|---|---|
| hero (2 sources) | 11–12 steps to 3000 | `100vw` | `eager` | `fetchpriority: high` |
| product card | 10 steps to 1200 | computed per tier | computed | — |
| gallery, first medium | 9 steps to 1800 | four-region formula | `eager` | `fetchpriority: high` |
| gallery, other media | 9 steps to 1800 | four-region formula | `lazy` | — |
| gallery thumbnails | 4 steps to 240 | `80px` | `lazy` | — |
| our story | 8 steps to 2400 | `(min-width: 1024px) 70vw, 100vw` | `lazy` | — |
| cart line | 7 steps to 300 | computed | computed | — |
| header logo | 6 steps to 600 | `(min-width: 1024px) 240px, 160px` | eager (default) | `preload: true` |

Measured at 375px, per page:

| page | images | lazy | not lazy |
|---|---|---|---|
| home | 10 | 8 | logo, hero (`high`) |
| product | 9 | 7 | logo, gallery first medium (`high`) |
| cart | 5 | 3 | logo, first line thumbnail |

**The LCP image is never lazy-loaded.** On the home page the hero carries `loading="eager"` and
`fetchpriority="high"`; on the product page the gallery's first medium does. Exactly two images per
page are not lazy, and both are above the fold on every viewport.

**Every image has `srcset` and intrinsic dimensions.** Zero images without `srcset`, zero without
`width`/`height`, on all three pages.

**Every image box is fully constrained.** This is the layout-shift precondition and it is the one
Phase 8 got caught by: `image_tag` emits `width` and `height` attributes, which are presentational
hints that defeat a CSS `aspect-ratio` when only `width` is set — a cart thumbnail rendered 76×900
before it was found. All seven image classes were re-checked this phase and each constrains both
axes: six sit inside an aspect-ratio'd wrapper with `width: 100%; height: 100%; object-fit: cover`,
and the cart line uses `width: 100%; height: auto; aspect-ratio: var(--product-aspect)`. The logo
uses `height: <token>; width: auto`, where the intrinsic attributes supply the ratio and the
reserved box is correct before the file arrives.

---

## 11. Accessibility

### Fixed this phase

**Five menu links and a close button left the tab order when the menu is shut.** Documented in full
in §3. This was a WCAG 2.4.3 (Focus Order) and 2.4.7 (Focus Visible) failure affecting every page at
every mobile width, and it is the most consequential defect Phase 9 found.

**The skip link meets 44px.** SC 2.5.5 / Phase 2 §23.7.

### Verified and unchanged

- **Zero targets below 24px** at twelve viewports across five pages (SC 2.5.8). The single element
  between 24 and 44px is justified in §9.
- **DOM order equals visual order** at every breakpoint. No section uses `order`, `row-reverse` or
  grid placement to move content away from the order a screen reader reads it. The product page's
  single-column stack is the DOM order; the Our Story band's mobile stack is the DOM order.
- **Body copy is 16px at every viewport**, never reduced for mobile. Headings scale with `clamp()`
  and never fall below 32px for an `h1`.
- **Focus management** in both overlays was delivered in Phases 4 and 8 and re-verified here: focus
  trap, Escape to close, overlay tap to close, focus returned to the invoking control.
- **No content is hidden on mobile.** Control counts are identical across viewports on the product
  page (15) and the cart (27 with the drawer open).
- **Contrast** re-measured after every CSS change: 56 measurements, all passing.
- **`prefers-reduced-motion`** is honoured in six places, including both new landscape blocks, which
  contain no animation.

### Safe-area insets — an honest caveat

The theme's viewport meta is `width=device-width, initial-scale=1`. `viewport-fit` is not set, so it
defaults to `auto`, and under `auto` **the browser insets the layout viewport away from the notch
and home indicator itself, and every `env(safe-area-inset-*)` reports 0**. This was confirmed
empirically: the drawer's computed `--drawer-pad-inline-end` resolves to `max(1.5rem, 0px)`.

So the safe-area padding added this phase is currently **inert**. It is correct, it costs nothing,
and safe-area compliance is meanwhile guaranteed by construction because the browser is doing the
insetting. It is kept rather than removed so that a future phase that wants the full-bleed hero to
reach a notched phone's physical edges has only one piece of work left.

`viewport-fit=cover` was deliberately **not** enabled in this phase, and §16 records what it would
require first. The short reason: headless Edge reports every inset as 0 regardless, so shipping
`cover` would mean shipping unmeasured layout changes on exactly the devices it affects — which is
the one thing this project has consistently refused to do.

---

## 12. Performance testing

Measured at 375px through an iframe of that exact size.

| page | DOM nodes | max depth | stylesheets | scripts |
|---|---|---|---|---|
| home | 253 | 13 | 12 | 2 |
| product | 205 | 13 | 7 | 3 |
| cart | 222 | 16 | 6 | 2 |

Lighthouse flags a DOM at 1,400 nodes and a depth of 32. The heaviest page here is 18% of the node
budget and 50% of the depth budget.

**Delivered weight**, all CSS and JavaScript in the theme:

| | size |
|---|---|
| raw source | 200.5 KB |
| with comments stripped | 100.6 KB — 50% of the source is documentation |
| gzip −9 | **65.5 KB** |

The comment density is deliberate and it compresses away: what the wire carries is 65.5 KB for
twelve stylesheets and three scripts.

**No external font requests.** Verified by grep across every CSS and layout file: no
`fonts.googleapis`, no `fonts.gstatic`, no `@import`, no Typekit.

**No JavaScript was added for responsiveness.** Phase 9 shipped zero lines of JavaScript. Every
correction in this phase is a CSS media query or token, plus one Liquid arithmetic change.

**The per-section stylesheet architecture was kept.** Twelve stylesheets on the home page is more
requests than a single bundle, but it is what Phase 2 chose so that each section ships only its own
CSS, and it is what the brief's *"Do not create one enormous mobile.css"* asks for. Phase 9 added no
new stylesheet: every change went into the file that already owned the component.

**No console errors** across 27 rendered pages, and no Liquid errors — the mini-Liquid harness is
strict and fails on an undefined filter or a missing translation. Zero missing translations.

### What was not measured

Core Web Vitals were **not** measured numerically. No Lighthouse run, no field data, no LCP or CLS
number is claimed anywhere in this document. What was verified is the set of *structural
preconditions*: the LCP candidate is eager with high fetch priority on both landing templates, every
image reserves its box before it loads, no layout uses a fixed pixel width at or above 100px, and no
element overflows horizontally. Actual vitals need a real device on a real network and belong to a
later phase.

---

## 13. Devices and viewports tested

The brief's matrix, in full, on every page:

375×812 · 390×844 · 430×932 · 480×1040 · 768×1024 · 834×1194 · 1024×1366 · 1280×800 · 1440×900 ·
1920×1080

Plus, added because the brief requires landscape and because the edges are where things break:

| viewport | why |
|---|---|
| 812×375 | iPhone 14/15 landscape |
| 932×430 | iPhone Pro Max landscape |
| 667×375 | iPhone SE 2/3 landscape |
| 568×320 | iPhone SE 1 landscape — the smallest realistic screen |
| 812×342 | landscape with the browser's own compact toolbar showing |
| 320 wide | the narrowest viewport the grid is asked to hold two columns at |

Pages measured at each: home (menu closed), home (menu open), home (drawer open), product, cart
page. Plus 27 harness pages checked for console and Liquid errors.

**Method.** Headless Edge's `--screenshot` never matches `--window-size` — below about 492px it
clamps the layout and crops the image, above it the layout comes out ~24px narrower than the window
and is scaled up. Every reading and every screenshot in this document was therefore taken through an
iframe of the exact target CSS size and cropped, which Phase 5 established and every phase since has
re-confirmed. Transitions are disabled before measuring, because headless virtual time does not
advance transform transitions and an un-disabled panel reports `translateX(-100%)` forever.

**Not tested: real devices.** Everything here is one browser engine driven headlessly. Real iOS
Safari and real Android Chrome — with their actual toolbar behaviour, their actual safe-area values,
and a real touch digitiser — are a gap this phase cannot close and §16 records as such.

---

## 14. Issues found

Nine, in the order they were found.

1. **The closed mobile menu kept six controls in the tab order** on every page at every mobile
   width. Cause: an author class's `display: flex` beats the user agent's `[hidden] { display: none }`
   at equal specificity. Measured 22 reachable controls with the menu shut, against 22 with it open.
   Carried as a known defect since Phase 4.

2. **The skip link was 38px tall** against Phase 2 §23.7's `--target-min` (44px).

3. **The cart drawer was unusable in landscape.** 375px of fixed chrome in a 375px viewport left the
   scroller at 0px against a 1091px list. Only Checkout was reachable.

4. **The hero's call to action was below the fold in landscape** at every landscape size — 494px in
   a 375px viewport. Cause: the `min-height` clamp floor of `32rem` (512px) exceeds a landscape
   phone's entire viewport.

5. **The mobile product grid inverted the spacing hierarchy.** A 32px gap between two 147px cards
   inside a 24px gutter.

6. **Three `vh` values assumed a browser with no chrome**: the drawer's `inset: 0`, the cart page's
   `min-height: 60vh`, and the product gallery's `max-height: calc(100vh - …)`.

7. **Neither fixed overlay reserved the safe area.**

8. **`capped_track` rounded down** in `featured-collection.liquid`, so the `sizes` attribute could
   declare a slot narrower than the card actually is.

9. **The new landscape block silently dropped the safe-area padding** — found in self-review after
   the fix for issue 3 was applied. A `padding-block` shorthand inside the landscape media query
   overrode the earlier `@supports` rule at equal specificity, and `safe-area-inset-bottom` is
   non-zero in landscape because the home indicator is still along the bottom edge. The control
   underneath it is Checkout.

---

## 15. Issues fixed

All nine. Each was measured before and after.

| # | Fix | File | Before → after |
|---|---|---|---|
| 1 | `.header__panel[hidden] { display: none }` | `header.css` | 22 → **16** reachable controls, menu shut |
| 2 | `inline-flex` + `min-height: var(--target-min)` | `header.css` | 38 → **44px** |
| 3 | Landscape block re-proportioning the drawer chrome; actions side by side | `section-cart-drawer.css` | scroller 0 → **100px** at 812×375, 55 → **155px** at 932×430 |
| 4 | Landscape block removing the floor and tightening the lockup one step | `section-hero.css` | CTA lower edge 494 → **319px** at 812×375; clears a 342px fold by 29px |
| 5 | 16px column gap below `--bp-md`, 32px row gap kept | `component-product-card.css` | cards 148 → **156px** at 375; 320px now holds 2 columns |
| 5b | `gap_m = 16` through the mobile `sizes` clauses | `featured-collection.liquid` | `sizes` exact at all 11 widths, 0 under-declarations |
| 6 | `100vh`→`100dvh`, `60vh`→`60svh`, `inset:0`→`height:100dvh` | 3 files | drawer sized by the visible viewport |
| 7 | `max()` with `env(safe-area-inset-*)` on both overlays | `header.css`, `section-cart-drawer.css` | inert under `viewport-fit=auto` — see §11 |
| 8 | `capped_track … \| plus: 1` | `featured-collection.liquid` | rounds up |
| 9 | Nested `@supports` inside the landscape media query | `section-cart-drawer.css` | Checkout keeps its inset clearance in landscape |

### Files changed

Six. No file was created.

| file | change |
|---|---|
| `assets/header.css` | issues 1, 2, 7 |
| `assets/section-hero.css` | issue 4 |
| `assets/section-cart-drawer.css` | issues 3, 6, 7, 9 |
| `assets/component-product-card.css` | issue 5 |
| `assets/section-main-cart.css` | issue 6 — one value |
| `assets/section-main-product.css` | issue 6 — one value |
| `sections/featured-collection.liquid` | issues 5b, 8 |

### Regression evidence

Re-run against the changed CSS, all green:

| suite | result |
|---|---|
| Phase 8 structural validator | 197 checks, 197 passed |
| Cart drawer interaction | 49 assertions, 0 failed |
| Cart page interaction | 17 assertions, 0 failed |
| Product page interaction | 26 assertions, 0 failed |
| Contrast | 56 measurements, 56 passed |
| Console / Liquid errors | 0 across 27 pages |
| Responsive sweep | 0 overflow, 0 sub-24px targets, 12 viewports × 5 pages |

Portrait and desktop hero geometry is byte-identical before and after (552 / 634 / 696 / 678px hero
heights; CTA lower edges 489 / 530 / 568 / 614px), which is the check that the landscape work did
not leak.

One harness change was needed and is recorded rather than hidden: the Phase 8 validator's
"no undefined custom property" check kept a hand-written allow-list of component-local properties,
and flagged the new `--drawer-pad-inline-end` even though it is defined in the same file. The check
now honours same-file definitions, which removes a whole class of false failure rather than growing
a list.

---

## 16. Known limitations

**Real devices were not tested.** Every measurement is headless Edge driven through an exact-size
iframe. Real iOS Safari and Android Chrome — actual toolbar behaviour, actual safe-area values, a
real touch digitiser, real network timing — remain unverified. This is the largest gap in the phase.

**`viewport-fit=cover` was not enabled, so the safe-area padding is inert.** Explained in §11.
Enabling it is not a one-line change and should not be done as one. It requires, in order: adding
`viewport-fit=cover` to the viewport meta; insetting `.header__inner`'s top padding by
`env(safe-area-inset-top)`; making `--header-overlay-offset` account for that, since it is currently
the static 88px token and the hero's landscape padding is computed from it; and then re-measuring
the hero at every viewport in this document. On a device with a real inset, the current arrangement
is safe because the browser letterboxes.

**Core Web Vitals were not measured.** Only their structural preconditions. See §12.

**`.cart-line__title` is 24–28px tall**, not 44px. Meets SC 2.5.8 AA and covered by the equivalent-
control exception; reasoning in §9.

**The cart drawer is not full-screen on a phone.** It is `min(90vw, 420px)` — 338px of a 375px
viewport. The brief called it "nearly full viewport width", which this already is, and the remaining
37px of scrim is what makes tap-to-dismiss possible. Recorded as a decision, reversible in one token
if the brand wants it.

**No sticky mobile purchase bar.** The brief lists it as optional and says to remove rather than
force one. The product page's Add to Cart is inside the single-column flow. A sticky bar would need
its own scroll-position logic in JavaScript, which this phase was told not to add, and would cover
content on a 375px-tall landscape viewport where §4 and §8 have just spent their effort reclaiming
vertical space.

**Two navigation trees remain** — a desktop list and a mobile panel, with five duplicated links.
Consolidating them is a header rebuild, and the brief says both to preserve Phase 4 and not to
rebuild completed functionality. Recorded for whichever phase is allowed to touch the header
structurally.

**Below 320px wide and below 320px tall are untested.** 320×568 and 568×320 both pass; nothing
smaller was measured, and no landscape tier exists below 320px of height.

**The landscape blocks fire on a small desktop window.** A browser window at, say, 900×500 satisfies
both `(max-height: 540px)` and `(max-width: 1023px)` and will get the landscape hero and drawer
proportions. This is intended — a 500px-tall window has the same problem a landscape phone does —
but it is a behaviour someone resizing a desktop browser will see, so it is written down.

---

## Appendix — for the next phase

Nothing in Phase 9 blocks Phase 10. Three items are carried forward for whoever picks them up:

1. `viewport-fit=cover` and the header inset work, as sequenced above.
2. Real-device verification on iOS Safari and Android Chrome.
3. A numeric Core Web Vitals run once the theme is on a real Shopify store with real images.

Phase 9 stops here.
