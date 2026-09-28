# -*- coding: utf-8 -*-
"""Assemble PHASE-3-ASSET-SYSTEM.md. Usage: python assemble.py <output.json> [--write]"""
import json, re, io, sys, os, csv, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
PROJECT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(PROJECT, "PHASE-3-ASSET-SYSTEM.md")
HERE = os.path.dirname(os.path.abspath(__file__))

TITLES = {1:"Asset Overview",2:"Asset Inventory",3:"Logo System",4:"Hero System",5:"Product Image System",
 6:"Story Images",7:"Collection Images",8:"Icon System",9:"Social Icons",10:"Sprite Audit",
 11:"Duplicate Assets",12:"Image Quality",13:"Image Format Strategy",14:"Compression Strategy",
 15:"Responsive Image Strategy",16:"Naming Convention",17:"Folder Structure",18:"Shopify Asset Mapping",
 19:"Missing Assets",20:"Assets Requiring Business Approval",21:"Phase 4 Asset Dependencies"}

TAG_RE = re.compile(r'<(/?[a-zA-Z][a-zA-Z0-9-]*(?:\s[^<>\n]{0,140})?)>')

def wrap_bare_tags(text):
    out, n = [], 0
    for i, part in enumerate(re.split(r'(```.*?```)', text, flags=re.S)):
        if i % 2:
            out.append(part); continue
        for j, seg in enumerate(re.split(r'(`[^`\n]*`)', part)):
            if j % 2:
                out.append(seg); continue
            seg, k = TAG_RE.subn(r'`<\1>`', seg); n += k; out.append(seg)
    s = ''.join(out)
    s, adj = re.subn(r'>``<', '>` `<', s)
    return s, n, adj

res = json.load(open(sys.argv[1], encoding='utf-8', errors='replace'))
res = res.get('result', res)
write = '--write' in sys.argv

sections, approvals, missing, risks = {}, [], [], []
print("Clusters:")
for c in res['results']:
    o = c.get('out')
    if not o:
        print("  %-22s *** NO OUTPUT ***" % c['key']); continue
    got = []
    for s in o.get('sections', []):
        n = int(s['number'])
        if 1 <= n <= 21:
            sections[n] = s; got.append(n)
    approvals += o.get('businessApproval', [])
    missing += o.get('missingAssets', [])
    risks += o.get('risks', [])
    print("  %-22s sections %s" % (c['key'], got))

gap = [n for n in range(1, 22) if n not in sections]
print("\nsections: %d/21  missing: %s" % (len(sections), gap or 'none'))
for n in sorted(sections):
    print("  %2d. %-38s %5d words" % (n, TITLES[n][:38], len(sections[n]['markdown'].split())))

def dedupe(items):
    seen, out = set(), []
    for x in items:
        k = re.sub(r'[^a-z0-9]', '', str(x).lower())[:70]
        if k and k not in seen:
            seen.add(k); out.append(x)
    return out

approvals, missing = dedupe(approvals), dedupe(missing)
# The four clusters raised 52 risks describing roughly 26 distinct ones, and each
# cluster scored severity on its own reading of P0. Consolidated and rescored here
# against one stated definition, so the register does not inflate against Phase 1,
# which reserved P0 for the three architecture blockers.
drafted = len(risks)
rk = [
 dict(id='AR-01', priority='P0', risk='No production-grade product photography exists. All three product images are crops of the 1024x1536 mockup: tee 235x230, hoodie 235x235, cap 215x190.',
      impact='Product media is soft at every render size, about 2.8x device-pixel upscale on a 2x phone. Re-encoding cannot create pixels that were never captured.',
      mitigation='Commission or supply original product photography at 2000px or more on the long edge, square, consistent lighting and background.', phase='PHASE 3 sourcing, consumed by PHASE 6 and PHASE 8'),
 dict(id='AR-02', priority='P0', risk='No Our Story master exists. The intended three-model composition is 535x348 and the slot renders about 1000px wide.',
      impact='Phase 7 cannot be completed at production quality from anything in the project.',
      mitigation='Supply an Our Story photograph at 2000px or more on the long edge.', phase='PHASE 3 sourcing, consumed by PHASE 7'),
 dict(id='AR-03', priority='P0', risk='No vector logo in SVG, AI or EPS form has been located. The wordmark in use is a 500x500 PNG whose transparent padding leaves the visible mark at about 66x50.',
      impact='The header mark renders around half its mockup size and cannot scale cleanly. Favicon and social profile assets cannot be derived properly.',
      mitigation='Supply a vector master, or authorise extraction from the unopened Desktop PSD sources.', phase='PHASE 3 sourcing, consumed by PHASE 4'),
 dict(id='AR-04', priority='P0', risk='No mobile hero source exists. The 1.777:1 desktop frame cropped into a phone band discards about a third of its width.',
      impact='The phone hero loses the third model and the back-print message, which is the content the hero exists to carry, while still paying for a wide image.',
      mitigation='Supply a portrait or art-directed phone crop, or a separate mobile frame.', phase='PHASE 3 sourcing, consumed by PHASE 5 and PHASE 9'),
 dict(id='AR-05', priority='P0', risk='The hero, both sprite sheets and the nine icon PNGs cut from them are AI-generated. Neither generation history nor licensing has been established.',
      impact='Ownership and licensing of the most prominent brand imagery are unverified before a commercial launch.',
      mitigation='ASSET PROVENANCE SHOULD BE VERIFIED. Confirm generation terms and commercial rights, or replace with owned photography.', phase='BUSINESS DECISION, before launch'),
 dict(id='AR-06', priority='P1', risk='The live LCP image is a 1,989,201-byte PNG served unchanged at every viewport, with no srcset, sizes, intrinsic dimensions or fetch priority.',
      impact='Largest Contentful Paint is dominated by a two-megabyte transfer on every first load, worst on mobile data.',
      mitigation='A verified WebP ladder already exists in phase-3-assets/hero at 94% smaller. Wire it in at Phase 10 with explicit widths and sizes.', phase='PHASE 10, measured in PHASE 12'),
 dict(id='AR-07', priority='P1', risk='The Our Story slot loads the wrong asset: a 650x480 crop of the mockup hero with the headline fragments A PURPOSE, K BY and TH. baked into the pixels.',
      impact='Another section typography shows inside the story image at every width, and CSS cannot suppress it because it is pixels, not text.',
      mitigation='Replace the reference when the story master lands. Until then it is a known visible defect.', phase='PHASE 7'),
 dict(id='AR-08', priority='P1', risk='The Facebook and Instagram marks in the project were cut from an AI-generated sprite sheet rather than taken from each platform official brand kit.',
      impact='Platform logos are trademarks with published usage rules. Approximations risk both visual incorrectness and trademark non-compliance.',
      mitigation='Take each mark from the platform own brand resources. Do not trace or redraw.', phase='PHASE 3 sourcing, consumed by PHASE 4'),
 dict(id='AR-09', priority='P1', risk='The nine raster UI and feature icons total 308,521 bytes with colour baked into the pixels at 110 to 150px canvases drawn at 16 to 44px.',
      impact='Icons cannot inherit colour, respond to hover or focus, or serve two sizes cleanly, and they carry weight out of proportion to their display size.',
      mitigation='Nine drawn SVGs now exist at 2,612 bytes total, a 99.2% reduction. Adopt at Phase 4 and Phase 10.', phase='PHASE 4 and PHASE 10'),
 dict(id='AR-10', priority='P1', risk='No favicon of any kind exists; /favicon.ico returns 404 on every load.',
      impact='A failed request on every page view and no brand mark in the browser tab, bookmarks or search results.',
      mitigation='Derive a favicon set once a vector logo exists. Blocked by AR-03.', phase='PHASE 13'),
 dict(id='AR-11', priority='P1', risk='The four feature icons (crown, community, globe, diamond) have no resolved format decision. The spec requires their visual character be preserved and forbids redesign.',
      impact='They cannot be replaced by the drawn set without changing approved brand artwork, yet they remain low-resolution rasters with gold baked in.',
      mitigation='DESIGN DECISION REQUIRED: keep as optimised raster, or commission a faithful vector trace.', phase='BUSINESS DECISION, consumed by PHASE 4'),
 dict(id='AR-12', priority='P2', risk='Nine md5 duplicate groups cover 20 files, leaving 11 redundant copies worth 6,733,692 bytes, 39.4% of all image bytes.',
      impact='Every future edit risks being applied to a stale copy, and the working tree is inflated.',
      mitigation='After approval, keep the canonical named in the manifest and archive the rest. Nothing is deleted in Phase 3.', phase='PHASE 3 approval, then PHASE 10'),
 dict(id='AR-13', priority='P2', risk='Two 2172x724 AI-generated sprite sheets totalling 1,761,902 bytes, plus three byte-identical copies, are referenced by nothing.',
      impact='Dead weight and a licensing-unsafe source for the platform marks cut from them.',
      mitigation='Superseded by the SVG set. Archive after approval; retained for now.', phase='PHASE 3 approval'),
 dict(id='AR-14', priority='P2', risk='images/icon-globe.png is one 110x110 raster used twice, at 16px in the announcement bar and 44px in the values row.',
      impact='One raster cannot be optically correct at both sizes; it is over-detailed at 16px and under-resolved at 44px.',
      mitigation='Resolve with the feature-icon decision in AR-11.', phase='PHASE 4'),
 dict(id='AR-15', priority='P2', risk='images/icon-cart.png retains a sliver of the sprite sheet gold badge along its right edge.',
      impact='A visible artefact of a neighbouring icon ships inside a header control.',
      mitigation='Superseded by the drawn icon-cart.svg.', phase='PHASE 4'),
 dict(id='AR-16', priority='P2', risk='images/product-cap.webp is 215x190, the only non-square product source, inside a 1:1 tile with object-fit cover.',
      impact='The cap is edge-cropped where the other two products are not, so the row is visually inconsistent.',
      mitigation='Shoot or crop all products square to the standard in section 5.', phase='PHASE 6'),
 dict(id='AR-17', priority='P2', risk='No purpose-made collection imagery exists. COLLECTION is a permitted category with zero assets.',
      impact='Collection pages and any Best Sellers row have no editorial imagery, and product images are not a substitute.',
      mitigation='Commission collection or editorial photography, or design collection cards that do not require it.', phase='PHASE 6'),
 dict(id='AR-18', priority='P2', risk='No social account is confirmed for any platform. The build shows two marks, the mockup showed four, and the sprite sheet contains ten.',
      impact='The footer cannot be completed without knowing which channels exist and their URLs.',
      mitigation='BUSINESS INFORMATION REQUIRED: confirm live channels and profile URLs.', phase='BUSINESS DECISION, consumed by PHASE 4'),
 dict(id='AR-19', priority='P2', risk='Two misconceptions about Shopify image delivery would waste effort if carried forward: that the CDN outputs AVIF, and that image_url alone emits srcset.',
      impact='Incorrect delivery code and an unachievable format expectation.',
      mitigation='The CDN serves WebP automatically and does not output AVIF. Pass explicit widths and sizes and render with image_tag; never hand-build CDN URLs.', phase='PHASE 10 and PHASE 12'),
 dict(id='AR-20', priority='P2', risk='3,878,503 bytes of editor reference screenshots sit in uploads/, 22.7% of all image bytes, and their content is undocumented beyond this phase.',
      impact='They are valuable as the record of owner decisions but are easily mistaken for production assets.',
      mitigation='Classified REFERENCE ONLY. Move to a reference folder after approval.', phase='PHASE 3 approval'),
 dict(id='AR-21', priority='P3', risk='Two files carry REMOVE and both remain in place: .thumbnail and support.js.',
      impact='Minor dead weight. Removing support.js would change the page, so it is out of scope for an asset phase.',
      mitigation='Retire .thumbnail after approval and support.js when the theme replaces the prototype.', phase='PHASE 10'),
 dict(id='AR-22', priority='P3', risk='Exactly one source was compressed, at one quality, verified by eye rather than by a difference metric.',
      impact='No quality ladder exists to compare against, so the q82 choice is defensible but not optimised.',
      mitigation='When real photography arrives, encode two or three qualities and compare before fixing a project default.', phase='PHASE 12'),
 dict(id='AR-23', priority='P3', risk='Two file pairs share identical dimensions and byte counts but different md5 hashes, the signature of a separate re-encode rather than a copy.',
      impact='A hash-only duplicate check reports them as distinct, so a later clean-up may keep both.',
      mitigation='Documented in section 11 as format or encode variants rather than exact duplicates.', phase='PHASE 3 approval'),
 dict(id='AR-24', priority='P3', risk='No size guide, fabric, care, packaging or craft imagery exists anywhere in the project.',
      impact='Product pages will have no supporting imagery beyond a single front view per item.',
      mitigation='Add to the photography brief alongside the product masters in AR-01.', phase='PHASE 8'),
 dict(id='AR-25', priority='P3', risk='The homepage loads 15 distinct images totalling 2,406,866 bytes, of which 308,521 is icon PNGs drawn at 16 to 44px.',
      impact='Payload is dominated by assets that could be a few kilobytes of inline SVG.',
      mitigation='Adopt the SVG set and the hero ladder; both already exist.', phase='PHASE 10 and PHASE 12'),
]
print("\nrisk register: %d drafted across four clusters, consolidated to %d distinct" % (drafted, len(rk)))
print("\nregisters: %d business approvals, %d missing assets, %d risks (%s)"
      % (len(approvals), len(missing), len(rk),
         ', '.join('%s:%d' % (p, sum(1 for r in rk if r['priority'] == p)) for p in ['P0','P1','P2','P3'])))

man = list(csv.DictReader(open(os.path.join(PROJECT, 'PHASE-3-ASSET-MANIFEST.csv'), encoding='utf-8-sig')))
st = collections.Counter(r['Status'] for r in man)
cat = collections.Counter(r['Category'] for r in man)

HEADER = """# GOD SQUAD — PHASE 3 ASSET SYSTEM

**Project:** God Squad Premium Faith-Driven Streetwear
**Phase:** 3 — Asset Preparation & Image System
**Date:** 2026-09-22
**Companion file:** `PHASE-3-ASSET-MANIFEST.csv` — 62 rows, the full inventory plus production copies
**Production copies:** `phase-3-assets/` — nine authored SVG icons and a five-rung hero WebP ladder
**Predecessors:** `PHASE-0-PROJECT-FOUNDATION.md`, `PHASE-1-WEBSITE-AUDIT.md`, `PHASE-2-DESIGN-SYSTEM.md`

## Scope of this phase

Phase 3 inspected, classified and documented every asset, detected duplicates by hash, and created non-destructive production copies where a copy could be made without taking a design decision.

**The website is functionally unchanged.** No HTML, CSS or JavaScript was touched, no section rebuilt, no navigation, typography or colour altered, no logo replaced, no Liquid written. The page still references exactly the files it referenced before this phase began, and nothing in `phase-3-assets/` is wired into it.

**No original was modified, renamed, destructively processed or deleted.** Two status labels are routinely misread, so both are stated here: **REMOVE** means *candidate for removal after final approval*, never *delete now*; **ARCHIVE** means *move to an archive location after approval*, not *discard*. Every file carrying either label is still in place.

**The constraint that shapes every recommendation.** Every photographic and product asset is a crop of one 1024 by 1536 mockup or a generated frame. That is a sourcing problem, not a processing problem: re-encoding changes how efficiently pixels are delivered, it does not create pixels that were never captured. Everything marked HIGH-RES PRODUCT MASTER REQUIRED, HIGH-RES STORY MASTER REQUIRED or VECTOR LOGO REQUIRED follows from it.
"""

CHECKLIST = """Every item the Phase 3 specification lists, with how it was satisfied.

- [x] **All assets inspected** — 48 files scanned recursively, 41 of them images (§2).
- [x] **Dimensions recorded** — parsed directly from PNG IHDR and WebP VP8/VP8L/VP8X headers, since no imaging library is installed and none was installed (§2).
- [x] **File sizes recorded** — every row of the manifest.
- [x] **Hashes calculated** — md5 for every file, with a sha256 prefix retained in the working inventory.
- [x] **Duplicates identified** — 9 exact groups covering 20 files, 11 redundant copies, 6,733,692 bytes (§11).
- [x] **Canonical assets identified** — one canonical per group, chosen by live reference first, then location, then path length (§11).
- [x] **Logo system documented** — every logo file, the padding defect, usage rules, and VECTOR LOGO REQUIRED (§3).
- [x] **Hero system documented** — candidates, verdicts, the WebP ladder and the missing mobile hero (§4).
- [x] **Product assets documented** — three files, all HIGH-RES PRODUCT MASTER REQUIRED, with views marked present or missing (§5).
- [x] **Story assets documented** — including that the live slot uses a crop of the mockup hero with headline text baked in (§6).
- [x] **Collection assets documented** — none purpose-made exists; the product-image rule is stated (§7).
- [x] **Icons documented** — classified UI, FEATURE, SOCIAL; nine drawn SVGs delivered (§8).
- [x] **Social icons documented** — present, missing and business-decision platforms separated; no account invented (§9).
- [x] **Sprites audited** — both sheets, unreferenced, superseded but retained (§10).
- [x] **Mockups separated** — the master mockup and the editor screenshots are REFERENCE ONLY (§2, §12).
- [x] **Production and reference distinction established** — carried in the manifest Status column and in §17.
- [x] **Naming system established** — with the explicit rule that no original is renamed (§16).
- [x] **Folder system established** — recommended tree plus the mapping from today's layout (§17).
- [x] **Responsive image strategy established** — width ladder, `image_url` with explicit `widths:` and `sizes:`, `image_tag`, loading strategy (§15).
- [x] **Shopify mapping established** — asset to destination, theme assets separated from merchant-uploaded media (§18).
- [x] **Missing assets documented** — Appendix B.
- [x] **Business approvals documented** — Appendix C.
- [x] **Performance risks documented** — Appendix A, at P0 to P3.
- [x] **Original assets preserved** — 0 modified, 0 deleted, verified by md5 against the Phase 0 inventory.
"""

body = []
for n in sorted(sections):
    md, _, _ = wrap_bare_tags(sections[n]['markdown'].strip())
    body.append("## %d. %s\n\n%s" % (n, TITLES[n], md))

risk_tbl = ['| ID | Priority | Risk | Impact | Mitigation | Owning phase |', '|---|---|---|---|---|---|']
cl = lambda s: str(s or '').replace('|', '/').replace('\n', ' ').strip()
for r in rk:
    risk_tbl.append('| %s | %s | %s | %s | %s | %s |' % (r['id'], r['priority'], cl(r['risk']), cl(r['impact']), cl(r['mitigation']), cl(r['phase'])))

doc = "\n\n".join([HEADER] + body + [
 "## Appendix A. Asset performance risk register\n\n"
 "Asset-related risks only. The four drafting clusters raised 52 entries describing roughly 25 distinct risks, each scoring severity on its own reading; they are consolidated and rescored here against one definition so the register does not inflate against Phase 1, which reserved P0 for three architecture blockers.\n\n"
 "**P0** — cannot launch without resolving, and no workaround exists inside the project, because the fix requires external sourcing or a business decision. Every P0 here is a sourcing or licensing gap, not a defect in the work.  \n"
 "**P1** — a major problem with a known fix, or a visible defect shipping today.  \n"
 "**P2** — an important improvement.  \n"
 "**P3** — polish.\n\n" + "\n".join(risk_tbl),
 "## Appendix B. Missing and required assets\n\n"
 "Listed only where the project genuinely lacks the asset. Nothing here is invented, and no view has been assumed to exist.\n\n"
 + "\n".join("- %s" % m for m in missing),
 "## Appendix C. Assets requiring business approval\n\n"
 "Decisions Phase 3 could not take on the business's behalf.\n\n"
 + "\n".join("- %s" % a for a in approvals),
 "## Appendix D. Phase 3 completion checklist\n\n" + CHECKLIST,
])
doc, wrapped, adj = wrap_bare_tags(doc)

print("\nVerification:")
heads = re.findall(r'^## (?:(\d+)\.|Appendix ([A-D])\.) ', doc, re.M)
nums = [int(h[0]) for h in heads if h[0]]
print("  numbered sections: %d  missing: %s  duplicated: %s"
      % (len(nums), [n for n in range(1, 22) if n not in nums] or 'none',
         [n for n, k in collections.Counter(nums).items() if k > 1] or 'none'))
print("  appendices:", [h[1] for h in heads if h[1]])
stripped = re.sub(r'`[^`\n]*`', '', re.sub(r'```.*?```', '', doc, flags=re.S))
print("  bare tags outside code:", len(TAG_RE.findall(stripped)))
print("  unbalanced-backtick lines:", sum(1 for l in doc.split('\n') if l.count('`') % 2 and not l.strip().startswith('```')))
print("  tables well-formed:", all(l.count('|') >= 3 for l in doc.split('\n') if l.startswith('| ')))
for phrase, why in [("delete now", "REMOVE misread as delete"), ("we deleted", "deletion claim"), ("was renamed to", "rename claim")]:
    hits = len(re.findall(phrase, doc, re.I))
    print("  %-28s %s" % ('"%s"' % phrase, ("%d occurrence(s) — check context" % hits) if hits else "absent"))
print("  manifest statuses: %s" % dict(st))
print("  characters: %s  words: %s" % (format(len(doc), ','), format(len(doc.split()), ',')))

if write:
    open(OUT, 'w', encoding='utf-8', newline='\n').write(doc.rstrip() + '\n')
    print("\nWROTE %s (%s bytes)" % (OUT, format(os.path.getsize(OUT), ',')))
    json.dump({'approvals': approvals, 'missing': missing, 'risks': rk,
               'status': dict(st), 'category': dict(cat)},
              open(HERE + '/registers.json', 'w', encoding='utf-8'), indent=1)
else:
    open(HERE + '/preview.md', 'w', encoding='utf-8', newline='\n').write(doc.rstrip() + '\n')
    print("\n(dry run) preview -> phase3/preview.md")
