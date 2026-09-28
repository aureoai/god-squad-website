# -*- coding: utf-8 -*-
"""Phase 4 theme validation."""
import json, re, io, sys, os, glob, hashlib, csv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
os.chdir(r"C:\Users\TEST\OneDrive\Documents\GodSquad Website")
SEP = os.sep
norm = lambda p: p.replace(SEP, '/')
ok = True

print("=== THEME FILES CREATED ===")
tot = 0
groups = ['layout/*', 'sections/*', 'snippets/*', 'assets/*', 'config/*', 'locales/*', 'templates/*']
for pat in groups:
    for p in sorted(glob.glob(pat)):
        s = os.path.getsize(p); tot += s
        print("  %-44s %9s B" % (norm(p), format(s, ',')))
print("  %-44s %9s B" % ("TOTAL", format(tot, ',')))

print("\n=== JSON AND SCHEMA PARSE ===")
for p in glob.glob('sections/*.json') + glob.glob('templates/*.json') + glob.glob('config/*.json') + glob.glob('locales/*.json'):
    try:
        json.load(open(p, encoding='utf-8')); print("  OK   %s" % norm(p))
    except Exception as e:
        ok = False; print("  FAIL %s -> %s" % (norm(p), e))
for p in glob.glob('sections/*.liquid'):
    m = re.search(r'\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}', open(p, encoding='utf-8').read(), re.S)
    if not m:
        ok = False; print("  FAIL %s -> no schema" % norm(p)); continue
    try:
        s = json.loads(m.group(1))
        print("  OK   %-34s settings=%-3d blocks=%-2d enabled_on=%s"
              % (norm(p), len(s.get('settings', [])), len(s.get('blocks', [])),
                 s.get('enabled_on', {}).get('groups')))
    except Exception as e:
        ok = False; print("  FAIL %s -> %s" % (norm(p), e))

print("\n=== SECTION GROUP RESOLVES ===")
g = json.load(open('sections/header-group.json', encoding='utf-8'))
for key, sec in g['sections'].items():
    f = 'sections/%s.liquid' % sec['type']
    e = os.path.exists(f)
    if not e: ok = False
    print("  %-18s -> %-34s %s" % (key, f, "EXISTS" if e else "*** MISSING ***"))
print("  type=%s  order=%s  order covers all sections: %s"
      % (g['type'], g['order'], set(g['order']) == set(g['sections'])))

print("\n=== SNIPPET AND ASSET REFERENCES RESOLVE ===")
for p in glob.glob('sections/*.liquid') + glob.glob('layout/*.liquid'):
    for name in re.findall(r"\{%-?\s*render\s+'([^']+)'", open(p, encoding='utf-8').read()):
        f = 'snippets/%s.liquid' % name
        e = os.path.exists(f)
        if not e: ok = False
        print("  %-30s renders %-26s %s" % (norm(p), name, "OK" if e else "*** MISSING ***"))
for m in re.findall(r"'([\w.-]+)'\s*\|\s*asset_url", open('layout/theme.liquid', encoding='utf-8').read()):
    f = 'assets/%s' % m
    e = os.path.exists(f)
    if not e: ok = False
    print("  %-30s asset   %-26s %s" % ('layout/theme.liquid', m, "OK" if e else "*** MISSING ***"))

print("\n=== TOKEN FIDELITY ===")
strip = lambda s: re.sub(r'/\*.*?\*/', '', s, flags=re.S)
tok = set(re.findall(r'(--[\w-]+)\s*:', strip(open('assets/design-tokens.css', encoding='utf-8').read())))
body = strip(open('assets/header.css', encoding='utf-8').read())
miss = sorted(u for u in set(re.findall(r'var\((--[\w-]+)', body)) if u not in tok)
if miss: ok = False
print("  tokens available      : %d" % len(tok))
print("  undefined in header.css:", miss or "none")
print("  raw hex               :", re.findall(r'#[0-9A-Fa-f]{3,6}\b', body) or "none")
print("  !important            :", body.count('!important'))
print("  palette layer direct  :", sorted(set(re.findall(r'var\((--gs-[\w-]+)', body))) or "none")

print("\n=== CANONICAL TOKENS VS THEME COPY ===")
ai = set(re.findall(r'(--[\w-]+)\s*:', strip(open('PHASE-2-DESIGN-TOKENS.css', encoding='utf-8').read())))
bi = set(re.findall(r'(--[\w-]+)\s*:', strip(open('assets/design-tokens.css', encoding='utf-8').read())))
if ai != bi: ok = False
print("  canonical %d, theme copy %d, symmetric difference: %s" % (len(ai), len(bi), sorted(ai ^ bi) or "none"))

print("\n=== TRANSLATION KEYS ===")
def flat(d, pre=''):
    out = {}
    for k, v in d.items():
        out.update(flat(v, pre + k + '.')) if isinstance(v, dict) else out.update({pre + k: v})
    return out
have = set(flat(json.load(open('locales/en.default.json', encoding='utf-8'))))
need = set()
for p in glob.glob('sections/*.liquid') + glob.glob('layout/*.liquid'):
    need |= set(re.findall(r"'([a-z0-9_]+\.[a-z0-9_.]+)'\s*\|\s*t\b", open(p, encoding='utf-8').read()))
if need - have: ok = False
print("  defined %d, referenced %d, missing: %s, unused: %s"
      % (len(have), len(need), sorted(need - have) or "none", sorted(have - need) or "none"))

print("\n=== ACCESSIBILITY CONTRACT IN MARKUP ===")
h = open('sections/header.liquid', encoding='utf-8').read()
checks = [
    ("menu trigger is a <button>", '<button' in h and 'data-menu-toggle' in h),
    ("aria-expanded present", 'aria-expanded' in h),
    ("aria-controls matches panel id", 'aria-controls="MobileMenu"' in h and 'id="MobileMenu"' in h),
    ("every icon control has a text label", h.count('visually-hidden') >= 6),
    ("active state from link.active", 'link.active' in h and 'aria-current' in h),
    ("cart count is real, not literal 0", 'cart.item_count' in h),
    ("nav has an accessible name", 'aria-label="{{ \'header.primary_nav\'' in h.replace("'", "'")
        or 'header.primary_nav' in h),
    ("skip link in layout", 'skip-link' in open('layout/theme.liquid', encoding='utf-8').read()),
    ("main landmark in layout", 'id="MainContent"' in open('layout/theme.liquid', encoding='utf-8').read()),
    ("html lang in layout", 'lang="{{ request.locale.iso_code }}"' in open('layout/theme.liquid', encoding='utf-8').read()),
]
for label, passed in checks:
    if not passed: ok = False
    print("  %-40s %s" % (label, "OK" if passed else "*** FAIL ***"))

print("\n=== ORIGINAL PROJECT FILES UNTOUCHED ===")
EV = r"C:\Users\TEST\AppData\Local\Temp\claude\C--Users-TEST-OneDrive-Documents-GodSquad-Website\de238d03-508d-43ce-a377-210f71ff0033\scratchpad\audit-evidence"
orig = {r['path']: r['md5'] for r in csv.DictReader(open(EV + '/inventory.tsv', encoding='utf-8'), delimiter='\t')}
mod = [p for p, hh in orig.items() if os.path.exists(p) and hashlib.md5(open(p, 'rb').read()).hexdigest() != hh]
gone = [p for p in orig if not os.path.exists(p)]
if mod or gone: ok = False
print("  tracked %d   MODIFIED: %s   DELETED: %s" % (len(orig), mod or "none", gone or "none"))

print("\nOVERALL:", "PASS" if ok else "*** FAILURES ABOVE ***")
