# -*- coding: utf-8 -*-
"""Split the global element layer out of design-tokens.css into assets/base.css.

Phase 1 section 29.1 names base.css as the theme's global layer and the Phase 10
brief's target tree repeats it. Today the reset, the focus ring and the
reduced-motion suppression sit at the bottom of a file called design-tokens.css,
which is a misnomer: a token file should define custom properties and nothing
else.

The split is drawn so that NO token definition moves. design-tokens.css keeps
every :root assignment, including the two gutter breakpoints and the
reduced-motion token overrides, because splitting a token's definition across
two files would be worse than the misnomer. base.css takes only the rules that
style ELEMENTS.
"""
import os

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'god-squad-theme')
tok_path = os.path.join(THEME, 'assets', 'design-tokens.css')
s = open(tok_path, encoding='utf-8').read()

MOVE_RESET = """*, *::before, *::after { box-sizing: border-box; }

/* The user agent's 8px body margin would inset every full-bleed band, so the
   container model in section 8 — full-bleed section, constrained content —
   could never reach the viewport edge. Measured in Phase 6: every band came
   out 16px narrower than the viewport at every width until this was added. */
body { margin: 0; }

:where(a, button, input, select, textarea, summary, [tabindex]):focus-visible {
  outline: var(--focus-width) solid var(--focus-ring);
  outline-offset: var(--focus-offset);
}

"""

MOVE_MOTION = """  *, *::before, *::after {
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 1ms !important;
    scroll-behavior: auto !important;
  }
"""

assert s.count(MOVE_RESET) == 1, 'reset block not found verbatim'
assert s.count(MOVE_MOTION) == 1, 'reduced-motion element block not found verbatim'

s = s.replace(MOVE_RESET, '', 1)
s = s.replace(MOVE_MOTION, '', 1)

# The heading now describes only what is left behind.
s = s.replace("""/* ============================================================================
   GLOBAL BEHAVIOUR
   ========================================================================== */

""",
              """/* ============================================================================
   TOKEN REASSIGNMENT BY MEDIA

   The element-level global layer — the reset, the focus ring and the motion
   suppression — moved to assets/base.css in Phase 10. What stays here is what
   belongs in a token file: custom property definitions, including the ones that
   change at a breakpoint or under a user preference. Splitting a single token's
   definition across two files would be worse than the old misnomer.
   ========================================================================== */

""", 1)

open(tok_path, 'w', encoding='utf-8', newline='').write(s)
print('design-tokens.css: element rules removed, every :root definition kept')

BASE = """/* ============================================================================
   GOD SQUAD — base.css

   The global element layer. Phase 10.

   This is the only stylesheet in the theme that styles bare elements. Every
   other file styles a component or a section through a class, which is what
   keeps the cascade flat enough that no rule in this theme needs !important.

   It consumes tokens and defines none: assets/design-tokens.css owns every
   custom property, and is loaded before this file.
   ========================================================================== */

/* Border-box everywhere. Every width in the system — the grid's column floor,
   the drawer's min(90vw, 420px), the container's max-width — is written as the
   outer box, so the content-box default would make all of them wrong. */
*, *::before, *::after {
  box-sizing: border-box;
}

/* The user agent's 8px body margin would inset every full-bleed band, so the
   container model — full-bleed section, constrained content — could never reach
   the viewport edge. Measured in Phase 6: every band came out 16px narrower
   than the viewport at every width until this was added. */
body {
  margin: 0;
}

/* One focus ring for the whole theme, and it is surface-aware: --focus-ring is
   reassigned by the .surface-dark and .surface-light context classes, because
   muted gold is 11.01:1 on ink and 1.55:1 on cream and a single fixed ring
   colour would be invisible on one of them.

   :where() keeps the specificity at zero so a component can override the ring
   without needing to out-specify a selector with seven element names in it.
   :focus-visible rather than :focus, so a pointer user does not get a ring on
   every click while a keyboard user always does. */
:where(a, button, input, select, textarea, summary, [tabindex]):focus-visible {
  outline: var(--focus-width) solid var(--focus-ring);
  outline-offset: var(--focus-offset);
}

/* Motion suppression. The token half of this — --duration-*, --hover-image-scale
   — lives with the other tokens in design-tokens.css; this is the element half,
   which has to reach declarations that were never written as tokens, including
   ones inside third-party or app markup.

   !important is correct here and is the one place in the theme that uses it: a
   user preference must beat an author declaration, which is the only thing
   !important is actually for. */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 1ms !important;
    scroll-behavior: auto !important;
  }
}
"""
base_path = os.path.join(THEME, 'assets', 'base.css')
assert not os.path.exists(base_path), 'base.css already exists'
open(base_path, 'w', encoding='utf-8', newline='').write(BASE)
print('assets/base.css created (%d lines)' % BASE.count('\n'))
