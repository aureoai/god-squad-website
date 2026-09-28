# Live DOM measurements per viewport (browser pane, page served over HTTP, 2026-09-20)

All values are CSS px unless noted. "fade offset" = hero-fade top vs hero-img top; below 900px the fade is anchored to the section, the image sits below the 88px in-flow nav, so the fade ends 88px above the image bottom (black band + hard edge).

| width | layout | docH | overflow | nav links | hamburger | hero cols | hero img | fade top / img top | h1 | h1 lines | product cols | product img (natural 235) | values cols | story img | announce pad-left | footer |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 375 (DPR2) | mobile rules | 4382 | none | hidden | shown 22x16 | 1 | 375x320 | 59 / 147 (88 off) | 56px, 327x99 | 2 | 1 | 327x327 (2.8x device upscale) | 1 | 375x280 | 16px | column |
| 390 | mobile rules | 4427 | none | hidden | shown 22x16 | 1 | 390x320 | 59 / 147 (88 off) | 56px, 342x99 | 2 | 1 | 342x342 | 1 | 390x280 | 16px | column |
| 430 | mobile rules | 4547 | none | hidden | shown 22x16 | 1 | 430x320 | 59 / 147 (88 off) | 56px, 382x99 | 2 | 1 | 382x382 | 1 | 430x280 | 16px | column |
| 720 (=200% zoom of 1440) | mobile rules | ~3400 | none | hidden | shown | 1 | 720x446 | 88 off | one line | 1 | 2 (cap orphaned) | ~340 | 2 | on top | 48px | column |
| 768 | mobile rules | 3837 | none | hidden | shown 22x16 | 1 | 753x476 | 41 / 129 (88 off) | 65px one line | 1 | 2 (342.5 each; cap alone on row 2) | 343x343 | 2 (376.5 each; stray right rule at viewport edge) | 753x461 | 48px (dead [data-r=pad] rule) | column, 164px tall although both groups fit one row |
| 900 (boundary, mobile rules apply at <=900) | mobile rules | 4151 | none | hidden | shown 22x16 | 1 | 885x558 | 41 / 129 (88 off) | 76.5px, 837x67 | 1 | 2 | 409x409 (1.74x) | 2 | 885x540 | 48px | column |
| 901 (desktop rules) | desktop | ~2400 | none | shown | hidden | 3 | absolute cover | n/a | ~76px | 3 (WALK/BY/FAITH.) | 3 | ~230 | 4 | absolute 70% | 48px | row |
| 920 | desktop | ~2400 | none | shown | hidden | 3 | cover | n/a | 78px | 3 | 3 (names wrap, View All wraps to 2 lines) | ~235 | 4 | 70% | 48px | row |
| 1024 | desktop | ~2400 | none | shown | hidden | 3 | cover | n/a | 87px | 3 | 3 ("Signature Oversized Tee" wraps, price misaligned) | ~250 | 4 | 70% | 48px | row |
| 1280x720 / 1366x768 | desktop | - | none | shown | hidden | 3 | cover | n/a | ~109/112px | 3 | fold falls inside the hero; no product visible on first screen | - | 4 | - | 48px | row |
| 1440 | desktop | 2055 | none | shown | hidden | 3 | 1425x719 (0.85x of 1672) | n/a | 112px | 3 | 3 | 288x288 (1.23x; cap 289 from 215 = 1.34x) | 4 | 998x520 (1.53x of 650) | 48px | row |
| 1920 | desktop, 1440 max-width wrapper | - | none | shown | hidden | 3 | 1440 wide box, dark gutters 240px each side | n/a | 112px (clamp cap) | 3 | 3 | 288 | 4 | - | 48px | row |

Other per-width facts
- DOM element count after render: 166 elements at every width (tiny DOM).
- Tap targets are identical at every phone width: hamburger 22x16, search/account/cart 24x24, social links 28x28, View All Products 242x50, Our Story CTA 169x50.
- Announcement bar: 48px side padding on desktop and at 521-900 (the 900px rule targets [data-r=pad], which no element carries); 16px and stacked to two centred lines at <=520.
- The 520px query switches products and values to one column and the announcement bar to a column; between 521 and 900 products and values are two columns.
- h1 sizing: clamp(56px, 8.5vw, 112px); it hits 56px at <=659px and 112px at >=1318px. The three-line stack at desktop comes from the hero copy column being ~1.1fr of 2.9fr minus 96px padding (about 450px at 1440) with text-wrap:balance; the mockup lockup is two lines.
- Focus order at 1440 (DOM order): Home, Shop, Collections, Our Story, Verse, View All Products, Our Story CTA, Facebook, Instagram. No skip link, no custom focus style, hamburger/search/account/cart not focusable.

Render files (scratchpad/shots): mobile-375-true.png, mobile-390-true.png, mobile-430-true.png (true phone layouts via iframe wrapper); zoom200-720.png; tablet-768.png; breakpoint-900.png; breakpoint-901.png; band-920.png; laptop-1024.png; laptop-1280-fold.png; laptop-1366-fold.png; desktop-1440.png; wide-1920-fold.png. IGNORE mobile-375.png and mobile-375-raw.png (clipped ~490px layouts).

External bundle sizes (downloaded): react 18.3.1 UMD 10,751 B (4,263 gz); react-dom 18.3.1 UMD 131,835 B (42,818 gz); support.js 69,150 B (19,037 gz); HTML 15,632 B (4,081 gz). @babel/standalone 3,137,752 B (653,872 gz) is referenced by the runtime but only loaded if an x-import of JSX is used, which this page does not do. JS actually executed per load: about 211 KB raw / 66 KB gz, all render-blocking in effect because the template is hidden until React mounts.

Inventory summary (inventory.tsv): 44 files, 17,185,754 bytes. Referenced by the HTML: 15 images + support.js (16 files) + the HTML itself = 17 files, 2,491,648 bytes. 9 md5 duplicate groups (DUP-01 hero-group x3, DUP-03 icons-sprite x3, seven pairs) = 11 redundant copies. NOTE: .thumbnail, images/hero-model.webp, images/logo.png and images/our-story.webp are NOT referenced by the HTML (the "README" tag in the inventory is a loose name match only). The sprites are referenced by nothing.
