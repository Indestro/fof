#!/usr/bin/env python3
"""Weekly Gedik/Onur/Haluk watch: TR news RSS + GEDIK.IS price + KAP mentions.
Report -> fof repo partners/gedik/watch/, auto-commit+push, macOS notification on hits."""
import urllib.request, urllib.parse, re, os, json, datetime, subprocess, html

REPO = os.path.expanduser('~/sourcing/fof')
OUT = f'{REPO}/partners/gedik/watch'; os.makedirs(OUT, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (research)'}
today = datetime.date.today().isoformat()
QUERIES = ['"Gedik Yatırım"', '"Onur Topaç"', '"Haluk Nişli"', '"Gedik Portföy"', 'Gedik Yatırım fon']
seen_f = f'{OUT}/seen.json'
seen = set(json.load(open(seen_f))) if os.path.exists(seen_f) else set()

def get(u):
    try: return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read().decode('utf-8','ignore')
    except Exception: return ''

items = []
for q in QUERIES:
    u = 'https://news.google.com/rss/search?' + urllib.parse.urlencode({'q': f'{q} when:8d', 'hl':'tr','gl':'TR','ceid':'TR:tr'})
    xml = get(u)
    for m in re.finditer(r'<item><title>(.*?)</title><link>(.*?)</link><pubDate>(.*?)</pubDate>', xml, re.S):
        title, link, pub = html.unescape(m.group(1)), m.group(2), m.group(3)
        key = title[:80]
        if key in seen: continue
        seen.add(key)
        items.append({'q': q, 'title': title, 'link': link, 'pub': pub})

# GEDIK.IS weekly price context
px = ''
try:
    d = json.loads(get('https://query1.finance.yahoo.com/v8/finance/chart/GEDIK.IS?range=1mo&interval=1d'))
    cl = [c for c in d['chart']['result'][0]['indicators']['quote'][0]['close'] if c]
    if len(cl) > 5:
        wk = (cl[-1]/cl[-6]-1)*100; mo = (cl[-1]/cl[0]-1)*100
        px = f'GEDIK.IS: {cl[-1]:.2f} TL ({wk:+.1f}% 1w, {mo:+.1f}% 1mo)'
except Exception: px = 'GEDIK.IS: fetch failed'

rpt = [f'# Gedik watch — {today}', px, '']
for it in items:
    rpt.append(f"- [{it['q']}] {it['title']} ({it['pub'][:16]})\n  {it['link']}")
if not items: rpt.append('_No new items this week._')
open(f'{OUT}/watch-{today}.md','w').write('\n'.join(rpt))
json.dump(sorted(seen)[-500:], open(seen_f,'w'))
subprocess.run(['git','-C',REPO,'add','-A'], capture_output=True)
subprocess.run(['git','-C',REPO,'commit','-q','-m',f'gedik watch {today}: {len(items)} items'], capture_output=True)
subprocess.run(['git','-C',REPO,'push','-q'], capture_output=True)
print(f'{len(items)} new items; {px}')
if items:
    subprocess.run(['osascript','-e',f'display notification "{len(items)} new items — see fof repo" with title "GEDIK WATCH"'])
