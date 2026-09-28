# -*- coding: utf-8 -*-
"""Harvest every operational requirement the theme states about itself.

Two structural critics independently reached the same conclusion about the
consolidated manual: it documents the theme and omits the STORE. The knowledge an
integrator needs is not missing from the project — it is scattered through schema
`info` strings, `paragraph` blocks, locale strings and section comments, which is
exactly the form in which nobody can follow it as a sequence.

This collects it deterministically so the runbook is built from what the theme
actually says, not from memory:

  1. Every setting a merchant must fill for a surface to render anything, with
     the section it belongs to and whether it has a default.
  2. Every `info`/`paragraph` string that states a dependency, a requirement or
     a consequence — the ones containing must/need/require/before/otherwise/
     empty/nothing/won't/will not.
  3. Every setting whose absence makes a built surface render NOTHING, which is
     the failure an integrator hits first and understands last.
  4. The app dependencies and platform choices named anywhere in the theme.
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
REQUIRE = re.compile(
    r'\b(must|need|needs|required|require|requires|before you|before the|'
    r'otherwise|nothing is shown|nothing shows|does not render|will not render|'
    r'renders nothing|no .{0,20} exists|until |install|enable|configure|'
    r'BUSINESS INFORMATION)\b', re.I)


def schemas():
    """Yield (file, schema dict) for every section and the theme settings."""
    sec = os.path.join(THEME, 'sections')
    for f in sorted(os.listdir(sec)):
        if not f.endswith('.liquid'):
            continue
        s = io.open(os.path.join(sec, f), encoding='utf-8').read()
        m = re.search(r'\{%-?\s*schema\s*-?%\}(.*?)\{%-?\s*endschema', s, re.S)
        if not m:
            continue
        try:
            yield ('sections/' + f, json.loads(m.group(1)))
        except ValueError:
            pass
    p = os.path.join(THEME, 'config', 'settings_schema.json')
    try:
        yield ('config/settings_schema.json', json.load(io.open(p, encoding='utf-8')))
    except ValueError:
        pass


def walk_settings(node, out, where):
    """Collect every setting dict, wherever it is nested."""
    if isinstance(node, dict):
        if 'type' in node and ('id' in node or node['type'] in ('header', 'paragraph')):
            out.append((where, node))
        for v in node.values():
            walk_settings(v, out, where)
    elif isinstance(node, list):
        for v in node:
            walk_settings(v, out, where)


rows = []
for where, doc in schemas():
    got = []
    walk_settings(doc, got, where)
    rows += got

print('=== SETTINGS WITH NO DEFAULT (a surface may render nothing until filled) ===')
nodefault = []
for where, s in rows:
    if s.get('type') in ('header', 'paragraph'):
        continue
    if not s.get('id'):
        continue
    if 'default' in s:
        continue
    if s.get('type') in ('image_picker', 'link_list', 'collection', 'product',
                         'page', 'blog', 'url', 'text', 'richtext', 'html',
                         'inline_richtext', 'menu', 'collection_list',
                         'product_list', 'video', 'video_url', 'article',
                         'font_picker', 'color', 'color_background'):
        nodefault.append((where, s))
print('  %-34s %-26s %s' % ('section', 'setting id', 'type'))
for where, s in nodefault:
    print('  %-34s %-26s %s' % (where.replace('sections/', ''), s['id'], s['type']))
print('  -> %d setting(s)' % len(nodefault))

print()
print('=== INFO / PARAGRAPH STRINGS THAT STATE A REQUIREMENT ===')
reqs = []
for where, s in rows:
    for key in ('info', 'content', 'label'):
        v = s.get(key)
        if isinstance(v, str) and REQUIRE.search(v) and len(v) > 40:
            reqs.append((where, s.get('id') or s.get('type'), key, ' '.join(v.split())))
seen = set()
for where, sid, key, v in reqs:
    k = v[:80]
    if k in seen:
        continue
    seen.add(k)
    print('  [%s / %s]' % (where.replace('sections/', ''), sid))
    print('      %s' % v[:300])
print('  -> %d requirement string(s)' % len(seen))

print()
print('=== APP / PLATFORM DEPENDENCIES NAMED IN THE THEME ===')
NEEDLES = ['Search & Discovery', 'Search and Discovery', 'shopify-account',
           'customer account', 'payment_button', 'Shop Pay', 'metafield',
           'Markets', 'locale', 'inventory', 'option_value', 'swatch']
hits = {}
for root, _d, fs in os.walk(THEME):
    for f in sorted(fs):
        if not f.endswith(('.liquid', '.json', '.js')):
            continue
        p = os.path.join(root, f)
        rel = os.path.relpath(p, THEME).replace(os.sep, '/')
        t = io.open(p, encoding='utf-8', errors='replace').read()
        for n in NEEDLES:
            if n.lower() in t.lower():
                hits.setdefault(n, []).append(rel)
for n, files in sorted(hits.items()):
    print('  %-24s %d file(s): %s' % (n, len(files), ', '.join(files[:4])))

print()
print('=== LOCALE STRINGS SHOWN WHEN SOMETHING IS UNCONFIGURED ===')
loc = json.load(io.open(os.path.join(THEME, 'locales', 'en.default.json'),
                        encoding='utf-8'))


def leaves(o, p=''):
    if isinstance(o, dict):
        for k, v in o.items():
            for r in leaves(v, p + '.' + k if p else k):
                yield r
    elif isinstance(o, str):
        yield (p, o)


n = 0
for k, v in leaves(loc):
    if REQUIRE.search(v) or re.search(r'\bempty\b|\bno results\b|\bnothing\b', v, re.I):
        print('  %-44s %s' % (k, ' '.join(v.split())[:90]))
        n += 1
print('  -> %d string(s)' % n)
