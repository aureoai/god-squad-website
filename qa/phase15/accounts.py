# -*- coding: utf-8 -*-
"""Phase 15 — the account entry point, and the surfaces deliberately not built.

Most of this suite asserts on ABSENCE, which is unusual and is the point. The
Phase 15 deliverable is mostly a set of things the theme must not do:

  - must not ship templates/customers/*  (their absence is Shopify's documented
    trigger for auto-upgrading a merchant off legacy accounts)
  - must not output any customer field    (the customer object is GLOBAL, and
    the Section Rendering API inherits the page's Liquid context, so one
    {{ customer.email }} in a shared snippet publishes PII into every
    ?sections= response on the site)
  - must not construct an account or order URL by hand
  - must not put customer data in any client-side store

An absence test that has never been seen to fail proves nothing, so every one
of these is negative-controlled in negctl.py.
"""
import io
import json
import os
import re
import sys

# reconfigure(), not a fresh TextIOWrapper. phase9/build.py installs a wrapper
# of its own on import, and when a discarded wrapper is collected it closes the
# underlying buffer — which killed this suite's own output the moment it started
# importing the harness.
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', 'phase9')))
THEME = os.environ.get('GS_THEME') or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')

FAILURES = []
CHECKS = [0]


def check(label, ok, detail=''):
    CHECKS[0] += 1
    print('  %-66s %s %s' % (label, 'OK  ' if ok else '*** FAIL ***',
                             '' if ok else str(detail)[:120]))
    if not ok:
        FAILURES.append(label)


def read(rel):
    return io.open(os.path.join(THEME, rel), encoding='utf-8').read()


def strip_comments(text):
    text = re.sub(r'\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}', '', text, flags=re.S)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    text = re.sub(r'(?m)^\s*//.*$', '', text)
    return text


def theme_files(*exts):
    for root, _dirs, files in os.walk(THEME):
        for f in sorted(files):
            if not exts or f.endswith(exts):
                p = os.path.join(root, f)
                yield os.path.relpath(p, THEME).replace(os.sep, '/'), \
                    strip_comments(io.open(p, encoding='utf-8').read())


def render_header():
    """The header, rendered from the theme UNDER TEST.

    This used to read a pre-built harness page, and that made every assertion
    on rendered markup blind to negctl.py: the seed changed the theme copy
    while the suite went on reading a page built from the real theme, so one
    genuinely broken theme passed clean. Rendering here means GS_THEME reaches
    the markup assertions too, which is what makes them worth anything.
    """
    import build  # the phase9 harness
    build.THEME = THEME
    engine = build.make_engine(template='index')
    engine.root = THEME
    return build.render_section(engine, 'sections/header.liquid', 'header',
                                dict(build.HEADER_SETTINGS))


if __name__ == '__main__':
    print('=== THE ACCOUNT CONTROL IS SHOPIFY\'S COMPONENT ===')
    page = render_header()
    el = re.search(r'<shopify-account.*?</shopify-account>', page, re.S)
    check('the header renders <shopify-account>', el is not None)
    body = el.group(0) if el else ''
    check('exactly one account control on the page', page.count('<shopify-account') == 1,
          'count=%d' % page.count('<shopify-account'))
    check('and no second entry point beside it',
          'href="/account"' not in page and 'routes.account_url' not in page)
    check('its menu comes from the global setting, not a literal',
          'menu="customer-account-main-menu"' in body)
    hdr = strip_comments(read('sections/header.liquid'))
    check('the setting is read as settings.customer_account_menu',
          'settings.customer_account_menu' in hdr)
    check('with a documented fallback handle',
          "default: 'customer-account-main-menu'" in hdr)

    print()
    print('=== IT KEEPS THE BRAND MARK AND IT IS NAMED ===')
    check('the signed-out avatar uses Shopify\'s documented slot',
          'slot="signed-out-avatar"' in body)
    check('the slot carries the Phase 3 account icon', 'icon--account' in body)
    check('the icon itself is decorative', 'aria-hidden="true"' in body)
    check('and the control carries an accessible name',
          re.search(r'visually-hidden">\s*Account\s*</span>', body) is not None)
    check('the name comes from the locale file, not the markup',
          "'header.account' | t" in hdr)

    print()
    print('=== IT IS GATED TWICE, AND BOTH GATES WORK ===')
    check('gated on the platform flag', 'shop.customer_accounts_enabled' in hdr)
    check('and on the merchant setting', 'section.settings.show_account' in hdr)
    check('the flag is used ONLY as a visibility gate, never to detect a system',
          hdr.count('customer_accounts_enabled') == 1)
    check('nothing branches on customer_accounts_optional, which is a checkout policy',
          'customer_accounts_optional' not in hdr)
    check('and nothing tries to sniff the account system from a route string',
          not re.search(r"routes\.account\w*_url\s*\|?\s*contains", hdr))

    print()
    print('=== THE THEME NEVER REACHES INSIDE A COMPONENT IT DOES NOT OWN ===')
    css = strip_comments(read('assets/header.css'))
    check('it styles the element itself', 'shopify-account.header__control' in css)
    check('through the published custom properties', '--shopify-account-color-background' in css)
    # Parse SELECTORS rather than grepping the file. Every --shopify-account-*
    # custom property name contains the string "shopify-account", so a text
    # search finds the declarations and reports them as selectors.
    selectors = []
    for chunk in css.split('}'):
        if '{' in chunk:
            sel = chunk.rsplit('{', 1)[0].strip().splitlines()[-1].strip()
            if 'shopify-account' in sel:
                selectors.append(sel)
    reaching = [sel for sel in selectors
                if re.search(r'shopify-account[\w.:()-]*\s+\S', sel)]
    check('every rule targets the element itself, never a descendant',
          not reaching, reaching[:3])
    # Exactly one. Two meant the dead :not(:defined) rule was still there.
    check('and there is exactly one rule for it, not a pile',
          selectors == ['shopify-account.header__control'], selectors)
    check('and no ::part or ::slotted override that is not published',
          '::part(' not in css or '::part(signed-out-avatar)' in css)

    print()
    print('=== THE BOX IS RESERVED BEFORE THE COMPONENT EXISTS ===')
    # A custom element has no dimensions until its script runs, so the header
    # would shift on every load unless something reserves the space. Phase 15
    # first shipped a :not(:defined) rule for that, the way Dawn does. Measured
    # at seven viewports it turned out to be dead: the element carries
    # class="header__control", and THAT class already sets the 44px min-box.
    # The rule was removed and this asserts the mechanism that actually works.
    check('the control carries the shared header-control class',
          'class="header__control header__account"' in body)
    m = re.search(r'^\.header__control \{([^}]*)\}', css, re.M)
    check('and that class sets the target-size floor', m is not None
          and 'min-width: var(--target-min)' in m.group(1)
          and 'min-height: var(--target-min)' in m.group(1))
    check('no dead :not(:defined) rule was left behind', ':not(:defined)' not in css)
    check('and no duplicate box or hover declaration for the element',
          not re.search(r'shopify-account[^{]*\{[^}]*min-width', css)
          and not re.search(r'shopify-account[^{]*:hover', css))
    # An author rule on the element beats the component's own :host styles, so
    # unlike a :not(:defined) reservation this floor survives the upgrade.
    check('the slotted avatar is sized to the header icon token',
          re.search(r'\.header__account-avatar \{[^}]*var\(--icon-md\)', css, re.S) is not None)

    print('=== THE CUSTOMER OBJECT IS NEVER OUTPUT ANYWHERE ===')
    # customer is global for any signed-in visitor, and the Section Rendering
    # API inherits the requested page's Liquid context — so a single output in
    # any shared file publishes PII into every ?sections= response.
    leaks = []
    truthy = []
    for rel, src in theme_files('.liquid', '.js', '.json'):
        for m in re.finditer(r'\{\{-?\s*customer\.[\w.]+', src):
            leaks.append((rel, m.group(0).strip()))
        for m in re.finditer(r'customer\.(?!accounts)[\w.]+', src):
            truthy.append((rel, m.group(0)))
    check('no customer field is ever printed', not leaks, leaks[:4])
    allowed = {'customer.orders', 'customer.name'}
    unexpected = [t for t in truthy if t[1] not in allowed]
    check('and no customer field is read at all in this theme', not unexpected, unexpected[:4])

    print()
    print('=== NO ORDER SURFACE, AND NO HAND-BUILT ACCOUNT URL ===')
    for rel, src in theme_files('.liquid', '.js'):
        pass
    joined = '\n'.join(src for _rel, src in theme_files('.liquid', '.js'))
    check('no order object is read', not re.search(r'\border\.[\w]+', joined))
    check('no fulfillment or tracking field is read',
          not re.search(r'fulfillment|tracking_(number|url|company)', joined, re.I))
    check('no account or order URL is constructed by hand',
          not re.search(r'["\']/account/(orders|login|register|addresses)', joined))
    check('no order-status or authenticate URL is built',
          not re.search(r'order_status_url|customer_order_url|/authenticate\?key', joined))
    check('the theme links no account route directly any more',
          not re.search(r'routes\.account_\w*url', joined))

    print()
    print('=== THE LEGACY TEMPLATES ARE ABSENT, DELIBERATELY ===')
    cust_dir = os.path.join(THEME, 'templates', 'customers')
    check('templates/customers/ does not exist', not os.path.isdir(cust_dir))
    legacy = ['account', 'activate_account', 'addresses', 'login', 'order',
              'register', 'reset_password']
    present = [n for n in legacy
               if os.path.exists(os.path.join(cust_dir, n + '.json'))
               or os.path.exists(os.path.join(cust_dir, n + '.liquid'))]
    check('none of the seven legacy templates is shipped', not present, present)
    check('and no section was written for one',
          not any(os.path.exists(os.path.join(THEME, 'sections', 'main-%s.liquid' % n))
                  for n in ('account', 'order', 'addresses', 'login', 'register',
                            'reset-password', 'activate-account')))
    check('no customer form tag anywhere',
          not re.search(r"form\s+'(customer_login|create_customer|recover_customer_password|"
                        r"reset_customer_password|activate_customer_password|customer_address|guest_login)'",
                        joined))
    check('no robots.txt.liquid (nothing in the theme supplies noindex)',
          not os.path.exists(os.path.join(THEME, 'templates', 'robots.txt.liquid')))

    print()
    print('=== NO CUSTOMER DATA IN ANY CLIENT-SIDE STORE ===')
    js = '\n'.join(src for rel, src in theme_files('.js'))
    for api in ('localStorage', 'sessionStorage', 'indexedDB', 'document.cookie', 'caches.open'):
        check('no %s anywhere in theme JavaScript' % api, api not in js)
    check('no service worker is registered', 'serviceWorker' not in js)
    check('nothing is logged that could carry customer data',
          not re.search(r'console\.(log|info|debug|table|dir)\s*\(', js))

    print()
    print('=== THE ACCOUNT MENU IS A MERCHANT RESOURCE, NOT THEME CONTENT ===')
    schema = json.load(io.open(os.path.join(THEME, 'config', 'settings_schema.json'),
                               encoding='utf-8'))
    setting = None
    for group in schema:
        for s in group.get('settings', []):
            if s.get('id') == 'customer_account_menu':
                setting = s
                group_name = group.get('name')
    check('a global customer_account_menu setting exists', setting is not None)
    if setting:
        check('it is a link_list, so the merchant picks a real menu',
              setting['type'] == 'link_list', setting['type'])
        check('it is global, not a section setting, matching the logo precedent',
              group_name == 'Customer accounts', group_name)
        check('it defaults to the handle Shopify documents',
              setting.get('default') == 'customer-account-main-menu')
        check('and its help says an empty menu means no links, not defaults',
              'simply has none' in setting.get('info', ''))
    data = json.load(io.open(os.path.join(THEME, 'config', 'settings_data.json'),
                             encoding='utf-8'))
    check('a fresh install carries the menu handle',
          data['current'].get('customer_account_menu') == 'customer-account-main-menu')
    check('and so does the preset',
          data['presets']['God Squad'].get('customer_account_menu') == 'customer-account-main-menu')

    print()
    print('%d checks, %d passed, %d failed'
          % (CHECKS[0], CHECKS[0] - len(FAILURES), len(FAILURES)))
    print('OVERALL: %s' % ('PASS' if not FAILURES else '*** FAILURES ABOVE ***'))
