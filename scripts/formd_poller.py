#!/usr/bin/env python3
"""Weekly EDGAR Form D poller — three consumers:
(a) FoF universe: new venture funds (esp. Fund I, <$200M) -> formd_universe.csv
(b) Fund-cycle: filings by the 29 live-T1 firms + Quiet/GPx -> fund_cycle_events.csv
(c) Angel->fund transitions: related persons matching our precursor/angel roster -> alerts
Runs weekly via launchd (com.t1sensor.formd). Idempotent: dedupes by accession number.
"""
import json, csv, os, re, time, urllib.request, urllib.parse, datetime, subprocess

D = os.path.expanduser('~/sourcing/t1-sensor')
OUT = f'{D}/formd'; os.makedirs(OUT, exist_ok=True)
UA = {'User-Agent': 'olympos research emrahyalaz@gmail.com'}
today = datetime.date.today()
start = (today - datetime.timedelta(days=9)).isoformat()   # 9d window, overlap-safe

def get(u, retry=3):
    for i in range(retry):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read().decode('utf-8','ignore')
        except Exception:
            time.sleep(3 + 3*i)
    return ''

seen_file = f'{OUT}/seen_accessions.txt'
seen = set(open(seen_file).read().split()) if os.path.exists(seen_file) else set()

# --- collect venture Form Ds in window (paginated FTS) ---
hits, frm = [], 0
while True:
    q = urllib.parse.urlencode({'q': '"Venture Capital Fund"', 'forms': 'D',
        'dateRange': 'custom', 'startdt': start, 'enddt': today.isoformat(), 'from': frm})
    d = json.loads(get(f'https://efts.sec.gov/LATEST/search-index?{q}') or '{}')
    batch = d.get('hits', {}).get('hits', [])
    if not batch: break
    hits += batch
    frm += len(batch)
    if frm >= min(d['hits']['total']['value'], 400): break
    time.sleep(0.5)
print(f'{len(hits)} venture Form D hits {start}..{today}')

# --- rosters for matching ---
t1 = {x['firm'].lower() for x in json.load(open(f'{D}/t1_live_list.json'))}
t1 |= {'quiet capital','gpx','google ventures','nventures','sequoia','a16z','andreessen'}
angels = set()
try:
    pre = json.load(open(f'{D}/precursors.json'))
    angels |= {k.lower() for k in pre.get('person', {})}
    angels |= {k.lower() for k in pre.get('org', {}) if ' ' in k and len(k.split()) == 2}
except Exception: pass
try:
    angels |= {k.lower() for k in json.load(open(f'{D}/quiet_coinvestors.json'))}
except Exception: pass
goldman = set()
try:
    norm = lambda s: re.sub(r'\b(ventures?|capital|partners?|fund|vc|lp|the)\b|\W', '', s.lower())
    goldman = {norm(x['fund']) for x in json.load(open(f'{D}/shai_goldman_funds.json'))}
except Exception: norm = lambda s: s.lower()

uni_rows, cycle_rows, alerts = [], [], []
for h in hits:
    src = h['_source']
    acc = h['_id'].split(':')[0]
    if acc in seen: continue
    seen.add(acc)
    cik = src['ciks'][0]
    name = (src.get('display_names') or ['?'])[0].split('(CIK')[0].strip()
    accn = acc.replace('-','')
    xml = get(f'https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accn}/primary_doc.xml')
    time.sleep(0.15)
    if not xml: continue
    offering = (re.search(r'<totalOfferingAmount>(.*?)</', xml) or [None,''])[1]
    sold = (re.search(r'<totalAmountSold>(.*?)</', xml) or [None,''])[1]
    persons = re.findall(r'<relatedPersonName>\s*<firstName>(.*?)</firstName>\s*(?:<middleName>.*?</middleName>\s*)?<lastName>(.*?)</lastName>', xml, re.S)
    pnames = [f'{a} {b}'.strip() for a,b in persons if a.lower() not in ('n/a','na','')]
    city = (re.search(r'<city>(.*?)</', xml) or [None,''])[1]
    is_amend = '<testOrLive>LIVE</testOrLive>' in xml and 'D/A' in src.get('file_type','') 
    # skip AngelList RUV/SPV mills and per-deal SPVs
    if re.search(r'roll ?up vehicles|series of .*(RUV|Rollups)|, a series of', name, re.I) and 'Fund' not in name.split(',')[0]:
        continue
    if city.lower() in ('lynnwood',) or re.match(r'^[A-Z]{2}-\d{4} ', name):
        continue
    row = {'filed': src.get('file_date'), 'fund': name, 'cik': cik, 'city': city,
           'offering': offering, 'sold': sold, 'persons': '; '.join(pnames), 'accession': acc}
    # (b) fund-cycle
    blob = (name + ' ' + ' '.join(pnames)).lower()
    if any(f in blob for f in t1):
        cycle_rows.append(row)
    # (c) angel transitions
    matched = [p for p in pnames if p.lower() in angels]
    if matched:
        alerts.append({**row, 'matched': ', '.join(matched)})
    # (a) universe: keep all; flag new-to-us
    row['in_goldman'] = norm(name) in goldman if goldman else ''
    uni_rows.append(row)

def append_csv(path, rows, fields):
    exists = os.path.exists(path)
    with open(path,'a',newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        if not exists: w.writeheader()
        w.writerows(rows)

F = ['filed','fund','cik','city','offering','sold','persons','in_goldman','accession']
append_csv(f'{OUT}/formd_universe.csv', uni_rows, F)
append_csv(f'{OUT}/fund_cycle_events.csv', cycle_rows, F[:-2]+['accession'])
open(seen_file,'w').write('\n'.join(seen))

rpt = [f'# Form D weekly — {today} (window {start}..)', f'{len(uni_rows)} new venture-fund filings']
if cycle_rows:
    rpt.append('\n## Fund-cycle events (T1/Quiet/GPx):')
    rpt += [f"- {r['filed']} {r['fund']} — offering {r['offering']}, sold {r['sold']} [{r['persons'][:80]}]" for r in cycle_rows]
if alerts:
    rpt.append('\n## ANGEL->FUND transitions (precursor roster match):')
    rpt += [f"- {r['filed']} {r['fund']} — {r['matched']} (offering {r['offering']})" for r in alerts]
new_f1 = [r for r in uni_rows if not r['in_goldman'] and (' I,' in r['fund'] or r['fund'].rstrip().endswith(' I') or 'Fund I' in r['fund'] or ' 1,' in r['fund'])]
if new_f1:
    rpt.append('\n## Likely Fund I, not on Goldman list:')
    rpt += [f"- {r['filed']} {r['fund']} ({r['city']}) offering {r['offering']} [{r['persons'][:70]}]" for r in new_f1[:20]]
report = '\n'.join(rpt)
open(f'{OUT}/report-{today}.md','w').write(report)
print(report)
if cycle_rows or alerts:
    msg = f'{len(cycle_rows)} fund-cycle, {len(alerts)} angel-transition'
    subprocess.run(['osascript','-e',f'display notification "{msg}" with title "FORM D POLLER"'])
