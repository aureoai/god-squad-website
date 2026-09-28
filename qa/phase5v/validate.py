# -*- coding: utf-8 -*-
"""Phase 5 theme validation. Extends the Phase 4 pass with hero-specific checks."""
import json, re, io, sys, os, glob, hashlib, csv
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
os.chdir(r"C:\Users\TEST\OneDrive\Documents\GodSquad Website")
norm = lambda p: p.replace(os.sep, '/')
ok = True
def check(label, passed, detail=''):
    global ok
    if not passed: ok = False
    print("  %-52s %s %s" % (label, "OK" if passed else "*** FAIL ***", detail))

strip = lambda s: re.sub(r'/\*.*?\*/', '', s, flags=re.S)
hero   = open('sections/hero.liquid', encoding='utf-8').read()
css    = open('assets/section-hero.css', encoding='utf-8').read()
cssb   = strip(css)
layout = open('layout/theme.liquid', encoding='utf-8').read()
tmpl   = json.load(open('templates/index.json', encoding='utf-8'))
schema = json.loads(re.search(r'\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}', hero, re.S).group(1))
# Liquid comments document what the section deliberately does NOT do, so they
# must not be searched for the very patterns they are warning against.
heroc = re.sub(r'\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}', '', hero, flags=re.S)

print("=== THEME FILES ===")
tot = 0
for pat in ['layout/*','sections/*','snippets/*','assets/*','config/*','locales/*','templates/*']:
    for p in sorted(glob.glob(pat)):
        s = os.path.getsize(p); tot += s
        print("  %-44s %9s B" % (norm(p), format(s, ',')))
print("  %-44s %9s B" % ("TOTAL", format(tot, ',')))

print("\n=== JSON AND SCHEMA PARSE ===")
for p in glob.glob('sections/*.json')+glob.glob('templates/*.json')+glob.glob('config/*.json')+glob.glob('locales/*.json'):
    try:
        json.load(open(p, encoding='utf-8')); print("  OK   %s" % norm(p))
    except Exception as e:
        ok = False; print("  FAIL %s -> %s" % (norm(p), e))
for p in glob.glob('sections/*.liquid'):
    m = re.search(r'\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}', open(p, encoding='utf-8').read(), re.S)
    if not m:
        ok = False; print("  FAIL %s no schema" % norm(p)); continue
    try:
        s = json.loads(m.group(1))
        print("  OK   %-30s settings=%-3d presets=%-2d enabled_on=%s"
              % (norm(p), len(s.get('settings',[])), len(s.get('presets',[])), s.get('enabled_on',{}).get('groups')))
    except Exception as e:
        ok = False; print("  FAIL %s -> %s" % (norm(p), e))

print("\n=== TEMPLATE WIRES TO THE SECTION ===")
types = {k: v['type'] for k, v in tmpl['sections'].items()}
check("templates/index.json order covers every section", set(tmpl['order']) == set(tmpl['sections']), str(tmpl['order']))
for k, t in types.items():
    check("section '%s' -> sections/%s.liquid" % (k, t), os.path.exists('sections/%s.liquid' % t))
ids = {s['id'] for s in schema['settings'] if s['type'] not in ('header','paragraph')}
unknown = sorted(set(tmpl['sections']['hero']['settings']) - ids)
check("every template setting exists in the schema", not unknown, str(unknown or ''))
sel = {s['id']: [o['value'] for o in s['options']] for s in schema['settings'] if s['type'] == 'select'}
bad = [(k, v) for k, v in tmpl['sections']['hero']['settings'].items() if k in sel and v not in sel[k]]
check("every select value is a declared option", not bad, str(bad or ''))

print("\n=== CSS CLASSES THE TEMPLATE CAN PRODUCE ALL EXIST ===")
classes = set(re.findall(r'\.(hero--[\w-]+)', cssb))
produced = set()
for s in schema['settings']:
    if s['type'] == 'select':
        pre = {'height':'hero--h-','text_alignment':'hero--align-','text_position':'hero--pos-',
               'overlay':'hero--overlay-','focal_point':'hero--focal-'}.get(s['id'])
        if pre: produced |= {pre + o['value'] for o in s['options']}
# Two classes are deliberately styleless. hero--overlay-none has no scrim
# element to style; hero--align-left is the base state of .hero__content, so a
# rule for it would only restate the default.
BASE = {'hero--overlay-none', 'hero--align-left'}
missing = sorted(c for c in produced if c not in classes and c not in BASE)
check("every modifier class the schema can emit is styled", not missing, str(missing or ''))
print("     styleless by design: %s" % ', '.join(sorted(BASE)))

print("\n=== TOKEN FIDELITY ===")
tok = set(re.findall(r'(--[\w-]+)\s*:', strip(open('assets/design-tokens.css', encoding='utf-8').read())))
published = {'--header-overlay-offset', '--hero-focal-x', '--hero-wash-hold', '--hero-wash-end'}
used = set(re.findall(r'var\((--[\w-]+)', cssb))
undef = sorted(u for u in used if u not in tok and u not in published)
check("no undefined custom property in section-hero.css", not undef, str(undef or ''))
hexes = re.findall(r'#[0-9A-Fa-f]{3,6}\b', cssb)
check("no raw hex in section-hero.css", not hexes, str(hexes[:5]))
check("no !important", '!important' not in cssb)
gs = sorted(set(re.findall(r'var\((--gs-[\w-]+)', cssb)))
check("no palette-layer token reached directly (Phase 2 R2)", not gs, str(gs))
print("     rgba(13, 12, 10, ...) scrim stops: %d  (the ink literal Phase 2 defines as the scrim base)"
      % len(re.findall(r'rgba\(13, 12, 10', cssb)))
check("stylesheet is loaded by the section, not the layout",
      "'section-hero.css' | asset_url | stylesheet_tag" in hero and 'section-hero.css' not in layout)

print("\n=== HERO MARKUP CONTRACT ===")
check("exactly one <h1>", hero.count('<h1') == 1 and hero.count('</h1>') == 1)
check("no <script> in the section", '<script' not in hero)
check("no <video>, no autoplay media", '<video' not in hero and 'autoplay' not in hero)
check("no inline event handlers", not re.findall(r'\son[a-z]+\s*=', heroc))
check("no hard-coded href", not re.findall(r'href="(?!\{\{)', heroc))
check("CTA renders only when a link exists", 'has_cta' in hero and 'btn_link != blank' in hero)
check("button_link has no default value",
      all('default' not in s for s in schema['settings'] if s.get('id') == 'button_link'))
check("scrim element is aria-hidden", 'class="hero__scrim" aria-hidden="true"' in hero)
check("decorative placeholder is aria-hidden", 'hero__image--placeholder" aria-hidden="true"' in hero)
check("section outputs shopify_attributes", '{{ section.shopify_attributes }}' in hero)
check("image alt comes from the asset, never invented", 'alt: img.alt' in hero)
check("eager + high fetchpriority on the LCP image",
      "loading: 'eager'" in hero and "fetchpriority: 'high'" in hero)
check("explicit widths and sizes on image_tag",
      hero.count("widths:") == 2 and hero.count("sizes: '100vw'") == 2)
check("no hand-built CDN URL", 'cdn.shopify.com' not in hero)
check("mobile source has explicit width/height", 'width="{{ img_mobile.width }}"' in hero)
check("surface context class applied", "'hero surface-dark'" in hero)
check("scripture reference unchanged",
      '2 Corinthians 5:7' in hero and hero.count('2 Corinthians') == 2)
extra = set(re.findall(r'\b(?:Corinthians|John|Romans|Psalm|Matthew|Proverbs|Isaiah|Galatians|Ephesians)\b', hero))
check("no scripture other than the approved reference", extra <= {'Corinthians'}, str(sorted(extra)))

print("\n=== TRANSLATION KEYS ===")
def flat(d, pre=''):
    out = {}
    for k, v in d.items():
        out.update(flat(v, pre+k+'.')) if isinstance(v, dict) else out.update({pre+k: v})
    return out
have = set(flat(json.load(open('locales/en.default.json', encoding='utf-8'))))
need = set()
for p in glob.glob('sections/*.liquid')+glob.glob('layout/*.liquid'):
    need |= set(re.findall(r"'([a-z0-9_]+\.[a-z0-9_.]+)'\s*\|\s*t\b", open(p, encoding='utf-8').read()))
check("no missing translation key", not (need - have), str(sorted(need-have) or ''))
check("no 't' filter with a default: parameter", not re.findall(r"\|\s*t:\s*default", hero+layout))
print("     hero uses %d translation keys: its copy is merchant text, not UI chrome"
      % len(re.findall(r"\|\s*t\b", hero)))

print("\n=== CANONICAL TOKENS VS THEME COPY ===")
a = set(re.findall(r'(--[\w-]+)\s*:', strip(open('PHASE-2-DESIGN-TOKENS.css', encoding='utf-8').read())))
b = set(re.findall(r'(--[\w-]+)\s*:', strip(open('assets/design-tokens.css', encoding='utf-8').read())))
check("theme token copy identical to the canonical file", a == b, str(sorted(a ^ b) or ''))

print("\n=== ORIGINAL PROJECT FILES UNTOUCHED ===")
EV = r"C:\Users\TEST\AppData\Local\Temp\claude\C--Users-TEST-OneDrive-Documents-GodSquad-Website\de238d03-508d-43ce-a377-210f71ff0033\scratchpad\audit-evidence"
orig = {r['path']: r['md5'] for r in csv.DictReader(open(EV+'/inventory.tsv', encoding='utf-8'), delimiter='\t')}
mod  = [p for p, h in orig.items() if os.path.exists(p) and hashlib.md5(open(p,'rb').read()).hexdigest() != h]
gone = [p for p in orig if not os.path.exists(p)]
check("tracked originals unmodified (%d files)" % len(orig), not mod and not gone,
      "MODIFIED=%s DELETED=%s" % (mod or 'none', gone or 'none'))

print("\nOVERALL:", "PASS" if ok else "*** FAILURES ABOVE ***")
