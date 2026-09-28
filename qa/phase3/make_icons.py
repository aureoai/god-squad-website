# -*- coding: utf-8 -*-
"""Author the GOD SQUAD UI icon set as clean SVG.

These are DRAWN to the Phase 2 specification, not traced from the raster PNGs.
Phase 3 spec section 16 forbids blindly converting raster artwork; the existing
icon PNGs are AI-generated with colour baked into the pixels, so tracing them
would carry the artefacts across. These nine are standard geometric UI glyphs
that can be constructed exactly.

Contract, from PHASE-2-DESIGN-TOKENS.css:
  24x24 viewBox            one optical size for the whole set
  stroke-width 1.5         --icon-stroke-width
  stroke: currentColor     inherits --accent-current / text colour per surface
  round caps and joins     matches the prototype's drawn-line character
  fill: none               outline set
  no metadata, no raster, no hard-coded colour

Writes to phase-3-assets/icons/. Creates nothing outside that folder.
"""
import os, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
OUT = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\phase-3-assets\icons"
os.makedirs(OUT, exist_ok=True)

HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" '
        'fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" '
        'stroke-linejoin="round" aria-hidden="true" focusable="false">')

ICONS = {
 # Magnifier: circle plus a 45-degree handle that stops cleanly at the rim.
 'icon-search': '<circle cx="11" cy="11" r="6.25"/><path d="M15.6 15.6 20.5 20.5"/>',

 # Account: head and shoulders, shoulders drawn as an arc rather than a closed body.
 'icon-account': '<circle cx="12" cy="8.25" r="3.75"/><path d="M4.75 19.75a7.25 7.25 0 0 1 14.5 0"/>',

 # Cart: shopping bag, which suits an apparel store better than a trolley.
 'icon-cart': '<path d="M5.5 7.75h13l-1.1 11.3a1.4 1.4 0 0 1-1.4 1.2H8a1.4 1.4 0 0 1-1.4-1.2Z"/>'
              '<path d="M9 10V6.9a3 3 0 0 1 6 0V10"/>',

 # Menu: three rules on the 6/12/18 grid, matching the prototype's hamburger.
 'icon-menu': '<path d="M3.75 6.5h16.5"/><path d="M3.75 12h16.5"/><path d="M3.75 17.5h16.5"/>',

 # Close: the same stroke length as menu, rotated.
 'icon-close': '<path d="M6.4 6.4 17.6 17.6"/><path d="M17.6 6.4 6.4 17.6"/>',

 # Chevron, pointing right. Rotate with CSS for the other three directions.
 'icon-chevron': '<path d="M9.5 5.5 16 12l-6.5 6.5"/>',

 # Arrow, pointing right. Matches the CTA arrow the prototype sets in text.
 'icon-arrow': '<path d="M4 12h15.5"/><path d="M13.5 6 19.5 12l-6 6"/>',

 'icon-plus': '<path d="M12 4.75v14.5"/><path d="M4.75 12h14.5"/>',
 'icon-minus': '<path d="M4.75 12h14.5"/>',
}

print("Authoring the UI icon set (24x24, stroke 1.5, currentColor):\n")
total = 0
for name, body in ICONS.items():
    svg = HEAD + body + '</svg>\n'
    p = os.path.join(OUT, name + '.svg')
    open(p, 'w', encoding='utf-8', newline='\n').write(svg)
    total += len(svg)
    print("  %-16s %4d bytes" % (name + '.svg', len(svg)))

print("\n  %d icons, %d bytes total (%.1f KB)" % (len(ICONS), total, total / 1024))
print("  the nine raster PNGs they can replace weigh 308,521 bytes")
print("  reduction: %.1f%%" % (100 * (1 - total / 308521)))

print("\n=== validation ===")
import re
for name in ICONS:
    s = open(os.path.join(OUT, name + '.svg'), encoding='utf-8').read()
    checks = {
        'single root': s.count('<svg') == 1 and s.count('</svg>') == 1,
        'no raster': 'data:image' not in s and '<image' not in s,
        'no hard colour': not re.search(r'(fill|stroke)="(?!none|currentColor)[^"]+"', s),
        'no metadata': '<metadata' not in s and '<!--' not in s and 'inkscape' not in s,
        'aria-hidden': 'aria-hidden="true"' in s,
        'viewBox 24': 'viewBox="0 0 24 24"' in s,
        'stroke 1.5': 'stroke-width="1.5"' in s,
    }
    bad = [k for k, v in checks.items() if not v]
    print("  %-16s %s" % (name, 'OK' if not bad else '*** ' + ', '.join(bad) + ' ***'))
