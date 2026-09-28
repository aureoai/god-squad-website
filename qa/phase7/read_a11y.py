# -*- coding: utf-8 -*-
import re, json, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
P = os.path.dirname(os.path.abspath(__file__))
d = open(os.path.join(P, 'a11y-dom.html'), encoding='utf-8', errors='replace').read()
m = re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
if not m:
    print('NO PAYLOAD')
    print(d[:400])
    raise SystemExit
j = json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
               .replace('&lt;', '<').replace('&gt;', '>'))
json.dump(j, open(os.path.join(P, 'a11y.json'), 'w'), indent=1)

print('positive tabindex anywhere on the page:', j['positiveTabindex'],
      '(must be 0: any positive value breaks DOM tab order)')
print()
print('HEADING OUTLINE')
for h in j['headings']:
    lvl = int(h[1])
    print('  ' + '  ' * (lvl - 1) + h)
levels = [int(h[1]) for h in j['headings']]
skips = [(levels[i], levels[i + 1]) for i in range(len(levels) - 1) if levels[i + 1] - levels[i] > 1]
print('  h1 count:', levels.count(1), ' skipped levels:', skips or 'none')
print()
print('TAB ORDER (%d focusable elements)' % len(j['order']))
for i, e in enumerate(j['order'], 1):
    print('  %2d. <%s> %-34s %s' % (i, e['tag'], e['cls'], e['name'][:56]))
print()
print('PRODUCT LINK ACCESSIBLE NAMES')
for l in j['links']:
    print('  alt=%-28r name=%r' % (l['alt'], l['name']))
print()
print('MOTION', j['motion'])
print()
print('INTERACTIVE TARGET SIZES (SC 2.5.8 needs 24x24)')
bad = 0
for t in j['targets']:
    okk = t['w'] >= 24 and t['h'] >= 24
    if not okk:
        bad += 1
    print('  %-32s %4d x %-4d %s' % (t['cls'], t['w'], t['h'], 'ok' if okk else '*** UNDER 24 ***'))
print('  under-size targets:', bad)
