# -*- coding: utf-8 -*-
"""Extract the sizes attribute each grid section emits, for a matrix of inputs."""
import json, os, re, sys
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import build, surfaces
from miniliquid import wrap

CASES=[('main-collection',{'columns_desktop':4,'columns_tablet':2,'columns_mobile':2}),
       ('main-collection',{'columns_desktop':3,'columns_tablet':2,'columns_mobile':2}),
       ('main-collection',{'columns_desktop':2,'columns_tablet':2,'columns_mobile':1}),
       ('featured-collection',{'columns_desktop':4,'columns_tablet':2,'columns_mobile':2}),
       ('featured-collection',{'columns_desktop':3,'columns_tablet':2,'columns_mobile':2}),
       ('main-search',{'columns_desktop':4,'columns_tablet':2,'columns_mobile':2}),
       ('main-search',{'columns_desktop':3,'columns_tablet':2,'columns_mobile':2})]
CONTAINERS=[1200,1440,1800]

def sizes_of(section, overrides, container):
    base,_=surfaces.schema_defaults(section)
    base.update(overrides)
    g={'collection':surfaces.COLL,'search':surfaces.SEARCH_HITS}
    kw={}
    if section=='main-collection': kw['collection']=surfaces.COLL; tmpl='collection'
    elif section=='main-search': kw['search']=surfaces.SEARCH_HITS; tmpl='search'
    else: kw['collection']=surfaces.COLL; tmpl='index'
    e=surfaces.engine(template=tmpl,**kw)
    s=dict(e.globals['settings']); s['container_width']=container
    e.globals['settings']=wrap(s)
    if section=='featured-collection': base['collection']=surfaces.COLL
    html=build.render_section(e,'sections/%s.liquid'%section,'x',base)
    m=re.search(r'class="product-card__image"[^>]*sizes="([^"]+)"',html)
    if not m: m=re.search(r'sizes="([^"]+)"[^>]*class="product-card__image"',html)
    return m.group(1) if m else None

out={}
for section,ov in CASES:
    for c in CONTAINERS:
        key='%s|d%d t%d m%d|c%d'%(section,ov['columns_desktop'],ov['columns_tablet'],ov['columns_mobile'],c)
        try: out[key]=sizes_of(section,ov,c)
        except Exception as e: out[key]='ERROR: %s: %s'%(type(e).__name__,e)
print(json.dumps(out,indent=1))
