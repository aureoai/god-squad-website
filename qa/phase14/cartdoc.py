# -*- coding: utf-8 -*-
"""Phase 14 — the cart as it is RENDERED, asserted against the built pages.

These read the real output of the real .liquid files, so nothing here can pass
because a fixture was written to make it pass. The browser behaviour is in
cartqa.py; this is the markup contract.
"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, '..', 'phase8', 'site'))
THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
FAILURES = []
CHECKS = [0]


def check(label, ok, detail=''):
    CHECKS[0] += 1
    print('  %-64s %s %s' % (label, 'OK  ' if ok else '*** FAIL ***',
                             '' if ok else str(detail)[:130]))
    if not ok:
        FAILURES.append(label)


def page(name):
    return io.open(os.path.join(SITE, name), encoding='utf-8').read()


def src(rel):
    return io.open(os.path.join(THEME, rel), encoding='utf-8').read()


def css(rel):
    """A stylesheet with its comments stripped.

    The Phase 14 comment in section-cart-drawer.css NAMES the selector that was
    moved out of it, to say where it went. Asserting on the raw file therefore
    reads the explanation as if it were a rule — Phase 13 made the same mistake
    with Liquid comments and the same fix applies.
    """
    return re.sub(r'/\*.*?\*/', '', io.open(os.path.join(THEME, rel), encoding='utf-8').read(), flags=re.S)


def surface(html, attr):
    """The cart surface's own markup, not the whole document.

    An empty-cart assertion made against the page finds `cart-line` in the
    stylesheet's FILENAME and `data-quantity` in the layout's cart-strings host
    — neither of which is a cart line or a quantity control. This walks the
    element carrying `attr` and returns its subtree.
    """
    i = html.index(attr)
    start = html.rindex('<', 0, i)
    depth, pos = 0, start
    for m in re.finditer(r'<(/?)(div|ul|li|form|section)\b[^>]*?(/?)>', html[start:]):
        if m.group(3) == '/':
            continue
        depth += -1 if m.group(1) else 1
        if depth == 0:
            pos = start + m.end()
            break
    return html[start:pos]


def code(rel):
    """A Liquid file with its comments stripped.

    Phase 13's lesson: the comments explain the mechanism and quote the very
    names the test is looking for, so asserting on the raw file tests the prose.
    """
    s = src(rel)
    s = re.sub(r'\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}', '', s, flags=re.S)
    return s


if __name__ == '__main__':
    print('=== THE ORDER NOTE IS OFF UNTIL A MERCHANT ASKS FOR IT ===')
    for name in ('c-one.html', 'c-many.html', 'c-page-many.html', 'c-page-empty.html'):
        h = page(name)
        check('%-18s renders no note field' % name,
              'data-cart-note' not in h and 'name="note"' not in h)
    check('the drawer setting defaults to off',
          re.search(r'"id":\s*"show_note".*?"default":\s*false',
                    src('sections/cart-drawer.liquid'), re.S) is not None)
    check('the cart page setting defaults to off',
          re.search(r'"id":\s*"show_note".*?"default":\s*false',
                    src('sections/main-cart.liquid'), re.S) is not None)

    print()
    print('=== AND IS SHOPIFY\'S OWN FIELD WHEN IT IS ON ===')
    n = page('c-note.html')
    check('exactly one note field on the surface', n.count('data-cart-note') == 1,
          'found %d' % n.count('data-cart-note'))
    check('it is a textarea named note',
          re.search(r'<textarea[^>]*name="note"', n) is not None)
    check('it sits inside the cart form',
          n.index('data-cart-note') > n.index('id="CartDrawerForm"'))
    check('it has a real label, not a placeholder',
          'for="CartDrawerNote"' in n and 'placeholder' not in n.split('cart-note')[1][:600])
    check('the label is the brief\'s wording',
          'Order note' in n and 'Special instructions' not in n)
    check('an empty note renders the disclosure CLOSED',
          re.search(r'<details class="cart-note"\s*>', n) is not None,
          n[n.index('cart-note') - 60:n.index('cart-note') + 40] if 'cart-note' in n else '')

    w = page('c-noted.html')
    check('a cart that already has a note renders it OPEN',
          re.search(r'<details class="cart-note"\s+open\s*>', w) is not None)
    check('and the field carries the cart\'s own text',
          'Please leave it with the guard at Gate 2.' in w)
    # Phase 17 added | escape. The assertion's intent — the value comes from
    # Shopify, not from a literal — is unchanged; matching the exact string
    # made it break on a security fix that strengthened the very line it guards.
    check('the value comes from cart.note, never a literal',
          re.search(r'\{\{\s*cart\.note\b', src('snippets/cart-note.liquid')) is not None)
    check('and it is escaped, because a customer writes it',
          'cart.note | escape' in src('snippets/cart-note.liquid'))

    p = page('c-page-note.html')
    check('the cart page renders the same one field', p.count('data-cart-note') == 1)
    check('with its own id, so two surfaces cannot collide',
          'CartPageNote' in p and 'CartDrawerNote' not in p)
    # It must be INSIDE the form, or a native submit posts no note at all and
    # the whole no-JavaScript path silently drops what the customer wrote.
    check('and inside the cart form, so a native submit carries it',
          'data-cart-note' in surface(p, 'id="CartPageForm"'))
    check('the drawer has its note inside its form too',
          'data-cart-note' in surface(n, 'id="CartDrawerForm"'))
    check('the drawer keeps its note in the scrolling region, not the footer',
          n.index('data-cart-note') < n.index('cart-drawer__footer'))
    check('both surfaces render the SAME snippet',
          "render 'cart-note'" in code('sections/cart-drawer.liquid')
          and "render 'cart-note'" in code('sections/main-cart.liquid'))

    print()
    print('=== THERE IS A WAY BACK TO SHOPPING FROM BOTH SURFACES ===')
    d = page('c-many.html')
    check('the drawer offers Continue shopping', 'cart-drawer__continue' in d)
    check('and it is a BUTTON that closes the drawer, not a navigation',
          re.search(r'<button[^>]*class="cart-drawer__continue"[^>]*data-cart-close', d) is not None)
    check('so the customer returns to the page they were shopping',
          'cart-drawer__continue' in d and not re.search(
              r'<a[^>]*class="cart-drawer__continue"', d))

    cp = page('c-page-many.html')
    check('the cart page offers Continue shopping', 'main-cart__continue' in cp)
    check('and it IS a link, because there is nothing to return to',
          re.search(r'<a[^>]*class="main-cart__continue"[^>]*href="[^"]+"', cp) is not None)
    check('pointing at the merchant\'s destination, defaulting to the shop root',
          re.search(r'<a class="main-cart__continue" href="/"', cp) is not None,
          re.search(r'<a class="main-cart__continue" href="([^"]*)"', cp).group(1)
          if 'main-cart__continue' in cp else 'absent')

    print()
    print('=== AN EMPTY CART OFFERS NO CHECKOUT AT ALL ===')
    for name, attr in (('c-empty.html', 'data-cart-drawer-inner'),
                       ('c-page-empty.html', 'data-cart-page-inner')):
        h = surface(page(name), attr)
        check('%-18s has no checkout control' % name,
              'name="checkout"' not in h)
        check('%-18s has no quantity control' % name, 'data-quantity' not in h)
        check('%-18s says so in words and offers a way out' % name,
              'Your cart is empty.' in h and 'Shop the collection' in h)
        check('%-18s invents no cart line' % name, 'data-cart-line' not in h)
        check('%-18s offers no note field either' % name, 'data-cart-note' not in h)

    print()
    print('=== THE CHECKOUT PATH IS SHOPIFY\'S, NOT THE THEME\'S ===')
    for rel in ('sections/cart-drawer.liquid', 'sections/main-cart.liquid'):
        c = code(rel)
        check('%-28s submits name="checkout" to the cart form' % rel,
              'name="checkout"' in c)
        check('%-28s posts to routes.cart_url' % rel,
              '{{ routes.cart_url }}' in c)
        check('%-28s builds no checkout URL of its own' % rel,
              '/checkout' not in c and 'checkout_url' not in c)
        check('%-28s contains no payment field' % rel,
              not re.search(r'card|cvv|expiry|payment.*input', c, re.I))
    check('no shipping or tax is calculated in the theme',
          not re.search(r'shipping_rate|calculate_shipping|tax_rate\s*\*',
                        code('snippets/cart-totals.liquid')))
    check('the totals come from the cart object',
          'cart.items_subtotal_price' in code('snippets/cart-totals.liquid')
          and 'cart.total_price' in code('snippets/cart-totals.liquid'))

    print()
    print('=== NOTHING ABOUT THE CART IS HARDCODED ===')
    cart_files = ['snippets/cart-line-item.liquid', 'snippets/cart-totals.liquid',
                  'snippets/cart-note.liquid', 'snippets/cart-empty-state.liquid',
                  'snippets/cart-icon-bubble.liquid', 'sections/cart-drawer.liquid',
                  'sections/main-cart.liquid']
    joined = '\n'.join(code(f) for f in cart_files)
    check('no currency symbol is written in markup',
          '₱' not in joined and '$' not in joined)
    check('every price goes through the money filter',
          joined.count('| money') >= 4 and not re.search(r'price\s*\|\s*times:\s*\d+\s*\}\}', joined))
    check('no product name, size or colour is written in markup',
          not re.search(r'(Oversized Tee|Heavyweight Hoodie|Utility Cap)', joined))
    check('no stock number or inventory claim',
          'inventory_quantity' not in joined and not re.search(r'Low stock|In stock|left', joined))
    check('no invented discount',
          'line_level_discount_allocations' in joined
          and not re.search(r'\d+\s*%\s*off|discount\s*=\s*\d', joined))
    check('the count is cart.item_count, never a literal',
          'cart.item_count' in code('snippets/cart-icon-bubble.liquid'))
    check('and an empty cart shows no badge',
          'if cart.item_count > 0' in code('snippets/cart-icon-bubble.liquid'))

    print()
    print('=== EVERY CART LINE IS SHOPIFY\'S LINE ===')
    li = code('snippets/cart-line-item.liquid')
    for field, what in (('item.product.title', 'the title'),
                        ('item.options_with_values', 'the selected options'),
                        ('item.final_line_price', 'the line price'),
                        ('item.quantity', 'the quantity'),
                        ('item.url_to_remove', 'the removal URL'),
                        ('item.image', 'the image'),
                        ('item.key', 'the line key')):
        check('%-22s comes from %s' % (what, field), field in li)
    check('the variant is shown by option, never by id',
          'variant.id' not in li and 'option.value' in li)
    check('the image is resized, not served at full resolution',
          'image_url: width: 300' in li and 'widths:' in li)
    check('the quantity input is never conditional (updates[] is positional)',
          li.count("name: 'updates[]'") == 1)

    print()
    print('=== THE TWO CART SURFACES NEVER COEXIST ===')
    lay = code('layout/theme.liquid')
    check('the drawer is not rendered on the cart template',
          re.search(r"unless template\.name == 'cart'", lay) is not None)
    check('nor when the merchant chose the cart page',
          re.search(r"if settings\.cart_type != 'page'", lay) is not None)
    for name in ('c-page-empty.html', 'c-page-many.html', 'c-page-note.html'):
        check('%-18s carries no drawer' % name, 'data-cart-drawer' not in page(name))

    print()
    print('=== THE ADD CONFIRMATION APPEARS ONLY WHERE IT IS NEEDED ===')
    nd = page('p-nodrawer.html')
    check('a product page with no drawer still has a confirmation line',
          'data-product-success' in nd)
    check('it ships hidden', re.search(r'data-product-success[^>]*\n?\s*role="status"\s*\n?\s*hidden', nd)
          is not None or re.search(r'data-product-success[\s\S]{0,80}?hidden', nd) is not None)
    check('it is a status region, not an alert',
          re.search(r'data-product-success[\s\S]{0,60}role="status"', nd) is not None)
    check('it says the words as well as using the colour',
          'data-product-success-text' in nd)
    check('and offers the one thing wanted next',
          re.search(r'main-product__success-link[^>]*href="/cart"', nd) is not None
          or re.search(r'href="/cart"[^>]*class="main-product__success-link"', nd) is not None)

    print()
    print('=== THE QUICK-ADD CARD USES THE FORM ERROR CONTRACT ===')
    pc = code('snippets/product-card.liquid')
    check('the card\'s failure line is [data-product-error]',
          'data-product-error' in pc)
    check('and no longer claims the cart surfaces\' attribute',
          'data-cart-error' not in pc)
    js = io.open(os.path.join(THEME, 'assets', 'cart.js'), encoding='utf-8').read()
    check('a form failure is read out of the form',
          "form.querySelector('[data-product-error], [data-cart-error]')" in js)
    check('a cart failure is scoped to the cart surfaces',
          "'[data-cart-drawer] [data-cart-error], [data-cart-page] [data-cart-error]'" in js)
    check('a multi-variant card sends the customer to the product page instead',
          'products.card.choose_options' in pc and 'product.variants.size > 1' in pc)
    check('a quick add can only ever post the one available variant',
          'product.selected_or_first_available_variant.id' in pc)

    print()
    print('=== THE UPDATE CONTROL IS HIDDEN BY A SHEET THE PAGE LOADS ===')
    mc = css('assets/section-main-cart.css')
    cd = css('assets/section-cart-drawer.css')
    check('the cart page rule is in the cart page stylesheet',
          '.cart-js .main-cart__update' in mc)
    check('and no longer in the drawer stylesheet the page never loads',
          '.main-cart__update' not in cd,
          [l for l in cd.splitlines() if '.main-cart__update' in l])
    check('the drawer keeps its own', '.cart-js .cart-drawer__update' in cd)
    check('the cart page links its own stylesheet',
          "'section-main-cart.css' | asset_url" in code('sections/main-cart.liquid'))

    print()
    print('%d checks, %d passed, %d failed'
          % (CHECKS[0], CHECKS[0] - len(FAILURES), len(FAILURES)))
    print('OVERALL: %s' % ('PASS' if not FAILURES else '*** FAILURES ABOVE ***'))
