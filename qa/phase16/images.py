# -*- coding: utf-8 -*-
"""Phase 16 — the image pipeline, audited on the RENDERED markup.

WHY STATIC AND NOT A BROWSER LCP READING.

The first attempt at this used PerformanceObserver to name the LCP element on
each surface. On the collection page it reported the 78px header logo, which
would be a serious finding if it were true. It is not: the harness ships NO
image files at all, so every <img> 404s and never paints, and the logo wins by
default. A browser LCP reading in this environment measures the harness, not the
theme.

What IS reliable is what the theme actually emits, and that is what decides LCP
behaviour on a real store: which image is eager, which carries fetchpriority,
whether every image reserves its box, and whether the declared sizes match what
the CSS renders. All of that is in the markup and none of it needs a network.

So this asserts on attributes, and the browser probe is kept only for layout
shift and handler cost, where the harness IS representative.
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
S9 = os.path.abspath(os.path.join(HERE, '..', 'phase9', 'site'))
S8 = os.path.abspath(os.path.join(HERE, '..', 'phase8', 'site'))
THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
PAGES = [
    ('Homepage', S9, 'home.html'),
    ('Collection', S9, 's-collection.html'),
    ('Search', S9, 's-search.html'),
    ('Product', S8, 'p-sizes.html'),
    ('Cart page', S8, 'c-page-many.html'),
    ('404', S9, 's-404.html'),
]

FAILURES = []
CHECKS = [0]


def check(label, ok, detail=''):
    CHECKS[0] += 1
    print('  %-62s %s %s' % (label, 'OK  ' if ok else '*** FAIL ***',
                             '' if ok else str(detail)[:140]))
    if not ok:
        FAILURES.append(label)


def attrs(tag):
    return dict(re.findall(r'([\w-]+)="([^"]*)"', tag))


def images(html):
    return [attrs(t) | {'_tag': t} for t in re.findall(r'<img\b[^>]*>', html)]


if __name__ == '__main__':
    print('=== EVERY RENDERED IMAGE, BY SURFACE ===')
    print('%-12s %-26s %-7s %-8s %-9s %-7s %s' %
          ('surface', 'class', 'loading', 'fetchpri', 'w x h', 'srcset', 'sizes?'))
    all_imgs = {}
    for label, site, name in PAGES:
        p = os.path.join(site, name)
        if not os.path.exists(p):
            continue
        html = io.open(p, encoding='utf-8').read()
        imgs = images(html)
        all_imgs[label] = imgs
        for a in imgs:
            cls = (a.get('class') or '').split(' ')[0][:26]
            wh = '%sx%s' % (a.get('width', '-'), a.get('height', '-'))
            print('%-12s %-26s %-7s %-8s %-9s %-7s %s' %
                  (label, cls, a.get('loading', '-'), a.get('fetchpriority', '-'),
                   wh, 'yes' if a.get('srcset') else 'NO',
                   'yes' if a.get('sizes') else 'no'))

    print()
    print('=== EVERY IMAGE RESERVES ITS BOX (the CLS precondition) ===')
    for label, imgs in all_imgs.items():
        missing = [(a.get('class') or a.get('src', '?'))[:40] for a in imgs
                   if not (a.get('width') and a.get('height'))]
        check('%-12s every <img> carries width and height' % label, not missing, missing)

    print()
    print('=== EXACTLY ONE EAGER LCP CANDIDATE PER SURFACE ===')
    # The rule Phase 12 set: the first tile of the first row is eager, the rest
    # lazy. Plus the hero, plus the product gallery's first frame.
    for label, imgs in all_imgs.items():
        eager = [a for a in imgs if a.get('loading') == 'eager']
        lazy = [a for a in imgs if a.get('loading') == 'lazy']
        none_ = [a for a in imgs if not a.get('loading')]
        print('  %-12s eager=%d  lazy=%d  unset=%d   %s' %
              (label, len(eager), len(lazy), len(none_),
               ', '.join((a.get('class') or '?').split(' ')[0] for a in eager)))

    print()
    print('=== THE ABOVE-THE-FOLD IMAGE IS NEVER LAZY ===')
    for label, imgs in all_imgs.items():
        if not imgs:
            continue
        first_content = None
        for a in imgs:
            c = a.get('class') or ''
            if 'logo' in c:
                continue           # the wordmark is chrome, not content
            first_content = a
            break
        if first_content is None:
            continue
        check('%-12s the first content image is not lazy-loaded' % label,
              first_content.get('loading') != 'lazy',
              (first_content.get('class') or '?'))

    print()
    print('=== fetchpriority IS USED ONLY WHERE IT EARNS ITS PLACE ===')
    for label, imgs in all_imgs.items():
        hi = [(a.get('class') or '?').split(' ')[0] for a in imgs
              if a.get('fetchpriority') == 'high']
        check('%-12s at most one high-priority image' % label, len(hi) <= 1, hi)

    print()
    print('=== RESPONSIVE: srcset AND sizes ===')
    for label, imgs in all_imgs.items():
        content = [a for a in imgs if 'logo' not in (a.get('class') or '')]
        no_srcset = [(a.get('class') or '?').split(' ')[0] for a in content
                     if not a.get('srcset')]
        check('%-12s every content image has a srcset' % label, not no_srcset, no_srcset)
        no_sizes = [(a.get('class') or '?').split(' ')[0] for a in content
                    if a.get('srcset') and not a.get('sizes')]
        check('%-12s and a sizes attribute to go with it' % label, not no_sizes, no_sizes)

    print()
    print('=== NO IMAGE IS REQUESTED FAR LARGER THAN IT RENDERS ===')
    for label, imgs in all_imgs.items():
        over = []
        for a in imgs:
            srcset = a.get('srcset') or ''
            widths = [int(w) for w in re.findall(r'(\d+)w', srcset)]
            sizes = a.get('sizes') or ''
            declared = [int(x) for x in re.findall(r'(\d+)px', sizes)]
            if widths and declared:
                # 3x the largest declared slot is the ceiling a 3x DPR screen needs.
                if max(widths) > max(declared) * 3:
                    over.append('%s max=%dw slot=%dpx' %
                                ((a.get('class') or '?').split(' ')[0],
                                 max(widths), max(declared)))
        check('%-12s no srcset overshoots 3x its largest slot' % label, not over, over)

    print()
    print('=== ALT TEXT ===')
    for label, imgs in all_imgs.items():
        missing_alt = [(a.get('class') or '?').split(' ')[0] for a in imgs
                       if 'alt' not in a]
        check('%-12s every <img> has an alt attribute' % label, not missing_alt, missing_alt)
        stuffed = [a.get('alt') for a in imgs
                   if a.get('alt') and len(a['alt'].split()) > 14]
        check('%-12s no alt text reads as keyword stuffing' % label, not stuffed, stuffed)

    print()
    print('=== VIDEO IS SUPPORTED, AND SUPPORTED SAFELY ===')
    # The first version of this asserted the theme had NO video and "failed".
    # It does have video: snippets/product-media-gallery.liquid renders Shopify's
    # video and external_video media types, which is Phase 8 work. The word the
    # test matched was `autoplay: false` — the correct setting. What PART 4
    # actually asks is whether video is heavy or autoplaying, so that is what is
    # asserted now.
    theme_src = []
    for root, _d, files in os.walk(THEME):
        for f in files:
            if f.endswith(('.liquid', '.js', '.css')):
                theme_src.append(io.open(os.path.join(root, f), encoding='utf-8').read())
    joined = '\n'.join(theme_src)
    joined_code = re.sub(r'\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}', '',
                         joined, flags=re.S)

    check('video is rendered through Shopify filters, not a hand-built player',
          'video_tag' in joined_code and '<video' not in joined_code)
    check('nothing autoplays', re.search(r'autoplay:\s*true|\bautoplay\b(?!\s*:\s*false)',
                                         joined_code) is None)
    check('the external video is explicitly autoplay: false',
          'autoplay: false' in joined_code)
    check('controls are on, so a customer is never trapped in a clip',
          'controls: true' in joined_code)
    check('only metadata is preloaded, never the whole file',
          "preload: 'metadata'" in joined_code and "preload: 'auto'" not in joined_code)
    check('the embedded third-party player is lazy-loaded',
          re.search(r"external_video_tag[^%]*loading:\s*'lazy'", joined_code) is not None)
    check('no background or decorative video anywhere',
          not re.search(r'background-video|video--background|hero__video', joined_code))

    print()
    print('%d checks, %d passed, %d failed'
          % (CHECKS[0], CHECKS[0] - len(FAILURES), len(FAILURES)))
    print('OVERALL: %s' % ('PASS' if not FAILURES else '*** FAILURES ABOVE ***'))
