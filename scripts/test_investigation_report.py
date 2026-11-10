#!/usr/bin/env python3
"""Regression test for the evidence-first full HTML report builder (stdlib only)."""
import json, re, subprocess, sys, tempfile
from pathlib import Path
root=Path(__file__).resolve().parent.parent
with tempfile.TemporaryDirectory() as tmp:
    output=Path(tmp)/'report.html'
    subprocess.run([sys.executable,str(root/'scripts/build_investigation_report.py'),
        '--data',str(root/'examples/anonymized-investigation-report.json'),'--output',str(output)],
        check=True, capture_output=True, text=True)
    text=output.read_text(encoding='utf-8')
    assert 'Record flags and unresolved verification' in text
    assert 'SAMPLE-PLATE' in text and 'SAMPLE-VIN-NOT-A-REAL-VIN' in text
    assert 'Official website field-by-field guide' in text
    assert text.count('data-check="') >= 134
    assert text.count('class="report-card"') >= 10
    assert not re.search(r'\bMH\d{2}[A-Z]{1,3}\d{4}\b', text), 'Report unexpectedly contains a live-format Maharashtra plate'
    print('PASS: full investigation report generated with 134-point checklist, portal links and no real case data')
