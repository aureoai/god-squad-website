# PHASE 19 — SHOPIFY INTEGRATION REPORT

**Date:** 2026-09-28
**Verdict:** **PHASE 19 STATUS: BLOCKED**

Blocked on one thing: **there is no Shopify store access.** Shopify CLI 4.8.2 is installed, but there is no authenticated session, no store URL and no credentials, and obtaining them is the owner's action. Roughly half of Phase 19's 44 steps require a live store — a real product, a real collection, a checkout, a Theme Editor, a served storefront. None of that is reachable from here, and this report does not pretend otherwise.

The offline half is done, and the theme is in better shape than when the phase started: **35/35 QA suites pass and Theme Check reports 0 offences** — the first clean Theme Check in the project's history.

---

## 1. Shopify architecture

Online Store 2.0. JSON templates, two section groups, `{% schema %}` with blocks and presets throughout, no build step, no dependencies. Full inventory in [PHASE-19-SHOPIFY-BASELINE.md](PHASE-19-SHOPIFY-BASELINE.md).

## 2. Theme architecture

107 files across 7 directories, ~500 KB packaged. Two layouts (`theme.liquid`, and `password.liquid` added here). Commerce markup is shared through snippets rather than duplicated.

## 3. Files created

| File | Why |
|---|---|
| `layout/password.liquid` | **P0 fix.** The password gate had no layout of its own. |
| `qa/make-theme-zip.py` | Packages the theme for upload with the folders at the archive root, and validates before writing. |
| `docs/phases/PHASE-19-SHOPIFY-BASELINE.md` | STEP 02. |
| `docs/phases/PHASE-19-SHOPIFY-INTEGRATION-REPORT.md` | STEP 43. |

## 4. Files modified

| File | Change |
|---|---|
| `templates/gift_card.liquid` | **P0 ×2** — added `{% layout none %}`; rebuilt the QR. |
| `templates/password.json` | **P0** — declared `"layout": "password"`. |
| `assets/section-main-password.css` | Split an ungated hover; fixed two undefined tokens. |
| `snippets/image-fallback.liquid` | Made `width`/`height` unconditional. |
| `qa/phase8/validate.py` | Scan `templates/` too. |
| `qa/phase16/refs.py` | See asset names passed as parameters and in lists. |
| `qa/phase9/settings.py` | Re-point two logo assertions at the new design. |

## 5. Files removed

None.

## 6–11. Integration status

| Area | Offline | Blocked on store |
|---|---|---|
| **Products** | Every field is a Shopify object; no hardcoded product fact anywhere. Inventory published as a boolean, never a count. | Real products; variant behaviour against real inventory. |
| **Collections** | `index.json` pins `new-drop` / `best-sellers`; a missing handle renders nothing. | Do those collections exist? Real titles, images, counts. |
| **Cart** | Ajax `/cart/add.js`, `/cart/change.js`, `/cart/update.js`; count from `cart.item_count`; drawer and page share four snippets. | Add, update, remove against a real cart. |
| **Checkout** | `{{ form | payment_button }}` is Shopify's own, unwrapped. | **The entire purchase flow.** Whether the button renders at all is a store payment setting. |
| **Search** | Shopify `search` object. | Real results; filters need the Search & Discovery app. |
| **Accounts** | `templates/customers/*` correctly absent; `<shopify-account>` gated on `shop.customer_accounts_enabled`; 52/52 pass. | Which account system the store uses. |

## 12. Verse integration

Three homepage sections. All three declare no `enabled_on`, so they are already addable to any template — a `/pages/verse` route needs a template plus a page at handle `verse`, not Liquid changes.

**Not built:** the `/pages/verse` route; the categories HOPE, LOVE, STRENGTH; the strings "THE VERSE", "WORDS TO LIVE BY.", "INSPIRED COLLECTION". Most of that is Theme Editor data entry. "INSPIRED COLLECTION" would be a new section. **Owner decision — see §20.**

## 13. Analytics

None, and none is possible from a theme: Shopify standard events moved to Custom Pixels in admin. 31 tracking checks clean, 12/12 seeded violations caught. `content_for_header` unmodified.

## 14. SEO

Title, meta description, canonical, Open Graph and Twitter cards present. Product structured data via Shopify's own `{{ product | structured_data }}` — the theme's only `ld+json`. **No Organization, WebSite/SearchAction or BreadcrumbList.** Whether STEP 29 wants those is an owner decision.

## 15. Accessibility

Landmarks, heading order, focus management, target sizes, contrast and reduced motion are asserted across the harness. Fixed this phase: the password input's text colour resolved to an **undefined token**, so the declaration was dropped and typed characters fell back to dark-on-dark — **you could not read your own password.** Its border now uses the interactive token measured for SC 1.4.11, and the hover/focus rule was split so gating the hover no longer takes the focus state with it.

## 16. Performance

~24 KB JavaScript gzipped, no dependencies. Fixed: the gift card loaded Shopify's QR generator through `script_tag`, which is parser-blocking.

**Outstanding:** the bundled hero is a single-candidate 120 KB image on the LCP element, served by `asset_url` with no resizing or format negotiation. A merchant upload goes through Shopify's image pipeline; the fallback does not.

## 17. Theme Check results

**0 offences.** Previously 2 long-standing (`theme_support_email`, `theme_documentation_url`) plus 3 introduced today. Cleared:

- `UnknownFilter` — `qr_code_svg` does not exist
- `ParserBlockingScript` — `script_tag` in the gift card head
- `ImgWidthAndHeight` — dimensions emitted inside an `{% if %}`
- `LiquidHTMLSyntaxError` — a Liquid comment placed inside an `<img>` tag's attribute list (mine, caught and fixed in the same pass)

## 18. Browser testing

**BLOCKED.** No served storefront. The offline harness renders the real Liquid at nine widths, but that is not browser QA of a live store.

## 19. E-commerce testing

**BLOCKED.** No checkout, no Buy It Now, no real variants.

## 20. Remaining issues

### P0 — fixed this phase

1. **`gift_card.liquid` had no `{% layout none %}`.** It emits a full `<!doctype html>` document; without the directive Shopify wraps it in `theme.liquid`, so the customer got two nested HTML documents, two `content_for_header`, and the storefront header, nav, cart drawer and footer around a printable gift card.
2. **The QR code did not exist.** `gift_card.qr_identifier_url | qr_code_svg` — neither the property nor the filter is real. Rebuilt with `gift_card.qr_identifier` and Shopify's own `vendor/qrcode.js`, deferred, initialised on `DOMContentLoaded`.
3. **`password.json` declared no layout**, so the password gate rendered inside the full storefront — the header, nav, search, account, cart controls, drawer and footer, listing every destination behind the lock to someone who had not authenticated.

### Blocking, and yours

| # | Item | Action |
|---|---|---|
| 1 | **`shopify-upload/products.csv` is fabricated** | **Do not import.** 5 products, 17 variants, invented prices, stock and SKUs — and compare-at prices that manufacture a discount from a price never charged, which is an advertising-compliance problem, not just fake data. Replace with your real catalogue. |
| 2 | **Store access** | An authenticated CLI session or admin login. Everything in §18–19 waits on this. |
| 3 | **`new-drop` / `best-sellers`** | Create them, or re-point the two homepage bands. Otherwise both render nothing. |
| 4 | **"Worldwide Shipping"** | Supply a shipping policy and rates, or remove it from `header-group.json:17` and `footer-group.json:47`. Your own theme refuses this claim elsewhere for exactly this reason. |

### Owner decisions

| # | Decision |
|---|---|
| 1 | **The six bundled images** — keep (an unconfigured store looks finished) or remove (230 KB per upload, and the hero bypasses Shopify's image pipeline on the LCP element)? |
| 2 | **The logo fallback** — the bundled `logo.png` now stands in where Phase 9 used a text wordmark and Phase 11 rendered nothing. Both reversals are defensible; both were recorded decisions. |
| 3 | **COLLECTIONS nav (STEP 05)** — build `list-collections.json`, re-point at `/collections/all`, or leave it out? |
| 4 | **`/pages/verse` (STEP 16)** — should it exist, and do the homepage bands stay as a teaser? |
| 5 | **Verse content** — HOPE, LOVE, STRENGTH, "THE VERSE", "WORDS TO LIVE BY.", "INSPIRED COLLECTION". |
| 6 | **Structured data scope (STEP 29)** — site-level Organization / WebSite / BreadcrumbList? |
| 7 | **Version control** — there is no git repository. Today's changes could not be diffed, only read. |

### Spec conflicts worth naming

- **STEP 12** reads as "remove the duplicate View cart control". They are **mutually exclusive at runtime** — `cart.js:650-667` opens the drawer *or* calls `showFormSuccess`, never both, and the product-page region ships `hidden`. Nothing was removed.
- **STEP 14** cannot mean order history or an address book: legacy customer account Liquid is deprecated and `templates/customers/*` must stay absent.
- **STEP 05** wants a COLLECTIONS nav item; the route has no template.
- **STEP 22** lists a newsletter; Phase 1 §29.7 recorded it ADD LATER and it is still out.

---

## PHASE 19 STATUS: BLOCKED

**The single blocking issue:** no Shopify store access. Every other item above is either fixed, or a decision waiting on you.

**Recommended fix, in order:**

1. Replace `shopify-upload/products.csv` with the real catalogue, or delete it.
2. `python qa/make-theme-zip.py` → Online Store → **Draft themes** → Import theme. It uploads unpublished.
3. Create `new-drop` and `best-sellers`; add products.
4. Upload images to Content → Files; select them in the Theme Editor.
5. Report what breaks. The store-dependent half of Phase 19 runs then.
