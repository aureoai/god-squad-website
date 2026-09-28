# -*- coding: utf-8 -*-
"""The store-setup runbook — the one section both structural critics asked for.

Sixteen section critics agreed the manual is trustworthy on mechanism and thin on
completeness. The two that judged STRUCTURE rather than prose reached the same
conclusion independently: the manual documents the theme and omits the store.
Critic 16 put it exactly — "the deficit is one section wide rather than diffuse",
and §9 (the integration contract) is "genuinely the best thing in the manual" but
states platform facts rather than an order of operations.

Everything here comes from `harvest_ops.py`, which read it out of the theme
itself: 26 settings with no default, 13 schema strings that state a requirement,
and the app and platform dependencies named in the code. Nothing is invented, and
nothing is a Shopify tutorial — this is only what THIS theme needs and the order
it needs it in.

Exported as RUNBOOK for assemble.py to insert after the integration contract.
"""

RUNBOOK = """## The store-setup runbook

The order of operations for connecting this theme to a real Shopify store. §9 states the platform facts; this is the sequence, and it exists because a correctly-built surface in this theme renders **nothing** when its data is absent — which is the failure an integrator hits first and diagnoses last.

Every requirement below is quoted from the theme's own schema strings or derived from a setting that ships with no default. None of it is general Shopify advice.

### Stage 0 — before the theme goes anywhere

| Do this | Why |
|---|---|
| Put the project under version control | There is no `git` repository. Phase 1 logged it as DEBT-12/DEBT-13 and recommended fixing it before Phase 2; nineteen phases later it is still a plain OneDrive folder. Do this before anything starts changing against a live store |
| Preserve the QA suite | 228 Python files and the only Theme Check runner live in a session temp directory, not in the project. When it is cleared, every measured claim in every phase document stops being reproducible |
| Decide the customer-accounts mode | `templates/customers/` is **deliberately absent** — that absence is Shopify's auto-upgrade trigger for new customer accounts, and the header uses `<shopify-account>`. Do not add legacy customer templates back |
| Fill two theme properties | `theme_support_email` and `theme_documentation_url` are the only two Theme Check offences outstanding. They are business information, not code |

### Stage 1 — upload

There is **no Shopify CLI in this project** and the theme has never been uploaded. Zip `god-squad-theme/` and upload it through Shopify admin → Online Store → Themes → Add theme → Upload zip. Do **not** publish it yet.

Expect, on first preview: every image slot empty, the hero without a photograph, the featured-collection band absent, no footer menus, and the filter UI missing. All of that is correct for a store with no data. Stages 2–6 fill it.

### Stage 2 — brand and global settings

Theme settings → Brand. These are the settings that ship with **no default**, so nothing renders until each is filled:

| Setting | Consequence while empty |
|---|---|
| `logo` | The wordmark falls back to text. The current raster wordmark carries heavy transparent padding and renders at roughly half its intended size — **upload a vector master**, not the existing PNG |
| `favicon` | Browsers show their own default mark. None exists in the project |
| `share_image` | Social shares have no image card |
| `social_facebook_url`, `social_instagram_url` | "Each icon appears once its address is filled in, and none is shown otherwise." Add only accounts that actually exist |

Also confirm the two font families resolve in Shopify's library. The theme loads exactly two — Playfair Display 900 and Jost 400/500/600, the latter with 500 and 600 registered through `font_modify`. There is no third font: the design names a script accent, but nothing in the theme consumes it.

### Stage 3 — navigation

The theme ships **no menus of its own** and reads the merchant's.

1. Build the main menu in **Navigation**. The header renders it directly; below `--bp-lg` it is the *only* navigation, through the mobile panel.
2. Build the footer menus. `footer.liquid`'s `menu` setting is a `link_list` with no default, and its own schema warns: *"The theme ships no footer menu of its own, and a column with no links does not render on the live store."* Each footer column needs its own menu selected.

### Stage 4 — pages and policies

Two buttons in the theme are **hidden until a destination exists**, deliberately, so they never render as dead links:

| Control | Requirement |
|---|---|
| Our Story button (`our-story.liquid` → `button_url`) | *"No Our Story page exists in this project yet… Create the page in Shopify admin first, then select it here."* |
| Hero button (`hero.liquid` → `button_link`) | *"The button is hidden until this points somewhere. No destination has been supplied for the collection yet."* Point it at the collection you want the hero to sell |

Publish the store policies as well — the footer renders whichever ones exist.

### Stage 5 — the catalogue

Nothing about products is in the theme; Shopify is the source of truth for every product, price, variant, image and stock level.

1. **Create products with real names.** Not a formality: a wrapped product name in the cart exposed a live typography defect in Phase 18 that the short invented fixture names had hidden completely. Long names, real descriptions and real image aspect ratios are what will surface the next one.
2. **Create the collection the homepage points at.** `featured-collection.liquid`'s own schema is explicit: *"Products, prices, images and availability all come from this collection. Nothing is set in the theme. Until a collection is chosen the section does not render on the live store."*
3. **Configure option-value swatches.** Swatch rendering appears in six files (product cards, facets, the variant picker). Colour swatches read Shopify's option-value swatch data; without it the colour name still shows — the mark is never the only carrier — but the swatch does not.
4. **Turn on inventory tracking.** The low-stock line and the sold-out states read real inventory. `low_stock_threshold` is **3**, set in both `templates/product.json` and the schema default.
5. Choose the product image ratio (`product_image_ratio`) — one ratio governs the whole catalogue.

### Stage 6 — the one app dependency

**Install Shopify's Search & Discovery app and create at least one filter.** Until you do, the collection page's filter UI does not exist, whatever the theme setting says. The theme states it plainly: *"Filters are created in Shopify admin under Apps › Search & Discovery › Filters. Until at least one exists, nothing is shown here whatever this is set to."*

This is the only app the theme depends on.

### Stage 7 — payments, checkout and markets

| Item | Note |
|---|---|
| Wallets | `payment_button` is rendered on the product page and the cart page. Enabling Shop Pay / Apple Pay / Google Pay makes the accelerated buttons appear. Their internals are Shopify's markup — the theme styles the container only and cannot restyle the button |
| Currency and money format | Every price runs through the `money` filter; the format is a store setting |
| Markets / multiple languages | `cart.js` builds every Ajax URL from `window.Shopify.routes.root` precisely so a locale-prefixed store keeps working. If you enable Markets, re-test add-to-cart first — a hardcoded path would have 404'd silently, and this is the guard against it |

### Stage 8 — the five things only a real store can verify

The theme was built and measured entirely offline. These five were explicitly **not** verifiable and should be the first smoke test after upload:

1. **Section Rendering API responses** — the Ajax cart applies returned sections; only a live store returns real ones.
2. **Real `content_for_header` output** — emitted once, unmodified, at `layout/theme.liquid:127`. Everything the theme gets from the platform arrives through it.
3. **Image CDN behaviour** — `image_url` / `image_tag` widths, formats and focal-point crops against real uploads.
4. **`paginate.parts` URLs** — the shared paginator builds its links from them.
5. **Theme Check against a live store** — the offline run reports two business-information offences; a live run can see more.

Add one more to that list: **open the Theme Editor and click through every section's settings.** Phase 11 found that a purely cosmetic toggle had broken the purchase flow, and editor defects only surface in the editor's own section lifecycle.

### Stage 9 — what will still look empty, and why that is correct

| Surface | Renders nothing until |
|---|---|
| Hero photograph | an image is uploaded (Stage 2/4) |
| Featured collection band | a collection is chosen (Stage 5) |
| Collection filters | Search & Discovery has a filter (Stage 6) |
| Footer columns | each has a menu (Stage 3) |
| Footer social icons | each address is filled (Stage 2) |
| Hero and Our Story buttons | each has a destination (Stage 4) |
| Announcement-bar icon and link | filled, both optional |
| Accelerated checkout buttons | wallets are enabled (Stage 7) |

None of these is a bug. The theme was built so that absent merchant data renders nothing rather than rendering a placeholder, a dead link or an invented value — which is the same rule that kept fake products, fake reviews and fake claims out of it for nineteen phases.
"""
