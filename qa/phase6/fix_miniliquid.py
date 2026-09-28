# -*- coding: utf-8 -*-
p = r"C:\Users\TEST\AppData\Local\Temp\claude\C--Users-TEST-OneDrive-Documents-GodSquad-Website\de238d03-508d-43ce-a377-210f71ff0033\scratchpad\phase6\miniliquid.py"
s = open(p, encoding='utf-8').read()

start = s.index("    def _conditional(self, env, toks, i):")
end = s.index("    def _for(self, env, toks, i):")

new = '''    OPENERS = {'if', 'unless', 'for', 'case'}
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

'''
s = s[:start] + new + s[end:]

# _for and its skipper now use the shared matcher.
s = s.replace(
    "        end = self._skip_to_end_generic(toks, i, {'endfor'}, {'for'})",
    "        end = self._match_end(toks, i, {'endfor'})")

old_generic = s.index("    def _skip_to_end_generic(self, toks, i, enders, openers):")
old_generic_end = s.index("    def _case(self, env, toks, i):")
s = s[:old_generic] + s[old_generic_end:]

# The unused double-render path in _render_snippet.
s = s.replace(
    """        sub = Env([dict(self.globals), scope], self)
        return self.render_file('snippets/%s.liquid' % name, scope) if False else \\
            self._render_with(sub, 'snippets/%s.liquid' % name)""",
    """        sub = Env([dict(self.globals), scope], self)
        return self._render_with(sub, 'snippets/%s.liquid' % name)""")

open(p, 'w', encoding='utf-8', newline='').write(s)
print('miniliquid cleaned')
