# -*- coding: utf-8 -*-
import os, re, json, shutil, subprocess, sys, io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8',errors='replace')
HERE=os.path.dirname(os.path.abspath(__file__)); EDGE=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
VP=[[375,812],[390,844],[430,932],[480,1040],[768,1024],[834,1194],[1024,1366],[1440,900],[812,375]]
P=r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre><script>
var W=VPS,res={},i=0;
function step(){if(i>=W.length){document.getElementById('o').textContent='<<<'+JSON.stringify(res)+'>>>';document.title='DONE';return;}
 var p=W[i++],w=p[0],h=p[1],f=document.createElement('iframe');
 f.style.cssText='width:'+w+'px;height:'+h+'px;border:0;position:absolute;left:-9999px;top:0';f.src='home-cta.html';
 f.onload=function(){var d=f.contentDocument,win=f.contentWindow;
  var st=d.createElement('style');st.textContent='*,*::before,*::after{transition:none!important;animation:none!important}';d.head.appendChild(st);
  win.setTimeout(function(){
   function g(s,p){var e=d.querySelector(s);return e?win.getComputedStyle(e)[p]:null;}
   function b(s){var e=d.querySelector(s);if(!e)return null;var r=e.getBoundingClientRect();
     return Math.round(r.width)+'x'+Math.round(r.height);}
   var img=d.querySelector('.our-story__image');
   res[w+'x'+h]={inner:g('.our-story__inner','gridTemplateColumns'),
     media:b('.our-story__media'), body:b('.our-story__body'),
     bodyFs:g('.our-story__body p','fontSize'), bodyMax:g('.our-story__body','maxWidth'),
     values:g('.our-story__value-list','gridTemplateColumns'),
     valueW:b('.our-story__value-list > *'),
     imgSizes:img?img.getAttribute('sizes'):null,
     imgCur:img?(img.currentSrc||'').replace(/^.*width=?/,'w=').slice(0,18):null,
     order:(function(){var n=d.querySelector('.our-story__inner');if(!n)return null;
       return [].slice.call(n.children).map(function(c){return (c.className||'').split(' ')[0].replace('our-story__','');}).join(' > ');})()};
   f.remove();step();},240);};
 document.body.appendChild(f);}
step();</script>"""
open(os.path.join(HERE,'site','_story.html'),'w',encoding='utf-8').write(P.replace('VPS',json.dumps(VP)))
PR=os.path.join(HERE,'edge-story'); shutil.rmtree(PR,ignore_errors=True)
out=os.path.join(HERE,'story-dom.html')
subprocess.run([EDGE,'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check',
 '--user-data-dir='+PR,'--virtual-time-budget=60000','--window-size=1600,1100','--dump-dom',
 'http://127.0.0.1:8809/_story.html'],stdout=open(out,'w',encoding='utf-8'),stderr=subprocess.DEVNULL)
d=open(out,encoding='utf-8',errors='replace').read()
m=re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>',d,re.S)
if not m: print('NO READING'); raise SystemExit(1)
data=json.loads(m.group(1).replace('&quot;','"').replace('&amp;','&').replace('&lt;','<').replace('&gt;','>'))
print('%-11s %-26s %-12s %-12s %-6s %-22s %s' % ('viewport','inner columns','media','body','p','value columns','order'))
for k,r in data.items():
    print('%-11s %-26s %-12s %-12s %-6s %-22s %s' % (k, (r['inner'] or '-')[:26], r['media'] or '-',
          r['body'] or '-', r['bodyFs'] or '-', (r['values'] or '-')[:22], r['order'] or '-'))
print()
print('story image sizes attribute: %s' % data[list(data)[0]]['imgSizes'])
print('body max-width: %s' % data[list(data)[0]]['bodyMax'])
