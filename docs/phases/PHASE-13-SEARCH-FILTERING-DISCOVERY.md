# GOD SQUAD — PHASE 13: SEARCH, FILTERING & PRODUCT DISCOVERY

Phase 13 deliverable. Built against the Phase 13 brief as issued, Shopify's storefront filtering and
predictive search documentation, and the discovery surfaces delivered in Phases 4, 10 and 12.

Status: **delivered**. **570 automated assertions pass**, across fourteen rendered pages at twelve
viewports each, with no console error on any of thirty-six pages.

This is the first phase since Phase 8 to add substantial net-new functionality. Filtering did not
exist — zero occurrences of `collection.filters` anywhere in the theme — because Phase 10 fork F1
deferred it deliberately, with the instruction that the section be built so "adding filters later is
additive, not a rewrite". It was, and it is.

---

## 1. Search architecture

Unchanged and already correct: `sections/main-search.liquid` renders a real `role="search"` GET form
with a labelled `q` input, three states (no query, results, zero results), `{% paginate %}`, product
results through the Phase 12 card, and non-product results in a separate group.

**What Phase 13 added is the header surface.** The control was a plain link to `/search` carrying a
`data-search-trigger` attribute that nothing read. It is now a disclosure panel — and the link is
left **byte-identical**.

That matters more than it sounds. With scripting off, the control still navigates to a complete
search page. A `<button>` would have been a control that does nothing. `assets/header.js` intercepts
the click, and the guard `assets/cart.js` already applies to the cart bubble is applied here too, so
a cmd-click still opens `/search` in a new tab.

### 1.1 Why a panel and not an expanding field

Arithmetic, not taste. At 375px the header row has 327px of content box. The start cluster takes
44px, the end cluster 148px (3 × 44 plus two gaps), and the two grid gaps 32px — leaving the branding
track exactly **103px**. A usable search field needs about 180px. Taking it means the logo goes or
the bar reflows, and that *is* redesigning the header, which the brief forbids.

A panel is a layer: `.header__inner`'s grid never changes, and nothing is added to that 327px row.
The overlay is the option that **preserves** the header.

### 1.2 ARIA applied at upgrade, never printed

`aria-haspopup="dialog"` and `aria-expanded` are set by JavaScript when it initialises, not rendered
by Liquid. They are claims about behaviour that only exists once the script runs; printing them into
a page where the script failed would describe a disclosure that is actually a link.

The panel's bindings are recorded in `header.js`'s existing registry and released by the same
teardown Phase 11 added — one place that knows what the header has bound outside its own subtree.

---

## 2. Predictive search

**Deferred, by the brand owner's decision, and the deferral is the deliverable.**

The brief says "if appropriate" and "if supported by current architecture". Its value is almost
entirely a function of catalogue size: below roughly 25 products a customer reaches everything faster
by scrolling one collection; above roughly 150 it becomes the fastest path in the store. Nobody on
this project has that number yet, and the owner confirmed the catalogue is small at launch.

The cost is real and measured: roughly 7KB gzipped — a ~37% increase on the theme's entire JavaScript
payload — plus a new section, a new snippet, a new stylesheet, an ARIA combobox (the highest-defect
pattern in the WAI-APG set) and a third dismissable surface.

**Building the header panel is what makes it a later drop-in rather than a rewrite.** The surface,
the trigger interception, the focus management and the Escape handling all exist now; predictive
search would add a results region inside a panel that is already there.

**The contract it must be built to, recorded so it is not re-researched:** Shopify's section-rendering
endpoint (`routes.predictive_search_url` with `section_id`), never the JSON endpoint and never a
hardcoded `/search/suggest` — which is locale-prefixed on non-primary locales. Section rendering
keeps every escaping decision in Liquid and reuses the theme's own templates, so it cannot create a
second card implementation or a second unreviewed escaping surface. 300ms debounce, a 2-character
minimum, an `AbortController` per request, a captured-term comparison at resolve because `abort()` is
not synchronous, a monotonic generation counter, and a cache keyed on the normalised term — six
guards, because no single one closes the stale-response window. `resources[limit]=4` with
`limit_scope=each`, because the default `limit_scope=all` means ten results across all types.

**What unblocks it:** a catalogue count. This is a BUSINESS INFORMATION REQUIRED item in the sense
Phase 1 Appendix A uses, and the precedent is Phase 5 shipping the hero with its CTA hidden pending a
collection URL.

---

## 3. Search result architecture

Unchanged. The Phase 12 product card, the shared `grid-sizes` snippet, the real result count from
Shopify, and the query echoed through the locale file rather than printed from a URL parameter.

**Filtering was deliberately not added to `/search`.** shopify.dev states that applying filters on the
search results page strips out all non-product results — and `main-search.liquid` renders a
non-product group, with a setting whose own help text promises the merchant that "pages and articles
come back as a titled list below it." The moment any filter were active, that promise would silently
stop being true: a customer picking a colour would make the size guide vanish with nothing explaining
it.

`snippets/facets.liquid` is written against a generic `results` parameter precisely so adding it later
is one `{% render %}`. What must accompany it, recorded now: three hidden inputs in the facets form —
`q` (or the search is discarded), `type` (or the merchant's configured scope silently reverts to
Shopify's all-types default), and `options[prefix]=last` (or the partial last-word match the section
documents stops applying) — plus `search.sort_options`, because a lone sort control over a
relevance-ranked set is a downgrade.

---

## 4. Filter architecture

Shopify's native filtering. No custom filter database, no second product index, no filtering logic in
JavaScript.

### 4.1 One form, one set of controls

**The single most consequential decision in this phase.** The filter controls are rendered **exactly
once** in the document. At `--bp-md` and above they are a horizontal row of `<details>` dropdowns
above the toolbar; below it, once script has upgraded them, the same element is a drawer. That is a
CSS difference, not a second copy.

Themes that render a desktop sidebar and a mobile drawer separately must keep two sets of checkboxes
in step and submit both. Here there is one checked state, one submitted value per choice, and nothing
to synchronise.

Every control binds to one `<form method="get">` by the HTML `form` attribute rather than by DOM
nesting — which also keeps the product grid outside the form, so a future quick-add `<form>` cannot
nest inside it.

### 4.2 The sort form was going to drop every filter

`main-collection.liquid` recorded this in writing two phases before it could happen. Its comment at
`:36` said the form "sends `sort_by` and nothing else", and `:46` explained why that was fine: "this
section renders no filter control, so `sort_by` is the only" parameter.

The moment filters entered the URL, submitting sort would have discarded all of them.

The form is now rendered whenever there is **either** a sort control or a filter control, with the
sort label and select behind their own condition inside it. Tested directly: with sorting switched
off, the form still exists and the facets are still bound to it.

### 4.3 A horizontal bar, not a sidebar — in numbers

`snippets/grid-sizes.liquid` derives the card slot from the row left after chrome. Today `chrome_d`
is 96, so at the 1440 container the capped row is 1344 and `(1344 + 32) / 304 = 4` columns fit.

A 240px sidebar plus a 48px gap makes `chrome_d` 384: the capped row is 1056 and only **3** columns
fit — and at the 1200px container a merchant may set, only **2**. Solving for a sidebar that still
paints four columns gives about 112px, which is narrower than the word "Availability".

The horizontal bar costs one control height plus one gap, once. Measured after the change: the grid
is still 2 columns at 156px on a 375px phone and 4 at 312px on a 1440px desktop — identical to before.

### 4.4 Filter quality

A group with a **single value is dropped**. Shopify returns one whenever a collection happens to hold
one vendor or one product type, and rendering it gives the customer a control whose only effect is to
filter nothing out. The rule lives in the snippet so every caller gets it, and the section's
`has_filters` counts only the groups the snippet would actually render — so a collection whose only
filter is degenerate shows no Filter button at all.

Every label, value, count and URL comes from Shopify. The code contains no hardcoded size, colour,
option name or currency symbol; the only literal parameters are `filter.v.price.gte` and
`filter.v.price.lte`, used as fallbacks when the customer has set no bound, and those are the names
Shopify documents.

### 4.5 Nothing renders until a merchant configures filters

`collection.filters` is empty until filters are created in Shopify admin under **Apps › Search &
Discovery › Filters**. Until then the theme renders no panel, no Filter button and no active-filter
row, and `component-facets.css` and `facets.js` are **not loaded at all** — a store with no filters
pays nothing for the feature.

In the Theme Editor only, a note says why, because a merchant who switched the setting on and saw
nothing would reasonably file it as a bug. The live storefront says nothing.

---

## 5. Sort architecture

Unchanged: Shopify's `collection.sort_options`, the store's own default order preserved, the label
"Sort by", and a visible submit rather than submit-on-change — the SC 3.2.2 fix Phase 12 made.

Sort and filters now submit **together**, through the one form.

---

## 6. Mobile filter UX

Below `--bp-md`, once `facets.js` has run, the panel becomes a fixed drawer: a header with a close
button, a scrolling group list with `overscroll-behavior: contain`, and a footer holding Apply and
Clear all that does not scroll — so Apply is reachable however many filters a merchant configures.

**The drawer is opt-in, not the base state.** `position: fixed` is applied only under
`.facets--drawer`, a class the script adds. That ordering is load-bearing: with no script the panel
must be in flow and visible, because the button that would open a drawer is the thing the script was
going to reveal. A fixed panel with no opener is a filter UI a customer cannot reach.

So the no-script mobile experience is a stack of collapsed groups above the grid — already a usable
filter UI, with zero JavaScript.

### 6.1 The scroll lock follows the menu, not the cart

`assets/cart.js` locks by setting `body.style.position = 'fixed'` and restoring `window.scrollY` on
close. That is correct for the cart and it does **not** compose: two owners doing it fight over one
recorded scroll position. The header's menu panel locks with a class instead —
`.menu-open body { overflow: hidden }` — and two classes compose without either knowing about the
other.

The filter drawer follows the header. Asserted in the test suite, against the code with comments
stripped.

---

## 7. Active filters

Applied values render as removable chips **outside** the panel, so a customer on a phone can see what
is applied without opening anything.

Each chip is a link carrying Shopify's own `url_to_remove`, and Clear all is a link to
`collection.url`. They therefore act immediately, while the checkboxes apply on confirm.

**That split is deliberate and is written into the snippet so it is not "harmonised" away.** SC 3.2.2
governs changing the setting of a control; activating a link is not that. Chips are 24px — the SC
2.5.8 floor — because removal is also reachable from the group the value came from, which is the
equivalent control that exception allows. Filter values themselves are 44px, because there is no
larger equivalent beside them.

---

## 8. Empty states

Two different nothings, and they now say different things.

A collection with **no products** is a merchandising state the customer cannot act on — it keeps its
existing words and its link away. A collection whose **active filters match nothing** is one they can
fix in a click, so it says so and offers Clear all. Telling a customer the collection is empty when
they have four filters applied would be false.

Neither invents a product.

---

## 9. URL state

Entirely Shopify's scheme. Checkboxes are named for the filter's own `param_name` and carry Shopify's
own `value`, so checking two boxes in one group submits the parameter twice — which is exactly the OR
encoding Shopify documents. The no-script path therefore produces the same URL the scripted one
would.

The form renders **no page parameter**, so any submission returns to page 1 — which is also what
Shopify's own `url_to_add` does, since it strips pagination.

Back and Forward behave normally because nothing manipulates history: every state change is an
ordinary navigation.

---

## 10. Accessibility

Filter groups are native `<details>`/`<summary>` — no `aria-expanded`, no `aria-controls`, no
`role="button"`, following the precedent `main-product.liquid` set for its description accordion:
"no script, no ARIA to get wrong, and it is keyboard-operable and announced correctly by default."

Checkboxes carry the theme's shared `.visually-hidden` utility rather than re-declaring the hiding
rules, matching the variant picker. They stay focusable and the ring is drawn on the label.

A group is server-rendered **open** when it holds an applied value, so what is active is visible
without interaction.

The drawer traps focus, closes on Escape, returns focus to its trigger, and its `matchMedia` listener
closes it if the viewport grows past the breakpoint — so focus is never trapped in something that is
no longer a drawer.

Measured: **zero horizontal overflow and zero sub-24px targets** across fourteen pages at twelve
viewports.

---

## 11. Performance

| Asset | Raw | Gzipped | Loaded |
|---|---|---|---|
| `facets.js` | 7,055 B | 2.4 KB | Only on a collection with filters configured |
| `component-facets.css` | 13,598 B | 3.8 KB | Same |
| `snippets/facets.liquid` | 14,118 B | — | Same |

Both assets are linked from inside the section's `has_filters` branch, so a store with no filters
configured downloads neither. Theme JavaScript is 22.2 KB gzipped across four files, and no page
loads all of them.

No framework, no dependency, no network layer. Filtering is server-rendered navigation.

*(Correcting a figure given earlier in this project: the theme's total is not "~65KB gzipped" — that
was Phase 9's number with twelve stylesheets. It is 22.2 KB gz of JavaScript and roughly 72 KB gz of
CSS across nineteen files, of which no single page loads more than a fraction.)*

---

## 12. SEO

Shopify emits the canonical through `content_for_header`; the theme adds no second canonical and no
filter-specific one. Filtered URLs are ordinary query strings on the collection's canonical path.

No structured data was added, and none was duplicated.

---

## 13. Testing

A new suite, `facets.py`, 62 assertions, run against four fixture states that mirror what Shopify
actually returns:

| Fixture | What it covers |
|---|---|
| `FILTERS_NONE` | No filters configured in the admin app |
| `FILTERS_ALL` | `list` × 2 (one with swatches), `boolean`, `price_range` — every type the API has |
| `FILTERS_ACTIVE` | The same, with values applied and a price floor set |
| `FILTERS_DEGENERATE` | A one-value group, which is not a choice |

Every field in those fixtures is one shopify.dev documents; nothing is invented.

---

## 14. Theme Editor compatibility

Phase 11's behaviour is intact — `editor.py` still passes 10/10. `facets.js` follows the same
lifecycle contract: idempotent per element, every global binding recorded and released as one unit,
and a teardown on `shopify:section:unload`.

---

## 15. Files created

| File | Purpose |
|---|---|
| `snippets/facets.liquid` | The filter UI, rendered once, generic on `results` |
| `assets/component-facets.css` | Two layouts from one element |
| `assets/facets.js` | The drawer, and only the drawer |

Plus one test suite, `facets.py`, and `collection.filters` fixtures in the harness.

## 16. Files modified

| File | Change |
|---|---|
| `sections/main-collection.liquid` | Filter state, the one-form fix, the Filter trigger, the filtered-empty state, a `show_filters` setting, conditional asset loading |
| `sections/header.liquid` | The search panel; the trigger left byte-identical |
| `assets/header.js` | The search panel's behaviour, in the existing registry |
| `assets/header.css` | The panel, as a layer |
| `locales/en.default.json` | 15 keys |

---

## 17. Known limitations

**Filtering cannot be demoed or QA'd on this machine.** It requires the Search & Discovery app on a
real store. The harness proves the guard renders nothing, proves the populated markup is correct
against documented fixtures, and proves the responsive behaviour — but it cannot prove the real
filter values look right.

**Predictive search is deferred**, §2. The contract is recorded; a catalogue count unblocks it.

**Filtering is not on `/search`**, §3, by decision, with the three hidden inputs recorded for
whoever adds it.

**Theme Check has never been run** — no Shopify CLI in this environment.

**`| t` interpolation escaping is documented but not empirically confirmed.** shopify.dev states
translated content is escaped by default, with `_html` as the only opt-out, and no locale key in this
theme carries that suffix — so the two `| t` calls echoing `search.terms` are safe under the
documented rule. The docs do not explicitly address interpolated *variables*, and that can only be
confirmed on a real store.

**No overlay behind the filter drawer.** Escape, the close button and the trigger all dismiss it; a
click-outside layer would need markup the brief lists only conditionally.

**Shopify's own ceilings apply:** at most 25 filters per store, none on collections over 5,000
products, none on search results over 1,000.

---

## 18. Future recommendations

1. **Install and configure Search & Discovery** before launch, or filtering is invisible.
2. **Supply a catalogue count** to settle predictive search.
3. **Filtering on `/search`**, with the four additions in §3, once the pages/articles contradiction
   has been decided.
4. **Run Theme Check** against a development store.

---

## Appendix — verification

| Suite | Result |
|---|---|
| `validate.py` | 198 / 198 |
| `interact.py` / `interact_cartpage.py` / `interact_product.py` | 49 / 17 / 26 |
| `contrast8.py` | 56 / 56 |
| `layout.py` | 19 / 19 |
| `surfaces.py` | 41 / 41 |
| `editor.py` | 10 / 10 |
| `settings.py` | 28 / 28 |
| `catalog.py` | 54 / 54 |
| `cardcascade.py` | 10 / 10 |
| **`facets.py`** | **62 / 62** |
| `respond.py` | 14 pages × 12 viewports, 0 problems |
| `console.py` | 0 errors across 36 pages |

**570 assertions.**

One method note worth carrying forward, because it caught two false failures in this phase alone:
a test that greps a source file will match the file's own **comments**. Both the "no hardcoded option
parameter" and the "does not use the cart's lock" assertions initially failed against prose that was
explaining the very rule being asserted. Strip comments before asserting on code.

Phase 13 stops here.
