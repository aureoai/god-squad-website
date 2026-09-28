# -*- coding: utf-8 -*-
"""Clear the overlaying header when this section is the first one on the page.

The Phase 4 header overlays the first section of the index template. Phase 5
gave the hero clearance by consuming --header-overlay-offset. Nothing stopped a
merchant from reordering the home page so a collection row came first, and the
render of that case put the heading underneath the navigation.

Adding the offset unconditionally would push every collection row down by the
header's height even when it sits third, so it is scoped to the first section
and composed with, rather than replacing, the merchant's spacing choice.
"""
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\section-featured-collection.css"
s = open(p, encoding='utf-8').read()

old = """/* Spacing is a choice between three system values, not a free pixel field. A
   raw number would let one band fall off the section rhythm that Phase 2
   section 7.4 defines. */
.featured-collection--pt-standard { padding-block-start: var(--section-pad-block); }
.featured-collection--pt-tight    { padding-block-start: var(--section-pad-block-tight); }
.featured-collection--pt-none     { padding-block-start: 0; }
.featured-collection--pb-standard { padding-block-end: var(--section-pad-block); }
.featured-collection--pb-tight    { padding-block-end: var(--section-pad-block-tight); }
.featured-collection--pb-none     { padding-block-end: 0; }"""

new = """/* Spacing is a choice between three system values, not a free pixel field. A
   raw number would let one band fall off the section rhythm that Phase 2
   section 7.4 defines.

   The chosen value lands in a custom property rather than straight into
   padding, so the header clearance below can be added to it instead of
   replacing it. */
.featured-collection {
  --fc-space-top: 0px;
  --fc-space-bottom: 0px;
  padding-block: calc(var(--fc-header-clearance, 0px) + var(--fc-space-top)) var(--fc-space-bottom);
}

.featured-collection--pt-standard { --fc-space-top: var(--section-pad-block); }
.featured-collection--pt-tight    { --fc-space-top: var(--section-pad-block-tight); }
.featured-collection--pt-none     { --fc-space-top: 0px; }
.featured-collection--pb-standard { --fc-space-bottom: var(--section-pad-block); }
.featured-collection--pb-tight    { --fc-space-bottom: var(--section-pad-block-tight); }
.featured-collection--pb-none     { --fc-space-bottom: 0px; }

/* The Phase 4 header overlays the FIRST section of the home page, and Phase 5
   gave the hero clearance by consuming --header-overlay-offset. Nothing stops a
   merchant reordering the page so a collection row comes first; rendered, that
   put the heading underneath the navigation. This gives the same clearance, and
   only to a section that is actually first. The custom property resolves to 0
   whenever the header is not overlaying, so a section that is first on a
   template without an overlaying header pays nothing. */
main > .shopify-section:first-child .featured-collection {
  --fc-header-clearance: var(--header-overlay-offset, 0px);
}"""

assert old in s, 'spacing block not found'
open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new, 1))
print('section-featured-collection.css: first-section header clearance added')
