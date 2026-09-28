# -*- coding: utf-8 -*-
"""Phase 17 PART 1 + PART 29 — the tracking inventory, measured.

Runs the brief's own search terms across every file in the theme, and separates
two things a plain grep conflates:

  CODE      an actual tracking API surface — gtag(, fbq(, dataLayer.push, a
            <script src> to a tracking host, a measurement ID literal
  PROSE     the same word inside a comment, a locale string or a class name.
            "checkout", "conversion" and "analytics" all appear in this theme in
            ordinary English and none of them is tracking.

Reporting a comment as an installed pixel would be the fourth time this project
asserted on prose, so the split is the point of the file.
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
THEME = os.environ.get('GS_THEME') or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')

FAILURES = []
CHECKS = [0]


def check(label, ok, detail=''):
    CHECKS[0] += 1
    print('  %-60s %s %s' % (label, 'OK  ' if ok else '*** FOUND ***',
                             '' if ok else str(detail)[:130]))
    if not ok:
        FAILURES.append(label)


def strip_comments(t):
    t = re.sub(r'\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}', '', t, flags=re.S)
    # Inside a {% liquid %} block `comment` is a bare STATEMENT with no {% %}
    # around it, and every long explanation in this theme's sections is written
    # that way. Missing this form reported prose in featured-collection.liquid
    # as executable code. Phase 13 recorded the same hazard from the other side.
    t = re.sub(r'(?m)^\s*comment\b.*?^\s*endcomment\b', '', t, flags=re.S)
    t = re.sub(r'/\*.*?\*/', '', t, flags=re.S)
    t = re.sub(r'(?m)^\s*//.*$', '', t)
    return t


def files():
    for root, _d, fs in os.walk(THEME):
        for f in sorted(fs):
            p = os.path.join(root, f)
            rel = os.path.relpath(p, THEME).replace(os.sep, '/')
            try:
                yield rel, io.open(p, encoding='utf-8').read()
            except Exception:
                continue


# The brief's PART 1 list. Each is (regex on CODE, human name). These match API
# SURFACES, not the English word — `fbq(` not "facebook".
CODE_PATTERNS = [
    (r'\bgtag\s*\(', 'gtag()'),
    (r'googletagmanager\.com|\bGTM-[A-Z0-9]{4,}', 'Google Tag Manager'),
    (r'google-analytics\.com|\bga\s*\(\s*[\'"]|analytics\.js', 'Google Analytics (legacy)'),
    (r'\bG-[A-Z0-9]{8,}\b', 'GA4 measurement ID'),
    (r'\bAW-\d{6,}\b', 'Google Ads conversion ID'),
    (r'\bGT-[A-Z0-9]{6,}\b', 'Google Tag ID'),
    (r'\bfbq\s*\(|connect\.facebook\.net', 'Meta Pixel'),
    (r'\bttq\s*\.|analytics\.tiktok\.com', 'TikTok Pixel'),
    (r'\bpintrk\s*\(|s\.pinimg\.com', 'Pinterest Tag'),
    (r'clarity\.ms|\bclarity\s*\(', 'Microsoft Clarity'),
    (r'static\.hotjar\.com|\bhj\s*\(|_hjSettings', 'Hotjar'),
    (r'\bdataLayer\b', 'dataLayer'),
    (r'\bsnaptr\s*\(|sc-static\.net', 'Snapchat Pixel'),
    (r'\bsegment\b.*analytics|cdn\.segment\.com', 'Segment'),
    (r'plausible\.io|umami|matomo|posthog', 'other analytics'),
    # Word-bounded. Unanchored, `rollbar` matches inside `scrollbar` and this
    # reported Phase 8's scrollbar-gutter rule as an installed error monitor.
    (r'\b(?:sentry|bugsnag|rollbar|datadog|newrelic)\b', 'error monitoring'),
]

# PART 29: literals that would be a real account identifier.
ID_PATTERNS = [
    (r'\bG-[A-Z0-9]{10}\b', 'GA4 measurement ID'),
    (r'\bAW-\d{9,11}\b', 'Google Ads ID'),
    (r'\bGTM-[A-Z0-9]{6,7}\b', 'GTM container ID'),
    (r'\bUA-\d{4,9}-\d{1,4}\b', 'Universal Analytics ID'),
    (r'(?<!\d)\d{15,16}(?!\d)', 'Meta Pixel ID shape'),
    (r'\bC[A-Z0-9]{19,21}\b', 'TikTok Pixel ID shape'),
]

# ANY absolute URL in executable code, not just one in a src/href attribute.
# The first version matched attributes only, and missed a seeded Meta Pixel
# entirely — because every real pixel injects its own <script> and therefore
# carries its host as a STRING LITERAL inside JavaScript, which is exactly the
# case the check exists for.
EXTERNAL_HOST = re.compile(r'https?://([\w.-]+)', re.I)

# Hosts that are Shopify's own, or a documentation link in merchant help text.
ALLOWED_HOSTS = re.compile(
    r'(?:^|\.)(?:shopify\.com|shopifycdn\.com|myshopify\.com|shopify\.dev|'
    r'w3\.org|schema\.org)$', re.I)


if __name__ == '__main__':
    corpus = list(files())
    code = {rel: strip_comments(s) for rel, s in corpus}
    all_code = '\n'.join(code.values())
    all_raw = '\n'.join(s for _r, s in corpus)

    print('=== PART 1 — TRACKING PLATFORM INVENTORY ===')
    print('scanned %d files' % len(corpus))
    print()
    print('  %-28s %-10s %s' % ('PLATFORM', 'IN CODE', 'WHERE'))
    found_any = False
    for pat, name in CODE_PATTERNS:
        hits = []
        for rel, src in code.items():
            for m in re.finditer(pat, src, re.I):
                line = src[:m.start()].count('\n') + 1
                hits.append('%s:%d' % (rel, line))
        if hits:
            found_any = True
        print('  %-28s %-10s %s' % (name, 'YES' if hits else 'none',
                                    ', '.join(hits[:3]) if hits else '-'))

    print()
    check('no tracking platform is implemented in the theme', not found_any)

    print()
    print('=== PART 29 — HARDCODED ACCOUNT IDENTIFIERS ===')
    for pat, name in ID_PATTERNS:
        hits = []
        for rel, src in code.items():
            for m in re.finditer(pat, src):
                line = src[:m.start()].count('\n') + 1
                hits.append('%s:%d %s' % (rel, line, m.group(0)))
        check('no %s literal' % name, not hits, hits[:3])

    print()
    print('=== EXTERNAL SCRIPT AND STYLE HOSTS ===')
    hosts = set()
    for rel, src in code.items():
        for m in EXTERNAL_HOST.finditer(src):
            host = m.group(1)
            if ALLOWED_HOSTS.search(host):
                continue
            hosts.add('%s (%s)' % (host, rel))
    check('the theme reaches no third-party host', not hosts, sorted(hosts)[:5])

    print()
    print('=== THE WORDS, WHERE THEY DO APPEAR (prose, not tracking) ===')
    # Reported so nothing is hidden: these are the brief's search terms matching
    # ordinary English. Each is shown with its file so a reader can check.
    for word in ('analytics', 'tracking', 'conversion', 'pixel', 'purchase'):
        prose, in_code = [], []
        for rel, src in corpus:
            n_raw = len(re.findall(r'\b%s' % word, src, re.I))
            n_code = len(re.findall(r'\b%s' % word, code[rel], re.I))
            if n_raw:
                prose.append((rel, n_raw))
            if n_code:
                in_code.append((rel, n_code))
        # The total is summed from the COUNTS, not re-parsed out of the display
        # string. It used to be `int(p.split('x')[1])` over 'name xN' entries,
        # which reads the text after the first letter x anywhere in the line —
        # so the first theme file with an x in its name (section-verse-index.css)
        # made this raise ValueError: invalid literal for int(): '.css '. The
        # crash killed the whole scanner, and because phase17/negctl.py grades
        # its seeds on what the scanner PRINTS, six seeded violations came back
        # as 'a seeded theme passed clean' — a negative control reporting that
        # the theme is safe because the tool checking it had died.
        print('  %-12s total %-3d  in comments/strings only: %s'
              % (word, sum(n for _rel, n in prose),
                 'yes' if not in_code
                 else 'NO — also in code: ' + ', '.join(
                     '%s x%d' % (rel, n) for rel, n in in_code[:3])))

    print()
    print('=== CONSENT AND PII HYGIENE ===')
    js = '\n'.join(code[rel] for rel in code if rel.endswith('.js'))
    for api, why in (('localStorage', 'survives logout on a shared device'),
                     ('sessionStorage', 'same class of leak'),
                     ('indexedDB', 'same class of leak'),
                     ('document.cookie', 'a theme-set cookie bypasses consent tooling'),
                     ('navigator.sendBeacon', 'an unsanctioned exfiltration path'),
                     ('new Image(', 'the classic tracking-pixel construction'),
                     ('fetch("https://', 'an off-origin request from the theme')):
        check('no %s in theme JavaScript' % api, api not in js, why)

    check('no customer field is read anywhere in the theme',
          not re.search(r'customer\.(?!accounts)[\w.]+', all_code))
    check('nothing is written into a cart attribute',
          not re.search(r'attributes\[|cart\.attributes\s*=|properties\[', all_code))
    check('no console logging that could carry a payload',
          not re.search(r'console\.(log|info|debug|table|dir)\s*\(', js))

    print()
    print('=== SHOPIFY-NATIVE SURFACES THE THEME MUST NOT BREAK ===')
    cart_js = code.get('assets/cart.js', '')
    check('the cart adds through Shopify\'s own /cart/add.js',
          "post('cart/add.js'" in cart_js)
    check('quantity changes go through /cart/change.js',
          "post('cart/change.js'" in cart_js)
    check('the note goes through /cart/update.js',
          "post('cart/update.js'" in cart_js)
    check('URLs are built from window.Shopify.routes, never hardcoded',
          'Shopify.routes.root' in cart_js)
    check('checkout is Shopify\'s own submit, not a constructed URL',
          'name="checkout"' in all_code and '/checkouts/' not in all_code)
    layout = code.get('layout/theme.liquid', '')
    check('content_for_header is present and unmodified',
          '{{ content_for_header }}' in layout)

    print()
    print('=== SHOPIFY-RESERVED QUERY PARAMETERS ===')
    # Shopify special-cases ref, source and r storefront-wide as the marketing
    # referral code, and the value lands in every order's conversion detail. A
    # theme form field with one of those names would silently overwrite a real
    # campaign attribution.
    form_names = set(re.findall(r'name="([\w.\[\]]+)"', all_code))
    reserved = {'ref', 'source', 'r'} & form_names
    check('no form field is named ref, source or r', not reserved, sorted(reserved))
    print('   form fields the theme submits: %s'
          % ', '.join(sorted(n for n in form_names if not n.startswith('updates'))))

    print()
    print('=== RETIRED SHOPIFY COOKIES ARE NOT READ ===')
    # _landing_page, _orig_referrer and _tracking_consent were removed 2025-09-15;
    # _shopify_s and _shopify_y on 2026-01-01. Any code reading them describes a
    # storefront that no longer exists.
    for ck in ('_landing_page', '_orig_referrer', '_tracking_consent',
               '_shopify_s', '_shopify_y', '_shopify_sa_'):
        check('nothing reads the retired %s cookie' % ck, ck not in all_code)

    print()
    print('%d checks, %d clean, %d findings'
          % (CHECKS[0], CHECKS[0] - len(FAILURES), len(FAILURES)))
    print('OVERALL: %s' % ('NO TRACKING PRESENT' if not FAILURES else '*** SEE FINDINGS ***'))
