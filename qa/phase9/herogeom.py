# -*- coding: utf-8 -*-
import os, re, json, shutil, subprocess, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__)); EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT, SITE, PROFILE = 8809, os.path.join(HERE, 'site'), os.path.join(HERE, 'edge-hg')
PAGEN='home-cta.html'
VP = [[812,375],[932,430],[667,375],[568,320],[812,342],[375,812],[430,932],[768,1024],[1440,900]]
P = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre><script>
var W = VPS, res = {}, i = 0;
function step(){ if(i>=W.length){document.getElementById('o').textContent='<<<'+JSON.stringify(res)+'>>>';document.title='DONE';return;}
 var p=W[i++],w=p[0],h=p[1],f=document.createElement('iframe');
 f.style.cssText='width:'+w+'px;height:'+h+'px;border:0;position:absolute;left:-9999px;top:0';f.src=PAGEN;
 f.onload=function(){var d=f.contentDocument,win=f.contentWindow;
  var st=d.createElement('style');st.textContent='*,*::before,*::after{transition:none!important;animation:none!important}';d.head.appendChild(st);
  win.setTimeout(function(){
   function b(s){var e=d.querySelector(s);if(!e)return null;var r=e.getBoundingClientRect();
     return [Math.round(r.top),Math.round(r.bottom),Math.round(r.height)];}
   var cta=d.querySelector('.hero__cta');
   res[w+'x'+h]={vh:h,hero:b('.hero'),inner:b('.hero__inner'),
     content:b('.hero__content'),cta:b('.hero__cta'),
     ctaHTML:cta?cta.outerHTML.slice(0,120):'ABSENT',
     desc:b('.hero__description'),
     offset:win.getComputedStyle(d.documentElement).getPropertyValue('--header-overlay-offset'),
     headerPos:(function(){var e=d.querySelector('.header');return e?win.getComputedStyle(e).position:null;})(),
     headerH:b('.header')};
   f.remove();step();},260);};
 document.body.appendChild(f);}
step();</script>"""
open(os.path.join(SITE,'_hg.html'),'w',encoding='utf-8').write(P.replace('VPS',json.dumps(VP)).replace('PAGEN',repr(PAGEN)))
shutil.rmtree(PROFILE, ignore_errors=True)
out=os.path.join(HERE,'hg-dom.html')
subprocess.run([EDGE,'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check',
 '--user-data-dir='+PROFILE,'--virtual-time-budget=60000','--window-size=1400,1000','--dump-dom',
 'http://127.0.0.1:%d/_hg.html'%PORT],stdout=open(out,'w',encoding='utf-8'),stderr=subprocess.DEVNULL)
d=open(out,encoding='utf-8',errors='replace').read()
m=re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>',d,re.S)
if not m: print('NO READING'); raise SystemExit(1)
data=json.loads(m.group(1).replace('&quot;','"').replace('&amp;','&').replace('&lt;','<').replace('&gt;','>'))
for k,r in data.items():
    print('=== %s   viewport height %d' % (k, r['vh']))
    print('   header  %-18s pos=%s  offset=%r' % (r['headerH'], r['headerPos'], r['offset'].strip()))
    for f in ('hero','inner','content','desc','cta'):
        v=r[f]
        tag='' 
        if v and f=='cta': tag = '   <-- BELOW FOLD' if v[1] > r['vh'] else '   <-- in view'
        print('   %-8s %s%s' % (f, v, tag))
    print('   cta html: %s' % r['ctaHTML'])
