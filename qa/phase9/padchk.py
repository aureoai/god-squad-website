# -*- coding: utf-8 -*-
import os, re, json, shutil, subprocess, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE=os.path.dirname(os.path.abspath(__file__)); EDGE=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
P = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre><script>
var f=document.createElement('iframe');
f.style.cssText='width:375px;height:812px;border:0;position:absolute;left:-9999px;top:0';f.src='home-cart.html';
f.onload=function(){var d=f.contentDocument,w=f.contentWindow;
 var st=d.createElement('style');st.textContent='*,*::before,*::after{transition:none!important}';d.head.appendChild(st);
 w.setTimeout(function(){var b=d.querySelector('[data-cart-bubble]');if(b)b.click();
  w.setTimeout(function(){var r={};
   ['.cart-drawer__header','.cart-drawer__footer','.cart-drawer__scroller'].forEach(function(s){
     var e=d.querySelector(s);r[s]=e?w.getComputedStyle(e).paddingInlineEnd+' / start '+w.getComputedStyle(e).paddingInlineStart:'ABSENT';});
   var p=d.querySelector('.cart-drawer__panel');
   r['--drawer-pad-inline-end']=p?w.getComputedStyle(p).getPropertyValue('--drawer-pad-inline-end').trim():'-';
   var c=d.querySelector('.cart-drawer__close');
   r['close box']=c?JSON.stringify(c.getBoundingClientRect().toJSON&&['x','width'].map(function(k){return Math.round(c.getBoundingClientRect()[k]);})):'-';
   document.getElementById('o').textContent='<<<'+JSON.stringify(r)+'>>>';document.title='DONE';},300);},200);};
document.body.appendChild(f);</script>"""
open(os.path.join(HERE,'site','_pad.html'),'w',encoding='utf-8').write(P)
PR=os.path.join(HERE,'edge-pad'); shutil.rmtree(PR,ignore_errors=True)
out=os.path.join(HERE,'pad-dom.html')
subprocess.run([EDGE,'--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check',
 '--user-data-dir='+PR,'--virtual-time-budget=40000','--window-size=1200,900','--dump-dom',
 'http://127.0.0.1:8809/_pad.html'],stdout=open(out,'w',encoding='utf-8'),stderr=subprocess.DEVNULL)
d=open(out,encoding='utf-8',errors='replace').read()
m=re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>',d,re.S)
print('NO READING' if not m else json.dumps(json.loads(m.group(1).replace('&quot;','"').replace('&amp;','&')),indent=2))
