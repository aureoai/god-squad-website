# -*- coding: utf-8 -*-
"""GOD SQUAD Phase 3 — complete asset inventory.

Parses PNG and WebP headers directly (no imaging library is installed and none
is being installed), hashes every file, verifies usage from the source rather
than from filenames, groups exact duplicates, and classifies each asset.

Read-only with respect to the project: writes only to the scratchpad.
"""
import os, re, io, sys, csv, json, struct, hashlib, math, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
PROJECT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__))

MIME = {'png': 'image/png', 'webp': 'image/webp', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
        'svg': 'image/svg+xml', 'txt': 'text/plain', 'js': 'text/javascript',
        'html': 'text/html', 'md': 'text/markdown', 'css': 'text/css', 'csv': 'text/csv',
        'json': 'application/json'}


def png_info(b):
    """width, height, colour mode, alpha — from the IHDR chunk."""
    if b[:8] != b'\x89PNG\r\n\x1a\n':
        return None
    w, h = struct.unpack('>II', b[16:24])
    depth, ctype = b[24], b[25]
    modes = {0: ('Greyscale', False), 2: ('RGB', False), 3: ('Indexed', False),
             4: ('Greyscale+Alpha', True), 6: ('RGBA', True)}
    mode, alpha = modes.get(ctype, ('Unknown', False))
    if ctype == 3 and b.find(b'tRNS') != -1:
        alpha = True
    return w, h, '%s %d-bit' % (mode, depth), alpha


def webp_info(b):
    """width, height, variant, alpha — VP8 / VP8L / VP8X."""
    if b[:4] != b'RIFF' or b[8:12] != b'WEBP':
        return None
    c = b[12:16]
    if c == b'VP8X':
        w = int.from_bytes(b[24:27], 'little') + 1
        h = int.from_bytes(b[27:30], 'little') + 1
        return w, h, 'WebP extended', bool(b[20] & 0x10)
    if c == b'VP8L':
        bits = int.from_bytes(b[21:25], 'little')
        w = (bits & 0x3FFF) + 1
        h = ((bits >> 14) & 0x3FFF) + 1
        return w, h, 'WebP lossless', bool((bits >> 28) & 1)
    if c == b'VP8 ':
        i = b.find(b'\x9d\x01\x2a', 20, 40)
        if i != -1:
            w = int.from_bytes(b[i + 3:i + 5], 'little') & 0x3FFF
            h = int.from_bytes(b[i + 5:i + 7], 'little') & 0x3FFF
            return w, h, 'WebP lossy', False
    return None


def ratio(w, h):
    if not w or not h:
        return ''
    g = math.gcd(w, h)
    a, b = w // g, h // g
    if a > 40 or b > 40:
        return '%.3f:1' % (w / h)
    return '%d:%d (%.3f)' % (a, b, w / h)


os.chdir(PROJECT)
html = open('God Squad Website.html', encoding='utf-8').read()
js = open('support.js', encoding='utf-8').read()
# Every src/url the page actually requests, resolved to a project-relative path.
refs = set()
for m in re.finditer(r'(?:src|href)="([^"{}]+)"', html):
    v = m.group(1).lstrip('./')
    if not v.startswith(('http', '#', 'mailto')):
        refs.add(v)
for m in re.finditer(r"img:\s*'([^']+)'|icon:\s*'([^']+)'", html):
    refs.add((m.group(1) or m.group(2)).lstrip('./'))

PHASE_FILES = {'PHASE-0-PROJECT-FOUNDATION.md', 'PHASE-1-WEBSITE-AUDIT.md',
               'PHASE-2-DESIGN-SYSTEM.md', 'PHASE-2-DESIGN-TOKENS.css',
               'PHASE-3-ASSET-SYSTEM.md', 'PHASE-3-ASSET-MANIFEST.csv'}

rows = []
for dp, dn, fn in os.walk('.'):
    parts = dp.replace(os.sep, '/').split('/')
    if '.claude' in parts or 'phase-3-assets' in parts:
        continue
    for f in sorted(fn):
        p = '/'.join([x for x in parts if x not in ('.', '')] + [f])
        b = open(p, 'rb').read()
        ext = (os.path.splitext(f)[1].lower().lstrip('.') or f.lstrip('.'))
        info = png_info(b) if ext == 'png' else (webp_info(b) if ext in ('webp', 'thumbnail') else None)
        if info is None and ext == 'thumbnail':
            info = webp_info(b)
        w, h, mode, alpha = info if info else ('', '', '', '')
        rows.append(dict(
            path=p, filename=f, folder=(os.path.dirname(p) or '(root)'), ext=ext,
            mime=MIME.get(ext, 'application/octet-stream'),
            bytes=len(b), width=w, height=h, ratio=ratio(w, h) if info else '',
            mode=mode, alpha=('yes' if alpha else ('no' if info else '')),
            md5=hashlib.md5(b).hexdigest(), sha256=hashlib.sha256(b).hexdigest()[:16],
            referenced=('yes' if p in refs else 'no'),
            is_phase_doc=(f in PHASE_FILES)))

# duplicate groups by md5
groups = collections.defaultdict(list)
for r in rows:
    groups[r['md5']].append(r['path'])
gid, n = {}, 0
for md5, paths in sorted(groups.items(), key=lambda kv: min(kv[1])):
    if len(paths) > 1:
        n += 1
        for p in paths:
            gid[p] = 'DUP-%02d' % n
for r in rows:
    r['dup_group'] = gid.get(r['path'], '')

# canonical member of each duplicate group: prefer a referenced file, then images/, then shortest path
canon = {}
for md5, paths in groups.items():
    if len(paths) < 2:
        continue
    ranked = sorted(paths, key=lambda p: (p not in refs, not p.startswith('images/'), len(p)))
    canon[gid[ranked[0]]] = ranked[0]
for r in rows:
    r['canonical'] = canon.get(r['dup_group'], '') if r['dup_group'] else ''

json.dump(rows, open(HERE + '/inventory-raw.json', 'w', encoding='utf-8'), indent=1)

print("=== PHASE 3 ASSET INVENTORY ===")
print("files scanned            : %d" % len(rows))
print("total bytes              : %s" % format(sum(r['bytes'] for r in rows), ','))
imgs = [r for r in rows if r['ext'] in ('png', 'webp', 'thumbnail')]
print("image files              : %d (%s bytes)" % (len(imgs), format(sum(r['bytes'] for r in imgs), ',')))
print("referenced by the page   : %d" % sum(1 for r in rows if r['referenced'] == 'yes'))
print("phase documents (not assets): %d" % sum(1 for r in rows if r['is_phase_doc']))
print("duplicate groups         : %d covering %d files" % (n, sum(1 for r in rows if r['dup_group'])))
print("\n=== PARSED DIMENSIONS (header-derived, no imaging library) ===")
bad = [r for r in imgs if not r['width']]
print("images whose header could not be parsed: %s" % ([r['path'] for r in bad] or 'none'))
print("\n%-52s %-11s %-18s %-16s %s" % ("path", "dims", "ratio", "mode", "alpha"))
for r in sorted(imgs, key=lambda r: r['path']):
    print("%-52s %-11s %-18s %-16s %s" % (r['path'][:52], '%sx%s' % (r['width'], r['height']),
                                          r['ratio'][:18], r['mode'][:16], r['alpha']))
print("\n=== DUPLICATE GROUPS (canonical first) ===")
for g in sorted(set(x for x in gid.values())):
    members = [r for r in rows if r['dup_group'] == g]
    c = canon[g]
    print("  %s  canonical: %s  (%s bytes)" % (g, c, format(members[0]['bytes'], ',')))
    for m in members:
        if m['path'] != c:
            print("        duplicate: %s" % m['path'])
print("\n=== REFERENCED BY THE PAGE ===")
for r in sorted(rows, key=lambda r: r['path']):
    if r['referenced'] == 'yes':
        print("  %-46s %9s B  %s" % (r['path'][:46], format(r['bytes'], ','), '%sx%s' % (r['width'], r['height'])))
print("\nwrote inventory-raw.json")
