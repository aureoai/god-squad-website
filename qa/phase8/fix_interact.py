# -*- coding: utf-8 -*-
"""Bring the cart interaction suite up to what the review changed, and add the
assertions that would have caught the findings it raised."""
p = 'interact.py'
s = open(p, encoding='utf-8').read()
done = []


def sub(old, new, label):
    global s
    assert old in s, 'NOT FOUND: ' + label
    s = s.replace(old, new, 1)
    done.append(label)


# The section list is built from what is on the page, so its ORDER is no longer
# fixed; assert on membership.
sub("""        t('add carries sections', r.form && r.form.sections === 'cart-drawer,cart-icon-bubble' || 'sections=' + (r.form && r.form.sections));""",
    """        t('add carries both render targets',
          (r.form && r.form.sections.indexOf('cart-drawer') !== -1
            && r.form.sections.indexOf('cart-icon-bubble') !== -1)
            || 'sections=' + (r.form && r.form.sections));
        t('add does not ask for a cart-page section that is not here',
          (r.form && r.form.sections.split(',').length === 2)
            || 'sections=' + (r.form && r.form.sections));""",
    'section membership, not order')

# The add button must keep focus: disabling the focused element blurs it.
sub("""        t('the add button is restored', q('[data-add-to-cart]').getAttribute('aria-busy') === null || 'still busy');""",
    """        t('the add button is restored', q('[data-add-to-cart]').getAttribute('aria-busy') === null || 'still busy');
        t('the add button is never disabled by the busy state',
          q('[data-add-to-cart]').disabled === false || 'the button was left disabled');""",
    'the busy state never disables')

# A failed change has to be visible, not only announced.
sub("""      .then(function () {
        window.__mode = 'error422';""",
    """      // ------------------------------------------------ a visible failure
      .then(function () {
        window.__mode = 'error422';
        window.__req.length = 0;
        var up = q('[data-cart-line] [data-quantity-step="1"]');
        if (up) up.click();
        return wait(420);
      })
      .then(function () {
        var box = q('[data-cart-error]');
        t('a failed quantity change is visible, not only announced',
          (box && box.hidden === false && box.textContent.indexOf("can't add more") !== -1)
            || 'box=' + (box && (box.hidden ? '(hidden)' : box.textContent)));
        t('a failed quantity change clears its busy state',
          q('[data-cart-line] [data-quantity]').getAttribute('aria-busy') === null
            || 'still busy');
        t('the failure is announced inside the dialog, not outside it',
          (q('[data-cart-drawer-status]') && q('[data-cart-drawer-status]').textContent.length > 0)
            || 'drawer region empty; layout region=' + document.getElementById('CartStatus').textContent);
        window.__mode = 'ok';
        return null;
      })
      .then(function () {
        window.__mode = 'error422';""",
    'a visible, in-dialog failure')

open(p, 'w', encoding='utf-8', newline='').write(s)
for label in done:
    print(' -', label)
