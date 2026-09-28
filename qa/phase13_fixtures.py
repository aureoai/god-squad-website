# -*- coding: utf-8 -*-
"""Phase 13 — collection.filters fixtures for the mini-Liquid harness.

Shapes taken from shopify.dev's filter and filter_value objects, verified this
phase. Nothing here is invented: every field is one Shopify documents, and the
values are the ones a real Search & Discovery configuration would produce for an
apparel store.

The three filter TYPES are all represented, because the section branches on
filter.type and an untested branch is an unwritten one:
  list        — Size, Colour (the common case, with counts and a swatch variant)
  boolean     — Availability
  price_range — Price
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
TARGETS = [os.path.join(BASE, 'phase9', 'build.py')]

BLOCK = '''

# ---------------------------------------------------------------- filters
# Phase 13. collection.filters, as Shopify's Search & Discovery app produces it.
# Field names and types are from shopify.dev's filter / filter_value objects.
#
# The URL forms are Shopify's own: a value is added with url_to_add and removed
# with url_to_remove, and BOTH strip pagination parameters, which is why a
# filtered collection always lands the customer back on page 1.


def filter_value(label, value, param, count, active=False, swatch=None):
    base = '/collections/the-faithful?' + param + '=' + value
    v = {
        'label': label,
        'value': value,
        'param_name': param,
        'count': count,
        'active': active,
        'url_to_add': base,
        'url_to_remove': '/collections/the-faithful',
    }
    if swatch is not None:
        v['swatch'] = wrap({'color': swatch})
    return wrap(v)


def list_filter(label, param, values, presentation='text'):
    active = [v for v in values if v['active']]
    inactive = [v for v in values if not v['active']]
    return wrap({
        'label': label,
        'type': 'list',
        'param_name': param,
        'operator': 'OR',
        'presentation': presentation,
        'values': values,
        'active_values': active,
        'inactive_values': inactive,
        'url_to_remove': '/collections/the-faithful',
    })


def boolean_filter(label, param, true_count, false_count, active=None):
    t = filter_value('In stock', '1', param, true_count, active == 'true')
    f = filter_value('Out of stock', '0', param, false_count, active == 'false')
    vals = [t, f]
    return wrap({
        'label': label,
        'type': 'boolean',
        'param_name': param,
        'operator': 'OR',
        'values': vals,
        'active_values': [v for v in vals if v['active']],
        'inactive_values': [v for v in vals if not v['active']],
        'true_value': t,
        'false_value': f,
        'url_to_remove': '/collections/the-faithful',
    })


def price_filter(range_max, gte=None, lte=None):
    """min_value/max_value are nil unless the customer has set them."""
    mn = filter_value('', str(gte), 'filter.v.price.gte', None) if gte is not None else BLANK
    mx = filter_value('', str(lte), 'filter.v.price.lte', None) if lte is not None else BLANK
    return wrap({
        'label': 'Price',
        'type': 'price_range',
        'param_name': 'filter.v.price',
        'min_value': mn,
        'max_value': mx,
        'range_max': range_max,
        'url_to_remove': '/collections/the-faithful',
        'values': [],
        'active_values': [],
        'inactive_values': [],
    })


def size_filter(active_labels=()):
    vals = [filter_value(lbl, lbl, 'filter.v.option.size', n, lbl in active_labels)
            for lbl, n in (('S', 4), ('M', 6), ('L', 5), ('XL', 2))]
    return list_filter('Size', 'filter.v.option.size', vals)


def colour_filter(active_labels=()):
    vals = [filter_value(lbl, lbl.lower(), 'filter.v.option.color', n,
                         lbl in active_labels, swatch=hexv)
            for lbl, n, hexv in (('Black', 7, '#0D0C0A'),
                                 ('Cream', 3, '#F3EFE6'),
                                 ('Olive', 2, '#4B5443'))]
    return list_filter('Colour', 'filter.v.option.color', vals, presentation='swatch')


FILTERS_NONE = []
FILTERS_ALL = [size_filter(), colour_filter(),
               boolean_filter('Availability', 'filter.v.availability', 12, 3),
               price_filter(299000)]
FILTERS_ACTIVE = [size_filter(('L',)), colour_filter(('Black',)),
                  boolean_filter('Availability', 'filter.v.availability', 12, 3, active='true'),
                  price_filter(299000, gte=100000)]
# A group Shopify returns with a single value carries no information: the
# section is expected to drop it rather than render a one-option control.
FILTERS_DEGENERATE = [
    list_filter('Vendor', 'filter.p.vendor',
                [filter_value('God Squad', 'god-squad', 'filter.p.vendor', 12)]),
    size_filter(),
]
'''


def main():
    for p in TARGETS:
        s = open(p, encoding='utf-8').read()
        if 'def list_filter(' in s:
            print('already present:', p)
            continue
        assert 'BLANK' in s or 'from miniliquid import' in s, 'unexpected build.py shape'
        open(p, 'w', encoding='utf-8', newline='').write(s.rstrip('\n') + BLOCK)
        print('filters fixtures added to', os.path.basename(p))


if __name__ == '__main__':
    main()
