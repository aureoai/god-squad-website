# -*- coding: utf-8 -*-
"""The header's two Phase 9 findings.

1. The closed mobile panel kept every one of its links in the tab order. The
   panel is display:flex, and an author class beats the user agent's
   [hidden]{display:none} at equal specificity, so `hidden` removed it from
   view and from nothing else. Measured: the page has the same number of
   reachable controls with the menu shut as with it open.

   This has been carried in the phase documents since Phase 6 as a known
   defect awaiting a phase that was allowed to touch the header. Phase 9 is
   that phase — it is asked to verify focus management across the storefront.

2. The skip link is 38px tall. Phase 2 §23.7 specifies --target-min.
"""
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\header.css"
s = open(p, encoding='utf-8').read()
done = []


def sub(old, new, label):
    global s
    assert old in s, 'NOT FOUND: ' + label
    assert s.count(old) == 1, 'AMBIGUOUS: ' + label
    s = s.replace(old, new, 1)
    done.append(label)


sub(""".header__panel {
  position: fixed;""",
    """/* The closed panel is display:none, and that rule has to be written here.
   .header__panel below sets display:flex, and an author class beats the user
   agent's [hidden]{display:none} at equal specificity — so before this, the
   panel was hidden from sight by translateX(-100%) alone and every link
   inside it stayed in the tab order on every page. A keyboard user pressing
   Tab from the logo walked five invisible menu links.

   It does not cost the slide: assets/header.js sets hidden=false, forces a
   reflow, and only then adds the open class, which is exactly the sequence a
   transition out of display:none needs. */
.header__panel[hidden] {
  display: none;
}

.header__panel {
  position: fixed;""",
    'the closed menu panel leaves the tab order')

sub("""  transform: translateX(-100%);
  transition: transform var(--transition-medium);
  overflow-y: auto;
  overscroll-behavior: contain;
}""",
    """  transform: translateX(-100%);
  transition: transform var(--transition-medium);
  overflow-y: auto;
  overscroll-behavior: contain;
}

/* The panel is fixed to the viewport edges, so on a phone with a home
   indicator or a notch its first and last controls sit under the system UI.
   max() keeps the designed padding wherever there is no inset to respect. */
@supports (padding: max(0px)) {
  .header__panel {
    padding-block-start: max(var(--space-5), env(safe-area-inset-top));
    padding-block-end: max(var(--space-8), env(safe-area-inset-bottom));
    padding-inline-start: max(var(--gutter), env(safe-area-inset-left));
  }
}""",
    'the menu panel respects the safe area')

sub("""  padding: var(--space-3) var(--space-5);
  background-color: var(--color-bg-primary);
  color: var(--color-text-primary);""",
    """  /* --target-min tall, which Phase 2 §23.7 specifies and which the brief
     repeats: the skip link is the first control a keyboard user reaches, and
     it was 38px. */
  display: inline-flex;
  align-items: center;
  min-height: var(--target-min);
  padding: var(--space-3) var(--space-5);
  background-color: var(--color-bg-primary);
  color: var(--color-text-primary);""",
    'the skip link meets the target minimum')

open(p, 'w', encoding='utf-8', newline='').write(s)
for i, label in enumerate(done, 1):
    print('%d. %s' % (i, label))
