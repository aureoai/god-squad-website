# -*- coding: utf-8 -*-
import re, json, io, sys, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = os.path.dirname(os.path.abspath(__file__))
name = sys.argv[1] if len(sys.argv) > 1 else 'probe-dom.html'
d = open(os.path.join(P, name), encoding='utf-8', errors='replace').read()
m = re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
if not m:
    print('NO PAYLOAD')
    print(d[:500])
    raise SystemExit
j = json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
               .replace('&lt;', '<').replace('&gt;', '>'))
json.dump(j, open(os.path.join(P, name.replace('-dom.html', '.json')), 'w'), indent=1)


def w(box):
    return (box[2] - box[0]) if box else 0


def h(box):
    return (box[3] - box[1]) if box else 0


print('%6s %7s %5s %9s %6s %-20s %-20s %-18s %s'
      % ('vw', 'scrollW', 'hscr', 'h1/h2/h3', 'bandH', 'media (w x h)', 'copy col', 'caption', 'heading'))
for k in sorted(j, key=int):
    r = j[k]
    print('%6s %7s %5s %3s/%s/%-3s %6s %-20s %-20s %-18s %s @%s L%s'
          % (k, r['scrollW'], r['hscroll'], r['h1'], r['h2'], r['h3'],
             h(r['band']),
             '%dx%d %s' % (w(r['media']), h(r['media']), r['media'][0] if r['media'] else '-'),
             '%d..%d' % (r['content'][0], r['content'][2]) if r['content'] else '-',
             ('%d..%d' % (r['caption'][0], r['caption'][2])) if r['caption'] else 'not rendered',
             w(r['heading']), r['headingFs'], r['headingLines']))
    if r['overflowing']:
        print('        OVERFLOW:', r['overflowing'][:3])
print()
k = '1440'
if k in j:
    r = j[k]
    print('at 1440:')
    print('  band   ', r['band'])
    print('  media  ', r['media'])
    print('  inner  ', r['inner'])
    print('  content', r['content'])
    print('  caption', r['caption'], 'grid-column-start', r['captionCols'])
    print('  values ', r['values'], 'list', r['valueList'], 'cols', r['valueCols'])
    print('  inner tracks', r['innerCols'])
