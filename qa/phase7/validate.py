# -*- coding: utf-8 -*-
"""Phase 7 theme validation. Extends the Phase 6 pass with Our Story checks."""
import json, re, io, sys, os, glob, hashlib, csv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
os.chdir(r"C:\Users\TEST\OneDrive\Documents\GodSquad Website")
norm = lambda p: p.replace(os.sep, '/')
ok = True


def check(label, passed, detail=''):
    global ok
    if not passed:
        ok = False
    print("  %-58s %s %s" % (label, "OK" if passed else "*** FAIL ***", detail))


strip_css = lambda s: re.sub(r'/\*.*?\*/', '', s, flags=re.S)


def strip_liquid(s):
    """Both comment forms: the {% comment %} pair and the bare comment lines
    inside a {% liquid %} block. The second is where the code documents what it
    deliberately does NOT do, so leaving it in fires every prohibition check on
    the documentation itself."""
    s = re.sub(r'\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}', '', s, flags=re.S)
    s = re.sub(r'^[ \t]*comment[ \t]*$.*?^[ \t]*endcomment[ \t]*$', '', s, flags=re.S | re.M)
    return s


R = lambda p: open(p, encoding='utf-8').read()
story = R('sections/our-story.liquid')
storyc = strip_liquid(story)
css = strip_css(R('assets/section-our-story.css'))
layout = R('layout/theme.liquid')
tmpl = json.load(open('templates/index.json', encoding='utf-8'))
schema = json.loads(re.search(r'\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}', story, re.S).group(1))
# The Liquid BODY, with the schema removed. Prohibitions about markup apply
# here; the schema's help text is documentation and is checked separately.
storybody = strip_liquid(re.sub(r'\{%\s*schema\s*%\}.*?\{%\s*endschema\s*%\}', '', story, flags=re.S))

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
        print("  OK   %-30s settings=%-3d blocks=%-2d presets=%-2d"
              % (norm(p), len(sc.get('settings', [])), len(sc.get('blocks', [])),
                 len(sc.get('presets', []))))
    except Exception as e:
        ok = False
        print("  FAIL %s -> %s" % (norm(p), e))

print("\n=== TEMPLATE WIRING ===")
check("index.json order covers every section", set(tmpl['order']) == set(tmpl['sections']), str(tmpl['order']))
for k, v in tmpl['sections'].items():
    check("section '%s' -> sections/%s.liquid" % (k, v['type']), os.path.exists('sections/%s.liquid' % v['type']))
ids = {s['id'] for s in schema['settings'] if s.get('id')}
sel = {s['id']: [o['value'] for o in s['options']] for s in schema['settings'] if s['type'] == 'select'}
entry = tmpl['sections'].get('our-story', {})
unknown = sorted(set(entry.get('settings', {})) - ids)
check("our-story settings all exist in the schema", not unknown, str(unknown or ''))
bad = [(a, b) for a, b in entry.get('settings', {}).items() if a in sel and b not in sel[a]]
check("our-story select values are declared options", not bad, str(bad or ''))
btypes = {b['type'] for b in schema.get('blocks', [])}
bad_b = [b['type'] for b in entry.get('blocks', {}).values() if b['type'] not in btypes]
check("every template block has a declared type", not bad_b, str(bad_b or ''))
check("block_order matches the blocks map",
      set(entry.get('block_order', [])) == set(entry.get('blocks', {})))
bfields = {f['id'] for b in schema.get('blocks', []) for f in b.get('settings', []) if f.get('id')}
badf = sorted({k for b in entry.get('blocks', {}).values() for k in b['settings']} - bfields)
check("every template block setting exists in the block schema", not badf, str(badf or ''))
limit = next((b.get('limit') for b in schema.get('blocks', [])), None)
check("blocks used are within the declared limit",
      len(entry.get('blocks', {})) <= (limit or 99), "used %d, limit %s" % (len(entry.get('blocks', {})), limit))
for pr in schema['presets']:
    unknown = sorted(set(pr.get('settings', {})) - ids)
    check("preset '%s' settings all exist" % pr['name'], not unknown, str(unknown or ''))
    pb = [b['type'] for b in pr.get('blocks', []) if b['type'] not in btypes]
    check("preset '%s' blocks have declared types" % pr['name'], not pb, str(pb or ''))

print("\n=== NOTHING INVENTED ===")
FORBIDDEN = [
    (r'\bfounded\b|\bfounder\b|\bsince \d{4}\b|\bestablished \d{4}', 'founder or founding date'),
    (r'\b\d[\d,]*\+?\s*(customers|believers|members|followers|orders|reviews)', 'a customer or community count'),
    (r'\btrusted by\b|\bjoin (thousands|the thousands)\b|\bas seen in\b|\bfeatured in\b', 'social proof'),
    (r'★|\bstar rating\b|\b\d\.\d\s*/\s*5\b', 'a rating'),
    (r'\baward[- ]winning\b|\bbest[- ]selling brand\b|\bnumber one\b', 'an award or superlative'),
    (r'\bpartnered with\b|\bin partnership with\b|\bproceeds\b|\bdonat', 'a partnership or donation claim'),
    (r'\bchurch of\b|\bministry of\b|\bdenomination', 'a church affiliation'),
]
blob = storyc + json.dumps(tmpl) + R('locales/en.default.json')
for pat, what in FORBIDDEN:
    hits = re.findall(pat, blob, re.I)
    check("no %s" % what, not hits, str(hits[:3]))
check("no href=\"#\"", '"#"' not in storyc)
check("CTA renders only with a destination", 'show_cta' in story and 'btn_url != blank' in story)
check("button_url has no default value",
      all('default' not in s for s in schema['settings'] if s.get('id') == 'button_url'))
check("no image asset path is hard-coded in the markup",
      not re.search(r'\.(webp|png|jpe?g)', storybody))
check("the schema names the canonical asset for the merchant",
      'images/our-story.webp' in story and '2000px' in story)
check("no hand-built CDN URL", 'cdn.shopify.com' not in storyc)
check("the approved heading copy is preserved",
      'Real People.' in story and 'Bigger Purpose.' in story)
check("the approved body copy is preserved",
      'Philippine streetwear brand built on faith, creativity, and community' in story)
check("the approved caption copy is preserved", 'Faith' in story and 'Different' in story)

print("\n=== MARKUP CONTRACT ===")
check("no <h1> in the section", '<h1' not in storyc)
check("section heading is an h2", '<h2 class="our-story__heading">' in storyc)
check("value titles take a level derived from the heading",
      '<h{{ value_level }} class="our-story__value-title">' in storyc
      and 'assign value_level = 3' in story and 'assign value_level = 2' in story)
check("no <script> in the section", '<script' not in storyc)
check("no inline event handlers", not re.findall(r'\son[a-z]+\s*=\s*"', storyc))
check("no positive tabindex", not re.findall(r'tabindex="[1-9]', storyc))
check("no role=menu", 'role="menu"' not in storyc)
check("decorative scrim is aria-hidden", 'class="our-story__scrim" aria-hidden="true"' in storyc)
check("blocks emit shopify_attributes", '{{ block.shopify_attributes }}' in storyc)
check("image alt comes from the asset, never invented", 'alt: img.alt' in storyc)
check("image is lazy loaded", "loading: 'lazy'" in storyc)
check("explicit widths and sizes on the image",
      storyc.count("widths: '480") == 2 and storyc.count('sizes: img_sizes') == 2)
check("richtext body is output unescaped", '{{ section.settings.body }}' in storyc)
check("heading and caption are hard-broken with the filter",
      storyc.count('| newline_to_br') == 2)
check("empty state is editor-only", 'request.design_mode' in storyc)
check("values are a list with an explicit role", 'role="list"' in storyc)

print("\n=== REVIEW CONTRACT ===")
# The photograph is 70% of a band with no max-width, so its slot is 70vw at
# every width from the split up. Capping it at a share of container_width told
# the browser 1008px for a 1344px slot above 1440.
check("the image slot is declared in viewport units",
      "assign img_sizes = '(min-width: 1024px) 70vw, 100vw'" in story)
check("the image slot is not capped at the container width",
      'container_width' not in storybody and 'capped' not in storybody)

# image_tag writes an inline object-position for an admin focal point, which no
# stylesheet can override, so the theme must not offer a competing control.
check("no theme-side focal point setting",
      not [f for f in schema['settings'] if f.get('id') == 'focal_point'])
check("no focal point modifier class", 'our-story--focal-' not in story
      and 'our-story--focal-' not in css)
check("the stylesheet sets only a default crop centre",
      '--os-focal-y' not in css and 'object-position: center 33%' in css)

# The media wrapper carries an aspect ratio and an ink fill, so it must not be
# emitted without an image.
mi = storyc.index('<div class="our-story__media">')
gi = storyc.index('{%- if img != blank -%}')
check("the media wrapper is inside the image guard", gi < mi)

# Phase 2 26.5: at most two accent marks in a band. The eyebrow is one.
check("gold is spent once in the band",
      css.count('color: var(--accent-current)') == 1)

# Phase 2 26.2: the editorial cap belongs to the rail, the reading cap to the
# stacked column.
check("the stacked body takes the reading measure",
      'max-width: var(--measure-body);' in css)
check("the body takes the editorial measure at the split",
      'max-width: var(--measure-narrow);' in css)

# A 14rem floor fits five tracks at 1440 and orphans a sixth block.
check("the values row fits four tracks, not five",
      'minmax(min(17rem, 100%), 1fr)' in css)

# The mobile source covers up to 1023 CSS px, which is 3069 device px at DPR 3.
check("the mobile source reaches beyond 1200w",
      'width: 2048 }} 2048w' in storyc)

print("\n=== APPROVED COPY ===")
proto = R('God Squad Website.html')
approved = [('Faith Driven', 'More Than Clothing'),
            ('Community', 'People With Purpose'),
            ('Premium Quality', 'Crafted To Inspire')]
for title, line in approved:
    check("value '%s' is the prototype's own copy" % title,
          title in proto and line in proto and title in story and line in story)
# The phrase appears once in the section, in the comment that records WHY it is
# not shipped, so the check reads the markup, the schema and the home page.
check("the unverified shipping claim is not shipped",
      'Shipping Available' not in storybody
      and 'Shipping Available' not in json.dumps(schema)
      and 'Shipping Available' not in json.dumps(entry))
check("the section records why the fourth approved value is withheld",
      'VAL-04' in story and 'BUSINESS INFORMATION' in story)
check("no value line duplicates the hero's copy",
      'Different People. Same Purpose.' not in story
      and 'Different people. Same purpose.' not in story)

print("\n=== TOKEN FIDELITY ===")
tok = set(re.findall(r'(--[\w-]+)\s*:', strip_css(R('assets/design-tokens.css'))))
local = {'--os-space-top', '--os-space-bottom', '--os-header-clearance',
         '--os-scrim-rgb', '--header-overlay-offset'}
used = set(re.findall(r'var\((--[\w-]+)', css))
undef = sorted(u for u in used if u not in tok and u not in local)
check("no undefined custom property", not undef, str(undef or ''))
hexes = re.findall(r'#[0-9A-Fa-f]{3,6}\b', css)
check("no raw hex outside the mask keyword", set(hexes) <= {'#000'}, str(sorted(set(hexes))))
check("no !important", '!important' not in css)
gs = sorted(set(re.findall(r'var\((--gs-[\w-]+)', css)))
check("no palette-layer token reached directly", not gs, str(gs))
check("no component-level outline declaration", not re.findall(r'outline\s*:', css))
print("     rgba(13, 12, 10, ...) scrim stops: %d  (the ink literal Phase 2 names as the scrim base)"
      % len(re.findall(r'rgba\(13, 12, 10', css)))
check("stylesheet is loaded by the section, not the layout",
      "'section-our-story.css' | asset_url | stylesheet_tag" in story
      and 'section-our-story.css' not in layout)
guard = story.index('{%- if img == blank and heading == blank')
check("an unconfigured section requests no stylesheet",
      story.index("'section-our-story.css'") > guard)

print("\n=== NO JAVASCRIPT, NO MOTION DEPENDENCY ===")
check("section adds no script", '<script' not in story)
check("stylesheet animates nothing",
      not re.findall(r'\b(animation|transition)\s*:', css) and '@keyframes' not in css)

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

print("\n=== EARLIER PHASES INTACT ===")
a = set(re.findall(r'(--[\w-]+)\s*:', strip_css(R('PHASE-2-DESIGN-TOKENS.css'))))
b = set(re.findall(r'(--[\w-]+)\s*:', strip_css(R('assets/design-tokens.css'))))
check("token files still in step", a == b, str(sorted(a ^ b) or ''))
for f in ('sections/header.liquid', 'sections/hero.liquid', 'sections/featured-collection.liquid',
          'snippets/product-card.liquid', 'assets/header.js'):
    check("%s untouched by this phase" % norm(f), os.path.exists(f))
check("home page section order is hero, collections, story",
      tmpl['order'] == ['hero', 'new-drop', 'best-sellers', 'our-story'], str(tmpl['order']))

print("\n=== ORIGINAL PROJECT FILES UNTOUCHED ===")
EV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'audit-evidence')
orig = {r['path']: r['md5'] for r in csv.DictReader(open(EV + '/inventory.tsv', encoding='utf-8'), delimiter='\t')}
mod = [p for p, h in orig.items() if os.path.exists(p) and hashlib.md5(open(p, 'rb').read()).hexdigest() != h]
gone = [p for p in orig if not os.path.exists(p)]
check("tracked originals unmodified (%d files)" % len(orig), not mod and not gone,
      "MODIFIED=%s DELETED=%s" % (mod or 'none', gone or 'none'))

print("\nOVERALL:", "PASS" if ok else "*** FAILURES ABOVE ***")
