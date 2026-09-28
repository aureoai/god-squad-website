# -*- coding: utf-8 -*-
"""Phase 13 — wire facets into sections/main-collection.liquid.

The sort form becomes the surface's ONE form. Every facet control binds to it by
the HTML form attribute, so submitting either the toolbar's button or the
drawer's Apply carries the sort AND every checked filter — which is the defect
the section predicted in writing two phases ago at :36 and :47 ("this section
renders no filter control, so sort_by is the only" parameter).
"""
import collections
import json
import os
import re

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'god-squad-theme')
P = os.path.join(THEME, 'sections', 'main-collection.liquid')
done = []


def patch(old, new, label):
    global s
    assert s.count(old) == 1, 'NOT FOUND or ambiguous: ' + label
    s = s.replace(old, new, 1)
    done.append(label)


s = open(P, encoding='utf-8').read()

# ------------------------------------------------- 1. derive the filter state
patch("""  assign sort_form_id = 'CollectionSort-' | append: section.id""",
      """  comment
    Filters exist only once a merchant has created them in Shopify admin, under
    Apps > Search & Discovery > Filters. Until then collection.filters is empty
    and nothing below renders — no empty Filter button, no empty drawer.

    A group with a single value is dropped by snippets/facets.liquid, so a
    collection that happens to hold one vendor does not get a control whose only
    effect is to filter nothing out. has_filters therefore counts the groups
    that snippet would actually render, not the ones Shopify returned.
  endcomment
  assign has_filters = false
  if section.settings.show_filters
    for f in collection.filters
      if f.type == 'price_range'
        assign has_filters = true
      elsif f.values.size > 1
        assign has_filters = true
      endif
    endfor
  endif

  assign active_filter_count = 0
  for f in collection.filters
    assign active_filter_count = active_filter_count | plus: f.active_values.size
    if f.type == 'price_range'
      if f.min_value.value != blank or f.max_value.value != blank
        assign active_filter_count = active_filter_count | plus: 1
      endif
    endif
  endfor

  assign sort_form_id = 'CollectionSort-' | append: section.id""",
      'the filter state is derived once, and counts only renderable groups')

# ------------------------------------- 2. the form exists for EITHER control
patch("""            {%- if show_sorting -%}
              <form
                method="get"
                action="{{ sort_action }}"
                id="{{ sort_form_id }}"
                class="main-collection__sort"
                data-collection-sort
              >
                <label class="main-collection__sort-label" for="{{ sort_id }}">
                  {{ 'collection.sort_label' | t }}
                </label>""",
      """            {%- comment -%}
              ONE form for the whole surface. It is rendered whenever there is a
              sort control OR a filter control, because every facet checkbox
              binds to it by the HTML form attribute rather than by sitting
              inside it — so submitting from the toolbar or from the drawer's
              Apply carries the sort and every checked filter together.

              Before Phase 13 this form existed only for sorting, and its own
              comment above recorded that it "sends sort_by and nothing else".
              That was correct while nothing else was in the URL. The moment
              filters arrived it would have discarded every one of them.

              No page parameter is rendered, so any submission returns to page 1
              — which is also what Shopify's own url_to_add does.
            {%- endcomment -%}
            {%- if show_sorting or has_filters -%}
              <form
                method="get"
                action="{{ sort_action }}"
                id="{{ sort_form_id }}"
                class="main-collection__sort"
                data-collection-sort
              >
                {%- if show_sorting -%}
                <label class="main-collection__sort-label" for="{{ sort_id }}">
                  {{ 'collection.sort_label' | t }}
                </label>""",
      'the form is rendered for sorting OR filtering')

# Close the sorting-only branch after the select, before the submit button.
patch("""                {%- comment -%}
                  The control that makes the form work with no script at all.""",
      """                {%- endif -%}

                {%- comment -%}
                  The control that makes the form work with no script at all.""",
      'the sort label and select stay behind their own condition')

open(P, 'w', encoding='utf-8', newline='').write(s)

# ------------------------------------------------------------ 3. the setting
s = open(P, encoding='utf-8').read()
m = re.search(r'\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}', s, re.S)
doc = json.loads(m.group(1), object_pairs_hook=collections.OrderedDict)
assert not any(x.get('id') == 'show_filters' for x in doc['settings'])
idx = next(i for i, x in enumerate(doc['settings']) if x.get('id') == 'show_sorting')
doc['settings'].insert(idx, collections.OrderedDict([
    ('type', 'checkbox'),
    ('id', 'show_filters'),
    ('label', 'Show filters'),
    ('default', True),
    ('info',
     'Filters are created in Shopify admin under Apps \u203a Search & Discovery \u203a '
     'Filters. Until at least one exists, nothing is shown here whatever this is '
     'set to.'),
]))
s = s[:m.start(1)] + '\n' + json.dumps(doc, indent=2, ensure_ascii=False) + '\n' + s[m.end(1):]
open(P, 'w', encoding='utf-8', newline='').write(s)
done.append('a Show filters setting, with the admin dependency in its own info string')

for i, label in enumerate(done, 1):
    print('%d. %s' % (i, label))
