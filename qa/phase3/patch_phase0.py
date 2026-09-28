# -*- coding: utf-8 -*-
"""Apply the verification findings to PHASE-0-PROJECT-FOUNDATION.md.

Three findings are rejected with reasons: the verifiers could read only the
project files, so they concluded the Phase 3 specification did not exist. It was
issued by the owner on 2026-09-21 and its section 1 does require this document.
The corrections below make that traceable instead of asserted.
"""
import io, sys, os, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
DOC = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\PHASE-0-PROJECT-FOUNDATION.md"
t = open(DOC, encoding='utf-8').read()

EDITS = [
 # ---- §0 mandate: make the precondition traceable rather than asserted
 ("Phase 3 requires this document to exist before asset work may begin. It is therefore written retrospectively, on 2026-09-21, and it is assembled **from the preserved evidence base rather than from recollection**.",
  "The owner's Phase 3 specification, issued on 2026-09-21, opens by requiring this document, `PHASE-1-WEBSITE-AUDIT.md` and `PHASE-2-DESIGN-SYSTEM.md` to be read first, and instructs that work stop if any is absent. This document was missing, so Phase 3 was halted and this record was written before asset work began. It is written retrospectively, on 2026-09-21, and assembled **from the preserved evidence base rather than from recollection**."),

 # ---- §1 brand origin is unconfirmed
 ("**The brand.** God Squad is a Philippine streetwear label positioned as faith-driven premium streetwear.",
  "**The brand.** God Squad is positioned as faith-driven premium streetwear. The prototype's Our Story paragraph describes it as \"a Philippine streetwear brand built on faith, creativity, and community\", but Phase 1 marks that origin statement as BUSINESS INFORMATION REQUIRED, so it is recorded here as the prototype's claim rather than as confirmed fact."),

 # ---- §2.3 standing rule attribution
 ("Phase 0 established this rule and every subsequent phase has followed it.",
  "The rule is visible in the owner's phase specifications from Phase 1 onward, and Phase 2 ends by instructing that Phase 3 not begin without explicit authorisation. Phase 0 operated under it but issued no specification and did not formalise it."),

 # ---- §3 roadmap row for Phase 3
 ("| 3 | Asset Preparation | Specified; awaiting this document as its precondition. |",
  "| 3 | Asset Preparation | In progress. Specification issued by the owner on 2026-09-21 and authorised; this document was written first because that specification requires it. |"),

 # ---- §4.2 template constructs and the editor property
 ("- A `<script type=\"text/x-dc\" data-dc-script>` holds a JavaScript class, `Component extends DCLogic`, whose `renderVals()` returns the products and brand-value data as object literals, plus a single editor property for currency.",
  "- A `<script type=\"text/x-dc\" data-dc-script>` holds a JavaScript class, `Component extends DCLogic`, whose `renderVals()` returns the products and brand-value data as object literals. Its single editor property is `currency`, an enum of ₱, $ and € defaulting to ₱.\n- The template's loop and conditional constructs are the custom elements `<sc-for list=\"{{ products }}\" as=\"p\">` (three occurrences) and `<sc-if value=\"{{ p.img }}\">` (two), together with the nonstandard `style-hover` attribute on the two calls to action and `data-screen-label` editor metadata on four sections."),

 # ---- §4.2 three 404s
 ("- **Two requests 404 on every load**, for the literal strings `{{ p.img }}` and `{{ v.icon }}`, because the browser parses the raw template before the runtime replaces it.",
  "- **Three requests 404 on every load.** Two are the literal strings `{{ p.img }}` and `{{ v.icon }}`, because the browser parses the raw template before the runtime replaces it. The third is `/favicon.ico`, because the document declares no favicon of any kind."),

 # ---- §4.5 nav positioning + metadata absence
 ("The rendered document contains 166 elements. It has no `<header>` and no `<main>`; the navigation is nested inside the hero section and absolutely positioned over it.",
  "The rendered document contains 166 elements. It has no `<header>` and no `<main>`; the navigation is nested inside the hero section and absolutely positioned over it at 901 px and above, becoming `position:relative` and sitting in flow at 900 px and below.\n\nThe document carries no metadata at all. `document.title` is empty, `<html>` has no `lang` attribute, and there is no meta description, canonical link, Open Graph or Twitter tag, robots meta, structured data or favicon."),

 # ---- §5 mockup master
 ("It is preserved in `uploads/God-Squad-Images/00-full-mockup-reference.webp`, a 1024 by 1536 master mockup.",
  "It is preserved as `uploads/GODSQUAD WEBSITE MOCKUP.png` (1024 by 1536, 1,872,888 bytes), which is the master, and as `uploads/God-Squad-Images/00-full-mockup-reference.webp` (the same image re-encoded at 182,250 bytes), which is the reference Phases 1 and 2 cite. Any later phase needing full-quality pixels should take the PNG."),

 # ---- §6 vector logo claim + logo padding fact
 ("No asset in the project is fit for production at its intended display size, and no vector logo exists anywhere. Layered logo sources were located **outside** the project, on the owner's Desktop, comprising two PSD files and several PNG exports. They were not opened during Phase 0 and their contents remain unverified.",
  "No photographic or product asset in the project is fit for production at its intended display size, and no vector logo in SVG, AI or EPS form has been located anywhere. The wordmark in use, `images/WHITE FONT LOGO.png`, is a 500 by 500 RGBA PNG carrying so much transparent padding that the visible mark renders at only 66 by 50 pixels in the header, roughly half its relative size in the mockup. Layered logo sources were located **outside** the project, on the owner's Desktop, comprising two PSD files and several PNG exports. They were not opened during Phase 0 and their contents remain unverified, so a vector master may yet exist inside them."),

 # ---- §7 environment provenance + OneDrive
 ("| OneDrive client | installed but not running during the inspection |",
  "| OneDrive | the project folder sits inside a personal OneDrive and syncs; the client's run state during the inspection was not recorded |"),

 ("The working copy is a single folder inside a personal OneDrive, with no version control and no build step. Phase 1 recorded the absence of version control as process debt and recommended resolving it before implementation begins.",
  "Tool versions were captured by direct query during the Phase 0 inspection; they were not written into the evidence files, so they are reported here from that inspection rather than from a preserved artefact.\n\nThe working copy is a single folder inside a personal OneDrive, with no version control and no build step. Phase 1 recorded the absence of a version-controlled working copy as process debt (DEBT-12) and recommended resolving it **before Phase 2 begins**, so that the rebuild would have a history and the prototype a frozen baseline (DEBT-13). Phase 2 was delivered without it, so the recommendation is now overdue rather than pending."),

 # ---- §7.1 captures retained
 ("An early mobile capture that did not use this technique was wrong and was discarded.",
  "Two early captures taken without this technique, `mobile-375.png` and `mobile-375-raw.png`, are clipped layouts of roughly 490 pixels rather than 375. They are retained in the evidence base but marked never to be cited; the valid phone captures are `mobile-375-true.png`, `mobile-390-true.png` and `mobile-430-true.png`."),

 # ---- §8 breakpoint labels
 ("| 375 | phone rules | 4,382 px | 5.4 screens; product tiles 327 px from 235 px sources |\n| 390 | phone rules | 4,427 px | as above at 342 px |\n| 430 | phone rules | 4,547 px | as above at 382 px |\n| 720 | phone rules | ~3,400 px | equals 200% zoom on a 1440 screen |\n| 768 | tablet rules | 3,837 px | two columns; third product orphaned |\n| 900 | tablet rules | 4,151 px | last width before the desktop layout |",
  "| 375 | 900px + 520px rules | 4,382 px | 5.4 screens; product tiles 327 px from 235 px sources |\n| 390 | 900px + 520px rules | 4,427 px | as above at 342 px |\n| 430 | 900px + 520px rules | 4,547 px | as above at 382 px |\n| 720 | 900px rules only | ~3,400 px | equals 200% zoom on a 1440 screen |\n| 768 | 900px rules only | 3,837 px | two columns; third product orphaned |\n| 900 | 900px rules only | 4,151 px | last width before the desktop layout |"),
 ("| 901 | desktop | ~2,400 px | navigation reappears |", "| 901 | no query, base rules | ~2,400 px | navigation links reappear |"),
 ("| 920 | desktop | ~2,400 px |", "| 920 | no query, base rules | ~2,400 px |"),
 ("| 1024 | desktop | ~2,400 px |", "| 1024 | no query, base rules | ~2,400 px |"),
 ("| 1280 / 1366 | desktop | — |", "| 1280 / 1366 | no query, base rules | — |"),
 ("| 1440 | desktop | 2,055 px |", "| 1440 | no query, base rules | 2,055 px |"),
 ("| 1920 | desktop | — |", "| 1920 | no query, base rules | — |"),

 # ---- §8 defects paragraph: nav, contrast
 ("**Structural defects found at baseline.** Below 900 pixels the hero's fade overlay is anchored to the section while the photograph sits below the 88-pixel in-flow navigation, so the gradient reaches solid black 88 pixels above the image's lower edge, producing a black band and a hard seam at every phone and tablet width. Below 900 pixels there is no navigation at all. Three of the five navigation links measure between 2.4:1 and 2.9:1 against the bright sky behind them, below the 4.5:1 threshold. No horizontal overflow was found at any width, although the wrapper's `overflow:hidden` masks anything that would extend past it.",
  "**Structural defects found at baseline.** At 900 pixels and below the hero's fade overlay is anchored to the section while the photograph sits below the 88-pixel in-flow navigation, so the gradient reaches solid black 88 pixels above the image's lower edge, producing a black band and a hard seam at every width in that band.\n\nAt 900 pixels and below the five navigation links are set to `display:none`. The navigation bar itself remains, 88 pixels tall, carrying the logo and a 22 by 16 pixel hamburger `<span>` that has an `aria-label` but no role, no tabindex and no handler, so no menu can be opened and those five destinations are unreachable.\n\nAt 1024 to 1440 pixels, where the links are visible, three of the five sit on the bright sky between the models. Pixel-sampled medians are 5.7:1 for Collections, 4.7:1 for Our Story and 4.6:1 for Verse, falling to 5.0, 4.4 and 4.2:1 over the brightest tenth of the backdrop and to 2.4 to 2.5:1 over the brightest fiftieth. A second method used in Phase 1, compositing the fade alphas over sampled photo luminance, puts the same three links at 2.4 to 2.9:1. Either way the worst case is well below the 4.5:1 threshold, and the risk is real because a link's legibility depends on which pixels fall behind it.\n\nNo horizontal overflow was found at any width, although the wrapper's `overflow:hidden` masks anything that would extend past it."),

 # ---- §9 capture scope + sceptic scope
 ("- Live DOM measurements at thirteen viewport widths, with full-page captures at each.",
  "- Live DOM measurements at thirteen viewport widths, with full-page captures at ten of them. The 1280, 1366 and 1920 widths were captured first-screen only, which is why §8 records no document height for them."),
 ("- A three-lens inspection of fidelity, responsive behaviour and technical quality, in which every finding was put to three independent sceptics. Forty-eight findings were confirmed, two of the lead's own claims were refuted and corrected, and a completeness critic added eight more.",
  "- A three-lens inspection of fidelity, responsive behaviour and technical quality, in which fifty findings were each put to three independent sceptics: forty-eight were confirmed and two of the lead's own claims were refuted and corrected. A completeness critic then added eight further findings, which did not themselves go through the sceptic rounds."),

 # ---- §10 title and integrity statement
 ("## 10. Changes to the project since the Phase 0 inspection",
  "## 10. Changes to the project during and since the Phase 0 inspection"),
 ("**No original project file has been modified or deleted at any point.** All 44 files present at the Phase 0 inspection remain byte-identical, verified by md5 after every write.",
  "**No original project file has been edited or deleted at any point.** All 44 original files remain byte-identical, checked by md5 against the Phase 0 inventory after each document was written. Two changes to the tree did occur and are listed above: the owner renamed the entry page, which altered its filename but not its contents, and four new files were added alongside the originals."),

 # ---- §12 attribution of the four gating decisions
 ("Phase 1 consolidated these into thirty decisions; Phase 2 identified the four that gate the design system.",
  "Phase 1 consolidated these into thirty decisions in its Appendix A and itself identified the four that gate the design system: confirmation of the extended palette beyond the three primaries; whether the 9 to 13 pixel tracked labels are brand-mandated on phones; the browser and device support matrix; and the intended behaviour above 1440 pixels."),

 # ---- §13 exit criteria honesty
 ("- [x] Scope and exclusions agreed.", "- [ ] Scope and exclusions drafted from the foundation conversation, but not formally confirmed by the owner."),
 ("- [x] Project identity, positioning and objective established.",
  "- [x] Project identity, positioning and objective established, with the brand-origin claim flagged as unconfirmed.\n- [x] Phase 0 had no written specification and therefore no contemporaneous exit criteria; the list below is reconstructed from what the phase actually produced."),
]

applied, failed = 0, []
for old, new in EDITS:
    if old in t:
        t = t.replace(old, new, 1); applied += 1
    else:
        failed.append(old[:90])

open(DOC, 'w', encoding='utf-8', newline='\n').write(t)
print("edits applied : %d/%d" % (applied, len(EDITS)))
if failed:
    print("NOT MATCHED:")
    for f in failed:
        print("   -", f)

print("\n=== structure after patch ===")
print("  bytes: %s  words: %s" % (format(len(t), ','), format(len(t.split()), ',')))
heads = re.findall(r'^## (\d+)\. ', t, re.M)
print("  sections:", [int(h) for h in heads])
s = re.sub(r'`[^`\n]*`', '', re.sub(r'```.*?```', '', t, flags=re.S))
print("  bare tags outside code:", len(re.findall(r'<(/?[a-zA-Z][a-zA-Z0-9-]*)[^>\n]{0,40}>', s)))
print("  unbalanced-backtick lines:", sum(1 for l in t.split('\n') if l.count('`') % 2 and not l.strip().startswith('```')))
print("  tables well-formed:", all(l.count('|') >= 3 for l in t.split('\n') if l.startswith('| ')))
print("\n=== claims that must no longer appear ===")
for bad, label in [
    ("no navigation at all", "'no navigation at all'"),
    ("was discarded", "'was discarded'"),
    ("full-page captures at each", "'full-page captures at each'"),
    ("Two requests 404", "'Two requests 404'"),
    ("| 768 | tablet rules", "'tablet rules' label"),
    ("Specified; awaiting this document", "old Phase 3 roadmap status"),
    ("verified by md5 after every write", "unqualified md5 claim"),
]:
    print("  %-34s %s" % (label, "GONE" if bad not in t else "*** STILL PRESENT ***"))
