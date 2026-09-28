# -*- coding: utf-8 -*-
"""Phase 6 theme validation. Extends the Phase 5 pass with collection checks."""
import json, re, io, sys, os, glob, hashlib, csv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
os.chdir(r"C:\Users\TEST\OneDrive\Documents\GodSquad Website")
norm = lambda p: p.replace(os.sep, '/')
ok = True


def check(label, passed, detail=''):
    global ok
    if not passed:
        ok = False
    print("  %-56s %s %s" % (label, "OK" if passed else "*** FAIL ***", detail))


strip_css = lambda s: re.sub(r'/\*.*?\*/', '', s, flags=re.S)
def strip_liquid(s):
    """Remove both comment forms: the {% comment %} tag pair AND the bare
    comment/endcomment lines that appear inside a {% liquid %} block. The second
    form is easy to miss and it is where the code explains what it deliberately
    does NOT do, so leaving it in makes every prohibition check fire on its own
    documentation."""
    s = re.sub(r'\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}', '', s, flags=re.S)
    s = re.sub(r'^[ \t]*comment[ \t]*$.*?^[ \t]*endcomment[ \t]*$', '', s, flags=re.S | re.M)
    return s

R = lambda p: open(p, encoding='utf-8').read()
card = R('snippets/product-card.liquid')
cardc = strip_liquid(card)
sect = R('sections/featured-collection.liquid')
sectc = strip_liquid(sect)
hero = R('sections/hero.liquid')
layout = R('layout/theme.liquid')
css_card = strip_css(R('assets/component-product-card.css'))
css_sect = strip_css(R('assets/section-featured-collection.css'))
css_btn = strip_css(R('assets/component-button.css'))
css_hero = strip_css(R('assets/section-hero.css'))
tmpl = json.load(open('templates/index.json', encoding='utf-8'))
schema = json.loads(re.search(r'\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}', sect, re.S).group(1))

print("=== THEME FILES ===")
tot = 0
for pat in ['layout/*', 'sections/*', 'snippets/*', 'assets/*', 'config/*', 'locales/*', 'templates/*']:
    for p in sorted(glob.glob(pat)):
        s = os.path.getsize(p)
        tot += s
        print("  %-46s %9s B" % (norm(p), format(s, ',')))
print("  %-46s %9s B" % ("TOTAL", format(tot, ',')))

print("\n=== JSON AND SCHEMA PARSE ===")
for p in glob.glob('sections/*.json') + glob.glob('templates/*.json') + glob.glob('config/*.json') + glob.glob('locales/*.json'):
    try:
        json.load(open(p, encoding='utf-8'))
        print("  OK   %s" % norm(p))
    except Exception as e:
        ok = False
        print("  FAIL %s -> %s" % (norm(p), e))
for p in glob.glob('sections/*.liquid'):
    m = re.search(r'\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}', R(p), re.S)
    if not m:
        ok = False
        print("  FAIL %s no schema" % norm(p))
        continue
    try:
        sc = json.loads(m.group(1))
        print("  OK   %-32s settings=%-3d presets=%-2d enabled_on=%s"
              % (norm(p), len(sc.get('settings', [])), len(sc.get('presets', [])),
                 sc.get('enabled_on', {}).get('groups')))
    except Exception as e:
        ok = False
        print("  FAIL %s -> %s" % (norm(p), e))

print("\n=== TEMPLATE WIRING ===")
check("index.json order covers every section", set(tmpl['order']) == set(tmpl['sections']), str(tmpl['order']))
for k, v in tmpl['sections'].items():
    check("section '%s' -> sections/%s.liquid" % (k, v['type']), os.path.exists('sections/%s.liquid' % v['type']))
ids = {s['id'] for s in schema['settings'] if s.get('id')}
sel = {s['id']: [o['value'] for o in s['options']] for s in schema['settings'] if s['type'] == 'select'}
rng = {s['id']: (s['min'], s['max']) for s in schema['settings'] if s['type'] == 'range'}
for k, v in tmpl['sections'].items():
    if v['type'] != 'featured-collection':
        continue
    unknown = sorted(set(v['settings']) - ids)
    check("'%s' settings all exist in the schema" % k, not unknown, str(unknown or ''))
    bad = [(a, b) for a, b in v['settings'].items() if a in sel and b not in sel[a]]
    check("'%s' select values are declared options" % k, not bad, str(bad or ''))
    oob = [(a, b) for a, b in v['settings'].items() if a in rng and not (rng[a][0] <= b <= rng[a][1])]
    check("'%s' range values are in range" % k, not oob, str(oob or ''))
for pr in schema['presets']:
    unknown = sorted(set(pr['settings']) - ids)
    check("preset '%s' settings all exist" % pr['name'], not unknown, str(unknown or ''))
    bad = [(a, b) for a, b in pr['settings'].items() if a in sel and b not in sel[a]]
    check("preset '%s' select values declared" % pr['name'], not bad, str(bad or ''))
check("no collection handle is invented anywhere",
      not any('collection' in v['settings'] for v in tmpl['sections'].values()),
      "index.json ships no collection: BUSINESS INFORMATION REQUIRED")

print("\n=== NO INVENTED STORE DATA ===")
money_lit = re.findall(r'[\u20B1$\u20AC\u00A3]\s?\d', cardc + sectc)
check("no currency symbol followed by a number in Liquid", not money_lit, str(money_lit[:4]))
check("price goes through the money filter", '| money' in cardc)
check("no bestseller or ranking logic", not re.search(r'\bsort\b|\bbest_selling\b|\brank', cardc + sectc, re.I))
check("no hard-coded product handle or title", not re.search(r'/products/[a-z0-9-]+', cardc + sectc))
check("no hand-built CDN URL", 'cdn.shopify.com' not in cardc + sectc)
check("no href=\"#\"", '"#"' not in cardc + sectc)
check("swatch colour comes only from Shopify swatch data",
      'value.swatch.color' in cardc and not re.search(r'#[0-9A-Fa-f]{6}', cardc))
check("collection URL is never constructed", '/collections/' not in cardc + sectc)
check("product URL comes from product.url", 'href="{{ product.url }}"' in cardc)

print("\n=== MARKUP CONTRACT ===")
check("card title is a heading element", '<h{{ heading_level }}' in cardc)
check("no h1 in either new file", '<h1' not in cardc + sectc)
check("section heading is an h2", '<h2 class="featured-collection__heading">' in sectc)
check("one anchor per card", cardc.count('<a class="product-card__link"') == 1)
check("no <script> in the new files", '<script' not in cardc + sectc)
check("no inline event handlers", not re.findall(r'\son[a-z]+\s*=\s*"', cardc + sectc))
check("grid is a list with an explicit role", 'role="list"' in sectc and '<ul class="product-grid"' in sectc)
check("swatch dots are aria-hidden", cardc.count('aria-hidden="true"') >= 2)
check("image alt is never invented", 'alt: alt_text' in cardc and 'assign alt_text = img.alt' in card)
check("lazy loading is the default", "assign loading_attr = 'lazy'" in card)
check("explicit widths and sizes on the card image",
      "widths: '180" in cardc and 'sizes: card_sizes' in cardc)
check("empty state is editor-only", 'request.design_mode' in sectc)
check("view-all falls back to the collection's own url", 'assign view_all_url = collection.url' in sect)

print("\n=== TOKEN FIDELITY ===")
tok = set(re.findall(r'(--[\w-]+)\s*:', strip_css(R('assets/design-tokens.css'))))
local = {'--product-cols', '--product-track-ideal', '--product-track-floor', '--product-title-lh',
         '--swatch-fill', '--swatch-image', '--header-overlay-offset',
         '--fc-space-top', '--fc-space-bottom', '--fc-header-clearance',
         '--hero-focal-x', '--hero-wash-hold', '--hero-wash-end'}
for name, body in (('component-product-card.css', css_card),
                   ('section-featured-collection.css', css_sect),
                   ('component-button.css', css_btn)):
    used = set(re.findall(r'var\((--[\w-]+)', body))
    undef = sorted(u for u in used if u not in tok and u not in local)
    check("%s: no undefined custom property" % name, not undef, str(undef or ''))
    hexes = re.findall(r'#[0-9A-Fa-f]{3,6}\b', body)
    check("%s: no raw hex" % name, not hexes, str(hexes[:4]))
    check("%s: no !important" % name, '!important' not in body)
    gs = sorted(set(re.findall(r'var\((--gs-[\w-]+)', body)))
    check("%s: no palette-layer token reached directly" % name, not gs, str(gs))
outlines = re.findall(r'outline\s*:', css_btn)
check("button component declares no outline (Phase 2 s10.3)", not outlines, str(outlines))
card_outlines = re.findall(r'outline\s*:\s*([^;]+);', css_card)
check("card's only outline use is remove-then-redraw",
      sorted(set(x.strip() for x in card_outlines)) ==
      sorted({'none', 'var(--focus-width) solid var(--focus-ring)'}), str(sorted(set(card_outlines))))

print("\n=== STYLESHEET LOADING ===")
check("card CSS loaded by the section, not the layout",
      "'component-product-card.css' | asset_url" in sect and 'component-product-card.css' not in layout)
check("section CSS loaded by the section, not the layout",
      "'section-featured-collection.css' | asset_url" in sect and 'section-featured-collection.css' not in layout)
check("button CSS is a shared component loaded by the layout",
      "'component-button.css' | asset_url" in layout and 'component-button.css' not in sect + hero)
guard = sect.index('{%- if has_products == false')
check("a section with nothing to show requests no stylesheet",
      sect.index("'component-product-card.css'") > guard)
check("the live guard tests products, not just a chosen collection",
      'has_products == false and request.design_mode == false' in sect)
check("card heading level follows whether the section renders its h2",
      'assign card_heading_level' in sect and 'heading_level: card_heading_level' in sect)
check("every button hover rule is pointer-gated (Phase 2 s22.1)",
      len(re.findall(r':hover', css_btn)) == len(re.findall(r'@media \(hover: hover\) and \(pointer: fine\)[^}]*\{(?:[^{}]|\{[^{}]*\})*\}', css_btn, re.S)) or
      all('@media (hover: hover)' in css_btn[max(0, m.start() - 400):m.start()]
          for m in re.finditer(r':hover', css_btn)))
check("secondary active state is surface-scoped like its hover",
      '.surface-light .button--secondary:active' in css_btn and '.surface-dark .button--secondary:active' in css_btn)
check("no span is styled as a button", 'span class="button' not in cardc)
check("colourway names come from the printed subset, not forloop.last",
      'swatch_names' in card and 'unless forloop.last' not in cardc)
check("body margin is reset so bands are full bleed",
      'body { margin: 0; }' in open('assets/design-tokens.css', encoding='utf-8').read())

print("\n=== BUTTON PROMOTION ===")
check("button system no longer defined in section-hero.css", '.button {' not in css_hero)
check("hero still places its CTA", '.hero__cta' in css_hero)
check("primary hover is not the accent (Phase 2 s10.3)",
      'var(--color-accent)' not in re.search(r'\.surface-dark \.button--primary:hover\s*\{[^}]*\}', css_btn).group(0))
check("accent variant exists only on the dark surface",
      '.surface-dark .button--accent' in css_btn and '.surface-light .button--accent' not in css_btn)
check("inline padding is --space-5 (Phase 2 s10.4)", 'padding: var(--space-4) var(--space-5);' in css_btn)

print("\n=== TRANSLATION KEYS ===")


def flat(d, pre=''):
    out = {}
    for k, v in d.items():
        out.update(flat(v, pre + k + '.')) if isinstance(v, dict) else out.update({pre + k: v})
    return out


have = set(flat(json.load(open('locales/en.default.json', encoding='utf-8'))))
need = set()
for p in glob.glob('sections/*.liquid') + glob.glob('snippets/*.liquid') + glob.glob('layout/*.liquid'):
    need |= set(re.findall(r"'([a-z0-9_]+\.[a-z0-9_.]+)'\s*\|\s*t\b", R(p)))
check("no missing translation key", not (need - have), str(sorted(need - have) or ''))
check("no unused translation key", not (have - need), str(sorted(have - need) or ''))
check("no 't' filter with a default: parameter", not re.findall(r"\|\s*t:\s*default", card + sect + layout))

print("\n=== THEME SETTINGS ===")
ss = json.load(open('config/settings_schema.json', encoding='utf-8'))
all_ids = {s['id'] for g in ss if isinstance(g, dict) for s in g.get('settings', []) if s.get('id')}
sd = json.load(open('config/settings_data.json', encoding='utf-8'))
check("product_image_ratio exists as a THEME setting", 'product_image_ratio' in all_ids)
check("image ratio is NOT a section setting (Phase 2 s27.6.5)", 'image_ratio' not in ids)
check("show_vendor is not offered (Phase 2 s27.1)", 'show_vendor' not in ids)
check("settings_data covers every schema setting",
      not (all_ids - set(sd['current'])), str(sorted(all_ids - set(sd['current'])) or ''))
check("theme.liquid consumes product_image_ratio", 'settings.product_image_ratio' in layout)

print("\n=== ORIGINAL PROJECT FILES UNTOUCHED ===")
EV = r"C:\Users\TEST\AppData\Local\Temp\claude\C--Users-TEST-OneDrive-Documents-GodSquad-Website\de238d03-508d-43ce-a377-210f71ff0033\scratchpad\audit-evidence"
orig = {r['path']: r['md5'] for r in csv.DictReader(open(EV + '/inventory.tsv', encoding='utf-8'), delimiter='\t')}
mod = [p for p, h in orig.items() if os.path.exists(p) and hashlib.md5(open(p, 'rb').read()).hexdigest() != h]
gone = [p for p in orig if not os.path.exists(p)]
check("tracked originals unmodified (%d files)" % len(orig), not mod and not gone,
      "MODIFIED=%s DELETED=%s" % (mod or 'none', gone or 'none'))

print("\nOVERALL:", "PASS" if ok else "*** FAILURES ABOVE ***")
