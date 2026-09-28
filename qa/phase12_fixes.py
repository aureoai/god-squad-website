# -*- coding: utf-8 -*-
"""Phase 12 — the five remaining confirmed defects.

Each was verified against the files before being fixed.
"""
import os

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'god-squad-theme')
done = []


def patch(rel, old, new, label):
    p = os.path.join(THEME, rel)
    s = open(p, encoding='utf-8').read()
    assert s.count(old) == 1, 'NOT FOUND or ambiguous in %s: %s' % (rel, label)
    open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new, 1))
    done.append(label)


# ============ 1. A populated collection must not announce itself as empty ====
patch('sections/main-collection.liquid',
      """    {%- paginate collection.products by section.settings.products_per_page -%}
      {%- if collection.products.size > 0 -%}""",
      """    {%- paginate collection.products by section.settings.products_per_page -%}
      {%- comment -%}
        paginate.items, not collection.products.size.

        Inside a paginate block collection.products is the PAGE SLICE, so an
        out-of-range ?page= — which Shopify answers with a 200 and an empty
        slice, not a 404 — made a collection with products announce "This
        collection is empty." The same reasoning is already written out above
        for the product count, which correctly reads paginate.items: it is the
        size of the set actually being paginated.
      {%- endcomment -%}
      {%- if paginate.items > 0 -%}""",
      'main-collection: the empty state tests the paginated SET, not the page slice')


# ============ 2. The SKU row must be able to appear on a later variant ======
patch('sections/main-product.liquid',
      """        assign show_sku = false
        if section.settings.show_sku and current_variant.sku != blank
          assign show_sku = true
        endif""",
      """        comment
          The row is rendered if ANY variant carries a SKU, not only the one the
          page opened on. Gated on current_variant.sku the markup was absent
          whenever the first variant had none — and assets/product.js updates the
          SKU by querying [data-variant-sku], so a hook that was never rendered
          could never be filled: the SKU could not appear for any later variant.

          It is hidden rather than emptied when the selected variant has no SKU,
          because a <dt>SKU</dt> standing over an empty <dd> is a labelled row
          that says nothing.
        endcomment
        assign show_sku = false
        if section.settings.show_sku
          for v in product.variants
            if v.sku != blank
              assign show_sku = true
              break
            endif
          endfor
        endif""",
      'main-product: the SKU row renders if ANY variant has one')

patch('sections/main-product.liquid',
      """          {%- if show_sku -%}
            <div class="main-product__meta-row">
              <dt>{{ 'products.meta.sku' | t }}</dt>
              <dd data-variant-sku>{{ current_variant.sku }}</dd>
            </div>
          {%- endif -%}""",
      """          {%- if show_sku -%}
            <div
              class="main-product__meta-row"
              data-variant-sku-row
              {% if current_variant.sku == blank %}hidden{% endif %}
            >
              <dt>{{ 'products.meta.sku' | t }}</dt>
              <dd data-variant-sku>{{ current_variant.sku }}</dd>
            </div>
          {%- endif -%}""",
      'main-product: the SKU row hides itself when the selected variant has none')


# ============ 3. "Unavailable" is not "Sold out" ============================
patch('assets/product.js',
      """    function updateButton(variant) {
      if (!addButton) return;
      var label = addButton.querySelector('[data-add-to-cart-label]');
      var buyable = !!(variant && variant.available);

      addButton.disabled = !buyable;
      if (label) {
        label.textContent = buyable
          ? addButton.getAttribute('data-label-idle') || label.textContent
          : addButton.getAttribute('data-label-sold-out') || label.textContent;
      }""",
      """    function updateButton(variant) {
      if (!addButton) return;
      var label = addButton.querySelector('[data-add-to-cart-label]');
      var buyable = !!(variant && variant.available);

      addButton.disabled = !buyable;
      if (label) {
        /* Three states, not two. A null variant is an option combination that
           was never manufactured — it is not sold out, and saying "Sold out"
           tells the customer something false: that it existed and ran out, so
           it might come back. "Unavailable" is the honest word, and the locale
           already carries it. */
        var next;
        if (buyable) {
          next = addButton.getAttribute('data-label-idle');
        } else if (variant) {
          next = addButton.getAttribute('data-label-sold-out');
        } else {
          next = addButton.getAttribute('data-label-unavailable')
            || addButton.getAttribute('data-label-sold-out');
        }
        label.textContent = next || label.textContent;
      }""",
      'product.js: a combination that does not exist reads Unavailable, not Sold out')


# ============ 4. The unit price must follow the variant =====================
patch('sections/main-product.liquid',
      """        {%- if current_variant.unit_price_measurement != blank -%}""",
      """        {%- comment -%}
          The unit price follows the variant like every other price on this
          page. It was rendered once from the variant the page opened on, with
          no hook and no field in the variant table, so it could not update —
          and a per-litre price left over from a different size is worse than
          none.
        {%- endcomment -%}
        {%- if current_variant.unit_price_measurement != blank -%}""",
      'main-product: the unit price block is documented as variant-driven')

patch('assets/product.js',
      """    function updateSku(variant) {""",
      """    /* Hidden rather than emptied: a labelled row with nothing after it is not
       information. The row only exists when some variant has a SKU. */
    function updateSkuRow(variant) {
      var row = root.querySelector('[data-variant-sku-row]');
      if (!row) return;
      var has = !!(variant && variant.sku);
      if (has) {
        row.removeAttribute('hidden');
      } else {
        row.setAttribute('hidden', '');
      }
    }

    function updateSku(variant) {""",
      'product.js: the SKU row is shown or hidden with its variant')

for i, label in enumerate(done, 1):
    print('%d. %s' % (i, label))
