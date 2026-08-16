#!/usr/bin/env python3
"""For each company the FoF's managers bought since Mar-2024, pull its founders from Crunchbase.
Feeds the convergence test: did Olympos signal these founders at stealth before the manager invested?"""
import json, subprocess, glob, os, time, sys
os.environ.setdefault('CDP_PORT','9222')
SK=os.path.expanduser('~/skills'); CA=os.path.expanduser('~/.local/share/showrun/data/crunchbase-companies/cache')
OUT=os.path.expanduser('~/sourcing/fof/backtests/portfolio_founders.json')
cos=json.load(open('/private/tmp/claude-502/-Users-emrahyalaz/3522596e-a3a4-41b4-ad0b-9766c12afdc5/scratchpad/mgr_cos.json'))
done=json.load(open(OUT)) if os.path.exists(OUT) else {}
todo=[c for c in cos if c['permalink'] and c['permalink'] not in done]
print(f'{len(todo)} to fetch ({len(done)} cached)', flush=True)
for i,c in enumerate(todo):
    p=c['permalink']
    try:
        subprocess.run(['node','crunchbase/companies/scripts/crunchbase-companies.mjs','view',p],
                       cwd=SK, capture_output=True, text=True, timeout=90)
        f=f'{CA}/view-{p}.json'
        if os.path.exists(f):
            s=json.load(open(f))
            fo=[]
            def walk(o):
                if isinstance(o,dict):
                    for k,v in o.items():
                        if k=='founder_identifiers' and isinstance(v,list):
                            for x in v:
                                if isinstance(x,dict) and x.get('value'): fo.append({'name':x['value'],'permalink':x.get('permalink','')})
                        else: walk(v)
                elif isinstance(o,list):
                    for x in o: walk(x)
            walk(s)
            seen=set(); uf=[]
            for x in fo:
                if x['name'] not in seen: seen.add(x['name']); uf.append(x)
            done[p]={'company':c['name'],'date':c['date'],'mgr':c['mgr'],'founders':uf}
    except Exception as e:
        print(f'ERR {p}: {e}', file=sys.stderr, flush=True)
    if i%20==0:
        json.dump(done, open(OUT,'w'), indent=1)
        print(f'[{i+1}/{len(todo)}] {p}: {len(done.get(p,{}).get("founders",[]))} founders', flush=True)
    time.sleep(1.1)
json.dump(done, open(OUT,'w'), indent=1)
print(f'DONE {len(done)} companies -> {OUT}', flush=True)
