# -*- coding: utf-8 -*-
"""Phase 15 — adopt <shopify-account>.

Written as a script, not a heredoc: this file carries backslashes, braces and
quotes that a shell rewrites, and that has cost this project three debugging
detours already.
"""
import io
import json
import os
from collections import OrderedDict

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
class F(object):
    def __init__(self, rel):
        self.rel = rel
        self.path = os.path.join(THEME, rel)
        self.s = io.open(self.path, encoding='utf-8').read()
        self.n0 = len(self.s)

    def sub(self, old, new, label):
        if old not in self.s:
            raise SystemExit('NOT FOUND in %s: %s' % (self.rel, label))
        if self.s.count(old) != 1:
            raise SystemExit('AMBIGUOUS (%d) in %s: %s' % (self.s.count(old), self.rel, label))
        self.s = self.s.replace(old, new, 1)
        print('  ok  %-30s %s' % (self.rel, label))

    def save(self):
        io.open(self.path, 'w', encoding='utf-8').write(self.s)
        print('      %-30s %d -> %d bytes' % (self.rel, self.n0, len(self.s)))


# ======================================================== 1. the header control
h = F('sections/header.liquid')
h.sub(
    """      {%- if shop.customer_accounts_enabled and section.settings.show_account -%}
        <a class="header__control" href="{{ routes.account_url }}">
          {% render 'icon-account' %}
          <span class="visually-hidden">
            {%- if customer -%}
              {{ 'header.account' | t }}
            {%- else -%}
              {{ 'header.log_in' | t }}
            {%- endif -%}
          </span>
        </a>
      {%- endif -%}""",
    """      {%- comment -%}
        PHASE 15 REPLACED THIS CONTROL AND NOTHING ELSE IN THIS FILE.

        It was an <a href="{{ routes.account_url }}"> carrying the Phase 3
        account icon and a label that switched between Account and Log in. It
        worked, and Shopify still redirects that URL. It is gone anyway,
        because the platform moved underneath it.

        WHY A SHOPIFY-OWNED ELEMENT IS HERE AT ALL.
        Legacy customer accounts were deprecated on 2026-02-26 and the account
        experience now lives on Shopify's own host, off this origin. A link
        could only ever navigate away from the store; <shopify-account> opens
        the account sheet in place. On a store still using legacy accounts
        Shopify documents the component as degrading to exactly what this used
        to be — a link straight to the sign-in page — so the replacement loses
        nothing on either system.

        ONE ENTRY POINT, NOT TWO.
        The old link is not kept beside this. Two account controls on one
        header would behave differently from each other — one opening a sheet,
        one navigating off-site — and there is no width in the 375px end
        cluster for a second control anyway.

        WHAT THIS THEME DOES NOT CONTROL.
        Shopify owns this element and says it may change it independently of
        the theme. Only three things are contractual: the published
        --shopify-account-* custom properties, ::part(signed-out-avatar), and
        the signed-out-avatar slot. assets/header.css uses the first and this
        uses the third; nothing here reaches inside it with a descendant
        selector, because that would break the first time Shopify ships a
        change.

        THE SLOT KEEPS THE BRAND'S OWN ICON.
        Without it the header would show Shopify's default avatar in place of
        the account mark Phase 3 drew to the Phase 2 icon contract. The slot is
        the documented way to supply your own, so the icon survives the change.

        THE HIDDEN LABEL IS DELIBERATE BELT AND BRACES.
        Dawn ships this component with no label at all, which implies Shopify
        names the control itself. "Implies" is not good enough for a Level A
        requirement that cannot be tested from here, so a visually-hidden name
        goes in the slot. If Shopify sets its own aria-label that label wins
        and this is ignored; if it does not, the control is still named. The
        two outcomes are "correct" and "correct" — whereas omitting it has an
        outcome that is an unnamed control (SC 4.1.2).
      {%- endcomment -%}
      {%- if shop.customer_accounts_enabled and section.settings.show_account -%}
        <shopify-account
          class="header__control header__account"
          menu="{{ settings.customer_account_menu | default: 'customer-account-main-menu' }}"
        >
          <span class="header__account-avatar" slot="signed-out-avatar">
            {% render 'icon-account' %}
            <span class="visually-hidden">{{ 'header.account' | t }}</span>
          </span>
        </shopify-account>
      {%- endif -%}""",
    'the account control becomes <shopify-account>')

h.sub(
    """    {
      "type": "checkbox",
      "id": "show_account",
      "label": "Show account",
      "default": true,
      "info": "Only appears when customer accounts are enabled for the store."
    },""",
    """    {
      "type": "checkbox",
      "id": "show_account",
      "label": "Show account",
      "default": true,
      "info": "Only appears when customer accounts are enabled for the store, under Settings > Customer accounts. The account pages themselves are hosted by Shopify and are styled in the checkout and accounts editor, not in this theme."
    },""",
    'the setting says where the account pages are styled')


# ================================================= 2. the global menu setting
sp = os.path.join(THEME, 'config', 'settings_schema.json')
schema = json.load(io.open(sp, encoding='utf-8'), object_pairs_hook=OrderedDict)

account_group = OrderedDict([
    ('name', 'Customer accounts'),
    ('settings', [
        OrderedDict([
            ('type', 'paragraph'),
            ('content',
             'Customer accounts are turned on in Shopify admin under Settings > '
             'Customer accounts, not here. When they are on, the header shows the '
             'account control and Shopify hosts the account pages on its own domain. '
             'Their colours and type come from the checkout and accounts editor, '
             'because the theme cannot reach a page it does not serve.'),
        ]),
        OrderedDict([
            ('type', 'link_list'),
            ('id', 'customer_account_menu'),
            ('label', 'Account menu'),
            ('default', 'customer-account-main-menu'),
            ('info',
             'The links inside the account sheet. Create the menu in Navigation, '
             'then choose it here. Leaving this empty does not fall back to a '
             'default set of links \u2014 the sheet simply has none.'),
        ]),
    ]),
])

# After Cart, before Social: the account control sits beside the cart control in
# the header, so the two read together in the editor's sidebar.
idx = next(i for i, g in enumerate(schema) if g.get('name') == 'Cart')
schema.insert(idx + 1, account_group)
io.open(sp, 'w', encoding='utf-8').write(json.dumps(schema, indent=2, ensure_ascii=False) + '\n')
print('  ok  %-30s Customer accounts group (customer_account_menu)' % 'config/settings_schema.json')

# The preset and the current values carry it too, or a fresh install has no menu.
dp = os.path.join(THEME, 'config', 'settings_data.json')
data = json.load(io.open(dp, encoding='utf-8'), object_pairs_hook=OrderedDict)
for block in (data['current'], data['presets']['God Squad']):
    block['customer_account_menu'] = 'customer-account-main-menu'
io.open(dp, 'w', encoding='utf-8').write(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
print('  ok  %-30s customer_account_menu in current + preset' % 'config/settings_data.json')


# ============================================================ 3. the locale
lp = os.path.join(THEME, 'locales', 'en.default.json')
loc = json.load(io.open(lp, encoding='utf-8'), object_pairs_hook=OrderedDict)
# header.log_in is dead: the control no longer chooses between two names, because
# whether the customer is signed in is now the component's state to show, not
# this theme's to assert.
loc['header'].pop('log_in', None)
io.open(lp, 'w', encoding='utf-8').write(json.dumps(loc, indent=2, ensure_ascii=False) + '\n')
print('  ok  %-30s header.log_in removed (dead with the old control)' % 'locales/en.default.json')

h.save()
