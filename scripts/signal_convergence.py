#!/usr/bin/env python3
"""Does the FoF's proposed manager roster invest in the founders Olympos signaled at stealth?
Stage 1: signaled founder (LinkedIn, dated) -> current company (Olympos profiles).
Stage 2: company -> investor list (Crunchbase via Olympos) -> match against the FoF roster.
Output: convergence table with dates, i.e. 'we flagged X in <month>; <manager> funded it <n> months later'.
Run: python3 signal_convergence.py <batch_json> ; resumable via cache."""
import json, os, sys, time
from pathlib import Path
CACHE = Path.home()/'sourcing/fof/backtests/convergence_cache.json'
cache = json.load(open(CACHE)) if CACHE.exists() else {'profile':{}, 'cb':{}}
ROSTER = ['Mei Z','Quiet Capital','JAM Fund','Justin Mateen','Humba','Soma Capital','Cota Capital',
          'Day One Ventures','SGH','Wischoff','Theory Ventures','Chemistry','Conviction','Kearny Jackson',
          'Basecase','Mischief','Category Ventures','Footwork','Pebblebed','Diffusion','Verdict','Boost VC',
          'Eniac','Susa','Marathon','Axiom','Pax Ventures','Orange Collective','Earthling','Perceptive','Outcast']
print('This module is the harness; enrichment is driven from the session via Olympos MCP in batches.')
print(f'roster terms: {len(ROSTER)}; cache at {CACHE}')
