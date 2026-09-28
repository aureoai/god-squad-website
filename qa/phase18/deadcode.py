# -*- coding: utf-8 -*-
"""Phase 18 — class names and data- hooks that nothing on the other side uses.

The audit reported several of these individually. Scanning for them is more
reliable than taking each report on trust, and it gives a number for the report
rather than a list of anecdotes.

Three questions:

  1. Which classes does the markup emit that no stylesheet matches? Harmless on
     its own, but it is how a renamed component leaves a hook behind, and it is
     what a reader greps for when they want to change something.
  2. Which classes do the stylesheets define that no markup emits? That is
     shipped CSS a customer downloads and can never see.
  3. Which data- attributes does the markup emit that no script reads? Those are
     the contract between Liquid and JS, and a stale one is a trap: the next
     person wires to it and nothing happens.

CAVEATS, because a scanner that overclaims is worse than none. Classes built by
string concatenation in Liquid or added at runtime by JS are invisible to a
static scan, so anything flagged here is a CANDIDATE, checked by hand before
removal. The theme's own conventions produce known-good exceptions — utility
classes applied by script, and `js-` style hooks — and those are listed rather
than silently skipped.
"""
import io
import os
import re
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
THEME = os.environ.get('GS_THEME') or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')

# Added or removed at runtime, so a static scan cannot see the markup side.
RUNTIME_CLASSES = {
    'is-open', 'is-closing', 'is-active', 'is-busy', 'cart-drawer-open',
    'facets-open', 'menu-open', 'header--menu-open', 'facets--drawer',
    'cart-js', 'no-js', 'js', 'surface-light', 'surface-dark',
    'shopify-section', 'visually-hidden', 'visually-hidden--until-focus',
    'skip-link', 'container', 'container--wide', 'container--narrow',
}


def read_all(*exts):
    out = {}
    for root, _d, fs in os.walk(THEME):
        for f in sorted(fs):
            if f.endswith(exts):
                p = os.path.join(root, f)
                out[os.path.relpath(p, THEME).replace(os.sep, '/')] = \
                    io.open(p, encoding='utf-8').read()
    return out


liquid = read_all('.liquid')
css = read_all('.css')
js = read_all('.js')
jsonf = read_all('.json')

liquid_all = '\n'.join(liquid.values())
css_all = '\n'.join(css.values())
js_all = '\n'.join(js.values())
json_all = '\n'.join(jsonf.values())


def strip_css_comments(s):
    return re.sub(r'/\*.*?\*/', '', s, flags=re.S)


def strip_liquid_comments(s):
    s = re.sub(r'\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}', '', s, flags=re.S)
    return re.sub(r'(?m)^\s*comment\b.*?^\s*endcomment\b', '', s, flags=re.S)


# ------------------------------------------------ classes emitted by markup
emitted = defaultdict(set)
for rel, s in liquid.items():
    body = strip_liquid_comments(s)
    for m in re.finditer(r'class="([^"]*)"', body):
        attr = m.group(1)
        # Skip the WHOLE attribute if any Liquid appears in it. Splitting first
        # and dropping only the brace tokens let the variable NAME through --
        # class="{{ classes }}" yielded a literal class called `classes`, and
        # the orphan list filled up with `endif`, `handle` and `cta_variant`.
        if '{' in attr or '}' in attr:
            continue
        for c in attr.split():
            emitted[c].add(rel)

# ------------------------------------------------ classes defined in CSS
defined = defaultdict(set)
for rel, s in css.items():
    body = strip_css_comments(s)
    # Every selector, at ANY nesting depth. The first version anchored to the
    # start of a line, which silently skipped every rule inside an @media block
    # -- and this theme puts its responsive and hover rules there, so live
    # classes like .price__current were reported as unstyled.
    for m in re.finditer(r'([^{}]+)\{', body):
        head = m.group(1).strip()
        if head.startswith('@'):
            continue                      # at-rule prelude, not a selector
        for c in re.findall(r'\.([A-Za-z_][\w-]*)', head):
            defined[c].add(rel)

# Classes a script adds or removes.
js_classes = set(re.findall(r"classList\.(?:add|remove|toggle|contains)\(\s*'([\w-]+)'", js_all))
js_classes |= set(re.findall(r"querySelector(?:All)?\(\s*'[^']*?\.([\w-]+)", js_all))
json_classes = set(re.findall(r'"([\w-]+(?:__|--)[\w-]+)"', json_all))

print('=== CLASSES IN MARKUP THAT NO STYLESHEET MATCHES ===')
orphan_markup = sorted(c for c in emitted
                       if c not in defined and c not in RUNTIME_CLASSES
                       and c not in js_classes)
for c in orphan_markup:
    print('  %-44s %s' % (c, ', '.join(sorted(emitted[c]))[:60]))
print('  %d class(es)' % len(orphan_markup))

print()
print('=== CLASSES IN CSS THAT NO MARKUP EMITS ===')
# CONSERVATIVE. snippets/quantity-selector.liquid builds its root class with
# `class="{{ classes }}"` from an assign, so a scan that reads only literal
# class attributes calls `quantity` dead when the stepper plainly exists. A
# class counts as live if its literal text appears ANYWHERE in the Liquid --
# in an assign, a capture, a condition or a comment-free string -- which
# trades some misses for not reporting live components as dead.
liquid_text = strip_liquid_comments(liquid_all)

# The theme builds modifier classes by CONCATENATION, so the full name never
# appears anywhere:
#     assign classes = classes | append: ' hero--pos-' | append:
#                      section.settings.text_position
# A scan that misses this calls every spacing and position modifier dead -- 42
# of them, all live. Collect the prefixes and treat any class starting with one
# as reachable; the schema decides the suffix and only the merchant knows which
# is in use.
BUILT_PREFIXES = set(re.findall(r"append:\s*'\s*([\w-]+-)'", liquid_text))
orphan_css = sorted(c for c in defined
                    if c not in emitted and c not in RUNTIME_CLASSES
                    and c not in js_classes and c not in json_classes
                    and c not in liquid_text
                    and not any(c.startswith(pre) for pre in BUILT_PREFIXES))
for c in orphan_css:
    print('  %-44s %s' % (c, ', '.join(sorted(defined[c]))[:60]))
print('  %d class(es)' % len(orphan_css))

# ------------------------------------------------ data- hooks
print()
print('=== data- ATTRIBUTES EMITTED BUT READ BY NO SCRIPT ===')
emitted_data = defaultdict(set)
for rel, s in liquid.items():
    body = strip_liquid_comments(s)
    for m in re.finditer(r'\s(data-[\w-]+)', body):
        emitted_data[m.group(1)].add(rel)

unread = []
for attr, files in sorted(emitted_data.items()):
    camel = re.sub(r'-(\w)', lambda m: m.group(1).upper(), attr[5:])
    if (attr in js_all or attr in css_all
            or ('dataset.' + camel) in js_all):
        continue
    unread.append((attr, files))
for attr, files in unread:
    print('  %-40s %s' % (attr, ', '.join(sorted(files))[:60]))
print('  %d attribute(s)' % len(unread))

print()
print('%d markup-orphan class(es), %d css-orphan class(es), %d unread data hook(s)'
      % (len(orphan_markup), len(orphan_css), len(unread)))
print('Every one is a CANDIDATE. Confirm by hand before removing: a class built')
print('by Liquid concatenation or added by a script is invisible to this scan.')
