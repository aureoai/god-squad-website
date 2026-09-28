# -*- coding: utf-8 -*-
"""Generate contrast8's probe pages and LEAVE them on disk.

Edge's --dump-dom has stopped producing output in this environment. The four QA
suites that depend on it -- contrast8, editor, cardcascade, facetsgate -- all
report NO READING, and they are exactly the four that use it; every suite that
avoids it still passes. So the browser is the problem, not the theme (confirmed
by reverting the only theme change and watching contrast8 fail identically).

contrast8 writes a probe page per surface, launches Edge to read the payload out
of it, and then DELETES the page (contrast8.py:248). That cleanup is why the
pages cannot simply be opened afterwards.

This reuses contrast8's own PROBE template and role lists -- so the measurement
is identical, not a re-implementation -- writes every probe page, and stops. The
payloads are then read through the Browser pane, which works, restoring the 73
contrast measurements that would otherwise be dark.
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
P8 = os.path.abspath(os.path.join(HERE, '..', 'phase8'))
sys.path.insert(0, P8)

import contrast8 as c8   # noqa: E402  (module-level PROBE and ROLES_* only)

SITE = c8.SITE

JOBS = [
    ('p-details.html', c8.ROLES_PRODUCT, False, 'product, cream'),
    ('p-ink.html', c8.ROLES_PRODUCT, False, 'product, ink'),
    ('c-many.html', c8.ROLES_CART, True, 'drawer, ink'),
    ('c-empty.html', c8.ROLES_EMPTY, True, 'drawer empty, ink'),
    ('c-page-many.html', c8.ROLES_CART_PAGE, False, 'cart page, ink'),
    ('c-noted.html', c8.ROLES_NOTE, True, 'order note, drawer ink'),
    ('c-page-note.html', c8.ROLES_NOTE + c8.ROLES_CART_PAGE, False,
     'order note, cart page ink'),
    ('p-nodrawer.html', c8.ROLES_CONFIRM, False, 'add confirmation, cream'),
    ('p-rule.html', [('price, current', '.price__current'),
                     ('price, unit', '.price__unit')], False, 'unit price, cream'),
]

written = []
for page, roles, open_drawer, tag in JOBS:
    if not os.path.exists(os.path.join(SITE, page)):
        print('  skip (no fixture): %s' % page)
        continue
    name = '_contrast-%s.html' % re.sub(r'[^a-z0-9]+', '-', (page + tag).lower())
    body = (c8.PROBE.replace('SRC', page)
            .replace('ROLESJSON', json.dumps(roles))
            .replace('OPENFLAG', 'true' if open_drawer else 'false'))
    io.open(os.path.join(SITE, name), 'w', encoding='utf-8').write(body)
    written.append({'probe': name, 'page': page, 'tag': tag, 'roles': len(roles)})
    print('  wrote %-52s (%s, %d roles)' % (name, tag, len(roles)))

io.open(os.path.join(HERE, 'contrast-probes.json'), 'w', encoding='utf-8').write(
    json.dumps(written, indent=1))
print()
print('%d probe page(s) written and LEFT in place.' % len(written))
print('Read each at http://127.0.0.1:8808/<probe> and pull the payload from')
print('the <pre id="o"> element.')
