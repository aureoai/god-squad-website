# GOD SQUAD — PHASE 15
## Customer Account + Order Tracking + Post-Purchase UX

**Status:** delivered · **Date:** 2026-09-24 · **Theme:** `god-squad-theme/`

---

## 0. The finding that reshaped this phase

**The Phase 15 brief was written against legacy customer accounts, and Shopify
deprecated them on 26 February 2026 — seven months before this phase started.**

That is not a quibble about terminology. It removes most of the brief's scope
from the theme's reach entirely, and it makes one of the brief's instructions
actively harmful to the merchant. Because getting this wrong would have cost the
whole phase, it was established before a line was written, by twelve researchers
working six areas from two independent angles — the reference documentation and
Dawn's shipped source — and then adversarially reconciled.

Five facts, each from a primary source:

1. **Legacy customer accounts are deprecated.** *"Legacy customer accounts are no
   longer available to new stores and existing stores not using it."*
   — shopify.dev changelog, 2026-02-26

2. **Shopify tells theme developers to stop shipping the files.** *"Theme
   developers should no longer include legacy customer account liquid files."*
   — same changelog

3. **Their absence is the upgrade trigger, which inverts the intuitive guess.**
   *"Publishing a theme without these templates automatically upgrades merchants
   to the latest customer accounts experience, which operates independently of
   themes."* — shopify.dev templates reference. Shipping `templates/customers/*`
   does not make a theme safer; it **withholds the merchant's upgrade.**

4. **Shopify's own reference theme has already removed them.** Dawn v16.0.0
   (2026-08-10) deleted all seven templates *and* all seven sections.

5. **The account experience is not on this origin and the theme cannot style
   it.** It is served from `shopify.com/<store-id>/account`, and its branding
   comes from *checkout* settings: *"Customer accounts: use branding from your
   checkout settings"* against legacy's *"use branding from your online store
   theme settings"* — the exact inverse.

**So Parts 2, 3, 4 and 5 of the brief — order history, order details, customer
information, account navigation — cannot be built in this theme.** Not "were
descoped": there is no surface to build them on. Every one of them now lives on
a Shopify-hosted page this theme does not serve, cannot template and cannot
style. The only way to make them theme-owned again would be to ship the
deprecated legacy templates, which is the one action Shopify explicitly tells
theme developers not to take and which would strand the merchant on a sunsetting
system.

What *is* in the theme's reach is the account **entry point**, and that is where
this phase's code went.

---

## 1. Customer account architecture

**Which system is this store on? I could not determine it, and neither can the
theme.**

The brief opens by asking me to inspect the store's customer-account
configuration and not to assume. There is no store connected to this environment
and no Shopify CLI, so I cannot read it. That would be a soft limitation except
for a harder one the research settled:

> **There is no Liquid-readable way to detect which account system is active.**

- `shop.customer_accounts_enabled` is documented as *"Returns true if the store
  shows a login link."* It is **true under both systems** and says nothing about
  which.
- `shop.customer_accounts_optional` is an independent *checkout policy* flag
  ("optional to complete checkout"). The name invites the wrong reading; it
  carries zero information about new vs legacy.
- No third property exists. All 33–36 `shop` properties were enumerated: there
  is no `customer_accounts_version`, no `customer_accounts_url`.
- The popular forum workaround — `{% if routes.account_login_url contains
  'shopify.com' %}` — is unsound. `account_login_url`'s documented value is the
  *relative* `/account/login` even on a store whose `account_profile_url` is an
  absolute `shopify.com` URL. String-matching a route tells you nothing.

**Therefore the theme has ONE code path and branches on nothing.** That is not a
compromise, it is the correct design: a merchant can also revert an upgrade
within 30 days, so a theme that hard-assumed one system at install time could be
wrong a week later on the same store, with no signal that anything changed.

`shop.customer_accounts_enabled` is used exactly once, as what it is documented
to be — a show/hide gate. The suite asserts that count is one.

### 1.1 What this theme does about the legacy templates: nothing, deliberately

`templates/customers/` does not exist and never has. That is now the
*recommended* state, and it means this theme already satisfies the condition for
Shopify's automatic upgrade. **No migration risk was introduced by this phase**,
because there was nothing to delete — worth stating plainly, since deleting
those files on a live store is a merchant-visible state change that would belong
in a release plan, not a code commit.

Eight separate assertions hold that absence in place, each seen to fail against
a seeded violation: no `templates/customers/`, none of the seven template names,
no `main-account`/`main-order`/`main-login`/… section, and no customer
`{% form %}` tag anywhere in the theme.

---

## 2. Account entry point

This is the whole of Phase 15's code surface, and it is in
`sections/header.liquid`.

**Before** — a working, fully-tested link:

```liquid
<a class="header__control" href="{{ routes.account_url }}">
  {% render 'icon-account' %}
  <span class="visually-hidden">{% if customer %}Account{% else %}Log in{% endif %}</span>
</a>
```

**After** — Shopify's own component, per your decision to adopt it:

```liquid
{%- if shop.customer_accounts_enabled and section.settings.show_account -%}
  <shopify-account
    class="header__control header__account"
    menu="{{ settings.customer_account_menu | default: 'customer-account-main-menu' }}"
  >
    <span class="header__account-avatar" slot="signed-out-avatar">
      {% render 'icon-account' %}
      <span class="visually-hidden">{{ 'header.account' | t }}</span>
    </span>
  </shopify-account>
{%- endif -%}
```

Four decisions inside that block:

**One entry point, not two.** The old link is not kept beside it. Two account
controls would behave differently from one another — one opening a sheet in
place, one navigating off-site — and the 375px end cluster has no room for a
second control anyway.

**The slot keeps the brand's mark.** `signed-out-avatar` is one of the three
things Shopify publishes as contractual, and without it the header would show
Shopify's default avatar in place of the account icon Phase 3 drew to the Phase 2
icon contract.

**The hidden label is deliberate belt and braces.** Dawn ships this component
with no label at all, which implies Shopify names the control itself. "Implies"
is not good enough for a Level A requirement I cannot test from here, so a
visually-hidden name goes in the slot. If Shopify sets its own `aria-label` that
wins and this is ignored; if it does not, the control is still named. Both
outcomes are correct — whereas omitting it has an outcome that is an unnamed
control (SC 4.1.2).

**Two gates, both preserved.** The platform flag and the existing merchant
`show_account` setting. Nothing else in the header changed.

### 2.1 The size reservation that turned out to be dead

A custom element has no dimensions until its script runs, so the usual guard is
a `:not(:defined)` rule reserving the box — Dawn ships one, and so did the first
version of this phase.

**Measurement killed it.** With the `:not(:defined)` rule removed, the element
still measured 44×44 at all seven viewports. With *every* account sizing rule
removed, still 44×44. Both rules had been dead from the moment they were
written.

The reason is that the element carries `class="header__control"` — the class
every header control already uses — and that class sets `min-width` and
`min-height` to `--target-min` inside a flex cluster. The box was reserved by a
rule that predates Phase 15 entirely.

This is **better** than a `:not(:defined)` reservation, not merely equal to it.
That rule stops applying the instant the component upgrades, leaving the
upgraded element free to be any size. An author rule on the element wins over
the component's own `:host` styles, so the 44px target floor holds permanently.

Both dead rules were removed. The end cluster measures **148px at every viewport
from 375 to 1920** — the same figure Phase 13 recorded before this phase touched
anything, so the component introduced no layout change at all.

---

## 3. Login behaviour

**Shopify's, entirely.** The theme contains no authentication of any kind: no
login form, no password field, no session handling, no `customer_login` form
tag, no token. Asserted and negative-controlled.

Under current customer accounts there is no password and no registration step to
build — *"Passwords aren't supported. Passwordless sign-in means that everyone
that signs in has verified that they have access to their email address"* — and
*"There's no way to require customers to complete a registration form … before
they sign in."*

The component handles the transition. On a store still using legacy accounts,
Shopify documents it as degrading to exactly what the old control was: *"for
shops using legacy customer accounts, the avatar links directly to the sign-in
page instead."* So the replacement loses nothing on either system.

One route fact worth recording for any future phase: `routes.account_login_url`
and `routes.storefront_login_url` are **not** interchangeable. The first lands
the customer on the account order index after sign-in; the second returns them
to the page they came from and emits `/customer_authentication/login?return_to=…`
— which is also the component's own `sign-in-url` default. For a storefront, the
second is almost always the one you want. The theme links neither, because the
component owns the transition.

---

## 4. Account dashboard

**Shopify hosts it. The theme has no dashboard and must not have one.**

`routes.account_url` goes directly to the **order index**, not to a profile
landing page — a detail worth knowing before anyone labels a link "My account"
and expects a dashboard.

What the merchant controls is the *menu inside the account sheet*, and that is
now a theme setting:

| Setting | Type | Default | Where |
|---|---|---|---|
| `customer_account_menu` | `link_list` | `customer-account-main-menu` | Theme settings › Customer accounts |

**Global, not a section setting.** shopify.dev's component page shows
`section.settings.customer_account_menu`; Dawn v16 defines it as a global
`link_list`. Dawn is right and the doc example is misleading — and a global
setting is also the precedent Phase 11 set for the logo. Copying the doc's form
into a theme that defines the global yields an empty `menu` attribute and a
sheet with no links.

The setting's help text says the part that is easy to get wrong: leaving it
empty does **not** fall back to a default set of links; the sheet simply has
none.

---

## 5. Order history · 6. Order details · 7. Tracking · 8. Customer information

**None of these four is implementable in the theme, and the theme deliberately
contains nothing for them.**

They all live on Shopify's hosted account pages, on a different origin, styled
from checkout settings. There is no theme surface for an order list, an order
detail view, a tracking panel or a customer profile, because there is no theme
template that renders at those URLs any more.

The theme is asserted to contain, across every `.liquid` and `.js` file:

- no read of any `order.*` field
- no read of any `fulfillment` or `tracking_*` field
- no hand-built `/account/orders/…`, `order_status_url`, `customer_order_url` or
  `/authenticate?key=` URL
- no `routes.account_*` link at all

Every one of those was seeded as a violation and caught.

### 5.1 What the research found anyway, and why it is recorded here

The order and fulfillment research is preserved in this document even though no
code came out of it, for one reason: **if this store is on legacy accounts and
you decide to stay there, somebody will have to build these surfaces, and these
are the traps.** They are expensive and mostly silent.

- **`order.fulfillments` does not exist in theme Liquid.** It exists in Admin
  REST, Admin GraphQL, the Customer Account API and Order Printer Liquid — so
  nearly every search result uses it. In a theme it iterates nothing, renders
  nothing, throws nothing and passes Theme Check. Tracking is reachable only via
  `line_item.fulfillment.tracking_number` / `.tracking_url` / `.tracking_company`.
- **`order.total_price` is calculated *before* refunds** — a verbatim note on the
  property. Showing it for a refunded order is a customer-facing money bug. Dawn
  uses `order.total_net_amount`.
- **`{% if line_item.product %}` is not a deleted-product guard.** A deleted
  product returns an EmptyDrop and *"EmptyDrop objects are also truthy"*. The
  guard passes and everything inside renders blank. Use `!= blank`. Dawn ships
  the truthy pattern in its cart, where the product provably still exists —
  copying that snippet onto an order page is the likeliest way to ship this bug.
- **`line_item.variant_title` does not exist** in Liquid. Zero occurrences in
  Shopify's object data. It exists in the Admin APIs and in blog snippets, and
  renders as an empty string with no error. Use `line_item.variant.title`.
- **`line_item.price`, `.line_price`, `.total_discount` and `.discounts` are
  deprecated** because they exclude automatic discounts and discount codes. They
  render a plausible number that is simply wrong on any discounted order — and
  correct on all your undiscounted test data.
- **`fulfillment_status_label` is localized**, and the five documented values
  belong to the *label*, not to the raw `fulfillment_status` field, which has no
  documented values at all. Never string-compare a label.
- **`customer.orders` caps at 20 per `{% paginate %}`**, and an unpaginated
  `{% for %}` silently truncates at 50.
- **Every money field is an integer in the currency subunit.** `{{ order.total_price }}`
  without a `money` filter prints `12999`.
- **There are three different order URLs** — `customer_url` (token path),
  `order_status_url` (`/authenticate?key=`), `customer_order_url` (shopify.com
  host, numeric id + JWT) — and the brief's assumed `/account/orders/<id>?key=`
  is none of them.

Where the brief asks for a neutral "tracking information will appear here when
available" message: correct instinct, and there is no theme surface to put it on.

---

## 9. Mobile UX

The account control is in the header's end cluster, which renders at every
width — so it is present on desktop and mobile without a second implementation,
and Shopify's own requirement that the component be visible in both headers is
met by the existing layout rather than by new markup.

Measured at 375, 390, 430, 768, 1280, 1440 and 1920, in Edge and Chrome:

| | |
|---|---|
| control box | **44×44 at every viewport** |
| end cluster | **148px at every viewport** (3 controls × 44 + 2 gaps × 8) |
| every sibling | 44×44 — a uniform row, so nothing moves when one is replaced |
| horizontal overflow | none at any viewport |

The full responsive sweep (18 pages × 12 viewports) reports **0 hard problems**.

There is no mobile account navigation to build, and no stacked order list,
because there is no order list. The brief's mobile order-history requirements
apply to a surface Shopify now owns.

---

## 10. Accessibility

| Item | State |
|---|---|
| Semantics | The control is a custom element Shopify upgrades to a button. No clickable `div` or `span` anywhere. |
| Accessible name | Supplied in the slot as visually-hidden text, from the locale file. See §18.1 — this is the one item that needs live verification. |
| Keyboard | Inherits the theme's global `:focus-visible` ring on the element. |
| Target size | 44×44, measured, from the shared `--target-min` token. |
| Icon | `aria-hidden="true"`, decorative — the name is the text beside it. |
| Status by colour | Not applicable: the theme renders no order status. |
| Contrast | 73 measurements across the theme, all passing. The control carries no text of its own. |

The brief's accessibility requirements for order links ("View order #1234" rather
than "View"), order tables and status badges all apply to surfaces Shopify now
owns.

---

## 11. Security

This is where the research changed the theme's test suite, not its code.

> **The `customer` object is global for any signed-in visitor** — *"directly
> accessible globally when a customer is logged in"* — **not scoped to account
> templates.**

That matters here because of something this theme does heavily: the **Section
Rendering API inherits the Liquid context of the requested page**. So a single
`{{ customer.email }}` in a shared snippet would not only render on every page —
it would be serialised into every `?sections=` response the cart makes. The leak
vector is a shared snippet plus section rendering, not some mythical
`/account.json` endpoint.

The theme is therefore asserted to contain **no read of any customer field at
all**, printed or otherwise. Both the output form and the bare read were seeded
as violations and caught.

Everything else the brief asks for:

- **No custom authentication.** No login form, no password field, no session, no
  token.
- **No customer data in any client-side store.** `localStorage`, `sessionStorage`,
  `indexedDB`, `document.cookie`, `caches.open` and service-worker registration
  are each asserted absent from every theme script. This is the one caching risk
  a Liquid theme *can* create — data that survives logout on a shared device.
- **No console logging.** Asserted across all theme JavaScript.
- **No arbitrary order lookup.** The theme reads no order object and builds no
  order URL, so there is nothing to point at another customer's order.
- **No customer data in a URL, a `data-` attribute or a query string.** The
  hygiene sweep checks these shapes directly.

Two facts worth recording because they contradict reasonable assumptions:

- **A Liquid theme cannot set any HTTP response header.** Shopify already serves
  account routes as `private, no-store`. The widely-repeated advice about setting
  `Cache-Control` on customer routes is Hydrogen/Oxygen guidance with no Liquid
  counterpart.
- **The order-status page is not private.** *"The unauthenticated Order status
  page can be accessed by anyone who has a direct link."* It redacts PII rather
  than blocking access — so any future phase must not treat that URL as a secret.

---

## 12. Performance

**This phase added zero JavaScript and zero network requests.**

No theme script was touched. The component's own script is served by Shopify
through `content_for_header`, which every Shopify storefront already loads — so
there is no new dependency, no new file, and nothing to defer.

CSS: `assets/header.css` grew by the token mapping and the avatar rule, then
shrank again when measurement showed the sizing rules were dead. Net change is
one rule of custom properties and two small rules for the slotted icon.

No image is loaded for the account control — the avatar is the existing inline
SVG snippet, which costs no request.

---

## 13. Theme Editor compatibility

Phase 11's architecture is intact. Phase 15 added **one global setting** and
changed **one help string**:

| Change | Where |
|---|---|
| New group "Customer accounts" with `customer_account_menu` (`link_list`) | `config/settings_schema.json` |
| The handle added to both `current` and the God Squad preset | `config/settings_data.json` |
| `show_account`'s help now says where the account pages are styled | `sections/header.liquid` schema |

The group sits directly after Cart, because the account control sits beside the
cart control in the header and the two read together in the editor sidebar.

All 13 section schemas and all 12 JSON files parse. The editor suite, the
settings suite and the section-lifecycle suites are unchanged and green.

---

## 14. Shopify Admin configuration required

Five items, none of which is a code task, and the first is the one to do first.

1. **Confirm which customer-account system this store uses.**
   *Settings › Customer accounts.* This is the Phase 1 item recorded as BUSINESS
   DECISION REQUIRED and it is still open. The theme is correct either way, but
   the answer determines whether anything else in this list applies.

2. **Create the account menu.** *Navigation › Add menu*, handle
   `customer-account-main-menu`, then select it in *Theme settings › Customer
   accounts*. Until this exists, the account sheet opens with no links in it.

3. **Brand the account pages — in the checkout and accounts editor, not here.**
   *Settings › Checkout › Customize.* This is the inverse of legacy accounts and
   the single most likely thing to be looked for in the wrong place. The Phase 2
   design tokens do not reach those pages; the theme cannot make them look like
   the store. Hiding built-in elements there is explicitly unsupported.

4. **Optionally connect a subdomain** so the account pages sit on
   `account.godsquad.com` rather than `shopify.com/<store-id>/account`. Cosmetic,
   but it is the only lever that makes the hosted pages feel like the store.

5. **Checkout branding** (carried from Phase 14) and **filters via Search &
   Discovery** (carried from Phase 13) remain outstanding.

---

## 15. Testing results

```
=== Phase 15 ===
accounts              52 / 52      the entry point, and the absences
negctl                22 / 22      every absence assertion seeded and seen to fail
geom                   7 viewports, 0 problems   (Edge and Chrome)
hygiene               71 files scanned, 0 findings

=== regression, every prior phase ===
validate             198 / 198     surfaces      41 / 41     catalog       55 / 55
cartdoc               84 /  84     facets        62 / 62     settings      28 / 28
layout                19 /  19     editor        10 / 10     cardcascade   10 / 10
interact              49           interact_cartpage  17     interact_product  26
cartqa                14           notes         40          lifecycle     18
contrast8             73 measurements, 73 pass
respond               18 pages x 12 viewports — 0 hard problems
console               38 pages — 0 errors
```

**796 assertions, 0 failures**, plus 22 seeded violations, 216 viewport
measurements and 38 console checks. Browser suites run under Edge 153 and
Chrome, both green.

### 15.1 The negative control is the point

`accounts.py` is almost entirely a list of things the theme must *not* contain,
and an absence assertion that has never been seen to fail is indistinguishable
from a typo in a regex. `negctl.py` seeds 22 violations into a throwaway copy of
the theme — one at a time — and requires the suite to catch each.

It caught its own blind spot doing it. Three of the assertions read a *pre-built*
harness page, so a seed that changed the theme copy never reached them: one
genuinely broken theme (an account control stripped of its shared class) passed
clean. The suite now renders the header from the theme under test, which makes
every markup assertion seed-sensitive. Two earlier rounds also failed for seeds
landing inside `{% comment %}` blocks — the seeds were wrong, not the
assertions, and both were fixed rather than explained away.

---

## 16. Files created

**None in the theme.** Phase 15 added no template, no section, no snippet and no
asset — the theme is the same 71 files it was before. That is the correct
outcome for this phase and it is worth stating explicitly rather than leaving it
to be inferred.

Test suites created, in `scratchpad/phase15/`:

| File | What it holds |
|---|---|
| `accounts.py` | 52 checks: the entry point, and every deliberate absence |
| `negctl.py` | 22 seeded violations, proving those 52 can fail |
| `geom.py` | the control's box at 7 viewports, in two browsers |
| `hygiene.py` | the PART 19/20 placeholder and private-data sweep |

---

## 17. Files modified

| File | Change |
|---|---|
| `sections/header.liquid` | The account link becomes `<shopify-account>`; `show_account`'s help string |
| `assets/header.css` | The `--shopify-account-*` token mapping and the slotted avatar |
| `config/settings_schema.json` | New "Customer accounts" group with `customer_account_menu` |
| `config/settings_data.json` | The menu handle in `current` and in the preset |
| `locales/en.default.json` | `header.log_in` removed — dead with the old control |
| *(harness)* `phase9/catalog.py`, `phase8/validate.py` | unchanged this phase |

---

## 18. Known limitations

1. **The account system could not be determined.** No store, no CLI, and no
   Liquid signal exists. The theme is built to be correct under all three
   configurations, which is the right answer regardless — but §14.1 is a real
   pre-launch check, not a formality.

2. **The component's accessible name needs one live check.** This is the single
   item I could not verify. Dawn ships the component with no label, implying
   Shopify names it; this theme supplies a visually-hidden name in the slot so
   that the control is named under either behaviour. What cannot be checked from
   here is whether the two combine into a doubled announcement. **Open the store
   with a screen reader and listen to the header control once.** If it announces
   twice, delete the `<span class="visually-hidden">` from the slot.

3. **The control is not focusable until Shopify's script upgrades it.** Measured:
   `tabIndex` is -1 while undefined. A custom element cannot be tabbed to or
   clicked before its script runs, so if that script is blocked the control is
   inert — where the old `<a href>` worked with no script at all. This is
   inherent to the component and is the cost of the approach you chose. It was
   not worked around, because a fallback link inside the slot would nest an
   anchor inside the upgraded button.

4. **The harness can never test the component.** It does not load Shopify's
   script, so the element is permanently un-upgraded there. Every measurement in
   this phase is of the *reservation*, never of the component. The account sheet
   itself — its layout, its menu, its token mapping, its dialog position — is
   verifiable only on a live store.

5. **`--shopify-account-dialog-position-top` is deliberately unset.** Its
   semantics could not be settled from the documentation, and this theme has a
   sticky header that a wrong guess would put the sheet underneath. Shopify's
   default is in place; this is the first knob to check live.

6. **Theme Check was not run** — Shopify CLI is not installed here. Everything it
   would check on this phase's surface was checked another way: JSON validity
   (12 files), section schemas (13), translation completeness, undefined custom
   properties, raw hex, `!important`. **Run `shopify theme check` before
   launch.**

7. **The `form-tags` research dimension did not reconcile.** Its adversarial
   cross-checker stalled on all six attempts; the two raw researcher reports
   exist but were never reconciled. It covered the legacy customer `{% form %}`
   tags, which this phase deliberately does not use — so nothing here rests on
   it. If anyone ever builds legacy account templates, that dimension needs
   redoing.

8. **Against Shopify's Theme Store list the theme is still missing six
   templates** — `article`, `blog`, `list-collections`, `page.contact`,
   `password`, `gift_card`. You chose bespoke, so this is not binding; it is
   recorded because Phase 1's SHOP-09 tracks the same list and a missing template
   serves an error page to anyone who reaches its URL.

---

## 19. Future recommendations

- **Answer §14.1 first.** Everything else about accounts follows from it.
- **Do the two live checks in §18.2 and §18.5** — the accessible name and the
  dialog position. They are five minutes with a real store and they are the only
  unverified things this phase shipped.
- **Brand the account pages in the checkout and accounts editor** (§14.3). This
  is where the customer notices the seam between a designed store and an
  undesigned account area, and no amount of theme work will reach it.
- **If the store must stay on legacy accounts**, treat §5.1 as the build brief —
  and note the trade: staying means the theme must ship the seven templates,
  which withholds the upgrade for as long as they are there.
- **The missing templates in §18.8** are their own small phase, and `password` in
  particular matters if the store ever goes behind a password page.

---

**STOP AFTER PHASE 15.**
