#!/usr/bin/env python3
"""GP-departure backtest, signal 1: Form D related-person diffs across fund vintages.
For each firm: collect its Form D filings via EDGAR FTS, extract related persons + dates,
build per-person first/last-named timeline. A person present in earlier vintages but absent
from the newest = departure signal; compare against known departure dates."""
import json, re, time, urllib.request, urllib.parse, sys
from collections import defaultdict
UA = {'User-Agent': 'olympos research emrahyalaz@gmail.com'}
def get(u):
    for i in range(3):
        try: return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read().decode('utf-8','ignore')
        except Exception: time.sleep(2+2*i)
    return ''

FIRMS = {
 'Eniac': ('"Eniac"', 'Vic Singh', '2024-05'),
 'Susa Ventures': ('"Susa Ventures"', 'Leo Polovets', '2024-06'),
 'Bessemer': ('"Bessemer Venture Partners"', 'Ethan Kurzweil', '2024-06'),
 'Redpoint': ('"Redpoint"', 'Tomasz Tunguz', '2022-11'),
 'NEA': ('"New Enterprise Associates"', 'Vanessa Larco', '2025-03'),
 'Lightspeed': ('"Lightspeed Venture Partners"', 'Mercedes Bent', '2025-05'),
 'Founders Fund': ('"Founders Fund"', 'Brian Singerman', '2024-12'),
 'RRE': ('"RRE Ventures"', 'Jason Black', '2024-06'),
}
out = {}
for firm, (q, leaver, dep) in FIRMS.items():
    persons_timeline = defaultdict(list)   # person -> [(date, fund)]
    frm = 0; hits = []
    while frm < 60:
        qq = urllib.parse.urlencode({'q': q, 'forms': 'D', 'from': frm})
        d = json.loads(get(f'https://efts.sec.gov/LATEST/search-index?{qq}') or '{}')
        b = d.get('hits',{}).get('hits',[])
        if not b: break
        hits += b; frm += len(b)
        if frm >= d['hits']['total']['value']: break
        time.sleep(0.4)
    for h in hits:
        src = h['_source']; cik = src['ciks'][0]
        name = (src.get('display_names') or ['?'])[0].split('(CIK')[0].strip()
        accn = h['_id'].split(':')[0].replace('-','')
        xml = get(f'https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accn}/primary_doc.xml')
        time.sleep(0.12)
        for a,b2 in re.findall(r'<relatedPersonName>\s*<firstName>(.*?)</firstName>\s*(?:<middleName>.*?</middleName>\s*)?<lastName>(.*?)</lastName>', xml, re.S):
            if a.lower() in ('n/a','na',''): continue
            persons_timeline[f'{a} {b2}'.strip()].append((src.get('file_date',''), name))
    tl = {p: sorted(v) for p,v in persons_timeline.items()}
    # leaver analysis
    lv = [p for p in tl if leaver.split()[-1].lower() in p.lower()]
    rec = {'filings': len(hits), 'persons': len(tl), 'leaver_matches': {}}
    for p in lv:
        rec['leaver_matches'][p] = {'first': tl[p][0], 'last': tl[p][-1], 'n': len(tl[p])}
    # everyone's last-named date (for later use)
    rec['last_named'] = {p: tl[p][-1][0] for p in tl}
    out[firm] = rec
    lm = rec['leaver_matches']
    print(f"{firm:16} filings:{len(hits):3} | {leaver} (departed ~{dep}): " +
          (', '.join(f"last-named {v['last'][0]} on {v['last'][1][:38]}" for v in lm.values()) if lm else 'NEVER NAMED in Form Ds'))
json.dump(out, open('/Users/emrahyalaz/sourcing/t1-sensor/departure_backtest_formd.json','w'), indent=1, default=str)
print('\nsaved departure_backtest_formd.json')
