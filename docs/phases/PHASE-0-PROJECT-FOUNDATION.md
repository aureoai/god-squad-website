# GOD SQUAD — PHASE 0 PROJECT FOUNDATION

**Project:** God Squad Premium Faith-Driven Streetwear  
**Phase:** 0 — Project Foundation  
**Foundation work carried out:** 2026-09-20  
**This document written:** 2026-09-21  
**Target:** Production-ready Shopify Online Store 2.0 theme  
**Status:** Complete. Phase 1 and Phase 2 are delivered; this record closes the gap left when Phase 0 produced no document of its own.

---

## 0. A note on this document

Phase 0 ran on 2026-09-20 as a read-only inspection of the existing prototype. It produced findings, measurements and an evidence base, but no written deliverable, because no Phase 0 specification was ever issued: the project moved directly from the foundation conversation into the Phase 1 audit specification.

The owner's Phase 3 specification, issued on 2026-09-21, opens by requiring this document, `PHASE-1-WEBSITE-AUDIT.md` and `PHASE-2-DESIGN-SYSTEM.md` to be read first, and instructs that work stop if any is absent. This document was missing, so Phase 3 was halted and this record was written before asset work began. It is written retrospectively, on 2026-09-21, and assembled **from the preserved evidence base rather than from recollection**. Every figure in it was measured from the actual files or the actual render and is reproducible from the artefacts listed in §9. Nothing has been reconstructed from memory, and nothing has been invented to fill a gap; where Phase 0 did not establish something, this document says so.

Two consequences of the retrospective writing should be read with the rest:

- Where a fact has changed since 20 September, the change is stated rather than silently updated. The entry file was renamed by the owner on 20 September at 15:34, and three documents have since been added to the project. Both are recorded in §4 and §10.
- This document does not re-open decisions that Phases 1 and 2 have already settled. It records the ground those phases were built on.

---

## 1. Project identity and objective

**The brand.** God Squad is positioned as faith-driven premium streetwear. The prototype's Our Story paragraph describes it as "a Philippine streetwear brand built on faith, creativity, and community", but Phase 1 marks that origin statement as BUSINESS INFORMATION REQUIRED, so it is recorded here as the prototype's claim rather than as confirmed fact. Its stated personality is premium, faith-driven, editorial, modern, urban, minimal, purposeful, cinematic, community-oriented, confident and authentic. Its brand messages, in the hierarchy later formalised in Phase 2, are *Good People. Higher Purpose.*, *Walk By Faith.*, *Different People. Same Purpose.*, *More Than Clothing.* and *Streetwear With A Purpose.*

**What existed at the start.** A single-page visual prototype exported from Claude Design, together with its runtime and a folder of image assets. It is a homepage only. It has no commerce of any kind.

**The objective.** Transform this approved visual direction into a production-ready Shopify Online Store 2.0 theme, without losing the design that has already been signed off.

**The central tension, identified in Phase 0 and confirmed by Phase 1.** The visual direction is strong and approved; the implementation beneath it is not reusable. The project is therefore a *rebuild against a preserved design*, not a conversion. Everything in the phase plan follows from that distinction.

---

## 2. Scope

### 2.1 In scope for the programme

- A complete Shopify Online Store 2.0 theme: layout, sections, snippets, templates, assets, config and locales.
- Faithful reproduction of the approved visual system in native Shopify architecture.
- The commerce surface the prototype entirely lacks: product pages, collections, cart, search and customer accounts.
- Performance, accessibility and SEO foundations.
- A design system and asset system to support all of the above.

### 2.2 Out of scope, or deferred pending a business decision

- Brand redesign. The visual identity is approved and is preserved, not revisited.
- Product photography and copywriting. The project can specify what is needed; it cannot originate it.
- Merchandising strategy, pricing, catalogue structure and policy content.
- Any third-party Shopify app selection.
- Marketing, email and social operations.

### 2.3 The working rule that governs every phase

Work proceeds only within the phase that the owner has specified and authorised. Each phase is gated: its specification arrives in writing, the work is done, the deliverable is produced, and the programme stops until the next phase is authorised. The rule is visible in the owner's phase specifications from Phase 1 onward, and Phase 2 ends by instructing that Phase 3 not begin without explicit authorisation. Phase 0 operated under it but issued no specification and did not formalise it.

---

## 3. The phase roadmap

| Phase | Name | Status as of 2026-09-21 |
|---|---|---|
| 0 | Project Foundation | Complete. This document. |
| 1 | Website Audit | Complete. `PHASE-1-WEBSITE-AUDIT.md`, 32 sections, 200 issues. |
| 2 | Design System | Complete. `PHASE-2-DESIGN-SYSTEM.md` and `PHASE-2-DESIGN-TOKENS.css`. |
| 3 | Asset Preparation | In progress. Specification issued by the owner on 2026-09-21 and authorised; this document was written first because that specification requires it. |
| 4 | Header & Navigation | Not started. |
| 5 | Hero | Not started. |
| 6 | Collections & Best Sellers | Not started. |
| 7 | Our Story | Not started. |
| 8 | Product & Shopping UX | Not started. |
| 9 | Mobile UX | Not started. |
| 10 | Shopify Theme Conversion | Not started. Retires all three P0 blockers. |
| 11 | Theme Editor | Not started. |
| 12 | Performance | Not started. |
| 13 | SEO | Not started. |
| 14 | Accessibility | Not started. |
| 15 | Ecommerce QA | Not started. |
| 16 | Final Polish | Not started. |

The ordering is dependency-driven rather than cosmetic. The design system precedes every section phase because those phases consume its vocabulary. Asset preparation precedes the hero, collection and story phases because none can be completed against mockup crops. Theme conversion precedes the editor, performance, SEO, accessibility and QA phases because each of those is cheap to do correctly in a native theme and expensive to retrofit twice.

---

## 4. The artefact as found

### 4.1 Location and form

The project lives at `C:\Users\TEST\OneDrive\Documents\GodSquad Website`, inside the owner's personal OneDrive. At the time of the Phase 0 inspection it contained 44 files totalling 17,185,754 bytes. It is not a git repository, has no `package.json`, no build tooling and no project instructions file.

The entry page was exported as `God Squad Website.dc.html` and was **renamed by the owner to `God Squad Website.html` on 2026-09-20 at 15:34**, deliberately and with the content unchanged at 15,632 bytes. The runtime is indifferent to the suffix and continues to boot correctly under the new name, which was verified directly. Specifications written before that time refer to the old name; they mean this file.

### 4.2 What the page actually is

This is the single most consequential finding of Phase 0, and everything downstream depends on understanding it correctly.

The page is not a static website. It is a **Claude Design "dc" document**: a template that requires a JavaScript runtime to become a page at all.

- All visible markup sits inside a custom `<x-dc>` element.
- A `<helmet>` child holds the only `<style>` block and the Google Fonts link.
- A `<script type="text/x-dc" data-dc-script>` holds a JavaScript class, `Component extends DCLogic`, whose `renderVals()` returns the products and brand-value data as object literals. Its single editor property is `currency`, an enum of ₱, $ and € defaulting to ₱.
- The template's loop and conditional constructs are the custom elements `<sc-for list="{{ products }}" as="p">` (three occurrences) and `<sc-if value="{{ p.img }}">` (two), together with the nonstandard `style-hover` attribute on the two calls to action and `data-screen-label` editor metadata on four sections.
- `support.js` (69,150 bytes, 1,911 generated lines) hides `<x-dc>` synchronously, fetches React 18.3.1 and ReactDOM from unpkg with subresource integrity hashes, compiles the template, evaluates the data class with `new Function`, and mounts the result with React.

The practical consequences, all verified:

- **Nothing renders without network access.** The template is hidden the moment the script parses, and it is only revealed by React mounting. If unpkg is unreachable, the entire page stays blank rather than degrading.
- **The document is fetched twice per load**, because the runtime re-fetches its own URL and recompiles from the raw text.
- **Three requests 404 on every load.** Two are the literal strings `{{ p.img }}` and `{{ v.icon }}`, because the browser parses the raw template before the runtime replaces it. The third is `/favicon.ico`, because the document declares no favicon of any kind.
- **The page does boot from a plain `file://` open.** An early assumption to the contrary was wrong and was corrected. Only the self-refresh fetch fails there; the render succeeds.

### 4.3 The delimiter collision

The template uses `{{ }}` for interpolation. These are Liquid's own delimiters. Pasting this markup into a Shopify section would cause Liquid to evaluate `{{ products }}` and `{{ p.name }}` as undefined variables and render empty tiles silently, with no error. This single fact makes a copy-and-adapt migration path unsafe and is the reason the programme is structured as a rebuild.

### 4.4 Presentation layer

| Measure | Value |
|---|---|
| Inline `style` attributes | 77, totalling 6,421 characters |
| Class attributes in the source | 0 |
| Embedded stylesheet | 2,916 bytes |
| `!important` declarations | 55 |
| Editor-generated `data-r` hooks | 25 distinct, across 26 occurrences |
| Media queries | 2, both `max-width`: 900px (26 rules) and 520px (5 rules) |
| Dead rules | 1, targeting a hook no element carries |
| Transitions, animations, keyframes | 0 |
| Reduced-motion support | none |
| `z-index` values in use | 1 and 2 only |

Roughly 69% of the CSS lives in inline attributes. There are no classes to hook, and the responsive behaviour is keyed to attributes that a Shopify theme will not have. This layer cannot be carried across.

### 4.5 Structure and interactivity

The rendered document contains 166 elements. It has no `<header>` and no `<main>`; the navigation is nested inside the hero section and absolutely positioned over it at 901 px and above, becoming `position:relative` and sitting in flow at 900 px and below.

The document carries no metadata at all. `document.title` is empty, `<html>` has no `lang` attribute, and there is no meta description, canonical link, Open Graph or Twitter tag, robots meta, structured data or favicon. There is one `<h1>` and two `<h2>` elements, and no headings within the product grid or the value tiles.

There are nine links, six of which point at `#`. There are **zero `<button>` elements and zero `<form>` elements**. Search, account and cart are bare `<img>` tags that cannot receive focus. The menu control is a `<span>` with an `aria-label` but no role and no handler. The runtime attaches no event handlers of its own, so the page has no interactivity beyond native anchor behaviour and two generated hover rules.

### 4.6 Payload

| Resource | Raw | Gzipped |
|---|---|---|
| React 18.3.1 UMD | 10,751 B | 4,263 B |
| ReactDOM 18.3.1 UMD | 131,835 B | 42,818 B |
| `support.js` | 69,150 B | 19,037 B |
| The HTML document | 15,632 B | 4,081 B |
| **JavaScript executed per load** | **~211 KB** | **~66 KB** |
| Google Fonts, five Latin files | 152,880 B | — |
| Google Fonts CSS | 7,461 B | — |

Babel Standalone is referenced by the runtime but is never loaded by this page. Of the fonts requested, Playfair Display 700 is declared and never used.

The hero is a 1,989,201-byte RGB PNG with no alpha channel, served unchanged at every viewport including a 375-pixel band. No image in the document carries `width`, `height`, `srcset`, `sizes`, `loading` or `decoding`.

---

## 5. The approved visual direction

The design is approved and is the fixed point of the programme. It is preserved as `uploads/GODSQUAD WEBSITE MOCKUP.png` (1024 by 1536, 1,872,888 bytes), which is the master, and as `uploads/God-Squad-Images/00-full-mockup-reference.webp` (the same image re-encoded at 182,250 bytes), which is the reference Phases 1 and 2 cite. Any later phase needing full-quality pixels should take the PNG.

**Palette.** Near black `#0D0C0A`, warm cream `#F3EFE6`, muted gold `#D8C08A`, with secondary neutrals and an olive present in the product swatch data.

**Typography.** Playfair Display for display, Jost for interface and body, Kaushan Script for hand-lettered accents. A tracked-uppercase label convention runs throughout and is a brand signature rather than an accident.

**Composition.** Urban, low-angle, natural-light photography; black and cream garments on location; generous whitespace; asymmetric editorial layouts; thin separators and restrained gold accents; alternating dark and light bands.

**Structure.** Announcement bar, header, hero, New Drop, Our Story, brand values, footer.

### 5.1 Owner decisions recorded during the build

The Claude Design editor history, preserved in three screenshots in `uploads/`, records changes the owner made deliberately. Phase 0 classified these as approved rather than as defects, and later phases have honoured that:

- The hero photograph was replaced with a three-model group image, where the mockup shows a single capped model.
- The announcement-bar globe was changed to gold, then restored and kept gold after a deliberate second request.
- Two placeholder social icons were removed from the footer, leaving Facebook and Instagram, where the mockup shows four networks.

Each remains listed for formal confirmation in the Phase 1 business register, but none is treated as an error to be corrected.

---

## 6. Asset baseline

| Measure | Value |
|---|---|
| Files in the project | 44 (17,185,754 bytes) |
| Image files | 41 |
| Files actually referenced by the page | 17 (2,491,648 bytes, 14.5%) |
| Exact duplicate groups, by md5 | 9, accounting for 11 redundant copies |
| Bytes held in redundant copies | 6,733,692 (39% of the folder) |

**The ceiling that shapes Phase 3 and beyond.** Every product image is a crop of the 1024 by 1536 mockup, between 215 and 235 pixels on its long edge. The Our Story slot is filled by a 650 by 480 crop of the mockup's *hero*, which carries fragments of the mockup headline baked into its pixels. The hero itself is a single AI-generated PNG. Two unreferenced AI-generated icon sheets of 2172 by 724 pixels sit in the folder, from which the individual icon PNGs were cut.

No photographic or product asset in the project is fit for production at its intended display size, and no vector logo in SVG, AI or EPS form has been located anywhere. The wordmark in use, `images/WHITE FONT LOGO.png`, is a 500 by 500 RGBA PNG carrying so much transparent padding that the visible mark renders at only 66 by 50 pixels in the header, roughly half its relative size in the mockup. Layered logo sources were located **outside** the project, on the owner's Desktop, comprising two PSD files and several PNG exports. They were not opened during Phase 0 and their contents remain unverified, so a vector master may yet exist inside them.

This is a sourcing problem, not a processing problem. It is recorded here so that no later phase mistakes optimisation for a solution.

---

## 7. Environment

| Tool | Status |
|---|---|
| Node.js | 22.23.2 |
| npm | 10.9.8 |
| Python | 3.12.10 |
| git | 2.54.0 |
| GitHub CLI | installed |
| Bun | not installed |
| Shopify CLI | **not installed** |
| OneDrive | the project folder sits inside a personal OneDrive and syncs; the client's run state during the inspection was not recorded |

Tool versions were captured by direct query during the Phase 0 inspection; they were not written into the evidence files, so they are reported here from that inspection rather than from a preserved artefact.

The working copy is a single folder inside a personal OneDrive, with no version control and no build step. Phase 1 recorded the absence of a version-controlled working copy as process debt (DEBT-12) and recommended resolving it **before Phase 2 begins**, so that the rebuild would have a history and the prototype a frozen baseline (DEBT-13). Phase 2 was delivered without it, so the recommendation is now overdue rather than pending.

### 7.1 Inspection technique established in Phase 0

Three practical constraints were discovered and are recorded because later phases depend on them:

1. **The page must be served over HTTP to be inspected in the desktop preview pane.** Opened as a local file there, it renders as a static snapshot in which the runtime and images never resolve. A local static server was configured for this purpose in `.claude/launch.json`. That file is audit tooling, not a site file.
2. **Headless Edge cannot lay out narrower than roughly 490 pixels on this machine.** A capture requested at 375 pixels is laid out at about 490 and clipped, which silently misrepresents the phone layout. True phone captures require a wrapper page containing an iframe of the target width, captured and then cropped. Two early captures taken without this technique, `mobile-375.png` and `mobile-375-raw.png`, are clipped layouts of roughly 490 pixels rather than 375. They are retained in the evidence base but marked never to be cited; the valid phone captures are `mobile-375-true.png`, `mobile-390-true.png` and `mobile-430-true.png`.
3. **The preview pane screenshot captures only part of an emulated viewport.** Full-page images come from headless Edge; the pane is used for DOM measurement.

---

## 8. Baseline measurements

Captured across thirteen widths on 2026-09-20.

| Width | Layout | Document height | Notable |
|---|---|---|---|
| 375 | 900px + 520px rules | 4,382 px | 5.4 screens; product tiles 327 px from 235 px sources |
| 390 | 900px + 520px rules | 4,427 px | as above at 342 px |
| 430 | 900px + 520px rules | 4,547 px | as above at 382 px |
| 720 | 900px rules only | ~3,400 px | equals 200% zoom on a 1440 screen |
| 768 | 900px rules only | 3,837 px | two columns; third product orphaned |
| 900 | 900px rules only | 4,151 px | last width before the desktop layout |
| 901 | no query, base rules | ~2,400 px | navigation links reappear |
| 920 | no query, base rules | ~2,400 px | product names and the button wrap |
| 1024 | no query, base rules | ~2,400 px | one product name wraps; price misaligns |
| 1280 / 1366 | no query, base rules | — | first screen is hero only; no product visible |
| 1440 | no query, base rules | 2,055 px | reference composition |
| 1920 | no query, base rules | — | 1440 px box with 240 px dark gutters each side |

**Structural defects found at baseline.** At 900 pixels and below the hero's fade overlay is anchored to the section while the photograph sits below the 88-pixel in-flow navigation, so the gradient reaches solid black 88 pixels above the image's lower edge, producing a black band and a hard seam at every width in that band.

At 900 pixels and below the five navigation links are set to `display:none`. The navigation bar itself remains, 88 pixels tall, carrying the logo and a 22 by 16 pixel hamburger `<span>` that has an `aria-label` but no role, no tabindex and no handler, so no menu can be opened and those five destinations are unreachable.

At 1024 to 1440 pixels, where the links are visible, three of the five sit on the bright sky between the models. Pixel-sampled medians are 5.7:1 for Collections, 4.7:1 for Our Story and 4.6:1 for Verse, falling to 5.0, 4.4 and 4.2:1 over the brightest tenth of the backdrop and to 2.4 to 2.5:1 over the brightest fiftieth. A second method used in Phase 1, compositing the fade alphas over sampled photo luminance, puts the same three links at 2.4 to 2.9:1. Either way the worst case is well below the 4.5:1 threshold, and the risk is real because a link's legibility depends on which pixels fall behind it.

No horizontal overflow was found at any width, although the wrapper's `overflow:hidden` masks anything that would extend past it.

---

## 9. Evidence base and method

Phase 0 was read-only throughout. The evidence it produced is preserved and was the input to both later phases:

- A recursive file inventory with md5 hashes, dimensions, byte sizes and usage verified from the source rather than inferred from filenames.
- A runtime analysis of `support.js` covering the boot sequence, the template compiler, the data evaluation path and the editor bridge.
- Live DOM measurements at thirteen viewport widths, with full-page captures at ten of them. The 1280, 1366 and 1920 widths were captured first-screen only, which is why §8 records no document height for them.
- Network, console, font and bundle measurements taken against the served page.
- Pixel-sampled contrast measurement of the navigation against the hero photograph.
- A three-lens inspection of fidelity, responsive behaviour and technical quality, in which fifty findings were each put to three independent sceptics: forty-eight were confirmed and two of the lead's own claims were refuted and corrected. A completeness critic then added eight further findings, which did not themselves go through the sceptic rounds.

Two corrections made during Phase 0 are recorded because they matter to anyone reading the earlier conversation: the prototype's call-to-action hover styles **do** work, contrary to a first assessment, because the runtime compiles them into generated `:hover` rules; and the page **does** boot from a plain file open.

---

## 10. Changes to the project during and since the Phase 0 inspection

| Date | Change | By |
|---|---|---|
| 2026-09-20 13:23 | `.claude/launch.json` added, 228 bytes, local dev-server configuration | Audit tooling |
| 2026-09-20 15:34 | Entry page renamed from `God Squad Website.dc.html` to `God Squad Website.html`, content unchanged | Owner, deliberate |
| 2026-09-21 | `PHASE-1-WEBSITE-AUDIT.md` added | Phase 1 deliverable |
| 2026-09-21 | `PHASE-2-DESIGN-SYSTEM.md` and `PHASE-2-DESIGN-TOKENS.css` added | Phase 2 deliverables |
| 2026-09-21 | This document added | Phase 0 deliverable, written retrospectively |

**No original project file has been edited or deleted at any point.** All 44 original files remain byte-identical, checked by md5 against the Phase 0 inventory after each document was written. Two changes to the tree did occur and are listed above: the owner renamed the entry page, which altered its filename but not its contents, and four new files were added alongside the originals.

---

## 11. Constraints and standing rules

1. **The visual direction is approved and preserved.** Branding, imagery, typography and content structure are not revisited.
2. **Phases are gated.** No phase begins without its written specification and the owner's authorisation.
3. **Inspect and document before changing anything.** Every phase begins by verifying the ground it stands on rather than trusting the previous report alone.
4. **Business facts are never invented.** Anything unknown is marked as requiring business information and is escalated, not guessed.
5. **Original assets are preserved.** Optimised copies are additions; originals are never overwritten, renamed or destructively processed.
6. **The prototype is the design baseline, not the codebase.** It is read for intent; it is not the thing being edited.

---

## 12. Known unknowns carried forward

Phase 0 deliberately did not resolve these, and later phases have carried them as an open register rather than filling them in:

- The entire commercial layer: catalogue, pricing, currency and markets, collection structure, variants and inventory.
- Every navigation destination, including what "Verse" is intended to be.
- Shipping scope behind the worldwide shipping claim, and all policy and legal text.
- Which social channels are live.
- A vector logo, and original photography for the hero, story and products.
- The Shopify store itself: whether one exists, its plan, domain and administrator.
- Browser and device support targets, and confirmation of the mobile type floor.

Phase 1 consolidated these into thirty decisions in its Appendix A and itself identified the four that gate the design system: confirmation of the extended palette beyond the three primaries; whether the 9 to 13 pixel tracked labels are brand-mandated on phones; the browser and device support matrix; and the intended behaviour above 1440 pixels. They remain the programme's largest external dependency.

---

## 13. Phase 0 exit criteria

- [x] Project identity, positioning and objective established, with the brand-origin claim flagged as unconfirmed.
- [x] Phase 0 had no written specification and therefore no contemporaneous exit criteria; the list below is reconstructed from what the phase actually produced.
- [ ] Scope and exclusions drafted from the foundation conversation, but not formally confirmed by the owner.
- [x] Phase roadmap defined and gating rule established.
- [x] The artefact understood at the architectural level, including the runtime, the data layer and the Liquid delimiter collision.
- [x] Presentation layer measured and its reusability assessed.
- [x] Asset baseline inventoried with hashes, and the resolution ceiling identified.
- [x] Approved visual direction recorded, including the owner's deliberate deviations from the mockup.
- [x] Environment and tooling confirmed, and a reliable inspection technique established.
- [x] Baseline measurements captured across thirteen widths.
- [x] Evidence base preserved and independently verified.
- [x] Known unknowns registered rather than guessed.
- [x] No project file modified.

**Handoff to Phase 1.** The audit took this foundation as its input and produced a 200-issue technical blueprint, confirming the central Phase 0 judgement: the visual system is worth preserving in full, and the implementation beneath it must be rebuilt natively rather than converted.
