# -*- coding: utf-8 -*-
"""
A deliberately small Liquid interpreter, written to render the God Squad theme's
own .liquid files for visual and structural QA.

It is STRICT on purpose: an unknown tag, filter or syntax raises instead of
rendering empty. The point of the harness is to catch Liquid mistakes, so
silently swallowing one would defeat it.

It implements only the subset the theme uses. It is NOT a Shopify emulator and
its output is evidence about layout and markup, not proof that Shopify will
behave identically.
"""
import datetime
import re, json, html, math
from urllib.parse import quote, quote_plus


class LiquidError(Exception):
    pass


# --------------------------------------------------------------------------- drops
class Drop(dict):
    """Attribute access over a dict, with blank-safe misses."""

    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            return None


def wrap(v):
    if isinstance(v, Drop):
        return v
    if isinstance(v, dict):
        return Drop({k: wrap(x) for k, x in v.items()})
    if isinstance(v, list):
        return [wrap(x) for x in v]
    return v


# --------------------------------------------------------------------------- lexing
TAG = re.compile(r'\{%-?\s*(.*?)\s*-?%\}|\{\{-?\s*(.*?)\s*-?\}\}', re.S)


def _tokenize(src):
    """Yield ('text', s) | ('tag', s, lstrip, rstrip) | ('out', s, lstrip, rstrip)."""
    out, pos = [], 0
    for m in TAG.finditer(src):
        if m.start() > pos:
            out.append(('text', src[pos:m.start()]))
        raw = m.group(0)
        lstrip = raw[:3] in ('{%-', '{{-')
        rstrip = raw[-3:] in ('-%}', '-}}')
        if m.group(1) is not None:
            out.append(('tag', m.group(1), lstrip, rstrip))
        else:
            out.append(('out', m.group(2), lstrip, rstrip))
        pos = m.end()
    if pos < len(src):
        out.append(('text', src[pos:]))
    return out


def _apply_whitespace_control(tokens):
    """Liquid's -%} / {%- trim adjacent text nodes."""
    for i, t in enumerate(tokens):
        if t[0] == 'text':
            continue
        if t[2] and i > 0 and tokens[i - 1][0] == 'text':
            tokens[i - 1] = ('text', tokens[i - 1][1].rstrip())
        if t[3] and i + 1 < len(tokens) and tokens[i + 1][0] == 'text':
            tokens[i + 1] = ('text', tokens[i + 1][1].lstrip())
    return tokens


# --------------------------------------------------------------------------- values
NUM = re.compile(r'^-?\d+(\.\d+)?$')


def _split_filters(expr):
    """Split 'a | b: x, y | c' on top-level pipes."""
    parts, depth, cur, q = [], 0, '', None
    for ch in expr:
        if q:
            cur += ch
            if ch == q:
                q = None
            continue
        if ch in '"\'':
            q = ch
            cur += ch
            continue
        if ch in '([':
            depth += 1
        elif ch in ')]':
            depth -= 1
        if ch == '|' and depth == 0:
            parts.append(cur)
            cur = ''
        else:
            cur += ch
    parts.append(cur)
    return [p.strip() for p in parts]


def _split_commas(s):
    parts, depth, cur, q = [], 0, '', None
    for ch in s:
        if q:
            cur += ch
            if ch == q:
                q = None
            continue
        if ch in '"\'':
            q = ch
            cur += ch
            continue
        if ch in '([':
            depth += 1
        elif ch in ')]':
            depth -= 1
        if ch == ',' and depth == 0:
            parts.append(cur)
            cur = ''
        else:
            cur += ch
    if cur.strip():
        parts.append(cur)
    return [p.strip() for p in parts]


class Env:
    def __init__(self, scopes, engine):
        self.scopes = scopes
        self.engine = engine

    def get(self, name):
        for s in reversed(self.scopes):
            if name in s:
                return s[name]
        return None

    def set(self, name, value):
        self.scopes[-1][name] = value

    def set_global(self, name, value):
        self.scopes[0][name] = value


def lookup(env, path):
    parts = re.findall(r'[^.\[\]]+|\[[^\]]+\]', path)
    cur = None
    for i, p in enumerate(parts):
        if p.startswith('['):
            key = evaluate(env, p[1:-1])
            cur = _index(cur, key)
            continue
        if i == 0:
            cur = env.get(p)
        else:
            cur = _index(cur, p)
        if cur is None:
            return None
    return cur


def _index(obj, key):
    if obj is None:
        return None
    if isinstance(key, str) and key == 'size':
        try:
            return len(obj)
        except TypeError:
            return None
    if isinstance(obj, (dict, Drop)):
        return obj.get(key)
    if isinstance(obj, (list, tuple)):
        if key == 'first':
            return obj[0] if obj else None
        if key == 'last':
            return obj[-1] if obj else None
        try:
            return obj[int(key)]
        except (ValueError, IndexError, TypeError):
            return None
    if isinstance(obj, str):
        if key == 'size':
            return len(obj)
        return None
    return getattr(obj, str(key), None)


def evaluate(env, expr):
    expr = expr.strip()
    if not expr:
        return None
    parts = _split_filters(expr)
    val = _atom(env, parts[0])
    for f in parts[1:]:
        val = _filter(env, val, f)
    return val


def _atom(env, tok):
    tok = tok.strip()
    if tok.startswith('"') and tok.endswith('"'):
        # CORRECTED IN PHASE 10. This used to interpolate #{...} inside a
        # double-quoted string, on the assumption that Shopify's Liquid does.
        # It does not: Liquid string literals do not interpolate, and the
        # documented way to build a string is the append filter.
        #
        # That assumption was made in Phase 8 to explain away a 133px logo and
        # a horizontal overflow at 320 in sections/header.liquid. Both were
        # REAL. Teaching the harness to interpolate did not fix a harness bug;
        # it hid a theme bug, and hid it for two phases. A harness must model
        # the platform, never the behaviour we expect from it.
        return tok[1:-1]
    if tok.startswith("'") and tok.endswith("'"):
        return tok[1:-1]
    if NUM.match(tok):
        return float(tok) if '.' in tok else int(tok)
    if tok == 'true':
        return True
    if tok == 'false':
        return False
    if tok in ('nil', 'null', 'blank', 'empty'):
        return BLANK if tok in ('blank', 'empty') else None
    return lookup(env, tok)


class _Blank:
    def __repr__(self):
        return 'blank'


BLANK = _Blank()


def is_blank(v):
    # BLANK belongs in this list. Shopify's `blank` compares equal to nil, to
    # an empty string, to an empty array and to false, so a variable that has
    # been explicitly assigned blank must test as blank too. Leaving it out
    # made `assign x = blank` followed by `if x != blank` take the TRUE branch,
    # which is the opposite of what Shopify does — found in Phase 8, where a
    # quantity ceiling that had not been set rendered as max="".
    return v is None or v is False or v is BLANK or v == '' or v == [] or v == {}


def _money(v, fmt='&#8369;{{amount}}'):
    cents = int(v or 0)
    whole, frac = divmod(cents, 100)
    return '&#8369;{:,}.{:02d}'.format(whole, frac)


def _filter(env, val, spec):
    m = re.match(r'^([\w_]+)\s*(?::\s*(.*))?$', spec, re.S)
    if not m:
        raise LiquidError('bad filter: %r' % spec)
    name, argstr = m.group(1), m.group(2)
    named, pos = {}, []
    if argstr:
        for a in _split_commas(argstr):
            km = re.match(r'^([\w_]+)\s*:\s*(.*)$', a, re.S)
            if km:
                named[km.group(1)] = evaluate(env, km.group(2))
            else:
                pos.append(evaluate(env, a))

    if name == 'default':
        return pos[0] if is_blank(val) else val
    if name == 'strip':
        return (val or '').strip() if isinstance(val, str) else val
    if name == 'append':
        return '%s%s' % (_s(val), _s(pos[0]))
    if name == 'prepend':
        return '%s%s' % (_s(pos[0]), _s(val))
    if name == 'plus':
        return _n(val) + _n(pos[0])
    if name == 'minus':
        return _n(val) - _n(pos[0])
    if name == 'times':
        return _n(val) * _n(pos[0])
    if name == 'divided_by':
        d = _n(pos[0])
        r = _n(val) / d
        return int(r) if isinstance(_n(val), int) and isinstance(d, int) else r
    if name == 'round':
        return round(_n(val), int(pos[0]) if pos else 0)
    if name == 'escape':
        return html.escape(_s(val), quote=True)
    if name == 'handle' or name == 'handleize':
        return re.sub(r'[^a-z0-9]+', '-', _s(val).lower()).strip('-')
    if name == 'join':
        return _s(pos[0]).join(_s(x) for x in (val or []))
    if name == 'size':
        return len(val or [])
    if name == 'money':
        return _money(val)
    if name == 'downcase':
        return _s(val).lower()
    if name == 'upcase':
        return _s(val).upper()
    if name == 'asset_url':
        return env.engine.asset_url(_s(val))
    if name == 'stylesheet_tag':
        return '<link rel="stylesheet" href="%s">' % _s(val)
    if name == 'image_url':
        return env.engine.image_url(val, named)
    if name == 'image_tag':
        return env.engine.image_tag(val, named)
    if name == 't':
        return env.engine.translate(_s(val), named)
    if name == 'font_modify':
        # Shopify's font_modify: returns a new font object with one property
        # changed, or NIL when the family has no such variant. The nil case is
        # the whole reason callers must guard it, so the stub models it: the
        # fixture declares which weights exist via a 'variants' list, and
        # anything outside that list comes back as nil exactly as it would on a
        # real store.
        if val is None or val is BLANK or val == '' or not hasattr(val, 'get'):
            return None
        prop = _s(pos[0]) if pos else ''
        want = _s(pos[1]) if len(pos) > 1 else ''
        if prop != 'weight':
            return val
        variants = val.get('variants') or []
        if variants and want not in [_s(v) for v in variants]:
            return None
        out = dict(val)
        out['weight'] = want
        return wrap(out)

    if name == 'font_face':
        # Shopify's font_face returns a BARE @font-face rule with no style
        # element around it. Stubbing it to '' meant the harness could never
        # see what happens when that text lands somewhere it must not, which
        # is exactly the production bug Phase 10 found in the layout.
        if val is None or val is BLANK or val == '':
            return ''
        fam = ''
        wt = ''
        if hasattr(val, 'get'):
            fam = _s(val.get('family') or '')
            wt = _s(val.get('weight') or '')
        fam = fam or 'Stub Family'
        wt = wt or '400'
        disp = ''
        for _k, _v in (named or {}).items():
            if _k == 'font_display':
                disp = '  font-display: ' + _s(_v) + ';'
        parts = ['@font-face {', '  font-family: ' + fam + ';',
                 '  font-weight: ' + wt + ';']
        if disp:
            parts.append(disp)
        parts.append("  src: url('stub.woff2') format('woff2');")
        parts.append('}')
        return chr(10).join(parts)
    if name == 'newline_to_br':
        return re.sub(r'\r?\n', '<br />' + chr(10), _s(val))
    if name == 'strip_html':
        return re.sub(r'<[^>]+>', '', _s(val))
    if name == 'truncate':
        n = int(pos[0]) if pos else 50
        t = _s(val)
        return t if len(t) <= n else t[:max(0, n - 3)] + '...'
    if name == 'within':
        return _s(val)

    # ------------------------------------------------------------- Phase 8
    # The product page and the cart reach for a wider slice of Liquid than the
    # editorial bands did. Everything below is added for those two templates.

    if name == 'json':
        return json.dumps(val, ensure_ascii=False, default=_jsonable)
    if name == 'money_with_currency':
        return _money(val) + ' ' + _s(env.engine.globals.get('currency') or 'PHP')
    if name == 'money_without_trailing_zeros':
        cents = int(_n(val) or 0)
        whole, frac = divmod(cents, 100)
        return '&#8369;{:,}'.format(whole) if frac == 0 else _money(val)
    if name == 'money_without_currency':
        cents = int(_n(val) or 0)
        whole, frac = divmod(cents, 100)
        return '{:,}.{:02d}'.format(whole, frac)
    if name == 'replace':
        return _s(val).replace(_s(pos[0]), _s(pos[1]) if len(pos) > 1 else '')
    if name == 'replace_first':
        return _s(val).replace(_s(pos[0]), _s(pos[1]) if len(pos) > 1 else '', 1)
    if name == 'remove':
        return _s(val).replace(_s(pos[0]), '')
    if name == 'split':
        return _s(val).split(_s(pos[0])) if _s(pos[0]) else list(_s(val))
    if name == 'first':
        return (val or [None])[0] if val else None
    if name == 'last':
        return (val or [None])[-1] if val else None
    if name == 'map':
        return [_index(x, _s(pos[0])) for x in (val or [])]
    if name == 'where':
        key = _s(pos[0])
        if len(pos) > 1:
            return [x for x in (val or []) if _eq(_index(x, key), pos[1])]
        return [x for x in (val or []) if not is_blank(_index(x, key))]
    if name == 'sort':
        key = _s(pos[0]) if pos else None
        return sorted(val or [], key=(lambda x: _index(x, key)) if key else (lambda x: x))
    if name == 'uniq':
        out = []
        for x in (val or []):
            if x not in out:
                out.append(x)
        return out
    if name == 'reverse':
        return list(reversed(val or []))
    if name == 'concat':
        return list(val or []) + list(pos[0] or [])
    if name == 'compact':
        return [x for x in (val or []) if not is_blank(x)]
    if name == 'slice':
        start = int(_n(pos[0]))
        length = int(_n(pos[1])) if len(pos) > 1 else 1
        return (val or [])[start:start + length] if isinstance(val, list) else _s(val)[start:start + length]
    if name == 'abs':
        return abs(_n(val))
    if name == 'at_least':
        return max(_n(val), _n(pos[0]))
    if name == 'at_most':
        return min(_n(val), _n(pos[0]))
    if name == 'ceil':
        return int(math.ceil(_n(val)))
    if name == 'floor':
        return int(math.floor(_n(val)))
    if name == 'modulo':
        return _n(val) % _n(pos[0])
    if name == 'lstrip':
        return _s(val).lstrip()
    if name == 'rstrip':
        return _s(val).rstrip()
    if name == 'strip_newlines':
        return re.sub(r'[\r\n]+', '', _s(val))
    if name == 'capitalize':
        s = _s(val)
        return s[:1].upper() + s[1:] if s else s
    if name == 'escape_once':
        return html.escape(html.unescape(_s(val)), quote=True)
    if name == 'url_encode':
        return quote_plus(_s(val))
    if name == 'url_escape':
        return quote(_s(val), safe='')
    if name == 'date':
        # 'now' and 'today' are Liquid's own inputs to this filter, evaluated at
        # render time. Returning the value unchanged made
        # sections/footer.liquid:133 (`assign year = 'now' | date: '%Y'`) print
        # the literal word, so every preview footer read "(c) now God Squad" --
        # visible on the page, and shipped that way for as long as the footer
        # has been rendered anywhere.
        if _s(val) in ('now', 'today'):
            return datetime.datetime.now().strftime(_s(pos[0]) if pos else '%Y')
        return _s(val)
    if name == 'script_tag':
        return '<script src="%s" type="text/javascript"></script>' % _s(val)
    if name == 'payment_button':
        # Shopify injects the real accelerated-checkout iframe here. The harness
        # cannot; it renders the container Shopify targets so the page's layout,
        # spacing and tab order can still be measured honestly. The markup is
        # labelled in the DOM so nothing mistakes it for the real button.
        return ('<div data-shopify="payment-button" class="shopify-payment-button"'
                ' data-harness-stub="payment-button">'
                '<button type="button" class="shopify-payment-button__button">'
                'Buy it now</button></div>')
    if name == 'link_to':
        return '<a href="%s">%s</a>' % (_s(pos[0]), _s(val))
    if name == 'external_video_url':
        # Shopify's own filter returns a URL that external_video_tag then
        # consumes. The harness keeps the media object flowing so the chain
        # reaches the tag filter intact; calling the two the wrong way round
        # still fails here, which is the mistake worth catching.
        return val
    if name in ('video_tag', 'media_tag', 'external_video_tag', 'model_viewer_tag'):
        return env.engine.media_tag(val, name, named)
    if name == 'structured_data':
        return env.engine.structured_data(val)
    if name == 'image_tag_stub':
        return ''
    if name == 'metafield_tag' or name == 'metafield_text':
        return _s(val)
    if name == 'inline_asset_content':
        return ''
    if name == 'weight_with_unit':
        return _s(val)
    if name == 'highlight_active_tag':
        return _s(val)
    if name == 'sort_natural':
        key = _s(pos[0]) if pos else None
        return sorted(val or [], key=(lambda x: _s(_index(x, key)).lower()) if key
                      else (lambda x: _s(x).lower()))
    raise LiquidError('unimplemented filter: %s' % name)


def _jsonable(o):
    """json.dumps fallback. Drop is already a dict; anything else the mock data
    carries is turned into a string rather than raising, so a stray object in a
    fixture surfaces in the output instead of killing the render."""
    if isinstance(o, dict):
        return dict(o)
    return _s(o)


def _s(v):
    if v is None or v is BLANK:
        return ''
    if v is True:
        return 'true'
    if v is False:
        return 'false'
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


def _n(v):
    if isinstance(v, bool):
        return 0
    if isinstance(v, (int, float)):
        return v
    try:
        return int(v)
    except (TypeError, ValueError):
        try:
            return float(v)
        except (TypeError, ValueError):
            return 0


# --------------------------------------------------------------------------- conditions
COMPARE = re.compile(r'^(.*?)\s+(==|!=|<>|>=|<=|>|<|contains)\s+(.*)$', re.S)


def truth(v):
    return not (v is None or v is False or v is BLANK)


def condition(env, expr):
    expr = expr.strip()
    for op, fn in (('or', any), ('and', all)):
        parts = _split_logic(expr, op)
        if len(parts) > 1:
            return fn(condition(env, p) for p in parts)
    m = COMPARE.match(expr)
    if not m:
        return truth(evaluate(env, expr))
    left, op, right = evaluate(env, m.group(1)), m.group(2), evaluate(env, m.group(3))
    if right is BLANK:
        return is_blank(left) if op == '==' else not is_blank(left)
    if left is BLANK:
        return is_blank(right) if op == '==' else not is_blank(right)
    if op == '==':
        return _eq(left, right)
    if op in ('!=', '<>'):
        return not _eq(left, right)
    if op == 'contains':
        try:
            return _s(right) in _s(left) if isinstance(left, str) else right in (left or [])
        except TypeError:
            return False
    l, r = _n(left), _n(right)
    return {'>': l > r, '<': l < r, '>=': l >= r, '<=': l <= r}[op]


def _eq(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return truth(a) == truth(b)
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a == b
    return _s(a) == _s(b)


def _split_logic(expr, op):
    parts, depth, cur, q = [], 0, '', None
    words = re.split(r'(\s+%s\s+)' % op, expr)
    if len(words) == 1:
        return [expr]
    out, buf = [], ''
    for w in words:
        if re.fullmatch(r'\s+%s\s+' % op, w):
            out.append(buf)
            buf = ''
        else:
            buf += w
    out.append(buf)
    return out


# --------------------------------------------------------------------------- engine
BLOCK_TAGS = {'if', 'unless', 'for', 'case', 'capture', 'comment', 'raw', 'style', 'schema', 'form', 'paginate'}


class Engine:
    def __init__(self, theme_root, globals_=None, translations=None, asset_base='assets/'):
        self.root = theme_root
        self.globals = globals_ or {}
        self.translations = translations or {}
        self.asset_base = asset_base
        self.missing_translations = []
        self.missing_interpolations = []
        self.image_requests = []

    # -- hooks the filters call
    def asset_url(self, name):
        return self.asset_base + name

    def image_url(self, img, named):
        if img is None:
            return ''
        src = img.get('src') if isinstance(img, (dict, Drop)) else str(img)
        w = named.get('width')
        self.image_requests.append((src, w))
        # Remembered so image_tag can emit width/height the way Shopify's own
        # filter does. The filter is handed a URL string, not the image, so it
        # has no other way to know the intrinsic size — and an <img> with no
        # dimensions is a layout-shift defect the harness must be able to see.
        if isinstance(img, (dict, Drop)):
            self._last_image = img
        return src

    # Attributes Shopify's image_tag understands that are NOT plain pass-through.
    IMAGE_TAG_SPECIAL = {'class', 'widths', 'sizes', 'alt', 'preload', 'width', 'height'}

    def image_tag(self, url, named):
        attrs = []
        cls = named.get('class')
        if cls:
            attrs.append('class="%s"' % cls)
        attrs.append('src="%s"' % url)
        if named.get('widths'):
            srcset = ', '.join('%s %sw' % (url, w.strip()) for w in _s(named['widths']).split(','))
            attrs.append('srcset="%s"' % srcset)
        if named.get('sizes'):
            attrs.append('sizes="%s"' % html.escape(_s(named['sizes']), quote=True))
        src_img = getattr(self, '_last_image', None)
        w = named.get('width') or (src_img.get('width') if src_img else None)
        h = named.get('height') or (src_img.get('height') if src_img else None)
        if w and h:
            attrs.append('width="%s"' % w)
            attrs.append('height="%s"' % h)
        for k, v in named.items():
            if k in self.IMAGE_TAG_SPECIAL or v in (None, False, BLANK, ''):
                continue
            attrs.append('%s="%s"' % (k, html.escape(_s(v), quote=True)))
        attrs.append('alt="%s"' % html.escape(_s(named.get('alt', '')), quote=True))
        return '<img %s>' % ' '.join(attrs)

    def structured_data(self, obj):
        """Shopify's structured_data filter, to the extent a harness can stand
        in for it: it emits schema.org JSON from the object's own fields and
        nothing else, so a theme that invented a rating or a review count could
        not hide it behind this. What Shopify emits exactly is Shopify's
        business; what is checkable here is that the theme emits it once, that
        it parses, and that every value in it came from product data."""
        if not isinstance(obj, (dict, Drop)):
            return '{}'
        offers = []
        for v in (obj.get('variants') or []):
            vid = _s(obj.get('url')) + '?variant=' + _s(v.get('id'))
            offers.append({
                '@type': 'Offer',
                '@id': vid,
                'availability': ('http://schema.org/InStock' if v.get('available')
                                 else 'http://schema.org/OutOfStock'),
                'price': '%.2f' % (_n(v.get('price')) / 100.0),
                'priceCurrency': 'PHP',
                'url': vid,
            })
        images = []
        for m in (obj.get('media') or []):
            prev = m.get('preview_image') if isinstance(m, (dict, Drop)) else None
            if prev:
                images.append(_s(prev.get('src')))
        doc = {
            '@context': 'http://schema.org/',
            '@type': 'ProductGroup' if len(offers) > 1 else 'Product',
            '@id': _s(obj.get('url')),
            'name': _s(obj.get('title')),
            'url': _s(obj.get('url')),
            'description': re.sub(r'<[^>]+>', '', _s(obj.get('description'))),
            'image': images,
            'brand': {'@type': 'Brand', 'name': _s(obj.get('vendor'))},
            'offers': offers,
        }
        return json.dumps(doc, ensure_ascii=False, indent=2)

    def media_tag(self, media, filter_name, named):
        """Shopify renders video, external video and 3D models through platform
        markup the harness cannot reproduce. It emits a labelled placeholder of
        the right shape so the gallery's layout can still be measured, and so a
        reviewer can see at a glance which slides are not real renders."""
        kind = (media.get('media_type') if isinstance(media, (dict, Drop)) else None) or filter_name
        cls = _s(named.get('class', ''))
        return ('<div class="%s" data-harness-stub="%s" data-media-type="%s"></div>'
                % (html.escape(cls, quote=True), html.escape(filter_name, quote=True),
                   html.escape(_s(kind), quote=True)))

    def translate(self, key, named):
        cur = self.translations
        for part in key.split('.'):
            if not isinstance(cur, dict) or part not in cur:
                self.missing_translations.append(key)
                return 'Translation missing: ' + key
            cur = cur[part]

        # Pluralisation: a key whose value is a dict of one/other is chosen by
        # the `count` argument, which is what Shopify does.
        if isinstance(cur, dict):
            count = _n(named.get('count', 0))
            form = 'one' if count == 1 else 'other'
            if form not in cur and 'other' in cur:
                form = 'other'
            if form not in cur:
                self.missing_translations.append(key + '.' + form)
                return 'Translation missing: ' + key
            cur = cur[form]

        # Interpolation. Shopify substitutes {{ name }} from the filter's named
        # arguments; without this the harness renders the placeholder and a
        # missing argument would never be noticed.
        def sub(m):
            name = m.group(1).strip()
            if name not in named:
                self.missing_interpolations.append(key + ':' + name)
                return m.group(0)
            return _s(named[name])

        return re.sub(r'\{\{\s*(\w+)\s*\}\}', sub, _s(cur))

    # -- rendering
    def render_file(self, relpath, extra=None):
        src = open('%s/%s' % (self.root, relpath), encoding='utf-8').read()
        return self.render(src, extra)

    def render(self, src, extra=None):
        scopes = [dict(self.globals)]
        if extra:
            scopes.append(dict(extra))
        env = Env(scopes, self)
        toks = _apply_whitespace_control(_tokenize(src))
        out, _ = self._block(env, toks, 0, None)
        return out

    def _block(self, env, toks, i, stop):
        """Render until one of `stop` tag-names. Returns (text, index_of_stop_tag)."""
        buf = []
        while i < len(toks):
            t = toks[i]
            if t[0] == 'text':
                buf.append(t[1])
                i += 1
                continue
            if t[0] == 'out':
                buf.append(_s(evaluate(env, t[1])))
                i += 1
                continue
            name = t[1].split()[0] if t[1].split() else ''
            if stop and name in stop:
                return ''.join(buf), i
            try:
                text, i = self._tag(env, toks, i)
            except _Loop as e:
                # Carry the text produced before break/continue, as Liquid does.
                e.text = ''.join(buf) + e.text
                raise
            buf.append(text)
        if stop:
            raise LiquidError('unclosed block, expected one of %s' % (stop,))
        return ''.join(buf), i

    def _tag(self, env, toks, i):
        stmt = toks[i][1]
        parts = stmt.split(None, 1)
        name = parts[0]
        rest = parts[1] if len(parts) > 1 else ''

        if name == 'comment':
            return '', self._skip_raw(toks, i, 'comment', 'endcomment') + 1
        if name == 'raw':
            j = self._skip_raw(toks, i, 'raw', 'endraw')
            return ''.join(t[1] for t in toks[i + 1:j] if t[0] == 'text'), j + 1
        if name == 'schema':
            return '', self._skip_raw(toks, i, 'schema', 'endschema') + 1
        if name == 'style':
            body, j = self._block(env, toks, i + 1, {'endstyle'})
            return '<style>%s</style>' % body, j + 1
        if name == 'assign':
            k, v = rest.split('=', 1)
            env.set_global(k.strip(), evaluate(env, v))
            return '', i + 1
        if name == 'capture':
            body, j = self._block(env, toks, i + 1, {'endcapture'})
            env.set_global(rest.strip(), body)
            return '', j + 1
        if name == 'echo':
            return _s(evaluate(env, rest)), i + 1
        if name == 'increment' or name == 'decrement':
            return '', i + 1
        if name == 'liquid':
            return self._liquid_block(env, rest), i + 1
        if name == 'render' or name == 'include':
            return self._render_snippet(env, rest), i + 1
        if name == 'section':
            return self.render_file('sections/%s.liquid' % _s(evaluate(env, rest))), i + 1
        if name == 'sections':
            return '', i + 1
        if name == 'if' or name == 'unless':
            return self._conditional(env, toks, i)
        if name == 'for':
            return self._for(env, toks, i)
        if name == 'case':
            return self._case(env, toks, i)
        if name == 'break' or name == 'continue':
            raise _Loop(name)
        if name == 'form':
            return self._form(env, toks, i, rest)
        if name == 'paginate':
            return self._paginate(env, toks, i, rest)
        raise LiquidError('unknown tag: %r' % stmt)

    # Shopify's {% form %} is not sugar for a <form> element: it also emits the
    # hidden inputs the platform's own handlers require, and the theme never
    # writes them. Rendering the element without them would let the harness
    # "pass" markup Shopify would reject, so they are emitted here too.
    FORM_ACTIONS = {
        'product': ('/cart/add', 'product'),
        'cart': ('/cart', 'cart'),
    }

    def _paginate(self, env, toks, i, rest):
        """{% paginate <path> by <n> %} ... {% endpaginate %}"""
        m = re.match(r'^(.+?)\s+by\s+(.+)$', rest.strip(), re.S)
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
        # _block returns the index OF the stop tag; step past endpaginate so the
        # dispatcher does not then try to execute it as a tag in its own right.
        return body, j + 1

    def _form(self, env, toks, i, rest):
        args = _split_commas(rest)
        kind = _s(evaluate(env, args[0])) if args else ''
        if kind not in self.FORM_ACTIONS:
            raise LiquidError('unsupported form kind: %r' % kind)
        action, form_type = self.FORM_ACTIONS[kind]

        attrs, subject = {}, None
        for a in args[1:]:
            km = re.match(r'^([\w:-]+)\s*:\s*(.*)$', a.strip(), re.S)
            if km:
                attrs[km.group(1)] = evaluate(env, km.group(2))
            else:
                subject = evaluate(env, a)

        body, j = self._block(env, toks, i + 1, {'endform'})

        out = ['<form method="post" action="%s" accept-charset="UTF-8"' % action]
        if kind == 'product':
            out.append(' enctype="multipart/form-data"')
        for k, v in attrs.items():
            if v is True:
                out.append(' %s="%s"' % (k, k))
            elif v not in (None, False, BLANK, ''):
                out.append(' %s="%s"' % (k, html.escape(_s(v), quote=True)))
        out.append('>')
        out.append('<input type="hidden" name="form_type" value="%s">' % form_type)
        out.append('<input type="hidden" name="utf8" value="✓">')
        out.append(body)
        out.append('</form>')
        env.set_global('_last_form_subject', subject)
        return ''.join(out), j + 1

    def _skip_raw(self, toks, i, opener, closer):
        """Index of the matching close tag, found lexically. The body is never
        evaluated, which is what makes a usage example inside a comment safe."""
        depth, k = 0, i + 1
        while k < len(toks):
            if toks[k][0] == 'tag':
                nm = toks[k][1].split()[0] if toks[k][1].split() else ''
                if nm == opener:
                    depth += 1
                elif nm == closer:
                    if depth == 0:
                        return k
                    depth -= 1
            k += 1
        raise LiquidError('unterminated %s' % opener)

    OPENERS = {'if', 'unless', 'for', 'case'}
    CLOSERS = {'endif': 'if', 'endunless': 'unless', 'endfor': 'for', 'endcase': 'case'}

    def _conditional(self, env, toks, i):
        """Render the winning branch, then resume after the matching end tag."""
        text = self._pick_branch(env, toks, i)
        return text, self._match_end(toks, i, {'endif', 'endunless'}) + 1

    def _pick_branch(self, env, toks, i):
        stmt = toks[i][1]
        name, rest = stmt.split(None, 1)
        cond, neg = rest, (name == 'unless')
        j = i
        while True:
            start = j + 1
            j = self._branch_end(toks, start)
            take = True if cond is None else (condition(env, cond) != neg)
            if take:
                text, _ = self._block(env, toks, start, {'elsif', 'else', 'endif', 'endunless'})
                return text
            nxt = toks[j][1].split(None, 1)
            if nxt[0] in ('endif', 'endunless'):
                return ''
            if nxt[0] == 'elsif':
                cond, neg = nxt[1], False
            else:
                cond, neg = None, False

    def _branch_end(self, toks, start):
        """Index of the next elsif/else/endif at this nesting level."""
        depth, k = 0, start
        while k < len(toks):
            if toks[k][0] == 'tag':
                nm = toks[k][1].split()[0]
                if nm in self.OPENERS:
                    depth += 1
                elif nm in self.CLOSERS:
                    if depth == 0:
                        return k
                    depth -= 1
                elif depth == 0 and nm in ('elsif', 'else'):
                    return k
            k += 1
        raise LiquidError('unterminated conditional')

    def _match_end(self, toks, i, enders):
        """Index of the end tag matching the opener at i."""
        depth, k = 0, i + 1
        while k < len(toks):
            if toks[k][0] == 'tag':
                nm = toks[k][1].split()[0]
                if nm in self.OPENERS:
                    depth += 1
                elif nm in self.CLOSERS:
                    if depth == 0:
                        if nm not in enders:
                            raise LiquidError('mismatched close: %s' % nm)
                        return k
                    depth -= 1
            k += 1
        raise LiquidError('unterminated block')

    def _for(self, env, toks, i):
        stmt = toks[i][1]
        m = re.match(r'^for\s+(\w+)\s+in\s+(.+?)(?:\s+limit:\s*(\S+))?$', stmt)
        if not m:
            raise LiquidError('bad for: %r' % stmt)
        var, srcexpr, limit = m.group(1), m.group(2), m.group(3)
        seq = evaluate(env, srcexpr) or []
        if limit:
            seq = list(seq)[: int(_n(evaluate(env, limit)))]
        seq = list(seq)
        end = self._match_end(toks, i, {'endfor'})
        body_toks = toks[i + 1: end]
        # PARENTLOOP. Shopify documents it as "the parent forloop object", nil
        # when the loop is not nested. Leaving it out did not throw — it
        # evaluated to empty, so `id_prefix | append: '-' | append:
        # forloop.parentloop.index` silently produced `prefix--1` instead of
        # `prefix-1-1`, and every filter group emitted the SAME element ids.
        # Three ids duplicated across eight checkboxes on the collection page,
        # which breaks every `<label for>` binding on it.
        #
        # The theme was correct the whole time; this interpreter was not. A gap
        # that renders as empty rather than raising is the dangerous kind,
        # because the output still looks plausible.
        parent = None
        for sc in reversed(env.scopes):
            if 'forloop' in sc:
                parent = sc['forloop']
                break

        out = []
        for idx, item in enumerate(seq):
            env.scopes.append({
                var: item,
                'forloop': Drop({'index': idx + 1, 'index0': idx, 'first': idx == 0,
                                 'last': idx == len(seq) - 1, 'length': len(seq),
                                 'rindex': len(seq) - idx, 'rindex0': len(seq) - idx - 1,
                                 'parentloop': parent}),
            })
            try:
                text, _ = self._block(env, body_toks, 0, None)
                out.append(text)
            except _Loop as e:
                env.scopes.pop()
                out.append(e.text)
                if e.kind == 'break':
                    break
                continue
            env.scopes.pop()
        return ''.join(out), end + 1

    def _case(self, env, toks, i):
        """{% case %} / {% when %} / {% else %} / {% endcase %}.

        Added in Phase 8: the product media gallery dispatches on
        media.media_type, which is the one place in the theme where a chain of
        elsifs would be the wrong shape.

        `when` accepts several values, separated by `or` or by commas, which is
        what Liquid itself allows."""
        m = re.match(r'^case\s+(.+)$', toks[i][1], re.S)
        if not m:
            raise LiquidError('bad case: %r' % toks[i][1])
        subject = evaluate(env, m.group(1))
        end = self._match_end(toks, i, {'endcase'})

        # The when/else tags at THIS nesting level, in order.
        marks, depth, k = [], 0, i + 1
        while k < end:
            if toks[k][0] == 'tag':
                nm = toks[k][1].split()[0]
                if nm in self.OPENERS:
                    depth += 1
                elif nm in self.CLOSERS:
                    depth -= 1
                elif depth == 0 and nm in ('when', 'else'):
                    marks.append((k, nm, toks[k][1]))
            k += 1
        marks.append((end, 'endcase', ''))

        for idx in range(len(marks) - 1):
            pos, nm, raw = marks[idx]
            nxt = marks[idx + 1][0]
            if nm == 'else':
                matched = True
            else:
                rest = raw.split(None, 1)
                if len(rest) < 2:
                    raise LiquidError('bad when: %r' % raw)
                options = [evaluate(env, part)
                           for part in re.split(r'\s+or\s+|,', rest[1]) if part.strip()]
                matched = any(_eq(subject, opt) for opt in options)
            if matched:
                text, _ = self._block(env, toks[pos + 1:nxt], 0, None)
                return text, end + 1
        return '', end + 1

    def _liquid_block(self, env, body):
        """The {% liquid %} shorthand: one statement per line.

        A comment block inside it spans several lines and its body is prose,
        not statements, so it is dropped before the lines become tags."""
        src, skipping = [], False
        for raw in body.split("\n"):
            l = raw.strip()
            if not l:
                continue
            head = l.split()[0]
            if skipping:
                if head == "endcomment":
                    skipping = False
                continue
            if head == "comment":
                skipping = True
                continue
            src.append("{%% %s %%}" % l)
        if skipping:
            raise LiquidError("unclosed comment inside a liquid block")
        return self._render_tokens(env, "".join(src))

    def _render_tokens(self, env, src):
        toks = _apply_whitespace_control(_tokenize(src))
        text, _ = self._block(env, toks, 0, None)
        return text

    def _render_snippet(self, env, rest):
        m = re.match(r"^'([^']+)'\s*(?:,\s*(.*))?$", rest.strip(), re.S)
        if not m:
            raise LiquidError('bad render: %r' % rest)
        name, argstr = m.group(1), m.group(2)
        scope = {}
        if argstr:
            for a in _split_commas(argstr):
                k, v = a.split(':', 1)
                scope[k.strip()] = evaluate(env, v)
        sub = Env([dict(self.globals), scope], self)
        return self._render_with(sub, 'snippets/%s.liquid' % name)

    def _render_with(self, env, relpath):
        src = open('%s/%s' % (self.root, relpath), encoding='utf-8').read()
        toks = _apply_whitespace_control(_tokenize(src))
        text, _ = self._block(env, toks, 0, None)
        return text


class _Loop(Exception):
    def __init__(self, kind):
        self.kind = kind
        self.text = ''
        super().__init__(kind)
