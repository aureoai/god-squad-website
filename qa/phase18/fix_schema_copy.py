# -*- coding: utf-8 -*-
"""Phase 18 — take the project's own vocabulary out of the merchant's editor.

Ten schema strings a shop owner reads in the Theme Editor refer to "the
prototype", "the approved mockup", "the rebuild", "Phase 3 records", "Phase 2
§26.1" and "BUSINESS INFORMATION REQUIRED". None of that means anything to the
person running the shop. Worse, one of them tells a merchant their hero image
is "AI-generated and unverified" in the voice of an internal audit rather than
as the instruction it needs to be.

THE SUBSTANCE STAYS. Every one of these says something the merchant genuinely
needs — the hero image needs confirming before launch, the logo needs a vector
master, no favicon exists, contact details are not invented. The rewrite keeps
the instruction and drops the project archaeology. Where a string said
"BUSINESS INFORMATION REQUIRED" it now says plainly that the theme supplies
nothing and the merchant must, which is the same gate in the merchant's own
language.

The internal record of WHY each gap exists stays where it belongs: in the phase
documents and in the Liquid comments above these schemas, both of which the
merchant never opens.
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
# (relative file, exact old string, new string)
JOBS = [
    ('sections/announcement-bar.liquid',
     'Optional, shown at 16px. The prototype places a gold globe beside the shipping message.',
     'Optional, shown at 16px. A small icon sits beside the message \u2014 a globe suits a shipping announcement.'),

    ('sections/footer.liquid',
     "The prototype's own footer line, kept so the approved composition survives the rebuild. "
     "It is not a heading and nothing else on the page depends on it, so clearing it simply "
     "removes the line.",
     'A short line above the footer columns. It is not a heading and nothing else depends on '
     'it, so clearing it simply removes the line.'),

    ('sections/footer.liquid',
     'Sits beside the copyright on the bottom row, which is where the prototype put it.',
     'Sits beside the copyright on the bottom row.'),

    ('sections/footer.liquid',
     'The addresses live in Theme settings, because they are the same on every page. Which '
     'accounts the brand actually operates is BUSINESS INFORMATION REQUIRED: the prototype '
     'linked Facebook and Instagram to nowhere, and the approved mockup shows four networks. '
     'Each link appears only once its address is filled in.',
     'The addresses live in Theme settings, because they are the same on every page. Add only '
     'the accounts you actually operate \u2014 each icon appears once its address is filled in, '
     'and none is shown otherwise.'),

    ('sections/footer.liquid',
     'Build the menu in Navigation. Which groups the footer carries, and what goes in them, is '
     'BUSINESS INFORMATION REQUIRED \u2014 no footer menu exists in the prototype or the mockup. '
     'A column with no links does not render on the live store.',
     'Build the menu in Navigation, then choose it here. The theme ships no footer menu of its '
     'own, and a column with no links does not render on the live store.'),

    ('sections/footer.liquid',
     'Contact details belong here. The theme supplies none: an address, an email or a phone '
     'number is BUSINESS INFORMATION REQUIRED and nothing is guessed.',
     'Contact details belong here. The theme supplies none and guesses nothing \u2014 add the '
     'address, email or phone number you want customers to use.'),

    ('sections/hero.liquid',
     'The approved hero. Phase 3 records its provenance as AI-generated and unverified; '
     'confirm before launch.',
     'The hero image. The image currently supplied with the theme is AI-generated and its '
     'rights are unconfirmed \u2014 replace it with your own photography, or confirm you are '
     'cleared to use it, before you launch.'),

    ('sections/our-story.liquid',
     'One paragraph is the house default: Phase 2 \u00a726.1 gives this band a single body '
     'paragraph. The Phase 7 brief allows up to four short ones, so the field accepts them, '
     'and the column is capped at a reading measure \u2014 longer copy makes the band taller '
     'rather than the lines wider.',
     'One paragraph reads best here, though the field accepts up to about four short ones. '
     'The column is capped at a comfortable reading width, so longer copy makes the band '
     'taller rather than the lines wider.'),

    ('config/settings_schema.json',
     'A transparent PNG or, better, an SVG. Phase 3 records that the current wordmark carries '
     'heavy transparent padding, so it renders at roughly half its intended size until a '
     'vector master replaces it.',
     'A transparent PNG or, better, an SVG. The wordmark supplied with the theme carries heavy '
     'transparent padding and renders at roughly half its intended size \u2014 upload a vector '
     'master to fix it.'),

    ('config/settings_schema.json',
     'None exists yet. Phase 3 records that /favicon.ico returns 404 on every load, and that a '
     'favicon cannot be derived properly until a vector logo is supplied.',
     'None is supplied, so browsers currently show their default mark. Upload a square image '
     '\u2014 a vector logo gives the cleanest result at small sizes.'),
]

changed = 0
for rel, old, new in JOBS:
    p = os.path.join(THEME, rel.replace('/', os.sep))
    s = io.open(p, encoding='utf-8').read()
    n = s.count(old)
    if n != 1:
        print('  *** %-38s %d matches, expected 1 — SKIPPED' % (rel, n))
        continue
    io.open(p, 'w', encoding='utf-8').write(s.replace(old, new, 1))
    changed += 1
    print('  ok  %-38s %s\u2026' % (rel, new[:52]))

print()
print('%d of %d string(s) rewritten' % (changed, len(JOBS)))
