# -*- coding: utf-8 -*-
import io
p = (r"C:\Users\TEST\.claude\projects\C--Users-TEST-OneDrive-Documents-GodSquad-Website"
     r"\memory\MEMORY.md")
s = open(p, encoding='utf-8').read()

old = ("- [GOD SQUAD phased roadmap](godsquad-phased-roadmap.md) \u2014 17 gated phases; "
       "Phases 0-5 delivered, awaiting Phase 6 spec")
new = ("- [GOD SQUAD phased roadmap](godsquad-phased-roadmap.md) \u2014 17 gated phases; "
       "Phases 0-6 delivered, awaiting Phase 7 spec")
assert old in s, 'roadmap line not found'
s = s.replace(old, new, 1)

lines = [
    ("- [Phase 6 collections status](godsquad-phase6-status.md) \u2014 delivered 2026-09-22; "
     "one section two presets, grid column settings are ceilings, mobile menu tab-order "
     "defect awaiting your call\n"),
    ("- [Mini-Liquid QA harness](godsquad-miniliquid-harness.md) \u2014 renders the real "
     ".liquid files against mock Shopify data; reuse it, do not hand-write fixtures\n"),
]
s = s.rstrip('\n') + '\n'
for l in lines:
    if l not in s:
        s += l
open(p, 'w', encoding='utf-8', newline='').write(s)
out = io.TextIOWrapper(__import__('sys').stdout.buffer, encoding='utf-8', errors='replace')
out.write(s)
out.flush()
