#!/bin/bash
# Tier-1 arrival charts: harvest Strebulaev top-30 deal tapes (local CB, no MCP), then founders.
for p in sequoia-capital andreessen-horowitz accel dst-global tiger-global-management index-ventures \
         lightspeed-venture-partners thrive-capital founders-fund iconiq-growth kleiner-perkins \
         new-enterprise-associates greylock benchmark bessemer-venture-partners khosla-ventures \
         general-catalyst ribbit-capital notable-capital ivp spark-capital; do
  echo "=== $p"
  python3 ~/sourcing/t1-sensor/harvest_investor_tape.py "$p" 2>&1 | tail -1
done
