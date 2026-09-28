# -*- coding: utf-8 -*-
"""A comment body must be SKIPPED, not rendered.

The theme's snippet headers contain usage examples such as
    {% render 'product-card', product: product %}
inside their {%- comment -%} block. Executing the body while scanning for
endcomment made product-card render itself forever.
"""
p = r"C:\Users\TEST\AppData\Local\Temp\claude\C--Users-TEST-OneDrive-Documents-GodSquad-Website\de238d03-508d-43ce-a377-210f71ff0033\scratchpad\phase6\miniliquid.py"
s = open(p, encoding='utf-8').read()

old = """        if name == 'comment':
            _, j = self._block(env, toks, i + 1, {'endcomment'})
            return '', j + 1
        if name == 'raw':
            body, j = self._block(env, toks, i + 1, {'endraw'})
            return body, j + 1
        if name == 'schema':
            _, j = self._block(env, toks, i + 1, {'endschema'})
            return '', j + 1"""

new = """        if name == 'comment':
            return '', self._skip_raw(toks, i, 'comment', 'endcomment') + 1
        if name == 'raw':
            j = self._skip_raw(toks, i, 'raw', 'endraw')
            return ''.join(t[1] for t in toks[i + 1:j] if t[0] == 'text'), j + 1
        if name == 'schema':
            return '', self._skip_raw(toks, i, 'schema', 'endschema') + 1"""

assert old in s, 'comment/raw/schema block not found'
s = s.replace(old, new, 1)

anchor = "    OPENERS = {'if', 'unless', 'for', 'case'}"
helper = '''    def _skip_raw(self, toks, i, opener, closer):
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

'''
assert anchor in s
s = s.replace(anchor, helper + anchor, 1)
open(p, 'w', encoding='utf-8', newline='').write(s)
print('comment/raw/schema now skip their bodies')
