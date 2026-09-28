# -*- coding: utf-8 -*-
"""The copy-rail heading broke mid-word. Measured, then fixed."""
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\section-featured-collection.css"
s = open(p, encoding='utf-8').read()

old = """  text-transform: uppercase;
  /* Phase 2 section 27.6.2: nothing load-bearing is hard-broken, and a
     merchant-entered heading is never text-wrap: balance'd into an
     unexpected shape. It wraps where the column ends. */
  overflow-wrap: anywhere;
}"""

new = """  text-transform: uppercase;
  /* NOT overflow-wrap: anywhere, which is what the prototype used (line 101).
     `anywhere` reduces an element's min-content width to a single character,
     which lets the 0.9fr copy track collapse below the width of its own
     longest word. Measured at 1440: the track came out 353px while FAITHFUL
     at 64px needs about 368px, so the brand word rendered as FAITHFU / L.
     Phase 2 section 27.6.2 forbids hard-breaking anything load-bearing.

     Dropping it restores the track's automatic min-content floor: the rail
     now sizes to its longest word and the product grid takes what is left,
     which is exactly the behaviour the approved composition assumes.
     `break-word` stays as the last resort for a pathological merchant entry;
     unlike `anywhere` it does not affect intrinsic sizing. */
  overflow-wrap: break-word;
}"""

assert old in s, 'heading rule not found'
open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new, 1))
print('section-featured-collection.css: heading no longer breaks mid-word')
