# GOD SQUAD — PHASE 17
## Analytics + Tracking + Marketing Integration

**Status:** delivered · **Date:** 2026-09-25 · **Theme:** `god-squad-theme/`

---

## 0. The finding that defines this phase

**A theme cannot do tracking on Shopify any more, and this one correctly does
none.**

That is not a shortcut. It is what the platform now requires, and four of the
five research dimensions returned **zero theme actions** — verified, not assumed:

> *"To ensure the quality of standard events, partners and merchants cannot
> publish standard events. `Shopify.analytics.publish` only exposes the method to
> publish custom events."* — shopify.dev, Web Pixels API

> *"Code snippets can be used to bypass customer consent requirements, which
> violates the Shopify Terms of Service and can lead to legal liability for
> you."* — Shopify Help Center

Every event the brief asks for — `view_item`, `add_to_cart`, `begin_checkout`,
`purchase` — is emitted by **Shopify**, from a sandbox the theme cannot reach,
in response to the storefront calls the theme already makes. The theme's entire
contribution is to keep making those calls correctly and to stay out of the way.

So Phase 17 ships **no tracking code**, and that is the deliverable. What it does
ship is a measured audit, a standing guard against the tracking code someone will
be tempted to paste in later, and the Shopify Admin configuration the business
actually needs.

It also fixed **a live stored-XSS vector** — surfaced by the privacy work, not by
the tracking work. See §13.

---

## 1. Existing tracking audit

Ran the brief's own PART 1 search terms across all **72 files**, separating an
actual API surface (`gtag(`, `fbq(`, `dataLayer.push`, a script host, an ID
literal) from the same word appearing in English prose.

| Platform | Present |
|---|---|
| Google Analytics (GA4 or legacy) | **none** |
| Google Tag Manager | **none** |
| Google Ads conversion | **none** |
| Meta Pixel | **none** |
| TikTok Pixel | **none** |
| Pinterest, Snapchat | **none** |
| Microsoft Clarity, Hotjar | **none** |
| Segment, Plausible, Matomo, PostHog | **none** |
| `dataLayer` | **none** |
| Error monitoring (Sentry, Bugsnag, Rollbar, Datadog, New Relic) | **none** |

**Hardcoded account identifiers: none.** No `G-`, `AW-`, `GTM-`, `UA-`, no
Meta-shaped 15–16 digit literal, no TikTok-shaped literal.

**Third-party hosts reached: none.** The only external origins in the theme are
`shopify.com`, `schema.org` and `w3.org`.

The words the brief asks about do appear — "tracking" 9 times, "pixel" 28,
"purchase" 5 — and every one is in a comment, a merchant help string, or an ARIA
label. The two that survive comment-stripping are `hero.liquid:224` ("the worst
pixel behind the heading measures 1.0:1", contrast help text) and
`en.default.json:70` ("Product details and purchase", a landmark label).

**31 checks, 0 findings.**

### 1.1 The audit is negative-controlled

An absence report nobody has seen fail is worthless. **12 realistic violations**
were seeded into throwaway copies of the theme — the snippets a developer
actually pastes — and **all 12 were caught**: GA4 and Meta in the layout, a
TikTok pixel in a section, a `dataLayer` push from `cart.js`,
`{{ customer.email }}` in the footer, an id in `localStorage`, a pixel built with
`new Image()`, a `sendBeacon` to an off-origin collector, a `console.log` of a
payload, customer data in a cart attribute, Hotjar, a GTM container.

Two seeds exposed bugs in the auditor before they exposed anything about the
theme:

- **`rollbar` matched inside `scrollbar`** and reported Phase 8's
  `scrollbar-gutter` rule as an installed error monitor.
- **The host check only looked at `src`/`href` attributes** — so it missed a
  seeded Meta Pixel completely, because every real pixel injects its own
  `<script>` and therefore carries its host as a **string literal inside
  JavaScript**. That is precisely the case the check exists for.

Both fixed; the second made the auditor genuinely better.

---

## 2. Shopify Analytics

Native and already working, with no theme involvement. Shopify records orders,
sales, sessions, conversion rate, top products and traffic sources server-side,
and surfaces attribution through `content_for_header`.

`layout/theme.liquid:127` emits `{{ content_for_header }}` once, unmodified,
inside `<head>` — which Shopify documents as required and warns must not be
parsed or altered. **That single line is the theme's entire load-bearing
dependency for analytics and consent**, and there is now a standing assertion on
it.

---

## 3. GA4 status

**Not configured. No measurement ID exists, and none was invented.**

> **GA4 measurement ID required.** Install the *Google & YouTube* channel app
> from the Shopify App Store and connect the Google account. The app installs its
> own app pixel; no theme code is added or needed.

Do **not** paste a `gtag` snippet into the theme. Under the current platform it
would run outside the consent framework, which Shopify states violates its Terms
of Service.

---

## 4. Meta Pixel status

**Not configured. No pixel ID exists, and none was invented.**

> **Meta pixel ID and Conversions API required.** Install the *Facebook &
> Instagram* app, which registers an app pixel and handles the Conversions API
> server-side. Do not add a second `fbq` implementation in the theme — a
> duplicated pixel double-counts every event, including purchases.

---

## 5. TikTok status

**Not configured. No pixel ID exists, and none was invented.**

> **TikTok pixel required.** Install the *TikTok* app. Same rule: one pixel, and
> the app owns it.

---

## 6. Google Ads status

**Not configured.** Google Ads conversion tracking arrives through the same
Google & YouTube channel app as GA4 and shares its purchase signal, so there is
no separate conversion tag to add and nothing to de-duplicate — provided nobody
also pastes an `AW-` tag into the theme.

---

## 7. Data layer

**There is no `dataLayer` in this theme, and there should not be one.**

A `dataLayer` exists to feed Google Tag Manager, GTM belongs in a pixel, and a
pixel cannot read the page. Under the Web Pixels API, app pixels run in a
**strict sandbox implemented with web workers** — no `window`, no `document` —
and custom pixels run in a **lax sandbox**, a sandboxed iframe where
`window.location` returns the sandbox URL, not the storefront's. A `dataLayer`
on `window` is unreachable from either.

Shopify states this directly: pixels cannot capture *"events from DOM scraping,
metadata from DOM scraping, user information such as email and phone from DOM
scraping"*.

---

## 8. Event architecture

Shopify emits **exactly 15 standard events** — enumerated from the reference, not
recalled:

```
page_viewed              product_viewed            collection_viewed
search_submitted         product_added_to_cart     product_removed_from_cart
cart_viewed              checkout_started          checkout_contact_info_submitted
checkout_address_info_submitted     checkout_shipping_info_submitted
payment_info_submitted   checkout_completed        alert_displayed
ui_extension_errored
```

There is **no `cart_updated`, no `cart_created`, no `variant_viewed`**. A pixel
can also subscribe in bulk via `all_events`, `all_standard_events`,
`all_custom_events`, `all_dom_events`.

Five **DOM events** are available on the storefront — `clicked`,
`form_submitted`, `input_blurred`, `input_changed`, `input_focused` — and are
*not* available on customer-account pages or the order-status page.

The theme can publish **custom** events only, via `Shopify.analytics.publish`,
prefixed (`my_app:event_name`). This theme publishes none, because it needs none.

---

## 9. Purchase tracking

**A theme cannot fire a purchase event, and this one does not try.**

`checkout_completed` fires *"once for each checkout, typically on the Thank you
page"*. Three facts the brief's duplicate-protection requirement depends on:

- **Upsells move it.** With post-purchase offers, it fires *"on the first upsell
  offer page instead"*.
- **It can fail to fire at all.** *"If the page where the event is supposed to be
  triggered fails to load, then the `checkout_completed` event isn't triggered."*
  So under-counting is possible; over-counting is what Shopify prevents.
- **Refreshing the thank-you page does not re-fire it** — the guarantee is per
  checkout, and it belongs to Shopify, not to any theme or pixel code.

### 9.1 Every legacy purchase-tracking mechanism is retired

All dates are in the **past** as of 2026-09-25:

| Mechanism | Status |
|---|---|
| `checkout.liquid` (Information, Shipping, Payment) | unsupported |
| `checkout.liquid` + Additional Scripts (Thank you, Order status) | **sunset 2025-08-28** |
| Script tags, Shopify Plus | **sunset 2025-08-28** |
| Script tags, non-Plus | sunset 2026-08-26 |
| `_landing_page`, `_orig_referrer`, `_tracking_consent` cookies | **removed 2025-09-15** |
| `_shopify_s`, `_shopify_y` cookies | **removed 2026-01-01** |

Any tutorial that tells you to paste a purchase tag into Additional Scripts, or
to read `_landing_page` from `document.cookie`, describes a storefront that no
longer exists. **Shopify's own cookie policy page is stale and still lists the
removed cookies; the developer changelog is the one that is correct.**

The theme is asserted to read none of the six retired cookies.

---

## 10. Duplicate event findings

The theme cannot emit an event, so it cannot emit a duplicate one. What it *can*
do is cause Shopify to emit one twice, by making two storefront calls for one
customer action. **That is fully testable here, and it was tested** — the
journey walked in a browser, counting Shopify calls per step:

| Customer action | Shopify calls | Endpoint |
|---|---:|---|
| select a variant | **0** | — |
| set quantity to 2 | **0** | — |
| add to cart (one press) | **1** | `/cart/add.js` |
| open the cart drawer | **0** | — |
| close and reopen the drawer | **0** | — |
| increase a cart line quantity | **1** | `/cart/change.js` q=2 |
| remove the line | **1** | `/cart/change.js` q=0 |

**Opening the drawer makes no call** — it is rendered with the page and shown,
never fetched. A drawer that fetched on open would make Shopify emit a cart event
on every open.

Carried from Phase 14 and still passing: five rapid quantity presses send **one**
request; the add path has a double-submit guard; a removal cancels the queued
change for that line.

### 10.1 Two events this theme's design affects

- **`cart_viewed` is documented as *"a customer visited the cart page"***, and
  the reference does not mention drawers, modals or overlays. This store's cart
  is drawer-first, so `cart_viewed` will fire **rarely** — only when someone
  reaches `/cart`. A funnel that expects `cart_viewed` between `add_to_cart` and
  `begin_checkout` will look broken and will not be.
- **Whether `product_added_to_cart` fires for an Ajax add is undocumented.**
  The reference says only that the event *"logs an instance where a customer adds
  a product to their cart"* and is *"available on the online store page"*. It
  says nothing about Ajax versus form POST. This theme adds exclusively over
  `/cart/add.js`. **This is the single most important thing to verify on the live
  store**, and it is recorded as an unknown rather than assumed either way.

---

## 11. Attribution and UTM behaviour

**Measured, real, and deliberately not changed.** All three GET forms in the
theme discard campaign parameters:

```
landing     ?utm_source=facebook&utm_medium=paid_social&utm_campaign=drop_01
sort     -> ?sort_by=price-ascending
filter   -> ?filter.v.price.gte=&filter.v.price.lte=&sort_by=manual
search   -> ?q=tee&type=product
```

This is the mechanism Phase 13 documented and relied on to drop the `page`
parameter: a GET form discards its action's query string and rebuilds it from its
own fields.

**It is harmless, and "fixing" it would have been worse.** Verified against
primary sources:

- Shopify records `landingPage` and `utmParameters` **server-side at the
  session's first request**.
- **GA4 fixes session source at session start** and does not open a new session
  on a mid-session source change. *(Universal Analytics did the opposite — which
  would have made this form genuinely destructive. UA is retired. Reasoning from
  UA intuition here is exactly the stale-platform-assumption class that has cost
  this project phases.)*
- Meta has already written `fbclid` into `_fbc` with a 90-day life.
- **Dawn behaves identically** — only `q` and `options[prefix]` survive its facet
  forms. No Shopify documentation mentions preserving UTM on filter forms.

Carrying UTM through internal forms would make internal navigation look like
campaign traffic and create self-referrals. The one genuine loss is a narrow
sequence: land with UTM → sort → idle past the 30-minute session timeout →
re-enter from the now-stripped URL. That second session is attributed to direct.

**A reserved-parameter guard was added.** Shopify special-cases `ref`, `source`
and `r` storefront-wide as the marketing referral code, and the value lands in
every order's conversion detail. A theme form field with one of those names would
silently overwrite a real attribution. The theme submits `add`, `checkout`,
`description`, `id`, `note`, `options[prefix]`, `q`, `quantity`, `sort_by`,
`type`, `update`, `viewport` — none reserved, now asserted.

---

## 12. UTM strategy and campaign naming

Conventions, not campaigns. **No campaign was created or launched.**

```
utm_source    the platform            facebook | instagram | tiktok | google | email
utm_medium    how it was paid for     paid_social | organic_social | cpc | email | referral
utm_campaign  {objective}_{subject}_{yymm}    launch_thefaithful_2610
utm_content   the creative            video01 | carousel_a | static_gold
utm_term      keyword, paid search only
```

Rules that keep the data usable: **lowercase everywhere** (GA4 is
case-sensitive — `Facebook` and `facebook` become two sources); underscores, not
spaces; never tag an internal link; and never use `ref`, `source` or `r` as a
parameter name.

Ad-platform campaign naming, for the same reason:

```
{platform}_{objective}_{subject}_{audience}_{creative}_{yymm}
meta_conv_thefaithful_retarget_video01_2610
```

---

## 13. Privacy and consent findings

**No consent work is required in the theme**, and the reason is structural:
Shopify's pixels respect consent because Shopify runs them. The theme has no
tracking to gate.

Verified absent from every theme script: `localStorage`, `sessionStorage`,
`indexedDB`, `document.cookie`, `navigator.sendBeacon`, `new Image(`, an
off-origin `fetch`, and any `console` logging. No customer field is read
anywhere. Nothing is written into a cart attribute.

Three prohibitions now enforced by the test suite rather than by good intentions:
no analytics `<script>` in any Liquid file; no call to
`customerPrivacy.setTrackingConsent()` (consent must *"never [be] done
automatically on behalf of the visitor"*); and nothing reading the six retired
cookies.

### 13.1 A live stored-XSS vector, found and fixed

The privacy question — *what customer-controlled data does the theme render?* —
turned up two values printed as raw markup. **Shopify Liquid does not escape
output.** Rendered with a payload:

```
cart line property   <p class="cart-line__property">Engraving: </p>
                     <img src=x onerror=alert(1)>
cart note            <textarea …></textarea><img src=x onerror=alert(2)>
```

Both broke out and produced a **live element with an event handler**. A line item
property is supplied by whoever posted to `/cart/add.js`; the cart note is also
settable through `/cart/update.js`. Both are untrusted input however they
arrived.

The theme already escaped `search.terms` — the same class of input — in 27
places, so this was an inconsistency, not a policy. Both now carry `| escape`,
verified by re-rendering the same payloads, and a standing suite renders real
payloads through the real snippets rather than grepping for the filter.

**This is a security fix surfaced by Phase 17's privacy work, not tracking
work.** Scoped strictly to tracking, the theme's action list is empty.

---

## 14. Third-party scripts

| Name | Purpose | Pages | Impact | Required | Consent | Recommendation |
|---|---|---|---|---|---|---|
| *(none)* | — | — | — | — | — | — |

The theme loads no third-party script and reaches no third-party host. Once the
Google, Meta and TikTok apps are installed, each registers an **app pixel** that
runs in Shopify's strict sandbox — off the main thread, outside the theme's
critical path, and not a theme asset.

**Error monitoring: none present.** Not recommended for a store this size; the
console suite (38 pages, 0 errors) is the current substitute. If it is ever
wanted, it belongs in a pixel or an app, not in `theme.liquid`.

---

## 15. Performance impact

**Zero.** No script, no request, no byte was added for tracking.

| Surface | requests | CSS gz | JS gz | vs Phase 16 |
|---|---:|---:|---:|---|
| Homepage | 24 | 50.2 KB | 16.4 KB | unchanged |
| Collection | 19 | 41.7 KB | 16.4 KB | unchanged |
| Product | 21 | 35.8 KB | 22.0 KB | unchanged |
| Cart page | 15 | 26.9 KB | 16.4 KB | unchanged |

The only theme change this phase is two `| escape` filters, which alter no asset.

---

## 16. Testing

```
=== Phase 17 (new) ===
tracking     31 / 31   the inventory, PART 1 + PART 29
negctl       12 / 12   seeded violations, all caught
funnel        8 /  8   one action, one Shopify call
escaping      7 /  7   payloads rendered, not grepped
utm           6 measured  all three GET forms drop campaign parameters

=== regression, every prior phase ===
validate    199/199   cartdoc  85/85   surfaces 41/41   facets   62/62
catalog      55/ 55   accounts 52/52   settings 28/28   seo      52/52
images       54/ 54   layout   19/19   editor   10/10   refs     10/10
cardcascade  10/ 10   facetsgate 10/10
interact     49   interact_cartpage 17   interact_product 26
cartqa       14   notes 40   lifecycle 18   negctl(15) 22/22
contrast8    73 measurements, 73 pass
respond      12 pages x 12 viewports — 0 hard problems
console      38 pages — 0 errors
Theme Check  49 files, 84 checks — 2 offenses (both business info, §19)
```

**992 assertions, 0 failures.** Browser suites green in Edge and Chrome.

### 16.1 The test journey, and where it stops

The brief's journey was walked as far as a theme can take it — homepage,
collection, product, variant, quantity, add to cart, open cart, quantity change,
removal — counting Shopify calls at every step (§10).

**No test purchase was made.** There is no store, no checkout and no payment
method in this environment, so no order exists to complete. The brief permits
exactly this: *"Otherwise: verify the event architecture without creating a real
transaction. Document the limitation."*

---

## 17. Event matrix

Every row is emitted by **Shopify**, not by the theme. "Theme role" is what this
theme does to make the event possible and correct.

| Event | Trigger | Theme role | Frequency | Duplicate risk |
|---|---|---|---|---|
| `page_viewed` | any storefront page | none | 1 / page | none — Shopify owns it |
| `collection_viewed` | collection page renders | none | 1 / view | none |
| `product_viewed` | product page renders | none | 1 / view | none |
| `search_submitted` | search results render | one GET form, `q` + `type` | 1 / search | none |
| `product_added_to_cart` | add succeeds | exactly one `/cart/add.js` per press, double-submit guarded | 1 / add | **guarded and measured** |
| `product_removed_from_cart` | quantity → 0 | one `/cart/change.js`, pending change cancelled | 1 / removal | **guarded** |
| `cart_viewed` | **`/cart` page only** | drawer makes no call | rare — see §10.1 | none |
| `checkout_started` | customer enters checkout | native `name="checkout"` submit | 1 / entry* | none |
| `checkout_completed` | thank-you page (or first upsell) | **none possible** | 1 / order | Shopify's guarantee |

\* every entry on Checkout Extensibility shops; first entry only otherwise.

There is deliberately **no row for filter clicks or keystrokes**. The brief warns
against both, and neither is a standard event.

---

## 18. Marketing readiness

The store is ready for paid acquisition in the only sense a theme can be: nothing
in it will break, duplicate or misattribute a campaign.

- **Meta, Google and TikTok** — install the channel app, and the pixel and
  server-side integration arrive with it. Nothing to change here.
- **Retargeting** — product viewers, cart abandoners and checkout abandoners all
  come from `product_viewed`, `product_added_to_cart` and `checkout_started`,
  which fire without theme involvement.
- **Abandoned cart** — Shopify's native abandoned-checkout emails. *Settings ›
  Notifications*, plus *Settings › Checkout* for timing. **Do not build one.**
- **Email** — Shopify Email, Klaviyo or Mailchimp all integrate as apps. The
  theme has no newsletter form; Phase 1 recorded FOOT-03 as BUSINESS DECISION
  REQUIRED and it still is.
- **Social profiles** — two URL settings, both empty, both guarded, and the whole
  social row is suppressed when they are. **No profile was invented**, and there
  is no TikTok setting because no TikTok profile was supplied.

**No campaign was created or launched.**

---

## 19. Shopify Admin configuration required

1. **Install the channel apps** you actually intend to spend on — *Google &
   YouTube*, *Facebook & Instagram*, *TikTok*. Each registers its own pixel.
   **Install at most one per platform.**
2. **Check Settings › Customer privacy** — banner state and configured regions.
   Also confirm whether Shopify Network Intelligence is on; if it is, Shopify's
   Consumer Privacy Policy should be linked from your own privacy policy page
   (ordinary page content, no theme code).
3. **Take Philippine RA 10173 / NPC applicability to counsel.** Shopify publishes
   no APAC-specific consent guidance, and this is a legal question, not a
   technical one.
4. **Verify `product_added_to_cart` fires on an Ajax add** (§10.1). One add to
   cart with the pixel debugger open settles it. This is the highest-value
   fifteen minutes in this document.
5. **Do not paste any tag into the theme or into Additional Scripts.** Additional
   Scripts was sunset on 2025-08-28.
6. Carried forward: Search & Discovery filters (P13), checkout branding (P14),
   confirm the customer-account system (P15), social sharing image and the
   two `theme_info` fields (P16).

---

## 20. Files created

**None in the theme.** It is the same 72 files it was at the end of Phase 16.

Test suites, in `scratchpad/phase17/`: `tracking.py` (31), `negctl.py` (12
seeded), `funnel.py` (8), `escaping.py` (7), `utm.py` (measurement).

---

## 21. Files modified

| File | Change |
|---|---|
| `snippets/cart-line-item.liquid` | `| escape` on both halves of a line item property (§13.1) |
| `snippets/cart-note.liquid` | `| escape` on `cart.note` (§13.1) |

Two filters. Nothing else in the theme changed this phase.

---

## 22. Known limitations

1. **No live store.** Nothing in Shopify Admin could be inspected, so "not
   configured" for GA4, Meta, TikTok and Google Ads means *not in the theme* —
   an app pixel could already exist in an Admin nobody has shown me. **Check
   Settings › Customer events before installing anything.**
2. **No test purchase.** No store, no checkout, no order. `checkout_completed`
   is documented, not observed.
3. **Ajax `product_added_to_cart` is undocumented** (§10.1) and this theme adds
   exclusively over Ajax. Recorded as an unknown; §19.4 is the check.
4. **`cart_viewed` will be rare** by design, because the cart is a drawer.
   Expected, not a defect — but a funnel report will look odd until someone
   knows why.
5. **Shopify's own cookie documentation is stale**, still listing cookies
   removed in 2025 and 2026. Where the help centre and the developer changelog
   disagree, this document follows the changelog.
6. **Two Theme Check errors remain**, both business information carried from
   Phase 16: `theme_support_email` and `theme_documentation_url`.
7. **Safari untested.** Edge and Chrome only, as in every prior phase.

---

## 23. Future recommendations

- **Verify the Ajax add event first** (§19.4). If `product_added_to_cart` does
  *not* fire for Ajax adds, the fix is a custom pixel subscribing to a custom
  event the theme publishes — and that is the one circumstance in which this
  theme should ever contain analytics code.
- **Install one app per platform, then stop.** The most common tracking defect on
  a Shopify store is a channel app *and* a pasted pixel both firing, which
  double-counts revenue.
- **Give it two weeks before judging the data.** Attribution is not readable
  immediately after an order — `momentsCount` returns null while processing, and
  the admin conversion summary *"might take up to 48 hours to display"*. QA that
  checks an order seconds after placing it produces a false negative.
- **Revisit error monitoring** only if console errors ever appear. They do not
  today, across 38 pages.
- **Keep the prohibition tests running.** They are the reason the next person
  cannot quietly paste a `gtag` snippet into `theme.liquid` and break consent
  compliance.

---

**STOP AFTER PHASE 17.**
