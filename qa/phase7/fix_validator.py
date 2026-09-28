# -*- coding: utf-8 -*-
"""Scope the hard-coded-asset check to the Liquid body.

It fired on the image setting's own help text, which names the canonical asset
for the merchant — "images/our-story.webp in the project" — because the Phase 7
brief asks the section to point at the approved asset the Phase 3 manifest
identifies. Naming it in the editor is the requirement; hard-coding it in the
markup is the prohibition. The check was reading both.
"""
p = (r"C:\Users\TEST\AppData\Local\Temp\claude"
     r"\C--Users-TEST-OneDrive-Documents-GodSquad-Website"
     r"\de238d03-508d-43ce-a377-210f71ff0033\scratchpad\phase7\validate.py")
s = open(p, encoding='utf-8').read()

old = """schema = json.loads(re.search(r'\\{%\\s*schema\\s*%\\}(.*?)\\{%\\s*endschema\\s*%\\}', story, re.S).group(1))"""
new = """schema = json.loads(re.search(r'\\{%\\s*schema\\s*%\\}(.*?)\\{%\\s*endschema\\s*%\\}', story, re.S).group(1))
# The Liquid BODY, with the schema removed. Prohibitions about markup apply
# here; the schema's help text is documentation and is checked separately.
storybody = strip_liquid(re.sub(r'\\{%\\s*schema\\s*%\\}.*?\\{%\\s*endschema\\s*%\\}', '', story, flags=re.S))"""
assert old in s, 'schema parse line not found'
s = s.replace(old, new, 1)

old2 = """check("no image asset path is hard-coded", not re.search(r'\\.(webp|png|jpe?g)', storyc))"""
new2 = """check("no image asset path is hard-coded in the markup",
      not re.search(r'\\.(webp|png|jpe?g)', storybody))
check("the schema names the canonical asset for the merchant",
      'images/our-story.webp' in story and '2000px' in story)"""
assert old2 in s, 'asset path check not found'
s = s.replace(old2, new2, 1)
open(p, 'w', encoding='utf-8', newline='').write(s)
print('validate.py: asset-path check scoped to the markup')
