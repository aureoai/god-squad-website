import json,os,sys,re
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pngtool import read_png

S=os.path.dirname(os.path.abspath(__file__))
SH=os.path.join(S,'shots')
boxes=json.load(open(os.path.join(S,'boxes.json')))

def lin(c):
    c=c/255.0
    return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def L(rgb):
    r,g,b=rgb
    return 0.2126*lin(r)+0.7152*lin(g)+0.0722*lin(b)
def ratio(a,b):
    la,lb=L(a),L(b)
    if la<lb: la,lb=lb,la
    return (la+0.05)/(lb+0.05)
def parse(col):
    m=re.findall(r'[\d.]+',col)
    return (round(float(m[0])),round(float(m[1])),round(float(m[2])))

def inside(x,y,box):
    return box and box[0]<=x<box[2] and box[1]<=y<box[3]

def core_pixels(fg,bgimg,txtimg,box,exclude=None,tol=14):
    """pixels in box whose rendered colour is within tol of fg on every channel
       and that differ from the backdrop (so they are glyph, not coincidence)."""
    out=[]
    x0,y0,x1,y1=box
    x0=max(0,x0);y0=max(0,y0);x1=min(txtimg.w,x1);y1=min(txtimg.h,y1)
    for y in range(y0,y1):
        for x in range(x0,x1):
            if exclude and inside(x,y,exclude): continue
            t=txtimg.px(x,y)
            if abs(t[0]-fg[0])>tol or abs(t[1]-fg[1])>tol or abs(t[2]-fg[2])>tol: continue
            b=bgimg.px(x,y)
            if abs(b[0]-t[0])+abs(b[1]-t[1])+abs(b[2]-t[2])<12: continue
            out.append((x,y,b))
    return out

THRESH={'eyebrow':4.5,'h1':3.0,'accent':3.0,'scripture':4.5,'desc':4.5,'cta':4.5}
rows=[]
for w in sorted(boxes,key=int):
    r=boxes[w]
    txt=read_png(os.path.join(SH,'w%s.png'%w))
    bgi=read_png(os.path.join(SH,'bg%s.png'%w))
    targets=[('eyebrow',r['eyebrow'],parse(r['sEyebrow']['color']),None),
             ('h1',r['h1'],parse(r['sH1']['color']),r.get('accent')),
             ('accent',r.get('accent'),parse(r['sAccent']['color']) if r.get('sAccent') else None,None),
             ('scripture',r['scripture'],parse(r['sScripture']['color']),None),
             ('desc',r['desc'],parse(r['sDesc']['color']),None)]
    for name,box,fg,exc in targets:
        if not box or not fg: continue
        px=core_pixels(fg,bgi,txt,box,exc)
        if not px:
            rows.append((w,name,fg,0,None,None,None,'NO CORE PIXELS')); continue
        rs=sorted(ratio(fg,p[2]) for p in px)
        worst=rs[0]; p1=rs[max(0,int(len(rs)*0.01))]; med=rs[len(rs)//2]
        th=THRESH[name]
        rows.append((w,name,fg,len(px),round(worst,2),round(p1,2),round(med,2),
                     'PASS' if worst>=th else 'FAIL'))
print(f"{'w':>5} {'element':<10} {'fg':<16} {'px':>7} {'worst':>6} {'p1':>6} {'median':>7}  req  verdict")
for w,name,fg,n,worst,p1,med,v in rows:
    th=THRESH[name]
    print(f"{w:>5} {name:<10} {str(fg):<16} {n:>7} {str(worst):>6} {str(p1):>6} {str(med):>7}  {th:<4} {v}")
fails=[r for r in rows if r[7]!='PASS']
print()
print('FAILURES:',len(fails))
for f in fails: print('  ',f)
