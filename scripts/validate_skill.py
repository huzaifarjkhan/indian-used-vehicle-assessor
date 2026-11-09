#!/usr/bin/env python3
"""Validate portable skill files, HTML completeness and exact no external resource dependency."""
from pathlib import Path
from collections import Counter
import json
import re

root=Path(__file__).resolve().parent.parent
checks=json.loads((root/'templates/checks.json').read_text(encoding='utf8'))
assert len(checks)>=125, 'Not enough checks'
assert len({x['id'] for x in checks})==len(checks),'Duplicate ids'
assert checks[0]['section'].startswith('RED-FLAG'), 'Red flags must come first'
assert all(x['description'] and x['title'] for x in checks)
html=(root/'output/Reusable_Used_Vehicle_Checklist.html').read_text(encoding='utf8')
assert html.lower().count('<select aria-label="status of ')==len(checks), 'Missing status dropdowns'
assert len(re.findall(r'data-check="V\d{3}" data-persist',html))==2*len(checks), 'Missing checklist controls'
assert '<script src=' not in html and '<link rel="stylesheet"' not in html, 'External resources found'
assert 'https://vahan.parivahan.gov.in/' in html
assert 'id="last4"' in html and 'id="last5"' in html
for f in ['SKILL.md','README.md','references/portals-india.md','references/photo-document-protocol.md','references/pricing-and-transaction.md','references/inspection-master.md','references/official-sources.md','templates/vehicle-data.json','templates/assessment-report.md','scripts/build_checklist.py']:
    assert (root/f).exists(),f'File missing: {f}'
print('PASS:', len(checks),'checks;',len({x['section'] for x in checks}),'sections;',html.count('href="https://'),'official links; no external JS/CSS.')