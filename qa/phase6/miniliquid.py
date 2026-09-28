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
import re, json, html


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
    if (tok.startswith('"') and tok.endswith('"')) or (tok.startswith("'") and tok.endswith("'")):
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
    return v is None or v is False or v == '' or v == [] or v == {}


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
    if name == 'font_face':
        return ''
    if name == 'within':
        return _s(val)
    raise LiquidError('unimplemented filter: %s' % name)


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
        return src

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
        for k in ('loading', 'fetchpriority', 'decoding'):
            if named.get(k):
                attrs.append('%s="%s"' % (k, named[k]))
        attrs.append('alt="%s"' % html.escape(_s(named.get('alt', '')), quote=True))
        return '<img %s>' % ' '.join(attrs)

    def translate(self, key, named):
        cur = self.translations
        for part in key.split('.'):
            if not isinstance(cur, dict) or part not in cur:
                self.missing_translations.append(key)
                return 'Translation missing: ' + key
            cur = cur[part]
        return cur

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
        if name in ('form', 'endform', 'paginate', 'endpaginate'):
            raise LiquidError('unimplemented tag: %s' % name)
        raise LiquidError('unknown tag: %r' % stmt)

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
        # evaluated to empty, so `forloop.parentloop.index` silently produced
        # `prefix--1` instead of `prefix-1-1`, and every filter group emitted
        # the SAME element ids. A gap that renders as empty rather than raising
        # is the dangerous kind: the output still looks plausible.
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
        raise LiquidError('case is not used by this theme; implement if that changes')

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
