# -*- coding: utf-8 -*-
"""`break` must emit everything rendered before it.

The engine raised _Loop straight out of _block, which threw away the buffer
built so far. Real Liquid keeps it. This silently swallowed the product card's
swatch row, which looked like a theme bug and was not one.
"""
p = r"C:\Users\TEST\AppData\Local\Temp\claude\C--Users-TEST-OneDrive-Documents-GodSquad-Website\de238d03-508d-43ce-a377-210f71ff0033\scratchpad\phase6\miniliquid.py"
s = open(p, encoding='utf-8').read()

old = """            name = t[1].split()[0] if t[1].split() else ''
            if stop and name in stop:
                return ''.join(buf), i
            text, i = self._tag(env, toks, i)
            buf.append(text)"""
new = """            name = t[1].split()[0] if t[1].split() else ''
            if stop and name in stop:
                return ''.join(buf), i
            try:
                text, i = self._tag(env, toks, i)
            except _Loop as e:
                # Carry the text produced before break/continue, as Liquid does.
                e.text = ''.join(buf) + e.text
                raise
            buf.append(text)"""
assert old in s, 'block loop body not found'
s = s.replace(old, new, 1)

old2 = """class _Loop(Exception):
    def __init__(self, kind):
        self.kind = kind
        super().__init__(kind)"""
new2 = """class _Loop(Exception):
    def __init__(self, kind):
        self.kind = kind
        self.text = ''
        super().__init__(kind)"""
assert old2 in s
s = s.replace(old2, new2, 1)

old3 = """            try:
                text, _ = self._block(env, body_toks, 0, None)
                out.append(text)
            except _Loop as e:
                env.scopes.pop()
                if e.kind == 'break':
                    break
                continue
            env.scopes.pop()"""
new3 = """            try:
                text, _ = self._block(env, body_toks, 0, None)
                out.append(text)
            except _Loop as e:
                env.scopes.pop()
                out.append(e.text)
                if e.kind == 'break':
                    break
                continue
            env.scopes.pop()"""
assert old3 in s, 'for loop body not found'
s = s.replace(old3, new3, 1)

open(p, 'w', encoding='utf-8', newline='').write(s)
print('break/continue now preserve the text rendered before them')
