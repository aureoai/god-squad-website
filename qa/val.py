import json,re,os
def schema(path):
    s=open(path,encoding='utf-8').read()
    m=re.search(r'\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}', s, re.S)
    return json.loads(m.group(1))
tpl=json.load(open('templates/index.json',encoding='utf-8'))
for sid,sec in tpl['sections'].items():
    t=sec['type']
    p='sections/%s.liquid'%t
    if not os.path.exists(p):
        print('MISSING SECTION FILE', t); continue
    sc=schema(p)
    defs={}
    for st in sc.get('settings',[]):
        if 'id' in st: defs[st['id']]=st
    print('===',sid,'type',t)
    for k,v in sec.get('settings',{}).items():
        if k not in defs:
            print('  UNDECLARED SETTING:',k,'=',repr(v))
        else:
            d=defs[k]
            if d['type']=='select':
                vals=[o['value'] for o in d['options']]
                if v not in vals:
                    print('  BAD SELECT VALUE:',k,'=',repr(v),'allowed',vals)
            if d['type']=='checkbox' and not isinstance(v,bool):
                print('  BAD CHECKBOX:',k,v)
            if d['type']=='range':
                if not (d['min']<=v<=d['max']) or ((v-d['min'])%d['step']!=0):
                    print('  BAD RANGE:',k,v,d)
    btypes={b['type']:b for b in sc.get('blocks',[])}
    for bid,b in sec.get('blocks',{}).items():
        if b['type'] not in btypes:
            print('  UNDECLARED BLOCK TYPE:',b['type'])
        else:
            bdefs={x['id']:x for x in btypes[b['type']].get('settings',[]) if 'id' in x}
            for k,v in b.get('settings',{}).items():
                if k not in bdefs: print('  UNDECLARED BLOCK SETTING:',bid,k)
    for x in sec.get('block_order',[]):
        if x not in sec.get('blocks',{}): print('  block_order references missing block',x)
    print('  declared but unset:', [k for k in defs if k not in sec.get('settings',{})])
print('order:',tpl['order'], 'keys:',list(tpl['sections'].keys()))
