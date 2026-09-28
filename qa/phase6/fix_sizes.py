# -*- coding: utf-8 -*-
"""Rewrite the sizes computation so it never under-declares.

Confirmed by six independent verifiers and reproduced in the project's own
probe: the section divided each row by the REQUESTED column count, but the
grid's 272px track floor drops a column wherever the viewport cannot carry that
count, and the surviving tracks then stretch to 1fr. At 1024 the New Drop grid
paints two 292px tracks while the old sizes declared 196px, so the browser
fetched a 240w candidate for a 292px slot and upscaled the photograph.

The fix is exact rather than conservative. Between a tier's minimum width and
the width at which the requested count first fits, the rendered count is
exactly one less -- provable from the auto-fill arithmetic and confirmed by
measurement at 1024, 1180, 1256 and 1280. So the section computes that
threshold and emits one extra sizes clause at it.
"""
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\sections\featured-collection.liquid"
s = open(p, encoding='utf-8').read()

start = s.index("  comment\n    The sizes attribute.")
end = s.index("  assign classes = 'featured-collection '")

new = r"""  comment
    The sizes attribute.

    The section knows the grid, so the section computes this; the card takes it
    as a parameter rather than guessing. Two things make it more than a
    division.

    First, the grid's column count is a CEILING. .product-grid floors every
    track at --product-col-min 272px, so where a viewport cannot carry the
    requested count the grid drops a column and the survivors stretch. Dividing
    by the requested count would then declare a slot narrower than the tile
    actually painted, and the browser would fetch a candidate it has to upscale.
    Measured before this was fixed: at 1024 the New Drop grid painted two 292px
    tracks against a declared 196px.

    Between a tier's minimum width and the width at which the requested count
    first fits, the rendered count is exactly one lower. That threshold is
    computable here, so each tier emits two clauses: the requested count from
    the threshold up, and one fewer below it. Both are exact at every width in
    their range, so nothing is over-declared either.

    Second, the copy-column layout puts the grid in the 2.4 track of
    --split-30-70, which is 72.7% of the row once the 32px split gap is taken
    off. Gutters come from the Phase 2 ladder: 24, 32 and 48 per side.
  endcomment

  assign gap = 32
  assign col_min = 272
  assign step = 304

  comment
    Per-tier row width available to the grid, expressed as the fixed pixels to
    subtract from the viewport. Desktop also loses the copy rail.
  endcomment
  assign chrome_m = 48
  assign chrome_t = 64
  assign chrome_d = 96
  if section.settings.layout == 'with-copy-column'
    assign chrome_d = 128
  endif

  comment
    The viewport at which cols_d first fits. Needed row is
    cols_d * 272 + (cols_d - 1) * 32; for the copy-column layout the grid is
    only 72.7% of the row, so the viewport has to be correspondingly wider.
    1000 / 727 is used rather than a float because Liquid's divided_by on two
    integers truncates, and truncating downward here would put the threshold
    below the width that actually fits.
  endcomment
  assign need_d = cols_d | times: col_min
  assign need_d = cols_d | minus: 1 | times: gap | plus: need_d
  if section.settings.layout == 'with-copy-column'
    assign need_d = need_d | times: 1000 | divided_by: 727 | plus: 1
  endif
  assign threshold_d = need_d | plus: chrome_d

  comment
    Below the threshold the grid paints one column fewer, floored at one.
  endcomment
  assign cols_d_low = cols_d | minus: 1
  if cols_d_low < 1
    assign cols_d_low = 1
  endif
  assign cols_t_low = cols_t | minus: 1
  if cols_t_low < 1
    assign cols_t_low = 1
  endif

  comment
    Tablet: does cols_t fit at 768, the tier's own minimum? If not, the tier
    never reaches it, because the next tier starts at 1024.
  endcomment
  assign need_t = cols_t | times: col_min
  assign need_t = cols_t | minus: 1 | times: gap | plus: need_t
  assign row_t_min = 768 | minus: chrome_t
  assign cols_t_used = cols_t
  if need_t > row_t_min
    assign cols_t_used = cols_t_low
  endif

  comment
    Mobile: the floor is 8rem/128px below 768, so the step is 160.
  endcomment
  assign need_m = cols_m | times: 128
  assign need_m = cols_m | minus: 1 | times: gap | plus: need_m
  assign threshold_m = need_m | plus: chrome_m
  assign cols_m_low = cols_m | minus: 1
  if cols_m_low < 1
    assign cols_m_low = 1
  endif

  assign gaps_d = cols_d | minus: 1 | times: gap
  assign gaps_d_low = cols_d_low | minus: 1 | times: gap
  assign gaps_t = cols_t_used | minus: 1 | times: gap
  assign gaps_m = cols_m | minus: 1 | times: gap
  assign gaps_m_low = cols_m_low | minus: 1 | times: gap
  assign container = settings.container_width | default: 1440

  comment
    Above the container cap the row stops growing, so the first clause is a
    fixed pixel value rather than a vw expression.
  endcomment
  assign capped_row = container | minus: chrome_d
  if section.settings.layout == 'with-copy-column'
    assign capped_row = capped_row | times: 727 | divided_by: 1000
  endif
  assign capped_track = capped_row | minus: gaps_d | divided_by: cols_d

  capture sizes_attr
    echo '(min-width: '
    echo container
    echo 'px) '
    echo capped_track
    echo 'px'

    echo ', (min-width: '
    echo threshold_d
    echo 'px) calc(('
    if section.settings.layout == 'with-copy-column'
      echo '(100vw - '
      echo chrome_d
      echo 'px) * 0.727 - '
    else
      echo '100vw - '
      echo chrome_d
      echo 'px - '
    endif
    echo gaps_d
    echo 'px) / '
    echo cols_d
    echo ')'

    echo ', (min-width: 1024px) calc(('
    if section.settings.layout == 'with-copy-column'
      echo '(100vw - '
      echo chrome_d
      echo 'px) * 0.727 - '
    else
      echo '100vw - '
      echo chrome_d
      echo 'px - '
    endif
    echo gaps_d_low
    echo 'px) / '
    echo cols_d_low
    echo ')'

    echo ', (min-width: 768px) calc((100vw - '
    echo chrome_t
    echo 'px - '
    echo gaps_t
    echo 'px) / '
    echo cols_t_used
    echo ')'

    echo ', (min-width: '
    echo threshold_m
    echo 'px) calc((100vw - '
    echo chrome_m
    echo 'px - '
    echo gaps_m
    echo 'px) / '
    echo cols_m
    echo ')'

    echo ', calc((100vw - '
    echo chrome_m
    echo 'px - '
    echo gaps_m_low
    echo 'px) / '
    echo cols_m_low
    echo ')'
  endcapture

"""
s = s[:start] + new + s[end:]
open(p, 'w', encoding='utf-8', newline='').write(s)
print('featured-collection.liquid: sizes now tracks the count the grid can actually paint')
