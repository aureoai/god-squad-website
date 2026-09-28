# -*- coding: utf-8 -*-
"""The hero's header clearance, first vs demoted."""
import json, os, re, shutil, subprocess, sys
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
EDGE=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
P=r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre><script>
var PAGES=['home-cta.html','home-reordered.html'],res={},i=0;
function step(){if(i>=PAGES.length){document.getElementById('o').textContent='<<<'+JSON.stringify(res)+'>>>';document.title='DONE';return;}
 var p=PAGES[i++],f=document.createElement('iframe');
 f.style.cssText='width:1440px;height:900px;border:0;position:absolute;left:-9999px;top:0';f.src=p;
 f.onload=function(){var d=f.contentDocument,w=f.contentWindow;
  var st=d.createElement('style');st.textContent='*,*::before,*::after{transition:none!important}';d.head.appendChild(st);
  w.setTimeout(function(){
   var inner=d.querySelector('.hero__inner'), hero=d.querySelector('.hero');
   res[p]={padTop: inner?w.getComputedStyle(inner).paddingTop:null,
           clearance: hero?w.getComputedStyle(hero).getPropertyValue('--hero-header-clearance').trim():null,
           heroTop: hero?Math.round(hero.getBoundingClientRect().top):null};
   f.remove();step();},260);};
 document.body.appendChild(f);}
step();</script>"""
open(os.path.join(HERE,'site','_heropad.html'),'w',encoding='utf-8').write(P)
PR=os.path.join(HERE,'edge-heropad'); shutil.rmtree(PR,ignore_errors=True)
out=os.path.join(HERE,'heropad-dom.html')
subprocess.run([EDGE,'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check',
 '--user-data-dir='+PR,'--virtual-time-budget=40000','--window-size=1600,1000','--dump-dom',
 'http://127.0.0.1:8809/_heropad.html'],stdout=open(out,'w',encoding='utf-8'),stderr=subprocess.DEVNULL)
d=open(out,encoding='utf-8',errors='replace').read()
m=re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>',d,re.S)
if not m: print('NO READING'); raise SystemExit(1)
data=json.loads(m.group(1).replace('&quot;','"').replace('&amp;','&').replace('&lt;','<').replace('&gt;','>'))
for k,v in data.items(): print('%-24s padding-top=%-9s clearance=%-9s heroTop=%s' % (k,v['padTop'],v['clearance'] or '(0)',v['heroTop']))
