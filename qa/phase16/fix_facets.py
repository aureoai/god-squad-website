# -*- coding: utf-8 -*-
"""Phase 16 P0 — the filter drawer must not exist above --bp-md.

Reproduced before fixing, at 1440, 1280 and 768: the Filter trigger is visible,
pressing it sets `overflow: hidden` on the desktop page, and the drawer header
that holds the close button is `display: none` at those widths — so focus stays
on the trigger, the panel's Tab guard then pulls it into an in-flow panel, and
Escape is the only way out of a page that no longer scrolls.

Two independent auditors found this from different directions (a JavaScript
audit and an accessibility audit) and traced it to the same two lines.
"""
import io
import os

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
def sub(rel, old, new, label):
    p = os.path.join(THEME, rel)
    s = io.open(p, encoding='utf-8').read()
    if old not in s:
        raise SystemExit('NOT FOUND in %s: %s' % (rel, label))
    if s.count(old) != 1:
        raise SystemExit('AMBIGUOUS (%d) in %s: %s' % (s.count(old), rel, label))
    n0 = len(s)
    io.open(p, 'w', encoding='utf-8').write(s.replace(old, new, 1))
    print('  ok  %-26s %-44s %d -> %d' % (rel, label, n0, n0 - len(old) + len(new)))


# ------------------------------------------------------------------ the JS
sub('assets/facets.js',
    """    var isOpen = false;

    /* The drawer behaviour is opt-in: the stylesheet only positions this panel
       as a drawer under .facets--drawer, so until this line runs it is an
       ordinary block in the page. */
    panel.classList.add('facets--drawer');
    toggle.hidden = false;
    toggle.setAttribute('aria-expanded', 'false');""",
    """    var isOpen = false;

    /* THE DRAWER EXISTS ONLY BELOW --bp-md, AND THE WIDTH IS THE GATE.

       Every drawer rule in component-facets.css lives inside
       @media (max-width: 767px). `.facets-open body { overflow: hidden }` does
       not — it is top level. So revealing the trigger at a desktop width gave
       the customer a button that locked the page and opened nothing: measured
       at 1440, 1280 and 768, body overflow became hidden, `.facets__bar` (which
       holds the close button) was display:none so closeBtn.focus() was a no-op,
       and the Tab guard below then pulled focus into an in-flow panel with
       Escape as the only exit. That is a keyboard trap, SC 2.1.2.

       The original code set the drawer up unconditionally and registered a
       media-query listener that only ran on CHANGE — so it correctly closed a
       drawer left open by a rotation, and never once evaluated the width the
       page actually loaded at. The fix is to drive both directions from one
       function and call it immediately.

       sections/header.liquid solves the same problem the same way: header.css
       retires the mobile menu with a min-width rule rather than trusting a
       listener. */
    var mq = window.matchMedia('(min-width: 768px)');

    function applyWidth(isDesktop) {
      if (isDesktop) {
        if (isOpen) close(false);
        panel.classList.remove('facets--drawer');
        toggle.hidden = true;
      } else {
        panel.classList.add('facets--drawer');
        toggle.hidden = false;
      }
    }

    applyWidth(mq.matches);
    toggle.setAttribute('aria-expanded', 'false');""",
    'width gates the drawer upgrade')

sub('assets/facets.js',
    """    function open() {
      if (isOpen) return;
      isOpen = true;""",
    """    function open() {
      if (isOpen) return;
      /* Belt and braces. applyWidth already hides the trigger above --bp-md, so
         this should be unreachable — but open() is what locks the page, and a
         second guard on the one function that can strand a customer costs a
         comparison. */
      if (mq.matches) return;
      isOpen = true;""",
    'open() refuses above the breakpoint')

sub('assets/facets.js',
    """    /* Above --bp-md the panel is a row in the page, not a layer, so an open
       drawer left behind by a rotation would trap focus in something that is no
       longer a drawer. */
    var mq = window.matchMedia('(min-width: 768px)');
    var onChange = function (event) { if (event.matches && isOpen) close(false); };""",
    """    /* Crossing the breakpoint in either direction, which a rotation or a
       resized window does. Re-uses the same function as the initial evaluation,
       so the two can never disagree. */
    var onChange = function (event) { applyWidth(event.matches); };""",
    'the change handler reuses applyWidth')


# ----------------------------------------------------------------- the CSS
sub('assets/component-facets.css',
    """.main-collection__filter-toggle {""",
    """/* Retired above --bp-md, where there is no drawer for it to open. display:none
   rather than visibility or opacity, because it must also leave the tab order —
   a focusable control that opens nothing is worse than one that is merely
   invisible. assets/facets.js sets the hidden attribute for the same reason;
   this is the half that holds with scripting off, and header.css retires the
   mobile menu button the same way. */
@media (min-width: 768px) {
  .main-collection__filter-toggle {
    display: none;
  }
}

.main-collection__filter-toggle {""",
    'the trigger is retired above --bp-md')
