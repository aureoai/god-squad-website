import re,glob,os,collections
root=r"C:/Users/TEST/OneDrive/Documents/GodSquad Website/god-squad-theme"
def clean(txt):
    out=[];incom=False
    for l in txt.split('\n'):
        s=l;res=''
        while s:
            if incom:
                if '*/' in s: s=s.split('*/',1)[1];incom=False
                else: s='';break
            else:
                if '/*' in s: pre,rest=s.split('/*',1);res+=pre;s=rest;incom=True
                else: res+=s;s=''
        out.append(res)
    return '\n'.join(out)
rules=[]
for f in sorted(glob.glob(os.path.join(root,'assets','*.css'))):
    c=clean(open(f,encoding='utf-8').read())
    stack=[];buf='';i=0
    while i<len(c):
        ch=c[i]
        if ch=='{':
            head=' '.join(buf.split());buf=''
            stack.append((head,c[:i].count('\n')+1))
        elif ch=='}':
            if stack:
                head,ln=stack.pop()
                buf=''
        else: buf+=ch
        i+=1
    # simpler: regex innermost blocks
    for m in re.finditer(r'([^{}@]+)\{([^{}]*)\}', c):
        sel=' '.join(m.group(1).split())
        if not sel or sel.startswith('@'): continue
        ln=c[:m.start(1)].count('\n')+1
        decls=tuple(sorted(d.strip() for d in m.group(2).split(';') if d.strip()))
        rules.append((os.path.basename(f),ln,sel,decls))
byd=collections.defaultdict(list)
for f,ln,sel,d in rules:
    if len(d)>=3: byd[d].append((f,ln,sel))
print("### IDENTICAL DECLARATION BODIES (>=3 decls) IN >1 FILE")
for d,v in byd.items():
    if len({x[0] for x in v})>1:
        print("  DECLS:", "; ".join(d)[:200])
        for x in v: print("     ",x)
print()
print("### IDENTICAL DECLARATION BODIES (>=4 decls) repeated anywhere")
for d,v in byd.items():
    if len(v)>1 and len(d)>=4:
        print("  DECLS:", "; ".join(d)[:200])
        for x in v: print("     ",x)
