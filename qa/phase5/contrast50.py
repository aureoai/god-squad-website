import json,os,sys,re
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pngtool import read_png
S=os.path.dirname(os.path.abspath(__file__)); SH=os.path.join(S,'shots50')
boxes=json.load(open(os.path.join(S,'boxes50.json')))
def lin(c):
    c=c/255.0
    return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def L(p): return 0.2126*lin(p[0])+0.7152*lin(p[1])+0.0722*lin(p[2])
def ratio(a,b):
    la,lb=L(a),L(b)
    if la<lb: la,lb=lb,la
    return (la+0.05)/(lb+0.05)
def parse(c):
    m=re.findall(r'[\d.]+',c); return (round(float(m[0])),round(float(m[1])),round(float(m[2])))
def inside(x,y,b): return b and b[0]<=x<b[2] and b[1]<=y<b[3]
THRESH={'eyebrow':4.5,'h1 (cream)':3.0,'h1 accent (gold)':3.0,'scripture':4.5,'supporting':4.5}
out=[]
for w in sorted(boxes,key=int):
    r=boxes[w]
    txt=read_png(os.path.join(SH,'w%s.png'%w)); bgi=read_png(os.path.join(SH,'bg%s.png'%w))
    tgts=[('eyebrow',r['eyebrow'],parse(r['sEyebrow']['color']),None),
          ('h1 (cream)',r['h1'],parse(r['sH1']['color']),r.get('accent')),
          ('h1 accent (gold)',r.get('accent'),parse(r['sAccent']['color']) if r.get('sAccent') else None,None),
          ('scripture',r['scripture'],parse(r['sScripture']['color']),None),
          ('supporting',r['desc'],parse(r['sDesc']['color']),None)]
    for name,box,fg,exc in tgts:
        if not box or not fg: continue
        x0,y0,x1,y1=max(0,box[0]),max(0,box[1]),min(txt.w,box[2]),min(txt.h,box[3])
        glyph=[]; allbox=[]
        for y in range(y0,y1):
            for x in range(x0,x1):
                if exc and inside(x,y,exc): continue
                b=bgi.px(x,y); t=txt.px(x,y)
                allbox.append(ratio(fg,b))
                if abs(t[0]-b[0])+abs(t[1]-b[1])+abs(t[2]-b[2])>8:
                    glyph.append(ratio(fg,b))
        if not glyph: continue
        g=sorted(glyph); a=sorted(allbox)
        out.append(dict(w=int(w),el=name,fg='#%02X%02X%02X'%fg,n=len(g),
            glyph_worst=round(g[0],2),glyph_med=round(g[len(g)//2],2),
            box_worst=round(a[0],2),req=THRESH[name],
            verdict='PASS' if g[0]>=THRESH[name] else 'FAIL',
            box_verdict='PASS' if a[0]>=THRESH[name] else 'FAIL'))
json.dump(out,open(os.path.join(S,'contrast50.json'),'w'),indent=1)
print(f"{'w':>5} {'element':<17} {'fg':<8} {'glyphpx':>8} {'worst':>6} {'median':>7} | {'boxworst':>8} {'req':>4}  glyph  box")
for o in out:
    print(f"{o['w']:>5} {o['el']:<17} {o['fg']:<8} {o['n']:>8} {o['glyph_worst']:>6} {o['glyph_med']:>7} | {o['box_worst']:>8} {o['req']:>4}  {o['verdict']:<5}  {o['box_verdict']}")
print()
print('glyph failures:',sum(1 for o in out if o['verdict']!='PASS'))
print('box  failures:',sum(1 for o in out if o['box_verdict']!='PASS'))
for o in out:
    if o['box_verdict']!='PASS': print('   box fail:',o['w'],o['el'],o['box_worst'])
