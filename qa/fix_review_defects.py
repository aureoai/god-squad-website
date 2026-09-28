# -*- coding: utf-8 -*-
"""The seven confirmed defects from the Phase 10 adversarial review.

Each was verified against the files and the cited documents before being fixed.
"""
import json
import os
import collections

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'god-squad-theme')
done = []


def patch(rel, old, new, label):
    p = os.path.join(THEME, rel)
    s = open(p, encoding='utf-8').read()
    assert s.count(old) == 1, 'NOT FOUND (or ambiguous) in %s: %s' % (rel, label)
    open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new, 1))
    done.append(label)


# --- 1. BLOCKER: the desktop sizes clause fires below its own breakpoint -----
patch('sections/main-collection.liquid',
      """  assign need_d = cols_d | times: col_min
  assign need_d = cols_d | minus: 1 | times: gap | plus: need_d
  assign threshold_d = need_d | plus: chrome_d""",
      """  assign need_d = cols_d | times: col_min
  assign need_d = cols_d | minus: 1 | times: gap | plus: need_d
  assign threshold_d = need_d | plus: chrome_d

  comment
    Floored at the tier boundary. The desktop column count only takes effect at
    --bp-lg 1024, but the threshold is derived from the column arithmetic alone,
    so at three desktop columns it computes 3*272 + 2*32 + 96 = 976. Left there,
    the desktop clause matches from 976px up while the grid at 976-1023px is
    still painting the TABLET column count — declaring 280px for a slot that
    actually paints 452px, a 38% under-declaration that makes the browser fetch
    a candidate it then has to upscale. A sizes clause must never claim a width
    before the layout that produces it applies.
  endcomment
  if threshold_d < 1024
    assign threshold_d = 1024
  endif""",
      'collection: the desktop sizes clause is floored at its own breakpoint')

# --- 2. BLOCKER: six blocks, not four, and thin tracks -----------------------
patch('assets/section-footer.css',
      """  .footer__blocks {
    grid-template-columns: none;
    grid-auto-flow: column;
    /* minmax(0, 1fr), not 1fr: a grid track's automatic floor is its content's
       min-content width, so one long menu item would push the row wider than
       the container instead of wrapping. */
    grid-auto-columns: minmax(0, 1fr);
    gap: var(--grid-gap-large);
  }""",
      """  /* Wrapping tracks, not one track per block.

     The ceiling here is SIX, not four: the section declares two block types —
     link_list at limit 4 and text at limit 2 — so a merchant can place six.
     With one track per block that is (1024 - 96 - 160) / 6 = 128px per column
     at the breakpoint, narrow enough to wrap every menu item to its own line.

     auto-fit with a floor degrades to more ROWS instead of thinner columns, so
     the row stays readable at any block count the schema actually permits.
     minmax(0, 1fr) is kept inside it for the original reason: a track's
     automatic floor is its content's min-content width, so one long menu item
     would otherwise push the row wider than its container. */
  .footer__blocks {
    grid-template-columns: repeat(auto-fit, minmax(11rem, 1fr));
    grid-auto-flow: row;
    grid-auto-columns: minmax(0, 1fr);
    gap: var(--grid-gap-large);
  }""",
      'footer: the block row wraps instead of thinning to six tracks')

# --- 3. BLOCKER: a Shopify admin title leaking to customers ------------------
p = os.path.join(THEME, 'sections', 'footer-group.json')
group = json.load(open(p, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
footer = group['sections']['footer']
footer.pop('blocks', None)
footer['block_order'] = []
json.dump(group, open(p, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
open(p, 'a', encoding='utf-8', newline='').write('\n')
done.append('footer-group.json: ships with no menu bound, so no admin title reaches a customer')

# --- 4. MAJOR: the social settings the footer reads never existed ------------
p = os.path.join(THEME, 'config', 'settings_schema.json')
schema = json.load(open(p, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
assert not any(g.get('name') == 'Social' for g in schema), 'Social area already present'
schema.append(collections.OrderedDict([
    ('name', 'Social'),
    ('settings', [
        collections.OrderedDict([
            ('type', 'paragraph'),
            ('content',
             'Paste the full address of each profile. A row with no address is '
             'not rendered, so the footer never shows a link that goes nowhere.'),
        ]),
        collections.OrderedDict([
            ('type', 'url'),
            ('id', 'social_facebook_url'),
            ('label', 'Facebook'),
            ('info', 'No address has been supplied for the brand yet.'),
        ]),
        collections.OrderedDict([
            ('type', 'url'),
            ('id', 'social_instagram_url'),
            ('label', 'Instagram'),
            ('info', 'No address has been supplied for the brand yet.'),
        ]),
    ]),
]))
json.dump(schema, open(p, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
open(p, 'a', encoding='utf-8', newline='').write('\n')
done.append('settings_schema.json: the Social area the footer reads now exists')

# --- 5. MAJOR: Phase 2 sizes the social row at 44px, explicitly --------------
patch('assets/section-footer.css',
      """.footer__social-link {""",
      """/* PHASE-2-DESIGN-SYSTEM.md line 2126 sizes this row explicitly — "social
   marks --icon-lg 28px inside --target-min 44px boxes, --space-5 apart" — so
   the general rule about secondary navigation does not cover it. The menu and
   policy links stay at --target-min-aa; this row does not. */
.footer__social-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: var(--target-min);
  min-width: var(--target-min);""",
      'footer: the social row gets the 44px box Phase 2 specifies for it')

# --- 6. MAJOR: uppercasing the customer's own search term --------------------
patch('assets/section-main-search.css',
      """.main-search__summary {""",
      """/* No text-transform here. The summary echoes the customer's own term back —
   the locale string fences it in curly quotes for exactly that reason — and
   uppercasing it destroys the casing they typed, which defeats the stated
   purpose of echoing it at all: letting them check a typo after the field has
   scrolled out of view. The zero-result line already echoes it untransformed,
   so this also keeps the two states consistent. */
.main-search__summary {""",
      "search: the customer's term is echoed as typed")

# --- 7. MAJOR: a pasted URL overflows the page surface ----------------------
patch('assets/section-main-page.css',
      """.main-page__content {""",
      """/* overflow-wrap is set on the CONTENT ROOT so it inherits to every text-
   bearing descendant. Set only on headings and table cells, a bare URL pasted
   into a paragraph — which is what a contact, shipping or returns page is full
   of — overflowed a 375px viewport: the content box there is ~327px and an
   unbroken 55-character URL sets around 420-480px at --type-body-size. */
.main-page__content {
  overflow-wrap: break-word;""",
      'page: merchant prose wraps instead of overflowing')

for i, label in enumerate(done, 1):
    print('%d. %s' % (i, label))
