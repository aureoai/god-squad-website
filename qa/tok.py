import re,glob,os
root=r"C:/Users/TEST/OneDrive/Documents/GodSquad Website/god-squad-theme"
dt=os.path.join(root,'assets','design-tokens.css')
txt=open(dt,encoding='utf-8').read()
def clean(t):
    out=[];incom=False
    for l in t.split('\n'):
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
c=clean(txt)
defs={}
for i,l in enumerate(c.split('\n'),1):
    m=re.match(r'\s*(--[\w-]+)\s*:',l)
    if m and m.group(1) not in defs: defs[m.group(1)]=i
others=[]
for pat in ['assets/*.css','assets/*.js','sections/*.liquid','snippets/*.liquid','layout/*.liquid','config/*.json']:
    others+=glob.glob(os.path.join(root,pat))
blob=''
for f in others:
    blob+=open(f,encoding='utf-8').read()
unused=[]
for t,ln in defs.items():
    # count var(--t) references anywhere
    n=len(re.findall(r'var\(\s*'+re.escape(t)+r'\s*[,)]', blob))
    if n==0: unused.append((ln,t))
print("defined in design-tokens.css:",len(defs))
print("NEVER referenced via var():",len(unused))
for ln,t in sorted(unused):
    src=txt.split('\n')[ln-1].strip()
    print(f"  {dt.split('/')[-1]}:{ln}  {src[:100]}")
