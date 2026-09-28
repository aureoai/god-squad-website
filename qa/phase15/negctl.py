# -*- coding: utf-8 -*-
"""Phase 15 — negative control for accounts.py.

accounts.py is mostly a list of things the theme must NOT contain, and an
absence assertion that has never been seen to fail is indistinguishable from a
typo in a regex. This seeds each violation into a throwaway COPY of the theme,
one at a time, and requires the suite to catch it.

A violation the suite does not catch is reported as UNGUARDED — which is the
real output of this file.
"""
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
def write(root, rel, text):
    p = os.path.join(root, rel.replace('/', os.sep))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, 'w', encoding='utf-8').write(text)


def edit(root, rel, old, new):
    p = os.path.join(root, rel.replace('/', os.sep))
    s = io.open(p, encoding='utf-8').read()
    assert old in s, 'seed anchor missing in %s' % rel
    io.open(p, 'w', encoding='utf-8').write(s.replace(old, new, 1))


# Each violation: (name, seeder, substring of the check label that must fail)
VIOLATIONS = [
    ('a legacy customer template is shipped',
     lambda r: write(r, 'templates/customers/account.json', '{"sections":{}}'),
     'templates/customers/ does not exist'),

    ('all seven legacy templates are shipped',
     lambda r: [write(r, 'templates/customers/%s.json' % n, '{"sections":{}}')
                for n in ('account', 'activate_account', 'addresses', 'login',
                          'order', 'register', 'reset_password')],
     'none of the seven legacy templates is shipped'),

    ('a section was written for a legacy template',
     lambda r: write(r, 'sections/main-account.liquid', '<div>account</div>'),
     'and no section was written for one'),

    ('a customer field is printed in a shared snippet',
     lambda r: edit(r, 'snippets/cart-totals.liquid', '<dl class="cart-totals">',
                    '<p>{{ customer.email }}</p>\n<dl class="cart-totals">'),
     'no customer field is ever printed'),

    ('a customer field is read without printing it',
     lambda r: edit(r, 'sections/header.liquid', '{%- liquid',
                    '{%- liquid\n  assign who = customer.first_name'),
     'no customer field is read at all'),

    ('an order field is read',
     lambda r: edit(r, 'snippets/cart-totals.liquid', '<dl class="cart-totals">',
                    '<p>{{ order.total_price | money }}</p>\n<dl class="cart-totals">'),
     'no order object is read'),

    ('a tracking field is read',
     lambda r: edit(r, 'snippets/cart-totals.liquid', '<dl class="cart-totals">',
                    '<p>{{ line_item.fulfillment.tracking_number }}</p>\n<dl class="cart-totals">'),
     'no fulfillment or tracking field is read'),

    ('an account URL is built by hand',
     lambda r: edit(r, 'sections/footer.liquid', '<footer class=',
                    '<a href="/account/orders/abc">Orders</a>\n<footer class='),
     'no account or order URL is constructed by hand'),

    ('an order-status URL is built',
     lambda r: edit(r, 'snippets/cart-totals.liquid', '<dl class="cart-totals">',
                    '<a href="{{ order.order_status_url }}">Track</a>\n<dl class="cart-totals">'),
     'no order-status or authenticate URL is built'),

    ('the theme links an account route directly again',
     lambda r: edit(r, 'sections/footer.liquid', '<footer class=',
                    '<a href="{{ routes.account_login_url }}">Log in</a>\n<footer class='),
     'links no account route directly'),

    ('a customer form tag is used',
     lambda r: write(r, 'sections/main-login.liquid',
                     "{% form 'customer_login' %}<input name=\"customer[email]\">{% endform %}"),
     'no customer form tag anywhere'),

    ('robots.txt.liquid is added',
     lambda r: write(r, 'templates/robots.txt.liquid', 'User-agent: *'),
     'no robots.txt.liquid'),

    ('customer data is put in localStorage',
     lambda r: edit(r, 'assets/cart.js', "(function () {\n  'use strict';",
                    "(function () {\n  'use strict';\n  localStorage.setItem('email', 'x');"),
     'no localStorage anywhere'),

    ('a console log is left in',
     lambda r: edit(r, 'assets/cart.js', "(function () {\n  'use strict';",
                    "(function () {\n  'use strict';\n  console.log('cart');"),
     'nothing is logged that could carry customer data'),

    ('a descendant selector reaches into the component',
     lambda r: edit(r, 'assets/header.css', '.header__account-avatar {',
                    'shopify-account.header__control .account-sheet__row { color: red; }\n\n.header__account-avatar {'),
     'every rule targets the element itself'),

    ('the control loses the shared header-control class',
     lambda r: edit(r, 'sections/header.liquid',
                    'class="header__control header__account"',
                    'class="header__account"'),
     'the control carries the shared header-control class'),

    ('a dead :not(:defined) rule is reintroduced',
     lambda r: edit(r, 'assets/header.css', '.header__account-avatar {',
                    'shopify-account.header__control:not(:defined) { width: 44px; }\n\n.header__account-avatar {'),
     'no dead :not(:defined) rule was left behind'),

    ('the token mapping is removed',
     lambda r: edit(r, 'assets/header.css',
                    '--shopify-account-color-background: var(--color-bg-primary);',
                    ''),
     'through the published custom properties'),

    ('the account control loses its accessible name',
     lambda r: edit(r, 'sections/header.liquid',
                    """            <span class="visually-hidden">{{ 'header.account' | t }}</span>\n""", ''),
     'the name comes from the locale file'),

    ('the menu setting is removed',
     lambda r: edit(r, 'config/settings_schema.json', '"id": "customer_account_menu"',
                    '"id": "customer_account_menu_REMOVED"'),
     'a global customer_account_menu setting exists'),

    ('the menu setting becomes a free-text field',
     lambda r: edit(r, 'config/settings_schema.json',
                    '"type": "link_list",\n        "id": "customer_account_menu"',
                    '"type": "text",\n        "id": "customer_account_menu"'),
     'it is a link_list'),

    ('the component gate is dropped',
     lambda r: edit(r, 'sections/header.liquid',
                    '{%- if shop.customer_accounts_enabled and section.settings.show_account -%}\n        <shopify-account',
                    '{%- if section.settings.show_account -%}\n        <shopify-account'),
     'gated on the platform flag'),
]


def run_suite(root):
    env = dict(os.environ, GS_THEME=root, PYTHONIOENCODING='utf-8')
    out = subprocess.run([sys.executable, os.path.join(HERE, 'accounts.py')],
                         capture_output=True, text=True, encoding='utf-8',
                         errors='replace', env=env).stdout
    return [re.sub(r'\s+', ' ', l.split('*** FAIL ***')[0]).strip()
            for l in out.splitlines() if '*** FAIL ***' in l]


if __name__ == '__main__':
    print('=== EVERY ABSENCE ASSERTION, SEEN TO FAIL ===')
    print()
    unguarded = []
    for name, seed, expect in VIOLATIONS:
        root = tempfile.mkdtemp(prefix='gs15-')
        shutil.rmtree(root)
        shutil.copytree(THEME, root)
        try:
            seed(root)
            failed = run_suite(root)
            caught = any(expect.lower() in f.lower() for f in failed)
            print('  %-52s %s' % (name, 'CAUGHT' if caught else '*** UNGUARDED ***'))
            if not caught:
                unguarded.append((name, expect, failed))
        finally:
            shutil.rmtree(root, ignore_errors=True)

    print()
    if unguarded:
        for name, expect, failed in unguarded:
            print('  UNGUARDED: %s' % name)
            print('    expected a failure matching: %s' % expect)
            print('    actual failures: %s' % (failed or 'NONE — the suite passed a broken theme'))
    print('%d violations seeded, %d caught, %d unguarded'
          % (len(VIOLATIONS), len(VIOLATIONS) - len(unguarded), len(unguarded)))
    print('OVERALL: %s' % ('PASS' if not unguarded else '*** GAPS ABOVE ***'))
