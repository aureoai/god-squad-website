# -*- coding: utf-8 -*-
"""Package god-squad-theme/ as a ZIP Shopify will accept.

    python make-theme-zip.py

WHAT SHOPIFY WANTS. The theme's own directories — assets, config, layout,
locales, sections, snippets, templates — at the ROOT of the archive. Zipping the
god-squad-theme folder itself from Explorer produces an archive with one folder
at the root and everything a level down, and Shopify rejects that. This writes
the members at the right depth, so the file it produces can be uploaded as it
stands.

WHAT IT REFUSES TO PACKAGE. Anything outside god-squad-theme/ — brand-assets/,
prototype/, preview-site/ and qa/ are project working files and are not part of
the theme. It also drops OS litter (.DS_Store, Thumbs.db, desktop.ini) and any
editor backup, because Shopify counts every file in the archive against the
theme's file limit and an unknown file at the root can fail validation.

WHAT IT CHECKS BEFORE WRITING. The seven directories a theme needs, the two
files it cannot boot without (layout/theme.liquid and config/settings_schema.json),
the platform's published ceilings — 50 MB compressed, 100,000 files, 256 KB per
Liquid file, 512 KB per JSON template — and that every JSON file parses. A theme
whose settings_schema.json is malformed uploads and then fails to open in the
Theme Editor, which is a confusing way to find out.
"""
import io
import json
import os
import sys
import zipfile

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
QA = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(QA)
THEME = os.path.join(PROJECT, 'god-squad-theme')
OUT = os.path.join(PROJECT, 'god-squad-theme.zip')

# Shopify's published limits, from shopify.dev theme architecture > limits.
MAX_ZIP = 50 * 1024 * 1024
MAX_FILES = 100000
MAX_LIQUID = 256 * 1024
MAX_JSON_TEMPLATE = 512 * 1024

THEME_DIRS = ('assets', 'config', 'layout', 'locales', 'sections', 'snippets',
              'templates')
SKIP_NAMES = {'.DS_Store', 'Thumbs.db', 'desktop.ini'}
SKIP_SUFFIX = ('.orig', '.rej', '.bak', '.swp', '~')


def collect():
    members = []
    for d in THEME_DIRS:
        root = os.path.join(THEME, d)
        if not os.path.isdir(root):
            continue
        for base, _dirs, files in os.walk(root):
            for f in sorted(files):
                if f in SKIP_NAMES or f.endswith(SKIP_SUFFIX):
                    continue
                full = os.path.join(base, f)
                rel = os.path.relpath(full, THEME).replace(os.sep, '/')
                members.append((full, rel))
    return sorted(members, key=lambda m: m[1])


def main():
    if not os.path.isdir(THEME):
        print('*** no theme at %s' % THEME)
        return 2

    problems = []
    for d in THEME_DIRS:
        if not os.path.isdir(os.path.join(THEME, d)):
            problems.append('missing directory: %s/' % d)
    for f in ('layout/theme.liquid', 'config/settings_schema.json'):
        if not os.path.isfile(os.path.join(THEME, f.replace('/', os.sep))):
            problems.append('missing required file: %s' % f)

    members = collect()
    if len(members) > MAX_FILES:
        problems.append('%d files exceeds the %d ceiling' % (len(members), MAX_FILES))

    for full, rel in members:
        size = os.path.getsize(full)
        if rel.endswith('.liquid') and size > MAX_LIQUID:
            problems.append('%s is %d B, over the 256 KB Liquid ceiling' % (rel, size))
        if rel.startswith('templates/') and rel.endswith('.json') and size > MAX_JSON_TEMPLATE:
            problems.append('%s is %d B, over the 512 KB JSON template ceiling' % (rel, size))
        if rel.endswith('.json'):
            try:
                json.load(io.open(full, encoding='utf-8'))
            except ValueError as e:
                problems.append('%s is not valid JSON: %s' % (rel, e))

    if problems:
        print('*** NOT PACKAGED — fix these first:')
        for p in problems:
            print('    - %s' % p)
        return 1

    if os.path.exists(OUT):
        os.remove(OUT)
    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for full, rel in members:
            z.write(full, rel)

    size = os.path.getsize(OUT)
    by_dir = {}
    for _full, rel in members:
        by_dir[rel.split('/')[0]] = by_dir.get(rel.split('/')[0], 0) + 1

    print('  wrote  %s' % OUT)
    print('  size   %.1f KB  (ceiling %d MB)' % (size / 1024.0, MAX_ZIP // (1024 * 1024)))
    print('  files  %d       (ceiling %d)' % (len(members), MAX_FILES))
    print()
    for d in THEME_DIRS:
        print('     %-12s %3d' % (d + '/', by_dir.get(d, 0)))
    print()

    # The archive must open with the theme's own folders at the root. Read it
    # back rather than trusting the write.
    with zipfile.ZipFile(OUT) as z:
        names = z.namelist()
    roots = sorted({n.split('/')[0] for n in names})
    ok = set(roots) <= set(THEME_DIRS)
    print('  archive roots: %s' % ', '.join(roots))
    print('  %s' % ('structure is what Shopify expects — the theme folders are at '
                    'the root, not nested inside one' if ok
                    else '*** WRONG: something other than a theme directory is at the root'))
    if size > MAX_ZIP:
        print('  *** over the 50 MB ceiling')
        return 1
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
