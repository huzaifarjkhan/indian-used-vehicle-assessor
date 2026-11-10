#!/usr/bin/env python3
"""Regression test for the evidence-first full HTML report builder (stdlib only)."""
import json, subprocess, sys, tempfile
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
    assert all(real not in text for real in ('MH43X3630','MH01AE3833','MALBT51GR9M100186'))
    print('PASS: full investigation report generated with 134-point checklist, portal links and no real case data')
