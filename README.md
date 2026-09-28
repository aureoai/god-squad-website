# GOD SQUAD — Shopify theme

A faith-driven Philippine streetwear brand. This project converts an approved
design into a production Shopify Online Store 2.0 theme.

**Status:** code-complete and internally coherent. **Not launchable yet** — the
theme has never been on a Shopify store, and the merchant content it needs does
not exist. See [What's left](#whats-left).

---

## Look at the design

**Open `preview-site/index.html`.** Double-click it. Nothing to install, nothing
to start.

It is the whole site as ordinary files — click a product card and you get the
product page, click the cart and you get the cart. A bar along the bottom jumps
to every state: filters, empty cart, no-results search, sold-out product, 404.
Click *hide* on the bar for a clean look.

**What is real:** every page is the theme's own Liquid, rendered, with the
theme's own CSS and JavaScript. Layout, typography, colour, spacing, responsive
behaviour, the cart drawer, the filter drawer, the variant picker and focus
order are all the real thing. Resize the window — the interesting boundary is
768px.

**What is not:** the routing, and the data. Shopify decides which product a URL
resolves to; the preview maps each link to whichever fixture best demonstrates
that kind of product, so the price on a card may not match the page it opens.
Every product, price and photograph is invented test data.

**What will fail:** add to cart, quantity changes, search, filtering, checkout.
They need Shopify, which is not here. *Watch how they fail* — a readable message
and no stuck spinner is what is being tested.

To rebuild the preview after changing the theme:

```bash
cd qa && python build-preview.py
```

---

## Check the theme

```bash
cd qa && python check-all.py
```

Runs all 32 automated suites plus Theme Check and prints one verdict. Rebuilds
the test fixtures from the theme first, so you are never testing stale output.
Takes about a minute.

**Current: 32 passed, 0 failed.** Theme Check reports 2 offences, both business
information rather than code — see below.

Useful flags: `--fast` skips the browser suites (~30s), `--list` prints the
inventory of what runs.

If Theme Check says it is not installed, run `npm install` inside `qa/` once.

---

## What is where

| | |
|---|---|
| `god-squad-theme/` | **The deliverable.** 75 files. This is what gets uploaded to Shopify. |
| `preview-site/` | The browsable design preview. Generated — safe to delete, rebuild with `qa/build-preview.py`. |
| `qa/` | The test suite: 32 suites, the Mini-Liquid harness, `check-all.py`. Generated fixtures under `qa/phase*/site/` rebuild on demand. |
| `docs/` | `GODSQUAD-THEME-REFERENCE-MANUAL.md` — the consolidated reference, and the one to read first. `PRE-INTEGRATION-DESIGN-REVIEW.md` alongside it. |
| `docs/phases/` | The 20 original phase documents, unchanged. The manual folds them together, but they remain the authority on detail. |
| `brand-assets/` | Source images, the Phase 3 asset set, the approved mockups. |
| `prototype/` | The original Claude Design export. **Read-only archive** — nothing is built from it, and a test asserts its files are unmodified. |

---

## What's left

None of this is a development task.

**Before the Shopify integration:**

1. **Merchant photography.** The theme ships zero images and none exists. The
   preview uses low-resolution prototype crops that are AI-generated with
   unconfirmed rights. This is the single biggest gap — and every measurement in
   this project was taken against invented fixture data, which has already
   hidden one live defect that only appeared with realistic product names.
2. **A vector logo master and a favicon.** The current wordmark carries heavy
   transparent padding and renders at roughly half its intended size.
3. **`theme_support_email` and `theme_documentation_url`** in
   `god-squad-theme/config/settings_schema.json` — the only two Theme Check
   offences outstanding.
4. **Collections named `new-drop` and `best-sellers`.** The homepage's two
   product bands point at those handles; until the collections exist, neither
   band renders.
5. **Version control.** There is no git repository. Nineteen phases of work with
   no history beyond OneDrive's file versioning.

**Then:** section 10 of the reference manual is the nine-stage store-setup
runbook — upload, brand settings, navigation, pages, catalogue, the Search &
Discovery app, payments, and the five things only a live store can verify.

**Five decisions are open** and listed at the end of the design review: the
"Add to bag" versus "cart" wording, the mobile menu's type, the footer's two
link systems, the "Worldwide Shipping" claim, and the announcement-bar icon.
