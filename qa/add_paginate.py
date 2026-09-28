# -*- coding: utf-8 -*-
"""Implement {% paginate %} in mini-Liquid.

Phase 10 added two surfaces that cannot render without it — main-collection and
main-search both wrap their grid in {% paginate ... by n %}. Until now the tag
raised "unimplemented", so neither surface could be rendered even once.

Shopify's semantics, which this models:
  - the paginated expression yields only the CURRENT PAGE's items inside the
    block, so `for product in collection.products` iterates a page, not the
    catalogue;
  - a `paginate` object is in scope carrying the counts and the link parts.

The slice is installed by swapping the owning object's key for the duration of
the block and restoring it afterwards, which is the closest honest model of
what Shopify does and keeps the swap invisible outside the block.
"""
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
NL = chr(10)

METHOD = '''
    def _paginate(self, env, toks, i, rest):
        """{% paginate <path> by <n> %} ... {% endpaginate %}"""
        m = re.match(r'^(.+?)\\s+by\\s+(.+)$', rest.strip(), re.S)
        if not m:
            raise LiquidError('malformed paginate: %r' % rest)
        path = m.group(1).strip()
        try:
            size = int(float(_s(evaluate(env, m.group(2).strip()))))
        except (TypeError, ValueError):
            raise LiquidError('paginate size is not a number: %r' % m.group(2))
        if size < 1:
            raise LiquidError('paginate size must be >= 1, got %d' % size)

        full = evaluate(env, path)
        items = list(full) if full else []
        total = len(items)
        pages = 1 if total == 0 else (total + size - 1) // size
        current = 1
        page_items = items[:size]

        parts = []
        if pages > 1:
            for n in range(1, pages + 1):
                parts.append(wrap({
                    'title': str(n),
                    'url': '' if n == current else '?page=%d' % n,
                    'is_link': n != current,
                }))
        pg = wrap({
            'items': total,
            'pages': pages,
            'page_size': size,
            'current_page': current,
            'current_offset': 0,
            'parts': parts,
            'previous': wrap({'title': 'Previous', 'url': '', 'is_link': False}),
            'next': wrap({
                'title': 'Next',
                'url': '?page=2' if pages > 1 else '',
                'is_link': pages > 1,
            }),
        })

        # Swap in the page slice for the duration of the block, exactly where the
        # template will look for it, then put the full list back.
        owner = None
        key = None
        if '.' in path:
            owner = evaluate(env, path.rsplit('.', 1)[0])
            key = path.rsplit('.', 1)[1]
        previous_value = None
        swapped = False
        if owner is not None and hasattr(owner, '__setitem__') and key:
            try:
                previous_value = owner[key]
                owner[key] = page_items
                swapped = True
            except Exception:
                swapped = False

        inner = Env(env.scopes + [{'paginate': pg}], env.engine)
        try:
            body, j = self._block(inner, toks, i + 1, {'endpaginate'})
        finally:
            if swapped:
                owner[key] = previous_value
        return body, j
'''

p = os.path.join(BASE, 'phase9', 'miniliquid.py')
s = open(p, encoding='utf-8').read()

OLD_DISPATCH = """        if name in ('paginate', 'endpaginate'):
            raise LiquidError('unimplemented tag: %s' % name)"""
NEW_DISPATCH = """        if name == 'paginate':
            return self._paginate(env, toks, i, rest)"""
assert s.count(OLD_DISPATCH) == 1, 'paginate dispatch not found'
s = s.replace(OLD_DISPATCH, NEW_DISPATCH, 1)

anchor = "    def _form(self, env, toks, i, rest):"
assert s.count(anchor) == 1, 'anchor method not found'
s = s.replace(anchor, METHOD.strip(NL) + NL + NL + anchor, 1)

open(p, 'w', encoding='utf-8', newline='').write(s)
print('phase9/miniliquid.py: {% paginate %} implemented')
