# -*- coding: utf-8 -*-
"""Phase 12 — Low stock, on the product page only.

The rule the brief sets is "do not invent Low stock; it must be based on actual
data" and "do not expose exact inventory numbers unless the merchant explicitly
wants that functionality".

So the comparison happens in Liquid, server-side, and only a BOOLEAN reaches the
page. variant.inventory_quantity is public on the storefront, and Phase 8 built
the variant table field-by-field precisely to keep it out of the source; that
decision stands.

Two guards, because the number alone does not mean what it looks like:
  inventory_management == 'shopify'  — Shopify is actually tracking this variant;
                                       an untracked variant reports 0 forever.
  inventory_policy == 'deny'         — it cannot be oversold. A continue-selling
                                       variant is never low: it is unlimited.

Product page only. On a card, repeated down a grid, "Low stock" stops being
information and becomes urgency marketing, which PHASE-1 section 29.8 and this
brief's CORE PRINCIPLE both rule out.
"""
import collections
import json
import os
import re

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'god-squad-theme')
done = []


def patch(rel, old, new, label):
    p = os.path.join(THEME, rel)
    s = open(p, encoding='utf-8').read()
    assert s.count(old) == 1, 'NOT FOUND or ambiguous in %s: %s' % (rel, label)
    open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new, 1))
    done.append(label)


# ------------------------------------------------- 1. the boolean, per variant
patch('sections/main-product.liquid',
      """          "sku": {{ v.sku | json }},""",
      """          "sku": {{ v.sku | json }},
          {%- comment -%}
            A boolean, never the figure. The threshold comparison happens here so
            inventory_quantity stays server-side: publishing it would leak either
            stock levels or lifetime sales, which Phase 8 refused and Phase 1
            recorded as BUSINESS INFORMATION REQUIRED.
          {%- endcomment -%}
          "low_stock": {% if low_stock_at > 0 and v.inventory_management == 'shopify' and v.inventory_policy == 'deny' and v.available and v.inventory_quantity > 0 and v.inventory_quantity <= low_stock_at %}true{% else %}false{% endif %},""",
      'main-product: each variant carries a low_stock boolean, not a count')


# --------------------------------------------------- 2. the threshold, and now
patch('sections/main-product.liquid',
      """  assign qty_min = 1
  assign qty_step = 1""",
      """  comment
    0 disables the line entirely, which is the default: a threshold nobody has
    chosen is a claim nobody has made.
  endcomment
  assign low_stock_at = section.settings.low_stock_threshold | default: 0
  comment
    One line, because inside a {% liquid %} tag every LINE is its own statement
    and a condition split across lines is not a condition.
  endcomment
  assign show_low_stock = false
  if low_stock_at > 0 and current_variant.inventory_management == 'shopify' and current_variant.inventory_policy == 'deny' and current_variant.available and current_variant.inventory_quantity > 0 and current_variant.inventory_quantity <= low_stock_at
    assign show_low_stock = true
  endif

  assign qty_min = 1
  assign qty_step = 1""",
      'main-product: the threshold is a setting, and 0 means silent')


# ------------------------------------------------------------- 3. the markup
patch('sections/main-product.liquid',
      """      {%- comment -%}
        The page's one h1.""",
      """      {%- comment -%}
        Low stock. Text only, no colour-coded pill and no figure — Phase 2
        section 27.3 puts availability in words, and a number here would be the
        inventory disclosure the theme has refused since Phase 8.

        aria-live is deliberately absent: this line changes as a side effect of
        choosing a variant, and the variant change is already announced. A second
        live region would make one action speak twice.
      {%- endcomment -%}
      <p
        class="main-product__low-stock"
        data-low-stock
        {% unless show_low_stock %}hidden{% endunless %}
      >{{ 'products.inventory.low_stock' | t }}</p>

      {%- comment -%}
        The page's one h1.""",
      'main-product: the Low stock line, in words')


# ---------------------------------------------------------------- 4. the schema
p = os.path.join(THEME, 'sections', 'main-product.liquid')
s = open(p, encoding='utf-8').read()
m = re.search(r'\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}', s, re.S)
doc = json.loads(m.group(1), object_pairs_hook=collections.OrderedDict)
assert not any(x.get('id') == 'low_stock_threshold' for x in doc['settings'])
idx = next(i for i, x in enumerate(doc['settings']) if x.get('id') == 'show_sku')
doc['settings'].insert(idx + 1, collections.OrderedDict([
    ('type', 'range'),
    ('id', 'low_stock_threshold'),
    ('label', 'Low stock threshold'),
    ('min', 0),
    ('max', 20),
    ('step', 1),
    ('default', 0),
    ('info',
     'Show a "Low stock" line when the chosen variant has this many left or '
     'fewer. 0 shows nothing. The number itself is never published — only '
     'whether the line appears — and it applies only to variants whose stock '
     'Shopify tracks and which cannot be oversold.'),
]))
s = s[:m.start(1)] + '\n' + json.dumps(doc, indent=2, ensure_ascii=False) + '\n' + s[m.end(1):]
open(p, 'w', encoding='utf-8', newline='').write(s)
done.append('main-product: a Low stock threshold setting, 0 by default')


# ------------------------------------------------------------------ 5. the JS
patch('assets/product.js',
      """    function updateSku(variant) {""",
      """    /* The theme never learns the count — the server sent a boolean — so this
       can only show or hide the line it was given. */
    function updateLowStock(variant) {
      var line = root.querySelector('[data-low-stock]');
      if (!line) return;
      if (variant && variant.low_stock) {
        line.removeAttribute('hidden');
      } else {
        line.setAttribute('hidden', '');
      }
    }

    function updateSku(variant) {""",
      'product.js: the Low stock line follows the variant')

patch('assets/product.js',
      """      updateSkuRow(variant);""",
      """      updateSkuRow(variant);
      updateLowStock(variant);""",
      'product.js: it is called on every variant change')


# ---------------------------------------------------------------- 6. the CSS
patch('assets/section-main-product.css',
      """.main-product__title {""",
      """/* Phase 12. The Low stock line sits above the title, in the muted token at the
   caption size — a statement of fact, not an alarm. No colour-coded pill: Phase
   2 section 27.3 puts availability in words, and a red chip on a premium
   streetwear page reads as a discount store. */
.main-product__low-stock {
  margin: 0 0 var(--space-3);
  color: var(--color-text-current-muted);
  font-family: var(--font-body);
  font-size: var(--type-caption-size);
  font-weight: var(--type-caption-weight);
  letter-spacing: var(--type-caption-ls);
  text-transform: uppercase;
}

.main-product__title {""",
      'section-main-product.css: the Low stock line, muted and uppercase')

for i, label in enumerate(done, 1):
    print('%d. %s' % (i, label))
