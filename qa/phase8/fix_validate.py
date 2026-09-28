# -*- coding: utf-8 -*-
"""Teach the validator the post-review contract.

Every finding the review confirmed gets an assertion here, so the same defect
cannot come back quietly.
"""
p = 'validate.py'
s = open(p, encoding='utf-8').read()
done = []


def sub(old, new, label):
    global s
    assert old in s, 'NOT FOUND: ' + label
    s = s.replace(old, new, 1)
    done.append(label)


sub("""NEW_SNIPPETS = ['product-media-gallery', 'product-variant-picker', 'quantity-selector',
                'cart-line-item', 'cart-icon-bubble', 'icon-plus', 'icon-minus', 'icon-chevron']""",
    """NEW_SNIPPETS = ['product-media-gallery', 'product-variant-picker', 'quantity-selector',
                'cart-line-item', 'cart-icon-bubble', 'cart-totals', 'cart-empty-state',
                'icon-plus', 'icon-minus', 'icon-chevron']""",
    'the two shared cart snippets are files')

# The component stylesheets moved to the layout.
sub("""check("no hard-coded /cart path in the markup",""",
    """check("the cart components are loaded once, from the layout",
      "'component-quantity.css'" in R('layout/theme.liquid')
      and "'component-cart-line.css'" in R('layout/theme.liquid')
      and 'component-quantity.css' not in R('sections/main-product.liquid')
      and 'component-cart-line.css' not in R('sections/main-cart.liquid'))
check("no hard-coded /cart path in the markup",""",
    'the components load once')

# The product form.
sub("""check("the accelerated checkout button is not wrapped",""",
    """check("the product form does not switch off constraint validation",
      'novalidate' not in product_body,
      'novalidate defeats the quantity input\\'s own min')
check("the variant picker is inside the product form",
      product_body.index("form 'product'")
      < product_body.index("render 'product-variant-picker'")
      < product_body.index('endform'))
check("the variant table carries the quantity rule",
      'quantity_rule' in product_body)
check("the sticky buying column is reachable by keyboard",
      re.search(r'class="main-product__info"\\s*\\n?\\s*tabindex="0"', product_body) is not None)
check("the accelerated checkout button is not wrapped",""",
    'the product form contract')

sub("""check("unavailable values stay in the DOM and stay focusable",
      'data-unavailable' in picker_body and 'disabled' not in picker_body)""",
    """check("unavailable values stay in the DOM and stay focusable",
      'data-unavailable' in picker_body and 'disabled' not in picker_body)
check("the server's unavailable note carries the hook the script manages",
      'data-unavailable-note' in picker_body
      and 'data-unavailable-note' in strip_js(R('assets/product.js')))""",
    'one unavailable note, not two')

# The cart surfaces.
sub("""check("the drawer is a dialog with a label",""",
    """check("the drawer is not rendered on the cart page",
      re.search(r"unless template\\.name == 'cart'", R('layout/theme.liquid')) is not None)
check("the cart page is its own render target",
      'data-cart-page-section' in cartpage_body and 'data-cart-page-inner' in cartpage_body
      and 'data-cart-page-inner' in strip_js(R('assets/cart.js')))
check("each cart surface has a visible failure line",
      drawer_body.count('data-cart-error') == 1 and cartpage_body.count('data-cart-error') == 1
      and 'showCartError' in strip_js(R('assets/cart.js')))
check("the drawer carries its own live region inside the dialog",
      'data-cart-drawer-status' in drawer_body
      and drawer_body.index('data-cart-drawer-status') < drawer_body.index('data-cart-drawer-inner'))
check("cart line ids are namespaced by their surface",
      "scope: 'CartDrawer'" in drawer_body and "scope: 'CartPage'" in cartpage_body
      and 'id_scope' in line_body)
check("the tax note is derived from the store, not asserted",
      'cart.taxes_included' in R('snippets/cart-totals.liquid'))
check("the empty-cart button goes somewhere this theme renders",
      'routes.root_url' in R('snippets/cart-empty-state.liquid')
      and 'all_products_collection_url' not in R('snippets/cart-empty-state.liquid'),
      'no collection template exists yet')
check("totals and the empty state are shared, not duplicated",
      "render 'cart-totals'" in drawer_body and "render 'cart-totals'" in cartpage_body
      and "render 'cart-empty-state'" in drawer_body
      and "render 'cart-empty-state'" in cartpage_body)
check("the drawer is a dialog with a label",""",
    'the cart contract')

# JavaScript.
sub("""check("the quantity debounce is a literal, not a motion token",""",
    """check("the busy state never disables the add button",
      not re.search(r'button\\.disabled = ', cart_js),
      'disabling a focused control blurs it')
check("render targets are collected from the page",
      'collectSections' in cart_js and "SECTIONS = ['cart-icon-bubble']" in cart_js)
check("an add carries a sequence guard",
      cart_js.count('var seq = ++requestSeq;') == 2)
check("a superseded change still clears its busy state",
      cart_js.index("control.removeAttribute('aria-busy')")
      < cart_js.index('if (seq !== requestSeq) return;'))
check("a re-rendered drawer tears its open state down",
      re.search(r'init: function \\(\\) \\{\\s*/\\*.*?if \\(this\\.isOpen\\)', cart_js, re.S) is not None)
check("the price is never blanked when no variant matches",
      "price: ''" not in product_js and 'if (variant) {' in product_js)
check("the quantity rule follows the variant",
      'updateQuantityRule' in product_js)
check("the gallery opens on the slide the server chose",
      "querySelector('.product-gallery__slide.is-active')" in product_js)
check("the scroll strategy reads the rendered layout, not the setting",
      'viewport.scrollWidth > viewport.clientWidth' in product_js
      and "getAttribute('data-gallery-layout') === 'carousel'" not in product_js)
check("the quantity debounce is a literal, not a motion token",""",
    'the JavaScript contract')

# The design system.
sub("""print("\\n=== LOCALES ===")""",
    """print("\\n=== DESIGN SYSTEM ===")
qty_css = strip_css(R('assets/component-quantity.css'))
check("the steppers are not shipped without the script that binds them",
      '.cart-js .quantity__button' in qty_css and 'display: none;' in qty_css)
check("the native spinner survives when the steppers do not",
      '.cart-js .quantity__input::-webkit-inner-spin-button' in qty_css)
check("the disabled stepper matches the system's 0.45",
      'opacity: 0.45' in qty_css and 'opacity: 0.35' not in qty_css)
check("an icon-only control hovers to the accent, not to opacity",
      'color: var(--accent-current)' in qty_css)
check("the compact quantity keeps the 16px value",
      'font-size: var(--type-body-sm-size)' not in qty_css)
check("one focus ring on the quantity control, not two",
      ':focus-within' not in qty_css and ':has(.quantity__input:focus-visible)' in qty_css)
check("the swatch uses its own token",
      'var(--swatch-size)' in strip_css(R('assets/section-main-product.css')))
check("the drawer's scrim takes the duration §21.4 assigns it",
      'transition: opacity var(--transition-slow)' in strip_css(R('assets/section-cart-drawer.css')))
check("the visually-hidden recipe is not copied a second time",
      '.visually-hidden--until-focus:focus-visible' in strip_css(R('assets/section-cart-drawer.css'))
      and 'clip: rect(0 0 0 0)' not in strip_css(R('assets/section-cart-drawer.css')))

print("\\n=== LOCALES ===")""",
    'the design-system corrections')

open(p, 'w', encoding='utf-8', newline='').write(s)
for i, label in enumerate(done, 1):
    print('%2d. %s' % (i, label))
