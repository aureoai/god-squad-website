# -*- coding: utf-8 -*-
p = r"C:\Users\TEST\AppData\Local\Temp\claude\C--Users-TEST-OneDrive-Documents-GodSquad-Website\de238d03-508d-43ce-a377-210f71ff0033\scratchpad\phase6\miniliquid.py"
s = open(p, encoding='utf-8').read()

marker = "    def _liquid_block(self, env, body):"
start = s.index(marker)
end = s.index("    def _render_tokens(self, env, src):")

new = '''    def _liquid_block(self, env, body):
        """The {% liquid %} shorthand: one statement per line.

        A comment block inside it spans several lines and its body is prose,
        not statements, so it is dropped before the lines become tags."""
        src, skipping = [], False
        for raw in body.split("\\n"):
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

'''
s = s[:start] + new + s[end:]
open(p, 'w', encoding='utf-8', newline='').write(s)
print("patched _liquid_block")
