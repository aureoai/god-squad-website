# -*- coding: utf-8 -*-
"""Phase 18 — build the .container utility Phase 2 specified and never shipped.

PHASE-2-DESIGN-SYSTEM.md section 8 defines it exactly:

    .container { width: 100%; max-width: var(--container-standard);
                 margin-inline: auto; padding-inline: var(--gutter); }
    .container--wide   { max-width: var(--container-wide); }
    .container--narrow { max-width: var(--container-narrow); }

and shows the markup it belongs in. The implementation never built it, so
twelve elements across eleven stylesheets each carry a private copy of the same
four declarations. Verified before touching anything: all twelve are byte-
identical, all use --container-standard and --gutter, and NONE is overridden at
a breakpoint — so this is a pure consolidation with no rendered change.

Three rules are deliberately left alone: .header__search-form,
.main-page__column and .main-search__form use a narrow width WITHOUT gutter
padding, so .container--narrow would add padding they do not have. They are
noted in the component file rather than forced into it.
"""
import io
import os
import re

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
# (stylesheet, selector, liquid file, the class attribute as written)
TARGETS = [
    ('header.css', '.header__inner', 'sections/header.liquid', 'header__inner'),
    ('section-featured-collection.css', '.featured-collection__inner',
     'sections/featured-collection.liquid', 'featured-collection__inner'),
    ('section-footer.css', '.footer__inner', 'sections/footer.liquid', 'footer__inner'),
    ('section-hero.css', '.hero__inner', 'sections/hero.liquid', 'hero__inner'),
    ('section-main-404.css', '.main-404__inner', 'sections/main-404.liquid', 'main-404__inner'),
    ('section-main-cart.css', '.main-cart__inner', 'sections/main-cart.liquid', 'main-cart__inner'),
    ('section-main-collection.css', '.main-collection__inner',
     'sections/main-collection.liquid', 'main-collection__inner'),
    ('section-main-page.css', '.main-page__inner', 'sections/main-page.liquid', 'main-page__inner'),
    ('section-main-product.css', '.main-product__inner',
     'sections/main-product.liquid', 'main-product__inner'),
    ('section-main-search.css', '.main-search__inner',
     'sections/main-search.liquid', 'main-search__inner'),
    ('section-our-story.css', '.our-story__inner', 'sections/our-story.liquid', 'our-story__inner'),
    ('section-our-story.css', '.our-story__values', 'sections/our-story.liquid', 'our-story__values'),
]

CONTAINER_DECLS = [
    'width: 100%',
    'max-width: var(--container-standard)',
    'margin-inline: auto',
    'padding-inline: var(--gutter)',
]


def read(rel):
    return io.open(os.path.join(THEME, rel), encoding='utf-8').read()


def write(rel, s):
    io.open(os.path.join(THEME, rel), 'w', encoding='utf-8').write(s)


# ============================================================ the component
COMPONENT = """/* ============================================================================
   GOD SQUAD — Container
   Phase 18. The content column, as one utility.

   PHASE-2-DESIGN-SYSTEM.md section 8 specifies this class, its two modifiers
   and the markup they belong in. The implementation never built it, so twelve
   elements across eleven stylesheets each grew a private copy of the same four
   declarations — the width of the site defined twelve times, and twelve places
   to miss if it ever changes.

   Verified before consolidating: all twelve were byte-identical, all used
   --container-standard with --gutter, and none was overridden at a breakpoint.
   Nothing about the rendered page changes.

   NOT EVERY max-width IS A CONTAINER. Three rules use a narrow width with no
   gutter padding — .header__search-form, .main-page__column and
   .main-search__form — and .container--narrow would give them padding they
   deliberately do not have. They keep their own declarations, and this note is
   here so the next person does not "finish the job" by sweeping them in.
   ========================================================================== */

.container {
  width: 100%;
  max-width: var(--container-standard);
  margin-inline: auto;
  padding-inline: var(--gutter);
}

/* The two modifiers Phase 2 defines. --wide is for full-width editorial
   imagery, --narrow for long-form reading. Neither has a consumer yet; they
   are here because the utility is incomplete without them and because a
   section that needs one should find it rather than invent a width. */
.container--wide {
  max-width: var(--container-wide);
}

.container--narrow {
  max-width: var(--container-narrow);
}
"""
write('assets/component-container.css', COMPONENT)
print('  ok  %-34s created' % 'assets/component-container.css')

# =============================================== link it, first of the components
layout = read('layout/theme.liquid')
anchor = """    {{ 'component-button.css' | asset_url | stylesheet_tag }}"""
assert layout.count(anchor) == 1
layout = layout.replace(anchor, """    {%- comment -%}
      Phase 18. The content column, which Phase 2 section 8 specified and the
      implementation never built — twelve private copies of four declarations
      until now. First of the components, because every other one sits inside
      it.
    {%- endcomment -%}
    {{ 'component-container.css' | asset_url | stylesheet_tag }}
""" + anchor, 1)
write('layout/theme.liquid', layout)
print('  ok  %-34s component-container.css linked' % 'layout/theme.liquid')

# ============================================ strip the copies, tag the markup
for css_file, selector, liquid_file, cls in TARGETS:
    css = read('assets/' + css_file)
    # The rule body for this exact selector.
    m = re.search(r'(?m)^' + re.escape(selector) + r'\s*\{([^}]*)\}', css)
    if not m:
        raise SystemExit('rule not found: %s in %s' % (selector, css_file))
    body = m.group(1)
    kept = []
    for decl in body.split(';'):
        if not decl.strip():
            continue
        if any(decl.strip() == d for d in CONTAINER_DECLS):
            continue
        kept.append(decl.strip())
    if kept:
        new_rule = selector + ' {\n  ' + ';\n  '.join(kept) + ';\n}'
    else:
        new_rule = ''      # the rule was nothing but the container
    css = css[:m.start()] + new_rule + css[m.end():]
    css = re.sub(r'\n{3,}', '\n\n', css)
    write('assets/' + css_file, css)

    lq = read(liquid_file)
    old_attr = 'class="%s"' % cls
    if lq.count(old_attr) != 1:
        raise SystemExit('class attribute not unique in %s: %s' % (liquid_file, cls))
    write(liquid_file, lq.replace(old_attr, 'class="%s container"' % cls, 1))
    print('  ok  %-34s %-30s %s' % (css_file, selector,
                                    'rule removed' if not kept else '%d decl(s) kept' % len(kept)))
