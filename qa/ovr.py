import re,glob,os,collections
root=r"C:/Users/TEST/OneDrive/Documents/GodSquad Website/god-squad-theme"
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
LOGICAL={'margin-block-start':'margin-top','margin-block-end':'margin-bottom','margin-inline-start':'margin-left','margin-inline-end':'margin-right',
'padding-block-start':'padding-top','padding-block-end':'padding-bottom','padding-inline-start':'padding-left','padding-inline-end':'padding-right',
'inset-block-start':'top','inset-block-end':'bottom','inset-inline-start':'left','inset-inline-end':'right',
'border-block-end':'border-bottom','border-block-start':'border-top','border-inline-start':'border-left','border-inline-end':'border-right'}
SHORT={'margin':['margin-top','margin-bottom','margin-left','margin-right'],
'padding':['padding-top','padding-bottom','padding-left','padding-right'],
'margin-block':['margin-top','margin-bottom'],'margin-inline':['margin-left','margin-right'],
'padding-block':['padding-top','padding-bottom'],'padding-inline':['padding-left','padding-right'],
'inset':['top','bottom','left','right'],'inset-block':['top','bottom'],'inset-inline':['left','right'],
'border':['border-top','border-bottom','border-left','border-right'],
'background':['background-color','background-image','background-position','background-size'],
'font':['font-size','font-family','font-weight','line-height'],'flex':['flex-grow','flex-shrink','flex-basis']}
def norm(p):
    p=p.strip().lower()
    return LOGICAL.get(p,p)
for f in sorted(glob.glob(os.path.join(root,'assets','*.css'))):
    c=clean(open(f,encoding='utf-8').read())
    seen=collections.defaultdict(list)
    for m in re.finditer(r'([^{}@]+)\{([^{}]*)\}', c):
        sel=' '.join(m.group(1).split())
        if not sel or sel.startswith('@'): continue
        # at-rule context
        before=c[:m.start(1)]
        at = 'media' if before.count('@media')>before.count('}')-before.count('{') else ''
        ln=before.count('\n')+1
        # crude media context: count braces
        depth=before.count('{')-before.count('}')
        ctx='MEDIA' if depth>0 else 'ROOT'
        for d in m.group(2).split(';'):
            if ':' not in d: continue
            p=norm(d.split(':',1)[0])
            props=SHORT.get(p,[p])
            for pp in props:
                seen[(sel,ctx,pp)].append((ln,d.strip()[:70]))
    out=[]
    for (sel,ctx,p),v in seen.items():
        if len(v)>1:
            lns=[x[0] for x in v]
            if len(set(lns))>1: out.append((lns[0],sel,ctx,p,v))
    if out:
        print("###",os.path.basename(f))
        for ln,sel,ctx,p,v in sorted(out):
            print("   ",sel,"|",ctx,"|",p)
            for x in v: print("        line",x[0],":",x[1])
