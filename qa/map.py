import re,glob,os
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
srcs={}
for pat in ['sections/*.liquid','snippets/*.liquid','layout/*.liquid','assets/*.js']:
    for f in glob.glob(os.path.join(root,pat)):
        key=os.path.basename(os.path.dirname(f))+'/'+os.path.basename(f)
        srcs[key]=open(f,encoding='utf-8').read()
for f in sorted(glob.glob(os.path.join(root,'assets','*.css'))):
    base=os.path.basename(f)
    c=clean(open(f,encoding='utf-8').read())
    classes=sorted({m.group(1) for m in re.finditer(r'\.(-?[_a-zA-Z][\w-]*)',c)})
    print("###",base)
    for cl in classes:
        where=[k for k,v in srcs.items() if cl in v]
        print("   %-42s -> %s" % (cl, ", ".join(sorted(where)) if where else "**NONE**"))
