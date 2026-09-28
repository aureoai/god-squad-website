# -*- coding: utf-8 -*-
"""Write full pages for the five Phase 10 surfaces so respond.py can measure them.

surfaces.py proves each section RENDERS. This builds real pages — header, the
surface, the footer, the drawer — so the responsive sweep can measure overflow,
touch targets, grid columns and type at all twelve viewports, exactly as it
already does for home, product and cart.

The footer is appended to every page because in production it comes from the
layout's footer group, which means it is on every page and must be measured on
every page.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build  # noqa: E402
import surfaces  # noqa: E402


def header_html(engine):
    return build.render_section(engine, 'sections/header.liquid', 'header',
                                dict(build.HEADER_SETTINGS))


def drawer_html(engine):
    return build.render_section(engine, 'sections/cart-drawer.liquid', 'cart-drawer',
                                dict(build.DRAWER_DEFAULTS))


def page(name, section, sid, template, settings=None, blocks=None, **globals_):
    """One harness page: header + the surface + footer + drawer."""
    base, _ = surfaces.schema_defaults(section)
    if settings:
        base.update(settings)
    engine = surfaces.engine(template=template, **globals_)
    part = (sid, build.render_section(engine, 'sections/%s.liquid' % section,
                                      sid, base, blocks))
    # The footer is NOT a body part. build.write puts it after </main>, where
    # layout/theme.liquid:305 puts it -- passing it here as a part is what used
    # to nest a role="contentinfo" landmark inside <main id="MainContent">.
    # demo_footer_blocks adds one menu column so .footer__heading and
    # .footer__menu exist somewhere to be measured; the shipped group has none.
    build.write(name, [part], header_html(engine), drawer_html(engine),
                template=template, engine=engine, demo_footer_blocks=True)
    return name


if __name__ == '__main__':
    written = []
    written.append(page('s-collection.html', 'main-collection', 'coll', 'collection',
                        collection=surfaces.COLL))

    # Phase 13. The same collection with filters configured, and with filters
    # applied — the two states a merchant with Search & Discovery actually has.
    from miniliquid import wrap as _wrap
    def _with(filters):
        c = dict(surfaces.COLL)
        c['filters'] = filters
        return _wrap(c)
    written.append(page('s-collection-filters.html', 'main-collection', 'coll', 'collection',
                        collection=_with(build.FILTERS_ALL)))
    written.append(page('s-collection-filtered.html', 'main-collection', 'coll', 'collection',
                        collection=_with(build.FILTERS_ACTIVE)))
    written.append(page('s-collection-empty.html', 'main-collection', 'coll', 'collection',
                        collection=surfaces.COLL_EMPTY))
    written.append(page('s-page.html', 'main-page', 'pg', 'page',
                        page=surfaces.PAGE))
    written.append(page('s-404.html', 'main-404', 'nf', '404'))
    written.append(page('s-search.html', 'main-search', 'sr', 'search',
                        search=surfaces.SEARCH_HITS))
    written.append(page('s-search-none.html', 'main-search', 'sr', 'search',
                        search=surfaces.SEARCH_NONE))

    for n in written:
        p = os.path.join(build.OUT, n)
        size = os.path.getsize(p)
        print('  %-26s %7d bytes' % (n, size))
    print()
    print('%d surface pages written' % len(written))
