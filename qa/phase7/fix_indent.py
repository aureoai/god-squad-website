# -*- coding: utf-8 -*-
"""The media block came out two spaces deep.

Swapping the wrapper and the guard did not change the nesting depth of what is
inside them, so the re-indent in fix_review.py was one step too many.
"""
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\sections\our-story.liquid"
s = open(p, encoding='utf-8').read()

start = s.index('    <div class="our-story__media">\n') + len('    <div class="our-story__media">\n')
end = s.index('      <div class="our-story__scrim" aria-hidden="true"></div>\n')
body = s[start:end]

out = []
for ln in body.split('\n'):
    if ln.startswith('  ') and ln.strip():
        out.append(ln[2:])
    else:
        out.append(ln)
body2 = '\n'.join(out)
assert body2 != body
s = s[:start] + body2 + s[end:]
open(p, 'w', encoding='utf-8', newline='').write(s)
print('media block de-indented by one step')
