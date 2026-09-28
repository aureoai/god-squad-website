# -*- coding: utf-8 -*-
"""Teach the harness what the review changed: the drawer is not on the cart
page, the two cart components load from the layout, and the cart object carries
its tax-inclusive flag."""
p = 'build.py'
s = open(p, encoding='utf-8').read()
done = []


def sub(old, new, label):
    global s
    assert old in s, 'NOT FOUND: ' + label
    s = s.replace(old, new, 1)
    done.append(label)


sub("""<link rel="stylesheet" href="assets/component-button.css">""",
    """<link rel="stylesheet" href="assets/component-button.css">
<link rel="stylesheet" href="assets/component-quantity.css">
<link rel="stylesheet" href="assets/component-cart-line.css">""",
    'the two cart components load from the layout')

# The cart object's tax flag drives the totals note.
s = s.replace("""CART_EMPTY = wrap({'item_count': 0, 'items': [], 'items_subtotal_price': 0,
                   'total_price': 0, 'cart_level_discount_applications': []})""",
              """CART_EMPTY = wrap({'item_count': 0, 'items': [], 'items_subtotal_price': 0,
                   'total_price': 0, 'cart_level_discount_applications': [],
                   'taxes_included': False})""", 1)
s = s.replace("""        'cart_level_discount_applications': disc,
        'empty?': len(items) == 0,""",
              """        'cart_level_discount_applications': disc,
        'taxes_included': False,
        'empty?': len(items) == 0,""", 1)
done.append('the cart carries taxes_included')

sub("""def write(name, parts, header_html, drawer_html, template='product'):""",
    """def write(name, parts, header_html, drawer_html, template='product'):
    # The layout does not render the drawer on the cart template: two views of
    # one cart on one page can disagree, and they collided on every line's ids.
    if template == 'cart':
        drawer_html = ''""",
    'the drawer is not on the cart page')

open(p, 'w', encoding='utf-8', newline='').write(s)
for label in done:
    if label != 'no-op':
        print(' -', label)
