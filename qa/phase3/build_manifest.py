# -*- coding: utf-8 -*-
"""GOD SQUAD Phase 3 — asset manifest.

Classifies every file, assigns a status, names the canonical member of each
duplicate group, and proposes a production name, format and Shopify destination.
Writes PHASE-3-ASSET-MANIFEST.csv to the project root. Reads only; creates no
asset and deletes nothing.
"""
import os, io, sys, csv, json, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
rows = json.load(open(HERE + '/inventory-raw.json', encoding='utf-8'))

# path -> (category, status, production name, format, shopify usage, notes)
# Statuses: KEEP OPTIMIZE REPLACE ARCHIVE REMOVE "REFERENCE ONLY" "BUSINESS INFORMATION REQUIRED"
C = {
 'images/WHITE FONT LOGO.png': ('LOGO', 'REPLACE', 'logo-god-squad.svg', 'SVG',
    'Theme setting: logo',
    'In use in header (78px) and footer (56px). 500x500 RGBA with heavy transparent padding, so the visible mark renders about 66x50 and reads half its mockup size. Filename contains spaces and upper case. Needs a vector master; PSD sources exist outside the project and were not opened. VECTOR LOGO REQUIRED.'),
 'images/logo.png': ('LOGO', 'ARCHIVE', 'logo-god-squad-on-black.png', 'PNG', 'None',
    'White wordmark on a solid black square. Not referenced by the page. Canonical of DUP-04. Possible social/profile candidate once a vector exists.'),
 'uploads/God-Squad-Images/06-logo.png': ('LOGO', 'ARCHIVE', '', 'PNG', 'None', 'Byte-identical duplicate of images/logo.png (DUP-04).'),
 'white-font-300x300-mu98qi59-mytq.png': ('LOGO', 'ARCHIVE', '', 'PNG', 'None', 'Unreferenced export artefact, 244x184 despite the 300x300 filename.'),
 'white-font-trans-mu98q2ez-zrdd.png': ('LOGO', 'ARCHIVE', '', 'PNG', 'None', 'Unreferenced export artefact. Same 500x500 size as its sibling but a different hash, so it is a separate encode, not a copy.'),
 'white-font-trans-mu98qky0-5tt6.png': ('LOGO', 'ARCHIVE', '', 'PNG', 'None', 'Unreferenced export artefact, sibling of the above.'),

 'images/hero-group.png': ('HERO', 'OPTIMIZE', 'hero-walk-by-faith-desktop.webp', 'WebP',
    'Hero section: image setting',
    'The live desktop hero and the LCP image. 1672x941 RGB PNG with no alpha, so PNG buys nothing. A WebP ladder at 1672/1280/960/640/420 now exists in phase-3-assets/hero (94% smaller at full size, verified free of visible artefacts). Canonical of DUP-01. Provenance is AI-generated: ASSET PROVENANCE SHOULD BE VERIFIED.'),
 'chatgpt-image-sep-20-2026-11_06_34-am-mu98j9xl-evm9.png': ('HERO', 'ARCHIVE', '', 'PNG', 'None', 'Byte-identical duplicate of images/hero-group.png (DUP-01), left in the project root.'),
 'uploads/ChatGPT Image Sep 20, 2026, 11_06_34 AM.png': ('HERO', 'ARCHIVE', '', 'PNG', 'None', 'Byte-identical duplicate of images/hero-group.png (DUP-01), the original upload.'),
 'images/hero-model.webp': ('HERO', 'REFERENCE ONLY', '', 'WebP', 'None',
    'A 650x480 crop of the mockup hero showing the single capped model. Not referenced. Canonical of DUP-02. Useful only as a composition reference.'),
 'uploads/God-Squad-Images/01-hero-model.webp': ('HERO', 'REFERENCE ONLY', '', 'WebP', 'None', 'Byte-identical duplicate of images/hero-model.webp (DUP-02).'),

 '01-hero-model-mu98p88t-7jig.webp': ('STORY', 'REPLACE', '(none - superseded, see note)', 'WebP',
    'Our Story section: image setting',
    'CURRENTLY IN USE as the Our Story background, and it is the wrong asset: a 650x480 crop of the mockup HERO with the headline fragments "A PURPOSE", "K BY" and "TH." baked into the pixels, visible at every width. Rendered at 998x520, a 1.53x upscale, with about 29% of its height cropped away. Separate re-encode of DUP-02, not byte-identical. It is superseded rather than renamed: the slot should be filled by story-community.webp cut from a NEW high-resolution master, so this file gets no production name of its own. HIGH-RES STORY MASTER REQUIRED.'),
 'images/our-story.webp': ('STORY', 'REPLACE', 'story-community.webp', 'WebP',
    'Our Story section: image setting',
    'The three-model composition the mockup intends for Our Story, but never referenced by the page. At 535x348 it is far too small for a slot that renders about 1000px wide. Canonical of DUP-05. HIGH-RES STORY MASTER REQUIRED.'),
 'uploads/God-Squad-Images/05-our-story-models.webp': ('STORY', 'REFERENCE ONLY', '', 'WebP', 'None', 'Byte-identical duplicate of images/our-story.webp (DUP-05).'),

 'images/product-tee.webp': ('PRODUCT', 'REPLACE', 'product-signature-tee-front.webp', 'WebP',
    'Shopify product media',
    '235x230 crop of the 1024x1536 mockup, rendered at 288px on desktop and 327-382px on phones, a device-pixel upscale of about 2.8x. Canonical of DUP-08. HIGH-RES PRODUCT MASTER REQUIRED. Views other than front are MISSING.'),
 'images/product-hoodie.webp': ('PRODUCT', 'REPLACE', 'product-heavyweight-hoodie-front.webp', 'WebP',
    'Shopify product media',
    '235x235 mockup crop. Canonical of DUP-07. HIGH-RES PRODUCT MASTER REQUIRED. Views other than front are MISSING.'),
 'images/product-cap.webp': ('PRODUCT', 'REPLACE', 'product-utility-cap-front.webp', 'WebP',
    'Shopify product media',
    '215x190 mockup crop, and the only non-square product source, so it is edge-cropped inside the 1:1 tile. Canonical of DUP-06. HIGH-RES PRODUCT MASTER REQUIRED.'),
 'uploads/God-Squad-Images/02-product-oversized-tee.webp': ('PRODUCT', 'REFERENCE ONLY', '', 'WebP', 'None', 'Byte-identical duplicate of images/product-tee.webp (DUP-08).'),
 'uploads/God-Squad-Images/03-product-heavyweight-hoodie.webp': ('PRODUCT', 'REFERENCE ONLY', '', 'WebP', 'None', 'Byte-identical duplicate of images/product-hoodie.webp (DUP-07).'),
 'uploads/God-Squad-Images/04-product-utility-cap.webp': ('PRODUCT', 'REFERENCE ONLY', '', 'WebP', 'None', 'Byte-identical duplicate of images/product-cap.webp (DUP-06).'),

 'images/icon-search.png': ('ICON', 'REPLACE', 'icon-search.svg', 'SVG', 'snippets/icon-search.liquid',
    'UI icon, 110x110 raster drawn at 24px with cream baked into the pixels, so it cannot inherit colour or respond to hover. A drawn SVG replacement exists in phase-3-assets/icons.'),
 'images/icon-account.png': ('ICON', 'REPLACE', 'icon-account.svg', 'SVG', 'snippets/icon-account.liquid', 'UI icon, 110x110 raster drawn at 24px. Drawn SVG replacement available.'),
 'images/icon-cart.png': ('ICON', 'REPLACE', 'icon-cart.svg', 'SVG', 'snippets/icon-cart.liquid',
    'UI icon, 110x110 raster drawn at 24px. Retains a sliver of the sprite sheet gold badge along its right edge. Drawn SVG replacement available.'),
 'images/icon-globe.png': ('ICON', 'REPLACE', 'icon-globe.svg', 'SVG', 'Announcement bar and Brand Values block',
    'Used twice, at 16px in the announcement bar and 44px in the values row, so one raster serves two very different sizes. Gold is baked in. A drawn SVG is NOT yet authored because the globe is a feature icon whose character is approved; see the feature-icon decision.'),
 'images/icon-crown.png': ('ICON', 'OPTIMIZE', 'icon-crown.webp', 'WebP', 'Brand Values block: icon setting',
    'FEATURE icon, 130x110 drawn at 44px. Phase 3 spec section 17 requires its visual character be preserved and forbids redesign, so it is not redrawn. Convert to WebP for weight, or commission a faithful SVG trace. DESIGN DECISION REQUIRED.'),
 'images/icon-community.png': ('ICON', 'OPTIMIZE', 'icon-community.webp', 'WebP', 'Brand Values block: icon setting', 'FEATURE icon, 150x110 drawn at 44px. Same treatment as the crown.'),
 'images/icon-diamond.png': ('ICON', 'OPTIMIZE', 'icon-diamond.webp', 'WebP', 'Brand Values block: icon setting', 'FEATURE icon, 130x110 drawn at 44px. Same treatment as the crown.'),

 'images/icon-facebook.png': ('SOCIAL', 'REPLACE', 'icon-facebook.svg', 'SVG', 'snippets/social-icons.liquid',
    'Circled two-tone badge cut from the social sprite, where the mockup shows a plain glyph. Platform marks are trademarks and should come from each platform official brand kit rather than being traced. BUSINESS INFORMATION REQUIRED: confirm the live Facebook URL.'),
 'images/icon-instagram.png': ('SOCIAL', 'REPLACE', 'icon-instagram.svg', 'SVG', 'snippets/social-icons.liquid',
    'As above. BUSINESS INFORMATION REQUIRED: confirm the live Instagram URL, and whether the TikTok and YouTube channels shown in the mockup exist.'),

 'images/icons-sprite.png': ('SPRITE', 'ARCHIVE', '', 'PNG', 'None',
    'A 2172x724 AI-generated contact sheet of UI and feature icons, with heavy matting halos. Never referenced by the page; the individual PNGs were cut from it. Superseded by the SVG set. Canonical of DUP-03.'),
 'images/social-sprite.png': ('SPRITE', 'ARCHIVE', '', 'PNG', 'None',
    'A 2172x724 AI-generated sheet of ten social marks in three styles. Never referenced. Canonical of DUP-09. Not a licensing-safe source for platform trademarks.'),
 'uploads/ChatGPT Image Sep 20, 2026, 10_11_00 AM.png': ('SPRITE', 'ARCHIVE', '', 'PNG', 'None', 'Byte-identical duplicate of images/icons-sprite.png (DUP-03).'),
 'uploads/ChatGPT Image Sep 20, 2026, 10_11_00 AM-34af7243.png': ('SPRITE', 'ARCHIVE', '', 'PNG', 'None', 'Second byte-identical duplicate of images/icons-sprite.png (DUP-03).'),
 'uploads/ChatGPT Image Sep 20, 2026, 10_56_48 AM.png': ('SPRITE', 'ARCHIVE', '', 'PNG', 'None', 'Byte-identical duplicate of images/social-sprite.png (DUP-09).'),

 'uploads/GODSQUAD WEBSITE MOCKUP.png': ('MOCKUP', 'REFERENCE ONLY', '', 'PNG', 'None',
    'THE APPROVED DESIGN MASTER, 1024x1536. Every product and story crop in the project was cut from it. Never use as a production website image. Take full-quality pixels from here, not from the WebP derivative.'),
 'uploads/God-Squad-Images/00-full-mockup-reference.webp': ('MOCKUP', 'REFERENCE ONLY', '', 'WebP', 'None',
    'The same mockup re-encoded to WebP at 182,250 bytes. The reference Phases 1 and 2 cite. Not a duplicate by hash because the format differs.'),
 'uploads/pasted-1789874193900-0.png': ('REFERENCE', 'REFERENCE ONLY', '', 'PNG', 'None', 'Screenshot of the Claude Design editor, 1920x1009. Records the owner decision history. Never a production image.'),
 'uploads/pasted-1789874322321-0.png': ('REFERENCE', 'REFERENCE ONLY', '', 'PNG', 'None', 'Editor screenshot, 1920x1009. Shows the globe icon and footer edits.'),
 'uploads/pasted-1789874476205-0.png': ('REFERENCE', 'REFERENCE ONLY', '', 'PNG', 'None', 'Editor screenshot, 1920x1009. Shows the restored gold globe.'),
 'uploads/pasted-1789874083026-0.png': ('REFERENCE', 'REFERENCE ONLY', '', 'PNG', 'None', 'A 118x77 crop of a globe icon, pasted during the editor session.'),
 'uploads/God-Squad-Images/README.txt': ('OTHER', 'KEEP', '', 'TXT', 'None',
    'States that the crops in this folder were cut from the 1024x1536 mockup. Primary evidence for the resolution ceiling; keep it with the assets it describes.'),

 '.thumbnail': ('OTHER', 'REMOVE', '', 'WebP', 'None',
    'A 640x355 editor-generated preview of the page. Not referenced and of no production value. Candidate for removal after approval.'),
 'God Squad Website.html': ('OTHER', 'KEEP', '', 'HTML', 'Design baseline only',
    'The approved visual baseline. Not an asset and not a migration source; its markup is rebuilt natively in Phase 10.'),
 'support.js': ('OTHER', 'REMOVE', '', 'JS', 'None',
    'The Claude Design runtime. Has no place in a storefront and is discarded at Phase 10. Candidate for removal once the prototype is retired.'),
}
DOCS = ('PHASE-0-PROJECT-FOUNDATION.md', 'PHASE-1-WEBSITE-AUDIT.md', 'PHASE-2-DESIGN-SYSTEM.md',
        'PHASE-2-DESIGN-TOKENS.css')

FIELDS = ['Category', 'Current Filename', 'Current Path', 'File Type', 'Width', 'Height',
          'Aspect Ratio', 'File Size', 'Hash', 'Current Usage', 'Duplicate Group', 'Status',
          'Canonical Asset', 'Recommended Production Name', 'Recommended Format',
          'Recommended Shopify Usage', 'Notes']

out, unclassified = [], []
for r in sorted(rows, key=lambda r: (r['folder'], r['path'])):
    if r['filename'] in DOCS:
        cat, st, pn, fmt, use, note = ('OTHER', 'KEEP', '', r['ext'].upper(), 'Project documentation',
                                       'Phase deliverable, not an asset.')
    elif r['path'] in C:
        cat, st, pn, fmt, use, note = C[r['path']]
    else:
        unclassified.append(r['path']); continue
    out.append({
        'Category': cat, 'Current Filename': r['filename'], 'Current Path': r['path'],
        'File Type': r['mime'], 'Width': r['width'], 'Height': r['height'],
        'Aspect Ratio': r['ratio'], 'File Size': r['bytes'], 'Hash': 'md5:' + r['md5'],
        'Current Usage': ('Referenced by the page' if r['referenced'] == 'yes' else 'Not referenced'),
        'Duplicate Group': r['dup_group'], 'Status': st,
        'Canonical Asset': r['canonical'], 'Recommended Production Name': pn,
        'Recommended Format': fmt, 'Recommended Shopify Usage': use, 'Notes': note})

# production copies created this phase
PROD = os.path.join(PROJECT, 'brand-assets', 'phase-3-assets')
for sub, cat, use, note in [
    ('icons', 'ICON', 'snippets/icon-*.liquid', 'Drawn to the Phase 2 contract: 24x24, stroke 1.5, currentColor. Not traced from the raster PNGs.'),
    ('hero', 'HERO', 'Hero section: image setting', 'Non-destructive WebP re-encode of images/hero-group.png at q82. Original preserved.')]:
    d = os.path.join(PROD, sub)
    if not os.path.isdir(d):
        continue
    for f in sorted(os.listdir(d)):
        p = os.path.join(d, f)
        import hashlib
        b = open(p, 'rb').read()
        out.append({
            'Category': cat, 'Current Filename': f, 'Current Path': 'phase-3-assets/%s/%s' % (sub, f),
            'File Type': ('image/svg+xml' if f.endswith('.svg') else 'image/webp'),
            'Width': '', 'Height': '', 'Aspect Ratio': '', 'File Size': len(b),
            'Hash': 'md5:' + hashlib.md5(b).hexdigest(),
            'Current Usage': 'Production copy created in Phase 3; not yet wired into anything',
            'Duplicate Group': '', 'Status': 'KEEP', 'Canonical Asset': '',
            'Recommended Production Name': f, 'Recommended Format': ('SVG' if f.endswith('.svg') else 'WebP'),
            'Recommended Shopify Usage': use, 'Notes': note})

if unclassified:
    print("*** UNCLASSIFIED — every file must be classified ***")
    for u in unclassified:
        print("   ", u)
    sys.exit(1)

dest = os.path.join(PROJECT, 'PHASE-3-ASSET-MANIFEST.csv')
with open(dest, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(out)

print("wrote %s" % dest)
print("rows: %d (%d original files + %d production copies)" % (len(out), len(rows), len(out) - len(rows)))
print("\nby category:")
for k, v in sorted(collections.Counter(r['Category'] for r in out).items()):
    print("  %-14s %d" % (k, v))
print("\nby status:")
for k, v in sorted(collections.Counter(r['Status'] for r in out).items(), key=lambda kv: -kv[1]):
    print("  %-30s %d" % (k, v))
json.dump(out, open(HERE + '/manifest.json', 'w', encoding='utf-8'), indent=1)
